"""Finalize changed artifacts and module-rendered BP report; no full QA execution."""
import hashlib
import json
import math
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd
from openpyxl import load_workbook
from pypdf import PdfReader
from valuation_agent import comparables as c
from valuation_agent.runstate import RunState

P = Path(__file__).resolve().parent
O = P.parent
ROOT = P.parents[2]
STATUS = 'provisional - limitations disclosed'
state = RunState(O / 'run_state.json')
assert not state.d['approved_remediation'].get('finished'), 'Finalization already complete'
state.d['approved_remediation']['started'] = '2026-11-02T12:54:13+00:00'
raw = pd.read_csv(P / 'candidate_raw.csv').set_index('ticker')
for file in ['comparables.csv', 'remediated_vendor_inputs.csv']:
    frame = pd.read_csv(P / file)
    for column in ['tier', 'hypothesis', 'europe', 'country', 'name']:
        frame[column] = frame.ticker.map(raw[column])
    frame.to_csv(P / file, index=False)
peers = pd.read_csv(P / 'comparables.csv')
assert peers.tier.between(1, 2).all() and peers.europe.sum() == 6
B = pd.read_csv(P / 'ev_bridge.csv').set_index('ticker')
M = pd.read_csv(P / 'multiples_summary.csv').set_index('multiple')
T = raw.loc['BP']
fx = json.loads((ROOT / 'cache/macro/2026-10-30.json').read_text())['fx_ecb_reference']['rates']
conversion = fx['GBP'] / fx['USD']
rr = json.loads((P / 'regression_results.json').read_text())
reg = next(r for r in rr['predictions'] if r['model'].startswith('EV/EBITDA'))
reg['actual'] = B.loc['BP', 'EV_pre_associate'] / T.EBITDA
reg['deviation'] = reg['actual'] / reg['predicted'] - 1
reg['value_per_share_gbp'] = reg['value_per_share']
(P / 'regression_results.json').write_text(json.dumps(rr, indent=2) + '\n')
wb = load_workbook(P / 'regression_valuation.xlsx')
wb['Inputs']['B9'] = 0
wb['Inputs']['C9'] = 'Approved uniform bridge: no extra preference proxy; historical carrying amount21 retained in issuer_crosschecks.json'
wb['Predictions']['C4'] = 'DIAGNOSTIC ONLY: low sector plausibility; not headline or price target'
wb['Predictions']['H4'] = reg['actual']
wb.save(P / 'regression_valuation.xlsx')
recalc = Path('/home/ubuntu/Documents/bp-peer-repair/approved-recalc')
recalc.mkdir(exist_ok=True)
subprocess.run(['libreoffice', '-env:UserInstallation=file:///home/ubuntu/Documents/bp-peer-repair/lo-profile', '--headless', '--convert-to', 'xlsx', '--outdir', str(recalc), str(P / 'regression_valuation.xlsx')], check=True)
(P / 'regression_valuation.xlsx').write_bytes((recalc / 'regression_valuation.xlsx').read_bytes())
cached = load_workbook(P / 'regression_valuation.xlsx', data_only=True)
assert math.isclose(cached['Predictions']['G4'].value, reg['value_per_share'], abs_tol=1e-9)
sens = pd.read_csv(P / 'sensitivities.csv')
base = M.loc['ev_ebitda', 'value_per_share_mid']
extra = []
for ticker, difference in [('SHEL', -45), ('TTE', -388)]:
    multiples = peers.set_index('ticker').ev_ebitda.copy()
    multiples.loc[ticker] += difference / B.loc[ticker, 'EBITDA']
    median = c.multiple_stats(multiples, min_valid=6)['median']
    value = c.implied_equity_from_ev(median, T.EBITDA, T.debt, T.NCI, T.cash, 0) / T.current_shares_m * conversion
    extra.append(dict(sensitivity=ticker + ' issuer-vendor debt difference only', multiple='ev_ebitda', value_per_share=value, base_value_per_share=base, change_fraction=value / base - 1, issuer_minus_vendor_debt=difference))
sens = pd.concat([sens, pd.DataFrame(extra)], ignore_index=True)
sens.to_csv(P / 'sensitivities.csv', index=False)
fig = json.loads((P / 'report_figures.json').read_text())
fig.update(tier12=10, tier3=0, peer_classification='Existing BP tiers and countries retained; reused cleaned target tier0 must not propagate to SHEL peer',
           issuer_vendor_debt_sensitivities=extra, source_files=['candidate_raw.csv', 'remediated_vendor_inputs.csv', 'ev_bridge.csv', 'peer_qualification.csv'],
           source_period_note='FY2025; vendor period-end labels incomplete; cached extracts confirm December annual basis; no dates invented')
def clean_json(obj):
    if isinstance(obj, dict):
        return {k: clean_json(v) for k, v in obj.items()}
    if isinstance(obj, list):
        return [clean_json(v) for v in obj]
    return None if isinstance(obj, float) and not math.isfinite(obj) else obj
(P / 'report_figures.json').write_text(json.dumps(clean_json(fig), indent=2, allow_nan=False) + '\n')
notes = (O / 'report_notes.md').read_text()
assert len(notes.splitlines()) == 6
audit = load_workbook(P / 'comparables_audit.xlsx')
for name, frame in [('Approved_Peers', peers), ('Approved_Sensitivity', sens)]:
    del audit[name]
    sheet = audit.create_sheet(name)
    sheet.append(list(frame.columns))
    for row in frame.itertuples(index=False, name=None):
        sheet.append([None if pd.isna(v) else v for v in row])
audit.save(P / 'comparables_audit.xlsx')
# The shared renderer appends the status qualifier; its base alias avoids duplication.
state.d['stages']['stage3_relative']['status'] = 'provisional'
state.save()
try:
    build = subprocess.run([sys.executable, '-m', 'valuation_agent.relative_report', str(O)], capture_output=True, text=True, check=True)
finally:
    state.d['stages']['stage3_relative']['status'] = STATUS
    state.save()
(P / 'report_build_log.txt').write_text(build.stdout + build.stderr)
assert 'WARNING' not in build.stdout + build.stderr
pdf = O / 'relative_report_BP.L.pdf'
pages = len(PdfReader(pdf).pages)
assert 2 <= pages <= 3
subprocess.run(['pdftotext', '-layout', str(pdf), str(P / 'pdf_text_validation.txt')], check=True)
summary = (O / 'relative_summary.md').read_text()
text = (P / 'pdf_text_validation.txt').read_text()
assert 'NO USABLE VALUATION RELEASED' not in text + summary
assert 'diagnostic only' in summary and STATUS in summary
for m in ['ev_ebitda', 'pe', 'pbv']:
    for key in ['value_per_share_low', 'value_per_share_mid', 'value_per_share_high']:
        assert f'{M.loc[m, key]:.2f}' in text and f'{M.loc[m, key]:.2f}' in summary
(P / 'valuation_summary.md').write_text(summary)
validation = dict(status='PASS', scope='Artifact checks only; no repeat of block C or unchanged passing items', pages=pages,
                  report_generator='valuation_agent.relative_report', warning_lines=0, notes_count=6,
                  headline='peer EV/EBITDA', regression='labelled diagnostic only', workbook_diagnostic_cached_value=cached['Predictions']['G4'].value,
                  pdf_sha256=hashlib.sha256(pdf.read_bytes()).hexdigest(), summary_sha256=hashlib.sha256((O / 'relative_summary.md').read_bytes()).hexdigest(),
                  checks=['all three requested ranges match rounded CSV figures in both outputs', 'six notes and large sensitivities present', 'correct peer tier/country metadata', 'regression uniform bridge cached value matches library to1e-9'],
                  renderer_status_alias='provisional passed to module which appends limitations disclosed; persisted status restored in finally')
(P / 'report_validation.json').write_text(json.dumps(validation, indent=2) + '\n')
finish = datetime.now(timezone.utc)
rem = state.d['approved_remediation']
rem.update(finished=finish.isoformat(timespec='seconds'), elapsed_min=round((finish - datetime.fromisoformat(rem['started'])).total_seconds() / 60, 1), report_warning_lines=0)
state.d['stages']['stage3_relative'].update(status=STATUS, finished=rem['finished'], elapsed_min=rem['elapsed_min'])
state.d['report'].update(status=STATUS, generator='valuation_agent.relative_report', pages=pages)
state.save()
state.append_run_log(ROOT / 'memory/run_log.csv')
print(build.stdout, 'Elapsed minutes:', rem['elapsed_min'])
