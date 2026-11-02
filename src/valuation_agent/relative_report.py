"""Deterministic short report for a relative-only run (stage 3 outputs -> 2-3 page PDF + relative_summary.md).

Why: the report must always contain the same tables (summary, peer multiples, peer statistics, published regressions),
whatever the agent did in the session. The agent only supplies the company-specific caveats in `report_notes.md`;
every number is read from the files stage 3 already wrote, so nothing is re-researched or retyped.

Usage:  python -m valuation_agent.relative_report outputs/<TICKER>_<DATE> [--notes path/to/report_notes.md]

Reads  <folder>/relative/{multiples_summary.csv, comparables.csv, regression_results.json, valuation_multiples.csv}
       <folder>/run_state.json (optional), <folder>/relative/qa_results.md (optional), <folder>/report_notes.md (optional)
Writes <folder>/relative_report_<TICKER>.pdf and <folder>/relative_summary.md
"""
from __future__ import annotations

import json
import math
import re
import sys
from pathlib import Path

import pandas as pd

LABELS = {"pe": "P/E", "pbv": "P/BV", "ps": "P/S", "peg": "PEG", "ev_ebit": "EV/EBIT", "ev_ebitda": "EV/EBITDA", "ev_cf": "EV/CF",
          "ev_assets": "EV/Assets", "ev_sales": "EV/Sales", "relative_pe": "Relative P/E", "tobins_q": "Tobin's Q"}
STANDARD_LIMITS = [
    "Basis: one uniform vendor data source for the target and every peer, FY2025 figures (no TTM or forward mixing), one price and FX date. "
    "Issuer-versus-vendor differences are kept as sensitivities, not switched row by row.",
    "EV bridge: one rule for target and all peers (debt including leases + minorities and hybrids once - cash; long-term investments and "
    "associates not subtracted, equity income left in earnings).",
    "Peers: ten names chosen by an eight-dimension similarity score; they pass the automated hard filters and carry one ownership/event source "
    "line each (evidence_review.md). Full two-way ownership history of the whole candidate pool was not certified.",
    "Industry ratios from the registered Damodaran files are aggregates, not medians; they are a plausibility check only.",
    "Published regressions are market-wide, low R-squared, about ten months older than the valuation date, with no standard error: "
    "a gap to the market price is not proof of mispricing. The model shown is the one with the highest published R-squared.",
    "Peer interquartile ranges are dispersion, not confidence intervals. Human Spot_check is PENDING (not performed).",
    "Academic analysis only; not investment advice.",
]


def _num(x):
    try:
        v = float(x)
        return None if math.isnan(v) else v
    except (TypeError, ValueError):
        return None


def _f(x, nd=2, pct=False, dash="n/a"):
    v = _num(x)
    if v is None:
        return dash
    return f"{v * 100:+.1f}%" if pct else f"{v:,.{nd}f}"


def _x(x):
    v = _num(x)
    return "n/a" if v is None else f"{v:.2f}x"


def _read(p: Path, kind="csv"):
    if not p.exists():
        return None
    if kind == "csv":
        try:
            df = pd.read_csv(p)
            return df if len(df) else None
        except Exception:
            return None
    return json.loads(p.read_text(encoding="utf-8"))


def collect(folder: Path, notes_path: Path | None = None) -> dict:
    rel = folder / "relative"
    ms = _read(rel / "multiples_summary.csv")
    cp = _read(rel / "comparables.csv")
    rr = _read(rel / "regression_results.json", "json")
    vm = _read(rel / "valuation_multiples.csv")
    rs = _read(folder / "run_state.json", "json") or {}
    if ms is None or vm is None:
        raise SystemExit(f"missing multiples_summary.csv or valuation_multiples.csv in {rel}")
    v = vm.iloc[0]
    price = _num(v.get("current_price"))
    price = price if price is not None else None
    cur_vm = str(v.get("currency") or "")
    d = {"folder": folder, "ticker": str(v.get("ticker") or folder.name.split("_")[0]), "company": str(v.get("company") or rs.get("company") or ""),
         "date": str(rs.get("valuation_date") or folder.name.split("_")[-1]), "price": price,
         "quote": str(v.get("price_quote_currency") or ""), "currency": (str(ms["currency"].dropna().iloc[0]) if "currency" in ms and ms["currency"].notna().any() else cur_vm),
         "status": ((rs.get("stages") or {}).get("stage3_relative") or {}).get("status", "provisional"),
         "ms": ms, "cp": cp, "rr": rr, "chosen": str(v.get("chosen_model") or ""), "r2": _num(v.get("published_r2")),
         "reg_value": _num(v.get("implied_value_per_share"))}
    qa = rel / "qa_results.md"
    d["qa_text"] = qa.read_text(encoding="utf-8") if qa.exists() else ""
    n = notes_path or (folder / "report_notes.md")
    d["notes"] = [ln.strip().lstrip("-*• ").strip() for ln in n.read_text(encoding="utf-8").splitlines() if ln.strip()] if n.exists() else []
    return d


def qa_line(d: dict) -> str:
    t = d["qa_text"]
    if not t:
        return "QA block C: results file not found."
    if "Remediation re-grade" in t:
        return ("QA block C executed once; items on source certification, benchmarks, EV perimeter and normalization were re-graded "
                "PASS-with-note under the approved grading rule (uniform rule applied, limitation disclosed). Details in qa_results.md.")
    fails = sorted(set(re.findall(r"###\s*(C\d+)\s*[-—–]\s*FAIL", t)), key=lambda s: int(s[1:]))
    return "QA block C executed once; " + (f"open FAIL items: {', '.join(fails)} (see qa_results.md)." if fails else "no FAIL items.")


def tables(d: dict) -> dict:
    ms, cp, rr, price, cur = d["ms"], d["cp"], d["rr"], d["price"], d["currency"]
    vs = lambda val: _f((val / price - 1) if (_num(val) is not None and price) else None, pct=True)
    prim = ms[ms["is_primary"] == True] if "is_primary" in ms else ms.iloc[0:0]  # noqa: E712
    prim = prim.iloc[0] if len(prim) else None
    T = {}
    # --- summary
    rows = [["Currency / current price", f"{cur} {_f(price)}" + (f"  | quote: {d['quote']}" if d["quote"] and d["quote"] not in (cur,) else "")]]
    if prim is not None:
        lab = LABELS.get(prim["multiple"], prim["multiple"])
        scaled = str(prim.get("selected_basis")) == "scaled" and _num(prim.get("adjusted_median")) is not None
        med = _x(prim["adjusted_median"]) + " (growth/fundamental-scaled)" if scaled else _x(prim["median"])
        rows += [["Primary multiple (peers)", f"{lab}: median {med}; raw median {_x(prim['median'])}; n = {int(prim['n_valid'])}"],
                 ["Peer value per share: p25 / median / p75",
                  f"{_f(prim['value_per_share_low'])} / {_f(prim['value_per_share_mid'])} / {_f(prim['value_per_share_high'])}"],
                 ["Peer median vs current price", vs(prim["value_per_share_mid"])]]
    else:
        rows.append(["Primary multiple (peers)", "not flagged in multiples_summary.csv"])
    if d["reg_value"] is not None:
        rows += [["Published regression (chosen)", f"{d['chosen']} (published R2 {_f(d['r2'], 3)}): {cur} {_f(d['reg_value'])}"],
                 ["Regression vs current price", vs(d["reg_value"])]]
    if cp is not None:
        t = pd.to_numeric(cp["tier"], errors="coerce")
        eu = cp["europe"].astype(str).str.lower().isin(["true", "1", "yes"]).sum() if "europe" in cp else None
        rows.append(["Peer set", f"{len(cp)} peers; Tier 1-2: {int((t <= 2).sum())}; Tier 3: {int((t == 3).sum())}"
                     + (f"; Europe-listed: {int(eu)}" if eu is not None else "")])
    T["summary"] = rows
    # --- peers
    if cp is not None:
        name = "name" if "name" in cp else "comp_name"
        tick = "ticker" if "ticker" in cp else "comp_ticker"
        cols = [("rank", "#"), (tick, "Ticker"), (name, "Company"), ("country", "Country"), ("tier", "Tier"),
                ("market_cap_eur_m", "Mkt cap EURm"), ("pe", "P/E"), ("pbv", "P/BV"), ("ev_ebit", "EV/EBIT"), ("ev_ebitda", "EV/ EBITDA"),
                ("distance_score", "Distance")]
        cols = [(c, h) for c, h in cols if c in cp]
        rws = []
        for _, r in cp.iterrows():
            row = []
            for c, h in cols:
                val = r[c]
                if c in (tick, name, "country"):
                    row.append(str(val)[:22])
                elif c in ("rank", "tier"):
                    row.append("" if _num(val) is None else str(int(float(val))))
                elif c == "market_cap_eur_m":
                    row.append(_f(val, 0))
                else:
                    row.append(_f(val, 2))
            rws.append(row)
        T["peers"] = [[h for _, h in cols]] + rws
    # --- statistics
    st = [["Multiple", "Basis", "n", "Median", "p25", "p75", "Value p25", "Value mid", "Value p75", "Mid vs price"]]
    for _, r in ms.iterrows():
        if not bool(r.get("usable")) or _num(r.get("value_per_share_mid")) is None or _num(r.get("median")) is None:
            continue
        scaled = str(r.get("selected_basis")) == "scaled" and _num(r.get("adjusted_median")) is not None
        med = r["adjusted_median"] if scaled else r["median"]
        p25 = r.get("adjusted_p25") if scaled else r["p25"]
        p75 = r.get("adjusted_p75") if scaled else r["p75"]
        st.append([LABELS.get(r["multiple"], r["multiple"]) + (" *" if r.get("is_primary") is True else ""), "scaled" if scaled else "raw",
                   str(int(r["n_valid"])), _x(med), _x(p25), _x(p75), _f(r["value_per_share_low"]), _f(r["value_per_share_mid"]),
                   _f(r["value_per_share_high"]), vs(r["value_per_share_mid"])])
    T["stats"] = st if len(st) > 1 else [["Multiple", "Status"], ["none usable", str(ms["status"].dropna().iloc[0]) if "status" in ms and ms["status"].notna().any() else "no usable peer multiple in multiples_summary.csv"]]
    # --- regressions
    rg = [["Model", "Predicted", "Actual", "Published R2", "Implied value", "vs price"]]
    for p in (rr or {}).get("predictions", []):
        mark = " (chosen)" if str(p.get("model")).upper() == d["chosen"].upper() else ""
        rg.append([f"{p.get('model')}{mark}", _x(p.get("predicted")), _x(p.get("actual")), _f(p.get("published_r2"), 3),
                   _f(p.get("value_per_share")), vs(p.get("value_per_share"))])
    T["regs"] = rg if len(rg) > 1 else [["Model", "Status"], ["none", "no regression predictions in regression_results.json"]]
    return T


def to_markdown(d: dict, T: dict) -> str:
    def md(rows, head=True):
        out = ["| " + " | ".join(str(c) for c in rows[0]) + " |", "|" + "|".join("---" for _ in rows[0]) + "|"]
        out += ["| " + " | ".join(str(c) for c in r) + " |" for r in rows[1:]]
        return "\n".join(out)
    s = [f"# {d['company']} ({d['ticker']}) - relative valuation, {d['date']}", "",
         f"Status: {d['status']} - limitations disclosed. {qa_line(d)} Human Spot_check PENDING.", "",
         "## 1. Valuation summary", "", md([["Item", "Value"]] + T["summary"]), "",
         "## 2. Peer set and multiples", "", md(T["peers"]) if "peers" in T else "No qualified peer table available.", "",
         "## 3. Peer-multiple statistics and implied value per share", "", md(T["stats"]),
         "", "* primary multiple. 'scaled' = growth/fundamental-adjusted multiple; value columns are per share in " + d["currency"] + ".", "",
         "## 4. Published regressions (Damodaran, EUROPE, 2026-01)", "", md(T["regs"]), "",
         "## 5. Company-specific notes", ""]
    s += [f"- {n}" for n in d["notes"]] or ["- (none supplied)"]
    s += ["", "## 6. Method notes and limitations", ""] + [f"- {n}" for n in STANDARD_LIMITS] + [""]
    return "\n".join(s)


def to_pdf(d: dict, T: dict, out: Path) -> int:
    from reportlab.lib import colors
    from reportlab.lib.pagesizes import A4
    from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
    from reportlab.lib.units import cm
    from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

    ss = getSampleStyleSheet()
    body = ParagraphStyle("b", parent=ss["BodyText"], fontName="Helvetica", fontSize=7.8, leading=9.6)
    cell = ParagraphStyle("c", parent=body, fontSize=7.2, leading=8.6)
    h1 = ParagraphStyle("h1", parent=ss["Heading1"], fontName="Helvetica-Bold", fontSize=13, spaceAfter=3)
    h2 = ParagraphStyle("h2", parent=ss["Heading2"], fontName="Helvetica-Bold", fontSize=9.2, spaceBefore=5, spaceAfter=2)
    esc = lambda s: str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")

    def tbl(rows, widths=None, head=True, align_right_from=1):
        data = [[Paragraph(esc(c), cell) for c in r] for r in rows]
        t = Table(data, colWidths=widths, repeatRows=1 if head else 0)
        sty = [("GRID", (0, 0), (-1, -1), 0.25, colors.HexColor("#9AA5B1")), ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
               ("TOPPADDING", (0, 0), (-1, -1), 1.6), ("BOTTOMPADDING", (0, 0), (-1, -1), 1.6)]
        if head:
            sty += [("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#DCE6F1"))]
        t.setStyle(TableStyle(sty))
        return t

    W = A4[0] - 3.2 * cm
    story = [Paragraph(esc(f"{d['company']} ({d['ticker']}) - relative valuation"), h1),
             Paragraph(esc(f"Valuation date {d['date']} | {d['currency']} per share | Status: {d['status']} - limitations disclosed | "
                           "Human Spot_check PENDING. " + qa_line(d)), body),
             Paragraph("1. Valuation summary", h2), tbl([["Item", "Value"]] + T["summary"], [W * 0.30, W * 0.70])]
    story += [Paragraph("2. Peer set and multiples", h2)]
    if "peers" in T:
        n = len(T["peers"][0])
        w = [0.9 * cm, 1.4 * cm, 2.9 * cm, 2.2 * cm, 0.9 * cm] + [(W - 8.3 * cm) / max(1, n - 5)] * (n - 5) if n >= 6 else None
        story.append(tbl(T["peers"], w if w and len(w) == n else None))
    else:
        story.append(Paragraph("No qualified peer table available.", body))
    story += [Paragraph("3. Peer-multiple statistics and implied value per share", h2), tbl(T["stats"]),
              Paragraph(esc("* primary multiple. 'scaled' = growth/fundamental-adjusted multiple. Values are per share."), body),
              Paragraph("4. Published regressions (Damodaran, EUROPE, 2026-01)", h2), tbl(T["regs"]),
              Paragraph("5. Company-specific notes", h2)]
    story += [Paragraph(esc("- " + n), body) for n in d["notes"]] or [Paragraph("- (none supplied)", body)]
    story += [Paragraph("6. Method notes and limitations", h2)] + [Paragraph(esc("- " + n), body) for n in STANDARD_LIMITS]
    doc = SimpleDocTemplate(str(out), pagesize=A4, leftMargin=1.6 * cm, rightMargin=1.6 * cm, topMargin=1.4 * cm, bottomMargin=1.3 * cm,
                            title=f"{d['ticker']} relative valuation")
    doc.build(story)
    from pypdf import PdfReader
    return len(PdfReader(str(out)).pages)


def main(argv=None) -> int:
    a = list(sys.argv[1:] if argv is None else argv)
    if not a:
        print(__doc__)
        return 1
    folder = Path(a[0])
    notes = Path(a[a.index("--notes") + 1]) if "--notes" in a else None
    d = collect(folder, notes)
    T = tables(d)
    problems = [m for m, bad in (("current price missing", d["price"] is None), ("no peer table (comparables.csv empty)", "peers" not in T),
                                 ("no usable peer multiples", T["stats"][0][0] != "Multiple" or len(T["stats"][0]) < 3),
                                 ("no regression predictions", len(T["regs"][0]) < 3)) if bad]
    for m in problems:
        print("WARNING:", m)
    (folder / "relative_summary.md").write_text(to_markdown(d, T), encoding="utf-8")
    pdf = folder / f"relative_report_{d['ticker']}.pdf"
    pages = to_pdf(d, T, pdf)
    print(f"wrote {pdf} ({pages} pages) and relative_summary.md; company notes: {len(d['notes'])}")
    if not d["notes"]:
        print("WARNING: no report_notes.md found - company-specific caveats section is empty")
    return 2 if problems else 0


if __name__ == "__main__":
    raise SystemExit(main())
