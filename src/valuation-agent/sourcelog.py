"""source_log.csv: the 21-field schema of methodology/data_sources.md, written and validated by code."""
from __future__ import annotations

import csv
import os
from pathlib import Path

FIELDS = ["input_id", "company", "metric", "value", "unit", "currency", "period_start", "period_end", "as_of_date",
          "publication_date", "access_date", "source_name", "url_or_local_file", "page_note_sheet_cell", "dataset_vintage",
          "reported_or_adjusted", "consolidation_scope", "method_or_formula", "cross_check_source", "status", "limitation"]
STATUSES = {"sourced", "derived", "estimated", "unavailable", "unverified"}
# stage 3 may append these (data_sources.md 'Stage 3 evidence and audit additions')
STAGE3_EXTRA = ["method", "entity_id", "target_ticker", "field_id", "price_date", "earnings_basis", "gics_level",
                "universe_vintage", "source_route", "raw_value", "normalized_value", "transformation", "review_status"]


class SourceLog:
    """Append-only writer. Missing fields become 'n/a' (never dropped). Existing rows and extra columns are preserved."""

    def __init__(self, path: str | os.PathLike):
        self.path = Path(path)
        self.extra: list[str] = []
        self.rows: list[dict] = []
        if self.path.exists():
            with open(self.path, newline="", encoding="utf-8") as fh:
                r = csv.DictReader(fh)
                self.rows = list(r)
                self.extra = [c for c in (r.fieldnames or []) if c not in FIELDS]

    @property
    def columns(self) -> list[str]:
        return FIELDS + self.extra

    def add(self, **kw) -> str:
        unknown = [k for k in kw if k not in FIELDS and k not in STAGE3_EXTRA and k not in self.extra]
        if unknown:
            raise KeyError(f"unknown source_log field(s): {unknown}")
        for k in kw:
            if k not in FIELDS and k not in self.extra:
                self.extra.append(k)
        row = {c: kw.get(c, "n/a") if kw.get(c) not in (None, "") else "n/a" for c in FIELDS + self.extra}
        if row["input_id"] == "n/a":
            row["input_id"] = f"IN{len(self.rows) + 1:04d}"
        if any(r["input_id"] == row["input_id"] for r in self.rows):
            raise ValueError(f"duplicate input_id {row['input_id']}: replacements are new rows that reference the old id")
        self.rows.append(row)
        return row["input_id"]

    def save(self) -> None:
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.path, "w", newline="", encoding="utf-8") as fh:
            w = csv.DictWriter(fh, fieldnames=self.columns, extrasaction="ignore")
            w.writeheader()
            for r in self.rows:
                w.writerow({c: r.get(c, "n/a") for c in self.columns})


def validate(path: str | os.PathLike) -> list[str]:
    """Return problems: missing columns, empty cells, bad status, duplicate ids, sourced rows without a locator."""
    problems = []
    with open(path, newline="", encoding="utf-8") as fh:
        r = csv.DictReader(fh)
        missing = [c for c in FIELDS if c not in (r.fieldnames or [])]
        if missing:
            problems.append(f"missing columns: {missing}")
        seen = set()
        for i, row in enumerate(r, start=2):
            rid = row.get("input_id", "")
            if rid in seen:
                problems.append(f"line {i}: duplicate input_id {rid}")
            seen.add(rid)
            for c in FIELDS:
                if c in row and (row[c] is None or row[c].strip() == ""):
                    problems.append(f"line {i}: empty '{c}' (write n/a)")
            st = (row.get("status") or "").strip()
            if st not in STATUSES:
                problems.append(f"line {i}: status '{st}' not in {sorted(STATUSES)}")
            if st == "sourced" and (row.get("url_or_local_file") in ("n/a", "", None) or row.get("page_note_sheet_cell") in ("n/a", "", None)):
                problems.append(f"line {i}: sourced input needs url_or_local_file AND page_note_sheet_cell (exact locator)")
    return problems
