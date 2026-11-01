"""Add missing NESTE.HE country asset without rebuilding existing assets."""
import json
from pathlib import Path

from valuation_agent import datasets

DATE = '2026-10-30'
ROOT = Path(__file__).resolve().parents[3]
macro_path = ROOT / 'cache/macro' / f'{DATE}.json'
macro = json.loads(macro_path.read_text())
before = json.loads(macro_path.read_text())
resolution = datasets.resolve('ctryprem', country='Finland', valuation_date=DATE)
assert resolution.found, resolution.message
rp = datasets.load_risk_premiums(resolution.dataset)
if 'Finland' not in macro['sovereign_default_spreads']:
    macro['sovereign_default_spreads']['Finland'] = datasets.country_risk(rp, 'Finland')
# NESTE.HE reports and trades in EUR: Bund 10y risk-free and ECB FX already in the snapshot;
# stage 3 relative does not discount, so no Finland-specific instrument is required.
for key in before:
    if key not in ('risk_free', 'sovereign_default_spreads'):
        assert before[key] == macro[key]
assert before['risk_free'] == macro['risk_free']
macro_path.write_text(json.dumps(macro, indent=2) + '\n')
print(json.dumps(macro['sovereign_default_spreads']['Finland'], indent=2))
