"""Validate recalculated numerical artifacts and checkpoint provisional evidence gates."""
from pathlib import Path
import json,shutil
import pandas as pd
from openpyxl import load_workbook
from valuation_agent.runstate import RunState
from valuation_agent import sourcelog
P=Path(__file__).resolve().parent;ROOT=P.parents[2]
r=json.loads((P/'regression_results.json').read_text());s=pd.read_csv(P/'comparables.csv');m=pd.read_csv(P/'multiples_summary.csv')
checks=[]
for name in ['regression_valuation.xlsx','comparables_audit.xlsx']:
 f=P/'recalculated'/name;wf=load_workbook(f,data_only=False);wc=load_workbook(f,data_only=True)
 errors=[f'{ws.title}!{cell.coordinate}:{cell.value}' for ws in wc for row in ws for cell in row if cell.data_type=='e']
 assert not errors,errors
 if name=='regression_valuation.xlsx':
  for i,p in enumerate(r['predictions'],2):
   delta=abs(wc['Equations'].cell(i,4).value-p['predicted']);price_delta=abs(wc['Equations'].cell(i,6).value-p['value_per_share']);assert delta<1e-9 and price_delta<1e-9
   checks.append(dict(check=p['model'],prediction_delta=delta,share_value_delta=price_delta,formula=wf['Equations'].cell(i,4).value,status='PASS'))
 else:
  scores={row[0]:row[-1] for row in list(wc['Score_Live'].values)[1:]}
  for _,row in s.iterrows():
   delta=abs(scores[row.ticker]-row.distance);assert delta<1e-9;checks.append(dict(check='score '+row.ticker,delta=delta,status='PASS'))
 shutil.copyfile(f,P/name)
(P/'formula_checks.json').write_text(json.dumps(checks,indent=2)+'\n')
assert not sourcelog.validate(P/'source_log.csv')
# Preserve the required fixed master prefix without opening the forbidden own-estimation procedure.
v=pd.read_csv(P/'valuation_multiples.csv',keep_default_na=False);prefix=list(pd.read_csv(ROOT/'outputs/ALFA.ST_2026-10-30/relative/valuation_multiples.csv',nrows=0).columns[:18])
for k in prefix:
 if k not in v:v[k]='n/a_published_route'
v['equation_dataset_id']=r['predictions'][0]['dataset'];v['damodaran_global']='not used until verified: GLOBAL PBV beta sign anomaly';v['damodaran_western_europe_uk']=r['predictions'][1]['predicted']
v['validation_status']='provisional; human review and peer-source gates unresolved'
v=v[prefix+[k for k in v if k not in prefix]];v.to_csv(P/'valuation_multiples.csv',index=False)
vr=P/'valuation_summary.md';vr.write_text(vr.read_text().replace('## Data','## Scope\nVWS.CO only; no market sample/own estimation/DATA_BASE_MSCI under published route. Other candidates are not additional valuation targets.\n\n## Data',1)+'\n## Exact equations and t-statistics\nSee Coefficients_PE/PBV/EV_EBITDA workbook sheets for each coefficient/t statistic and dataset SHA.\n'+ '\n'.join(p['equation'] for p in r['predictions'])+'\n')
for f in (P/'recalculated').glob('*.xlsx'):f.unlink()
(P/'recalculated').rmdir()
state=RunState(P.parent/'run_state.json');state.checkpoint('stage3_relative',next_step='QA block C once, then required PDF/plaintext; evidence gates and human review remain unresolved',note='10 numerical peers on first Europe step (9 Tier1/2, 1 Tier3, all Europe-listed); no relaxation. EV/EBIT qualified primary; regression PBV. Not an unqualified final valuation.',outputs=[str(f.relative_to(ROOT)) for f in P.iterdir() if f.is_file()]);state.finish('stage3_relative',status='provisional',note='Numerical deliverables complete/recalculated; candidate-source qualification and human Spot_check not complete.');state.append_run_log(ROOT/'memory/run_log.csv')
print('stage3 checkpoint',state.d['stages']['stage3_relative'])
