"""Stage 1 anomaly check (valuation-1-data-sourcing step 5)."""
from __future__ import annotations

import numpy as np
import pandas as pd


def anomaly_table(data: pd.DataFrame, threshold: float = 0.30, flag_on: str = "yoy") -> pd.DataFrame:
    """data: rows = line items, columns = fiscal years in chronological order (ideally 5).
    For each item/year returns YoY change and deviation from the multi-year average, using abs() in denominators so
    negative bases give a signed, interpretable change. flag_on='yoy' (default, reading of 'flag changes above +/-30%')
    or 'either' (also flag deviation from the 5-year average). Both measures are always reported.
    Flags are the START of the investigation (write them to anomaly_report.md first, then search news/annual report)."""
    if flag_on not in ("yoy", "either"):
        raise ValueError("flag_on must be 'yoy' or 'either'")
    rows = []
    cols = list(data.columns)
    for item, s in data.iterrows():
        avg = np.nanmean(s.to_numpy(dtype=float))
        for i, year in enumerate(cols):
            v = s[year]
            if pd.isna(v):
                rows.append((item, year, v, np.nan, np.nan, False, "missing value"))
                continue
            prev = s[cols[i - 1]] if i > 0 else np.nan
            yoy = (v - prev) / abs(prev) if pd.notna(prev) and prev != 0 else np.nan
            dev = (v - avg) / abs(avg) if avg != 0 else np.nan
            f_yoy = bool(pd.notna(yoy) and abs(yoy) > threshold)
            f_dev = bool(pd.notna(dev) and abs(dev) > threshold)
            flagged = f_yoy or (flag_on == "either" and f_dev)
            note = []
            if pd.isna(yoy) and i > 0:
                note.append("YoY undefined (prior value zero/missing)")
            if f_dev and not f_yoy:
                note.append("deviation from average only")
            rows.append((item, year, float(v), yoy, dev, flagged, "; ".join(note)))
    return pd.DataFrame(rows, columns=["item", "year", "value", "yoy_change", "dev_from_avg", "flag", "note"])


def to_markdown(table: pd.DataFrame, only_flags: bool = True) -> str:
    t = table[table["flag"]] if only_flags else table
    if t.empty:
        return "No line item exceeded the threshold.\n"
    lines = ["| item | year | value | YoY | vs 5y avg | cause / decision (fill) |", "|---|---|---:|---:|---:|---|"]
    for r in t.itertuples():
        fm = lambda x: "n/a" if pd.isna(x) else f"{x:+.1%}"
        lines.append(f"| {r.item} | {r.year} | {r.value:,.2f} | {fm(r.yoy_change)} | {fm(r.dev_from_avg)} |  |")
    return "\n".join(lines) + "\n"
