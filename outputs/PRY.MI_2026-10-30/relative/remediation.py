"""PRY.MI remediation checks (PENDING items): pool, ISIN format, EV random checks, sensitivities, dataset sha256.

Everything reads existing files in relative/ and the dated cache; no new web collection.
"""
import hashlib
import json
import random
from pathlib import Path

import numpy as np
import pandas as pd

from valuation_agent import comparables as comp
from valuation_agent import datasets
from valuation_agent import published_regressions as pr
import stage3 as s3
from pool import load, f

P = Path(__file__).resolve().parent
OUT = P.parent
ROOT = P.parents[2]

elig = pd.read_csv(P / 'pool_eligible.csv').set_index('ticker')
rej = pd.read_csv(P / 'pool_rejected.csv')
sel = pd.read_csv(P / 'peer_selection_raw.csv').set_index('ticker')
dims = list(comp.WEIGHTS)

# ---------------------------------------------------------------- (1) fresh 20-30 candidate pool with reasons
scored, _ = comp.similarity_scores(elig[dims], dict(growth=s3.G_FUND, beta=s3.BETA, net_debt_ebitda=s3.NET_DEBT_EBITDA,
                                                   roe=s3.ROE, ebitda_margin=s3.EBITDA_M, payout=s3.PAYOUT,
                                                   capex_sales=s3.CAPEX_SALES, ln_mcap=float(np.log(s3.MCAP))))
rank = scored.sort_values('distance')
pool_rows = []
for i, (t, r) in enumerate(rank.iterrows(), 1):
    pool_rows.append(dict(ticker=t, name=elig.loc[t, 'name'] if 'name' in elig else '', source='cache candidate_raw (eligible)',
                          distance=round(r['distance'], 4), status='selected' if t in sel.index else 'eligible, not selected (rank below top 10)',
                          reason='' if t in sel.index else f'rank {i}; Tier {int(elig.loc[t, "tier"])}; distance above top 10 cut-off'))
for _, r in rej.iterrows():
    pool_rows.append(dict(ticker=r['ticker'], name=r['name'], source='cache candidate_raw (rejected)', distance=None,
                          status='rejected', reason=r['reason']))
pool = pd.DataFrame(pool_rows).drop_duplicates('ticker')
# fixed 20-30 pool: all 10 selected, next eligible up to 30 total, then rejected rows to fill to 25 min
keep = pool[pool.status == 'selected']
extra_elig = pool[pool.status.str.startswith('eligible')].head(12)
rejected_rows = pool[pool.status == 'rejected'].head(8)
pool_final = pd.concat([keep, extra_elig, rejected_rows])
pool_final.to_csv(P / 'candidate_pool_20_30.csv', index=False)
n_pool = len(pool_final)

# ---------------------------------------------------------------- (2) market cap reconciliation (internal; annual report not fetched)
mcap_calc = s3.PRICE * s3.SHARES
mcap_recon = dict(price=s3.PRICE, shares_m=s3.SHARES, mcap_price_x_shares=mcap_calc, mcap_stockanalysis=s3.MCAP,
                  diff_pct=(mcap_calc / s3.MCAP - 1) * 100)

# ---------------------------------------------------------------- (3) ISIN format (ISO 6166 check digit) for the ten peers
def isin_ok(s):
    if not isinstance(s, str) or len(s) != 12 or not s[:2].isalpha():
        return False
    digits = ''.join(str(int(c, 36)) for c in s)
    tot = 0
    for i, ch in enumerate(reversed(digits[:-1])):
        n = int(ch)
        if i % 2 == 0:
            n *= 2
            n = n - 9 if n > 9 else n
        tot += n
    return (10 - tot % 10) % 10 == int(s[-1])

ISIN = {'NEX': 'FR0000044448', 'NKT': 'DK0010287663', 'ABBN': 'CH0012221716', 'VWS': 'DK0061539921',
        'IMI': 'GB00BGLP8L22', 'ALFA': 'SE0000695876', 'NDX1': 'DE000A0D6554', 'HLMA': 'GB0004052071',
        'G1A': 'DE0006602006', 'WRT1V': 'FI0009003727'}
ALT_VWS = 'DK0010268606'
isin_rows = [dict(ticker=t, isin=ISIN[t], format_check_digit_ok=isin_ok(ISIN[t]),
                  source='other runs comparables.csv (cache)', exchange_register_check='not performed (no web access in this step)',
                  note=('second ISIN also found in cache: %s (checksum ok); ambiguous, needs register check' % ALT_VWS) if t == 'VWS' else '')
             for t in ISIN]
pd.DataFrame(isin_rows).to_csv(P / 'isin_check.csv', index=False)

# ---------------------------------------------------------------- (4) three reproducible random EV checks
raw = load()
rng = random.Random(20261030)
pick = rng.sample(list(sel.index), 3)
ev_rows = []
for t in pick:
    r = sel.loc[t]
    e = raw[t]
    mc, d_, n_, c_, ev_s = f(e['market_cap_eur_m']), f(e['debt']), f(e['NCI']), f(e['cash']), f(e['EV_before_associates'])
    ev_calc = mc + d_ + n_ - c_
    ev_rows.append(dict(ticker=t, mcap_eur_m=mc, debt=d_, nci=n_, cash=c_,
                        ev_recomputed=ev_calc, ev_stored=ev_s, diff_pct=(ev_calc / ev_s - 1) * 100))
pd.DataFrame(ev_rows).to_csv(P / 'ev_random_checks.csv', index=False)

# ---------------------------------------------------------------- (5) peer-set and quartile sensitivities
def values(peers, metric, driver=None):
    st = comp.multiple_stats(peers[metric].to_numpy(), min_valid=6)
    return st

base_pe_adj = comp.scaled_multiple(sel['pe'], sel['growth'], s3.G_FUND, driver_scale=100, min_valid=6)
base_pe = base_pe_adj['median'] * s3.EPS
sens = []
for t in sel.index:
    sub = sel.drop(t)
    adj = comp.scaled_multiple(sub['pe'], sub['growth'], s3.G_FUND, driver_scale=100, min_valid=6)
    sens.append(dict(scenario=f'drop {t}', pe_adj_median=adj['median'], value_eur=adj['median'] * s3.EPS,
                     change_vs_base_pct=(adj['median'] / base_pe_adj['median'] - 1) * 100))
raw = comp.multiple_stats(sel['pe'].to_numpy(), min_valid=6)
q = [dict(scenario='quartile p25 (adjusted PE)', value_eur=base_pe_adj['p25'] * s3.EPS, change_vs_base_pct=(base_pe_adj['p25'] / base_pe_adj['median'] - 1) * 100),
     dict(scenario='quartile p75 (adjusted PE)', value_eur=base_pe_adj['p75'] * s3.EPS, change_vs_base_pct=(base_pe_adj['p75'] / base_pe_adj['median'] - 1) * 100),
     dict(scenario='raw PE median (no growth scaling)', value_eur=raw['median'] * s3.EPS, change_vs_base_pct=(raw['median'] / base_pe_adj['median'] - 1) * 100)]
# EUROPE regression unit sensitivity for EV/EBITDA (only equation using DFR and tax)
eq, res, *_ = datasets.equation_for('Italy', 'EV/EBITDA', s3.DATE)
inp = dict(beta=s3.BETA, g_eps=s3.G_FUND, g_rev=s3.G_FUND, payout=s3.PAYOUT, roe=s3.ROE, roic=s3.ROIC, dfr=s3.DFR,
           tax_rate=s3.TAX, oper_margin=s3.EBIT / s3.SALES)
p_dec = pr.predict(eq, inp, 'as_published_note')
p_pct = pr.predict(eq, inp, 'dfr_tax_percent_points')
ev_val = lambda m: comp.implied_equity_from_ev(m, s3.EBITDA, s3.DEBT, s3.NCI, s3.CASH) / s3.SHARES
unit_sens = dict(decimal_multiple=p_dec, pct_points_multiple=p_pct, decimal_value=ev_val(p_dec), pct_value=ev_val(p_pct),
                 change_pct=(ev_val(p_pct) / ev_val(p_dec) - 1) * 100)
sens_df = pd.DataFrame(sens + q + [dict(scenario='EV/EBITDA regression units (pct-points vs decimal)', value_eur=unit_sens['pct_value'],
                                        change_vs_base_pct=unit_sens['change_pct'])])
sens_df.to_csv(P / 'sensitivities.csv', index=False)

# ---------------------------------------------------------------- (6) dataset integrity + sha256 into source_log
reg = [r for r in datasets.registry() if r.family == 'regressions'][0]
path = reg.abspath(datasets.DATA_DIR)
sha = hashlib.sha256(path.read_bytes()).hexdigest()
findings = datasets.check_dataset(reg, datasets.DATA_DIR)
integrity = dict(dataset_id=reg.dataset_id, file=str(path.relative_to(ROOT)), sha256=sha, registry_sha256=reg.sha256,
                 sha_matches_registry=(sha == reg.sha256), errors=[f.message for f in findings if f.severity == 'error'],
                 warnings=[f.code + ': ' + f.message for f in findings if f.severity == 'warn'],
                 infos=[f.code for f in findings if f.severity == 'info'])
json.dump(dict(integrity=integrity, mcap=mcap_recon, pool_count=n_pool, sensitivity_unit=unit_sens), open(P / 'remediation_results.json', 'w'), indent=2, default=float)
print(json.dumps(dict(pool=n_pool, mcap=mcap_recon, integrity=integrity['sha_matches_registry'], errs=len(integrity['errors']),
                      warns=len(integrity['warnings']), isin=[(r['ticker'], r['format_check_digit_ok']) for r in isin_rows],
                      ev=ev_rows, unit=unit_sens), indent=1, default=float))
print(sens_df.to_string())
