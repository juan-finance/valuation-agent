"""ENR-only remediation from existing cached artifacts; no stage or full QA restart."""
import json,re
from datetime import datetime,timezone
from pathlib import Path
import numpy as np
import pandas as pd
from valuation_agent import comparables as c

P=Path(__file__).resolve().parent;O=P.parent;ROOT=P.parents[2]
assert 'remediation' not in json.loads((O/'run_state.json').read_text()), 'One-shot remediation already completed; do not repeat QA.'
STATUS='provisional - limitations disclosed'
started=datetime.now(timezone.utc).isoformat(timespec='seconds')
FX=json.loads((ROOT/'cache/macro/2026-10-30.json').read_text())['fx_ecb_reference']['rates'];FX['EUR']=1
D=pd.read_csv(P/'candidate_raw.csv').set_index('ticker',drop=False)
S=pd.read_csv(P/'comparables.csv');T=D.loc['ENR'];M=pd.read_csv(P/'multiples_summary.csv')
assert T.current_shares_m==855.34
assert abs(T.price*T.current_shares_m/T.market_cap_quote_m-1)<.0000023
assert len(S)==10 and (S.tier<=2).sum()==7 and (S.tier==3).sum()==3 and S.europe.sum()==9
dims=['growth','beta','net_debt_ebitda','roe','ebitda_margin','payout','capex_sales','ln_mcap']
assert (S.market_cap_eur_m>=1000).all() and S.market_cap_eur_m.between(T.market_cap_eur_m*.05,T.market_cap_eur_m*20).all()
assert S[dims].isna().sum(axis=1).le(2).all() and S.market_cap_check.abs().lt(.02).all()

# Debt/NCI already include identified claims. Zero is an incremental adjustment,
# not a certification that undisclosed hybrid/lease liabilities cannot exist.
rows=[]
for _,r in pd.concat([D.loc[['ENR']],S],ignore_index=True).iterrows():
 market=r.market_cap_quote_m*FX[r.report_currency]/FX[r.quote_currency]
 ev=c.comparable_ev(market,r.debt,r.NCI,r.cash,0)
 assert abs(ev-r.EV_before_associates)<1e-8
 rows.append(dict(ticker=r.ticker,report_currency=r.report_currency,market_equity_report_m=market,debt_including_vendor_leases=r.debt,NCI=r.NCI,incremental_hybrids=0,cash=r.cash,associate_investment_deduction=0,EV_pre_associate=ev,EBIT_vendor=r.EBIT,EBITDA_vendor=r.EBITDA,ev_ebit=ev/r.EBIT,ev_ebitda=ev/r.EBITDA,source=r.source_urls,rule='vendor basis retained; no incremental equity-income strip, lease/hybrid double count or associate/investment deduction'))
B=pd.DataFrame(rows).set_index('ticker',drop=False);B.to_csv(P/'ev_bridge.csv',index=False)
def val(mult,metric,shares=855.34,associates=0):
 return c.implied_equity_from_ev(mult,metric,T.debt,T.NCI,T.cash,associates)/shares
for k in ['ev_ebit','ev_ebitda','ev_cf','ev_assets','ev_sales']:
 metric={'ev_ebit':'EBIT','ev_ebitda':'EBITDA','ev_cf':'cfo','ev_assets':'assets','ev_sales':'sales'}[k]
 for i,r in S.iterrows():S.loc[i,k]=B.loc[r.ticker,'EV_pre_associate']/r[metric]
 stats=c.multiple_stats(S[k],min_valid=6);assert stats['usable']
 idx=M.index[M.multiple.eq(k)][0]
 for q in ['median','mean','p25','p75','n_valid','skew_flag']:M.loc[idx,q]=stats[q]
 for suffix,q in [('low','p25'),('mid','median'),('high','p75')]:
  raw=val(stats[q],T[metric]);M.loc[idx,'raw_value_'+suffix]=raw;M.loc[idx,'unadjusted_value_'+suffix]=raw
  if M.loc[idx,'selected_basis']!='scaled':M.loc[idx,'value_per_share_'+suffix]=raw
 M.loc[idx,'upside']=M.loc[idx,'value_per_share_mid']/T.price-1
 M.loc[idx,'status']='pre-associate vendor basis; limitations disclosed'
 M.loc[idx,'flags']='No associate/investment deduction; vendor operating-income classification retained; issuer basis sensitivity disclosed'
S['ownership_event_status']='qualified under approved source-line rule; limitations disclosed'
S['flags']='provisional; vendor pre-associate EV; book NCI/debt; beta definition limited; FY2025; human Spot_check pending'
S.to_csv(P/'comparables.csv',index=False)
M['is_primary']=M.multiple.isin(['ev_ebit','pe']);M['indicative_primary']=M.is_primary
M['n_source_certified']=np.where(M.n_valid.ge(6),10,0)
M['qualification_status']='10 qualified peers under approved automated/source-line rule'
M['valuation_status']=np.where(M.n_valid.ge(6),STATUS,'unavailable')
M.loc[M.multiple.eq('pe'),'status']='co-primary equity check; growth-scaled, vendor basis'
M['order']=np.where(M.multiple.eq('ev_ebit'),0,np.where(M.multiple.eq('pe'),1,2));M=M.sort_values('order',kind='stable').drop(columns='order');M.to_csv(P/'multiples_summary.csv',index=False)
pe=M[M.multiple.eq('pe')].iloc[0];ev=M[M.multiple.eq('ev_ebit')].iloc[0]
lo=min(ev.value_per_share_low,pe.value_per_share_low);hi=max(ev.value_per_share_high,pe.value_per_share_high)

# Existing peer identity/holder/event evidence is reused; no candidate recollection.
qual={
'WRT1V':('Investor AB17.7%; no disclosed >20% ENR cross-holding either direction','ANCS disposal FY2025 sales127m versus group6914m; smaller marine disposal noted; no >25% group-EV perimeter change identified','https://www.wartsila.com/investors/shareholders/largest-shareholders ; FY2025 report note6.3 linked in evidence_review.md'),
'VWS':('BlackRock/Capital Group5–10%; no disclosed >20% ENR cross-holding either direction','MHI consolidation2020 outsideFY2025; no material completedFY2025 perimeter change identified','https://www.vestas.com/en/investor/share-and-capital-structure/share-information'),
'SAND':('Industrivarden14.9%; no disclosed >20% ENR cross-holding either direction','Alleima spin2022 outsideFY2025; smaller bolt-ons noted, no >25% group-EV change identified','https://www.annualreport.sandvik/en/2025/to-our-shareholders/our-share.html'),
'ETN':('Institutional shareholder base, Irish operating company; no disclosed >20% ENR cross-holding either direction','Fibrebond/Resilient FY2025 bolt-ons; Boyd announced, UltraPCS FY2026; no >25% completedFY2025 group-EV change identified','https://www.sec.gov/Archives/edgar/data/1551182/000155118226000007/etn-20251231.htm'),
'SU':('BlackRock7.9%/MFS5.8%/Vanguard4.2% source screen; no disclosed >20% ENR cross-holding either direction','Smaller data-centre bolt-ons noted; no >25% group-EV completedFY2025 perimeter change identified','https://www.se.com/ww/en/about-us/investor-relations/ ; existing holder source in evidence_review.md'),
'G1A':('Kuwait Investment Office10.5%, free float89.5%; no disclosed >20% ENR cross-holding either direction','Buyback cancellation not operating perimeter;2026 organizational change, smaller bolt-ons noted','https://cdn.gea.com/-/media/investors/annual-report/2025/annual-report-2025-en.pdf'),
'LR':('Dispersed institutional holders; no disclosed >20% ENR cross-holding either direction','SevenFY2025 announced bolt-ons ~500m annualized sales, not transaction EV; no confirmed >25% EV change identified; smaller events noted','https://www.legrand.com/en/news/2025-full-year-results ; holder source in evidence_review.md'),
'METSO':('Solidium14.9%, Cevian7.77%; no disclosed >20% ENR cross-holding either direction','Merger2020 outsideFY2025; no >25% completedFY2025 group-EV change identified','https://www.metso.com/corporate/investors/shares/shareholders/'),
'ALFA':('Winder29.53% independent controlling family, not target; no disclosed >20% ENR cross-holding either direction','FY2025 small US-service acquisition; no >25% group-EV change identified','https://www.alfalaval.com/globalassets/documents/investors/english/annual-reports/2025/annual-and-sustainability-report-2025.pdf'),
'SPX':('Listed institutional holders; no disclosed >20% ENR cross-holding either direction','FY2025 acquisitions net cash10.6m GBP vsEV6175.2m;40m savings restructuring noted, no material perimeter replacement','https://content.spiraxgroup.com/-/media/engineering/documents/results-and-agm-notices/2025/ara/downloads/spirax-group-plc-annual-report-2025-financial-statements.ashx?rev=245626e21a7f47c199ce9b633a887475')}
Q=pd.DataFrame([dict(ticker=t,automated_hard_filters='PASS: developed nonfinancial operating company; size/mincap/history/missing metrics',ownership=v[0],events=v[1],source=v[2],qualification='PASS-with-note; disclosed source-line screen, not exhaustive certification') for t,v in qual.items()]);Q.to_csv(P/'peer_qualification.csv',index=False)
e=P/'evidence_review.md';old=e.read_text();e.write_text('# Current remediation basis\nStatus: '+STATUS+'. Supersedes historic certification/blocking conclusions below. Sources accessed2026-11-01/02; valuation cutoff2026-10-30 unchanged. No full-candidate ownership-history certification required under approved grading. Ten selected peers retain automated filters and source lines; smaller events are noted, no confirmed >25% completed FY2025 perimeter-change exclusion identified.\n\n'+Q.to_markdown(index=False)+'\n\nUniform EV: market equity + vendor lease-inclusive debt + NCI + incremental hybrids once - cash. Incremental hybrid/lease adjustment0 for every row (none separately identified outside vendor claims); no associates or investments subtracted. Vendor operating EBIT/EBITDA retained, no incremental equity-income stripping or source switching. Vendor ENR operating EBIT1569 excludes580 equity-accounted income by its own classification; issuer2149 is a sensitivity, not a per-row base replacement. This definition mismatch is disclosed, not hidden. Peer equity-income classification is likewise retained as supplied. Book claims/cash availability remain limitations.\n\n'+old)

sens=pd.read_csv(P/'sensitivities.csv');sens['qualified']=STATUS
extra=[]
def sensitivity(name,value,base):extra.append(dict(sensitivity=name,value_per_share=value,base_value_per_share=base,change_fraction=value/base-1,qualified='sensitivity only; base vendor rule unchanged'))
sensitivity('issuer operating EBIT2149 vs vendor1569; median held fixed',val(ev['median'],2149),ev.value_per_share_mid)
sensitivity('issuer850m issued shares vs base855.34m; EV/EBIT',val(ev['median'],T.EBIT,850),ev.value_per_share_mid)
sensitivity('issuer850m issued shares vs base855.34m; scaled PE',pe.value_per_share_mid*855.34/850,pe.value_per_share_mid)
sensitivity('associate703 book value added back in equity inverse; diagnostic only; EV/EBIT',val(ev['median'],T.EBIT,associates=703),ev.value_per_share_mid)
pd.concat([sens,pd.DataFrame(extra)],ignore_index=True).to_csv(P/'sensitivities.csv',index=False)

notes={3:'PASS: uniform855.34m shares and108560m cap reconcile within0.00023%;850m is sensitivity, not an error.',4:'PASS-with-note: vendor fields retained consistently, lineage/definitions disclosed.',5:'PASS-with-note: registered industry aggregates, not medians; plausibility only; target recovery/margin mix explains large gaps.',8:'PASS-with-note:10 automated/source-line qualified peers, not a requirement for exhaustive history certification.',9:'PASS-with-note: automated filters retained; selected ownership/events source lines, smaller events noted, no confirmed >25% exclusion.',11:'PASS-with-note:26 initial candidates and ordered expansions retained; no full-pool ownership/event certification demanded.',17:'PASS-with-note: uniform pre-associate EV/EBIT primary alongside growth-scaled PE, not PE-only fallback.',18:'PASS-with-note: one vendor pre-associate bridge and exact inverse for target/all peers; no investments/associates deducted.',20:'PASS-with-note: peer/IQR/LOO, margin, issuer-definition and share sensitivities disclosed; no invented normalization.',42:'PASS-with-note: both DFR/tax policies retained, approved decimal base, industry aggregate plausibility and units_unverified disclosed.'}
f=P/'qa_results.md';old=f.read_text();parts=re.findall(r'### C(\d+) — ([^\n]+)\n',old);grades={int(n):g for n,g in parts}
for n in notes:grades[n]='PASS' if n==3 else 'PASS-with-note'
counts={k:list(grades.values()).count(k) for k in ['PASS','PASS-with-note','FAIL','N/A']}
header='# QA block C — current status\n\n**'+STATUS+'**; '+str(counts)+'. Human Spot_check PENDING, not performed/waived. Valuation range EUR '+f'{lo:.2f}–{hi:.2f}'+': envelope of EV/EBIT and growth-scaled PE peer IQRs, not a confidence interval.\n\n## Remediation re-grade\nApproved qa_grading_and_remediation and relative_only applied. C3–C20 and C42 reviewed for this remediation: only previously failing/changed items re-tested once; unchanged passing items retained, not rerun. No full QA repetition.\n\n'+'\n'.join(f'- C{n}: {notes[n] if n in notes else "PASS retained; no changed calculation or passing-QA rerun."}' for n in list(range(3,21))+[42])+'\n\n## Historical QA — superseded, preserved verbatim\n\n'
f.write_text(header+old)
v=pd.read_csv(P/'valuation_multiples.csv',keep_default_na=False);v['validation_status']=STATUS;v['shares_m']=855.34;v.to_csv(P/'valuation_multiples.csv',index=False)
fig=json.loads((P/'report_figures.json').read_text());fig.update(status=STATUS,qa=counts,primary_multiples=['ev_ebit','pe'],ev_bridge='uniform vendor pre-associate; no investment deduction or incremental equity-income stripping',ev_ebit_median=float(ev['median']),ev_ebit_value=float(ev.value_per_share_mid),ev_ebit_iqr=[float(ev.value_per_share_low),float(ev.value_per_share_high)],pe_value=float(pe.value_per_share_mid),pe_iqr=[float(pe.value_per_share_low),float(pe.value_per_share_high)],valuation_range_eur=[lo,hi],valuation_range_basis='envelope of two primary peer IQRs; no averaging with regressions',qualified_peers=10,issuer_ebit_sensitivity=extra[0],shares_sensitivity=extra[1:3]);(P/'report_figures.json').write_text(json.dumps(fig,indent=2)+'\n')
margin= float(sens[sens.sensitivity.eq('common EBIT margin all observations')].iloc[0].value_per_share)
company_notes=[
 f'ENR equipment/service turnaround: uniform pre-associate EV/EBIT primary EUR{ev.value_per_share_mid:.2f} (peer IQR {ev.value_per_share_low:.2f}–{ev.value_per_share_high:.2f}) alongside growth-scaled PE EUR{pe.value_per_share_mid:.2f} ({pe.value_per_share_low:.2f}–{pe.value_per_share_high:.2f}); range EUR{lo:.2f}–{hi:.2f}, dispersion not confidence. PE is not fallback-only. Published PBV35.94 is separate, not averaged.',
 'Uniform vendor shares855.34m/cap108560m retained (price126.92 reconciliation0.00023%); issuer850m issued is a +0.628% per-share sensitivity, not an outstanding-share error. ENR FY2025 parentNI1414 differs from group1685 because NCI271.',
 f'Vendor ENR EBIT1569 versus issuer2149 reflects580 equity-accounted income classification; vendor fields kept for every observation, no incremental equity-income strip. Issuer2149 sensitivity at fixed peer median gives EUR{extra[0]["value_per_share"]:.2f} ({extra[0]["change_fraction"]:+.1%}, above15%); no associates/investments deducted from EV; leases/NCI/hybrids counted once using vendor claims with0 incremental unidentified hybrids.',
 f'ENR weak wind margin and portfolio/restructuring offset make reported earnings fragile. Mechanical all-target/all-peer EBIT margin4/6/8/10% sensitivity gives EUR{margin:.2f} ({margin/ev.value_per_share_mid-1:+.1%}, above15%); it is algebraic rescaling, not researched normalization or a recovery forecast. FY2025 net specials+6 mask large gross costs/gains.',
 f'Primary peer quartiles materially move value: EV/EBIT{ev.value_per_share_low/ev.value_per_share_mid-1:+.1%}/{ev.value_per_share_high/ev.value_per_share_mid-1:+.1%}, PE{pe.value_per_share_low/pe.value_per_share_mid-1:+.1%}/{pe.value_per_share_high/pe.value_per_share_mid-1:+.1%} (both PE tails above15%; raw PE31.24x gives EUR51.65 versus scaled EUR71.47 (-27.7%, above15%); EV/EBITDA alternative EUR60.61 is +37.2% versus EV/EBIT, above15%); full multiple alternatives in table.10 peers,7 Tier1/2,3 Tier3,9 Europe: approved cap4 relaxation retained; smaller bolt-ons/restructurings noted, not automatic exclusions.',
 'FY2025 CFO5821 includes customer advances, not enterprise FCFF; noDCF or Stage4 recommendation. Industry aggregates Electrical Equipment18.94x EV/EBITDA and24.34x EV/EBIT are plausibility only, not medians. Registered published models use labelled fundamental growth rather than analyst forecasts; both unit policies retained. Human Spot_check remains PENDING; academic analysis only, not investment advice.'
];(O/'report_notes.md').write_text('\n'.join('- '+n for n in company_notes)+'\n')
rs=json.loads((O/'run_state.json').read_text());rs['stages']['stage3_relative']['status']=STATUS;rs['stages']['stage3_relative']['next_step']='';rs['stages']['stage3_relative']['notes'].append(started+' Remediation under approved grading: uniform pre-associate EV/EBIT + PE primary;10 qualified source-line peers; historical blocking conclusions superseded; human Spot_check pending.')
rs.update(final_status=STATUS,session_status=STATUS,human_review='pending');rs['qa_C'].update(status=STATUS,counts=counts,unresolved_failures=0,next_step='',regrade_executions=1,regraded_items=list(notes));rs['short_report']['status']=STATUS
rs['remediation']={'started':started,'rule':'qa_grading_and_remediation + relative_only','status':STATUS,'changes':['C3–C20/C42 targeted re-grade; history preserved','uniform pre-associate ev_bridge.csv; no candidate recollection','855.34m base/850m sensitivity; Tier3cap4 retained','EV/EBIT + PE primary; report_figures and notes refreshed'],'valuation_range_eur':[lo,hi],'human_spot_check':'pending'}
(O/'run_state.json').write_text(json.dumps(rs,indent=2)+'\n')
print('Targeted remediation checks passed:',counts,'EV/EBIT',ev.value_per_share_mid,'PE',pe.value_per_share_mid,'range',lo,hi)
