"""Finalize VER.VI stage 3: formula checks, evidence review, summary/report files, run_state + run_log."""
import json, time
from pathlib import Path
import numpy as np
import pandas as pd
from openpyxl import load_workbook
from valuation_agent import comparables as c, datasets, published_regressions as pr
from valuation_agent.runstate import RunState

P=Path(__file__).resolve().parent; O=P.parent; ROOT=P.parents[2]
r=json.loads((P/'regression_results.json').read_text())
s=pd.read_csv(P/'comparables.csv'); m=pd.read_csv(P/'multiples_summary.csv')
checks=[]
# Recompute published predictions in Python (LibreOffice absent; disclosed).
inputs=r['inputs']
for p_ in r['predictions']:
 eq,res,region=datasets.equation_for('Austria',p_['model'],'2026-10-30')
 v=pr.predict(eq,{k:float(x) for k,x in inputs.items()},unit_policy='as_published_note')
 checks.append(dict(check=p_['model'],workbook=p_['predicted'],recomputed=float(v),delta=abs(v-p_['predicted']),status='PASS' if abs(v-p_['predicted'])<1e-9 else 'FAIL'))
# Peer EV recompute evidence (seeded sample of 3).
import random
for t in sorted(random.Random(20261030).sample(list(s.ticker),3)):
 row=s[s.ticker.eq(t)].iloc[0];me=row.pe*row.ni if np.isfinite(row.ni) and row.ni>0 else row.market_cap_eur_m
 ev=c.comparable_ev(me,row.debt,row.NCI,row.cash,0)
 checks.append(dict(check='EV_recompute '+t,recorded=row.EV_before_associates,recomputed=float(ev),delta=ev-row.EV_before_associates,status='PASS' if np.isfinite(ev) and abs(ev-row.EV_before_associates)<1e-6*max(1,abs(row.EV_before_associates)) else 'FAIL'))
(P/'formula_checks.json').write_text(json.dumps(checks,indent=2,default=str)+'\n')
assert all(x['status']=='PASS' for x in checks)

g=pd.read_csv(P/'candidate_gates.csv');g['selected']=g.ticker.isin(s.ticker)
ev_b=json.loads((P/'industry_benchmarks.json').read_text())
ev_gen=[b for b in ev_b if b['family']=='evebitda_industry' and b['industry']=='Utility (General)'][0]['values']['EV/EBITDA (All firms)']
pbv_gen=[b for b in ev_b if b['family']=='pbv_industry' and b['industry']=='Utility (General)'][0]['values']['PBV']
(P/'evidence_review.md').write_text('# VER.VI candidate evidence review - 2026-10-30\n\nNumeric screens and proxy membership only; no official-source certification completed (web_minimum route). Selection is provisional.\n\n## Exclusions\n'+g[~g.selected][['ticker','gate_result']].to_markdown(index=False)+'\n\n## Selected peers and membership basis\n'+s[['ticker','tier','distance','membership','isin','inclusion_reason']].to_markdown(index=False)+'\n\n## Benchmarks (published industry ratios, not verified medians)\n'+pd.DataFrame([dict(multiple=k,peer_median=float(m[m.multiple.eq(k)].iloc[0]['median']),industry_ratio=b,gap=float(m[m.multiple.eq(k)].iloc[0]['median'])/b-1) for k,b in [('ev_ebitda',ev_gen),('pbv',pbv_gen)]]).to_markdown(index=False)+'\n\nSeeded EV checks embedded in comparables_audit.xlsx EV_check sheet (seed 20261030). Arithmetic checks pass; no human/source approval claimed.\n')

prim=m[m.multiple.eq('ev_ebitda')].iloc[0]
preds={x['model']:x for x in r['predictions']}
(P/'comparables_report.md').write_text(f"""# Verbund comparables - 2026-10-30

DRAFT pending human Spot_check. Primary EV/EBITDA per bucket-A integrated-utilities mapping; ordered cross-checks PE and PBV kept. Peer EV uses vendor debt incl. leases + book NCI - cash; associates proxied by long-term investments - qualified only. Austrian windfall-profit levy (EUR135.9m) inside FY2025 cost base flagged for comparability; issuer-vs-vendor EBITDA/EBIT gaps small (-0.8%/-0.2%), sensitivities shown. No DCF, no recommendation, no synthesis weight, no residual-band classification.

## Selection
Initial pool {len(g)-1} candidates after source-availability and ownership gates (CEZ source-unavailable/EM; ELE and EDPR subsidiary exclusions; EKT/PNE3 size; US/CA names held for World relaxation that was never needed). Ordered expansion log in peer_selection.json; Europe step already feasible (n_pool as recorded). Eight required score weights, pool-only 5/95 winsorization, STDEV.S standardization; missing dimensions renormalized.

{s[['ticker','tier','distance','country','membership','inclusion_reason']].to_markdown(index=False)}

## Primary and raw/scaled values
{m.to_markdown(index=False)}

## Bridge and fiscal bases
FY2025 financials at each fiscal end (all December); quote prices/cap at 2026-10-30; FX ECB same date (GBP 0.8785, DKK 7.4735, NOK 11.49 per ECB snapshot). EV numerator: debt incl. leases + NCI - cash, associates excluded. EV/CF uses reported CFO - financing-classification differences remain. Target: EUR basis throughout; NI 1,489 / parent common equity 10,341 / EBITDA vendor 2,715 (issuer 2,737.5).

## Sensitivities
p25/median/p75 are peer dispersion, not confidence intervals. Leave-one-out and issuer-basis EBIT/EBITDA diagnostics in sensitivities.csv. Vendor betas across the pool are low (uniform source, disclosed); beta dimension kept but distance is driven mainly by size/leverage/margins.

## Benchmarks
Utility (General)/(Water) EUROPE published ratios in industry_benchmarks.json are NOT verified medians; gap checks in evidence_review.md and qa_results.md. Peer EV/EBITDA medians versus closest published industry ratios recorded, not "fixed" to match.

## Sources and audit
Field-level sources in source_log.csv; selection logs and live scores in comparables_audit.xlsx; three seeded EV arithmetic rows in EV_check; human review explicitly pending.
""")

chosen=max(r['predictions'],key=lambda x:x['published_r2'])
(P/'valuation_summary.md').write_text(f"""# Relative valuation by regression - Europe, VER.VI, 2026-10-30

## Scope
VER.VI only; no market sample/own estimation/DATA_BASE_MSCI under the published route.

## Headline
Draft {chosen['model']} selected by highest eligible published R2 ({chosen['published_r2']:.3f}), a weaker heuristic than adjusted-R2/industry fit.

## Data
FY2025 uniform vendor inputs cross-checked with the VERBUND integrated annual report 2025. Austria listing resolves EUROPE exact. Sourced analyst consensus inputs used (g_eps -4.51%, g_rev -0.98%); no substitution needed. Payout 0.466 on FY2025 declared DPS 2.00/EPS 4.29 (cash-paid basis 0.89 flagged - special dividend). ROE on closing parent-common equity 10,341.

## Fitted models
{pd.DataFrame(r['predictions'])[['model','predicted','published_r2','value_per_share','actual','deviation']].to_markdown(index=False)}

## Diagnostics
Integrity findings retained in regression_results.json and dataset_checks.json. GLOBAL PEG/PBV and EM EVEBITDA source anomalies do not affect these EUROPE equations. No n, SEy, adjusted R2, p-values, A/B/C, typicality or D1-D10 available: n/a_published_route. Classification: Not classified (no SEy published).

## Exact equations and t-statistics
See Coefficients_PE/PBV/EV_EBITDA workbook sheets.

## Valuation results (sorted from most undervalued to most overvalued)
{pd.DataFrame(r['predictions']).sort_values('value_per_share',ascending=False)[['model','value_per_share']].to_markdown(index=False)}

## Robustness
All units decimal as approved; predict_both_policies alternatives recorded in regression_results.json. Live predictions and price bridges reference Inputs; recalculation validation in formula_checks.json. Published EV definition undocumented.

## Key warnings
Market-wide, low-R2 equations are not sector fair-value proof. January 2026 vintage ~9 months old at valuation date. Published EV definition undocumented. Beta benchmark/frequency unspecified; vendor beta 0.14 atypically low. Negative consensus growth inputs (g_eps -4.51%, g_rev -0.98%) reflect normalization off the 2022-24 price spike - flagged; PE equation sensitive to sign of g. Austrian windfall levy EUR135.9m in FY2025 costs.

## Limitations
Equation R2 low (PE 0.201/PBV 0.423/EVEBITDA 0.262 published). Analyst-growth definition differs from our fundamental growth; sourced consensus used so no substitution. No residual dispersion or confidence range invented.

## Sources
source_log.csv; registered regressions_multi_2026-01 SHA {r['predictions'][0]['dataset']}; issuer cross-check in relative_inputs.md.
""")
state=RunState(O/'run_state.json')
state.checkpoint('stage3_relative',next_step='QA block C once, then required PDF/plaintext; evidence gates and human review remain unresolved',note='10 numerical peers on first Europe step (no relaxation); default Tier3 cap 2 kept (0 used); regression PBV chosen by published R2. Not an unqualified final valuation.',outputs=[str(f.relative_to(ROOT)) for f in P.iterdir() if f.is_file()])
state.finish('stage3_relative',status='provisional',note='Numerical deliverables complete/recalculated; candidate-source qualification and human Spot_check not complete.')
state.append_run_log(ROOT/'memory/run_log.csv')
print('done')
