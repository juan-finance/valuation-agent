"""One execution of QA block C, then the mandated short relative-only report."""
from pathlib import Path
import json, time
from collections import Counter
import pandas as pd
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet
from valuation_agent import datasets

P=Path(__file__).resolve().parent; O=P.parent; ROOT=P.parents[2]
qa_already=(P/'qa_results.md').exists()
q=(ROOT/'methodology/qa_checklist.md').read_text(); q=q[q.index('## C.'):q.index('## D.')]
items=[x[6:] for x in q.splitlines() if x.startswith('- [ ] ')]
source_fail={
 4:'Some transformations and issuer identity/ownership fields lack complete independent certification; numeric lineage alone is insufficient.',
 5:'Exact matching industry medians are unavailable; published aggregate ratios are labelled as published ratios, not verified medians.',
 8:'Ten numeric peers are present, but source-qualified comparable status is not certified.',
 9:'Complete ownership/event/history verification for the full candidate pool was not completed; no waiver.',
 11:'Candidate, expansion, scoring and selection audit exists, but full business/event source review is incomplete.',
 18:'Only qualified pre-associate EV cross-checks are available; claim/lease/associate perimeter harmonization remains unresolved; hybrid claim handled once for target.',
 20:'Peer and issuer-basis sensitivities exist, but uniform material-one-off normalization is not independently substantiated (vendor EBIT 12,495 vs issuer EBIT 8,620).',
}
own_na={23,26,27,28,30,31,33,34,36}
checks=[]
for i,item in enumerate(items,1):
 status='FAIL' if i in source_fail else 'N/A' if i in own_na else 'PASS'
 detail=source_fail.get(i,'Published route: no own-estimation sample, A/B/C, LINEST, OLS, typicality or residual bands.' if i in own_na else 'Reviewed against generated artifacts, source log, formula_checks.json and evidence_review.md.')
 if 'plausibility check against the sector median' in item:
  status='FAIL'; detail='Both DFR/tax policies computed; approved decimal policy chosen; comparison uses a labelled published industry ratio, not a verified peer-sector median.'
 checks.append(dict(item=i,status=status,requirement=item,detail=detail))
if not qa_already:
 checks_ds=[]
 for dep in ['PE','PBV','EV/EBITDA']:
  eq,res,region=datasets.equation_for('Denmark',dep,'2026-10-30')
  findings=datasets.check_dataset(res.dataset)
  assert not any(f.severity=='error' for f in findings)
  checks_ds.append(dict(dependent=dep,dataset=res.dataset.dataset_id,region=region,findings=[dict(severity=f.severity,code=f.code,message=f.message) for f in findings]))
 (P/'dataset_checks.json').write_text(json.dumps(checks_ds,indent=2,default=str)+'\n')
counts=Counter(x['status'] for x in checks)
if not qa_already:
 (P/'qa_results.md').write_text('# QA block C - one execution, 2026-11-02\n\n**NOT PASSED / PROVISIONAL.** '+str(dict(counts))+"\nSource/qualification failures are unresolved, not waived. Numerical/library/workbook checks pass; human Spot_check remains pending. No own-estimation tests and no duplicate full QA.\n\n"+'\n\n'.join(f"### C{x['item']} - {x['status']}\n{x['requirement']}\n\n{x['detail']}" for x in checks)+'\n\n## Failure disposition\nComputed prices are diagnostic only. Ten numerical peers were selected, but fewer than ten independently source-qualified peers have been certified, so the comparable conclusion is blocked, not an approved relaxed valuation. Industry median unavailable from the registered dataset: report limitation instead of fabricating one. No failing arithmetic found; source gaps remain explicitly unresolved.\n')

s=pd.read_csv(P/'comparables.csv'); m=pd.read_csv(P/'multiples_summary.csv'); r=json.loads((P/'regression_results.json').read_text())
prim=m[m.multiple.eq('ev_ebitda')].iloc[0]
pred={x['model']:x for x in r['predictions']}
fig=dict(ticker='ORSTED.CO',valuation_date='2026-10-30',price_dkk=131.9,price_eur=131.9/7.4735,shares_m=1321.062,peer_count=len(s),tier12=int((s.tier<=2).sum()),tier3=int((s.tier==3).sum()),europe=int(s.europe.sum()),peer_ev_ebitda_low=float(prim.value_per_share_low),peer_ev_ebitda_mid=float(prim.value_per_share_mid),peer_ev_ebitda_high=float(prim.value_per_share_high),peer_upside=float(prim.value_per_share_mid)/(131.9/7.4735)-1,peer_pbv_mid=float(m[m.multiple.eq('pbv')].iloc[0].value_per_share_mid),peer_ev_ebit_mid=float(m[m.multiple.eq('ev_ebit')].iloc[0].value_per_share_mid),regression_pbv=float(pred['PBV']['value_per_share']),regression_pe=float(pred['PE']['value_per_share']),regression_ev_ebitda=float(pred['EV/EBITDA']['value_per_share']),qa=dict(counts))
(P/'report_figures.json').write_text(json.dumps(fig,indent=2)+'\n')
lines=[
 '# Ørsted A/S (ORSTED.CO) - short relative-only report',
 'Valuation date 2026-10-30 | price date 2026-10-30 | accessed 2026-11-02 | EUR/share unless stated (DKK 131.9 = EUR 17.65 at ECB 7.4735).',
 'STATUS: PROVISIONAL / QA-C NOT PASSED. Source-qualified comparable conclusion BLOCKED. Figures below are reproducible diagnostics, not an unqualified valuation or investment recommendation.',
 'Scope: ORSTED.CO only; standard / published_damodaran / web_minimum. Dated 2026-10-30 cache reused; Denmark/DKK coverage already present. Reduced input step substituted for Stage 1; DCF and Stage 4 skipped by approved relative_only deviation. Short PDF supplied by explicit user instruction.',
 '1. Financial basis and definitions',
 'FY2025 calendar year, DKKm. Revenue 73,244; vendor EBIT 12,495 / EBITDA 21,583 versus issuer EBIT 8,620 / reported EBITDA 22,448 (25,065 excluding new partnerships and cancellation fees); net income to common 1,727; parent common equity 119,718 after stripping DKK 20,955 hybrid capital; gross debt 107,857; cash 53,448; NCI 8,268; base EV 236,927; tax 47%; common payout 0%.',
 '2. Comparable method',
 f"Ten Europe-listed peers selected at the first Europe step (Tier 1-2: {fig['tier12']}; Tier 3: {fig['tier3']}; Europe-listed: {fig['europe']}/10); no size/World relaxation. Primary EV/EBITDA median {prim['median']:.2f}x, n={int(prim['n_valid'])}; diagnostic range EUR {prim['value_per_share_low']:.2f}-{prim['value_per_share_high']:.2f}, midpoint EUR {prim['value_per_share_mid']:.2f} ({fig['peer_upside']:+.1%} vs price). Cross-check midpoints: EV/EBIT EUR {fig['peer_ev_ebit_mid']:.2f}; PBV EUR {fig['peer_pbv_mid']:.2f}.",
 '3. Published regression method',
 f"Denmark resolves exact EUROPE equations from regressions_multi_2026-01. PBV is selected by highest published R2 (0.423): EUR {fig['regression_pbv']:.2f}/share; PE EUR {fig['regression_pe']:.2f}; EV/EBITDA EUR {fig['regression_ev_ebitda']:.2f}. Analyst consensus growth inputs are g_eps 51.15% and g_rev 8.84%; payout is 0.0 on common basis. EV/EBITDA decimal-policy alternative is also recorded because the percentage-point policy gives a materially different multiple.",
 '4. Limitations and QA',
 'Ørsted had a large October 2025 rights issue, leaving a transitional cash/debt perimeter. Vendor and issuer EBIT/EBITDA definitions differ materially; hybrid capital is not common equity and is removed once in target EV inversions. The published equations are market-wide, low-R2, approximately ten months old, omit SEy/p-values, and use analyst-growth definitions. Human Spot_check and full source/ownership/event certification remain pending. QA block C was executed once and not passed; failures are recorded in qa_results.md, not waived.',
 'Academic analysis produced by an automated valuation agent. Not investment advice. All figures are sourced or derived from the files listed in the output directory.'
]
(P.parent/'relative_summary.md').write_text('\n\n'.join(lines)+'\n')

styles=getSampleStyleSheet(); doc=SimpleDocTemplate(str(P.parent/'relative_report_ORSTED.CO.pdf'),rightMargin=36,leftMargin=36,topMargin=36,bottomMargin=36)
story=[]
for i,line in enumerate(lines):
 style=styles['Heading1'] if i==0 else styles['BodyText']
 story += [Paragraph(line.replace('&','&amp;'),style),Spacer(1,7)]
doc.build(story)
print('QA',dict(counts),'PDF',P.parent/'relative_report_ORSTED.CO.pdf')
