"""Adds the fields relative_report.py reads (usable, selected_basis, adjusted_median, chosen model, predictions list)
from existing stage 3 numbers. No new data; values come from multiples_summary.csv, regression_results.json and the
PRY inputs in stage3.py. Scaled rows (P/E, P/BV) use the growth/ROE-adjusted median and its quartiles.
"""
import json
from pathlib import Path

import numpy as np
import pandas as pd

import stage3 as s3

P = Path(__file__).resolve().parent
R = json.load(open(P / 'regression_results.json'))
ms = pd.read_csv(P / 'multiples_summary.csv')
adj = R['comparables_adjust']
EPS, BVPS = s3.EPS, s3.EQ / s3.SHARES

ms['usable'] = (ms['n_valid'] >= 6) & ms['median'].notna()
ms['selected_basis'] = np.where(ms['multiple'].isin(['pe', 'pbv']), 'scaled', 'raw')
ms['adjusted_median'] = np.nan
ms['adjusted_p25'] = np.nan
ms['adjusted_p75'] = np.nan
per_share = {'pe': EPS, 'pbv': BVPS}
for key in ['pe', 'pbv']:
    m = ms['multiple'] == key
    ms.loc[m, 'adjusted_median'] = adj[key]['median']
    ms.loc[m, 'adjusted_p25'] = adj[key]['p25']
    ms.loc[m, 'adjusted_p75'] = adj[key]['p75']
    ms.loc[m, 'value_per_share_low'] = adj[key]['p25'] * per_share[key]
    ms.loc[m, 'value_per_share_mid'] = adj[key]['median'] * per_share[key]
    ms.loc[m, 'value_per_share_high'] = adj[key]['p75'] * per_share[key]
ms['status'] = np.where(ms['usable'], 'usable', 'n_valid < 6')
ms['currency'] = 'EUR'
ms.to_csv(P / 'multiples_summary.csv', index=False)

vm = pd.read_csv(P / 'valuation_multiples.csv')
chosen = 'PBV'
vm['ticker'] = s3.TARGET
vm['company'] = 'Prysmian S.p.A.'
vm['current_price'] = s3.PRICE
vm['price_quote_currency'] = 'EUR'
vm['currency'] = 'EUR'
vm['chosen_model'] = np.where(vm['multiple'] == chosen, chosen, '')
vm['implied_value_per_share'] = vm['value_per_share_eur']
vm = pd.concat([vm[vm.multiple == chosen], vm[vm.multiple != chosen]], ignore_index=True)
vm.to_csv(P / 'valuation_multiples.csv', index=False)

preds = []
for dep in ['PE', 'PBV', 'EV/EBITDA']:
    d = R['regressions'][dep]
    row = vm[vm.multiple == dep].iloc[0]
    preds.append(dict(model=dep, predicted=d['predicted'], actual=row['actual_multiple'], published_r2=d['r2'],
                      value_per_share=row['value_per_share_eur']))
R['predictions'] = preds
json.dump(R, open(P / 'regression_results.json', 'w'), indent=2, default=float)

sens = pd.read_csv(P / 'sensitivities.csv')
pbv_v = float(vm.loc[vm.multiple == chosen, 'value_per_share_eur'].item())
pe_lo, pe_hi = adj['pe']['p25'] * EPS, adj['pe']['p75'] * EPS
ev = ms[ms.multiple == 'ev_ebit'].iloc[0]
ebit_lo, ebit_hi = ev['value_per_share_low'], ev['value_per_share_high']
range_lo, range_hi = min(pe_lo, ebit_lo), max(pe_hi, ebit_hi)
figs = dict(
    ticker=s3.TARGET, valuation_date=s3.DATE, current_price=s3.PRICE, shares_m=s3.SHARES, mcap_eur_m=round(s3.MCAP, 1),
    peer_count=10, tier12=10, tier3=0, europe=10, raw_pe_median=float(ms.loc[ms.multiple == 'pe', 'median'].item()),
    scaled_pe_median=adj['pe']['median'], pe_value=adj['pe']['median'] * EPS, pe_iqr=[pe_lo, pe_hi],
    ev_ebit_median=float(ev['median']), ev_ebit_value=float(ev['value_per_share_mid']), ev_ebit_iqr=[ebit_lo, ebit_hi],
    regression_pbv=pbv_v, regression_pbv_multiple=float(R['regressions']['PBV']['predicted']),
    regression_pe=float(vm.loc[vm.multiple == 'PE', 'value_per_share_eur'].item()),
    regression_ev_ebitda=float(vm.loc[vm.multiple == 'EV/EBITDA', 'value_per_share_eur'].item()),
    valuation_range_eur=[range_lo, range_hi],
    valuation_range_basis='envelope of primary P/E (growth-adjusted) IQR and EV/EBIT cross-check IQR; no averaging with regressions',
    qa=dict(source='qa_results.md (remediated)'), status='provisional - limitations disclosed',
    human_spot_check='pending', chosen_model='PBV', chosen_r2=R['regressions']['PBV']['r2'],
    ev_bridge='pre-associate: debt + NCI - cash (associates not collected, not subtracted)',
    sensitivities={r.scenario: round(float(r.change_vs_base_pct), 2) for r in sens.itertuples()
                   if not str(r.scenario).startswith('drop ')},
)
(P.parent / 'report_figures.json').write_text(json.dumps(figs, indent=2, default=float))
(P / 'report_figures.json').write_text(json.dumps(figs, indent=2, default=float))
print('chosen', round(pbv_v, 2), 'range', [round(range_lo, 2), round(range_hi, 2)], 'pe_iqr', [round(pe_lo, 2), round(pe_hi, 2)],
      'ebit_iqr', [round(ebit_lo, 2), round(ebit_hi, 2)])
