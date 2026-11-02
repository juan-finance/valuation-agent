"""Builds SU.PA stage 3 deliverables from relative/*.csv|json (no new numbers)."""
import json
from pathlib import Path

import pandas as pd
from openpyxl import Workbook
from openpyxl.styles import Font
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table

from valuation_agent import comparables as comp
import stage3 as s3

P = Path(__file__).resolve().parent
OUT = P.parent
R = json.load(open(P / 'regression_results.json'))
MS = pd.read_csv(P / 'multiples_summary.csv')
VM = pd.read_csv(P / 'valuation_multiples.csv')
CP = pd.read_csv(P / 'comparables.csv')
PE_ADJ = R['comparables_adjust']['pe']
PBV_ADJ = R['comparables_adjust']['pbv']
DISCLAIMER = ('Academic analysis for coursework only; not investment advice. Figures are from public web sources '
              'accessed 2026-10-30/31 and cross-checked against Schneider Electric FY2025 results (26 Feb 2026).')
EPS, BVPS = s3.EPS, s3.EQ / s3.SHARES
PE_RAW = MS.loc[MS.multiple == 'pe', 'median'].item()
PBV_RAW = MS.loc[MS.multiple == 'pbv', 'median'].item()
EVE_MED = MS.loc[MS.multiple == 'ev_ebitda', 'median'].item()
EV_SALES_MED = MS.loc[MS.multiple == 'ev_sales', 'median'].item()
eq_pe, eq_pbv, eq_ev = (R['regressions'][k] for k in ['PE', 'PBV', 'EV/EBITDA'])
chosen = 'PBV'  # highest published R2 among eligible PE, PBV, EV/EBITDA (regression_published_route section 7)
V = {
    'pe_comp_raw': PE_RAW * EPS, 'pe_comp_adj': PE_ADJ['median'] * EPS,
    'pbv_comp_raw': PBV_RAW * BVPS, 'pbv_comp_adj': PBV_ADJ['median'] * BVPS,
    'reg_pe': eq_pe['predicted'] * EPS, 'reg_pbv': eq_pbv['predicted'] * BVPS,
    'reg_eve': VM.loc[VM.multiple == 'EV/EBITDA', 'value_per_share_eur'].item(),
}
V['reg_chosen'] = V['reg_pbv']
ev_bridge = lambda ev: (ev - s3.DEBT - s3.NCI + s3.CASH) / s3.SHARES
V['ev_ebitda_comp'] = ev_bridge(EVE_MED * s3.EBITDA)
V['ev_ebit_comp'] = ev_bridge(MS.loc[MS.multiple == 'ev_ebit', 'median'].item() * s3.EBIT)
V['ev_sales_comp'] = ev_bridge(EV_SALES_MED * s3.SALES)
ROWS = [
    ('Comparables P/E, median raw (n=10)', f"{PE_RAW:.2f}x", V['pe_comp_raw']),
    ('Comparables P/E, median growth-adjusted (n=10, PRIMARY)', f"{PE_ADJ['median']:.2f}x", V['pe_comp_adj']),
    ('Comparables P/BV, median raw (n=10)', f"{PBV_RAW:.2f}x", V['pbv_comp_raw']),
    ('Comparables P/BV, median ROE-adjusted (n=10)', f"{PBV_ADJ['median']:.2f}x", V['pbv_comp_adj']),
    ('Comparables EV/EBITDA, median (n=9)', f"{EVE_MED:.2f}x", V['ev_ebitda_comp']),
    ('Comparables EV/EBIT, median (n=9)', f"{MS.loc[MS.multiple=='ev_ebit','median'].item():.2f}x", V['ev_ebit_comp']),
    ('Comparables EV/Sales, median (n=9, cross-check)', f"{EV_SALES_MED:.2f}x", V['ev_sales_comp']),
    ('Published regression P/E (EUROPE, R2 0.201)', f"{eq_pe['predicted']:.2f}x", V['reg_pe']),
    ('Published regression P/BV (EUROPE, R2 0.423, CHOSEN)', f"{eq_pbv['predicted']:.2f}x", V['reg_pbv']),
    ('Published regression EV/EBITDA (EUROPE, R2 0.262)', f"{eq_ev['predicted']:.2f}x", V['reg_eve']),
]
PRICE = s3.PRICE


def pct(x):
    return f"{(x / PRICE - 1) * 100:+.1f}%"


def fmt(x):
    return f"EUR {x:,.2f}"


# ---- comparables_report.md, valuation_summary.md -------------------------------------------------------------------
peers = ', '.join(f"{r.comp_ticker_raw} ({r.name})" for r in CP.itertuples())
comp_md = f"""# SU.PA comparables report (relative-only, 2026-10-30)

{DISCLAIMER}

## Peer set
10 peers, all European-listed, 8 tiers 1-2 + 2 tier 3 (at the cap). Selection by comparables.select_peers with
min_tier_1_2=6, max_tier_3=2, min_europe=5 (procedure section 3). Peers: {peers}.

Candidate universe: shared dated stockanalysis extracts of all prior runs (104 European rows screened). SU's
~EUR 134bn market cap sets the 0.1-10x size band at EUR 13.4bn-1,337bn, which excludes most mid-cap electrical
names (NEX, NKT, IMI, SPX, SKF.B, ANDR, G1A, SUN, WEIR, ROR...). Restructuring exclusions per the FY2024-25 window:
ABBN (Robotics disposal + Gamesa), SIE (Altair), NEX (divestments), SMIN, SKF.B, GEV. Tier 3 was required because
only 9 tier-1/2 candidates survived all filters.

## Multiples (median, n valid >= 6)
| Multiple | n | Median | P25 | P75 | Value/share median |
|---|---|---|---|---|---|
""" + '\n'.join(
    f"| {r.multiple} | {int(r.n_valid)} | {r.median:.2f} | {r.p25:.2f} | {r.p75:.2f} | {('n/a' if pd.isna(r.value_per_share_mid) else fmt(r.value_per_share_mid))} |"
    for r in MS.itertuples()) + f"""

Growth-adjusted P/E median {PE_ADJ['median']:.2f}x (scaled_multiple, driver 100 x growth, target fundamental growth
{s3.G_FUND*100:.2f}%). ROE-adjusted P/BV median {PBV_ADJ['median']:.2f}x. Positive extremes retained (ENR P/E 76.8).

## Limitations
- Peers and tiers are judgement (agent). Index membership and ISIN checks not performed (IEUR proxy membership only).
- Peer data from stockanalysis dated extracts, not verified against filings. Growth is fundamental (ROE x retention), no consensus.
- EV multiples have n=9 (HLMA lacks EV in the source); EV basis is before associates.
- Tier-3 peers (Sandvik, Epiroc) are mining equipment: allowed under the cap because tier-1/2 supply 9 < 10; documented shortfall driver is the target's size band.
- Payout scoring basis is CF dividends paid / NI (0.526); the published-route payout input is declared DPS/EPS (0.567).
"""
(P / 'comparables_report.md').write_text(comp_md)

sum_md = f"""# SU.PA relative valuation summary (published route + comparables)

## 1. Scope and route
Relative-only, stage 3. Stages 1, 2, 4 skipped_by_deviation (standing_approvals relative_only). Published
Damodaran regression route, EUROPE equations (dataset regressions_multi_2026-01, as_of 2026-01-01); comparables
per comparables_procedure.

## 2. Inputs
Price {fmt(PRICE)}; shares {s3.SHARES:.2f}m; market cap EUR {s3.MCAP:,.0f}m; EPS {EPS:.4f} (basic); book
value/share {BVPS:.4f}; sources in relative_inputs.md (vendor extract cross-checked vs Schneider FY2025 release).

## 3. Published regression predictions (decimal units, as_published_note)
| Multiple | Predicted | Actual | Published R2 | Value/share |
|---|---|---|---|---|
| P/E | {eq_pe['predicted']:.2f}x | {VM.loc[VM.multiple=='PE','actual_multiple'].item():.2f}x | {eq_pe['r2']:.3f} | {fmt(V['reg_pe'])} |
| P/BV (chosen) | {eq_pbv['predicted']:.2f}x | {VM.loc[VM.multiple=='PBV','actual_multiple'].item():.2f}x | {eq_pbv['r2']:.3f} | {fmt(V['reg_pbv'])} |
| EV/EBITDA | {eq_ev['predicted']:.2f}x | {VM.loc[VM.multiple=='EV/EBITDA','actual_multiple'].item():.2f}x | {eq_ev['r2']:.3f} | {fmt(V['reg_eve'])} |

Inputs: analyst consensus growth g_eps 20.40% / g_rev 11.56% (3Y, vendor statistics) — NO fundamental substitution
needed; roe 17.20% (closing book), payout 0.567 (declared DPS/EPS), beta 1.19, dfr 0.1296, tax 25.06%, roic 13.23%.

## 4. Comparables
See comparables_report.md. Primary P/E median growth-adjusted {fmt(V['pe_comp_adj'])} (raw {fmt(V['pe_comp_raw'])});
P/BV median ROE-adjusted {fmt(V['pbv_comp_adj'])}; EV/EBITDA {fmt(V['ev_ebitda_comp'])}; EV/EBIT {fmt(V['ev_ebit_comp'])}.

## 5. Model choice and result
Published model chosen by highest published R2 among PE, PBV, EV/EBITDA: P/BV, value {fmt(V['reg_chosen'])}
({pct(V['reg_chosen'])} vs price). Alternatives: P/E {fmt(V['reg_pe'])}, EV/EBITDA {fmt(V['reg_eve'])}.
The P/BV prediction (3.39x vs actual 5.53x, +63% deviation) cannot see Schneider's ROE premium — a market-wide
equation limitation, not evidence of mispricing.

## 6. Limitations
- Relative only: no DCF, no recommendation (approved deviation).
- Published R2 values are low (0.20 to 0.42); the regression is a market cross-section, not an SU-specific fit.
- Peer and tier choices are agent judgement; index and ISIN checks pending; IEUR proxy membership only.
- Tier-3 peers used at cap (mining equipment economics) because the size band excluded most mid-cap electrical names.
- Workbook formulas are live but not recalculated (LibreOffice not installed); see regression_valuation.xlsx.
- No Spot_check by a human reviewer yet (human_review pending).

{DISCLAIMER}
"""
(P / 'valuation_summary.md').write_text(sum_md)

# ---- workbooks -----------------------------------------------------------------------------------------------------
wb = Workbook()
ws = wb.active
ws.title = 'Inputs'
ws.append(['Input', 'Value', 'Source'])
for k, v in R['inputs'].items():
    ws.append([k, v, 'SU inputs; g_eps/g_rev = analyst consensus (not substituted); payout = declared DPS/EPS'])
ws.append(['beta', s3.BETA, 'StockAnalysis extract 2026-10-30'])
for c in ws[1]:
    c.font = Font(bold=True)
ws2 = wb.create_sheet('Regression')
ws2.append(['Model', 'Term', 'Coefficient', 'Input (cell)', 'Contribution'])
row = 2
ws2.append(['Constant', '', 0, '', ''])
preds = {}
for dep in ['PE', 'PBV', 'EV/EBITDA']:
    d = R['regressions'][dep]
    start = ws2.max_row + 1
    ws2.append([dep, 'constant', d['constant'], '', f'=C{start}'])
    for t in d['terms']:
        if t['variable'] not in R['inputs']:
            raise SystemExit(f"missing input {t['variable']}")
        idx = list(R['inputs']).index(t['variable']) + 2
        r_ = ws2.max_row + 1
        ws2.append([dep, t['variable'], t['coef'], f"=Inputs!B{idx}", f'=C{r_}*D{r_}'])
    end = ws2.max_row
    ws2.append([dep, 'PREDICTED (sum)', '', '', f'=SUM(E{start}:E{end})'])
    manual = d['constant'] + sum(t['coef'] * R['inputs'][t['variable']] for t in d['terms'])
    assert abs(manual - d['predicted']) < 1e-9, (dep, manual, d['predicted'])
    preds[dep] = manual
    ws2.append([])
wb.save(P / 'regression_valuation.xlsx')

wa = Workbook()
a = wa.active
a.title = 'peers'
a.append(list(CP.columns))
for r in CP.itertuples(index=False):
    a.append(list(r))
b = wa.create_sheet('multiples')
b.append(list(MS.columns))
for r in MS.itertuples(index=False):
    b.append([None if pd.isna(x) else x for x in r])
wa.save(P / 'comparables_audit.xlsx')

# ---- sensitivities --------------------------------------------------------------------------------------------------
sens = []
sel = pd.read_csv(P / 'peer_selection_raw.csv').set_index('ticker')
for t in sel.index:
    a2 = sel.drop(index=t)
    ad = comp.scaled_multiple(a2.pe, a2.growth, s3.G_FUND, driver_scale=100, min_valid=6)
    raw = comp.multiple_stats(a2.pe.to_numpy(), min_valid=6)
    sens.append(dict(sensitivity='leave-one-out selected peer', removed=t,
                     adj_pe_value=ad['median'] * s3.EPS if ad.get('available') else None,
                     raw_pe_value=raw.get('median', 0) * s3.EPS, n_valid=ad['n_valid']))
sens.append(dict(sensitivity='issuer adjusted measures: adj NI 4829 (EPS adj 8.59) on raw PE median',
                 value_per_share=PE_RAW * 8.59))
sens.append(dict(sensitivity='target declared payout basis payout=0.567 (vs CF basis 0.526): fundamental growth 0.0685 vs 0.0721',
                 value_per_share=None))
pd.DataFrame(sens).to_csv(P / 'sensitivities.csv', index=False)

# ---- source log append ----------------------------------------------------------------------------------------------
src = pd.DataFrame([
    ('SU.PA StockAnalysis financials', 'cache/market/2026-10-30/candidates/SU_*', '2026-10-30', 'price, shares, P&L, balance sheet, multiples', 'used'),
    ('Schneider Electric FY2025 results release', 'https://www.se.com/ww/en/assets/564/document/528237/release-fy-results-2025.pdf', '2026-11-02', 'issuer cross-check', 'used'),
    ('ENR/PRY/NKT/other candidate rows', 'outputs/*/relative/candidate_raw.csv', '2026-11-02', 'European peer candidates', 'used'),
    ('Damodaran published regressions EUROPE', 'data/ regressions_multi_2026-01 (as_of 2026-01-01)', '2026-10-30', 'PE, PBV, EV/EBITDA equations', 'used'),
    ('Damodaran country risk (France)', 'cache/macro/2026-10-30.json (ctryprem_global_2026-07)', '2026-10-30', 'France CRP 0.74%', 'used'),
], columns=['source', 'location', 'accessed', 'used_for', 'status'])
src.to_csv(OUT / 'source_log_stage3.csv', index=False)

# ---- relative_summary.md --------------------------------------------------------------------------------------------
sumtxt = [
    'SU.PA (Schneider Electric) relative valuation (published route + comparables), batch date 2026-10-30',
    f'Price EUR {PRICE:.2f}; market cap EUR {s3.MCAP:,.0f}m; EPS {EPS:.4f}; BVPS {BVPS:.4f}',
    f'Chosen regression model: published P/BV (highest R2 0.423), value EUR {V["reg_chosen"]:.2f} ({pct(V["reg_chosen"])})',
    f'Alternatives: P/E regression EUR {V["reg_pe"]:.2f} ({pct(V["reg_pe"])}); EV/EBITDA regression EUR {V["reg_eve"]:.2f} ({pct(V["reg_eve"])})',
    f'Comparables (10 peers): P/E growth-adj median {PE_ADJ["median"]:.2f}x = EUR {V["pe_comp_adj"]:.2f} ({pct(V["pe_comp_adj"])}); raw median {PE_RAW:.2f}x = EUR {V["pe_comp_raw"]:.2f} ({pct(V["pe_comp_raw"])})',
    f'Comparables P/BV ROE-adj {PBV_ADJ["median"]:.2f}x = EUR {V["pbv_comp_adj"]:.2f}; EV/EBITDA median (n=9) {EVE_MED:.2f}x = EUR {V["ev_ebitda_comp"]:.2f}; EV/EBIT = EUR {V["ev_ebit_comp"]:.2f}',
    'Relative only (stages 1, 2, 4 skipped by approved deviation). Not investment advice.',
]
(OUT / 'relative_summary.md').write_text('\n'.join(sumtxt) + '\n')

# ---- PDF short report ----------------------------------------------------------------------------------------------
st = getSampleStyleSheet()
doc = SimpleDocTemplate(str(OUT / 'relative_report_SU.PA.pdf'), pagesize=A4, leftMargin=40, rightMargin=40,
                        topMargin=40, bottomMargin=40)
story = [Paragraph('SU.PA (Schneider Electric SE) relative valuation, batch date 2026-10-30', st['Title']),
         Paragraph(DISCLAIMER, st['Italic']), Spacer(1, 10),
         Paragraph(f'Price EUR {PRICE:.2f}; market cap EUR {s3.MCAP:,.0f}m; EPS {EPS:.2f}; BVPS {BVPS:.2f}. '
                   'Relative-only stage 3 (published Damodaran EUROPE regressions and 10 European peers). '
                   'No DCF and no recommendation (approved deviation).', st['BodyText']), Spacer(1, 8)]
tbl = [['Method', 'Multiple', 'Value per share (EUR)', 'vs price']] + [
    [m, mult, f'{v:,.2f}', pct(v)] for m, mult, v in ROWS]
t = Table(tbl, colWidths=[270, 70, 110, 70])
t.setStyle([('GRID', (0, 0), (-1, -1), 0.3, '#888888'), ('FONTSIZE', (0, 0), (-1, -1), 8),
            ('BACKGROUND', (0, 0), (-1, 0), '#DDDDDD')])
story += [t, Spacer(1, 10),
          Paragraph(f'Chosen model: published P/BV regression (highest published R2 0.423) at EUR {V["reg_chosen"]:.2f}. '
                    'Inputs use analyst consensus growth (no substitution); the market-wide equation cannot see '
                    "Schneider's ROE premium (actual P/BV 5.53x vs predicted 3.39x).", st['BodyText']),
          Paragraph('Peer set: Legrand, Prysmian, Siemens Energy (T1); Atlas Copco, Metso, Halma, Alfa Laval, '
                    'Wartsila (T2); Sandvik, Epiroc (T3, at cap — size band excluded most mid-cap electrical names). '
                    'Limitations: peer tiers are judgement; index/ISIN checks pending; published R2 is low; '
                    'workbook not recalculated; human review pending.', st['BodyText'])]
doc.build(story)
print('built', len(ROWS), 'rows; chosen', round(V['reg_chosen'], 2))
