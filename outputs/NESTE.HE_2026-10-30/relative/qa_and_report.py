"""Single QA-C assessment and short, explicitly provisional report for NESTE.HE."""
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
source_fail={4:'Some transformations lack complete issuer/source certification; numeric lineage alone is insufficient.',5:'Exact matching industry medians unavailable; published aggregate ratios are labelled, not called medians.',8:'10 numeric peers are not certified as ten qualified peers; comparable conclusion blocked.',9:'Complete ownership/event/history verification for all candidates not completed; no waiver.',11:'Candidate/expansion/scoring audit exists, but full business/event source review incomplete.',17:'Primary EV/EBITDA basis qualified only; peer claim/lease/associate EV perimeter unresolved.',18:'Only qualified pre-LT-investment EV cross-checks available; claim/lease/associate fair-value consistency unresolved.',20:'Peer/IQR/LOO/EBITDA sensitivities exist, but no substantiated uniform material-one-off normalization.'}
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
 ds=datasets.equation_for('Finland','PBV','2026-10-30')[1].dataset if family=='regressions_multi' else datasets.resolve(family,country='Finland',valuation_date='2026-10-30').dataset
 findings=datasets.check_dataset(ds);integrity.append(dict(family=family,dataset=ds.dataset_id,findings=[dict(severity=f.severity,code=f.code,message=f.message) for f in findings]));assert not any(f.severity=='error' for f in findings)
(P/'dataset_checks.json').write_text(json.dumps(integrity,indent=2)+'\n')
counts=Counter(x['status'] for x in checks)
(P/'qa_results.md').write_text('# QA block C — one execution, 2026-11-01\n\n**NOT PASSED / PROVISIONAL.** '+str(dict(counts))+'\nSource/qualification failures below are unresolved, not waived. Numerical/library/workbook checks pass; human Spot_check pending separately. No own-estimation tests, no duplicate full QA. No failure silently converted to a pass.\n\n'+ '\n\n'.join(f"### C{x['item']} — {x['status']}\n{x['requirement']}\n\n{x['detail']}" for x in checks)+'\n\n## Failure disposition\nComputed prices are diagnostic only. Fewer than8 independently source-qualified peers have been certified, so the comparable conclusion is blocked, not an approved relaxed valuation. Human review plus completion of source/normalization/claim gates required before use. Industry median unavailable from registered dataset: report limitation instead of fabricating statistic. No failing code arithmetic found; source gaps remain explicitly unresolved.\n')
s=pd.read_csv(P/'comparables.csv');m=pd.read_csv(P/'multiples_summary.csv');r=json.loads((P/'regression_results.json').read_text());ev=m[m.multiple.eq('ev_ebitda')].iloc[0]
price=28.34;shares=768.28
pbv=[p for p in r['predictions'] if p['model']=='PBV'][0]
figures=dict(ticker='NESTE.HE',valuation_date='2026-10-30',current_price=price,quote_currency='EUR',shares_m=shares,peer_count=len(s),tier12=int((s.tier<=2).sum()),tier3=int((s.tier==3).sum()),europe=int(s.europe.sum()),raw_evebitda_median=float(ev['median']),scaled_evebitda_median=float(ev.adjusted_median),peer_indicative=float(ev.value_per_share_mid),peer_iqr_low=float(ev.value_per_share_low),peer_iqr_high=float(ev.value_per_share_high),peer_upside=float(ev.value_per_share_mid)/price-1,regression_pbv=float(pbv['value_per_share']),qa=dict(counts))
lines=[
 '# Neste Oyj (NESTE.HE) — short relative-only report',
 'Valuation date2026-10-30 | price date2026-10-30 | accessed2026-11-01 | EUR/share unless stated.',
 'STATUS: PROVISIONAL / QA-C NOT PASSED. Source-qualified comparable conclusion BLOCKED. Figures below are reproducible diagnostics, not an unqualified valuation or investment recommendation.',
 'Scope: NESTE.HE only; standard / published_damodaran / web_minimum. 2026-10-30 dated cache reused; stage0 Finland sovereign top-up only. Full Stage1, DCF and Stage4 skipped by approved relative_only deviation. Mandatory short PDF supplied per explicit user override of no-PDF default.',
 '1. Financial basis and definitions',
 'FY2025 calendar year (not TTM/forward); EURm. Sales19016; EBIT466 (issuer503, 7.9% vendor gap); EBITDA1124 vendor-uniform basis (issuer reported1438 / comparable1683, sensitivities shown); CFO1747; capex910; common equity7314; assets15749; debt incl leases5183; cash&ST1367; NCI0; LT investments90 excluded from EV bridge; dividends paid154.',
 'Issuer cross-check via Neste FY2025 financial statements release: NI144, EPS0.19, DPS0.20; effective tax27.64% (tax55/pretax199). ROE1.96% is a cyclical trough and payout1.069 capped at1.0 collapses fundamental growth to ~0; this substituted_input (approved for the published route) is NOT analyst consensus.',
 'Current quote28.34 EUR; shares768.28m; market cap EUR21772m. EV EUR25586m = 21772+5183+0-1367 (debt+NCI-cash&ST); LT investments not in bridge. Vendor beta0.56 kept (within 0-2.5 band); no relevering needed.',
 '2. Peer diagnostics — not source-qualified fair value',
 f'40 candidate rows collected, 38-name scored initial pool, Europe-first; Europe step infeasible (7 T12_EU under Tier3 cap2) -> World expansion (ordered step b) used, default Tier3 cap2 kept; final numeric10 peers, {figures["tier12"]} Tier1/2, {figures["tier3"]} Tier3, {figures["europe"]} Europe-listed. Standard proxies: IEUR MSCI Europe IMI for European names, URTH MSCI World (holdings2026-10-29) entity/name match for US/Canada. Ordered expansion World used; size band and Tier3 cap unchanged. No other hard filter waived. Peers: '+', '.join(s.ticker)+'.',
 'Eight score weights: growth30%, beta15%, net debt/EBITDA10%, ROE10%, EBITDAmargin10%, payout7.5%, capex/sales7.5%, log EURcap10%. Pool-only5/95 clipping/sampleSD; positive extremes retained. Vendor 5Y betas across the pool are implausibly low/negative (uniform source, disclosed); distance driven mainly by size/leverage/margins.',
 f'Bucket F primary EV/EBITDA, unscaled per procedure rule 118 (no prescribed EV driver; EV/Sales-by-margin equivalent is not independent evidence). Peer EV/EBITDA median{ev["median"]:.6f}x; target growth0.00% vs peer median growth0.71% (same fundamental basis). Indicative value{ev.value_per_share_mid:.6f}EUR; peer-IQR dispersion{ev.value_per_share_low:.6f}–{ev.value_per_share_high:.6f}; vs quote{(ev.value_per_share_mid/price-1)*100:.4f}%. IQR is NOT a confidence interval; peer EV basis is pre-LT-investment and qualified only.',
 f'Raw equals chosen basis (unscaled): {ev.raw_value_mid:.6f}EUR. Cross-checks EV/CF then PE in multiples_summary.csv; TobinQ and matching-index relativePE unavailable, not invented. BP FY2025 NI collapse (PE2362) retained as positive extreme.',
 '3. Published-regression diagnostics',
 'Finland resolves EUROPE exact; January2026 equations asof2026-01-01 (302days old). No market estimation, sector-specific fit, SEy, p-values, adjustedR2, A/B/C, D1–D10 or residual classification. Classification: Not classified (no SEy published). Model choice by highest publishedR2 is a weak heuristic only.',
 ]
for p in r['predictions']:
 equation={'PE':'9.72 +2.99 beta +49.82 g_eps +7.98 payout','PBV':'.73 +3.92 g_eps +.13 beta +10.75 ROE -.25 payout','EV/EBITDA':'18.15 +35.25 g_rev -.11 DFR -.12 tax +2.29 ROIC'}[p['model']]
 lines.append(f'{p["model"]}: prediction{p["predicted"]:.9f}x; publishedR2{p["published_r2"]:.3f}; implied{p["value_per_share"]:.6f}EUR. Equation: {equation}.')
alt=[p for p in r['predictions'] if p['model']=='EV/EBITDA'][0]['unit_alternative']['dfr_tax_percent_points']
lines +=[
 f'Chosen published PBV implied{figures["regression_pbv"]:.6f}EUR; vs quote{(figures["regression_pbv"]/price-1)*100:.4f}%. Highest publishedR20.423, not sector fit or proof of mispricing. Decimal DFR/tax policy explicitly approved; EV/EBITDA alternative percent-point prediction{alt:.9f}x. Both scenarios preserved; source-unit ambiguity not resolved by approval.',
 'Registered dataset regressions_multi_2026-01 SHA a894ea86f209d59c68c57ba5674ee096ee875cf9726af2cfe84ec212af1d9bf5. GLOBAL PEG sign/tstat, GLOBAL PBV beta sign and EM ROIC sign warnings not used. All exact coefficients/tstats and input IDs in live workbook; post-LibreOffice recalculation all predictions/prices/scores agree with library within1e-9. Published EV definition undocumented.',
 '4. Benchmark, sensitivity and limits',
 'Closest Oil/Gas (Integrated) EUROPE published ratios: EVEBITDA5.94x (12 firms, pos-EBITDA basis), PBV2.14. E&P alternative2.66x (83 firms). These are NOT verified industry medians; aggregate-versus-median comparison remains a QA failure. Target EVEBITDA22.76x exceeds both published ratios; peer-median8.39x far below the target multiple drives the large negative indicative gap (implied below quote); not proof of mispricing.',
 'Sensitivities: raw/scaled and peer quartiles, leave-one-out peer set, issuer EBITDA-basis diagnostic (vendor1124 vs reported1438 / comparable1683) and target EBITDA -10% cyclicality diagnostic (not normalized); details in sensitivities.csv. No substantiated uniform normalization constructed.',
 'Unresolved QA: full two-way ownership/event/history qualification for all candidates, authentic matching industry medians, uniform material-one-off normalization and comparable EV claim/lease/LT-investment consistency. Three seeded arithmetic EV checks PASS, human Spot_check PENDING (not performed/waived). Ten numeric names do not satisfy ten qualified peers until these gates are cleared. No final fair-value recommendation is issued.',
 '5. Source and reproducibility pointers',
 'Uniform raw financial/statistics/history: https://stockanalysis.com/quote/hel/NESTE/financials/ and peer-specific URLs in relative/source_log.csv. Issuer: Neste FY2025 financial statements release (linked in relative_inputs.md). Standard proxy dated2026-10-29: https://www.ishares.com/us/products/239696/ishares-msci-world-etf/latest-holdings.csv . Library IDs/SHA/vintage/mappings and all qualification evidence: relative/evidence_review.md, regression_results.json, dataset_checks.json, candidate_gates.csv. All numbers derive from the attached run artifacts; no DCF used.',
 'Reproduce from repository root: PYTHONPATH=src python outputs/NESTE.HE_2026-10-30/relative/build.py; LibreOffice headless recalculate both workbooks in a separate directory, compare with formula_checks.json. finalize_stage3.py is a one-time checkpoint helper, not safe to rerun on finished state. qa_and_report.py intentionally refuses a second full QA run. Cached parsed data and source locators committed; market cache never rebuilt except the approved Finland sovereign top-up.',
 'Academic analysis only. Not investment advice; source limitations and model assumptions can materially change results.'
 ]
(O/'relative_summary.md').write_text('\n\n'.join(lines)+'\n');(P/'report_figures.json').write_text(json.dumps(figures,indent=2)+'\n')
styles=getSampleStyleSheet();styles['BodyText'].fontSize=9;styles['BodyText'].leading=12;story=[]
for i,line in enumerate(lines):
 style=styles['Title'] if i==0 else styles['Heading2'] if line[:2] in ['1.','2.','3.','4.','5.'] else styles['BodyText']
 story.append(Paragraph(html.escape(line.lstrip('# ')),style));story.append(Spacer(1,6))
pdf=O/'relative_report_NESTE.HE.pdf';SimpleDocTemplate(str(pdf),pagesize=(595,842),rightMargin=42,leftMargin=42,topMargin=38,bottomMargin=38).build(story)
state=json.loads((O/'run_state.json').read_text());now=datetime.datetime.now(datetime.timezone.utc).isoformat(timespec='seconds');elapsed=round((datetime.datetime.fromisoformat(now)-datetime.datetime.fromisoformat(state['stages']['stage3_relative']['finished'])).total_seconds()/60,2)
state['qa_C']={'status':'failed_provisional','executions':1,'counts':dict(counts),'human_spot_check':'pending','evidence_failures_waived':False,'finished':now}
state['short_report']={'status':'done_provisional','pdf':str(pdf.relative_to(ROOT)),'plaintext':str((O/'relative_summary.md').relative_to(ROOT)),'same_figures':True,'elapsed_min':elapsed,'finished':now}
state['stages']['stage3_relative']['next_step']='Do not issue qualified comparable conclusion until QA source failures are resolved; human Spot_check pending.'
(O/'run_state.json').write_text(json.dumps(state,indent=2)+'\n')
with (ROOT/'memory/run_log.csv').open('a',newline='') as f:csv.writer(f,lineterminator='\n').writerow(['NESTE.HE_2026-10-30','Neste Oyj','standard','qa_C_short_report','done_provisional',elapsed,now])
print('QA',dict(counts),'PDF',pdf.stat().st_size,'bytes',figures)
