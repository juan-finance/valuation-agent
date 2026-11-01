#!/usr/bin/env python3
"""Build relative_report_IBE.MC.pdf from existing stage-3 output files. No new research."""
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
pe = ms[ms.multiple.eq('pe')].iloc[0]
pbv = ms[ms.multiple.eq('pbv')].iloc[0]
evebit = ms[ms.multiple.eq('ev_ebit')].iloc[0]
evcf = ms[ms.multiple.eq('ev_cf')].iloc[0]
eva = ms[ms.multiple.eq('ev_assets')].iloc[0]

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
pdf.cell(0, 9, "Iberdrola (IBE.MC) - Relative Valuation Report", new_x="LMARGIN", new_y="NEXT")
pdf.set_font("Helvetica", size=8)
pdf.cell(0, 5, "Valuation date: 2026-10-30 | Mode: relative_only deviation (no DCF, no stage 2/4) | Status: PROVISIONAL", new_x="LMARGIN", new_y="NEXT")
pdf.ln(2)

# --- 1. Summary -------------------------------------------------------------
sect("1. Valuation summary")
reg_val = vm["implied_value_per_share"]
rows = [
    ["Currency", "EUR (reporting FY2025: EUR millions)"],
    ["Current price (close 2026-10-30)", "22.18"],
    ["Primary multiple (comparables)", "EV/EBITDA (bucket-A integrated utility); peer median "
     "12.56x, n = 10"],
    ["Comparables, p25 - median - p75 per share", f"{prim.value_per_share_low:.2f} - {prim.value_per_share_mid:.2f} - {prim.value_per_share_high:.2f}"],
    ["Median vs price", f"{prim.value_per_share_mid:.2f} vs 22.18 = {prim.value_per_share_mid/22.18-1:+.1%} (vendor EBITDA basis)"],
    ["Issuer-EBITDA sensitivity (median)", f"{sens.iloc[2].EUR_per_share:.2f} (adjusted) / {sens.iloc[1].EUR_per_share:.2f} (reported) vs 22.18"],
    ["Regression estimate per share", f"{reg_val:.2f} (published EUROPE regression, chosen model: PBV, R2 = 0.423)"],
    ["Regression vs price", f"{reg_val:.2f} vs 22.18 = {reg_val/22.18-1:+.1%}"],
]
table(["Item", "Value"], rows, [60, 120])
pdf.ln(1)
line(f"Peer-multiple cross-checks (medians, per share): PE raw {pe.raw_value_mid if 'raw_value_mid' in pe else 15.53:.2f}; PBV ROE-scaled {pbv.value_per_share_mid:.2f}; "
     f"EV/EBIT {evebit.value_per_share_mid:.2f}; EV/CF {evcf.value_per_share_mid:.2f}; EV/Assets {eva.value_per_share_mid:.2f}. Published EUROPE "
     "regressions: PE (R2 0.201) 19.62; EV/EBITDA (R2 0.262) 33.04. IBE trades at a premium to peers "
     "(actual EV/EBITDA 14.8x vs peer median 12.6x; PE 24.4x vs 17.1x); both the peer EV/EBITDA and the "
     "published PBV read it ~22-24% rich; the market-wide EV/EBITDA equation reads it ~33 cheap - "
     "sector-blind equation, flagged not reconciled.")
line("Basis notes: vendor FY2025 EBITDA 14,700m sits below issuer adjusted EBITDA 15,684m / reported "
     "16,592m (definition scope; sensitivity retained). Vendor NI to common 6,055m vs issuer reported "
     "6,285m (230m hybrid-coupon deduction - real claim, kept). Declared FY2025 dividend ~4,543m "
     "(0.68/share; scrip dividend - CF-paid 1,275m understates) implies payout 0.75.")
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
line("Composition: 10 peers Tier 1-2 (8 integrated/regulated utilities, 2 grid operators), "
     "10/10 Europe-listed - all requirements met at the first (strictest) selection step; no size-band or "
     "region relaxation. Pool of 33 candidates + 1 subsidiary evidence row built from issuer-named "
     "competitors, sector_adjustments Tier-1 seeds and own research; all extracts reused from the dated cache.")
line("Exclusions documented: Endesa (~70% subsidiary of candidate ENEL, hard gate); CEZ (uniform web "
     "source unavailable; MSCI EM listing anyway); CNA/A2A/REE/IG and small IPPs (below size-band floor "
     "EUR 14.79bn); AY/BLX/INE (no common 2026-10-30 price date); ORA (US-listed, World-only pool never "
     "reached). ENEL scored 11th and just missed selection; FORTUM and ORSTED also above the set.")
line("IBE vs selected-peer medians: actual EV/EBITDA 14.8x vs 12.6x; PE 24.4x vs 17.1x; ROE 12.1% vs "
     "~10.6%; net debt/EBITDA 3.79x vs ~5.03x; EBITDA margin 33.4% vs ~26.7%; growth 9.8% vs ~3.1%; "
     "beta 0.45 vs ~0.57. Premium multiples are consistent with higher growth/ROE and lower leverage.")

# --- 3. Method notes and caveats ---------------------------------------------
pdf.add_page()
sect("3. Method notes and caveats")
for t in [
 "Comparable companies: similarity scoring on 8 dimensions; pool-only 5/95% winsorization; Europe step "
 "feasible at default caps; per-share values in EUR on uniform vendor FY2025 fundamentals; EV basis = "
 "before associates (peers and target inverse both exclude the associates adjustment).",
 "Primary multiple: EV/EBITDA; min_valid = 6 per standing approval (ev_cf and peg n = 9, all others 10). "
 "Growth-scaled PE/PEG distorted by near-zero peer growth - flagged, raw multiples retained.",
 "Published regressions: Damodaran regressions_multi_2026-01, EUROPE equations, decimal unit policy for "
 "DFR/tax (user-approved). Chosen model = highest published R2 (PBV).",
 "Regression inputs: beta 0.45 (5Y observed); g_eps 9.15% and g_rev 4.05% analyst consensus (sourced); "
 "ROE 0.121 closing book; payout 0.750 declared-dividend basis (CF-paid 0.21 distorted by scrip, flagged); "
 "dfr 0.287; effective tax 0.2064; roic 0.0749.",
 "Caveats: (a) regression file ~10 months older than valuation date; (b) published file gives no n, SEy "
 "or p-values - residual-band/diagnostic fields n/a_published_route; (c) GLOBAL-equation sign warnings "
 "recorded at stage 0, EUROPE equations unaffected but noted; (d) market-wide equations, low R2 - "
 "deviation is not proof of mispricing; (e) market-wide EV/EBITDA prediction (19.7x) sits above the "
 "European utility peer median (12.6x) - recorded, not resolved.",
 "QA block C: PROVISIONAL - human Spot_check PENDING (recorded, not claimed); ISIN issuer-page "
 "verification PENDING; ownership/event audit outstanding. EV-to-equity inverse check passed "
 "(associates = 0 on both sides); three reproducibly random EV recomputes matched. No failures; "
 "warned items disclosed.",
 "Data route: stockanalysis.com uniform web route (profile/statistics/financials/history); all figures "
 "from the 2026-10-30 cache; vendor figures cross-checked against the Iberdrola FY2025 CNMV filing "
 "(equity/NCI/assets/group NI exact; revenue/EBITDA/EBIT definition gaps documented).",
]:
    line("- " + t, h=4.6)

# --- 4. Sources ---------------------------------------------------------------
sect("4. Sources")
for t in [
 "Market data: cache/market/2026-10-30/ (universe.csv = IEUR MSCI Europe IMI proxy; per-candidate "
 "EDPRpool_*/ENELpool_* fetches in candidates/; fetch_manifest.json).",
 "Macro/FX: cache/macro/2026-10-30.json (ECB FX snapshot; Bund 10y; Spain A3 CRP 1.48% via top-up).",
 "Company fundamentals: Iberdrola FY2025 results (CNMV filing: revenues 45,546.8m; EBITDA 16,592.4m; "
 "EBIT 10,276.4m; net profit 6,285m; equity 63,419m; net financial debt 51,755m; EPS 0.925) and press "
 "release (adjusted EBITDA 15,684m; adjusted NI 6,749m) via relative_inputs.md.",
 "Vendor route: stockanalysis.com bme/IBE and per-candidate pages (dated 2026-10-30 cache).",
 "Published regressions: Damodaran regressions_multi_2026-01 (EUROPE), PE / PBV / EV/EBITDA equations, "
 "sha256 a894ea86...",
 "Working files: outputs/IBE.MC_2026-10-30/relative/ (comparables.csv, multiples_summary.csv, "
 "comparables_audit.xlsx, regression_valuation.xlsx with live formulas, qa_results.md, source_log.csv).",
]:
    line("- " + t, h=4.6)

pdf.ln(4)
pdf.set_font("Helvetica", "I", 7.5)
pdf.multi_cell(0, 4, "Academic analysis produced by an automated valuation agent. Not investment advice. "
                     "All figures cited from the files listed in section 4; nothing recomputed for this report.")

out = f"{D}/relative_report_IBE.MC.pdf"
pdf.output(out)
print(out)
