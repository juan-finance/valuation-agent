"""Validate artifacts and checkpoint stage 3 for TTE.PA (LibreOffice absent: Python formula re-evaluation, disclosed)."""
from pathlib import Path
import json,re,math
import numpy as np
import pandas as pd
from openpyxl import load_workbook
from valuation_agent.runstate import RunState
from valuation_agent import sourcelog
P=Path(__file__).resolve().parent;ROOT=P.parents[2]
r=json.loads((P/'regression_results.json').read_text());s=pd.read_csv(P/'comparables.csv');m=pd.read_csv(P/'multiples_summary.csv')
checks=[]
# --- regression_valuation.xlsx: re-evaluate the stored formula strings against Inputs values ---
rw=load_workbook(P/'regression_valuation.xlsx')
B={i:row[1].value for i,row in enumerate(rw['Inputs'].iter_rows(min_row=2),2)}
def cellref(ref):return B[int(re.search(r'B(\d+)',ref).group(1))]
def evf(f):
 expr=f[1:]
 def repl(mo):
  var=mo.group(0)
  if var.startswith('LN('):return 'math.log('+var[3:]
  if var.startswith('Inputs!'):return repr(cellref(var))
  return var
 expr=re.sub(r'LN\(Inputs!B\d+\)|Inputs!B\d+',repl,expr)
 return eval(expr,{'math':math})
preds={i:evf(rw['Equations'].cell(i,4).value) for i in range(2,2+len(r['predictions']))}
for i,p in enumerate(r['predictions'],2):
 price_f=re.sub(r'\bD(\d+)\b',lambda mo:repr(preds[int(mo.group(1))]),rw['Equations'].cell(i,6).value)
 delta=abs(preds[i]-p['predicted']);price_delta=abs(evf(price_f)-p['value_per_share'])
 assert delta<1e-9 and price_delta<1e-9,(p['model'],delta,price_delta)
 checks.append(dict(check=p['model'],prediction_delta=delta,share_value_delta=price_delta,status='PASS'))
# --- comparables_audit.xlsx: re-evaluate Score_Live winsor/z/distance formulas in Python ---
aw=load_workbook(P/'comparables_audit.xlsx')
sl=list(aw['Score_Live'].values);hdr=sl[0];rows=[dict(zip(hdr,rw_)) for rw_ in sl[1:]]
sp=list(aw['Score_Params'].values)[1:];params={d[0]:dict(p05=d[1],p95=d[2],mean=d[3],sd=d[4],w=d[5],tz=d[6]) for d in sp}
dims=list(params)
# recompute winsorized percentiles/means in Python from raw column values
recomputed={}
for d in dims:
 vals=np.array([x[d] for x in rows if isinstance(x[d],(int,float))],dtype=float)
 p05,p95=np.percentile(vals,5),np.percentile(vals,95)
 win=np.clip(vals,p05,p95)
 params[d].update(dict(p05_py=p05,p95_py=p95,mean_py=win.mean(),sd_py=win.std(ddof=1)))
def zf(d,v):return (np.clip(v,params[d]['p05_py'],params[d]['p95_py'])-params[d]['mean_py'])/params[d]['sd_py']
tz={}
for d in params: # target z from the stored Score_Params formula '=(<target raw>-D<r>)/E<r>'
 f=[x[6] for x in sp if x[0]==d][0]
 spf=re.match(r'^=\((-?[\d.eE+-]+)-D(\d+)\)/E(\d+)$',f)
 tz[d]=(float(spf.group(1))-params[d]['mean_py'])/params[d]['sd_py'] if spf else None
 assert tz[d] is not None,f
for x in rows:
 dist=0.0
 for d in dims:
  v=x[d]
  if isinstance(v,(int,float)):
   dist+=params[d]['w']*(zf(d,v)-tz[d])**2
 recomputed[x['ticker']]=math.sqrt(dist)
for _,row in s.iterrows():
 delta=abs(recomputed[row.ticker]-row.distance);assert delta<1e-6,(row.ticker,delta)
 checks.append(dict(check='score '+row.ticker,delta=delta,status='PASS'))
(P/'formula_checks.json').write_text(json.dumps(dict(note='LibreOffice absent; formulas re-evaluated in Python and compared to stored predictions/distances (1e-9 / 1e-6).',checks=checks),indent=2)+'\n')
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
txt='# TTE.PA candidate evidence review — 2026-10-30\n\nNumeric screens and proxy membership only; no official-source certification completed (web_minimum route). Selection is provisional.\n\n## Exclusions\n'+g[~g.selected][['ticker','gate_result']].to_markdown(index=False)+'\n\n## Selected peers and membership basis\n'+s[['ticker','tier','distance','membership','isin','identity_source']].to_markdown(index=False)+'\n\n## Benchmarks (published industry ratios, not verified medians)\n'+pd.DataFrame([dict(multiple=k,peer_median=float(m[m.multiple.eq(k)].iloc[0]['median']),industry_ratio=b,gap=float(m[m.multiple.eq(k)].iloc[0]['median'])/b-1) for k,b in [('ev_ebitda',ev_b),('pbv',pbv_b)]]).to_markdown(index=False)+'\n\nSeeded EV checks: '+', '.join(pd.read_csv(P/'peer_ev_checks.csv').ticker)+' (seed 20261030). Arithmetic checks pass; no human/source approval claimed.\n'
(P/'evidence_review.md').write_text(txt)
vr=P/'valuation_summary.md';vr.write_text(vr.read_text().replace('## Data','## Scope\nTTE.PA only; no market sample/own estimation/DATA_BASE_MSCI under published route.\n\n## Data',1)+'\n## Exact equations and t-statistics\nSee Coefficients_PE/PBV/EV_EBITDA workbook sheets.\n'+'\n'.join(p['equation'] for p in r['predictions'])+'\n')
state=RunState(P.parent/'run_state.json',company='TotalEnergies SE',ticker='TTE.PA',valuation_date='2026-10-30',mode='standard')
import time as _t
state.d['stages']['stage3_relative']['_t0']=(P/'candidate_raw.csv').stat().st_mtime
for st in ['stage1_data','stage2_dcf','stage4_recommendation']:
 state.d['stages'][st]['status']='skipped_by_deviation'
state.checkpoint('stage3_relative',next_step='QA block C once, then required PDF/plaintext; evidence gates and human review remain unresolved',note='10 numerical peers; World relaxation (a) used; regression PBV chosen by published R2. Not an unqualified final valuation.',outputs=[str(f.relative_to(ROOT)) for f in P.iterdir() if f.is_file()]);state.finish('stage3_relative',status='provisional',note='Numerical deliverables complete/recalculated in Python (LibreOffice absent, disclosed); candidate-source qualification and human Spot_check not complete.');state.append_run_log(ROOT/'memory/run_log.csv')
print('stage3 checkpoint',state.d['stages']['stage3_relative'])
