"""Only add missing United Kingdom and GBP macro coverage."""
import csv
import io
import json
from datetime import datetime
from pathlib import Path
from valuation_agent import datasets
from valuation_agent.cachefetch import CachedFetcher

ROOT = Path(__file__).resolve().parents[3]
DATE = '2026-10-30'
p = ROOT / 'cache/macro' / f'{DATE}.json'
before = json.loads(p.read_text())
macro = json.loads(p.read_text())
r = datasets.resolve('ctryprem', country='United Kingdom', valuation_date=DATE)
assert r.found
macro['sovereign_default_spreads'].setdefault('United Kingdom', datasets.country_risk(datasets.load_risk_premiums(r.dataset), 'United Kingdom'))
if 'GBP' not in macro['risk_free']:
    url = 'https://www.bankofengland.co.uk/boeapps/database/_iadb-fromshowcolumns.asp?csv.x=yes&Datefrom=26/Oct/2026&Dateto=30/Oct/2026&SeriesCodes=IUDMNPY&CSVF=TN&UsingCodes=Y&VPD=Y&VFD=N'
    response = CachedFetcher(ROOT / 'cache/web' / DATE).get(url)
    assert response.ok
    rows = [x for x in csv.DictReader(io.StringIO(response.text())) if x.get('IUDMNPY')]
    rows = [x for x in rows if datetime.strptime(x['DATE'], '%d %b %Y').strftime('%Y-%m-%d') <= DATE]
    row = max(rows, key=lambda x: datetime.strptime(x['DATE'], '%d %b %Y'))
    spread = macro['sovereign_default_spreads']['United Kingdom']['default_spread']
    macro['risk_free']['GBP'] = dict(yield_value=float(row['IUDMNPY']) / 100, instrument='UK government securities 10-year nominal par yield, BoE IUDMNPY', sovereign_default_spread=spread, default_free_rate=float(row['IUDMNPY']) / 100-spread, source=url, obs_date=datetime.strptime(row['DATE'], '%d %b %Y').strftime('%Y-%m-%d'), access_date='2026-11-01', note='Latest observation returned by official endpoint through valuation date; Oct 29/30 unavailable. Not represented as a same-day quote.')
for k, v in before.items():
    if k in ('risk_free', 'sovereign_default_spreads'):
        assert all(macro[k][kk] == vv for kk, vv in v.items())
    else:
        assert macro[k] == v
p.write_text(json.dumps(macro, indent=2)+'\n')
equations = {}
for dep in ('PE', 'PBV', 'EV/EBITDA'):
    eq, res, meta = datasets.equation_for('United Kingdom', dep, DATE)
    assert eq is not None
    equations[dep] = dict(equation=eq.raw, r2=eq.r2, **meta)
Path(__file__).with_name('topup_BP.L.json').write_text(json.dumps(dict(country='United Kingdom', country_risk=macro['sovereign_default_spreads']['United Kingdom'], risk_free=macro['risk_free']['GBP'], resolution=r.summary(), equations=equations, existing_assets_preserved=True, candidate_data_collected=False), indent=2)+'\n')
print(json.dumps(macro['risk_free']['GBP'], indent=2))
