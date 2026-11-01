#!/usr/bin/env python3
"""Build relative_report_ALFA.ST.pdf from existing stage-3 output files. No new research."""
from fpdf import FPDF
import pandas as pd, json, os

D = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
R = os.path.join(D, "relative")

ms = pd.read_csv(f"{R}/multiples_summary.csv")
peers = pd.read_csv(f"{R}/comparables.csv")
vm = pd.read_csv(f"{R}/valuation_multiples.csv").iloc[0]
reg = json.load(open(f"{R}/regression_results.json"))
prim = ms[ms.is_primary].iloc[0]

pdf = FPDF(format="A4")
pdf.set_auto_page_break(auto=True, margin=15)
pdf.set_margins(15, 15, 15)

T = dict(family="Helvetica", size=9)
H = dict(family="Helvetica", style="B", size=13)
S = dict(family="Helvetica", style="B", size=10)

def line(txt, style=None, h=5):
    pdf.set_font(**(style or T))
    pdf.set_x(pdf.l_margin)
    pdf.multi_cell(0, h, txt)

def sect(title):
    pdf.ln(3); pdf.set_font(**S); pdf.cell(0, 7, title, new_x="LMARGIN", new_y="NEXT"); pdf.ln(0.5)

def table(headers, rows, widths):
    pdf.set_font("Helvetica", "B", 8)
    for h_, w in zip(headers, widths):
        pdf.cell(w, 5.5, h_, border=1)
    pdf.ln()
    pdf.set_font("Helvetica", size=8)
    for r in rows:
        for c, w in zip(r, widths):
            pdf.cell(w, 5.5, str(c), border=1)
        pdf.ln()

pdf.add_page()
pdf.set_font(**H)
pdf.cell(0, 9, "Alfa Laval (ALFA.ST) - Relative Valuation Report", new_x="LMARGIN", new_y="NEXT")
pdf.set_font("Helvetica", size=8)
pdf.cell(0, 5, "Valuation date: 2026-10-30 | Mode: relative_only deviation (no DCF, no stage 2/4) | Status: PROVISIONAL", new_x="LMARGIN", new_y="NEXT")
pdf.ln(2)

# --- 1. Summary table -------------------------------------------------------
sect("1. Valuation summary")
pbv_reg = vm["implied_value_per_share"]
rows = [
    ["Currency", "SEK (reporting FY2025: SEK millions)"],
    ["Current price (close 2026-10-30)", "545.60"],
    ["Primary multiple", "PE, growth-scaled by consensus g_eps = 12.72% (earnings-based multiple most "
     "representative for a profitable large-cap machinery group; equity multiples have all 10 peers valid)"],
    ["Comparables, p25 - median - p75 per share", f"{prim.value_per_share_low:.2f} - {prim.value_per_share_mid:.2f} - {prim.value_per_share_high:.2f}"],
    ["Difference vs price (median)", f"{prim.value_per_share_mid:.2f} vs 545.60 = +21.9%"],
    ["Regression estimate per share", f"{pbv_reg:.2f} (published EUROPE regression, chosen model: PBV, R2 = 0.423)"],
    ["Difference vs price (regression)", f"{pbv_reg:.2f} vs 545.60 = -37.1%"],
]
table(["Item", "Value"], rows, [60, 120])
pdf.ln(1)
line("Peer-multiple cross-checks (medians, per share): PBV-scaled 544.93; PS 534.16; EV/EBITDA 468.41; "
     "EV/EBIT 501.24; EV/CF 362.46. Published EUROPE regressions: PE (R2 0.201) 434.06; EV/EBITDA (R2 0.262) "
     "710.47. Peer-adjusted view: fairly priced to ~22% cheap; market-wide published equations read ALFA "
     "~20-37% rich on earnings and book value. No football-field chart was generated in this run.")
line("No intrinsic (DCF) estimate is produced under the relative_only deviation; stages 1, 2 and 4 are marked "
     "skipped_by_deviation in run_state.json.")

# --- 2. Peers ---------------------------------------------------------------
sect("2. Peer set (10 of 10 selected at the Europe step)")
rows = []
for _, p in peers.iterrows():
    mult = f"PE {p.pe:.1f} / PBV {p.pbv:.1f}" if pd.notna(p.pe) else "n/a"
    rows.append([p.comp_name, p.comp_ticker, p.country, int(p.tier), mult])
table(["Name", "Ticker", "Country", "Tier", "PE / PBV"], rows, [52, 22, 42, 14, 50])
pdf.ln(1)
line("Composition: 9 peers Tier 1-2, 1 Tier 3 (Halma); 10/10 Europe-listed - all requirements met at the "
     "first (strictest) selection step, no size-band or region relaxation needed. Pool of 31 candidates "
     "(incl. target) built from the 2026-10-30 cached universe.")
line("Exclusions documented: KSB (universe membership unverified), BCHN (market cap ~EUR 1.73bn below the "
     "0.1x size band), FLS (3 missing scoring dimensions > hard limit of 2).")
line("Tier 3 shortfall is limited to the single weakest-similarity name (Halma, diversified instrumentation); "
     "within the documented cap max_tier_3 = 2.")

# --- 3. Method notes and caveats --------------------------------------------
pdf.add_page()
sect("3. Method notes and caveats")
for t in [
 "Comparable companies: similarity scoring on 8 dimensions (subsector, size, geography, margins, growth, "
 "capital intensity, listing geography, business model); pool-only 5/95% winsorization; per-share values "
 "computed in SEK on issuer-verified FY2025 fundamentals.",
 "Primary multiple: PE scaled by consensus EPS growth (g_eps = 12.72%, 3Y, stockanalysis.com); min_valid = 6 "
 "per standing approval; 10/10 peers valid for PE.",
 "Published regressions: Damodaran regressions_multi_2026-01, EUROPE equations, decimal unit policy for "
 "DFR/tax (user-approved). EV/EBITDA unit policies differ 18.3% (>10% divergence); decimal policy applied, "
 "both recorded. Chosen model = highest published R2 (PBV, R2 0.423).",
 "Regression inputs: g_eps 12.72%, g_rev 9.41%, beta 0.75 (5Y), ROE 19.1%, payout 42.5%, debt fraction 8.5%, "
 "effective tax 25.7%.",
 "Caveats: (a) regression file is ~10 months older than the valuation date - flagged as a limitation; "
 "(b) published file provides no n, SEy or p-values, so residual-band and diagnostic fields are "
 "n/a_published_route; (c) GLOBAL-coefficient sign warnings recorded (PEG/ln(g_eps), PBV/beta) - EUROPE "
 "equations unaffected but noted; (d) ATCO.A and EPI.A cap-reconcile flags (+4.25%/+4.75%) explained by "
 "dual A/B share classes, retained with flag.",
 "QA block C: PROVISIONAL - human Spot_check PENDING (recorded, not claimed); ISIN issuer-page verification "
 "PENDING; ownership/event audit outstanding. EV-to-equity inverse check passed; associates = 0 flagged.",
 "Data route: stockanalysis.com uniform web route (statistics/, financials/, balance-sheet/); all figures "
 "cited from the 2026-10-30 cache and fetched candidate tables; vendor figures cross-checked against the "
 "Alfa Laval FY2025 release.",
]:
    line("- " + t, h=4.6)

# --- 4. Sources ---------------------------------------------------------------
sect("4. Sources")
for t in [
 "Market data: cache/market/2026-10-30/ (universe.csv = IEUR MSCI Europe IMI proxy; per-candidate fetches in "
 "candidates/; candidate_fetch_manifest.json).",
 "Macro/FX: cache/macro/2026-10-30.json (ECB FX, SEK 10.978/EUR; Bund 10y 3.38%; mature ERP 4.20%).",
 "Company fundamentals: Alfa Laval FY2025 report/issuer figures (revenue 69,674m, EBITDA 14,252m, EBIT 11,749m, "
 "NI 8,322m, equity 43,409m, EPS 20.01, DPS 9.00) via relative_inputs.md, cross-checked vs vendor extracts.",
 "Vendor route: stockanalysis.com statistics/financials/balance-sheet pages per candidate (fetched 2026-10-30/31).",
 "Published regressions: Damodaran regressions_multi_2026-01 (EUROPE), PE / PBV / EV/EBITDA equations.",
 "Working files: outputs/ALFA.ST_2026-10-30/relative/ (comparables.csv, multiples_summary.csv, "
 "comparables_audit.xlsx, regression_valuation.xlsx with live formulas, qa_results.md, source_log.csv).",
]:
    line("- " + t, h=4.6)

pdf.ln(4)
pdf.set_font("Helvetica", "I", 7.5)
pdf.multi_cell(0, 4, "Academic analysis produced by an automated valuation agent. Not investment advice. "
                     "All figures cited from the files listed in section 4; nothing recomputed for this report.")

out = f"{D}/relative_report_ALFA.ST.pdf"
pdf.output(out)
print(out)
