"""SU.PA comparable pool: European candidates from cached stockanalysis extracts (all prior runs), deduplicated by ticker."""
import csv, glob, math
from pathlib import Path
P = Path(__file__).resolve().parent
ROOT = P.parents[2]
NUM = ['price','current_shares_m','market_cap_eur_m','ni','sales','EBIT','DA','EBITDA','equity','equity_prior','assets','debt','cash','NCI',
       'EV_before_associates','roe','payout','growth','beta','net_debt_ebitda','ebitda_margin','capex','capex_sales','cfo','net_margin','tax_rate',
       'pe','pbv','ps','ev_ebit','ev_ebitda','ev_cf','ev_assets','ev_sales','peg','ln_mcap']
def f(x):
    try: return float(x)
    except (TypeError, ValueError): return float('nan')
def load():
    rows = {}
    for path in sorted(glob.glob(str(ROOT / 'outputs/*/relative/candidate_raw.csv'))):
        if "SU.PA" in path.split('/')[-3]: continue
        for r in csv.DictReader(open(path)):
            t = r['ticker']
            if r.get('europe') != 'True' or t in rows and f(rows[t]['market_cap_eur_m']) > 0: continue
            rows[t] = r
    return rows
if __name__ == '__main__':
    rows = load()
    for t, r in sorted(rows.items(), key=lambda kv: -f(kv[1]['market_cap_eur_m']) if f(kv[1]['market_cap_eur_m']) == f(kv[1]['market_cap_eur_m']) else 0):
        ok = all(f(r[c]) == f(r[c]) for c in ['ni','sales','EBITDA','equity','debt','cash','market_cap_eur_m','beta'])
        print(f"{t:8s} {r['name'][:28]:28s} {r['country'][:12]:12s} mcap={f(r['market_cap_eur_m']):>10.0f} ni={f(r['ni']):>9.1f} complete={ok}")
