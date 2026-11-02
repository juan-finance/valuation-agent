"""NESTE.HE remediation: business-description peer review, re-grade under approved rules,
FY2023-25 average-EBITDA sensitivity + EV/Sales cross-check, status provisional - limitations disclosed."""
import json
from pathlib import Path
import numpy as np
import pandas as pd
from valuation_agent import comparables as c

P = Path(__file__).resolve().parent
ROOT = P.parents[2]
D = pd.read_csv(P / 'candidate_gates.csv').set_index('ticker', drop=False)
T = D.loc['NESTE'].copy()

# --- 1. Business-description peer review -------------------------------------
# SPM (Saipem) and SUBC (Subsea7) are oilfield engineering/offshore services, not refiners,
# renewable-fuels or downstream businesses -> replaced by next-ranked qualifying candidates.
REMOVE = {'SPM': 'Saipem - oil & gas engineering and drilling services, not a refiner/renewable-fuels/downstream peer',
          'SUBC': 'Subsea7 - offshore energy services, not a refiner/renewable-fuels/downstream peer'}
# Recompute pool scoring with the same library call used in build.py to get consistent distances.
pool = D[(D.gate_result == 'numeric eligible; evidence review detailed in evidence_review.md')].copy()
band = pool[(pool.market_cap_eur_m >= T.market_cap_eur_m * .1) & (pool.market_cap_eur_m <= T.market_cap_eur_m * 10)]
scores, params = c.similarity_scores(band, T)
band = band.join(scores)
ranked = band.sort_values('distance')
# Qualifying business test: refiner, renewable-fuels or downstream/integrated-with-refining.
BUSINESS_OK = {'GALP', 'VLO', 'PSX', 'MPC', 'SHEL', 'BP', 'TTE', 'ENI', 'REP', 'OMV', 'EQNR', 'XOM', 'CVX'}
kept = [t for t in pd.read_csv(P / 'comparables.csv').ticker if t not in REMOVE]
replacements = [t for t in ranked.ticker if t in BUSINESS_OK and t not in kept][: len(REMOVE)]
print('replacements:', replacements)
assert len(replacements) == 2
sel = band[band.ticker.isin(kept + replacements)].copy()
sel = sel.sort_values('distance').reset_index(drop=True)
sel['rank'] = sel.index + 1
sel['target_ticker'] = 'NESTE.HE'
sel['comp_ticker'] = sel.ticker
sel['comp_name'] = sel['name']
sel['comp_isin'] = sel['isin']
sel['distance_score'] = sel.distance
sel['effective_weight_coverage'] = sel.weight_coverage
sel['market_cap_eur'] = sel.market_cap_eur_m * 1e6
sel['inclusion_reason'] = sel.hypothesis
sel['source_route'] = 'web_minimum'
sel['metric_fallbacks'] = 'fundamental growth, income-statement EBITDA, FY closing EV balances'
ident = dict(zip(pd.read_csv(P / 'comparables.csv').comp_ticker, pd.read_csv(P / 'comparables.csv').identity_source))
ident.update({'CVX': 'https://www.chevron.com/investors', 'XOM': 'https://investor.exxonmobil.com/',
              'MPC': 'https://www.marathonpetroleum.com/Investors/', 'GALP': 'https://www.galp.com/corp/en/investors'})
sel['identity_source'] = [ident[t] for t in sel.ticker]
sel['flags'] = 'DRAFT: human review pending; EV pre-LT-investments qualified only; NCI book proxy; beta benchmark/frequency unavailable; reported FY2025 uncalendarized; IFRS/US GAAP differences'
sel.to_csv(P / 'comparables.csv', index=False)
D['selected'] = D.index.isin(sel.ticker)
for t in REMOVE:
    D.loc[t, 'gate_result'] = 'business-description review: ' + REMOVE[t] + '; replaced by next-ranked qualifying candidate'
for t in replacements:
    D.loc[t, 'gate_result'] = 'numeric eligible + business-description review (refiner/integrated-downstream); replaces services peer on remediation'
D.to_csv(P / 'candidate_gates.csv', index=False)

# --- 2. Recompute multiples summary on the remediated peer set ----------------
def value(name, m, metric=None):
    if not np.isfinite(m):
        return np.nan
    key = {'pe': 'ni', 'peg': 'ni', 'pbv': 'equity', 'ps': 'sales', 'ev_ebit': 'EBIT',
           'ev_ebitda': 'EBITDA', 'ev_cf': 'cfo', 'ev_assets': 'assets', 'ev_sales': 'sales'}.get(name)
    if key is None:
        return np.nan
    if name == 'peg':
        m *= 100 * T.growth
    eq = c.implied_equity_from_ev(m, T[key] if metric is None else metric, T.debt, T.NCI, T.cash, 0) \
        if name.startswith('ev_') else m * (T[key] if metric is None else metric)
    return eq / T.current_shares_m if eq > 0 else np.nan

summary = []
for name in ['pe', 'peg', 'relative_pe', 'ev_ebit', 'ev_ebitda', 'ev_cf', 'pbv', 'ev_assets', 'tobins_q', 'ps', 'ev_sales']:
    vals = sel[name].where(sel[name] > 0)
    stats = c.multiple_stats(vals, min_valid=6)
    driver = {'pe': 'growth', 'pbv': 'roe', 'ps': 'net_margin', 'ev_sales': 'ebitda_margin'}.get(name)
    adj = c.scaled_multiple(vals, sel[driver], T[driver], driver_scale=100 if name == 'pe' else 1, min_valid=6) \
        if driver else dict(available=False, n_valid=0)
    chosen = adj if adj['available'] else stats
    row = dict(target_ticker='NESTE.HE', multiple=name, **stats,
               adjusted_multiple=adj.get('median', np.nan), adjusted_n_valid=adj['n_valid'], currency='EUR',
               basis='FY2025', is_primary=name == 'ev_ebitda',
               status='draft qualified cross-check' if name.startswith('ev_') else 'draft' if stats['usable'] else 'unavailable',
               flags='EV before LT-investment perimeter: qualified only; supplemental' if name.startswith('ev_')
               else 'matching index PE unavailable' if name == 'relative_pe' else 'replacement costs unavailable' if name == 'tobins_q' else '')
    for q, s in [('p25', 'low'), ('median', 'mid'), ('p75', 'high')]:
        row['value_per_share_' + s] = value(name, chosen.get(q, np.nan)) if stats['usable'] else np.nan
        row['raw_value_' + s] = value(name, stats.get(q, np.nan)) if stats['usable'] else np.nan
        row['adjusted_' + q] = adj.get(q, np.nan)
    row['upside'] = row['value_per_share_mid'] / T.price - 1
    summary.append(row)
S = pd.DataFrame(summary)
S['n_valid_adjusted'] = S.adjusted_n_valid
S['valuation_status'] = S.status
S['selected_basis'] = ['scaled' if n >= 6 else 'raw' for n in S.adjusted_n_valid]
for suffix, qq in [('low', 'p25'), ('mid', 'median'), ('high', 'p75')]:
    S['unadjusted_value_' + suffix] = S['raw_value_' + suffix]
    S['adjusted_value_' + suffix] = [value(n, S.loc[i, 'adjusted_' + qq]) if np.isfinite(S.loc[i, 'adjusted_' + qq]) else np.nan
                                     for i, n in enumerate(S.multiple)]
S.to_csv(P / 'multiples_summary.csv', index=False)
prim = S[S.multiple.eq('ev_ebitda')].iloc[0]

# --- 3. Sensitivities: keep existing, add FY2023-25 avg-EBITDA and EV/Sales ----
sens = pd.read_csv(P / 'sensitivities.csv')
ev_med = prim['median']
avg_ebitda = (2285 + 700 + 1124) / 3  # vendor income-statement EBITDA FY2023/24/25
new_rows = [
    dict(sensitivity='FY2023-25 average vendor EBITDA (2285/700/1124=1369.7), cyclicality diagnostic',
         value_per_share=value('ev_ebitda', ev_med, avg_ebitda), n_valid=prim['n_valid'], removed=''),
    dict(sensitivity='EV/Sales cross-check, peer median scaled basis',
         value_per_share=S[S.multiple.eq('ev_sales')].iloc[0]['value_per_share_mid'], n_valid=10, removed=''),
]
sens = pd.concat([sens, pd.DataFrame(new_rows)], ignore_index=True)
sens.to_csv(P / 'sensitivities.csv', index=False)

# --- 4. peer_selection.json: record remediation -------------------------------
steps = json.loads((P / 'peer_selection.json').read_text())
steps.append(dict(step='remediation_business_review', date='2026-11-01',
                  removed=REMOVE,
                  added={t: f'next-ranked qualifying candidate (distance {float(band[band.ticker.eq(t)].distance.iloc[0]):.4f}); refiner/integrated-downstream' for t in replacements},
                  rule='qa_grading_and_remediation: peer must be refiner, renewable-fuels or downstream; services/E&P replaced by next-ranked qualifying pool candidate; World expansion already approved',
                  events_notes='CVX completed Hess acquisition 2025-07 (~$53bn EV <25% of CVX EV, noted not excluded); XOM no >25%-EV perimeter event in FY2025 (Pioneer closed FY2024, noted); no cross-holding >20% with target in either direction for CVX/XOM',
                  final_peers=sel.ticker.tolist()))
(P / 'peer_selection.json').write_text(json.dumps(steps, indent=2, default=str) + '\n')

print(json.dumps(dict(peers=sel.ticker.tolist(),
                    primary_EVEBITDA_mid=float(prim.value_per_share_mid),
                    primary_p25=float(prim.value_per_share_low),
                    primary_p75=float(prim.value_per_share_high),
                    upside=float(prim.upside),
                    avg_ebitda_value=float(new_rows[0]['value_per_share'])), indent=2))
