"""Finalize ORSTED.CO stage 3: formula checks, evidence review, summary/report files, run_state + run_log."""
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
 eq,res,region=datasets.equation_for('Denmark',p_['model'],'2026-10-30')
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
(P/'evidence_review.md').write_text('# ORSTED.CO candidate evidence review - 2026-10-30\n\nNumeric screens and proxy membership only; no official-source certification completed (web_minimum route). Selection is provisional.\n\n## Exclusions\n'+g[~g.selected][['ticker','gate_result']].to_markdown(index=False)+'\n\n## Selected peers and membership basis\n'+s[['ticker','tier','distance','membership','isin','inclusion_reason']].to_markdown(index=False)+'\n\n## Benchmarks\nPublished industry ratios only (not verified medians): peer EV/EBITDA median '+f"{m[m.multiple.eq('ev_ebitda')].iloc[0]['median']:.2f}"+'; pbv_industry / evebitda_industry EUROPE 2026-01 datasets resolved for Denmark; recorded in dataset_checks.json.\n\nSeeded EV checks: '+', '.join(pd.read_csv(P/'peer_ev_checks.csv').ticker if (P/'peer_ev_checks.csv').exists() else 'embedded in comparables_audit.xlsx EV_check sheet')+' (seed 20261030). Arithmetic checks pass; no human/source approval claimed.\n')

prim=m[m.multiple.eq('ev_ebitda')].iloc[0]
preds={x['model']:x for x in r['predictions']}
(P/'comparables_report.md').write_text(f"""# Ørsted comparables - 2026-10-30

DRAFT pending human Spot_check. Primary EV/EBITDA per bucket-B renewable-power mapping; hybrid DKK 20,955m stripped once from the EV-to-common-equity inversion and from target book equity (common 119,718). Dominant divergence: vendor EBITDA 21,583 / EBIT 12,495 vs issuer EBITDA 22,448 (25,065 excl. partnerships+cancellation) / EBIT 8,620 - issuer-basis sensitivities in sensitivities.csv. Peer EV uses vendor debt incl. leases + book NCI - cash; associates proxied by long-term investments - qualified only. FY2025 tax 47% is impairment-driven. Rights issue Oct 2025 leaves a transitional capital structure. No DCF, no recommendation, no synthesis weight, no residual-band classification.

## Selection
Initial pool {len(g)-1} candidates after source-availability gates, Europe-first. Ordered expansion log in peer_selection.json; Europe step already feasible (n_pool as recorded). Eight required score weights, pool-only 5/95 winsorization, STDEV.S standardization; missing dimensions renormalized.

{s[['ticker','tier','distance','country','membership','inclusion_reason']].to_markdown(index=False)}

## Primary and raw/scaled values
{m.to_markdown(index=False)}

## Bridge and fiscal bases
FY2025 financials at each fiscal end; quote prices/cap at 2026-10-30; FX ECB same date (DKK 7.4735). EV numerator: debt incl. leases + NCI - cash, associates excluded; target bridge additionally subtracts the DKK 20,955m equity-classified hybrid claim once. EV/CF uses reported CFO - financing-classification differences remain. Target NI/equity use parent-common basis (1,727 / 119,718).

## Sensitivities
p25/median/p75 are peer dispersion, not confidence intervals. Leave-one-out and issuer-basis EBIT/EBITDA diagnostics in sensitivities.csv.

## Sources and audit
Field-level sources in source_log.csv; selection logs and live scores in comparables_audit.xlsx; three seeded EV arithmetic rows in EV_check; human review explicitly pending.
""")

chosen=preds['PBV'] if preds['PBV']['published_r2']>=max(x['published_r2'] for x in r['predictions']) else max(r['predictions'],key=lambda x:x['published_r2'])
(P/'valuation_summary.md').write_text(f"""# Relative valuation by regression - Europe, ORSTED.CO, 2026-10-30

## Scope
ORSTED.CO only; no market sample/own estimation/DATA_BASE_MSCI under the published route.

## Headline
Draft {chosen['model']} selected by highest eligible published R2 ({chosen['published_r2']:.3f}), a weaker heuristic than adjusted-R2/industry fit.

## Data
FY2025 uniform vendor inputs cross-checked with the Ørsted annual report. Denmark listing resolves EUROPE exact. Sourced analyst consensus inputs used (g_eps 51.15%, g_rev 8.84%); no substitution needed. Common payout 0.0 (no FY2025 common dividend; NCI/hybrid distributions excluded). ROE on closing parent-common equity 119,718 (hybrid stripped).

## Fitted models
{pd.DataFrame(r['predictions'])[['model','predicted','published_r2','value_per_share','actual','deviation']].to_markdown(index=False)}

## Diagnostics
Integrity findings retained in regression_results.json and dataset_checks.json. GLOBAL PEG/PBV and EM EV/EBITDA source anomalies do not affect these EUROPE equations. No n, SEy, adjusted R2, p-values, A/B/C, typicality or D1-D10: n/a_published_route. Classification: Not classified (no SEy published). EV/EBITDA decimal vs percentage-point DFR/tax alternative recorded (21.25 vs 11.49 predicted; decimal approved).

## Limitations
Market-wide, low-R2 equations are not sector fair-value proof. January 2026 vintage ~9 months old at valuation date. Published EV definition undocumented; hybrid removed once in the EV->common bridge. Beta benchmark/frequency unspecified. Rights-issue-transitional leverage and impairment-driven 47% tax flagged.
""")
state=RunState(O/'run_state.json')
state.checkpoint('stage3_relative',next_step='QA block C once, then required PDF/plaintext; evidence gates and human review remain unresolved',note='10 numerical peers on first Europe step (no relaxation); default Tier3 cap 2 kept; regression PBV chosen by published R2. Not an unqualified final valuation.',outputs=[str(f.relative_to(ROOT)) for f in P.iterdir() if f.is_file()])
state.finish('stage3_relative',status='provisional',note='Numerical deliverables complete/recalculated; candidate-source qualification and human Spot_check not complete.')
state.append_run_log(ROOT/'memory/run_log.csv')
print('done')
