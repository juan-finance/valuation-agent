"""Parse the Damodaran datasets supplied as Markdown (tables, header metadata, numbers, dates).

Conversion rules (kept auditable: the original text is always retained next to the converted value):
  '33.09%' -> 0.3309 (decimal, unit 'pct');  '$1,252.30' / '-$3.70' -> number (unit 'usd');  '0.92' -> number;
  'NA' / '' -> NaN. Columns where >= 80% of the non-NA cells parse become numeric; others stay text.
"""
from __future__ import annotations

import math
import re
from dataclasses import dataclass, field
from pathlib import Path

import pandas as pd

_MONTHS = {"ene": 1, "jan": 1, "feb": 2, "mar": 3, "abr": 4, "apr": 4, "may": 5, "jun": 6, "jul": 7, "ago": 8, "aug": 8,
           "sep": 9, "set": 9, "oct": 10, "nov": 11, "dic": 12, "dec": 12,
           "january": 1, "february": 2, "march": 3, "april": 4, "june": 6, "july": 7, "august": 8, "september": 9,
           "october": 10, "november": 11, "december": 12}


@dataclass
class MDTable:
    context: str                 # nearest preceding heading
    header: list[str]
    rows: list[list[str]]
    start_line: int
    raw_rows: list[list[str]] = field(default_factory=list)


def clean_cell(s: str) -> str:
    return re.sub(r"\s+", " ", s.replace("**", "").replace("\\_", "_")).strip()


def to_number(cell: str):
    """Return (value, unit) or None if the cell is not numeric. unit in {'pct','usd','number','na'}."""
    c = clean_cell(cell).replace("$", "").replace(",", "")
    if c.upper() in ("NA", "N/A", "", "-"):
        return (math.nan, "na")
    pct = c.endswith("%")
    c2 = c[:-1] if pct else c
    try:
        v = float(c2)
    except ValueError:
        return None
    usd = "$" in cell
    return (v / 100.0, "pct") if pct else (v, "usd" if usd else "number")


def parse_tables(text: str) -> list[MDTable]:
    lines = text.splitlines()
    tables, heading, i = [], "", 0
    while i < len(lines):
        ln = lines[i]
        if ln.startswith("#"):
            heading = ln.lstrip("#").strip()
        if ln.lstrip().startswith("|") and i + 1 < len(lines) and re.match(r"^\s*\|[\s:\-|]+\|\s*$", lines[i + 1]):
            hdr = [clean_cell(c) for c in ln.strip().strip("|").split("|")]
            j, rows = i + 2, []
            while j < len(lines) and lines[j].lstrip().startswith("|"):
                cells = [c.strip() for c in lines[j].strip().strip("|").split("|")]
                if len(cells) == len(hdr):
                    rows.append(cells)
                j += 1
            tables.append(MDTable(heading, hdr, [[clean_cell(c) for c in r] for r in rows], i + 1, rows))
            i = j
            continue
        i += 1
    return tables


def to_frame(t: MDTable, numeric: bool = True):
    """DataFrame with converted columns plus a {column: unit} map. Raw text kept in df.attrs['raw']."""
    raw = pd.DataFrame(t.rows, columns=t.header)
    out, units = pd.DataFrame(index=raw.index), {}
    for col in raw.columns:
        conv = [to_number(v) for v in raw[col]]
        real = [c for c in conv if c is not None and c[1] != "na"]
        non_na = [v for v, c in zip(raw[col], conv) if clean_cell(v).upper() not in ("NA", "N/A", "", "-")]
        if numeric and non_na and len(real) / len(non_na) >= 0.8:
            out[col] = [c[0] if c is not None else math.nan for c in conv]
            kinds = {c[1] for c in real}
            units[col] = "pct" if kinds == {"pct"} else ("usd" if "usd" in kinds else "number")
        else:
            out[col] = raw[col].values
            units[col] = "text"
    out.attrs["raw"], out.attrs["units"] = raw, units
    return out, units


def parse_date(s: str):
    """Find dates in free text: '5-ene-26', '1-Jul-26', 'July 9, 2026', 'January 2026'.
    Returns list of ISO strings (YYYY-MM-DD; month-only dates use day 01)."""
    found = []
    for d, m, y in re.findall(r"\b(\d{1,2})[-/ ]([A-Za-z]{3,9})[-/ ,]*(\d{2,4})\b", s):
        mo = _MONTHS.get(m.lower())
        if mo:
            yy = int(y) + (2000 if int(y) < 100 else 0)
            found.append(f"{yy:04d}-{mo:02d}-{int(d):02d}")
    for m, d, y in re.findall(r"\b([A-Za-z]{3,9})\s+(\d{1,2}),\s*(\d{4})\b", s):
        mo = _MONTHS.get(m.lower())
        if mo:
            found.append(f"{int(y):04d}-{mo:02d}-{int(d):02d}")
    for m, y in re.findall(r"\b([A-Za-z]{3,9})\s+(\d{4})\b", s):
        mo = _MONTHS.get(m.lower())
        if mo and not any(f.startswith(f"{int(y):04d}-{mo:02d}") for f in found):
            found.append(f"{int(y):04d}-{mo:02d}-01")
    return sorted(set(found))


def extract_meta(text: str) -> dict:
    """Title (first '# ' heading), '**Key:** value' lines, and the dates found on any 'date' line (latest = as_of)."""
    meta = {"title": "", "fields": {}, "dates_found": [], "as_of_date": None}
    for ln in text.splitlines():
        if ln.startswith("# ") and not meta["title"]:
            meta["title"] = ln[2:].strip()
        m = re.match(r"^\*\*([^*]+?):\*\*\s*(.*)$", ln.strip())
        if m:
            meta["fields"][m.group(1).strip()] = m.group(2).strip()
        if re.search(r"date|updated|\*\*(January|February|March|April|May|June|July|August|September|October|November|December)", ln, re.I):
            meta["dates_found"] += parse_date(ln)
    for ln in text.splitlines()[:8]:                       # 'January 2026' style stand-alone lines
        if re.fullmatch(r"\*\*[A-Za-z]+ \d{4}\*\*", ln.strip()):
            meta["dates_found"] += parse_date(ln.strip("* "))
    meta["dates_found"] = sorted(set(meta["dates_found"]))
    meta["as_of_date"] = meta["dates_found"][-1] if meta["dates_found"] else None
    return meta


def read(path) -> str:
    return Path(path).read_text(encoding="utf-8")
