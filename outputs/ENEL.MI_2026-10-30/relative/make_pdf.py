#!/usr/bin/env python3
"""Build relative_report_ENEL.MI.pdf from existing stage-3 output files. No new research."""
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
pdf.cell(0, 9, "Enel (ENEL.MI) - Relative Valuation Report", new_x="LMARGIN", new_y="NEXT")
pdf.set_font("Helvetica", size=8)
pdf.cell(0, 5, "Valuation date: 2026-10-30 | Mode: relative_only deviation (no DCF, no stage 2/4) | Status: PROVISIONAL", new_x="LMARGIN", new_y="NEXT")
pdf.ln(2)

# --- 1. Summary -------------------------------------------------------------
sect("1. Valuation summary")
reg_val = vm["implied_value_per_share"]
rows = [
    ["Currency", "EUR (reporting FY2025: EUR millions)"],
    ["Current price (close 2026-10-30)", "9.32"],
    ["Primary multiple (comparables)", "EV/EBITDA (bucket-A integrated utility); peer median "
     "12.56x, n = 10"],
    ["Comparables, p25 - median - p75 per share", f"{prim.value_per_share_low:.2f} - {prim.value_per_share_mid:.2f} - {prim.value_per_share_high:.2f}"],
    ["Median vs price", f"{prim.value_per_share_mid:.2f} vs 9.32 = {prim.value_per_share_mid/9.32-1:+.1%} (vendor EBITDA basis)"],
    ["Issuer-EBITDA sensitivity (median)", f"{sens.iloc[1].EUR_per_share:.2f} vs 9.32 = {sens.iloc[1].EUR_per_share/9.32-1:+.1%} (reported) / {sens.iloc[2].EUR_per_share:.2f} (ordinary)"],
    ["Regression estimate per share", f"{reg_val:.2f} (published EUROPE regression, chosen model: PBV, R2 = 0.423)"],
    ["Regression vs price", f"{reg_val:.2f} vs 9.32 = {reg_val/9.32-1:+.1%}"],
]
table(["Item", "Value"], rows, [60, 120])
pdf.ln(1)
line("Peer-multiple cross-checks (medians, per share): PE 7.11; PBV ROE-scaled 6.90; "
     "EV/EBIT 22.34; EV/CF 12.21; EV/Assets 10.79; EV/Sales-scaled/PS 7.11/17.79. Published EUROPE "
     "regressions: PE (R2 0.201) 10.41; EV/EBITDA (R2 0.262) 31.81. Peer EV multiples read ENEL cheap "
     "(actual EV/EBITDA 8.4x vs peer median 12.6x); the published PBV equation reads it ~25% rich. The two "
     "methods bracket the price in opposite directions; both are shown, none reconciled under relative_only.")
line("Basis notes: vendor FY2025 EBITDA 20,311m sits below issuer reported EBITDA 22,073m / ordinary "
     "22,874m (definition scope; sensitivity retained). Vendor NI to common 3,959m vs issuer group net "
     "income 4,225m (a further 266m 'preferred/other' vendor deduction though Enel has no preferred - "
     "flagged). Declared FY2025 dividend 4,982m (0.49/share, part-funded from retained earnings) implies "
     "payout >100% - fundamental growth = 0, so PEG and growth-scaled PE adjustment are not meaningful.")
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
line("Composition: 10 peers Tier 1-2 (8 integrated/regulated utilities, 2 grid/renewable operators), "
     "10/10 Europe-listed - all requirements met at the first (strictest) selection step; no size-band or "
     "region relaxation. Pool of 33 candidates + 1 subsidiary evidence row built from issuer-named "
     "competitors, sector_adjustments Tier-1 seeds and own research.")
line("Exclusions documented: Endesa (~70% subsidiary of ENEL, hard gate); CEZ (uniform web source "
     "unavailable; MSCI EM listing anyway); CNA/A2A/REE/IG and small IPPs (below size-band floor "
     "EUR 9.25bn); AY/BLX/INE (no common 2026-10-30 price date); ORA (US-listed, World-only pool never "
     "reached). Iberdrola and RWE scored above the selected set.")
line("ENEL vs selected-peer medians: actual EV/EBITDA 8.4x vs 12.6x; PE 23.4x vs 17.8x; ROE 12.0% vs "
     "~10%; net debt/EBITDA 3.1x vs ~4.3x; EBITDA margin 25.6% vs ~34%; beta 0.84 vs ~0.6.")

# --- 3. Method notes and caveats ---------------------------------------------
pdf.add_page()
sect("3. Method notes and caveats")
for t in [
 "Comparable companies: similarity scoring on 8 dimensions; pool-only 5/95% winsorization; Europe step "
 "feasible at default caps; per-share values in EUR on uniform vendor FY2025 fundamentals; EV basis = "
 "before associates (peers and target inverse both exclude the associates adjustment).",
 "Primary multiple: EV/EBITDA; min_valid = 6 per standing approval (ev_cf n = 9, all others 10; peg "
 "NM for target with zero fundamental growth).",
 "Published regressions: Damodaran regressions_multi_2026-01, EUROPE equations, decimal unit policy for "
 "DFR/tax (user-approved). EV/EBITDA percent-point alternative gives predicted 10.83x vs 19.41x decimal "
 "(44% divergence); decimal policy applied, both recorded. Chosen model = highest published R2 (PBV).",
 "Regression inputs: beta 0.84 (5Y observed); g_eps 7.63% and g_rev 3.17% analyst consensus (sourced, "
 "consistent with Enel plan EPS ~6% CAGR); ROE 0.124 closing book; payout 1.26 declared-dividend basis "
 "(1.18 on issuer group NI, flagged); dfr 0.427; effective tax 0.3305; roic 0.0994.",
 "Caveats: (a) regression file ~10 months older than valuation date; (b) published file gives no n, SEy "
 "or p-values - residual-band/diagnostic fields n/a_published_route; (c) GLOBAL-equation sign warnings "
 "recorded at stage 0, EUROPE equations unaffected but noted; (d) market-wide equations, low R2 - "
 "deviation is not proof of mispricing; (e) market-wide EV/EBITDA prediction (19.4x) sits above the "
 "European utility peer median (12.6x) - recorded, not resolved.",
 "QA block C: PROVISIONAL - human Spot_check PENDING (recorded, not claimed); ISIN issuer-page "
 "verification PENDING; ownership/event audit outstanding. EV-to-equity inverse check passed "
 "(associates = 0 on both sides); three reproducibly random EV recomputes matched. No failures; "
 "warned items disclosed.",
 "Data route: stockanalysis.com uniform web route (profile/statistics/financials/history); all figures "
 "from the 2026-10-30 cache and fetched candidate tables; vendor figures cross-checked against the Enel "
 "FY2025 results press release (equity/NCI exact; group NI exact; revenue as-reported exact; "
 "EBITDA definition differences documented).",
]:
    line("- " + t, h=4.6)

# --- 4. Sources ---------------------------------------------------------------
sect("4. Sources")
for t in [
 "Market data: cache/market/2026-10-30/ (universe.csv = IEUR MSCI Europe IMI proxy; per-candidate "
 "EDPRpool_*/ENELpool_* fetches in candidates/; fetch_manifest.json).",
 "Macro/FX: cache/macro/2026-10-30.json (ECB FX snapshot; Bund 10y; mature ERP).",
 "Company fundamentals: Enel FY2025 results press release (revenues 80,346m; ordinary EBITDA 22,874m; "
 "reported EBITDA 22,073m; group NI 4,225m; net financial debt 57,182m; DPS 0.49) via relative_inputs.md, "
 "cross-checked vs vendor extracts.",
 "Vendor route: stockanalysis.com bit/ENEL and per-candidate pages (fetched 2026-10-30/11-01).",
 "Published regressions: Damodaran regressions_multi_2026-01 (EUROPE), PE / PBV / EV/EBITDA equations, "
 "sha256 a894ea86...",
 "Working files: outputs/ENEL.MI_2026-10-30/relative/ (comparables.csv, multiples_summary.csv, "
 "comparables_audit.xlsx, regression_valuation.xlsx with live formulas, qa_results.md, source_log.csv).",
]:
    line("- " + t, h=4.6)

pdf.ln(4)
pdf.set_font("Helvetica", "I", 7.5)
pdf.multi_cell(0, 4, "Academic analysis produced by an automated valuation agent. Not investment advice. "
                     "All figures cited from the files listed in section 4; nothing recomputed for this report.")

out = f"{D}/relative_report_ENEL.MI.pdf"
pdf.output(out)
print(out)
