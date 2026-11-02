"""Single QA-C assessment and short, explicitly provisional report — VWS.CO."""
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
# fail-index map for the current checklist (1-based over items)
source_fail={4:'Some transformations lack complete issuer/source certification; numeric lineage alone is insufficient.',5:'Exact matching industry medians unavailable; published aggregate ratios are labelled, not called medians.',8:'10 numeric peers are not certified as ten qualified peers; comparable conclusion blocked.',9:'Complete ownership/event/history verification for all 26 candidates not completed; no waiver.',11:'Candidate/expansion/scoring audit exists, but full business/event source review incomplete.',15:'Only qualified pre-associate EV cross-checks available; claim/lease/associate fair-value consistency unresolved.',19:'Human Spot_check is pending; 20-row reproducible check not performed.',37:'Both policies computed; approved decimal chosen; plausibility uses labelled published industry ratio, not a verified median.'}
own_na={20,21,23,24,25,27,28,29,30,31,32,33}
checks=[]
for i,item in enumerate(items,1):
 status='FAIL' if i in source_fail else 'N/A' if i in own_na else 'PASS'
 detail=source_fail.get(i,'Published route: no own-estimation sample, A/B/C, LINEST, OLS, typicality or residual bands.' if i in own_na else 'Reviewed against generated artifacts, source log, formula_checks.json and evidence_review.md.')
 checks.append(dict(item=i,status=status,requirement=item,detail=detail))
integrity=[]
for family in ['regressions_multi','evebitda_industry','pbv_industry']:
 ds=datasets.equation_for('Denmark','PBV','2026-10-30')[1].dataset if family=='regressions_multi' else datasets.resolve(family,country='Denmark',valuation_date='2026-10-30').dataset
 findings=datasets.check_dataset(ds);integrity.append(dict(family=family,dataset=ds.dataset_id,findings=[dict(severity=f.severity,code=f.code,message=f.message) for f in findings]));assert not any(f.severity=='error' for f in findings)
(P/'dataset_checks.json').write_text(json.dumps(integrity,indent=2)+'\n')
counts=Counter(x['status'] for x in checks)
(P/'qa_results.md').write_text('# QA block C — one execution, 2026-11-02\n\n**NOT PASSED / PROVISIONAL.** '+str(dict(counts))+'\nSource/qualification failures below are unresolved, not waived. Numerical/library/workbook checks pass; human Spot_check pending separately. No own-estimation tests, no duplicate full QA. No failure silently converted to a pass.\n\n'+ '\n\n'.join(f"### C{x['item']} — {x['status']}\n{x['requirement']}\n\n{x['detail']}" for x in checks)+'\n\n## Failure disposition\nComputed prices are diagnostic only. Fewer than 8 independently source-qualified peers have been certified, so the comparable conclusion is blocked, not an approved relaxed valuation. Human review plus completion of source/normalization/claim gates required before use. Industry median unavailable from registered dataset: report limitation instead of fabricating statistic. No failing code arithmetic found; source gaps remain explicitly unresolved.\n')
s=pd.read_csv(P/'comparables.csv');m=pd.read_csv(P/'multiples_summary.csv').set_index('multiple');r=json.loads((P/'regression_results.json').read_text())
price=189.25;shares=978.25
ev=m.loc['ev_ebit'];pe=m.loc['pe'];evs=m.loc['ev_sales'];pbv=m.loc['pbv']
chosen=max(r['predictions'],key=lambda p:p['published_r2'])
figures=dict(ticker='VWS.CO',valuation_date='2026-10-30',current_price_dkk=price,shares_m=shares,peer_count=len(s),tier12=int((s.tier<=2).sum()),tier3=int((s.tier==3).sum()),europe=int(s.europe.sum()),ev_ebit_n=int(ev.n_valid),ev_ebit_median=float(ev['median']),ev_ebit_mid_dkk=float(ev.value_per_share_mid),ev_ebit_iqr=[float(ev.value_per_share_low),float(ev.value_per_share_high)],ev_ebit_upside=float(ev.value_per_share_mid)/price-1,pe_mid_dkk=float(pe.value_per_share_mid),ev_sales_mid_dkk=float(evs.value_per_share_mid),regression_model=chosen['model'],regression_r2=chosen['published_r2'],regression_value_dkk=chosen['value_per_share'],qa=dict(counts))
lines=[
 '# Vestas Wind Systems A/S (VWS.CO) — short relative-only report',
 'Valuation date 2026-10-30 | information cutoff 2026-10-30 | accessed 2026-11-02 | DKK/share unless stated.',
 'STATUS: PROVISIONAL / QA-C NOT PASSED. Source-qualified comparable conclusion BLOCKED. Figures below are reproducible diagnostics, not an unqualified valuation or investment recommendation.',
 'Scope: VWS.CO only; standard / published_damodaran / web_minimum. Denmark/DKK dated cache reused (DKK 7.4735/EUR); no Stage 0 rebuild or top-up needed. Full Stage 1, DCF and Stage 4 skipped by approved relative_only deviation. Mandatory short PDF supplied per explicit user instruction.',
 '1. Financial basis and definitions',
 'FY2025 ended 2025-12-31 (calendar year); EURm. Revenue 18822; vendor EBIT 1067 (= issuer EBIT before special items; issuer reported 1015, special items -52 = 4.9% of EBIT, below the 10% normalized-alternative trigger); vendor EBITDA 1501 (issuer 2053, -26.9% definitional gap — favours EV/EBIT primary); NI 778 (issuer 780, minority -2); CFO 2286; PP&E capex 821 (total investments 1251 incl. intangibles 457); common equity 3867 (prior 3529); assets 25732; lease-inclusive debt 3374; cash 4384 + ST investments 164; NCI 14; LT investments 739 (recorded, not deducted — equity-investment earnings remain in denominators).',
 'EV base: mcap 24772 (DKK 185.13bn / 7.4735) + debt 3374 + NCI 14 - cash 4384 = 23776 EURm. Pre-associate bridge; peer associates/claim/lease definitions unresolved (qualified status).',
 f'Current quote DKK {price:.2f} (Nasdaq Copenhagen, 2026-10-30 close); shares {shares:.2f}m current (weighted basic 999m). Declared FY2025 DPS DKK 0.74 (~EUR 0.10) -> declared payout 0.128 for regression input; consensus 3Y g_eps 32.41%, g_rev 8.34%; beta 0.94; closing-equity ROE 20.12%.',
 '2. Peer diagnostics — not source-qualified fair value',
 f'27 initial candidates incl. target; final numeric 10 peers on the FIRST Europe step (no relaxation): {figures["tier12"]} Tier1/2, {figures["tier3"]} Tier3, {figures["europe"]} Europe-listed. Ordered expansions Europe -> World -> 0.05-20x size -> Tier3 cap 4 were defined but not needed. Peers: '+', '.join(s.ticker)+'.',
 'Europe membership evidence = dated IEUR MSCI Europe IMI holdings proxy (Oct 29 2026); URTH World standard proxy required only for non-European World expansion (ETN confirmed member, not needed; GEV event-excluded). This diverges deliberately from the ENR.DE run, which excluded IMI-only names — recorded in evidence_review.md. Hard exclusions: SIE (Altair), PRY (Encore Wire), ABBN (Robotics/Gamesa), GEV (spin), SMIN (disposals), NEX (Lynxeo), SKF.B (separation), ATCO.A and EPI.A (class-cap reconciliation >2%).',
 'Eight score weights: growth30%, beta15%, leverage10%, ROE10%, EBITDAmargin10%, payout7.5%, capex/sales7.5%, log EURcap10%. Pool-only 5/95 clipping/sampleSD; positive extremes retained. Full pool/selection/parameter/source schedules retained.',
 f'Equipment-primary EV/EBIT is the declared primary, qualified (pre-associate EV only): raw median {ev["median"]:.6f}x on {int(ev.n_valid)} valid observations; implied DKK {ev.value_per_share_mid:.6f}; peer-IQR dispersion {ev.value_per_share_low:.6f}-{ev.value_per_share_high:.6f}; vs quote {(ev.value_per_share_mid/price-1)*100:.4f}%. IQR is NOT a confidence interval.',
 f'Cross-checks: PE raw median {pe["median"]:.6f}x / PEG-scaled {pe.adjusted_median:.6f}x -> DKK {pe.value_per_share_mid:.6f} ({(pe.value_per_share_mid/price-1)*100:.2f}%); EV/Sales -> DKK {evs.value_per_share_mid:.6f} ({(evs.value_per_share_mid/price-1)*100:.2f}%); PBV median {pbv["median"]:.6f}x -> DKK {pbv.value_per_share_mid:.6f} ({(pbv.value_per_share_mid/price-1)*100:.2f}%). EV multiples n=8 (IMI, NKT invalid denominators). relativePE and TobinQ unavailable, not invented.',
 '3. Published-regression diagnostics',
 'Denmark resolves EUROPE exact; January 2026 equations as of 2026-01-01 (~304 days old). No market estimation, sector-specific fit, SEy, p-values, adjustedR2, A/B/C, D1-D10 or residual classification. Classification: Not classified (no SEy published). Model choice by highest published R2 is a weak heuristic only.',
]
for p in r['predictions']:
 lines.append(f'{p["model"]}: prediction {p["predicted"]:.9f}x; published R2 {p["published_r2"]:.3f}; implied DKK {p["value_per_share"]:.6f} ({(p["value_per_share"]/price-1)*100:.2f}%). Equation: {p["equation"]}.')
lines +=[
 f'Chosen published {chosen["model"]} (highest R2 {chosen["published_r2"]:.3f}) implied DKK {chosen["value_per_share"]:.6f}; vs quote {(chosen["value_per_share"]/price-1)*100:.4f}%. EUROPE PBV/PE carry no DFR/tax terms (unit policies identical); EV/EBITDA percent-point alternative preserved in regression_results.json — decimal policy approved.',
 'Registered dataset regressions_multi_2026-01 SHA a894ea86f209d59c68c57ba5674ee096ee875cf9726af2cfe84ec212af1d9bf5. GLOBAL/EM anomaly warnings not used (EUROPE exact). All exact coefficients/t-stats and input IDs in live workbook; post-LibreOffice recalculation all predictions/prices/scores agree with the library within 1e-9. Published EV definition undocumented; no associate removal imposed on the regression EV bridge.',
 '4. Benchmark, sensitivity and limits',
 'Closest published EUROPE industry ratios (Machinery 210 firms, Green & Renewable Energy 60, Electrical Equipment 146; see industry_benchmarks.json). These are NOT verified medians; aggregate-versus-median comparison remains a QA failure. Peer EV/EBIT median 18.96 sits inside the published range, not grounds to overwrite data.',
 'Sensitivities: raw/scaled and peer quartiles, leave-one-out PE/growth set, all-observation EBIT margins 4/6/8/10%, target-only issuer-reported-EBIT-1015 diagnostic (special items 4.9% EBIT, below trigger — diagnostic only, not uniform normalization), both unit policies. No substantiated uniform normalization constructed.',
 'Unresolved QA: full two-way ownership/event/history qualification for all candidates, authentic matching industry medians, comparable EV claim/lease/associate consistency, substantiated uniform normalization. Three seeded arithmetic EV checks PASS; human Spot_check PENDING (not performed/waived). Ten numeric names do not satisfy ten qualified peers until these gates are cleared. No final fair-value recommendation is issued.',
 '5. Source and reproducibility pointers',
 'Uniform raw financial/statistics/history: stockanalysis.com (per-ticker URLs in relative/source_log.csv); issuer figures cross-checked against the Vestas FY2025 annual report (links in relative_inputs.md / evidence_review.md). Standard proxies dated 2026-10-29: iShares MSCI World (URTH) and MSCI Europe IMI (IEUR) holdings CSVs. Library IDs/SHA/vintage/mappings: relative/evidence_review.md, regression_results.json, dataset_checks.json, candidate_gates.csv. All numbers derive from the attached run artifacts; no DCF used.',
 'Reproduce from repository root: PYTHONPATH=src python3 outputs/VWS.CO_2026-10-30/relative/build.py; LibreOffice headless recalculate both workbooks in a separate directory, compare with formula_checks.json. finalize_stage3.py is a one-time checkpoint helper, not safe to rerun on finished state. qa_and_report.py intentionally refuses a second full QA run. Cached parsed data and source locators committed; market cache never rebuilt.',
 'Academic analysis only. Not investment advice; source limitations and model assumptions can materially change results.'
]
(O/'relative_summary.md').write_text('\n\n'.join(lines)+'\n');(P/'report_figures.json').write_text(json.dumps(figures,indent=2)+'\n')
styles=getSampleStyleSheet();styles['BodyText'].fontSize=9;styles['BodyText'].leading=12;story=[]
for i,line in enumerate(lines):
 style=styles['Title'] if i==0 else styles['Heading2'] if line[:2] in ['1.','2.','3.','4.','5.'] else styles['BodyText']
 story.append(Paragraph(html.escape(line.lstrip('# ')),style));story.append(Spacer(1,6))
pdf=O/'relative_report_VWS.CO.pdf';SimpleDocTemplate(str(pdf),pagesize=(595,842),rightMargin=42,leftMargin=42,topMargin=38,bottomMargin=38).build(story)
state=json.loads((O/'run_state.json').read_text());now=datetime.datetime.now(datetime.timezone.utc).isoformat(timespec='seconds');elapsed=round((datetime.datetime.fromisoformat(now)-datetime.datetime.fromisoformat(state['stages']['stage3_relative']['finished'])).total_seconds()/60,2)
state['qa_C']={'status':'failed_provisional','executions':1,'counts':dict(counts),'human_spot_check':'pending','evidence_failures_waived':False,'finished':now}
state['short_report']={'status':'done_provisional','pdf':str(pdf.relative_to(ROOT)),'plaintext':str((O/'relative_summary.md').relative_to(ROOT)),'same_figures':True,'elapsed_min':elapsed,'finished':now}
state['stages']['stage3_relative']['next_step']='Do not issue qualified comparable conclusion until QA source failures are resolved; human Spot_check pending.'
(O/'run_state.json').write_text(json.dumps(state,indent=2)+'\n')
with (ROOT/'memory/run_log.csv').open('a',newline='') as f:csv.writer(f,lineterminator='\n').writerow(['VWS.CO_2026-10-30','Vestas Wind Systems A/S','standard','qa_C_short_report','done_provisional',elapsed,now])
print('QA',dict(counts),'PDF',pdf.stat().st_size,'bytes')
print(json.dumps(figures,indent=1))
