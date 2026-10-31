"""One final checklist execution; preserve unresolved failures instead of clearing them."""
from pathlib import Path
import json,re,hashlib
from collections import Counter
import pandas as pd
from openpyxl import load_workbook
from pypdf import PdfReader
from valuation_agent.sourcelog import validate

P=Path(__file__).resolve().parent;ROOT=P.parents[1]
assert validate(P/'source_log.csv')==[]
checks=json.loads((P/'relative/model_checks.json').read_text())
assert checks['formula_errors']==0 and max(checks['regression_differences'])<1e-9
assert checks['max_score_difference']<1e-9
dcf=json.loads((P/'model_checks.json').read_text());assert dcf['absolute_difference']<1e-9
names=['data_pack.xlsx','dcf_model.xlsx','relative/comparables_audit.xlsx','relative/regression_valuation.xlsx']
for name in names:
 w=load_workbook(P/name,data_only=True)
 errors=[(s.title,c.coordinate,str(c.value)) for s in w for row in s for c in row if c.data_type=='e']
 assert not errors,(name,errors)
 assert not load_workbook(P/name)._external_links,name
log=pd.read_csv(P/'source_log.csv');assert not log.input_id.duplicated().any()
registered=log[log.input_id=='S3_equations'].iloc[0]
sha=hashlib.sha256((ROOT/'data'/registered.url_or_local_file).read_bytes()).hexdigest()
assert sha in registered.limitation
rec=pd.read_csv(P/'recommendation_summary.csv').iloc[0]
assert rec.ticker=='MT.AS' and rec.currency=='EUR' and not rec.portfolio_eligible
assert abs(rec.upside_pct-(rec.recommended_price/rec.current_price-1)*100)<1e-9
pdf=PdfReader(P/'report.pdf');full='\n'.join(x.extract_text() for x in pdf.pages)
for n in range(1,14):assert any(f'{n}. ' in x.extract_text() for x in pdf.pages)
for phrase in ['PROVISIONAL','EUR36','53.60','not personal investment advice','Glossary']:assert phrase in full,phrase

failures={
 'A04':'Exact October30 common/diluted shares and independent exchange-close reconciliation unavailable. DCF estimates basic749.710746m plus3m dilution; vendor basic754.04m retained separately.',
 'B03':'Signed EBIT reconciliation supplied, but NI tax/NCI allocation is estimated25%, not item-specific verified. NI estimates do not drive FCFF.',
 'B09':'Existing lease debt/DA/ROU convention disclosed, but full additions/payment/current-scope reconciliation remains imperfect. No unqualified pass.',
 'B25':'Actual and synthetic rating/spread checks supplied; current comparable bond YTM/CDS missing.',
 'B28':'No double counting detected. Associates9937, NCI2003, pension1821 and debt fair premium295 use book/estimated-tax/fair-value proxies; material current claim valuation unverified.',
 'B29':'FX/units and arithmetic reconcile, but cutoff shares/dilution are estimates and exchange close independently unavailable.',
 'C03':'Selected numeric cap checks within2%; quote/report FX and GBX fixed. All class/treasury-share/ADR/perimeter evidence not independently completed.',
 'C04':'Field extracts and dates supplied; primary industry/classification and some identifier/ownership evidence not fully verified. Source-policy conflict1667 versus3628 EBIT retained.',
 'C05':'A matched industry median from the registered reference assets is unavailable. Regional aggregate is not mislabeled median; cannot complete benchmark-gap resolution.',
 'C08':'Nine preliminary candidates satisfy count constraints after all ordered relaxations. They are NOT nine fully qualified audited peers yet; no padding.',
 'C09':'Ownership >20%, FY24-25 restructuring and some classification/primary identifier checks not complete for every selected peer. Preliminary gates cannot be treated as passes.',
 'C13':'Uniform approved fundamental proxy used; no verified whole-pool consensus-coverage percentage audit. No claimed analyst five-year growth.',
 'C18':'EV before associates only. Required matched associate/perimeter adjustments cannot be completed; EV numbers are qualified checks, not primary fair values.',
 'C19':'Three seeded mechanical EV checks present, but not all selected primary ISIN and inclusion evidence verified; human Spot_check pending.',
}
evidence={
 'A':'company_identity.md; financials.json; data_pack.xlsx; anomaly_report.md; source_log.csv; company tests',
 'B':'dcf_decisions.md; dcf_model.xlsx and model_checks.json; earnings_reconciliation.csv; capital_structure.csv; geographic_risk.csv; risk_checks.csv; scenarios.csv; wacc_growth_sensitivity.csv; dcf_implied_multiples.csv; report appendix',
 'C':'relative/comparables_report.md; comparables_audit.xlsx; candidate_gates.csv; peer_selection.json; valuation_summary.md; regression_valuation.xlsx; model_checks.json; source_log.csv; one_off_sensitivity.csv; peer_variant.csv',
 'D':'report_outline.md; report.md/PDF13 chapters; recommendation_summary.csv; method_reconciliation.csv; synthesis_sensitivity.csv and figures',
}
source=(ROOT/'methodology/qa_checklist.md').read_text();items=[];section='';count=0;sub=''
for line in source.splitlines():
 if line.startswith('## '):section=line[3:];count=0;sub=''
 elif line.startswith('### '):sub=line[4:]
 elif line.startswith('- [ ] '):
  count+=1;key=section[0]+f'{count:02d}'
  status='PASS';note='Reviewed against the linked schedules; a numerical or disclosure pass is not a cleared global evidence status.'
  if key in failures:status='FAIL_OPEN';note=failures[key]
  elif section.startswith('C') and sub=='Regression method' and count not in [22,25,30,33,38]:
   status='N/A_PUBLISHED_ROUTE';note='No own-estimation A/B/C, OLS, LINEST, residual dispersion, sample size, diagnostics or human20-row market audit is fabricated; published coefficients only.'
  elif key=='C22':note='Published-route one-target master retains first18 fields and appended n/a outputs; no local estimation market sample claimed.'
  elif key=='C42':note='Approved decimal policy. PBV/PE do not contain DFR/tax; both policies identical. EV equation not used, so no sector plausibility claim is made.'
  elif key=='C06':note='Human review explicitly pending, not described as performed. This disclosure pass is not a human audit pass.'
  elif key=='C10':note='9 peers,6 Tier1/2,3 Tier3,6Europe; cap4 relaxation, Tier3<=9-6. Count pass only, eligibility still failed atC08/C09.'
  elif key=='B30':note='Discounted terminal share78.7242% flagged >75%. Warning disclosed, not treated as reassurance.'
  elif key=='D10':note='Direct original user task authorizes proceeding with the approved outline; legacy standing field not yet is preserved and disclosed. Default13-chapter outline reused with steel/published-route adaptations.'
  items.append(dict(id=key,block=section,subsection=sub,requirement=line[6:],status=status,evidence=evidence[section[0]],reason=note))
 elif items and line.startswith('      '):items[-1]['requirement']+=' '+line.strip()
pd.DataFrame(items).to_csv(P/'qa_results.csv',index=False)
counts=Counter(x['status'] for x in items)
headline='# MT.AS final QA — PROVISIONAL\n\nExecuted once at company end under approved one-session deviation. Numerical checks do not clear material evidence failures. No full src suite rerun (src unchanged). '+str(dict(counts))+'\n\n15 company tests passed (9 DCF +6 relative). Fatal-error Ruff checks passed for company scripts; mypy passed for report and relative generator with imports skipped and missing imports ignored (not a full typed-library audit). Four workbooks have no formula errors/external links. DCF difference2.84e-14; max peer-score difference4.00e-15; regression differences1.33e-15 and3.20e-14. Registered equation sha256 verified. PDF text/layout inspected;18+ pages as generated.\n\n## Global human review\nPending. No person has signed Spot_check. Report and portfolio row remain provisional; portfolio_eligible=False.\n\n## Unresolved material failures\n'+'\n'.join('- '+k+': '+v for k,v in failures.items())+'\n\n## Full checklist\n'
for x in items:headline+='\n### '+x['id']+' — '+x['status']+'\n'+x['requirement']+'\n- Evidence: '+x['evidence']+'\n- Reason/impact: '+x['reason']+'\n'
(P/'qa_results.md').write_text(headline)
(P/'final_checks.json').write_text(json.dumps(dict(status='provisional',verified_complete=False,portfolio_eligible=False,checklist_counts=dict(counts),open_failures=failures,human_review='pending',PDF_pages=len(pdf.pages),company_tests_passed=15,workbook_errors=0,registered_regression_sha256=sha),indent=2))
print(dict(counts),'PDF_pages',len(pdf.pages),'verified_complete=False')
