"""Single QA-C assessment and short, explicitly provisional report for NKT.CO."""
from pathlib import Path
import json,time,datetime,csv,html
from collections import Counter
import pandas as pd
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer
from reportlab.lib.styles import getSampleStyleSheet
from valuation_agent import datasets
P=Path(__file__).resolve().parent;O=P.parent;ROOT=P.parents[2];start=time.time()
assert not (P/'qa_results.md').exists(),'QA C already executed; do not repeat passing checks'
q=(ROOT/'methodology/qa_checklist.md').read_text();q=q[q.index('## C.'):q.index('## D.')];items=[x[6:] for x in q.splitlines() if x.startswith('- [ ] ')]
source_fail={4:'Some transformations lack complete issuer/source certification; numeric lineage alone is insufficient.',5:'Exact matching industry medians unavailable; published aggregate ratios are labelled, not called medians.',8:'10 numeric peers are not certified as ten qualified peers; comparable conclusion blocked.',9:'Complete ownership/event/history verification for all 31 candidates not completed; no waiver.',11:'Candidate/expansion/scoring audit exists, but full business/event source review incomplete.',18:'Only qualified pre-LT-investment EV cross-checks available; claim/lease/associate fair-value consistency unresolved (hybrid claim handled once).',20:'Peer/IQR/LOO/issuer-basis sensitivities exist, but no substantiated uniform material-one-off normalization (vendor EBIT 578 vs issuer 257).'}
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
 ds=datasets.equation_for('Denmark','PBV','2026-10-30')[1].dataset if family=='regressions_multi' else datasets.resolve(family,country='Denmark',valuation_date='2026-10-30').dataset
 findings=datasets.check_dataset(ds);integrity.append(dict(family=family,dataset=ds.dataset_id,findings=[dict(severity=f.severity,code=f.code,message=f.message) for f in findings]));assert not any(f.severity=='error' for f in findings)
(P/'dataset_checks.json').write_text(json.dumps(integrity,indent=2)+'\n')
counts=Counter(x['status'] for x in checks)
(P/'qa_results.md').write_text('# QA block C - one execution, 2026-11-01\n\n**NOT PASSED / PROVISIONAL.** '+str(dict(counts))+'\nSource/qualification failures below are unresolved, not waived. Numerical/library/workbook checks pass; human Spot_check pending separately. No own-estimation tests, no duplicate full QA. No failure silently converted to a pass.\n\n'+ '\n\n'.join(f"### C{x['item']} - {x['status']}\n{x['requirement']}\n\n{x['detail']}" for x in checks)+'\n\n## Failure disposition\nComputed prices are diagnostic only. Fewer than 10 independently source-qualified peers have been certified, so the comparable conclusion is blocked, not an approved relaxed valuation. Human review plus completion of source/normalization/claim gates required before use. Industry median unavailable from registered dataset: report limitation instead of fabricating statistic. No failing code arithmetic found; source gaps remain explicitly unresolved.\n')
s=pd.read_csv(P/'comparables.csv');m=pd.read_csv(P/'multiples_summary.csv');r=json.loads((P/'regression_results.json').read_text());pe=m[m.multiple.eq('pe')].iloc[0];eveb=m[m.multiple.eq('ev_ebit')].iloc[0]
price_dkk=839.0;price=price_dkk/7.4735;shares=53.45
pbv=[p for p in r['predictions'] if p['model']=='PBV'][0];peq=[p for p in r['predictions'] if p['model']=='PE'][0];evq=[p for p in r['predictions'] if p['model']=='EV/EBITDA'][0]
figures=dict(ticker='NKT.CO',valuation_date='2026-10-30',current_price=price,current_price_dkk=price_dkk,quote_currency='DKK',shares_m=shares,peer_count=len(s),tier12=int((s.tier<=2).sum()),tier3=int((s.tier==3).sum()),europe=int(s.europe.sum()),raw_pe_median=float(pe['median']),scaled_pe_median=float(pe.adjusted_median),peer_indicative=float(pe.value_per_share_mid),peer_iqr_low=float(pe.value_per_share_low),peer_iqr_high=float(pe.value_per_share_high),peer_upside=float(pe.value_per_share_mid)/price-1,regression_pbv=float(pbv['value_per_share']),regression_pe=float(peq['value_per_share']),regression_evebitda=float(evq['value_per_share']),qa=dict(counts))
lines=[
 '# NKT A/S (NKT.CO) - short relative-only report',
 'Valuation date 2026-10-30 | price date 2026-10-30 | accessed 2026-11-01 | EUR/share unless stated (quote DKK 839.0 = EUR 112.26 at ECB 7.4735).',
 'STATUS: PROVISIONAL / QA-C NOT PASSED. Source-qualified comparable conclusion BLOCKED. Figures below are reproducible diagnostics, not an unqualified valuation or investment recommendation.',
 'Scope: NKT.CO only; standard / published_damodaran / web_minimum. 2026-10-30 dated cache reused; stage0 Denmark sovereign top-up only. Full Stage1, DCF and Stage4 skipped by approved relative_only deviation. Mandatory short PDF supplied per explicit user override of no-PDF default.',
 '1. Financial basis and definitions',
 'FY2025 calendar year (not TTM/forward); EURm. Sales 3,565; EBIT 578 / EBITDA 680 vendor-uniform basis (issuer EBIT 257 / operational EBITDA 390; pretax 294 reconciles exactly - dominant divergence, sensitivities shown); NI 275; NI to common 264 (hybrid coupon ~11 stripped); group equity 2,193 incl EUR 150m equity-classified hybrid -> common 2,043; debt incl leases 251; cash&ST 1,214 (net cash 963); NCI 0; CFO 499; capex 695; dividends paid 11; effective tax 6.46% one-off-driven (tax 19/pretax 294).',
 'Issuer cross-check via NKT annual report 2025: revenue 3,565, NI 275, equity 2,193, NIBD -963, CFO 499, CapEx -695 match vendor exactly. Hybrids: EUR 150m 7.24% callable 1-Jul-2026 (DK0030510995) and EUR 150m 5.00% issued Mar 2026; equity-classified - claim deducted once in the EV-to-common bridge.',
 'Current quote DKK 839.0 (EUR 112.26); shares 53.45m; market cap EUR ~6,001m. EV EUR 5,038m = 6,001+251+0-1,214 (debt+NCI-cash&ST); LT investments not in bridge. Vendor beta 0.65 kept (within 0-2.5 band); no relevering needed.',
 '2. Peer diagnostics - not source-qualified fair value',
 f'31 candidate rows collected, Europe-first; first Europe step already feasible - 10 numeric peers, {figures["tier12"]} Tier1/2, {figures["tier3"]} Tier3, {figures["europe"]} Europe-listed; no relaxation step used. Standard proxies: IEUR MSCI Europe IMI for European names. Hard exclusions: ELHA (Greece MSCI EM), GEV (Apr-2024 spin-off inside FY2024-25 comparison period + one-off FY2025 tax benefit), ATCO.A/EPI.A (dual-class cap reconciliation >2%). Peers: '+', '.join(s.ticker)+'.',
 'Eight score weights: growth 30%, beta 15%, net debt/EBITDA 10%, ROE 10%, EBITDA margin 10%, payout 7.5%, capex/sales 7.5%, log EUR cap 10%. Pool-only 5/95 clipping/sampleSD; positive extremes retained. Vendor betas carry a benchmark/frequency-unavailable flag; distance driven mainly by size/leverage/margins.',
 f'Bucket-D primary PE (scaled by growth, 10 valid). Peer PE median {pe["median"]:.4f}x raw / {pe.adjusted_median:.4f}x growth-scaled; target growth {r["inputs"]["g_eps"]*100:.2f}% fundamental (ROE x retention). Indicative value {pe.value_per_share_mid:.6f} EUR (scaled); raw-basis {pe.raw_value_mid:.6f} EUR; peer-IQR dispersion {pe.value_per_share_low:.6f}-{pe.value_per_share_high:.6f} EUR; vs EUR quote {(pe.value_per_share_mid/price-1)*100:.4f}%. IQR is NOT a confidence interval.',
 f'Cross-check EV/EBIT median {eveb["median"]:.4f}x -> {eveb.value_per_share_mid:.6f} EUR (qualified: pre-LT-investment perimeter, hybrid claim once). Other multiples in multiples_summary.csv; relative PE (matching index) and Tobin Q unavailable, not invented.',
 '3. Published-regression diagnostics',
 'Denmark resolves EUROPE exact; January 2026 equations as-of 2026-01-01 (302 days old). No market estimation, sector-specific fit, SEy, p-values, adjusted R2, A/B/C, D1-D10 or residual classification. Classification: Not classified (no SEy published). Model choice by highest published R2 is a weak heuristic only.',
 f'PE: prediction {peq["predicted"]:.9f}x; published R2 {peq["published_r2"]:.3f}; implied {peq["value_per_share"]:.6f} EUR. Equation: 9.72 +2.99 beta +49.82 g_eps +7.98 payout.',
 f'PBV: prediction {pbv["predicted"]:.9f}x; published R2 {pbv["published_r2"]:.3f}; implied {pbv["value_per_share"]:.6f} EUR. Equation: .73 +3.92 g_eps +.13 beta +10.75 ROE -.25 payout.',
 f'EV/EBITDA: prediction {evq["predicted"]:.9f}x; published R2 {evq["published_r2"]:.3f}; implied {evq["value_per_share"]:.6f} EUR. Equation: 18.15 +35.25 g_rev -.11 DFR -.12 tax +2.29 ROIC. Extreme implied value driven by substituted 12.4% growth and vendor EBITDA basis - diagnostic only.',
 f'Chosen published PBV implied {figures["regression_pbv"]:.6f} EUR; vs EUR quote {(figures["regression_pbv"]/price-1)*100:.4f}%. Highest published R2 0.423, not sector fit or proof of mispricing. Decimal DFR/tax policy explicitly approved; EV/EBITDA alternative percent-point prediction {evq["unit_alternative"]["dfr_tax_percent_points"]:.9f}x.',
 'Registered dataset regressions_multi_2026-01 SHA a894ea86f209d59c68c57ba5674ee096ee875cf9726af2cfe84ec212af1d9bf5. GLOBAL PEG sign/tstat, GLOBAL PBV beta sign and EM ROIC sign warnings not used. All exact coefficients/tstats and input IDs in live workbook; post-LibreOffice recalculation all predictions/prices/scores agree with library within 1e-9. Published EV definition undocumented.',
 '4. Benchmark, sensitivity and limits',
 'Closest Electrical Equipment EUROPE published ratios: EVEBITDA 18.94x, EVEBIT 24.34x (146 firms, pos-EBITDA basis), PBV 5.71. Machinery alternative: 14.98x / 4.05 (210 firms). These are NOT verified industry medians; aggregate-versus-median comparison remains a QA failure.',
 'Sensitivities: raw/scaled and peer quartiles, leave-one-out peer set, group-NI 275 (vs common 264), issuer EBITDA 390 and issuer EBIT 257 basis diagnostics (vs vendor 680/578) in sensitivities.csv. No substantiated uniform normalization constructed.',
 'Unresolved QA: full two-way ownership/event/history qualification for all candidates, authentic matching industry medians, uniform material-one-off normalization and comparable EV claim/lease/LT-investment consistency. Three seeded arithmetic EV checks PASS, human Spot_check PENDING (not performed/waived). Ten numeric names do not satisfy ten qualified peers until these gates are cleared. No final fair-value recommendation is issued.',
 '5. Source and reproducibility pointers',
 'Uniform raw financial/statistics/history: https://stockanalysis.com/quote/cph/NKT/financials/ and peer-specific URLs in relative/source_log.csv. Issuer: NKT annual report 2025 (linked in relative_inputs.md). Standard proxy dated 2026-10-29: https://www.ishares.com/us/products/239696/ishares-msci-world-etf/latest-holdings.csv . Library IDs/SHA/vintage/mappings and all qualification evidence: relative/evidence_review.md, regression_results.json, dataset_checks.json, candidate_gates.csv. All numbers derive from the attached run artifacts; no DCF used.',
 'Reproduce from repository root: PYTHONPATH=src python outputs/NKT.CO_2026-10-30/relative/build.py; LibreOffice headless recalculate both workbooks in a separate directory, compare with formula_checks.json. finalize_stage3.py is a one-time checkpoint helper, not safe to rerun on finished state. qa_and_report.py intentionally refuses a second full QA run. Cached parsed data and source locators committed; market cache never rebuilt except the approved Denmark sovereign top-up.',
 'Academic analysis only. Not investment advice; source limitations and model assumptions can materially change results.'
]
(O/'relative_summary.md').write_text('\n\n'.join(lines)+'\n');(P/'report_figures.json').write_text(json.dumps(figures,indent=2)+'\n')
styles=getSampleStyleSheet();styles['BodyText'].fontSize=9;styles['BodyText'].leading=12;story=[]
for i,line in enumerate(lines):
 style=styles['Title'] if i==0 else styles['Heading2'] if line[:2] in ['1.','2.','3.','4.','5.'] else styles['BodyText']
 story.append(Paragraph(html.escape(line.lstrip('# ')),style));story.append(Spacer(1,6))
pdf=O/'relative_report_NKT.CO.pdf';SimpleDocTemplate(str(pdf),pagesize=(595,842),rightMargin=42,leftMargin=42,topMargin=38,bottomMargin=38).build(story)
state=json.loads((O/'run_state.json').read_text());now=datetime.datetime.now(datetime.timezone.utc).isoformat(timespec='seconds');elapsed=round((datetime.datetime.fromisoformat(now)-datetime.datetime.fromisoformat(state['stages']['stage3_relative']['finished'])).total_seconds()/60,2)
state['qa_C']={'status':'failed_provisional','executions':1,'counts':dict(counts),'human_spot_check':'pending','evidence_failures_waived':False,'finished':now}
state['short_report']={'status':'done_provisional','pdf':str(pdf.relative_to(ROOT)),'plaintext':str((O/'relative_summary.md').relative_to(ROOT)),'same_figures':True,'elapsed_min':elapsed,'finished':now}
state['stages']['stage3_relative']['next_step']='Do not issue qualified comparable conclusion until QA source failures are resolved; human Spot_check pending.'
(O/'run_state.json').write_text(json.dumps(state,indent=2)+'\n')
with (ROOT/'memory/run_log.csv').open('a',newline='') as f:csv.writer(f,lineterminator='\n').writerow(['NKT.CO_2026-10-30','NKT A/S','standard','qa_C_short_report','done_provisional',elapsed,now])
print('QA',dict(counts),'PDF',pdf.stat().st_size,'bytes',figures)
