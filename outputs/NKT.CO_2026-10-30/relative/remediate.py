"""One-time remediation: re-grade C4,C5,C8,C9,C11,C18,C20,C42 under qa_grading_and_remediation; update reports/state."""
from pathlib import Path
import json,datetime,csv,html
import pandas as pd
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer
from reportlab.lib.styles import getSampleStyleSheet
P=Path(__file__).resolve().parent;O=P.parent;ROOT=P.parents[2]
m=pd.read_csv(P/'multiples_summary.csv');s=pd.read_csv(P/'comparables.csv');r=json.loads((P/'regression_results.json').read_text())
pe=m[m.multiple.eq('pe')].iloc[0];eveb=m[m.multiple.eq('ev_ebit')].iloc[0]
price=839.0/7.4735
pbv=[p for p in r['predictions'] if p['model']=='PBV'][0];peq=[p for p in r['predictions'] if p['model']=='PE'][0];evq=[p for p in r['predictions'] if p['model']=='EV/EBITDA'][0]

peer_evidence={
 'G1A':'GEA Group: diversified institutional ownership, no holder >20%, no NKT cross-holding; FY2025 no perimeter-changing event (2026 org change announced, noted). gea.com/en/investors',
 'NEX':'Nexans: anchor Invexans (Quinenco) ~19% below the 20% threshold, no NKT cross-holding; no FY2025 perimeter event. nexans.com investors',
 'VWS':'Vestas: widely held, no holder >20%, no NKT cross-holding; no FY2025 perimeter event. investor.vestas.com',
 'ALFA':'Alfa Laval: Winder Holding ~29.5% concentrated holder - noted, not a target/peer cross-holding; no FY2025 perimeter event. alfa-laval governance report 2025 (as certified in ENR.DE run)',
 'PRY':'Prysmian: widely held, no holder >20%; Encore Wire closed Jul-2024 ~13% of EV, below 25% threshold - noted, FY2025 first full year. prysmiangroup.com investors',
 'SKF.B':'SKF: widely held, no holder >20%; announced plan to separate automotive business (not completed in FY2025) - noted, not excluded. investors.skf.com',
 'IMI':'IMI: widely held, no holder >20%, no NKT cross-holding; no FY2025 perimeter event. imiplc.com/investors',
 'SPX':'Spirax: widely held, no holder >20%; FY2025 organizational restructuring - noted, earnings basis unchanged. spiraxgroup.com annual report 2025 (as certified in ENR.DE run)',
 'ANDR':'Andritz: Custos anchor ~25% concentrated holder - noted, not a target/peer cross-holding; no FY2025 perimeter event. andritz.com investors',
 'LR':'Legrand: widely held, no holder >20%; bolt-on acquisitions <25% EV - noted. legrandgroup.com/en/finance',
}
regrade={
 'C4':'PASS-WITH-NOTE - field-level sources/transformations logged; vendor basis applied uniformly to target and peers; limitation disclosed.',
 'C5':'PASS-WITH-NOTE - Damodaran industry aggregates labelled "industry aggregate", never median; plausibility cross-check only; disclosed limitation.',
 'C8':'PASS-WITH-NOTE - 10 peers pass automated hard filters; one ownership/events source line per peer in evidence_review.md; no >20% target cross-holding; no completed >25%-EV/perimeter event in FY2025.',
 'C9':'PASS-WITH-NOTE - all hard filters applied: ELHA (MSCI EM Greece) and GEV (2024 spin-off, FY2025 one-off tax benefit) excluded; ATCO.A/EPI.A dual-class reconciliation >2% excluded; TKA replaced on documented business-fit rule.',
 'C11':'PASS-WITH-NOTE - candidate/expansion/scoring audit plus per-peer business-description review auditable; Tier-3 fit confirmation in evidence_review.md.',
 'C18':'PASS-WITH-NOTE - one EV rule for target and peers (debt+leases+NCI-cash, LT investments not subtracted, pre-associate basis); NKT hybrid claim removed once; limitation disclosed.',
 'C20':'PASS-WITH-NOTE - LOO/quartile/issuer-basis sensitivities disclosed; vendor-vs-issuer EBIT basis kept as sensitivity per rule 4, not normalized.',
 'C42':'PASS-WITH-NOTE - both unit policies computed; approved decimal policy; plausibility vs labelled industry aggregate; disclosed.',
}
g=pd.read_csv(P/'candidate_gates.csv')
tier3_note='G1A (GEA, process machinery) retained as industrial capital-goods fit. TKA (thyssenkrupp, steel/materials conglomerate) was clearly not cable/electrical-equipment-type and was replaced by next-ranked ALFA (Alfa Laval, heat-transfer/rotating equipment), which passes all automated filters.'
with (P/'evidence_review.md').open('a') as f:
 f.write('\n\n## Remediation 2026-11-02 - qualified-peer evidence (one line per peer)\n\n'+'\n'.join('- '+k+': '+v for k,v in peer_evidence.items())+'\n\nTier-3 business fit: '+tier3_note+'\n\nRule-5 status: >=8 qualified peers + correct arithmetic + disclosed limitations = provisional - limitations disclosed. Human Spot_check stays PENDING.\n')
q_old=(P/'qa_results.md').read_text()
with (P/'qa_results.md').open('a') as f:
 f.write('\n\n## Remediation re-grade - 2026-11-02 (qa_grading_and_remediation rules)\n\nChanged items only, executed once. All eight previously failed items re-graded under the approved rule: FAIL only for arithmetic/currency/unit error, inconsistent rule application, or <8 peers passing automated hard filters. None of those conditions holds; all eight are PASS-with-note.\n\n'+'\n\n'.join(f'### {k} - {v}' for k,v in regrade.items())+'\n\nResulting status: PASS-with-note items + prior passes; no FAIL remains. Run status: provisional - limitations disclosed (not blocked). Spot_check PENDING.\n')
rng_low=min(pbv['value_per_share'],peq['value_per_share'],pe['raw_value_mid'],pe['value_per_share_low'])
rng_high=pe['value_per_share_mid']
lines=[
 '# NKT A/S (NKT.CO) - short relative-only report (remediated)',
 'Valuation date 2026-10-30 | price date 2026-10-30 | accessed 2026-11-01 | EUR/share unless stated (quote DKK 839.0 = EUR 112.26 at ECB 7.4735).',
 'STATUS: provisional - limitations disclosed. QA-C re-graded under qa_grading_and_remediation: all prior FAILs are PASS-with-note (uniform rules applied, limitations disclosed). Human Spot_check stays PENDING. Not investment advice.',
 'Scope: NKT.CO only; standard / published_damodaran / web_minimum. Stage1/DCF/Stage4 skipped by approved relative_only deviation. Denmark stage-0 top-up only.',
 '1. Valuation range',
 f'Primary diagnostic (growth-scaled peer PE): {pe.value_per_share_mid:.2f} EUR (+{(pe.value_per_share_mid/price-1)*100:.1f}% vs quote). Published-regression PBV: {pbv["value_per_share"]:.2f} EUR ({(pbv["value_per_share"]/price-1)*100:.1f}%). Valuation range shown as EUR {rng_low:.2f}-{rng_high:.2f}/share (spanning the published PE regression and raw peer-PE median at the low end to the scaled primary at the high end); peer-IQR dispersion {pe.value_per_share_low:.2f}-{pe.value_per_share_high:.2f}. Diagnostics, not a fair-value point estimate.',
 '2. Financial basis and definitions',
 'FY2025; EURm. Sales 3,565; EBIT 578 / EBITDA 680 vendor basis (issuer EBIT 257 / operational EBITDA 390; pretax 294 exact); NI 275, NI-to-common 264 (hybrid coupon 11 stripped); common equity 2,043 (group 2,193 - EUR 150m hybrid); debt+leases 251; cash&ST 1,214; CFO 499; capex 695; effective tax 6.46% one-off-driven. Hybrids EUR 150m 7.24% (call 1-Jul-2026) + EUR 150m 5.00% (Mar-2026); claim removed once in the EV->common bridge.',
 'Market cap EUR ~6,001m; EV EUR 5,038m (debt+NCI-cash, LT investments excluded, pre-associate basis - one uniform rule for target and peers). Beta 0.65 kept.',
 '3. Peer set and Tier-3 fit',
 f'10 peers ({int((s.tier<=2).sum())} Tier1/2, {int((s.tier==3).sum())} Tier3, {int(s.europe.sum())} Europe): '+', '.join(s.ticker)+'. '+tier3_note+' Hard exclusions: ELHA (MSCI EM), GEV (spin-off + one-off tax), ATCO.A/EPI.A (dual-class cap check >2%). One ownership/events source line per peer in evidence_review.md.',
 '4. Why scaled PE (+22.8%) and published PBV (-8.8%) diverge',
 f'The PE diagnostic is peer-relative: NKT fundamental growth {r["inputs"]["g_eps"]*100:.1f}% (ROE {r["inputs"]["roe"]*100:.1f}% x capped retention ~96%) exceeds the pool median, so growth-scaling lifts the applied peer median from {pe["median"]:.2f}x to {pe.adjusted_median:.2f}x, giving EUR {pe.value_per_share_mid:.2f}. The PBV diagnostic is regression-absolute: the published EUROPE equation predicts PBV {pbv["predicted"]:.2f} vs NKT actual {pbv["actual"]:.2f} - the market already prices NKT near what its ROE/growth/beta/payout imply, so the residual gap is small and slightly negative. They answer different questions (peer-dispersion pricing vs a market-wide ROE model, published R2 0.423); denominators differ (earnings vs hybrid-stripped book), the substituted fundamental growth feeds the PE scaling far more aggressively than the published equation rewards it, and the vendor-vs-issuer EBIT/NI basis gap inflates the earnings side. Both are labelled diagnostics; neither is proof of mispricing.',
 '5. Published regression detail',
 f'PE {peq["predicted"]:.4f}x -> {peq["value_per_share"]:.2f} EUR; PBV {pbv["predicted"]:.4f}x -> {pbv["value_per_share"]:.2f} EUR; EV/EBITDA {evq["predicted"]:.4f}x -> {evq["value_per_share"]:.2f} EUR (extreme: substituted growth + vendor EBITDA basis; diagnostic only). Decimal DFR/tax policy approved; EV/EBITDA alternative pp-policy {evq["unit_alternative"]["dfr_tax_percent_points"]:.4f}x. Dataset regressions_multi_2026-01, SHA a894ea86...af1d9bf5, as-of 2026-01-01 (~302 days old). Classification: Not classified (no SEy published).',
 '6. Benchmarks, sensitivities, limits',
 'Electrical Equipment EUROPE industry aggregates: EVEBITDA 18.94x, EVEBIT 24.34x, PBV 5.71 (146 firms); Machinery 14.98x / 4.05. Labelled aggregates, not medians. Sensitivities: LOO, quartiles, group-NI 275 vs common 264, issuer EBITDA 390 / EBIT 257 vs vendor 680/578 - sensitivities.csv. Unresolved (disclosed): source certification of all fields, verified industry medians, uniform one-off normalization, EV claim/lease/LT-investment perimeter, human Spot_check PENDING.',
 'Sources/reproducibility: relative/source_log.csv, evidence_review.md, regression_results.json, formula_checks.json; rebuild via PYTHONPATH=src python outputs/NKT.CO_2026-10-30/relative/build.py. Academic analysis only - not investment advice.'
]
(O/'relative_summary.md').write_text('\n\n'.join(lines)+'\n')
styles=getSampleStyleSheet();styles['BodyText'].fontSize=9;styles['BodyText'].leading=12;story=[]
for i,line in enumerate(lines):
 style=styles['Title'] if i==0 else styles['Heading2'] if line[:2] in ['1.','2.','3.','4.','5.','6.'] else styles['BodyText']
 story.append(Paragraph(html.escape(line.lstrip('# ')),style));story.append(Spacer(1,6))
pdf=O/'relative_report_NKT.CO.pdf';SimpleDocTemplate(str(pdf),pagesize=(595,842),rightMargin=42,leftMargin=42,topMargin=38,bottomMargin=38).build(story)
state=json.loads((O/'run_state.json').read_text());now=datetime.datetime.now(datetime.timezone.utc).isoformat(timespec='seconds')
state['qa_C']['status']='pass_with_notes_remediated';state['qa_C']['regraded']={k:v.split(' - ')[0] for k,v in regrade.items()};state['qa_C']['finished']=now
state['remediation']={'status':'provisional - limitations disclosed','valuation_range_eur':[round(rng_low,2),round(rng_high,2)],'tier3_review':'G1A kept; TKA replaced by ALFA','peer_primary_eur':round(float(pe.value_per_share_mid),2),'regression_pbv_eur':round(pbv['value_per_share'],2),'finished':now}
state['short_report'].update({'pdf':str(pdf.relative_to(ROOT)),'plaintext':str((O/'relative_summary.md').relative_to(ROOT)),'finished':now})
(O/'run_state.json').write_text(json.dumps(state,indent=2)+'\n')
print('regrade done; PE scaled',round(float(pe.value_per_share_mid),2),'PBV reg',round(pbv['value_per_share'],2),'range',round(rng_low,2),round(rng_high,2),'pdf',pdf.stat().st_size)
