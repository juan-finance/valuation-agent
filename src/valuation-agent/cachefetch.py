"""Polite, cached, parallel HTTP fetching: one fetch per URL per cache namespace, ever.

Why: the slowest part of a run is collecting the same market data again. Fetch once into
cache/<namespace>/, reuse across companies and sessions, and log provenance for source_log.csv.
Keep max_workers small and min_delay >= 1s per host; check each site's terms of use before bulk collection.
"""
from __future__ import annotations

import hashlib
import json
import threading
import time
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlparse

import requests


@dataclass
class FetchResult:
    url: str
    status: int | None
    body: bytes | None
    from_cache: bool
    fetched_at: str | None
    path: str | None
    error: str | None = None

    @property
    def ok(self) -> bool:
        return self.status is not None and 200 <= self.status < 300 and self.body is not None

    def text(self, encoding: str = "utf-8") -> str:
        return (self.body or b"").decode(encoding, errors="replace")


class CachedFetcher:
    def __init__(self, cache_dir: str | Path, max_workers: int = 4, min_delay: float = 1.0, ttl_days: float | None = None,
                 timeout: float = 30.0, retries: int = 3, user_agent: str = "valuation-agent/1.0 (academic project)",
                 session: requests.Session | None = None):
        self.dir = Path(cache_dir)
        self.dir.mkdir(parents=True, exist_ok=True)
        self.max_workers, self.min_delay, self.ttl, self.timeout, self.retries = max_workers, min_delay, ttl_days, timeout, retries
        self.session = session or requests.Session()
        self.session.headers.update({"User-Agent": user_agent})
        self._host_lock: dict[str, threading.Lock] = {}
        self._host_last: dict[str, float] = {}
        self._guard = threading.Lock()
        self.stats = {"hits": 0, "network": 0, "failures": 0}

    # -- paths
    def _base(self, url: str) -> Path:
        host = urlparse(url).netloc.replace(":", "_") or "local"
        d = self.dir / host
        d.mkdir(parents=True, exist_ok=True)
        return d / hashlib.sha1(url.encode()).hexdigest()

    def _fresh(self, meta: dict) -> bool:
        if self.ttl is None:
            return True
        age = (datetime.now(timezone.utc) - datetime.fromisoformat(meta["fetched_at"])).total_seconds() / 86400
        return age <= self.ttl

    def _throttle(self, host: str) -> None:
        with self._guard:
            lock = self._host_lock.setdefault(host, threading.Lock())
        with lock:
            wait = self._host_last.get(host, 0) + self.min_delay - time.time()
            if wait > 0:
                time.sleep(wait)
            self._host_last[host] = time.time()

    # -- API
    def get(self, url: str, force: bool = False) -> FetchResult:
        base = self._base(url)
        body_p, meta_p = base.with_suffix(".body"), base.with_suffix(".meta.json")
        if not force and body_p.exists() and meta_p.exists():
            meta = json.loads(meta_p.read_text())
            if self._fresh(meta):
                self.stats["hits"] += 1
                return FetchResult(url, meta["status"], body_p.read_bytes(), True, meta["fetched_at"], str(body_p))
        host, last_err, status = urlparse(url).netloc, None, None
        for attempt in range(self.retries):
            self._throttle(host)
            try:
                r = self.session.get(url, timeout=self.timeout)
                self.stats["network"] += 1
                status = r.status_code
                if status == 429 or status >= 500:
                    last_err = f"HTTP {status}"
                    time.sleep(min(2 ** attempt * max(self.min_delay, 1.0), 30))
                    continue
                if 200 <= status < 300:
                    ts = datetime.now(timezone.utc).isoformat(timespec="seconds")
                    body_p.write_bytes(r.content)
                    meta_p.write_text(json.dumps({"url": url, "status": status, "fetched_at": ts,
                                                  "sha256": hashlib.sha256(r.content).hexdigest(), "bytes": len(r.content)}))
                    return FetchResult(url, status, r.content, False, ts, str(body_p))
                self.stats["failures"] += 1
                return FetchResult(url, status, None, False, None, None, f"HTTP {status}")   # 4xx: not cached, not retried
            except requests.RequestException as e:
                last_err = str(e)
                time.sleep(min(2 ** attempt * max(self.min_delay, 1.0), 30))
        self.stats["failures"] += 1
        return FetchResult(url, status, None, False, None, None, last_err)

    def get_many(self, urls: list[str], force: bool = False) -> list[FetchResult]:
        """Parallel across hosts, serialised per host by min_delay. Returns results in input order."""
        with ThreadPoolExecutor(max_workers=self.max_workers) as ex:
            return list(ex.map(lambda u: self.get(u, force), urls))

    def manifest(self) -> list[dict]:
        """Provenance for every cached file: url, access date, sha256, bytes (feed source_log.csv access_date/locator)."""
        rows = []
        for p in sorted(self.dir.rglob("*.meta.json")):
            rows.append(json.loads(p.read_text()))
        return rows


def html_tables(html: bytes | str):
    """All <table>s of a page as DataFrames (pandas.read_html). Verify which table is which before relying on it."""
    import io
    import pandas as pd
    text = html.decode("utf-8", errors="replace") if isinstance(html, bytes) else html
    return pd.read_html(io.StringIO(text))
