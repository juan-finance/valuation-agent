"""Validate recalculated artifacts and checkpoint stage 3 for EQNR.OL."""
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
v=pd.read_csv(P/'valuation_multiples.csv',keep_default_na=False);prefix=list(pd.read_csv(ROOT/'outputs/ALFA.ST_2026-10-30/relative/valuation_multiples.csv',nrows=0).columns[:18])
for k in prefix:
 if k not in v:v[k]='n/a_published_route'
v['equation_dataset_id']=r['predictions'][0]['dataset'];v['damodaran_global']='not used until verified: GLOBAL PBV beta sign anomaly';v['damodaran_western_europe_uk']=[p for p in r['predictions'] if p['model']=='PBV'][0]['predicted']
v['validation_status']='provisional; human review and peer-source gates unresolved'
v=v[prefix+[k for k in v if k not in prefix]];v.to_csv(P/'valuation_multiples.csv',index=False)
g=pd.read_csv(P/'candidate_gates.csv')
bench=json.loads((P/'industry_benchmarks.json').read_text())
def benchv(fam,ind,col):return [b['values'].get(col) for b in bench if b['family']==fam and b['industry']==ind][0]
ev_b=benchv('evebitda_industry','Oil/Gas (Integrated)','EV/EBITDA (Pos. EBITDA)');pbv_b=benchv('pbv_industry','Oil/Gas (Integrated)','PBV')
txt='# EQNR.OL candidate evidence review — 2026-10-30\n\nNumeric screens and proxy membership only; no official-source certification completed (web_minimum route). Selection is provisional.\n\n## Exclusions\n'+g[~g.selected][['ticker','gate_result']].to_markdown(index=False)+'\n\n## Selected peers and membership basis\n'+s[['ticker','tier','distance','membership','isin','identity_source']].to_markdown(index=False)+'\n\n## Benchmarks (published industry ratios, not verified medians)\n'+pd.DataFrame([dict(multiple=k,peer_median=float(m[m.multiple.eq(k)].iloc[0]['median']),industry_ratio=b,gap=float(m[m.multiple.eq(k)].iloc[0]['median'])/b-1) for k,b in [('ev_ebitda',ev_b),('pbv',pbv_b)]]).to_markdown(index=False)+'\n\nSeeded EV checks: '+', '.join(pd.read_csv(P/'peer_ev_checks.csv').ticker)+' (seed 20261030). Arithmetic checks pass; no human/source approval claimed.\n'
(P/'evidence_review.md').write_text(txt)
vr=P/'valuation_summary.md';vr.write_text(vr.read_text().replace('## Data','## Scope\nEQNR.OL only; no market sample/own estimation/DATA_BASE_MSCI under published route.\n\n## Data',1)+'\n## Exact equations and t-statistics\nSee Coefficients_PE/PBV/EV_EBITDA workbook sheets.\n'+'\n'.join(p['equation'] for p in r['predictions'])+'\n')
for f in (P/'recalculated').glob('*.xlsx'):f.unlink()
(P/'recalculated').rmdir()
state=RunState(P.parent/'run_state.json');state.checkpoint('stage3_relative',next_step='QA block C once, then required PDF/plaintext; evidence gates and human review remain unresolved',note='10 numerical peers; Tier3 cap 4 relaxation used; regression PBV chosen by published R2. Not an unqualified final valuation.',outputs=[str(f.relative_to(ROOT)) for f in P.iterdir() if f.is_file()]);state.finish('stage3_relative',status='provisional',note='Numerical deliverables complete/recalculated; candidate-source qualification and human Spot_check not complete.');state.append_run_log(ROOT/'memory/run_log.csv')
print('stage3 checkpoint',state.d['stages']['stage3_relative'])
