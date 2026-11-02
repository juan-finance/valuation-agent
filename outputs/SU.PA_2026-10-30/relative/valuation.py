"""SU.PA stage 3 outputs: multiples statistics, implied values, published EUROPE regression predictions."""
import json
from pathlib import Path

import numpy as np
import pandas as pd

from valuation_agent import comparables as comp
from valuation_agent import datasets, published_regressions as pr
import stage3 as s3

P = Path(__file__).resolve().parent
sel = pd.read_csv(P / 'peer_selection_raw.csv').set_index('ticker')
MULT = ['pe', 'pbv', 'ps', 'ev_ebit', 'ev_ebitda', 'ev_cf', 'ev_sales', 'ev_assets']
UNAVAIL_NOTE = {'ps': 'PS: included in required set', 'ev_cf': 'EV/CF uses reported CFO (qualified cross-check)'}

# implied values per share, EUR
def per_share_from(mult_name, value):
    if mult_name == 'pe':
        return value * s3.EPS
    if mult_name == 'pbv':
        return value * s3.EQ / s3.SHARES
    if mult_name == 'ev_ebit':
        return comp.implied_equity_from_ev(value, s3.EBIT, s3.DEBT, s3.NCI, s3.CASH) / s3.SHARES
    if mult_name == 'ev_ebitda':
        return comp.implied_equity_from_ev(value, s3.EBITDA, s3.DEBT, s3.NCI, s3.CASH) / s3.SHARES
    if mult_name == 'ps':
        return value * s3.SALES / s3.SHARES
    if mult_name == 'ev_sales':
        return comp.implied_equity_from_ev(value, s3.SALES, s3.DEBT, s3.NCI, s3.CASH) / s3.SHARES
    return float('nan')

rows, summ = [], []
for m in MULT:
    st = comp.multiple_stats(sel[m].to_numpy(), min_valid=6)
    if not st.get('usable'):
        summ.append(dict(target_ticker=s3.TARGET, multiple=m, n_valid=st.get('n_valid', 0), valuation_status='unavailable (<6 valid)'))
        continue
    vals = {k: per_share_from(m, st[k]) for k in ['median', 'p25', 'p75']}
    summ.append(dict(target_ticker=s3.TARGET, multiple=m, n_valid=st['n_valid'], median=st['median'], mean=st['mean'],
                     p25=st['p25'], p75=st['p75'], skew_flag=st['skew_flag'], value_per_share_low=vals['p25'],
                     value_per_share_mid=vals['median'], value_per_share_high=vals['p75'], currency='EUR',
                     is_primary=(m == 'pe'), valuation_status='valued'))

# fundamental adjustment for PE (driver 100*g), PBV (ROE), PS (net margin), EV/Sales (EBITDA margin)
adj = {}
adj['pe'] = comp.scaled_multiple(sel['pe'], sel['growth'], s3.G_FUND, driver_scale=100, min_valid=6)
adj['pbv'] = comp.scaled_multiple(sel['pbv'], sel['roe'], s3.ROE, min_valid=6)
adj['ps'] = comp.scaled_multiple(sel['ps'], sel['net_margin'], s3.NET_MARGIN, min_valid=6)
adj['ev_sales'] = comp.scaled_multiple(sel['ev_sales'], sel['ebitda_margin'], s3.EBITDA_M, min_valid=6)
for row in summ:
    m = row['multiple']
    if m in adj and adj[m]['available']:
        row['adjusted_multiple'] = adj[m]['median']
        row['adjusted_p25'], row['adjusted_p75'] = adj[m]['p25'], adj[m]['p75']
        row['n_valid_adjusted'] = adj[m]['n_valid']
        row['adjusted_value_mid'] = per_share_from(m, adj[m]['median'])

pd.DataFrame(summ).to_csv(P / 'multiples_summary.csv', index=False)

# comparables.csv (peer rows, per procedure section 7 schema core fields)
out = sel.reset_index()[['ticker', 'name', 'tier', 'tier_reason', 'country', 'isin', 'distance', 'mcap', 'growth', 'beta',
                        'net_debt_ebitda', 'roe', 'ebitda_margin', 'payout', 'capex_sales', 'pe', 'pbv', 'ps', 'ev_ebit',
                        'ev_ebitda', 'ev_cf', 'ev_sales', 'ev_assets', 'source_urls']].copy()
out.insert(0, 'target_ticker', s3.TARGET)
out.insert(1, 'rank', range(1, len(out) + 1))
out.insert(out.columns.get_loc('ticker') + 1, 'comp_ticker', out['ticker'])
out = out.rename(columns={'ticker': 'comp_ticker_raw', 'mcap': 'market_cap_eur_m', 'distance': 'distance_score'})
out['valuation_date'] = s3.DATE
out['earnings_basis'] = 'FY2025'
out['growth_basis'] = 'fundamental ROE x (1-payout); web route, no consensus'
out['isin'] = out['isin'].fillna('not verified')
out['membership'] = 'IEUR MSCI Europe IMI proxy; index/ISIN verification pending'
out.to_csv(P / 'comparables.csv', index=False)

# regression (published EUROPE equations, France listing) ------------------------------------------------------
SU_INPUTS = dict(beta=s3.BETA, g_eps=s3.G_EPS_CONS, g_rev=s3.G_REV_CONS, payout=s3.PAYOUT_DECLARED,
                 roe=s3.ROE_CLOSING, roic=s3.ROIC, dfr=s3.DFR, tax_rate=s3.TAX, oper_margin=s3.EBIT / s3.SALES)
regs = {}
for dep in ['PE', 'PBV', 'EV/EBITDA']:
    eq, res, *_ = datasets.equation_for('France', dep, s3.DATE)
    pred = pr.predict(eq, SU_INPUTS, 'as_published_note')
    uses_dfr_tax = any(t.variable in ('dfr', 'tax_rate') for t in eq.terms)
    alt = pr.predict(eq, SU_INPUTS, 'dfr_tax_percent_points') if uses_dfr_tax else None
    regs[dep] = dict(region=eq.region, r2=eq.r2, predicted=pred, alt_units=alt, dataset=res.dataset.dataset_id,
                     vintage=res.dataset.vintage, as_of=res.dataset.as_of_date, sha256=res.dataset.sha256,
                     variables=[t.variable for t in eq.terms], constant=eq.constant,
                     terms=[dict(variable=t.variable, coef=t.coef, tstat=t.tstat) for t in eq.terms])

def reg_value(dep, pred):
    if dep == 'PE':
        return pred * s3.EPS
    if dep == 'PBV':
        return pred * s3.EQ / s3.SHARES
    return comp.implied_equity_from_ev(pred, s3.EBITDA, s3.DEBT, s3.NCI, s3.CASH) / s3.SHARES

vm = []
for dep, d in regs.items():
    vps = reg_value(dep, d['predicted'])
    actual = {'PE': s3.PRICE / s3.EPS, 'PBV': s3.MCAP / s3.EQ,
              'EV/EBITDA': (s3.MCAP + s3.DEBT + s3.NCI - s3.CASH) / s3.EBITDA}[dep]
    vm.append(dict(target_ticker=s3.TARGET, model=f'published_damodaran_EUROPE_{d["vintage"]}', multiple=dep,
                   predicted_multiple=d['predicted'], actual_multiple=actual, deviation=actual / d['predicted'] - 1,
                   value_per_share_eur=vps, published_r2=d['r2'], n_a='n/a_published_route',
                   classification='Not classified (no SEy published)', units_policy='as_published_note (decimal)',
                   units_unverified='no (decimal per standing approval)', equation_dataset_id=d['dataset'],
                   substituted_input='none: analyst consensus g_eps 20.40% / g_rev 11.56% (3Y, vendor statistics) used as published'))
pd.DataFrame(vm).to_csv(P / 'valuation_multiples.csv', index=False)
json.dump({'regressions': regs, 'inputs': SU_INPUTS, 'comparables_adjust': {k: v for k, v in adj.items()}},
          open(P / 'regression_results.json', 'w'), indent=2, default=float)
print(pd.DataFrame(summ)[['multiple', 'n_valid', 'median', 'p25', 'p75', 'value_per_share_mid']].to_string())
print(pd.DataFrame(vm)[['multiple', 'predicted_multiple', 'actual_multiple', 'deviation', 'value_per_share_eur', 'published_r2']].to_string())
print(adj)
