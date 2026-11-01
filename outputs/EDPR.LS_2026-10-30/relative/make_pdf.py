#!/usr/bin/env python3
"""Build relative_report_EDPR.LS.pdf from existing stage-3 output files. No new research."""
from fpdf import FPDF
import pandas as pd, json, os

D = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
R = os.path.join(D, "relative")

ms = pd.read_csv(f"{R}/multiples_summary.csv")
peers = pd.read_csv(f"{R}/comparables.csv")
vm = pd.read_csv(f"{R}/valuation_multiples.csv").iloc[0]
reg = json.load(open(f"{R}/regression_results.json"))
prim = ms[ms.is_primary].iloc[0]
sens = pd.read_csv(f"{R}/sensitivities.csv")

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
pdf.cell(0, 9, "EDP Renovaveis (EDPR.LS) - Relative Valuation Report", new_x="LMARGIN", new_y="NEXT")
pdf.set_font("Helvetica", size=8)
pdf.cell(0, 5, "Valuation date: 2026-10-30 | Mode: relative_only deviation (no DCF, no stage 2/4) | Status: PROVISIONAL", new_x="LMARGIN", new_y="NEXT")
pdf.ln(2)

# --- 1. Summary -------------------------------------------------------------
sect("1. Valuation summary")
reg_val = vm["implied_value_per_share"]
rows = [
    ["Currency", "EUR (reporting FY2025: EUR millions)"],
    ["Current price (close 2026-10-30)", "12.50"],
    ["Primary multiple (comparables)", "EV/EBITDA (bucket-B renewable developer/operator); peer median "
     "11.99x, n = 10"],
    ["Comparables, p25 - median - p75 per share", f"{prim.value_per_share_low:.2f} - {prim.value_per_share_mid:.2f} - {prim.value_per_share_high:.2f}"],
    ["Median vs price", f"{prim.value_per_share_mid:.2f} vs 12.50 = {prim.value_per_share_mid/12.50-1:+.1%} (vendor EBITDA basis; see warning)"],
    ["Issuer-EBITDA sensitivity (median)", f"{sens.iloc[1].EUR_per_share:.2f} vs 12.50 = {sens.iloc[1].EUR_per_share/12.50-1:+.1%}"],
    ["Regression estimate per share", f"{reg_val:.2f} (published EUROPE regression, chosen model: PBV, R2 = 0.423)"],
    ["Regression vs price", f"{reg_val:.2f} vs 12.50 = +31.6%"],
]
table(["Item", "Value"], rows, [60, 120])
pdf.ln(1)
line("Peer-multiple cross-checks (medians, per share): PE 4.48; PBV ROE-scaled 4.59 (raw 20.07); "
     "EV/CF 3.68; EV/Assets 16.07; EV/Sales 3.92; PS 4.48. Published EUROPE regressions: PE (R2 0.201) "
     "5.48; EV/EBITDA (R2 0.262) 14.10. Peer multiples read EDPR cheap on earnings/book (EUR 3.9-4.6) "
     "except asset-based 16.07; published equations read it cheap on PBV (16.45) and EV/EBITDA (14.10) "
     "but rich on PE (5.48). No football-field chart was generated in this run.")
line("EBITDA-definition warning (material): vendor FY2025 EBITDA (1,187m) excludes equity-method and "
     "institutional-partnership income that issuer EBITDA (1,947m reported / 1,974m recurring) includes, "
     "while EDPR's EV carries the matching claims (NCI 1,906m, deferred partnership revenues). The "
     "vendor-basis EV/EBITDA headline (3.92/share) is biased low; issuer-basis sensitivity gives ~12.6, "
     "near the 12.50 price. Both retained; deferred institutional-partnership revenues are not deducted "
     "as a debt-like claim in either variant (recorded limitation).")
line("No intrinsic (DCF) estimate is produced under the relative_only deviation; stages 1, 2 and 4 are "
     "marked skipped_by_deviation in run_state.json.")

# --- 2. Peers ----------------------------------------------------------------
sect("2. Peer set (10 of 10 selected at the Europe step)")
rows = []
for _, p in peers.iterrows():
    mult = f"EVEBITDA {p.ev_ebitda:.1f} / PBV {p.pbv:.1f}" if pd.notna(p.ev_ebitda) else "n/a"
    rows.append([p.comp_name, p.comp_ticker, p.country, int(p.tier), mult])
table(["Name", "Ticker", "Country", "Tier", "EV/EBITDA / PBV"], rows, [52, 22, 42, 14, 50])
pdf.ln(1)
line("Composition: 10 peers Tier 1-2 (5 renewable IPPs, 5 integrated utilities), 10/10 Europe-listed - "
     "all requirements met at the first (strictest) selection step; no size-band or region relaxation. "
     "Pool of 34 candidates + 1 parent evidence row built from issuer-named competitors, "
     "sector_adjustments Tier-1 seeds and own research.")
line("Exclusions documented: EDP (~71% parent, hard gate); NEOEN/OX2/IREN/HERA (uniform web source "
     "unavailable); EKT/PNE3 (below EUR 1bn); AY/BLX/INE (no common 2026-10-30 price date); ORA "
     "(US-listed, kept for World relaxation that was never reached).")
line("EDPR vs peer medians: ROE 2.1% vs ~10%; fundamental growth 1.7% vs ~4%; net debt/EBITDA 6.9x vs "
     "~4.1x; EBITDA margin 52% vs ~28%; capex/sales 124% vs ~37% - low-return, high-leverage, "
     "high-reinvestment profile, consistent with scaled-multiple discounts.")

# --- 3. Method notes and caveats ---------------------------------------------
pdf.add_page()
sect("3. Method notes and caveats")
for t in [
 "Comparable companies: similarity scoring on 8 dimensions; pool-only 5/95% winsorization; Europe step "
 "feasible at default caps; per-share values in EUR on uniform vendor FY2025 fundamentals; EV basis = "
 "before associates (peers and target inverse both exclude the associates adjustment).",
 "Primary multiple: EV/EBITDA; min_valid = 6 per standing approval (ev_cf n = 9, all others 10; peg "
 "n = 5 excluded).",
 "Published regressions: Damodaran regressions_multi_2026-01, EUROPE equations, decimal unit policy for "
 "DFR/tax (user-approved). EV/EBITDA percent-point alternative gives predicted 12.37x vs 21.09x decimal "
 "(41% divergence); decimal policy applied, both recorded. Chosen model = highest published R2 (PBV).",
 "Regression inputs: beta 0.72 (5Y observed); g_eps 20.42% and g_rev 8.51% analyst consensus (sourced); "
 "ROE 0.021 closing book; payout 0.61 proposed-dividend basis (0.40 recurring policy, sensitivity shown); "
 "dfr 0.416; effective tax 0.3537; roic 0.0106.",
 "Caveats: (a) regression file ~10 months older than valuation date; (b) published file gives no n, SEy "
 "or p-values - residual-band/diagnostic fields n/a_published_route; (c) GLOBAL-equation sign warnings "
 "recorded at stage 0, EUROPE equations unaffected but noted; (d) market-wide equations, low R2 - "
 "deviation is not proof of mispricing.",
 "QA block C: PROVISIONAL - human Spot_check PENDING (recorded, not claimed); ISIN issuer-page "
 "verification PENDING; ownership/event audit outstanding. EV-to-equity inverse check passed "
 "(associates = 0 on both sides). No failures; two warned items disclosed.",
 "Data route: stockanalysis.com uniform web route (profile/statistics/financials/history); all figures "
 "from the 2026-10-30 cache and fetched candidate tables; vendor figures cross-checked against the EDPR "
 "FY25 Results Report (equity exact match; NI within 0.1%; EBITDA/revenue definition differences "
 "documented).",
]:
    line("- " + t, h=4.6)

# --- 4. Sources ---------------------------------------------------------------
sect("4. Sources")
for t in [
 "Market data: cache/market/2026-10-30/ (universe.csv = IEUR MSCI Europe IMI proxy; per-candidate "
 "EDPRpool_* fetches in candidates/; fetch_manifest.json).",
 "Macro/FX: cache/macro/2026-10-30.json (ECB FX snapshot; Bund 10y; mature ERP).",
 "Company fundamentals: EDPR FY25 Results Report (EBITDA 1,947m reported / 1,974m recurring; NI 216m; "
 "net debt 8,109m; equity 10,274m; proposed dividend EUR 132.09m) via relative_inputs.md, cross-checked "
 "vs vendor extracts.",
 "Vendor route: stockanalysis.com eli/EDPR and per-candidate pages (fetched 2026-10-30/11-01).",
 "Published regressions: Damodaran regressions_multi_2026-01 (EUROPE), PE / PBV / EV/EBITDA equations, "
 "sha256 a894ea86...",
 "Working files: outputs/EDPR.LS_2026-10-30/relative/ (comparables.csv, multiples_summary.csv, "
 "comparables_audit.xlsx, regression_valuation.xlsx with live formulas, qa_results.md, source_log.csv).",
]:
    line("- " + t, h=4.6)

pdf.ln(4)
pdf.set_font("Helvetica", "I", 7.5)
pdf.multi_cell(0, 4, "Academic analysis produced by an automated valuation agent. Not investment advice. "
                     "All figures cited from the files listed in section 4; nothing recomputed for this report.")

out = f"{D}/relative_report_EDPR.LS.pdf"
pdf.output(out)
print(out)
