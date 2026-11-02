"""Single QA-C assessment and short, explicitly provisional report for SHEL.L."""
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
source_fail={4:'Some transformations lack complete issuer/source certification; numeric lineage alone is insufficient.',5:'Exact matching industry medians unavailable; published aggregate ratios are labelled, not called medians.',8:'10 numeric peers are not certified as ten qualified peers; comparable conclusion blocked.',9:'Complete ownership/event/history verification for all candidates not completed; no waiver.',11:'Candidate/expansion/scoring audit exists, but full business/event source review incomplete.',17:'Primary EV/EBITDA basis qualified only; peer claim/lease/associate EV perimeter unresolved.',18:'Only qualified excl-LT-investment EV cross-checks available; claim/lease/associate fair-value consistency unresolved.',20:'Peer/IQR/LOO/EBITDA sensitivities exist, but no substantiated uniform material-one-off normalization.'}
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
 ds=datasets.equation_for('United Kingdom','PBV','2026-10-30')[1].dataset if family=='regressions_multi' else datasets.resolve(family,country='United Kingdom',valuation_date='2026-10-30').dataset
 findings=datasets.check_dataset(ds);integrity.append(dict(family=family,dataset=ds.dataset_id,findings=[dict(severity=f.severity,code=f.code,message=f.message) for f in findings]));assert not any(f.severity=='error' for f in findings)
(P/'dataset_checks.json').write_text(json.dumps(integrity,indent=2)+'\n')
counts=Counter(x['status'] for x in checks)
(P/'qa_results.md').write_text('# QA block C — one execution, 2026-11-02\n\n**NOT PASSED / PROVISIONAL.** '+str(dict(counts))+'\nSource/qualification failures below are unresolved, not waived. Numerical/library/workbook checks pass; human Spot_check pending separately. No own-estimation tests, no duplicate full QA. No failure silently converted to a pass.\n\n'+ '\n\n'.join(f"### C{x['item']} — {x['status']}\n{x['requirement']}\n\n{x['detail']}" for x in checks)+'\n\n## Failure disposition\nComputed prices are diagnostic only. Fewer than 8 independently source-qualified peers have been certified, so the comparable conclusion is blocked, not an approved relaxed valuation. Human review plus completion of source/normalization/claim gates required before use. Industry median unavailable from registered dataset: report limitation instead of fabricating statistic. No failing code arithmetic found; source gaps remain explicitly unresolved.\n')
s=pd.read_csv(P/'comparables.csv');m=pd.read_csv(P/'multiples_summary.csv');r=json.loads((P/'regression_results.json').read_text());ev=m[m.multiple.eq('ev_ebitda')].iloc[0]
price=40.365;shares=5700
pbv=[p for p in r['predictions'] if p['model']=='PBV'][0]
figures=dict(ticker='SHEL.L',valuation_date='2026-10-30',current_price=price,quote_currency='GBP',shares_m=shares,peer_count=len(s),tier12=int((s.tier<=2).sum()),tier3=int((s.tier==3).sum()),europe=int(s.europe.sum()),raw_evebitda_median=float(ev['median']),scaled_evebitda_median=float(ev.adjusted_median) if pd.notna(ev.adjusted_median) else None,peer_indicative=float(ev.value_per_share_mid),peer_iqr_low=float(ev.value_per_share_low),peer_iqr_high=float(ev.value_per_share_high),peer_upside=float(ev.value_per_share_mid)/price-1,regression_pbv=float(pbv['value_per_share']),qa=dict(counts))
lines=[
 '# Shell plc (SHEL.L) — short relative-only report',
 'Valuation date 2026-10-30 | price date 2026-10-30 | accessed 2026-11-02 | GBP/share unless stated.',
 'STATUS: PROVISIONAL / QA-C NOT PASSED. Source-qualified comparable conclusion BLOCKED. Figures below are reproducible diagnostics, not an unqualified valuation or investment recommendation.',
 'Scope: SHEL.L only; standard / published_damodaran / web_minimum. 2026-10-30 dated cache reused as approved (United Kingdom/USD/GBP already present); no stage-0 rebuild or top-up. Full Stage1, DCF and Stage4 skipped by approved relative_only deviation. Mandatory short PDF supplied per explicit user override of no-PDF default.',
 '1. Financial basis and definitions',
 'FY2025 calendar year (not TTM/forward); USDm. Revenue 266,886 (issuer Total revenue and other income 273,731 recorded separately); EBIT 29,834; EBITDA 47,658 = EBIT + D&A-for-EBITDA 17,824 (issuer adjusted EBITDA 56,135, APM basis); CFO 42,863 (= issuer); capex 18,947; parent common equity 174,392; assets 370,350; debt incl. leases 75,688; cash & ST investments 30,216; NCI 927; LT investments 29,332 excluded from EV bridge; dividends paid 8,472; buybacks 15,179.',
 'Issuer cross-check via Shell Q4/FY2025 results (published 2026-02-05): income attributable to shareholders 17,838 vs vendor 17,837; CFO 42,863 = vendor exactly; DPS 1.446 = vendor; basic EPS 3.03 = vendor. Effective tax 39.11% (tax 11,637 / pretax 29,756). Closing-parent-ROE x capped-retention fundamental growth 5.37% is NOT analyst consensus and is an approved substituted_input for the published route.',
 'Current quote GBP 40.365 (4,036.5 GBX); shares 5,700m; market cap GBP 230.23bn ≈ EUR 276.12bn ≈ USD 308.47bn (ECB 2026-10-30, USD 1.1172/EUR, GBP 0.8338/EUR). EV USD 354.87bn using debt + NCI − cash & ST investments; LT investments/equity-accounted investments not in bridge. Vendor 5Y beta -0.19 is negative: retained for scoring with flag, replaced in the published regression by the relevered industry beta ~0.47.',
 '2. Peer diagnostics — not source-qualified fair value',
 f'33 initial candidates; Europe step infeasible (5 eligible), World developed-market relaxation (a) applied -> pool 13; final numeric {len(s)} peers, {figures["tier12"]} Tier1/2, {figures["tier3"]} Tier3, {figures["europe"]} Europe-listed (min 5 met). Proxies: IEUR MSCI Europe IMI for European names, URTH MSCI World (holdings 2026-10-29) entity/name match for US/Canada. No other hard filter waived; Tier 3 cap and size-band relaxations not invoked. Peers: '+', '.join(s.ticker)+'.',
 'Eight score weights: growth 30%, beta 15%, net debt/EBITDA 10%, ROE 10%, EBITDA margin 10%, payout 7.5%, capex/sales 7.5%, log EUR cap 10%. Pool-only 5/95 clipping/sample SD; positive extremes retained. Vendor 5Y betas across the pool are implausibly low/negative (uniform source, disclosed); distance driven mainly by size/leverage/margins.',
 f'Bucket F primary EV/EBITDA, unscaled per procedure (no prescribed EV driver). Peer EV/EBITDA median {ev["median"]:.2f}x (p25 {ev["p25"]:.2f} / p75 {ev["p75"]:.2f}); target 7.45x; target fundamental growth 5.31% vs peer median 3.31%. Indicative value {ev.value_per_share_mid:.2f} GBP; peer-IQR dispersion {ev.value_per_share_low:.2f}–{ev.value_per_share_high:.2f}; vs quote {(ev.value_per_share_mid/price-1)*100:.1f}%. IQR is NOT a confidence interval; peer EV basis is pre-LT-investment and qualified only.',
 'Cross-checks EV/CF then PE in multiples_summary.csv (EV/CF median 9.10x, PE median 24.82x; BP FY2025 NI collapse PE 2362 retained as positive extreme). Tobin Q and matching-index relative PE unavailable, not invented.',
 '3. Published-regression diagnostics',
 'United Kingdom resolves EUROPE exact; January 2026 equations as-of 2026-01-01 (~305 days old). No market estimation, sector-specific fit, SEy, p-values, adjusted R2, A/B/C, D1–D10 or residual classification. Classification: Not classified (no SEy published). Model choice by highest published R2 is a weak heuristic only.',
]
for p in r['predictions']:
 equation={'PE':'9.72 + 2.99 beta + 49.82 g_eps + 7.98 payout','PBV':'0.73 + 3.92 g_eps + 0.13 beta + 10.75 ROE - 0.25 payout','EV/EBITDA':'18.15 + 35.25 g_rev - 0.11 DFR - 0.12 tax + 2.29 ROIC'}[p['model']]
 lines.append(f'{p["model"]}: prediction {p["predicted"]:.2f}x; published R2 {p["published_r2"]:.3f}; implied {p["value_per_share"]:.2f} GBP; actual {p["actual"]:.2f}, gap {p["actual_predicted_gap"]*100:.0f}%. Equation: {equation}.')
alt=[p for p in r['predictions'] if p['model']=='EV/EBITDA'][0]['unit_alternative']['dfr_tax_percent_points']
lines +=[
 f'Chosen published PBV implied {figures["regression_pbv"]:.2f} GBP; vs quote {(figures["regression_pbv"]/price-1)*100:.1f}%. Highest published R2 0.423, not sector fit or proof of mispricing. Decimal DFR/tax policy explicitly approved; EV/EBITDA alternative percent-point prediction {alt:.2f}x. Both scenarios preserved; source-unit ambiguity not resolved by approval. EV/EBITDA equation predicted 20.2x vs actual 7.4x (−63%): market-wide equation cannot see oil-major pricing; headline limitation, not a mispricing signal.',
 'Registered dataset regressions_multi_2026-01 SHA a894ea86f209d59c68c57ba5674ee096ee875cf9726af2cfe84ec212af1d9bf5. GLOBAL PEG sign/tstat, GLOBAL PBV beta sign and EM ROIC sign warnings not used (EUROPE equations only). All exact coefficients/t-stats and input IDs in live workbook; Python formula re-evaluation (LibreOffice absent on this box) agrees with library predictions within 1e-9, disclosed. Published EV definition undocumented.',
 '4. Benchmark, sensitivity and limits',
 'Closest Oil/Gas (Integrated) EUROPE published ratios in industry_benchmarks.json are NOT verified medians; aggregate-versus-median comparison remains a QA failure. Peer EV/EBITDA median 8.43x vs published integrated ratio recorded, not "fixed" to match. Target EV/EBITDA 7.45x below peer p25.',
 'Sensitivities: raw/scaled and peer quartiles, leave-one-out peer set, target EBITDA −10% cyclicality diagnostic (not normalized), LT-investments/equity-affiliate exclusion note; details in sensitivities.csv. No substantiated uniform normalization constructed.',
 'Unresolved QA: full two-way ownership/event/history qualification for all candidates, authentic matching industry medians, uniform material-one-off normalization and comparable EV claim/lease/LT-investment consistency (SHEL earnings from equity investments 1,618 in pretax vs LT investments 29,332 outside EV). Three seeded arithmetic EV checks PASS, human Spot_check PENDING (not performed/waived). Ten numeric names do not satisfy ten qualified peers until these gates are cleared. No final fair-value recommendation is issued.',
 '5. Source and reproducibility pointers',
 'Uniform raw financial/statistics/history: https://stockanalysis.com/quote/lon/SHEL/financials/ and peer-specific URLs in relative/source_log.csv. Issuer: Shell plc Q4/FY2025 unaudited results (linked in relative_inputs.md). Standard proxy dated 2026-10-29: https://www.ishares.com/us/products/239696/ishares-msci-world-etf/latest-holdings.csv . Library IDs/SHA/vintage/mappings and all qualification evidence: relative/evidence_review.md, regression_results.json, dataset_checks.json, candidate_gates.csv. All numbers derive from the attached run artifacts; no DCF used.',
 'Reproduce from repository root: PYTHONPATH=src python outputs/SHEL.L_2026-10-30/relative/build.py; formula re-evaluation in Python (LibreOffice absent — disclosed), compare with formula_checks.json. finalize_stage3.py is a one-time checkpoint helper, not safe to rerun on finished state. qa_and_report.py intentionally refuses a second full QA run. Cached parsed data and source locators committed; market cache never rebuilt (no top-up needed: United Kingdom/USD/GBP already dated).',
 'Academic analysis only. Not investment advice; source limitations and model assumptions can materially change results.'
]
(O/'relative_summary.md').write_text('\n\n'.join(lines)+'\n');(P/'report_figures.json').write_text(json.dumps(figures,indent=2)+'\n')
styles=getSampleStyleSheet();styles['BodyText'].fontSize=9;styles['BodyText'].leading=12;story=[]
for i,line in enumerate(lines):
 style=styles['Title'] if i==0 else styles['Heading2'] if line[:2] in ['1.','2.','3.','4.','5.'] else styles['BodyText']
 story.append(Paragraph(html.escape(line.lstrip('# ')),style));story.append(Spacer(1,6))
pdf=O/'relative_report_SHEL.L.pdf';SimpleDocTemplate(str(pdf),pagesize=(595,842),rightMargin=42,leftMargin=42,topMargin=38,bottomMargin=38).build(story)
state=json.loads((O/'run_state.json').read_text());now=datetime.datetime.now(datetime.timezone.utc).isoformat(timespec='seconds');elapsed=round((datetime.datetime.fromisoformat(now)-datetime.datetime.fromisoformat(state['stages']['stage3_relative']['finished'])).total_seconds()/60,2)
state['qa_C']={'status':'failed_provisional','executions':1,'counts':dict(counts),'human_spot_check':'pending','evidence_failures_waived':False,'finished':now}
state['short_report']={'status':'done_provisional','pdf':str(pdf.relative_to(ROOT)),'plaintext':str((O/'relative_summary.md').relative_to(ROOT)),'same_figures':True,'elapsed_min':elapsed,'finished':now}
state['stages']['stage3_relative']['next_step']='Do not issue qualified comparable conclusion until QA source failures are resolved; human Spot_check pending.'
(O/'run_state.json').write_text(json.dumps(state,indent=2)+'\n')
with (ROOT/'memory/run_log.csv').open('a',newline='') as f:csv.writer(f,lineterminator='\n').writerow(['SHEL.L_2026-10-30','Shell plc','standard','qa_C_short_report','done_provisional',elapsed,now])
print('QA',dict(counts),'PDF',pdf.stat().st_size,'bytes',figures)
