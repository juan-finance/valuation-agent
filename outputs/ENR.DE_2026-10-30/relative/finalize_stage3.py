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
e=P/'evidence_review.md';txt=e.read_text().replace('## Selected-peer official ISIN evidence and business review','## Initial numeric-screen identity and business evidence (superseded selection below)').replace('## Membership and country','## Initial membership review (superseded by standard-proxy check below)')
start=txt.index('## Candidate rejections');end=txt.index('## Review gates')
txt=txt[:start]+txt[start:end].replace('Full final numeric pool17, final size0.05–20x leaves16 (Rotork below widened size floor); selected10.','Initial IMI-only diagnostic had17 numerically eligible rows. Final standard-index check removes small caps before scoring; see final selection below.').replace('Peer medians EVEBITDA17.45696 (−7.83% vs18.94), EVEBIT21.39845 (−12.09% vs24.34), PBV5.39066 (−5.59% vs5.71).','Initial-set benchmark comparisons superseded by final table below.')+txt[end:]
txt+='\n## FINAL standard-index check and effective selection\nThe complete cached URTH source header is2026-10-29. Entity/name/market matching avoids ticker collisions: SU=SchneiderFrance, not SuncorCanada; SUN=SuncorpAustralia is NOT SulzerSwitzerland. ATCO A/EPI A/SKF B are the corresponding Nordic classes. NDX1/ANDR/IMI/NKT/NEX/SUN/WEIR/ROR are absent as matching entities and cannot qualify from IEUR IMI alone. Standard matches are extracted in world_pool_membership.csv. European standard World constituents with matching developed listing country supply Europe eligibility proxy; no exact MSCI constituent-file claim. Final numeric pool10 after existing exclusions; initial Europe band8, World9, widened band10 but only7 Tier1/2, so final Tier3-cap relaxation4 required (3 used). No other filter relaxed. Full candidate ownership/event/history source certification still incomplete: the numeric set remains provisional, not falsely qualified.\n\n'+s[['ticker','tier','distance','membership']].to_markdown(index=False)+'\n'
txt+='\nNew selected official ISINs (all pages opened): ALFA SE0000695876 https://www.boerse-frankfurt.de/aktie/alfa-laval ; SPX GB00BWFGQN14 https://www.londonstockexchange.com/en/news/article/SPX/change-in-major-shareholding/2666-8e-82-9c-bd-4b7d88 ; G1A DE0006602006 https://www.gea.com/en/company/investor-relations/share-information/share-price/ . ALFA heat-transfer/rotating equipment Tier2: FY2025 governance Winder29.53%, independent of ENR, https://www.alfalaval.com/globalassets/documents/investors/english/corporate-governance-reports/alfa-laval_corporate-governance-report_2025_260324.pdf.pdf . SPX steam/thermal equipment Tier2, listed1959,2025 organizational restructuring (not an assumed unchanged margin): https://www.spiraxgroup.com/en/investors/results-reports-and-presentations/2025-digital-annual-report . GEA process/food machinery Tier3,2026 organization change announcedFY2025; buyback cancellation explains shares decline, https://cdn.gea.com/-/media/investors/annual-report/2025/annual-report-2025-en.pdf . Neither new name silently upgrades incomplete event/ownership certification.\n'
txt+='\nFinal benchmark schedule (industry published ratios, not verified medians):\n'+pd.DataFrame([dict(multiple=k,peer_median=float(m[m.multiple.eq(k)].iloc[0]['median']),industry_ratio=b,gap=float(m[m.multiple.eq(k)].iloc[0]['median'])/b-1) for k,b in [('ev_ebitda',18.94),('ev_ebit',24.34),('pbv',5.71)]]).to_markdown(index=False)+'\nFinal seeded EV checks are '+', '.join(pd.read_csv(P/'peer_ev_checks.csv').ticker)+' (seed20261030); prior LR/NDX1/VWS diagnostic is superseded. All arithmetic checks pass, not a claim human/source approval occurred.\n'
e.write_text(txt)
vr=P/'valuation_summary.md';vr.write_text(vr.read_text().replace('## Data','## Scope\nENR.DE only; no market sample/own estimation/DATA_BASE_MSCI under published route. Other candidates are not additional valuation targets.\n\n## Data',1)+'\n## Exact equations and t-statistics\nSee Coefficients_PE/PBV/EV_EBITDA workbook sheets for each coefficient/t statistic and dataset SHA.\n'+ '\n'.join(p['equation'] for p in r['predictions'])+'\n')
root=P.parent
# Reusable parsed statement excerpts, not redundant complete annual-report copies.
raw=root/'annual_report_2025.txt'
if raw.exists():
 lines=raw.read_text().splitlines();(ROOT/'cache/market/2026-10-30/candidates/ENR_issuer_FY2025_statements.txt').write_text('\n'.join(lines[8017:8310])+'\n')
 raw.unlink();(root/'annual_report_2025.pdf').unlink()
for f in (P/'recalculated').glob('*.xlsx'):f.unlink()
(P/'recalculated').rmdir()
state=RunState(root/'run_state.json');state.checkpoint('stage3_relative',next_step='QA block C once, then required PDF/plaintext; evidence gates and human review remain unresolved',note='10 numerical peers; 7 Tier1/2,3 Tier3,9Europe, cap4 relaxation. PE fallback; regression PBV. Not an unqualified final valuation.',outputs=[str(f.relative_to(ROOT)) for f in P.iterdir() if f.is_file()]);state.finish('stage3_relative',status='provisional',note='Numerical deliverables complete/recalculated; candidate-source qualification, normalization and human Spot_check not complete.');state.append_run_log(ROOT/'memory/run_log.csv')
print('stage3 checkpoint',state.d['stages']['stage3_relative'])
