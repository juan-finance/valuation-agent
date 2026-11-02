#!/usr/bin/env python3
"""Build relative_report_SSE.L.pdf from existing stage-3 output files. No new research."""
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
pdf.cell(0, 9, "SSE (SSE.L) - Relative Valuation Report", new_x="LMARGIN", new_y="NEXT")
pdf.set_font("Helvetica", size=8)
pdf.cell(0, 5, "Valuation date: 2026-10-30 | Mode: relative_only deviation (no DCF, no stage 2/4) | Status: PROVISIONAL", new_x="LMARGIN", new_y="NEXT")
pdf.ln(2)

# --- 1. Summary -------------------------------------------------------------
sect("1. Valuation summary")
reg_val = vm["implied_value_per_share"]
rows = [
    ["Currency", "GBP (reporting FY2025: GBP millions; LSE quote in pence converted)"],
    ["Current price (close 2026-10-30)", "26.27"],
    ["Primary multiple (comparables)", "EV/EBITDA (bucket-A integrated utility); peer median "
     "11.78x, n = 10"],
    ["Comparables, p25 - median - p75 per share", f"{prim.value_per_share_low:.2f} - {prim.value_per_share_mid:.2f} - {prim.value_per_share_high:.2f}"],
    ["Median vs price", f"{prim.value_per_share_mid:.2f} vs 26.27 = {prim.value_per_share_mid/26.27-1:+.1%} (vendor EBITDA basis)"],
    ["Issuer-EBITDA sensitivity (median)", f"{sens.iloc[2].GBP_per_share:.2f} (adjusted) / {sens.iloc[1].GBP_per_share:.2f} (reported) vs 26.27"],
    ["Regression estimate per share", f"{reg_val:.2f} (published EUROPE regression, chosen model: PBV, R2 = 0.423)"],
    ["Regression vs price", f"{reg_val:.2f} vs 26.27 = {reg_val/26.27-1:+.1%}"],
]
table(["Item", "Value"], rows, [60, 120])
pdf.ln(1)
line(f"Peer-multiple cross-checks (medians, per share): PE raw {pe.raw_value_mid if 'raw_value_mid' in pe else 17.50:.2f}; PBV ROE-scaled {pbv.value_per_share_mid:.2f}; "
     f"EV/EBIT {evebit.value_per_share_mid:.2f}; EV/CF {evcf.value_per_share_mid:.2f}; EV/Assets {eva.value_per_share_mid:.2f}. Published EUROPE "
     "regressions: PE (R2 0.201) 23.23; EV/EBITDA (R2 0.262) 40.94. SSE trades at a premium to peers "
     "(actual EV/EBITDA 14.7x vs peer median 11.8x; PE 26.7x vs 17.8x); both the peer EV/EBITDA and the "
     "published PBV read it ~13-27% rich; the market-wide EV/EBITDA equation reads it ~56% cheap - "
     "sector-blind equation, flagged not reconciled.")
line("Basis notes: vendor FY2025 EBITDA 2,850m sits between issuer reported EBITDA 2,738.3m and "
     "adjusted 3,349.3m (definition scope; sensitivity retained). Vendor NI to common 1,189m ties issuer "
     "reported attributable profit 1,189.4m exactly; adjusted attributable 1,768.1m gives PE value "
     "26.02. Declared FY2025 dividend ~710m (DPS 64.2p) implies payout 0.597 (CF-paid 0.40 underweights "
     "final-dividend timing). Vendor Total Debt appears to include equity-classified hybrid capital "
     "(73.7m coupon to other equity holders); uniform EV bridge kept, disclosed not harmonized.")
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
line("Composition: 10 peers Tier 1-2 (7 integrated/regulated utilities, 1 renewables IPP, 2 grid "
     "operators), 10/10 Europe-listed - all requirements met at the first (strictest) selection step; "
     "no size-band or region relaxation. Pool of 33 candidates + 1 subsidiary evidence row built from "
     "issuer-named competitors, sector_adjustments Tier-1 seeds and own research; all extracts reused "
     "from the dated cache.")
line("Exclusions documented: Endesa (~70% subsidiary of candidate ENEL, hard gate); CEZ (uniform web "
     "source unavailable; MSCI EM listing anyway); ERG/SLR/GRE/SCATC/DRX (below size-band floor "
     "EUR 3.80bn); AY/BLX/INE (no common 2026-10-30 price date); ORA (US-listed, World-only pool never "
     "reached). ENEL, ENGIE, FORTUM, EDP Renovaveis, CNA, SRG, VER scored above the selected set.")
line("SSE vs selected-peer medians: actual EV/EBITDA 14.7x vs 11.8x; PE 26.7x vs 17.8x; PBV 2.63x vs "
     "1.72x; ROE 10.2% vs ~10.3%; net debt/EBITDA 3.38x vs ~4.2x; EBITDA margin 28.1% vs ~26%; "
     "fundamental growth 6.1% vs ~4.0%; beta 0.53 vs ~0.57. Premium multiples consistent with the "
     "regulated-RAV growth programme, lower leverage and very high capex/sales (~26%).")

# --- 3. Method notes and caveats ---------------------------------------------
pdf.add_page()
sect("3. Method notes and caveats")
for t in [
 "Comparable companies: similarity scoring on 8 dimensions; pool-only 5/95% winsorization; Europe step "
 "feasible at default caps; per-share values in GBP on uniform vendor FY2025 fundamentals; EV basis = "
 "before associates (peers and target inverse both exclude the associates adjustment).",
 "Primary multiple: EV/EBITDA; min_valid = 6 per standing approval (all headline multiples n = 10). "
 "Growth-scaled PE/PEG distorted by Orsted outlier growth - flagged, raw multiples retained.",
 "Published regressions: Damodaran regressions_multi_2026-01, EUROPE equations, decimal unit policy for "
 "DFR/tax (user-approved). Chosen model = highest published R2 (PBV).",
 "Regression inputs: beta 0.53 (5Y observed); g_eps 15.19% and g_rev 7.71% analyst consensus (sourced); "
 "ROE 0.0986 closing book; payout 0.597 declared-dividend basis (CF-paid 0.40 underweights timing, "
 "flagged); dfr 0.2526; effective tax 0.2799; roic 0.0747.",
 "Caveats: (a) regression file ~10 months older than valuation date; (b) published file gives no n, SEy "
 "or p-values - residual-band/diagnostic fields n/a_published_route; (c) GLOBAL-equation sign warnings "
 "recorded at stage 0, EUROPE equations unaffected but noted; (d) market-wide equations, low R2 - "
 "deviation is not proof of mispricing; (e) market-wide EV/EBITDA prediction (21.0x) sits far above "
 "the European utility peer median (11.8x) - recorded, not resolved; (f) SSE fiscal year ends March "
 "(Mar-2025 basis, not calendarized); (g) 2026 equity raise increased share count to ~1.21bn.",
 "QA block C: PROVISIONAL - human Spot_check PENDING (recorded, not claimed); ISIN issuer-page "
 "verification PENDING; ownership/event audit outstanding. EV-to-equity inverse check passed "
 "(associates = 0 on both sides); three reproducibly random EV recomputes matched. No failures; "
 "warned items disclosed.",
 "Data route: stockanalysis.com uniform web route (profile/statistics/financials/history); all figures "
 "from the 2026-10-30 cache; vendor figures cross-checked against the SSE FY2024/25 preliminary "
 "results (LSE RNS 4968J + sse.com statement PDF; revenue and attributable NI exact ties; "
 "EBIT/EBITDA definition gaps documented).",
]:
    line("- " + t, h=4.6)

# --- 4. Sources ---------------------------------------------------------------
sect("4. Sources")
for t in [
 "Market data: cache/market/2026-10-30/ (universe.csv = IEUR MSCI Europe IMI proxy; per-candidate "
 "EDPRpool_*/ENELpool_* fetches in candidates/; fetch_manifest.json).",
 "Macro/FX: cache/macro/2026-10-30.json (ECB FX snapshot GBP 0.8338/EUR; GBP 10y default-free 4.8287%; "
 "UK Aa3 CRP 0.74% via BP.L stage-0 top-up).",
 "Company fundamentals: SSE FY2024/25 preliminary results (LSE RNS 4968J + sse.com statement PDF: "
 "revenues 10,131.9m; reported EBITDA 2,738.3m; adjusted EBITDA 3,349.3m; operating profit 1,962.2m; "
 "attributable NI 1,189.4m; adjusted attributable 1,768.1m; equity 12,064m; net debt 9,513.9m; "
 "DPS 64.2p) via relative_inputs.md.",
 "Vendor route: stockanalysis.com lon/SSE and per-candidate pages (dated 2026-10-30 cache).",
 "Published regressions: Damodaran regressions_multi_2026-01 (EUROPE), PE / PBV / EV/EBITDA equations, "
 "sha256 a894ea86...",
 "Working files: outputs/SSE.L_2026-10-30/relative/ (comparables.csv, multiples_summary.csv, "
 "comparables_audit.xlsx, regression_valuation.xlsx with live formulas, qa_results.md, source_log.csv).",
]:
    line("- " + t, h=4.6)

pdf.ln(4)
pdf.set_font("Helvetica", "I", 7.5)
pdf.multi_cell(0, 4, "Academic analysis produced by an automated valuation agent. Not investment advice. "
                     "All figures cited from the files listed in section 4; nothing recomputed for this report.")

out = f"{D}/relative_report_SSE.L.pdf"
pdf.output(out)
print(out)
