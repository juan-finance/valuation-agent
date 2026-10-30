"""Download and parse the Damodaran industry/country datasets ONCE per vintage into tidy CSVs.

The procedures require the agent to verify the exact column and definition it uses: parse() therefore keeps every
original column, header_row and sheet name, and writes a manifest. Header detection looks for a key cell
('Industry Name' for industry files, 'Country' for ctryprem) instead of assuming a fixed row offset.
Untested against the live files from the build environment (no access): run `python -m valuation_agent.damodaran --selftest`
and then one real download, and fix header_key if a file differs.
"""
from __future__ import annotations

import hashlib
import io
import json
import re
from datetime import date
from pathlib import Path

import pandas as pd

BASE = "https://pages.stern.nyu.edu/~adamodar/pc/datasets/"
DATASETS = {   # name -> (url, header key); URLs from methodology/data_sources.md, verify they still resolve
    "ctryprem": ("https://www.stern.nyu.edu/~adamodar/pc/datasets/ctryprem.xlsx", "Country"),
    "dbtfundEurope": (BASE + "dbtfundEurope.xls", "Industry Name"),
    "capexEurope": (BASE + "capexEurope.xls", "Industry Name"),
    "wcdataEurope": (BASE + "wcdataEurope.xls", "Industry Name"),
    "betaEurope": (BASE + "betaEurope.xls", "Industry Name"),
}


def _norm(c) -> str:
    return re.sub(r"\s+", " ", str(c)).strip()


def parse(source: bytes | str | Path, header_key: str = "Industry Name", sheet: str | int | None = None):
    """Return (DataFrame, meta). Scans sheets (or the one given) for the first row containing header_key."""
    buf = io.BytesIO(source) if isinstance(source, (bytes, bytearray)) else source
    xl = pd.ExcelFile(buf)
    sheets = [sheet] if sheet is not None else xl.sheet_names
    for sh in sheets:
        raw = xl.parse(sh, header=None)
        for i in range(min(len(raw), 60)):
            if any(_norm(v).lower() == header_key.lower() for v in raw.iloc[i].tolist() if pd.notna(v)):
                hdr = [_norm(v) if pd.notna(v) else f"col{j}" for j, v in enumerate(raw.iloc[i].tolist())]
                body = raw.iloc[i + 1:].copy()
                body.columns = hdr
                key_col = next(c for c in hdr if c.lower() == header_key.lower())
                body = body[body[key_col].notna()].reset_index(drop=True)
                body = body.loc[:, [c for c in body.columns if not (c.startswith("col") and body[c].isna().all())]]
                return body, {"sheet": sh, "header_row": int(i), "columns": list(body.columns), "rows": int(len(body))}
    raise ValueError(f"header key '{header_key}' not found in {sheets}: open the file and set header_key/sheet explicitly")


def fetch_all(dest_root: str | Path, vintage: str | None = None, fetcher=None, names: list[str] | None = None) -> dict:
    """Download (cached) + parse every dataset into dest_root/<vintage>/<name>.csv and write manifest.json.
    Returns the manifest. Reuse the folder for every company valued on this vintage."""
    from .cachefetch import CachedFetcher
    vintage = vintage or date.today().isoformat()
    out = Path(dest_root) / vintage
    out.mkdir(parents=True, exist_ok=True)
    fetcher = fetcher or CachedFetcher(out / "_raw", max_workers=2, min_delay=1.0)
    manifest = {"vintage": vintage, "datasets": {}}
    for name in names or DATASETS:
        url, key = DATASETS[name]
        res = fetcher.get(url)
        if not res.ok:
            manifest["datasets"][name] = {"url": url, "error": res.error or f"HTTP {res.status}"}
            continue
        try:
            df, meta = parse(res.body, key)
        except Exception as e:   # keep going: report which file needs manual attention
            manifest["datasets"][name] = {"url": url, "error": f"parse failed: {e}"}
            continue
        df.to_csv(out / f"{name}.csv", index=False)
        manifest["datasets"][name] = {"url": url, "access_date": res.fetched_at, "sha256": hashlib.sha256(res.body).hexdigest(),
                                      **meta, "csv": f"{name}.csv"}
    (out / "manifest.json").write_text(json.dumps(manifest, indent=2))
    return manifest


def find_rows(df: pd.DataFrame, text: str, key_col: str | None = None, limit: int = 8) -> pd.DataFrame:
    """Case-insensitive substring/token match on the first (key) column; best matches first. Map each segment to
    its ACTUAL industry and state the mapping in dcf_decisions.md."""
    key_col = key_col or df.columns[0]
    toks = [t for t in re.split(r"\W+", text.lower()) if t]
    s = df[key_col].astype(str).str.lower()
    score = s.apply(lambda v: sum(t in v for t in toks) + (2 if text.lower() in v else 0))
    return df.assign(_score=score)[score > 0].sort_values("_score", ascending=False).drop(columns="_score").head(limit)


if __name__ == "__main__":   # python -m valuation_agent.damodaran --selftest | --fetch <dest_root> [vintage]
    import sys
    if "--selftest" in sys.argv:
        from openpyxl import Workbook
        wb = Workbook(); ws = wb.active; ws.title = "Industry Averages"
        ws.append(["Data used: 2026"]); ws.append([]); ws.append(["Industry Name", "Number of firms", "Beta"])
        ws.append(["Utility (General)", 12, 0.45]); ws.append(["Power", 30, 0.7]); ws.append([None, None, None])
        bio = io.BytesIO(); wb.save(bio)
        df, meta = parse(bio.getvalue(), "Industry Name")
        assert list(df["Industry Name"]) == ["Utility (General)", "Power"] and meta["header_row"] == 2, (df, meta)
        print("selftest ok", meta)
    elif "--fetch" in sys.argv:
        i = sys.argv.index("--fetch")
        m = fetch_all(sys.argv[i + 1], sys.argv[i + 2] if len(sys.argv) > i + 2 else None)
        print(json.dumps(m, indent=2))
