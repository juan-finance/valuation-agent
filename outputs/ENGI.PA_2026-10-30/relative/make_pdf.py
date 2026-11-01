#!/usr/bin/env python3
"""Build relative_report_ENGI.PA.pdf from existing stage-3 output files. No new research."""
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
pdf.cell(0, 9, "ENGIE (ENGI.PA) - Relative Valuation Report", new_x="LMARGIN", new_y="NEXT")
pdf.set_font("Helvetica", size=8)
pdf.cell(0, 5, "Valuation date: 2026-10-30 | Mode: relative_only deviation (no DCF, no stage 2/4) | Status: PROVISIONAL", new_x="LMARGIN", new_y="NEXT")
pdf.ln(2)

# --- 1. Summary -------------------------------------------------------------
sect("1. Valuation summary")
reg_val = vm["implied_value_per_share"]
rows = [
    ["Currency", "EUR (reporting FY2025: EUR millions)"],
    ["Current price (close 2026-10-30)", "23.43"],
    ["Primary multiple (comparables)", "EV/EBITDA (bucket-A integrated utility); peer median "
     "12.23x, n = 10"],
    ["Comparables, p25 - median - p75 per share", f"{prim.value_per_share_low:.2f} - {prim.value_per_share_mid:.2f} - {prim.value_per_share_high:.2f}"],
    ["Median vs price", f"{prim.value_per_share_mid:.2f} vs 23.43 = {prim.value_per_share_mid/23.43-1:+.1%} (vendor EBITDA basis)"],
    ["Issuer-EBITDA sensitivity (median)", f"{sens.iloc[1].EUR_per_share:.2f} vs 23.43 = {sens.iloc[1].EUR_per_share/23.43-1:+.1%} (consolidated) / {sens.iloc[2].EUR_per_share:.2f} (ex-nuclear)"],
    ["Regression estimate per share", f"{reg_val:.2f} (published EUROPE regression, chosen model: PBV, R2 = 0.423)"],
    ["Regression vs price", f"{reg_val:.2f} vs 23.43 = {reg_val/23.43-1:+.1%}"],
]
table(["Item", "Value"], rows, [60, 120])
pdf.ln(1)
line("Peer-multiple cross-checks (medians, per share): PE 35.44; PBV ROE-scaled 34.55; "
     "EV/EBIT 52.31; EV/CF NM (target FY2025 vendor CFO negative); EV/Assets 49.71; "
     "PS raw/EV-Sales-scaled 35.44/73.41. Published EUROPE regressions: PE (R2 0.201) 31.69; "
     "EV/EBITDA (R2 0.262) 88.37. Peer EV multiples read ENGIE cheap (actual EV/EBITDA 8.1x vs "
     "peer median 12.2x); the published PBV equation reads it ~12% cheap. Both methods point the "
     "same direction; none reconciled under relative_only.")
line("Basis notes: vendor FY2025 EBITDA 13,012m sits below issuer consolidated EBITDA 14,700m / "
     "ex-nuclear 13,400m (definition scope; sensitivity retained). Vendor NI to common 3,687m vs "
     "issuer net income Group share 3,827m (further ~140m hybrid-coupon deduction - flagged). "
     "Proposed FY2025 dividend EUR1.35/share (~3,283m, issuer-stated 67% of NRIgs) -> payout 0.89 "
     "declared basis; paid-cash basis 1.23 makes scoring growth 0, so PEG and growth-scaled PE "
     "adjustment are not meaningful.")
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
     "region relaxation. Pool of 34 candidates built from issuer-named competitors, sector_adjustments "
     "Tier-1 seeds and own research.")
line("Exclusions documented: CEZ (uniform web source unavailable; MSCI EM listing anyway); A2A/REE/IG "
     "and small IPPs (below size-band floor EUR 5.70bn); AY/BLX/INE (no common 2026-10-30 price date); "
     "ORA (US-listed, World-only pool never reached). Endesa eligible for ENGIE (Enel subsidiary, not a "
     "target relationship - flagged for pending ownership audit). Iberdrola, RWE, NTGY, ELE, A2A scored "
     "above the selected set.")
line("ENGI vs selected-peer medians: actual EV/EBITDA 8.1x vs 12.2x; PE 15.5x vs 23.4x; ROE 10.9% vs "
     "~9.7%; net debt/EBITDA 3.1x vs ~3.3x; EBITDA margin 18.1% vs ~27.8% (vendor scope); beta 0.57 "
     "vs ~0.57.")

# --- 3. Method notes and caveats ---------------------------------------------
pdf.add_page()
sect("3. Method notes and caveats")
for t in [
 "Comparable companies: similarity scoring on 8 dimensions; pool-only 5/95% winsorization; Europe step "
 "feasible at default caps; per-share values in EUR on uniform vendor FY2025 fundamentals; EV basis = "
 "before associates (peers and target inverse both exclude the associates adjustment).",
 "Primary multiple: EV/EBITDA; min_valid = 6 per standing approval (pe n = 9, all others 10; ev_cf "
 "NM for target - vendor FY2025 CFO -1,476m vs issuer CFFO 13,600m; peg NM with zero scoring growth).",
 "Published regressions: Damodaran regressions_multi_2026-01, EUROPE equations, decimal unit policy for "
 "DFR/tax (user-approved). EV/EBITDA percent-point alternative gives predicted 11.92x vs 20.23x decimal "
 "(41% divergence); decimal policy applied, both recorded. Chosen model = highest published R2 (PBV).",
 "Regression inputs: beta 0.57 (5Y observed); g_eps 4.73% and g_rev 5.60% analyst consensus (sourced, "
 "consistent with issuer NRIgs 2026 guidance EUR4.6-5.2bn); ROE 0.1119 closing book; payout 0.89 "
 "declared-dividend basis (1.23 paid-cash, flagged); dfr 0.492; effective tax 0.2485; roic 0.0851.",
 "Caveats: (a) regression file ~10 months older than valuation date; (b) published file gives no n, SEy "
 "or p-values - residual-band/diagnostic fields n/a_published_route; (c) GLOBAL-equation sign warnings "
 "recorded at stage 0, EUROPE equations unaffected but noted; (d) market-wide equations, low R2 - "
 "deviation is not proof of mispricing; (e) market-wide EV/EBITDA prediction (20.2x) sits above the "
 "European utility peer median (12.2x) - recorded, not resolved.",
 "QA block C: PROVISIONAL - human Spot_check PENDING (recorded, not claimed); ISIN issuer-page "
 "verification PENDING; ownership/event audit outstanding. EV-to-equity inverse check passed "
 "(associates = 0 on both sides); three reproducibly random EV recomputes matched. No failures; "
 "warned items disclosed.",
 "Data route: stockanalysis.com uniform web route (profile/statistics/financials/history); all figures "
 "from the 2026-10-30 cache and fetched candidate tables; vendor figures cross-checked against the "
 "ENGIE FY2025 results press release (revenue ~exact; NIGs exact 3,827m; EBITDA scope differences "
 "and CFO/CFFO definitional gap documented).",
]:
    line("- " + t, h=4.6)

# --- 4. Sources ---------------------------------------------------------------
sect("4. Sources")
for t in [
 "Market data: cache/market/2026-10-30/ (universe.csv = IEUR MSCI Europe IMI proxy; per-candidate "
 "EDPRpool_*/ENELpool_* fetches in candidates/; fetch_manifest.json).",
 "Macro/FX: cache/macro/2026-10-30.json (ECB FX snapshot; Bund 10y; mature ERP).",
 "Company fundamentals: ENGIE FY2025 results press release (revenue 71.9bn; EBITDA 14.7bn / ex-nuclear "
 "13.4bn; EBIT 9,471m / ex-nuclear 8,757m; NIGs 3,827m; NRIgs 4.9bn; net financial debt 38.9bn; "
 "net economic debt 45.2bn; DPS EUR1.35, 67% NRIgs payout) via relative_inputs.md, cross-checked vs "
 "vendor extracts.",
 "Vendor route: stockanalysis.com epa/ENGI and per-candidate pages (cached 2026-10-30, accessed "
 "2026-11-01).",
 "Published regressions: Damodaran regressions_multi_2026-01 (EUROPE), PE / PBV / EV/EBITDA equations, "
 "sha256 a894ea86...",
 "Working files: outputs/ENGI.PA_2026-10-30/relative/ (comparables.csv, multiples_summary.csv, "
 "comparables_audit.xlsx, regression_valuation.xlsx with live formulas, qa_results.md, source_log.csv).",
]:
    line("- " + t, h=4.6)

pdf.ln(4)
pdf.set_font("Helvetica", "I", 7.5)
pdf.multi_cell(0, 4, "Academic analysis produced by an automated valuation agent. Not investment advice. "
                     "All figures cited from the files listed in section 4; nothing recomputed for this report.")

out = f"{D}/relative_report_ENGI.PA.pdf"
pdf.output(out)
print(out)
