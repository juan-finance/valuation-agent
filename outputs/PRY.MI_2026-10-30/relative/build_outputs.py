"""Builds PRY.MI stage 3 deliverables from relative/*.csv|json (no new numbers)."""
import json
from pathlib import Path

import pandas as pd
from openpyxl import Workbook
from openpyxl.styles import Font
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table

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
              'accessed 2026-11-01 and are not verified against annual reports.')
EPS, BVPS = s3.EPS, s3.EQ / s3.SHARES
PE_RAW = MS.loc[MS.multiple == 'pe', 'median'].item()
PBV_RAW = MS.loc[MS.multiple == 'pbv', 'median'].item()
EVE_MED = MS.loc[MS.multiple == 'ev_ebitda', 'median'].item()
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
V['ps_comp'] = MS.loc[MS.multiple == 'ps', 'median'].item() * s3.SALES / s3.SHARES
ROWS = [
    ('Comparables P/E, median raw (n=10)', f"{PE_RAW:.2f}x", V['pe_comp_raw']),
    ('Comparables P/E, median growth-adjusted (n=10, PRIMARY)', f"{PE_ADJ['median']:.2f}x", V['pe_comp_adj']),
    ('Comparables P/BV, median raw (n=10)', f"{PBV_RAW:.2f}x", V['pbv_comp_raw']),
    ('Comparables P/BV, median ROE-adjusted (n=10)', f"{PBV_ADJ['median']:.2f}x", V['pbv_comp_adj']),
    ('Comparables EV/EBITDA, median (n=7)', f"{EVE_MED:.2f}x", V['ev_ebitda_comp']),
    ('Comparables EV/EBIT, median (n=7)', f"{MS.loc[MS.multiple=='ev_ebit','median'].item():.2f}x", V['ev_ebit_comp']),
    ('Comparables EV/Sales, median (n=10, cross-check)', f"{MS.loc[MS.multiple=='ev_sales','median'].item():.2f}x", V['ps_comp']),
    ('Published regression P/E (EUROPE, R2 0.201)', f"{eq_pe['predicted']:.2f}x", V['reg_pe']),
    ('Published regression P/BV (EUROPE, R2 0.423, CHOSEN)', f"{eq_pbv['predicted']:.2f}x", V['reg_pbv']),
    ('Published regression EV/EBITDA (EUROPE, R2 0.262)', f"{eq_ev['predicted']:.2f}x", V['reg_eve']),
]
PRICE = s3.PRICE
cfg = dict(price=PRICE, eps=EPS, bvps=BVPS, chosen=chosen)


def pct(x):
    return f"{(x / PRICE - 1) * 100:+.1f}%"


def fmt(x):
    return f"EUR {x:,.2f}"


# ---- comparables_report.md, valuation_summary.md -------------------------------------------------------------------
peers = ', '.join(f"{r.comp_ticker_raw} ({r.name})" for r in CP.itertuples())
comp_md = f"""# PRY.MI comparables report (relative-only, 2026-10-30)

{DISCLAIMER}

## Peer set
10 peers, all European, all tiers 1-2 (0 tier 3). Selection by comparables.select_peers with min_tier_1_2=6, max_tier_3=2, min_europe=5 (procedure section 3). Peers: {peers}.

## Multiples (median, n valid >= 6)
| Multiple | n | Median | P25 | P75 | Value/share median |
|---|---|---|---|---|---|
""" + '\n'.join(
    f"| {r.multiple} | {int(r.n_valid)} | {r.median:.2f} | {r.p25:.2f} | {r.p75:.2f} | {('n/a' if pd.isna(r.value_per_share_mid) else fmt(r.value_per_share_mid))} |"
    for r in MS.itertuples()) + f"""

Growth-adjusted P/E median {PE_ADJ['median']:.2f}x (scaled_multiple, driver 100 x growth, target fundamental growth {s3.G_FUND*100:.2f}%). ROE-adjusted P/BV median {PBV_ADJ['median']:.2f}x.

## Limitations
- Peers and tiers are judgement (agent). Index membership and ISIN checks not performed.
- Peer data from StockAnalysis (accessed 2026-11-01), not verified against filings. Growth is fundamental (ROE x retention), no consensus.
- EV multiples have n=7 (IMI, HLMA, NKT lack EV multiples in the source).
- Per-share values use the target's parent equity, debt, NCI and cash; associates not collected (EV before associates).
"""
(P / 'comparables_report.md').write_text(comp_md)

sum_md = f"""# PRY.MI relative valuation summary (published route + comparables)

## 1. Scope and route
Relative-only, stage 3. Stages 1, 2, 4 skipped_by_deviation (standing_approvals relative_only). Published Damodaran regression route, EUROPE equations (dataset regressions_multi_2026-01, as_of 2026-01-01); comparables per comparables_procedure.

## 2. Inputs
Price {fmt(PRICE)}; shares {s3.SHARES:.2f}m; market cap EUR {s3.MCAP:,.0f}m; EPS {EPS:.4f}; book value/share {BVPS:.4f}; source StockAnalysis, accessed 2026-11-01 (see relative_inputs.md).

## 3. Published regression predictions (decimal units, as_published_note)
| Multiple | Predicted | Actual | Published R2 | Value/share |
|---|---|---|---|---|
| P/E | {eq_pe['predicted']:.2f}x | {VM.loc[VM.multiple=='PE','actual_multiple'].item():.2f}x | {eq_pe['r2']:.3f} | {fmt(V['reg_pe'])} |
| P/BV (chosen) | {eq_pbv['predicted']:.2f}x | {VM.loc[VM.multiple=='PBV','actual_multiple'].item():.2f}x | {eq_pbv['r2']:.3f} | {fmt(V['reg_pbv'])} |
| EV/EBITDA | {eq_ev['predicted']:.2f}x | {VM.loc[VM.multiple=='EV/EBITDA','actual_multiple'].item():.2f}x | {eq_ev['r2']:.3f} | {fmt(V['reg_eve'])} |

Substituted input: g_eps and g_rev set to fundamental growth {s3.G_FUND*100:.2f}% (ROE x retention; approval published_route_allow_fundamental_growth = yes), labelled substituted_input in valuation_multiples.csv.

## 4. Comparables
See comparables_report.md. Primary P/E median growth-adjusted {fmt(V['pe_comp_adj'])}; P/BV median ROE-adjusted {fmt(V['pbv_comp_adj'])}; EV/EBITDA {fmt(V['ev_ebitda_comp'])}.

## 5. Model choice and result
Published model chosen by highest published R2 among PE, PBV, EV/EBITDA: P/BV, value {fmt(V['reg_chosen'])} ({pct(V['reg_chosen'])} vs price). Alternatives: P/E {fmt(V['reg_pe'])}, EV/EBITDA {fmt(V['reg_eve'])}.

## 6. Limitations
- Relative only: no DCF, no recommendation (approved deviation).
- Published R2 values are low (0.20 to 0.42); the regression is a cross-section, not a PRY-specific fit.
- Peer and tier choices are agent judgement; index and ISIN checks not done.
- Annual-report cross-check of PRY inputs not performed; figures are web-sourced.
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
    ws.append([k, v, 'stage3 PRY inputs; g_eps/g_rev = fundamental growth (substituted_input)'])
ws.append(['beta', s3.BETA, 'StockAnalysis 2026-11-01'])
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
    # check value vs published_regressions.predict output
    manual = d['constant'] + sum(t['coef'] * R['inputs'][t['variable']] for t in d['terms'])
    assert abs(manual - d['predicted']) < 1e-9, (dep, manual, d['predicted'])
    preds[dep] = manual
    ws2.append([])
wb.save(P / 'regression_valuation.xlsx')
(P.parent / 'regression_valuation.xlsx').write_bytes((P / 'regression_valuation.xlsx').read_bytes())

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
(P.parent / 'comparables_audit.xlsx').write_bytes((P / 'comparables_audit.xlsx').read_bytes())

# ---- source log, relative_summary.md --------------------------------------------------------------------------------
src = pd.DataFrame([
    ('PRY.MI StockAnalysis financials', 'https://stockanalysis.com', '2026-11-01', 'price, shares, P&L, balance sheet, multiples', 'used'),
    ('ENR/ORSTED/other candidate rows', 'outputs/*/relative/candidate_raw.csv', '2026-11-01', 'European peer candidates', 'used'),
    ('Damodaran published regressions EUROPE', 'data/ regressions_multi_2026-01 (as_of 2026-01-01)', '2026-10-30', 'PE, PBV, EV/EBITDA equations', 'used'),
    ('Damodaran country risk (Italy)', 'cache/macro/2026-10-30.json (ctryprem_global_2026-07)', '2026-10-30', 'Italy default spread 0.0152, CRP 0.0236', 'used'),
], columns=['source', 'location', 'accessed', 'used_for', 'status'])
src.to_csv(OUT / 'source_log.csv', index=False)

sumtxt = [
    'PRY.MI relative valuation (published route + comparables), batch date 2026-10-30',
    f'Price EUR {PRICE:.2f}; market cap EUR {s3.MCAP:,.0f}m; EPS {EPS:.4f}; BVPS {BVPS:.4f}',
    f'Chosen model: published P/BV regression, value EUR {V["reg_chosen"]:.2f} ({pct(V["reg_chosen"])})',
    f'Alternatives: P/E regression EUR {V["reg_pe"]:.2f}; EV/EBITDA regression EUR {V["reg_eve"]:.2f}',
    f'Comparables (10 peers): P/E growth-adj median {PE_ADJ["median"]:.2f}x = EUR {V["pe_comp_adj"]:.2f}; P/BV ROE-adj median {PBV_ADJ["median"]:.2f}x = EUR {V["pbv_comp_adj"]:.2f}',
    f'Comparables EV/EBITDA median (n=7) {EVE_MED:.2f}x = EUR {V["ev_ebitda_comp"]:.2f}',
    'Relative only (stages 1, 2, 4 skipped by approved deviation). Not investment advice.',
]
(OUT / 'relative_summary.md').write_text('\n'.join(sumtxt) + '\n')

# ---- PDF short report ----------------------------------------------------------------------------------------------
st = getSampleStyleSheet()
doc = SimpleDocTemplate(str(OUT / 'relative_report_PRY.MI.pdf'), pagesize=A4, leftMargin=40, rightMargin=40,
                        topMargin=40, bottomMargin=40)
story = [Paragraph('PRY.MI (Prysmian S.p.A.) relative valuation, batch date 2026-10-30', st['Title']),
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
                    'Substituted input: g_eps and g_rev = fundamental growth ROE x retention.', st['BodyText']),
          Paragraph('Limitations: web-sourced inputs (annual-report cross-check not done); peer tiers are judgement; '
                    'published R2 is low; index and ISIN checks pending; workbook formulas not recalculated; '
                    'human review pending.', st['BodyText'])]
doc.build(story)
print('built', len(ROWS), 'rows; chosen', round(V['reg_chosen'], 2))
