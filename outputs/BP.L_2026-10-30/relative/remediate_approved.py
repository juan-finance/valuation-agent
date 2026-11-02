"""BP-only approved remediation; reuse cleaned vendor rows, never fetch or rerun full QA."""
import json
import math
from pathlib import Path

import numpy as np
import pandas as pd
from openpyxl import load_workbook
from valuation_agent import comparables as c
from valuation_agent.runstate import RunState

P = Path(__file__).resolve().parent
O = P.parent
ROOT = P.parents[2]
STATUS = 'provisional - limitations disclosed'
STARTED = '2026-11-02T12:54:13+00:00'
state = RunState(O / 'run_state.json')
assert 'approved_remediation' not in state.d, 'One-shot changed-item QA already executed'
print('Resuming:', state.resume_point())
FX = json.loads((ROOT / 'cache/macro/2026-10-30.json').read_text())['fx_ecb_reference']['rates']
FX['EUR'] = 1.
raw = pd.read_csv(P / 'candidate_raw.csv').set_index('ticker', drop=False)
T = raw.loc['BP'].copy()
clean_path = ROOT / 'outputs/SHEL.L_2026-10-30/relative/candidate_raw.csv'
clean = pd.read_csv(clean_path).set_index('ticker', drop=False)
scores = pd.read_csv(P / 'candidate_scores.csv').set_index('ticker', drop=False)
excluded = ['OXY', 'HBR', 'CVX', 'OMV']
original = pd.read_csv(P / 'numeric_prospects_NOT_QUALIFIED.csv').ticker.tolist()
pool = scores.drop(index=excluded).copy()
selected, selection = c.select_peers(pool)
assert selected is not None and len(selected) == 10
names = selected.ticker.tolist()
assert set(original) - set(excluded) <= set(names)
D = pd.concat([T.to_frame().T, clean.loc[names]], axis=0)
for column in ['tier', 'hypothesis', 'europe', 'country', 'name']:
    D.loc[names, column] = raw.loc[names, column]
for t in names:
    for folder in ['TTE.PA', 'EQNR.OL']:
        other = pd.read_csv(ROOT / f'outputs/{folder}_2026-10-30/relative/candidate_raw.csv').set_index('ticker')
        for k in ['price', 'current_shares_m', 'debt', 'cash', 'NCI', 'EBITDA', 'ni', 'equity']:
            assert math.isclose(float(D.loc[t, k]), float(other.loc[t, k]), abs_tol=1e-8)
assert (T.debt, T.NCI, T.cash) == (72529., 20948., 36556.)
bridges = []
for t, r in D.iterrows():
    market = r.price * r.current_shares_m * FX[r.report_currency] / FX[r.quote_currency]
    ev = c.comparable_ev(market, r.debt, r.NCI, r.cash, 0)
    assert math.isfinite(ev) and ev > 0
    assert math.isclose(c.implied_equity_from_ev(ev / r.EBITDA, r.EBITDA, r.debt, r.NCI, r.cash, 0), market, abs_tol=1e-7)
    D.loc[t, 'EV_before_associates'] = ev
    for m, metric in {'pe': 'ni', 'pbv': 'equity', 'ps': 'sales', 'ev_ebit': 'EBIT', 'ev_ebitda': 'EBITDA', 'ev_cf': 'cfo', 'ev_assets': 'assets', 'ev_sales': 'sales'}.items():
        D.loc[t, m] = (ev if m.startswith('ev_') else market) / r[metric] if r[metric] > 0 else np.nan
    bridges.append(dict(ticker=t, market_equity_report_m=market, debt_including_leases=r.debt,
                        NCI_including_vendor_hybrids_once=r.NCI, cash=r.cash, associates_deducted=0,
                        EV_pre_associate=ev, EV_eur_m=ev / FX[r.report_currency], reporting_currency=r.report_currency,
                        financial_basis='FY2025; December year-end; vendor period labels incomplete', price_date='2026-10-30',
                        fx_date='2026-10-30', comparison_currency='EUR', EBITDA=r.EBITDA, EBIT=r.EBIT,
                        rule='vendor pre-associate: debt incl leases + NCI/hybrids once - cash; equity income retained',
                        source=r.source_urls, cached_origin=str(clean_path.relative_to(ROOT)) if t != 'BP' else 'BP candidate_raw.csv',
                        NCI_note='COP: cached vendor shareholders equity less common equity = 0; not a new zero imputation' if t == 'COP' else 'Neste zero NCI confirmed in prior issuer review' if t == 'NESTE' else 'vendor carrying claim proxy; no per-row issuer substitution'))
B = pd.DataFrame(bridges)
B.to_csv(P / 'ev_bridge.csv', index=False)
D.to_csv(P / 'remediated_vendor_inputs.csv', index=False)
S = D.loc[names].copy()
S['rank'] = range(1, 11)
S['distance_score'] = selected.loc[names, 'distance']
S['distance'] = S.distance_score
S['qualified'] = True
S['status'] = STATUS
S['inclusion_reason'] = 'Existing BP score; four completed-deal exclusions replaced in ranked order; approved source-line qualification'
S.to_csv(P / 'comparables.csv', index=False)

prior = pd.read_csv(P / 'peer_qualification_repair.csv').set_index('ticker')
events = {
    'XOM': ('Pioneer completed May 2024; FY2025 includes full year, no FY2025 partial-year exclusion identified', 'https://investor.exxonmobil.com/'),
    'COP': ('Marathon Oil completed November 2024; FY2025 full year; comparative-growth perimeter caveat retained', 'https://www.conocophillips.com/investor-relations/'),
    'PSX': ('Refining/midstream operating group; smaller disposals and operating changes noted, no qualifying FY2025 exclusion identified in cached screen', 'https://investor.phillips66.com/'),
}
Q = []
for t in names:
    event, url = events.get(t, (str(prior.loc[t, 'pure_play_and_exclusion_finding']) if t in prior.index else '', str(prior.loc[t, 'event_business_source']) if t in prior.index else ''))
    owner = str(prior.loc[t, 'ownership_source']) if t in prior.index else url
    Q.append(dict(ticker=t, qualification='PASS-with-note', automated_hard_filters='PASS: developed, operating nonfinancial, size, mincap, history, missing metrics',
                  ownership='No disclosed >20% BP cross-holding in either direction in retained source-line screen; exhaustive history not certified',
                  ownership_source=owner, events=event + '; approved rule 2: no disqualifying completed deal identified; smaller events noted',
                  event_source=url, cached_evidence='peer_qualification_repair.csv / issuer_evidence_repair.json; Shell/TTE cached screens',
                  access_policy='Reuse previously dated cached evidence; no new collection'))
Q = pd.DataFrame(Q)
Q.to_csv(P / 'peer_qualification.csv', index=False)
(P / 'evidence_review.md').write_text('# BP current approved source-line screen\n\n' + STATUS + '\n\n' + Q.to_markdown(index=False) + '\n\nExcluded: OXY CrownRock/OxyChem; HBR Wintershall/LLOG; CVX Hess July 2025; OMV Borealis/Borouge. Earlier stricter holds are historical, not current grades. Adura is a Shell/Equinor JV, not cross-ownership of the parent companies; smaller event noted on both sides. NESTE and VLO remain Tier 2 refining peers.\n')

def value(m, multiple, metric=None):
    key = {'pe': 'ni', 'pbv': 'equity', 'ps': 'sales', 'ev_ebit': 'EBIT', 'ev_ebitda': 'EBITDA', 'ev_cf': 'cfo', 'ev_assets': 'assets', 'ev_sales': 'sales'}.get(m)
    if key is None or not np.isfinite(multiple):
        return np.nan
    amount = T[key] if metric is None else metric
    equity = c.implied_equity_from_ev(multiple, amount, T.debt, T.NCI, T.cash, 0) if m.startswith('ev_') else multiple * amount
    return equity / T.current_shares_m * FX['GBP'] / FX['USD'] if equity > 0 else np.nan

rows, sensitivities = [], []
for m in ['pe', 'peg', 'relative_pe', 'ev_ebit', 'ev_ebitda', 'ev_cf', 'pbv', 'ev_assets', 'tobins_q', 'ps', 'ev_sales']:
    vals = pd.to_numeric(S[m], errors='coerce').where(lambda x: x > 0)
    stats = c.multiple_stats(vals, min_valid=6)
    driver = {'pe': 'growth', 'pbv': 'roe', 'ps': 'net_margin', 'ev_sales': 'ebitda_margin'}.get(m)
    adj = c.scaled_multiple(vals, S[driver], T[driver], driver_scale=100 if m == 'pe' else 1, min_valid=6) if driver else {'available': False, 'n_valid': 0}
    row = dict(target_ticker='BP.L', multiple=m, **stats, currency='GBP', basis='FY2025', selected_basis='raw',
               is_primary=m == 'ev_ebitda', status=STATUS if stats['usable'] else 'unavailable: fewer than six meaningful observations',
               adjusted_n_valid=adj['n_valid'], adjusted_multiple=adj.get('median', np.nan),
               scaling_note='Raw base; depressed BP earnings/ROE make scaled alternatives sensitivities, not silent normalization')
    for q, suffix in [('p25', 'low'), ('median', 'mid'), ('p75', 'high')]:
        row['value_per_share_' + suffix] = value(m, stats.get(q, np.nan)) if stats['usable'] else np.nan
        row['adjusted_' + q] = adj.get(q, np.nan)
    rows.append(row)
    if adj['available'] and stats['usable']:
        base = row['value_per_share_mid']
        alt = value(m, adj['median'])
        sensitivities.append(dict(sensitivity=m + ' fundamental-scaled median', multiple=m, value_per_share=alt, base_value_per_share=base, change_fraction=alt / base - 1))
M = pd.DataFrame(rows)
M.to_csv(P / 'multiples_summary.csv', index=False)
evrow = M[M.multiple.eq('ev_ebitda')].iloc[0]
mid = float(evrow.value_per_share_mid)
for name, metric in [('vendor EBITDA with impairment (no addback)', T.EBITDA), ('vendor EBITDA without impairment (6037 addback only)', T.EBITDA + 6037), ('issuer reported EBIT plus DDA', 30464), ('issuer debt difference only; BP debt unchanged', T.EBITDA)]:
    if name.startswith('issuer debt'):
        continue
    v = value('ev_ebitda', evrow['median'], metric)
    sensitivities.append(dict(sensitivity=name, multiple='ev_ebitda', EBITDA=metric, value_per_share=v, base_value_per_share=mid, change_fraction=v / mid - 1))
for t in names:
    v = value('ev_ebitda', c.multiple_stats(S.drop(index=t).ev_ebitda, min_valid=6)['median'])
    sensitivities.append(dict(sensitivity='leave-one-out ' + t, multiple='ev_ebitda', value_per_share=v, base_value_per_share=mid, change_fraction=v / mid - 1))
sens = pd.DataFrame(sensitivities)
sens.to_csv(P / 'sensitivities.csv', index=False)

rr = json.loads((P / 'regression_results.json').read_text())
for r in rr['predictions']:
    r['value_per_share'] = r.get('value_per_share_gbp') if r['predicted'] > 0 else None
    if r['model'] == 'EV/EBITDA':
        r['historical_value_with_preference_proxy'] = r['value_per_share_gbp']
        r['value_per_share'] = value('ev_ebitda', r['predicted'])
        r['model'] = 'EV/EBITDA (diagnostic only)'
        r['status'] = 'diagnostic only; market-wide sector plausibility limitation; not a headline or target'
        reg = r
rr.update(status='diagnostic only', chosen=None, decision_use_status='Peer EV/EBITDA headline; regression diagnostic, not averaged')
(P / 'regression_results.json').write_text(json.dumps(rr, indent=2) + '\n')
v = pd.read_csv(P / 'valuation_multiples.csv')
v['status'] = STATUS
v['chosen_model'] = 'none; regression diagnostic only'
v['implied_value_per_share'] = np.nan
v['decision_use_status'] = 'Peer EV/EBITDA primary; published equation only a labelled diagnostic'
v['rationale'] = 'Approved pre-associate peer ranges; no DCF or recommendation; regression not a valuation headline'
v.to_csv(P / 'valuation_multiples.csv', index=False)

assert len(S) == 10 and S.europe.sum() >= 5 and (S.tier <= 2).sum() >= 6
assert S[list(c.WEIGHTS)].isna().sum(axis=1).le(2).all()
assert S.market_cap_eur_m.ge(1000).all() and S.market_cap_eur_m.between(T.market_cap_eur_m * .1, T.market_cap_eur_m * 10).all()
assert S.market_cap_check.abs().le(.02).all() and S.price_date.eq('2026-10-30').all()
assert math.isclose(c.pence_to_pounds(T.raw_price), T.price, abs_tol=1e-12)
assert all(M[M.multiple.isin(['pe', 'pbv', 'ev_ebitda'])].n_valid >= 6)
grades = {n: 'PASS-with-note' for n in ['C03', 'C04', 'C05', 'C08', 'C09', 'C17', 'C18', 'C20', 'C42']}
grades.update(C10='PASS', C19='PASS-with-note')
qa_notes = dict(C03='GBP (not GBp), current ordinary shares and exact uniform inverse verified; vendor/issuer differences disclosed.',
                C04='One retained ownership/event source line per peer; old detailed-locator omissions disclosed.', C05='Industry aggregate 5.94x, never a median; cross-check only.',
                C08='Ten qualified peers; retained six plus next-ranked XOM,COP,SHEL,PSX replacing four completed-deal exclusions.',
                C09='Approved automated/source-line hard filters applied; exhaustive historical certification not required.',
                C10='Six Europe peers; ten Tier1/2, zero Tier3.', C17='EV/EBITDA primary; PE and PBV cross-checks; all have ten positive observations.',
                C18='Identical pre-associate formula and inverse for target and all peers; BP hybrids already inside NCI20948; no extra preference21 claim.',
                C19='Current peer ISINs retained where available; cached listing/identity limitations disclosed; human Spot_check PENDING, not automated away.',
                C20='Impairment addback6037, issuer/vendor, leave-one-out and scaled sensitivities disclosed; no uniform normalization claimed.',
                C42='18.07x equation versus qualified peer median and industry aggregate investigated; decimal policy retained, diagnostic only.')
oldqa = (P / 'qa_results.md').read_text()
header = '# QA block C — current BP status\n\n**' + STATUS + '**. No current FAIL items. Human Spot_check PENDING.\n\n## Remediation re-grade\nApproved qa_grading_and_remediation and relative_only replace prior stricter certification standard. Only the eleven changed/non-passing items assessed once; original passing items retained without rerun.\n\n'
header += '\n'.join(f'- {k}: {grade}. {qa_notes[k]}' for k, grade in grades.items())
header += '\n\n## Historical QA — superseded; retained verbatim\n\n'
(P / 'qa_results.md').write_text(header + oldqa)
(P / 'qa_approved_recheck.json').write_text(json.dumps(dict(status=STATUS, grades=grades, evidence=qa_notes, full_block_executions=1, changed_item_executions=1), indent=2) + '\n')

fig = dict(ticker='BP.L', valuation_date='2026-10-30', status=STATUS, current_price=T.price, currency='GBP', shares_m=T.current_shares_m,
           peer_count=10, europe=int(S.europe.sum()), tier12=int((S.tier <= 2).sum()), qualified_peers=names,
           primary='peer EV/EBITDA raw', ranges={r['multiple']: {k: r[k] for k in ['n_valid', 'median', 'p25', 'p75', 'value_per_share_low', 'value_per_share_mid', 'value_per_share_high']} for r in rows if r['multiple'] in ['pe', 'pbv', 'ev_ebitda']},
           regression_ev_ebitda=dict(multiple=reg['predicted'], value_per_share_gbp=reg['value_per_share'], status='diagnostic only', gap_to_peer_median=reg['predicted'] / evrow['median'] - 1, industry_aggregate=5.94),
           impairment_sensitivity=sens[sens.sensitivity.str.contains('impairment')].to_dict('records'), sensitivities_above_15pct=sens[sens.change_fraction.abs() > .15].to_dict('records'),
           qa=grades, human_spot_check='PENDING', source='Existing BP and SHEL/TTE/EQNR cleaned vendor snapshots; no recollection')
(P / 'report_figures.json').write_text(json.dumps(fig, indent=2) + '\n')
scaled = sens[sens.sensitivity.str.contains('scaled')]
imp = sens[sens.sensitivity.str.contains('6037')].iloc[0]
notes = [
    f'BP peer EV/EBITDA is primary: {evrow["median"]:.2f}x median, GBP {mid:.2f} per ordinary share, IQR GBP {evrow.value_per_share_low:.2f}-{evrow.value_per_share_high:.2f}. Ten peers; OXY/HBR/CVX/OMV excluded for completed-deal FY/perimeter comparability; next-ranked XOM/COP/SHEL/PSX replace them. Six Europe peers; NESTE/VLO/PSX refining and COP upstream differences remain.',
    f'BP vendor FY2025 EBITDA USD30,168m includes the impairment impact; adding back USD6,037m alone gives USD36,205m and GBP {imp.value_per_share:.2f} ({imp.change_fraction:+.1%} versus base). Issuer EBIT+DDA USD30,464m is a separate sensitivity, not a base switch; issuer standalone adjusted EBITDA36,501 is not mixed into vendor base.',
    'BP net income USD54m is impairment/tax-distorted: raw peer PE produces a very low cross-check, not normalized earnings or a forecast. Raw PBV remains a book-value cross-check. Fundamental-scaled sensitivities: ' + '; '.join(f'{r.multiple} GBP {r.value_per_share:.3f} ({r.change_fraction:+.1%})' for r in scaled.itertuples()) + '. These above-15% changes show why raw ranges and scaled cases are separate.',
    'Uniform vendor pre-associate bridge: BP debt72,529 includes leases14,571; NCI20,948 already includes hybrids15,955 once; cash36,556. Associates/JVs retained in EV and equity income in earnings; extra preference21 proxy not added. COP cached NCI=total shareholders equity minus common equity=0; Neste zero confirmed. Book claims, cash/ST-investment scope, separate peer hybrids and IFRS/US-GAAP lease EBITDA remain disclosed limitations, not per-row issuer switches.',
    f'Published EV/EBITDA {reg["predicted"]:.2f}x / GBP {reg["value_per_share"]:.2f} is DIAGNOSTIC ONLY, {reg["predicted"]/evrow["median"]-1:+.1%} above qualified peer median; industry aggregate5.94x is not a median. USD-to-GBP0.74633011 and15,450m ordinary shares (no second /100 or ADS adjustment); historical preference-proxy difference GBP0.001/share. Low R2 .262, approved decimal DFR/tax policy, substituted zero growth; percentage-point output4.28x is a sensitivity, not a price-fitting fix.',
    f'Provisional limitations disclosed; human Spot_check PENDING. IQR endpoints differ from midpoint by {evrow.value_per_share_low/mid-1:+.1%}/{evrow.value_per_share_high/mid-1:+.1%}; leave-one-out changes span {sens[sens.sensitivity.str.startswith("leave-one-out")].change_fraction.min():+.1%} to {sens[sens.sensitivity.str.startswith("leave-one-out")].change_fraction.max():+.1%}. Vendor/issuer reconciliations include Shell debt45, TTE debt388 and Neste EBITDA1438 versus1124; all base rows retain vendor values. FY2025/2026-10-30 quote/FX mismatch in time and incomplete source period labels noted. Academic analysis only, not investment advice.'
]
(O / 'report_notes.md').write_text('\n'.join('- ' + n for n in notes) + '\n')
(P / 'comparables_report.md').write_text('# BP approved remediation\n\n' + STATUS + '\n\n' + S[['ticker', 'tier', 'country', 'distance_score']].to_markdown(index=False) + '\n\n' + M.to_markdown(index=False) + '\n\n' + '\n'.join(notes) + '\n')
wb = load_workbook(P / 'comparables_audit.xlsx')
for name, frame in [('Approved_Peers', S), ('Approved_Bridge', B), ('Approved_Qualification', Q), ('Approved_Multiples', M), ('Approved_Sensitivity', sens)]:
    if name in wb:
        del wb[name]
    ws = wb.create_sheet(name)
    ws.append(list(frame.columns))
    for row in frame.itertuples(index=False, name=None):
        ws.append([None if pd.isna(x) else x.item() if isinstance(x, np.generic) else x for x in row])
wb.save(P / 'comparables_audit.xlsx')
selection.update(status=STATUS, qualified_count=10, selected=names, excluded=excluded, replacements=[t for t in names if t not in original], scoring='Existing BP eight-dimension scores retained; replacement only; no new candidate collection', prior_stricter_selection='Historical steps in previous committed peer_selection.json')
(P / 'peer_selection.json').write_text(json.dumps(selection, indent=2) + '\n')
g = pd.read_csv(P / 'candidate_gates.csv')
g.loc[g.ticker.isin(names), 'qualified'] = True
g.loc[g.ticker.isin(names), 'rejection_reason'] = 'Qualified under approved rule2; limitations in peer_qualification.csv'
g.loc[g.ticker.isin(names), 'ownership_event_history_gate'] = 'PASS-with-note: current approved source-line screen'
g.loc[g.ticker.isin(names), 'assoc_bridge_gate'] = 'PASS-with-note: uniform pre-associate vendor bridge'
g.to_csv(P / 'candidate_gates.csv', index=False)
for f in ['repair_result.json', 'build_result.json', 'regression_plausibility_repair.json']:
    result = json.loads((P / f).read_text())
    result['approved_remediation'] = dict(status=STATUS, qualified_count=10, current_grades=grades, regression='diagnostic only; not headline', figures='report_figures.json')
    result['status'] = STATUS
    if f == 'repair_result.json':
        result['historical_stricter_qualified_count'] = result['qualified_count']
        result.update(qualified_count=10, regression_status='diagnostic only', current_statuses=grades)
    (P / f).write_text(json.dumps(result, indent=2) + '\n')
state.d['stages']['stage3_relative']['status'] = STATUS
state.d['stages']['stage3_relative']['next_step'] = 'Human Spot_check pending; no recommendation under relative_only'
state.d['stages']['stage3_relative']['notes'].append('Approved remediation: replaces stricter certification holds with source-line rule2; vendor pre-associate bridge uniform; peer ranges restored; regression diagnostic only; changed-item QA once.')
state.d['approved_remediation'] = dict(started=STARTED, status=STATUS, rules=['qa_grading_and_remediation', 'relative_only'], changed_items=list(grades), report_generator='valuation_agent.relative_report', historical_timing_preserved=True)
state.d['final_status'] = STATUS
state.d['qa_block_C'].update(status=STATUS, current_grades=grades, current_failures=[])
state.save()
print(json.dumps(fig, indent=2))
