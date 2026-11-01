"""Single QA-C assessment and short, explicitly provisional report."""
from pathlib import Path
import json,time,datetime,csv,html
from collections import Counter
import pandas as pd
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,Table,TableStyle,PageBreak
from reportlab.lib.styles import getSampleStyleSheet
from reportlab.lib import colors
from valuation_agent import datasets
P=Path(__file__).resolve().parent;O=P.parent;ROOT=P.parents[2];start=time.time()
assert not (P/'qa_results.md').exists(),'QA C already executed; do not repeat passing checks'
q=(ROOT/'methodology/qa_checklist.md').read_text();q=q[q.index('## C.'):q.index('## D.')];items=[x[6:] for x in q.splitlines() if x.startswith('- [ ] ')]
source_fail={3:'Vendor855.34m versus issuer850m outstanding/issued definition unresolved.',4:'Some transformations lack complete issuer/source certification; numeric lineage alone is insufficient.',5:'Exact matching industry medians unavailable; published aggregate ratios are labelled, not called medians.',8:'10 numeric peers are not certified as ten qualified peers; comparable conclusion blocked.',9:'Complete ownership/event/history verification for all26 candidates not completed; no waiver.',11:'Candidate/expansion/scoring audit exists, but full business/event source review incomplete.',17:'PE is indicative fallback only; source gates prevent a qualified primary.',18:'Only qualified pre-associate EV cross-checks available; claim/lease/associate fair-value consistency unresolved.',20:'Peer/IQR/LOO/common-margin sensitivities exist, but no substantiated uniform material-one-off normalization.'}
own_na={23,26,27,28,30,31,33,34,36}
checks=[]
for i,item in enumerate(items,1):
 status='FAIL' if i in source_fail else 'N/A' if i in own_na else 'PASS'
 detail=source_fail.get(i,'Published route: no own-estimation sample, A/B/C, LINEST, OLS, typicality or residual bands.' if i in own_na else 'Reviewed against generated artifacts, source log, formula_checks.json and evidence_review.md.')
 if 'plausibility check against the sector median' in item:status='FAIL';detail='Both policies computed; approved decimal chosen; plausibility uses labelled published industry ratio, not a verified median.'
 if 'column' in item.lower() and 'logical' in item.lower():detail='Resolver families and exact logical column names recorded in evidence_review.md; no guessed aliases.'
 checks.append(dict(item=i,status=status,requirement=item,detail=detail))
integrity=[]
for family in ['regressions_multi','evebitda_industry','pbv_industry']:
 ds=datasets.equation_for('Germany','PBV','2026-10-30')[1].dataset if family=='regressions_multi' else datasets.resolve(family,country='Germany',valuation_date='2026-10-30').dataset
 findings=datasets.check_dataset(ds);integrity.append(dict(family=family,dataset=ds.dataset_id,findings=[dict(severity=f.severity,code=f.code,message=f.message) for f in findings]));assert not any(f.severity=='error' for f in findings)
(P/'dataset_checks.json').write_text(json.dumps(integrity,indent=2)+'\n')
counts=Counter(x['status'] for x in checks)
(P/'qa_results.md').write_text('# QA block C — one execution, 2026-11-01\n\n**NOT PASSED / PROVISIONAL.** '+str(dict(counts))+'\nSource/qualification failures below are unresolved, not waived. Numerical/library/workbook checks pass; human Spot_check pending separately. No own-estimation tests, no duplicate full QA. No failure silently converted to a pass.\n\n'+ '\n\n'.join(f"### C{x['item']} — {x['status']}\n{x['requirement']}\n\n{x['detail']}" for x in checks)+'\n\n## Failure disposition\nComputed prices are diagnostic only. Fewer than8 independently source-qualified peers have been certified, so the comparable conclusion is blocked, not an approved relaxed valuation. Human review plus completion of source/normalization/claim gates required before use. Industry median unavailable from registered dataset: report limitation instead of fabricating statistic. No failing code arithmetic found; source gaps remain explicitly unresolved.\n')
s=pd.read_csv(P/'comparables.csv');m=pd.read_csv(P/'multiples_summary.csv');r=json.loads((P/'regression_results.json').read_text());pe=m[m.multiple.eq('pe')].iloc[0]
price=126.92;shares=855.34
figures=dict(ticker='ENR.DE',valuation_date='2026-10-30',current_price=price,shares_m=shares,issuer_issued_shares_m=850,peer_count=len(s),tier12=int((s.tier<=2).sum()),tier3=int((s.tier==3).sum()),europe=int(s.europe.sum()),raw_pe_median=float(pe['median']),scaled_pe_median=float(pe.adjusted_median),peer_indicative=float(pe.value_per_share_mid),peer_iqr_low=float(pe.value_per_share_low),peer_iqr_high=float(pe.value_per_share_high),peer_upside=float(pe.value_per_share_mid)/price-1,regression_pbv=float(r['predictions'][1]['value_per_share']),qa=dict(counts))
lines=[
 '# Siemens Energy AG (ENR.DE) — short relative-only report',
 'Valuation date2026-10-30 | information cutoff2026-10-30 | accessed2026-11-01 | EUR/share unless stated.',
 'STATUS: PROVISIONAL / QA-C NOT PASSED. Source-qualified comparable conclusion BLOCKED. Figures below are reproducible diagnostics, not an unqualified valuation or investment recommendation.',
 'Scope: ENR.DE only; standard / published_damodaran / web_minimum. Germany/EUR dated cache reused, no Stage0 rebuild or top-up. Full Stage1, DCF and Stage4 skipped by approved relative_only deviation. Mandatory short PDF supplied per explicit user override of no-PDF default.',
 '1. Financial basis and definitions',
 'FY2025 ended2025-09-30 (not TTM/forward); EURm. Sales39077; parent NI1414; standardized vendor EBIT1569; income-statement D&A1111; EBITDA2680; CFO5821; capex1724; common equity10301 (prior9075); assets56637; lease-inclusive debt3966; cash9162; NCI375; associates703 book proxy.',
 'Issuer operating2149 less equity-accounted580 reconciles vendor1569. ParentNI1414 plus minority271 reconciles group1685. EBITDA2680 is not cashflow D&A-based; customer advances make CFO unlike FCFF. FY2025 cash dividend0; proposed0.70 is not paid-FY2025 payout. NI/average-common-equity fundamental growth14.5954% for peers; closing-common-equity13.7278% for published route. Growth is NOT analyst consensus.',
 f'Current quote{price:.2f}; uniform vendor shares{shares:.2f}m and rounded cap108560m. Issuer states850m ISSUED asof2026-10-13: outstanding/treasury definition unresolved. Cap arithmetic within0.00023% does not settle it. All fixed-equity per-share values at850m increase{(shares/850-1)*100:.6f}%.',
 '2. Peer diagnostics — not source-qualified fair value',
 f'26 initial candidates; final numeric10 peers, {figures["tier12"]} Tier1/2, {figures["tier3"]} Tier3, {figures["europe"]} Europe-listed. Standard World proxy entity/name match used; IMI-only candidates excluded. Ordered expansions: Europe -> World ->0.05–20x size ->Tier3 cap4 (3 used). No other hard filter waived. Peers: '+', '.join(s.ticker)+'.',
 'Eight score weights: growth30%, beta15%, leverage10%, ROE10%, EBITDAmargin10%, payout7.5%, capex/sales7.5%, log EURcap10%. Pool-only5/95 clipping/sampleSD; positive extremes remain in multiple distributions. Full pool/selection/parameter/source schedules retained.',
 f'Equipment default EV/EBIT cannot be unqualified because peer associates/claim/lease definitions are unresolved; EV/sales shares the same bridge problem. PE used only as indicative equity fallback. Raw PE median{pe["median"]:.6f}x; growth-scaled PE median{pe.adjusted_median:.6f}x (10 valid). Indicative scaled-PE value{pe.value_per_share_mid:.6f}; peer-IQR dispersion{pe.value_per_share_low:.6f}–{pe.value_per_share_high:.6f}; vs quote{(pe.value_per_share_mid/price-1)*100:.4f}%. IQR is NOT a confidence interval.',
 f'Raw PE value{pe.raw_value_mid:.6f}. Share sensitivity at850m: indicative scaled PE{pe.value_per_share_mid*shares/850:.6f}; IQR{pe.value_per_share_low*shares/850:.6f}–{pe.value_per_share_high*shares/850:.6f}. Other full raw/scaled multiples/counts/skew in multiples_summary.csv; relativePE and TobinQ unavailable, not invented.',
 '3. Published-regression diagnostics',
 'Germany resolves EUROPE; January2026 equations asof2026-01-01 (302days old). No market estimation, sector-specific fit, SEy, p-values, adjustedR2, A/B/C, D1–D10 or residual classification. Classification: Not classified (no SEy published). Model choice by highest publishedR2 is a weak heuristic only.',
 ]
for p in r['predictions']:
 equation={'PE':'9.72 +2.99 beta +49.82 g_eps +7.98 payout','PBV':'.73 +3.92 g_eps +.13 beta +10.75 ROE -.25 payout','EV/EBITDA':'18.15 +35.25 g_rev -.11 DFR -.12 tax +2.29 ROIC'}[p['model']]
 lines.append(f'{p["model"]}: prediction{p["predicted"]:.9f}x; publishedR2{p["published_r2"]:.3f}; implied{p["value_per_share"]:.6f};850m sensitivity{p["value_per_share"]*shares/850:.6f}. Equation: {equation}.')
alt=r['predictions'][2]['unit_alternative']['dfr_tax_percent_points'];altprice=(alt*2680-3966-375+9162)/shares
lines +=[
 f'Chosen published PBV implied{figures["regression_pbv"]:.6f}; vs quote{(figures["regression_pbv"]/price-1)*100:.4f}%. Highest publishedR2.423, not sector fit or proof of mispricing. Decimal DFR/tax policy explicitly approved; EVEBITDA alternative percent-point prediction{alt:.9f}x, implied{altprice:.6f}. Both scenarios preserved; source-unit ambiguity not resolved by approval.',
 'Registered dataset regressions_multi_2026-01 SHA a894ea86f209d59c68c57ba5674ee096ee875cf9726af2cfe84ec212af1d9bf5. GLOBAL PEG sign/tstat, GLOBAL PBV beta sign and EM ROIC sign warnings not used. All exact coefficients/tstats and input IDs in live workbook; post-LibreOffice recalculation all predictions/prices/scores agree with library within1e-9. Published EV definition undocumented; no associate removal imposed on regression EV bridge.',
 '4. Benchmark, sensitivity and limits',
 'Closest Electrical Equipment EUROPE published ratios: EVEBITDA18.94, EVEBIT24.34, PBV5.71 (146 firms). Machinery/GreenRenewable alternatives investigated. These are NOT verified industry medians; aggregate-versus-median comparison remains a QA failure. Target EVEBITDA38.70858 is104.38% above18.94, plausibly recovery-priced against weak reported FY margins, not grounds to overwrite data. Neither unit policy >30% above18.94; this plausibility is not unit proof.',
 'Sensitivities: raw/scaled and peer quartiles, leave-one-out peer set, all-observation EBIT margins4/6/8/10% (mechanical scaling largely cancels),850m share denominator, both unit policies; target-only net special-item+6 removal is a diagnostic, NOT uniform normalized peer earnings. Gross target restructuring/standalone costs exceed10% EBIT while offsetting portfolio gains mask net. No substantiated uniform normalization constructed.',
 'Unresolved QA: full two-way ownership/event/history qualification for all candidates, valid outstanding shares, authentic matching industry medians, uniform material-one-off normalization and comparable EV claim/lease/associate consistency. Three seeded arithmetic EV checks PASS, human Spot_check PENDING (not performed/waived). Ten numeric names do not satisfy ten qualified peers until these gates are cleared. No final fair-value recommendation is issued.',
 '5. Source and reproducibility pointers',
 'Uniform raw financial/statistics/history: https://stockanalysis.com/quote/etr/ENR/financials/ and peer-specific URLs in relative/source_log.csv. Issuer: https://www.siemens-energy.com/global/en/home/investor-relations/share.html and FY2025 annual report (linked in relative_inputs.md / relative/evidence_review.md). Standard proxy dated2026-10-29: https://www.ishares.com/us/products/239696/ishares-msci-world-etf/latest-holdings.csv . Library IDs/SHA/vintage/mappings and all qualification evidence: relative/evidence_review.md, regression_results.json, dataset_checks.json, candidate_gates.csv. All numbers derive from the attached run artifacts; no DCF used.',
 'Reproduce from repository root: PYTHONPATH=src python outputs/ENR.DE_2026-10-30/relative/build.py; LibreOffice headless recalculate both workbooks in a separate directory, compare with formula_checks.json. finalize_stage3.py is a one-time checkpoint helper, not safe to rerun on finished state. qa_and_report.py intentionally refuses a second full QA run. Cached parsed data and source locators committed; market cache never rebuilt.',
 'Academic analysis only. Not investment advice; source limitations and model assumptions can materially change results.'
 ]
(O/'relative_summary.md').write_text('\n\n'.join(lines)+'\n');(P/'report_figures.json').write_text(json.dumps(figures,indent=2)+'\n')
styles=getSampleStyleSheet();styles['BodyText'].fontSize=9;styles['BodyText'].leading=12;story=[]
for i,line in enumerate(lines):
 style=styles['Title'] if i==0 else styles['Heading2'] if line[:2] in ['1.','2.','3.','4.','5.'] else styles['BodyText']
 story.append(Paragraph(html.escape(line.lstrip('# ')),style));story.append(Spacer(1,6))
pdf=O/'relative_report_ENR.DE.pdf';SimpleDocTemplate(str(pdf),pagesize=(595,842),rightMargin=42,leftMargin=42,topMargin=38,bottomMargin=38).build(story)
state=json.loads((O/'run_state.json').read_text());now=datetime.datetime.now(datetime.timezone.utc).isoformat(timespec='seconds');elapsed=round((datetime.datetime.fromisoformat(now)-datetime.datetime.fromisoformat(state['stages']['stage3_relative']['finished'])).total_seconds()/60,2)
state['qa_C']={'status':'failed_provisional','executions':1,'counts':dict(counts),'human_spot_check':'pending','evidence_failures_waived':False,'finished':now}
state['short_report']={'status':'done_provisional','pdf':str(pdf.relative_to(ROOT)),'plaintext':str((O/'relative_summary.md').relative_to(ROOT)),'same_figures':True,'elapsed_min':elapsed,'finished':now}
state['stages']['stage3_relative']['next_step']='Do not issue qualified comparable conclusion until QA source failures are resolved; human Spot_check pending.'
(O/'run_state.json').write_text(json.dumps(state,indent=2)+'\n')
with (ROOT/'memory/run_log.csv').open('a',newline='') as f:csv.writer(f,lineterminator='\n').writerow(['ENR.DE_2026-10-30','Siemens Energy AG','standard','qa_C_short_report','done_provisional',elapsed,now])
print('QA',dict(counts),'PDF',pdf.stat().st_size,'bytes',figures)
