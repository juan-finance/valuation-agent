"""Add missing VER.VI country asset (Austria) without rebuilding existing assets."""
import json
from pathlib import Path

from valuation_agent import datasets

DATE = '2026-10-30'
ROOT = Path(__file__).resolve().parents[3]
macro_path = ROOT / 'cache/macro' / f'{DATE}.json'
macro = json.loads(macro_path.read_text())
before = json.loads(macro_path.read_text())
resolution = datasets.resolve('ctryprem', country='Austria', valuation_date=DATE)
assert resolution.found, resolution.message
rp = datasets.load_risk_premiums(resolution.dataset)
if 'Austria' not in macro['sovereign_default_spreads']:
    macro['sovereign_default_spreads']['Austria'] = datasets.country_risk(rp, 'Austria')
# VER.VI reports and trades in EUR: ECB FX and the EUR Bund yield are already in the snapshot;
# stage 3 relative does not discount.
for key in before:
    if key not in ('sovereign_default_spreads',):
        assert before[key] == macro[key], key
for country, val in before['sovereign_default_spreads'].items():
    assert macro['sovereign_default_spreads'][country] == val, country
macro_path.write_text(json.dumps(macro, indent=2) + '\n')
resolved = {}
for family in ('beta', 'capex', 'ctryprem', 'dbtfund', 'wcdata', 'regressions', 'ratings'):
    r = datasets.resolve(family, country='Austria', valuation_date=DATE)
    assert r.found, r.summary()
    resolved[family] = r.summary()
equations = {}
for dep in ('PE', 'PBV', 'EV/EBITDA'):
    eq, r, meta = datasets.equation_for('Austria', dep, DATE)
    assert eq is not None
    equations[dep] = {'equation': eq.raw, 'r2': eq.r2, **meta}
out = {'ticker': 'VER.VI', 'valuation_date': DATE, 'country': 'Austria',
       'currency': 'EUR', 'resolutions': resolved, 'equations': equations,
       'ratings_fallback_reason': 'Global corporate coverage-to-spread schedule; used as a common synthetic-rating cross-check, not a regional industry debt estimate.',
       'existing_assets_preserved': True, 'candidate_data_collected': False}
Path(__file__).with_name('topup_VER.VI.json').write_text(json.dumps(out, indent=2) + '\n')
print(json.dumps(macro['sovereign_default_spreads']['Austria'], indent=2))
