"""Add missing MT.AS country/currency assets without rebuilding existing assets."""
import csv
import io
import json
from pathlib import Path

from valuation_agent import datasets
from valuation_agent.cachefetch import CachedFetcher

DATE = '2026-10-30'
ROOT = Path(__file__).resolve().parents[3]
macro_path = ROOT / 'cache/macro' / f'{DATE}.json'
macro = json.loads(macro_path.read_text())
before = json.loads(macro_path.read_text())
resolution = datasets.resolve('ctryprem', country='Luxembourg', valuation_date=DATE)
rp = datasets.load_risk_premiums(resolution.dataset)
for country in ('Luxembourg', 'United States'):
    if country not in macro['sovereign_default_spreads']:
        macro['sovereign_default_spreads'][country] = datasets.country_risk(rp, country)
if 'USD' not in macro['risk_free']:
    url = ('https://home.treasury.gov/resource-center/data-chart-center/interest-rates/'
           'daily-treasury-rates.csv/2026/all?field_tdr_date_value=2026&type=daily_treasury_yield_curve')
    result = CachedFetcher(ROOT / 'cache/web' / DATE).get(url)
    if not result.ok:
        raise RuntimeError(result.error)
    rows = list(csv.DictReader(io.StringIO(result.text().lstrip('\ufeff'))))
    row = next(row for row in rows if row['Date'] == '10/30/2026')
    yield_value = float(row['10 Yr']) / 100
    spread = macro['sovereign_default_spreads']['United States']['default_spread']
    macro['risk_free']['USD'] = {
        'yield': yield_value, 'instrument': 'US Treasury 10-year par yield',
        'sovereign_default_spread': spread, 'default_free_rate': yield_value - spread,
        'source': url, 'obs_date': DATE, 'access_date': '2026-10-31',
        'note': 'Treasury same-day observation used; FRED latest available was Oct 29 (4.98%).'
    }
for key in before:
    if key not in ('risk_free', 'sovereign_default_spreads'):
        assert before[key] == macro[key]
assert before['risk_free']['EUR'] == macro['risk_free']['EUR']
macro_path.write_text(json.dumps(macro, indent=2) + '\n')
resolved = {}
for family in ('beta', 'capex', 'ctryprem', 'dbtfund', 'wcdata', 'regressions', 'ratings'):
    r = datasets.resolve(family, country='Luxembourg', valuation_date=DATE)
    assert r.found, r.summary()
    resolved[family] = r.summary()
equations = {}
for dep in ('PE', 'PBV', 'EV/EBITDA'):
    eq, r, meta = datasets.equation_for('Luxembourg', dep, DATE)
    assert eq is not None
    equations[dep] = {'equation': eq.raw, 'r2': eq.r2, **meta}
out = {'ticker': 'MT.AS', 'valuation_date': DATE, 'country': 'Luxembourg',
       'currency': 'USD', 'resolutions': resolved, 'equations': equations,
       'ratings_fallback_reason': 'Global corporate coverage-to-spread schedule; used as a common synthetic-rating cross-check, not a regional industry debt estimate.',
       'existing_assets_preserved': True, 'candidate_data_collected': False}
Path(__file__).with_name('topup_MT.AS.json').write_text(json.dumps(out, indent=2) + '\n')
print(json.dumps(macro['risk_free']['USD'], indent=2))
