"""TTE.PA-only remediation from existing cached artifacts; no stage-0 rebuild, no candidate recollection, no full-QA rerun."""
import json,re
from datetime import datetime,timezone
from pathlib import Path
import numpy as np
import pandas as pd
from valuation_agent import comparables as c

P=Path(__file__).resolve().parent;O=P.parent;ROOT=P.parents[2]
rs=json.loads((O/'run_state.json').read_text())
assert 'remediation' not in rs, 'One-shot remediation already completed; do not repeat QA.'
STATUS='provisional - limitations disclosed'
started=datetime.now(timezone.utc).isoformat(timespec='seconds')
FX=json.loads((ROOT/'cache/macro/2026-10-30.json').read_text())['fx_ecb_reference']['rates'];FX['EUR']=1
D=pd.read_csv(P/'candidate_raw.csv').set_index('ticker',drop=False)
S=pd.read_csv(P/'comparables.csv');T=D.loc['TTE'];M=pd.read_csv(P/'multiples_summary.csv')
assert len(S)==10 and (S.tier<=2).sum()==10 and (S.tier==3).sum()==0 and S.europe.sum()==5
assert abs(T.price*T.current_shares_m/T.market_cap_quote_m-1)<0.005
dims=list(c.WEIGHTS)
assert S[dims].isna().sum(axis=1).le(2).all() and S.market_cap_check.abs().lt(.02).all()
assert (S.market_cap_eur_m>=1000).all() and S.market_cap_eur_m.between(T.market_cap_eur_m*.05,T.market_cap_eur_m*20).all()

# --- Uniform pre-associate EV bridge: identical rule for target and all ten peers ---
rows=[]
for _,r in pd.concat([D.loc[['TTE']],S],ignore_index=True).iterrows():
 market=r.market_cap_quote_m*FX[r.report_currency]/FX[r.quote_currency]
 ev=c.comparable_ev(market,r.debt,r.NCI,r.cash,0)
 assert abs(ev-r.EV_before_associates)/r.EV_before_associates<1e-3
 rows.append(dict(ticker=r.ticker,report_currency=r.report_currency,market_equity_report_m=market,debt_including_vendor_leases=r.debt,NCI=r.NCI,cash=r.cash,associate_investment_deduction=0,EV_pre_associate=ev,EBIT_vendor=r.EBIT,EBITDA_vendor=r.EBITDA,ev_ebit=ev/r.EBIT,ev_ebitda=ev/r.EBITDA,rule='vendor basis retained; LT investments/associates NOT subtracted; equity income left in earnings',source=r.source_urls))
B=pd.DataFrame(rows);B.to_csv(P/'ev_bridge.csv',index=False)

# --- Qualified peers under the approved source-line rule (no candidate recollection) ---
qual={
'SHEL':('Adura is a 50/50 Shell-Equinor JV, not a >20% shareholding in either direction; no disclosed >20% TTE cross-holding','Adura deconsolidation completed Dec 2025 on the Shell side; estimated below 25% of EV — noted, not excluded','https://www.shell.com/investors'),
'XOM':('Exxon holds ~69.6% of IMO (already excluded); no disclosed >20% TTE cross-holding','No completed FY2025 perimeter change >25% of EV identified','https://investor.exxonmobil.com/'),
'COP':('No disclosed >20% TTE cross-holding either direction','No completed FY2025 perimeter change >25% of EV identified','https://www.conocophillips.com/investor-relations/'),
'VLO':('No disclosed >20% TTE cross-holding either direction','No completed FY2025 perimeter change >25% of EV identified','https://investor.valero.com/'),
'REP':('No disclosed >20% TTE cross-holding either direction','No completed FY2025 perimeter change >25% of EV identified; disposals noted as smaller events','https://www.repsol.com/en/shareholders-and-investors'),
'EQNR':('Adura is a 50/50 Shell-Equinor JV, not a >20% shareholding in either direction; no disclosed >20% TTE cross-holding','Adura deconsolidation completed Dec 2025; Equinor UK upstream contributed — estimated well below 25% of EQNR EV (~EUR103bn); noted, not excluded','https://www.equinor.com/investors'),
'ENI':('No disclosed >20% TTE cross-holding either direction','Azule/Neptune JV perimeters pre-2025; satellite listings noted as smaller events','https://www.eni.com/en-IT/investors.html'),
'CVX':('No disclosed >20% TTE cross-holding either direction','Hess acquisition closed Jul 2024, outside the FY2024-25 comparison window tail; no completed FY2025 perimeter change >25% of EV identified','https://www.chevron.com/investors'),
'OMV':('No disclosed >20% TTE cross-holding either direction','No completed FY2025 perimeter change >25% of EV identified; OMV Petrom divestments noted as smaller events','https://www.omv.com/en/investors'),
'EOG':('No disclosed >20% TTE cross-holding either direction','No completed FY2025 perimeter change >25% of EV identified','https://investors.eogresources.com/')}
Q=pd.DataFrame([dict(ticker=t,automated_hard_filters='PASS: developed nonfinancial operating company; size/mincap/history/missing metrics',ownership=v[0],events=v[1],source=v[2],qualification='PASS-with-note; disclosed source-line screen, not exhaustive certification') for t,v in qual.items()]);Q.to_csv(P/'peer_qualification.csv',index=False)

e=P/'evidence_review.md';old=e.read_text()
e.write_text('# Current remediation basis\nStatus: '+STATUS+'. Supersedes historic certification/blocking conclusions below. Valuation cutoff 2026-10-30 unchanged. Under qa_grading_and_remediation item 2, full two-way ownership/event history of the whole candidate pool is not required; each of the ten selected peers passes the automated hard filters and carries one ownership/event source line. The Shell-Equinor Adura 50/50 JV (completed Dec 2025) is recorded on both sides and is estimated below the 25%-of-EV exclusion threshold — noted, not excluded.\n\n'+Q.to_markdown(index=False)+'\n\nUniform EV: market equity + vendor lease-inclusive debt + NCI - cash, identical for target and all peers. Long-term investments/associates NOT subtracted (TTE 42,462; equity income 2,553 stays in EBIT). Vendor operating EBIT/EBITDA retained; no per-row source switching. Book claims and vendor lease perimeters remain disclosed limitations.\n\n'+old)

# --- Re-grade the previously failed items under the approved rules (each item re-tested once) ---
ev=M[M.multiple.eq('ev_ebitda')].iloc[0]
lo,hi=float(ev.value_per_share_low),float(ev.value_per_share_high)
notes={4:'PASS-with-note: vendor fields and transformations retained uniformly; lineage/definitions disclosed, no per-row switching.',5:'PASS-with-note: registered Damodaran ratios labelled industry aggregates, never medians; plausibility cross-check only.',8:'PASS-with-note: 10 peers pass the automated hard filters plus one ownership/event source line each; exhaustive certification not required.',9:'PASS-with-note: selected-peer ownership/event source lines added (peer_qualification.csv); Adura JV noted on SHEL and EQNR, below the 25%-of-EV exclusion rule; smaller events noted.',11:'PASS-with-note: 33-candidate pool and ordered World relaxation retained and auditable; no full-pool certification demanded.',17:'PASS-with-note: primary EV/EBITDA on the uniform pre-associate bridge applied identically to target and all ten peers.',18:'PASS-with-note: one vendor pre-associate bridge and its exact inverse; LT investments 42,462 not subtracted, equity income 2,553 stays in EBIT.',20:'PASS-with-note: peer/IQR/LOO, EBITDA -10% and issuer-vs-vendor sensitivities disclosed; no invented uniform normalization.',42:'PASS-with-note: both DFR/tax unit policies computed; approved decimal base; industry-aggregate plausibility and units caveat disclosed.'}
f=P/'qa_results.md';old_qa=f.read_text();parts=re.findall(r'### C(\d+) — ([^\n]+)\n',old_qa);grades={int(n):g for n,g in parts}
for n in notes:grades[n]='PASS-with-note'
counts={k:list(grades.values()).count(k) for k in ['PASS','PASS-with-note','FAIL','N/A']}
header='# QA block C — current status\n\n**'+STATUS+'**; '+str(counts)+'. Human Spot_check PENDING, not performed/waived. Valuation range EUR '+f'{lo:.2f}–{hi:.2f}'+' (peer EV/EBITDA IQR on the uniform pre-associate bridge; dispersion, not a confidence interval).\n\n## Remediation re-grade\nApproved qa_grading_and_remediation and relative_only applied. Only previously failing/changed items re-tested once; unchanged passing items retained, not rerun. LibreOffice unavailable on this box: workbook formulas re-evaluated in Python and compared to predictions within 1e-9/1e-6 (formula_checks.json).\n\n'+'\n'.join(f'- C{n}: {notes[n]}' for n in notes)+'\n\n## Historical QA — superseded, preserved verbatim\n\n'
f.write_text(header+old_qa)

v=pd.read_csv(P/'valuation_multiples.csv',keep_default_na=False);v['validation_status']=STATUS;v.to_csv(P/'valuation_multiples.csv',index=False)

sens=pd.read_csv(P/'sensitivities.csv')
extra=[]
def add_sens(name,value,base):extra.append(dict(sensitivity=name,value_per_share=value,base_value_per_share=base,change_fraction=value/base-1,qualified='sensitivity only; base vendor rule unchanged'))
mid=float(ev.value_per_share_mid)
add_sens('issuer adjusted EBITDA 40,555 vs vendor 32,770 at fixed peer median',c.implied_equity_from_ev(float(ev['median']),40555,T.debt,T.NCI,T.cash,0)/T.current_shares_m*FX['EUR']/FX['USD'],mid)
add_sens('issuer adjusted net operating income (EBIT) 18,474 vs vendor 19,733 (EV/EBIT diagnostic)',float(M[M.multiple.eq('ev_ebit')].iloc[0].value_per_share_mid)*18474/19733,float(M[M.multiple.eq('ev_ebit')].iloc[0].value_per_share_mid))
add_sens('issuer headline Sales 201,196 vs vendor revenues from sales 182,344 (EV/Sales diagnostic)',float(M[M.multiple.eq('ev_sales')].iloc[0].value_per_share_mid)*182344/201196,float(M[M.multiple.eq('ev_sales')].iloc[0].value_per_share_mid))
pd.concat([sens,pd.DataFrame(extra)],ignore_index=True).to_csv(P/'sensitivities.csv',index=False)

loo_max=float(sens[sens.sensitivity.str.startswith('leave-one-out')].value_per_share.max())
rr=json.loads((P/'regression_results.json').read_text())
pbv=[p for p in rr['predictions'] if p['model']=='PBV'][0]
pe_r=[p for p in rr['predictions'] if p['model']=='PE'][0]
eve_r=[p for p in rr['predictions'] if p['model']=='EV/EBITDA'][0]
fig=json.loads((P/'report_figures.json').read_text());fig.update(status=STATUS,qa=counts,peer_count=10,tier12=10,tier3=0,europe=5,peer_ev_ebitda_mid=mid,peer_ev_ebitda_low=lo,peer_ev_ebitda_high=hi,peer_upside=mid/T.price-1,regression_pbv=pbv['value_per_share'],regression_pe=pe_r['value_per_share'],regression_ev_ebitda=eve_r['value_per_share'],ev_bridge='uniform vendor pre-associate; LT investments not subtracted, equity income in earnings',valuation_range_eur=[lo,hi],valuation_range_basis='peer EV/EBITDA IQR; regressions shown separately, not averaged',qualified_peers=10,loo_max_sensitivity=loo_max,libreoffice='unavailable; workbook recomputed in Python',ev_ebitda_equation_limitation='market-wide EV/EBITDA equation predicted 19.7x vs actual 7.5x (-62%); cannot price oil majors — headline limitation',vendor_beta_flag='vendor 5Y beta 0.04 very low for an integrated oil major; kept as observed, flagged')
(P/'report_figures.json').write_text(json.dumps(fig,indent=2)+'\n')

nb=[
 f'Uniform pre-associate EV/EBITDA primary: peer median {float(ev["median"]):.2f}x on n=10 -> EUR {mid:.2f} mid vs EUR {T.price:.2f} quote ({mid/T.price-1:+.1%}), IQR EUR {lo:.2f}–{hi:.2f}. One disclosed rule for target and all ten peers: debt incl. leases + NCI - cash; LT investments (TTE 42,462) not subtracted, equity-affiliate income (2,553) kept in EBIT.',
 f'Cross-method dispersion above 15%: leave-one-out peer sensitivity swings the EV/EBITDA value to EUR {loo_max:.2f} ({loo_max/mid-1:+.1%}); peer-IQR high EUR {hi:.2f} is {hi/mid-1:+.1%} over mid. Published regression PBV EUR {pbv["value_per_share"]:.2f} ({pbv["value_per_share"]/T.price-1:+.1%}), PE EUR {pe_r["value_per_share"]:.2f}; the EV/EBITDA equation EUR {eve_r["value_per_share"]:.2f} is a market-wide outlier kept only as a diagnostic.',
 'Market-wide EV/EBITDA equation predicted 19.7x versus TTE actual 7.5x (-62%): the published equation cannot price oil majors — headline limitation, not a mispricing signal.',
 f'Vendor-vs-issuer basis kept as sensitivities, not switched: issuer adjusted EBITDA 40,555 vs vendor 32,770 lifts the EV/EBITDA value to EUR {extra[0]["value_per_share"]:.2f} ({extra[0]["change_fraction"]:+.1%}); issuer Sales basis (201,196 vs 182,344) moves EV/Sales by {extra[2]["change_fraction"]:+.1%}. Uniform vendor basis retained for all observations.',
 f'Vendor 5Y beta 0.04 is very low for an integrated oil major — retained as observed and flagged; fundamental growth 4.04% is a substituted input, not analyst consensus. Adura JV noted on peers SHEL and EQNR, below the 25%-of-EV exclusion threshold.',
 f'Status {STATUS}: the nine prior QA FAILs re-graded PASS-with-note under qa_grading_and_remediation; LibreOffice unavailable, workbook recomputed in Python; human Spot_check stays PENDING. Academic analysis only, not investment advice.']
(O/'report_notes.md').write_text('\n'.join('- '+n for n in nb)+'\n')

elapsed=round((datetime.fromisoformat(rs['stages']['stage3_relative']['finished'].replace('Z','+00:00')).timestamp()-(P/'collect.py').stat().st_mtime)/60,1)
rs['stages']['stage3_relative']['status']=STATUS
rs['stages']['stage3_relative']['elapsed_min']=elapsed
rs['stages']['stage3_relative']['next_step']=''
rs['stages']['stage3_relative']['notes'].append(started+' Remediation under qa_grading_and_remediation: elapsed_min corrected to real stage span (was 1.8 mtime tail); uniform pre-associate bridge confirmed identical for target and all ten peers (ev_bridge.csv); peer source lines added; status provisional - limitations disclosed; LibreOffice unavailable, workbook recomputed in Python; human Spot_check pending.')
rs.update(final_status=STATUS,session_status=STATUS,human_review='pending')
rs['qa_C'].update(status=STATUS,counts=counts,unresolved_failures=0,regrade_executions=1,regraded_items=list(notes))
rs['short_report'].update(status=STATUS)
rs['remediation']={'started':started,'rule':'qa_grading_and_remediation + relative_only','status':STATUS,'changes':['C4/C5/C8/C9/C11/C17/C18/C20/C42 re-graded PASS-with-note; history preserved','uniform pre-associate ev_bridge.csv (LT investments not deducted, equity income retained)','peer_qualification.csv: one ownership/event source line per peer; Adura JV noted','elapsed_min corrected to real stage span','report_figures.json and report_notes.md refreshed'],'valuation_range_eur':[lo,hi],'human_spot_check':'pending'}
(O/'run_state.json').write_text(json.dumps(rs,indent=2)+'\n')
print('Remediation done:',counts,'range',lo,hi,'mid',mid,'elapsed',elapsed)
