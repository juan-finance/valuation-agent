"""Add missing PRY.MI country asset (Italy) without rebuilding existing assets."""
import json
from pathlib import Path

from valuation_agent import datasets

DATE = '2026-10-30'
ROOT = Path(__file__).resolve().parents[3]
macro_path = ROOT / 'cache/macro' / f'{DATE}.json'
macro = json.loads(macro_path.read_text())
before = json.loads(macro_path.read_text())
resolution = datasets.resolve('ctryprem', country='Italy', valuation_date=DATE)
assert resolution.found, resolution.message
rp = datasets.load_risk_premiums(resolution.dataset)
if 'Italy' not in macro['sovereign_default_spreads']:
    macro['sovereign_default_spreads']['Italy'] = datasets.country_risk(rp, 'Italy')
# PRY.MI reports and trades in EUR: ECB FX already in the snapshot; stage 3 relative does not discount.
for key in before:
    if key not in ('sovereign_default_spreads',):
        assert before[key] == macro[key], key
for country, val in before['sovereign_default_spreads'].items():
    assert macro['sovereign_default_spreads'][country] == val, country
macro_path.write_text(json.dumps(macro, indent=2) + '\n')
print(json.dumps(macro['sovereign_default_spreads']['Italy'], indent=2))
