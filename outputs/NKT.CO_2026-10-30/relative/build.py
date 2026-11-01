"""NKT-only published-route valuation; arithmetic delegated to valuation_agent."""
import json,random,io
from pathlib import Path
import numpy as np
import pandas as pd
from openpyxl import Workbook
from valuation_agent import comparables as c,datasets,published_regressions as pr,regression
from valuation_agent.cachefetch import CachedFetcher

P=Path(__file__).resolve().parent;ROOT=P.parents[2]
D=pd.read_csv(P/'candidate_raw.csv').set_index('ticker',drop=False);T=D.loc['NKT'].copy()
FX=json.loads((ROOT/'cache/macro/2026-10-30.json').read_text())['fx_ecb_reference']['rates'];FX['EUR']=1

# NKT-specific: parent-common basis (hybrid coupon/principal stripped); vendor fields retained for peers.
NI_COMMON=264.0        # issuer NI 275 - hybrid coupon 11 (vendor 'Net Income to Common')
EQUITY_COMMON=2043.0   # issuer group equity 2193 - EUR 150m equity-classified hybrid (2022 issue)
HYBRID_CLAIM=150.0     # EUR m, equity-classified claim deducted once in the EV->common bridge
T['ni_val']=NI_COMMON; T['equity_val']=EQUITY_COMMON
# Vendor summary tables lack Pretax/Tax amounts; issuer annual report FY2025 (income statement).
T['pretax']=294.0; T['tax']=19.0  # effective 6.46%, one-off-driven - flagged in inputs/report

# World membership via cached URTH MSCI World proxy (iShares holdings CSV, dated header).
F=CachedFetcher(ROOT/'cache/web/2026-10-30',min_delay=1.1,user_agent='ValuationResearchAI/1.0 (educational AI research; robots compliant)')
world_url='https://www.ishares.com/us/products/239696/ishares-msci-world-etf/latest-holdings.csv'
body=F.get(world_url).text();lines=body.splitlines();start=next(i for i,l in enumerate(lines) if l.startswith('Ticker,Name,'))
world=pd.read_csv(io.StringIO('\n'.join(lines[start:])),on_bad_lines='skip').fillna('')
world=world[world['Asset Class'].eq('Equity')]
world[world.Ticker.isin(['ETN','GEV','5802','5801','ELHA'])].to_csv(P/'world_candidate_membership.csv',index=False)
world[world.Ticker.isin([t for t in D.index if t!='NKT'])].to_csv(P/'world_pool_membership.csv',index=False)

standard=set(D.index)-{'NKT'}
for t in D.index:
 if t=='NKT':continue
 if t in standard and D.loc[t,'europe']:
  D.loc[t,'membership']='IEUR MSCI Europe IMI proxy Oct29 (not standard index); entity/name matched'
 if t in world.Ticker.values:
  D.loc[t,'membership']='URTH MSCI World standard proxy, holdings 2026-10-29; entity/name+listing matched'

ISIN={'NKT':'DK0010287663','NEX':'FR0000044448','PRY':'IT0004176001','5802':'JP3407400005','5801':'JP3827200001','ELHA':'GRS282003003','ABBN':'CH0012221716','SU':'FR0000121972','LR':'FR0010307819','SIE':'DE0007236101','ENR':'DE000ENER6Y0','VWS':'DK0010268606','NDX1':'DE000A0D6554','ETN':'IE00B8KQN827','GEV':'US36828A1016','WRT1V':'FI0009003727','ANDR':'AT0000730007','IMI':'GB00BGLP8L22','ROR':'GB00BVFNZH21','SPX':'GB00BWFGQN14','SKF.B':'SE0000108227','SUN':'CH0038388911','ALFA':'SE0000695876','ATCO.A':'SE0011166610','SAND':'SE0000127891','METSO':'FI0009014572','WEIR':'GB0009465807','G1A':'DE0006602006','EPI.A':'SE0015658109','SMIN':'GB00B1WY2338','TKA':'DE0007500001'}
identity={
 'NKT':'https://investors.nkt.com/','NEX':'https://www.nexans.com/en/investors.html','PRY':'https://www.prysmiangroup.com/en/investors',
 '5802':'https://sumitomoelectric.com/ir','5801':'https://www.furukawa.co.jp/en/ir/','ELHA':'https://www.elvalhalcor.com/investor-relations/',
 'ABBN':'https://global.abb/group/en/investors','SU':'https://www.se.com/ww/en/about-us/investor-relations/','LR':'https://www.legrandgroup.com/en/finance',
 'SIE':'https://www.siemens.com/global/en/company/investor-relations.html','ENR':'https://www.siemens-energy.com/global/en/home/investor-relations.html',
 'VWS':'https://investor.vestas.com/','NDX1':'https://www.nordex-online.com/en/investor-relations/','ETN':'https://www.eaton.com/us/en-us/company/investor-relations.html',
 'GEV':'https://www.gevernova.com/investors','WRT1V':'https://www.wartsila.com/investors','ANDR':'https://www.andritz.com/group/en/investors',
 'IMI':'https://www.imiplc.com/investors','ROR':'https://www.rotork.com/en/investors','SPX':'https://www.spiraxgroup.com/investors',
 'SKF.B':'https://investors.skf.com/','SUN':'https://www.sulzer.com/en/investors','ALFA':'https://www.alfalaval.com/investors/',
 'ATCO.A':'https://www.atlascopcogroup.com/en/investors','SAND':'https://www.home.sandvik/en/investors/','METSO':'https://www.metso.com/investors/',
 'WEIR':'https://www.global.weir/investors/','G1A':'https://www.gea.com/en/investors/','EPI.A':'https://www.epiroc.com/en-in/investors',
 'SMIN':'https://www.smiths.com/investors','TKA':'https://www.thyssenkrupp.com/en/investors'}

# Event/ownership screens fixed before valuation; unknown evidence is never relabelled.
excluded={'ELHA':'emerging-market classification (Greece, MSCI EM) and non-IEUR/World membership unverified',
 'GEV':'GE spin-off Apr 2024 inside FY2024-25 comparison period; FY2025 NI includes one-off tax benefit (noncomparable)',
 'IMO':'n/a'}
del excluded['IMO']
for t,r in D.iterrows():
 if t=='NKT':continue
 if not r.europe and t not in world.Ticker.values:excluded.setdefault(t,'developed World membership not established')
 if abs(r.market_cap_check)>.02:excluded[t]=f'class capitalization reconciliation exceeds 2% ({100*r.market_cap_check:.3f}%)'
 if r.market_cap_eur_m<1000:excluded[t]='below EUR1bn'
 if r[list(c.WEIGHTS)].isna().sum()>2:excluded[t]='more than two missing score dimensions'
D['isin']=[ISIN.get(t,'not selected; not verified') for t in D.index]
pool=D.drop(index=['NKT',*excluded.keys()],errors='ignore').copy()
steps=[];sel=None
for label,use_world,b,cap in [('Europe',False,.1,2),('World',True,.1,2),('size',True,.05,2),('tier3',True,.05,4)]:
 x=pool[(pool.market_cap_eur_m>=T.market_cap_eur_m*b)&(pool.market_cap_eur_m<=T.market_cap_eur_m/b)]
 if not use_world:x=x[x.europe]
 scores,params=c.similarity_scores(x,T);x=x.join(scores)
 sel,info=c.select_peers(x,max_tier_3=cap)
 steps.append(dict(step=label,n_pool=len(x),band=[b,1/b],selection=info,scoring=params))
 if sel is not None:break
if sel is None:
 for n in [9,8]:
  sel,info=c.select_peers(x,n=n,max_tier_3=4)
  if sel is not None:break
assert sel is not None,'fewer than 8 feasible peers: blocked'
sel['target_ticker']='NKT.CO';sel['comp_ticker']=sel.ticker;sel['comp_name']=sel['name'];sel['comp_isin']=sel['isin']
sel['distance_score']=sel.distance;sel['effective_weight_coverage']=sel.weight_coverage;sel['market_cap_eur']=sel.market_cap_eur_m*1e6
sel['inclusion_reason']=sel.hypothesis;sel['source_route']='web_minimum';sel['metric_fallbacks']='fundamental growth, income-statement EBITDA, FY closing EV balances'
sel['identity_source']=[identity.get(t,'pending') for t in sel.ticker]
sel['flags']='DRAFT: human review pending; EV pre-LT-investments qualified only; NCI book proxy; beta benchmark/frequency unavailable; reported FY2025 uncalendarized; IFRS/US GAAP differences'
sel.to_csv(P/'comparables.csv',index=False)
D['gate_result']=[('target' if t=='NKT' else excluded.get(t,'numeric eligible; evidence review detailed in evidence_review.md')) for t in D.index]
D['selected']=D.index.isin(sel.index);D.to_csv(P/'candidate_gates.csv',index=False)
(P/'peer_selection.json').write_text(json.dumps(steps,indent=2,default=str)+'\n')

def value(name,m,metric=None):
 if not np.isfinite(m):return np.nan
 key={'pe':'ni_val','peg':'ni_val','pbv':'equity_val','ps':'sales','ev_ebit':'EBIT','ev_ebitda':'EBITDA','ev_cf':'cfo','ev_assets':'assets','ev_sales':'sales'}.get(name)
 if key is None:return np.nan
 if name=='peg':m*=100*T.growth
 base=T[key] if metric is None else metric
 if name.startswith('ev_'):
  eq=c.implied_equity_from_ev(m,base,T.debt,T.NCI,T.cash,0)-HYBRID_CLAIM  # hybrid claim once; peers unadjusted
 else:
  eq=m*base
 return eq/T.current_shares_m if eq>0 else np.nan  # EUR/share
summary=[]
for name in ['pe','peg','relative_pe','ev_ebit','ev_ebitda','ev_cf','pbv','ev_assets','tobins_q','ps','ev_sales']:
 vals=sel[name].where(sel[name]>0);stats=c.multiple_stats(vals,min_valid=6)
 driver={'pe':'growth','pbv':'roe','ps':'net_margin','ev_sales':'ebitda_margin'}.get(name)
 adj=c.scaled_multiple(vals,sel[driver],T[driver],driver_scale=100 if name=='pe' else 1,min_valid=6) if driver else dict(available=False,n_valid=0)
 chosen=adj if adj['available'] else stats
 row=dict(target_ticker='NKT.CO',multiple=name,**stats,adjusted_multiple=adj.get('median',np.nan),adjusted_n_valid=adj['n_valid'],currency='EUR',basis='FY2025',is_primary=name=='pe',status='draft qualified cross-check' if name.startswith('ev_') else 'draft' if stats['usable'] else 'unavailable',flags='EV before LT-investment perimeter + EUR150m hybrid claim: qualified only; supplemental' if name.startswith('ev_') else 'matching index PE unavailable' if name=='relative_pe' else 'replacement costs unavailable' if name=='tobins_q' else 'hybrid-adjusted NI/common equity basis' if name in ('pe','peg','pbv') else '')
 for q,s in [('p25','low'),('median','mid'),('p75','high')]:
  row['value_per_share_'+s]=value(name,chosen.get(q,np.nan)) if stats['usable'] else np.nan
  row['raw_value_'+s]=value(name,stats.get(q,np.nan)) if stats['usable'] else np.nan
  row['adjusted_'+q]=adj.get(q,np.nan)
 row['upside']=row['value_per_share_mid']/T.price-1
 summary.append(row)
S=pd.DataFrame(summary)
S['n_valid_adjusted']=S.adjusted_n_valid;S['valuation_status']=S.status
S['selected_basis']=['scaled' if n>=6 else 'raw' for n in S.adjusted_n_valid]
for suffix,qq in [('low','p25'),('mid','median'),('high','p75')]:
 S['unadjusted_value_'+suffix]=S['raw_value_'+suffix]
 S['adjusted_value_'+suffix]=[value(row.multiple,row['adjusted_'+qq]) for _,row in S.iterrows()]
S.to_csv(P/'multiples_summary.csv',index=False);primary=S[S.is_primary].iloc[0]

def sheet(wb,name,frame):
 w=wb.create_sheet(name);w.append(list(map(str,frame.columns)))
 for row in frame.itertuples(index=False,name=None):w.append([None if pd.isna(v) else v.item() if isinstance(v,np.generic) else v for v in row])
 w.freeze_panes='A2';w.auto_filter.ref=w.dimensions
 return w
wb=Workbook();wb.remove(wb.active)
sheet(wb,'Candidate_Pool',D.reset_index(drop=True));sheet(wb,'Peer_Scores',x.reset_index(drop=True));sheet(wb,'Peer_Selection',sel.reset_index(drop=True));sheet(wb,'Peer_Multiples',S)
spot=[]
for t in sorted(random.Random(20261030).sample(list(sel.ticker),3)):
 r=sel.loc[t];m=r.market_cap_quote_m*FX[r.report_currency]/FX[r.quote_currency]
 ev=c.comparable_ev(m,r.debt,r.NCI,r.cash,0) if np.isfinite(r.NCI) else np.nan
 spot.append(dict(ticker=t,market_equity_report_m=m,debt=r.debt,nci=r.NCI,cash=r.cash,associates='unavailable; zero only in pre-investment sensitivity',EV_before_associates=ev,stored=r.EV_before_associates,arithmetic_delta=ev-r.EV_before_associates,source=r.source_urls,automated_check='PASS' if np.isfinite(ev) and abs(ev-r.EV_before_associates)<1e-8 else 'UNAVAILABLE',human_review='pending, not performed or waived'))
sheet(wb,'Peer_Spot_check',pd.DataFrame(spot));pd.DataFrame(spot).to_csv(P/'peer_ev_checks.csv',index=False)
dims=list(c.WEIGHTS);par=wb.create_sheet('Score_Params');par.append(['dimension','P05','P95','winsor mean','sample SD','weight','target raw z'])
live=wb.create_sheet('Score_Live');live.append(['ticker',*dims,*['winsor_'+d for d in dims],*['z_'+d for d in dims],'distance'])
from openpyxl.utils import get_column_letter as col
for i,(_,r) in enumerate(x.iterrows(),2):
 live.append([r.ticker,*[float(r[d]) if np.isfinite(r[d]) else None for d in dims]])
 for j,d in enumerate(dims):
  raw=col(j+2);win=col(j+10);z=col(j+18);pi=j+2
  live[f'{win}{i}']=f'=IF(ISNUMBER({raw}{i}),MIN(MAX({raw}{i},Score_Params!B{pi}),Score_Params!C{pi}),"")'
  live[f'{z}{i}']=f'=IF(ISNUMBER({win}{i}),({win}{i}-Score_Params!D{pi})/Score_Params!E{pi},"")'
 live[f'Z{i}']='=IFERROR(SQRT('+ '+'.join(f'{c.WEIGHTS[d]}*({col(j+18)}{i}-Score_Params!G{j+2})^2' for j,d in enumerate(dims))+'),"")'
for j,d in enumerate(dims):
 raw=col(j+2);win=col(j+10);pi=j+2;end=len(x)+1
 par.append([d,f'=PERCENTILE(Score_Live!{raw}2:{raw}{end},0.05)',f'=PERCENTILE(Score_Live!{raw}2:{raw}{end},0.95)',f'=AVERAGE(Score_Live!{win}2:{win}{end})',f'=STDEV(Score_Live!{win}2:{win}{end})',c.WEIGHTS[d],f'=({T[d]}-D{pi})/E{pi}'])
qa=wb.create_sheet('QA');qa.append(['Status','Details']);qa.append(['DRAFT','Human Spot_check pending. EV investment/lease harmonization incomplete; see qa_results.md.'])
wb.save(P/'comparables_audit.xlsx')

# Published-route regression inputs (approved fundamental growth substitution, closing ROE).
closing_roe=T.ni_val/T.equity_val;payout_reg=min(T.payout,1) if T.payout>=0 else np.nan
geps=closing_roe*(1-payout_reg) if closing_roe>0 else np.nan;tax=T.tax/T.pretax
beta_rep,beta_replaced,beta_note=regression.replace_beta(T.beta,1.01,0.22,T.debt/T.market_cap_quote_m)
inputs={'g_eps':geps,'beta':beta_rep,'roe':closing_roe,'payout':payout_reg,'g_rev':geps,'dfr':T.debt/(T.debt+T.market_cap_quote_m*FX[T.report_currency]/FX[T.quote_currency]),'tax_rate':tax,'roic':T.EBIT*(1-tax)/(T.equity+T.debt-T.cash)}
reg_wb=Workbook();w=reg_wb.active;w.title='Inputs';w.append(['Variable','value','definition/source'])
for k,v in inputs.items():w.append([k,float(v),'approved fundamental growth substitution, closing parent-common ROE x retention; g_rev uses g_eps fallback' if k in ['g_eps','g_rev'] else ('observed 5Y beta 0.65 within bounds, kept; fallback beta_u 1.01 cash-corrected Electrical Equipment EUROPE, marginal 22%, market D/E' if k=='beta' else 'vendor FY2025; see relative_inputs.md and source_log.csv')])
for k in ['equity','ni','EBITDA','debt','NCI','cash','current_shares_m']:w.append([k,float(T[k]),'S3_NKT_'+k])
w.append(['equity_val',float(T['equity_val']),'S3_NKT_equity_val (common equity, hybrid claim stripped)'])
w.append(['ni_val',float(T['ni_val']),'S3_NKT_ni_val (NI to common, hybrid coupon stripped)'])
eqws=reg_wb.create_sheet('Equations');eqws.append(['model','constant','terms','predicted','published R2','EUR/share','dataset','actual','actual/predicted - 1'])
preds=[];checks=[]
for i,dep in enumerate(['PE','PBV','EV/EBITDA'],2):
 eq,res,region=datasets.equation_for('Denmark',dep,'2026-10-30');findings=datasets.check_dataset(res.dataset);checks.append(dict(dataset=res.dataset.dataset_id,findings=[vars(f) for f in findings]))
 assert not any(f.severity=='error' for f in findings)
 pv=pr.predict(eq,inputs,unit_policy='as_published_note');both=pr.predict_both_policies(eq,inputs)
 formula='='+str(eq.constant)
 for term in eq.terms:
  ri=list(inputs).index(term.variable)+2;formula+=f'+({term.coef})*'+(f'LN(Inputs!B{ri})' if term.transform=='ln' else f'Inputs!B{ri}')
 actual={'PE':T.pe,'PBV':T.pbv,'EV/EBITDA':T.ev_ebitda}[dep]
 priceformula=f'=D{i}*Inputs!B18/Inputs!B16' if dep=='PE' else f'=D{i}*Inputs!B17/Inputs!B16' if dep=='PBV' else f'=(D{i}*Inputs!B12-Inputs!B13-Inputs!B14+Inputs!B15-{HYBRID_CLAIM})/Inputs!B16'
 eqws.append([dep,eq.constant,str([(a.variable,a.coef) for a in eq.terms]),formula,eq.r2,priceformula,res.dataset.dataset_id,float(actual),f'=H{i}/D{i}-1'])
 def val(dep,m):
  if dep=='PE':eqv=m*T.ni_val
  elif dep=='PBV':eqv=m*T.equity_val
  else:eqv=c.implied_equity_from_ev(m,T.EBITDA,T.debt,T.NCI,T.cash,0)-HYBRID_CLAIM
  return eqv/T.current_shares_m
 sh=val(dep,pv)
 preds.append(dict(model=dep,predicted=pv,published_r2=eq.r2,value_per_share=sh,actual=actual,actual_predicted_gap=actual/pv-1,unit_alternative=both,equation=eq.raw,dataset=res.dataset.dataset_id,sha256=res.dataset.sha256,as_of=res.dataset.as_of_date,region=region,match_level=res.match_level,warnings=res.warnings))
 co=reg_wb.create_sheet('Coefficients_'+dep.replace('/','_'));co.append(['term','coefficient','t statistic','dataset','sha256']);co.append(['constant',eq.constant,eq.constant_tstat,res.dataset.dataset_id,res.dataset.sha256])
 for term in eq.terms:co.append([term.variable,term.coef,term.tstat,res.dataset.dataset_id,res.dataset.sha256])
reg_wb.save(P/'regression_valuation.xlsx');chosen=max(preds,key=lambda v:v['published_r2'])
regresult=dict(inputs=inputs,beta_note=beta_note,predictions=preds,chosen=chosen['model'],substituted_input='approved fundamental g_eps and g_rev fallback (not analyst consensus); published ROE closing parent-common equity (hybrid stripped), peer-score ROE average equity',status='draft pending human review',dataset_checks=checks)
(P/'regression_results.json').write_text(json.dumps(regresult,indent=2,default=str)+'\n')
row=dict(company='NKT A/S',ticker='NKT.CO',isin='DK0010287663',gics_sector='not independently verified; internal bucket D not GICS',typicality_result='n/a_published_route',primary_regression='published_damodaran_EUROPE_2026-01',chosen_model=chosen['model'],predicted_primary=chosen['predicted'],actual_multiple=chosen['actual'],published_r2=chosen['published_r2'],implied_value_per_share=chosen['value_per_share'],current_price=T.price,upside=chosen['value_per_share']/T.price-1,classification='Not classified (no SEy published)',units_policy='as_published_note; decimal approved',units_unverified='no; alternative policy disclosed',substituted_input=regresult['substituted_input'],rationale=f"{chosen['model']} highest published R2; beta kept ({beta_note}); hybrid EUR150m stripped from NI/equity for parent-common basis; FY2025 effective tax 6.46% one-off-driven - flagged.",source_urls=T.source_urls)
for k in ['failed_test','adj_r2','predicted_A','predicted_B','predicted_C','residual','std_residual','damodaran_predicted','sector_dummy_coef']:row[k]='n/a_published_route'
for i,p in enumerate([p for p in preds if p is not chosen],2):row[f'alternative_{i}_model']=p['model'];row[f'alternative_{i}_prediction']=p['predicted']
pd.DataFrame([row]).to_csv(P/'valuation_multiples.csv',index=False)

bench=[]
for fam in ['evebitda_industry','pbv_industry']:
 rr=datasets.resolve(fam,country='Denmark',valuation_date='2026-10-30');fr=datasets.load_industry(rr.dataset)
 for ind in ['Electrical Equipment','Machinery','Engineering & Construction','Industrial Services']:
  try:br=datasets.industry_row(fr,ind)
  except Exception:continue
  bench.append(dict(family=fam,industry=ind,values=br.to_dict(),dataset=rr.dataset.dataset_id,sha256=rr.dataset.sha256,as_of=rr.dataset.as_of_date,identity='published industry ratio; NOT verified median'))
(P/'industry_benchmarks.json').write_text(json.dumps(bench,indent=2,default=str)+'\n')

from valuation_agent.sourcelog import SourceLog
log=SourceLog(P/'source_log.csv');log.rows=[]
for _,r in D.iterrows():
 for k in ['price','current_shares_m','market_cap_quote_m','ni','sales','EBIT','DA','EBITDA','equity','equity_prior','debt','cash','NCI','associates','assets','payout','beta','growth','roe','capex','cfo','pretax','tax']:
  v=r[k];der=k in ['growth','roe','payout']
  base=r.source_urls.split('financials/')[0]
  suffix='history/' if k=='price' else 'statistics/' if k in ['beta','current_shares_m','market_cap_quote_m'] else 'financials/balance-sheet/' if k in ['equity','equity_prior','debt','cash','NCI','associates','assets'] else 'financials/cash-flow-statement/' if k in ['cfo','capex'] else 'financials/income-statement/'
  location=r.source_urls if der else base+suffix
  log.add(input_id=f'S3_{r.ticker}_{k}',company=r['name'],metric=k,value='n/a' if pd.isna(v) else str(v),unit='ratio' if k in ['growth','roe','payout','beta'] else 'currency/share' if k=='price' else 'millions',currency='n/a' if k in ['current_shares_m','growth','roe','payout','beta'] else r.quote_currency if k in ['price','market_cap_quote_m'] else r.report_currency,as_of_date='2026-10-30',access_date='2026-11-01',period_end=r.financial_period_end if k not in ['price','current_shares_m','market_cap_quote_m','beta'] else 'n/a',source_name='StockAnalysis uniform raw fields',url_or_local_file=location,page_note_sheet_cell='candidate_raw.csv '+r.ticker+':'+k,reported_or_adjusted='derived' if der else 'reported',consolidation_scope='parent NI/equity; consolidated operating fields',method_or_formula='normalize.py; uniform FY2025 income-statement EBITDA; average equity for peers, closing parent-common equity (hybrid stripped) for published regression',status='unavailable' if pd.isna(v) else 'derived' if der else 'sourced',limitation='FY balance; EV pre-LT-investments only; shares/current FY EPS not substituted',entity_id=r.ticker,price_date=r.price_date,review_status='pending human review')
for b in [*bench,dict(dataset=preds[0]['dataset'],sha256=preds[0]['sha256'],as_of=preds[0]['as_of'],family='regressions',industry='EUROPE PE/PBV/EVEBITDA')]:
 log.add(input_id='dataset_'+b['dataset']+'_'+b['industry'],company='NKT A/S',metric=b['family'],value=b['industry'],unit='equation or published industry ratio',as_of_date=b['as_of'],access_date='2026-11-01',source_name='registered Damodaran data library',url_or_local_file='data registry '+b['dataset'],dataset_vintage='2026-01',page_note_sheet_cell='industry_benchmarks.json or Coefficients sheets',status='sourced',limitation='sha256 '+b['sha256']+'; industry ratio not verified median')
log.save()

sens=[]
for loo in sel.index:
 a=sel.drop(index=loo);ad=c.scaled_multiple(a.pe,a.growth,T.growth,driver_scale=100,min_valid=6)
 sens.append(dict(sensitivity='leave-one-out selected peer',removed=loo,value_per_share=value('pe',ad['median']),n_valid=ad['n_valid']))
for lbl,mult_name in [('target group NI 275 (vs parent-common 264; hybrid not stripped)','pe'),('target EBITDA issuer operational 390 (vs vendor 680 uniform basis)','ev_ebitda'),('target EBIT issuer 257 (vs vendor 578 uniform basis)','ev_ebit')]:
 if mult_name=='pe':
  m=S[S.multiple.eq('pe')].iloc[0]['median'];sens.append(dict(sensitivity=lbl,value_per_share=(m*275-0)/T.current_shares_m))
 else:
  alt={'ev_ebitda':390.0,'ev_ebit':257.0}[mult_name]
  m=S[S.multiple.eq(mult_name)].iloc[0]['median'];sens.append(dict(sensitivity=lbl,value_per_share=value(mult_name,m,alt)))
pd.DataFrame(sens).to_csv(P/'sensitivities.csv',index=False)
warnings='DRAFT pending human Spot_check. Primary PE per bucket-D electrical-equipment/cables mapping; hybrid EUR150m stripped from NI-to-common (264) and book common equity (2,043) for the parent-common basis - flagged. Dominant divergence: vendor uniform EBIT 578/EBITDA 680 vs issuer EBIT 257/operational EBITDA 390 (vendor routes -272 metal-price/hedge/other below EBIT; pretax 294 exact) - EV cross-checks qualified only, issuer-basis sensitivities shown. Peer EV uses cash&ST-investments and book NCI with no associate/LT-investment harmonization - qualified. FY2025 effective tax 6.46% is one-off-driven; vendor 5Y betas across the pool carry benchmark/frequency unavailable flag. No DCF, recommendation, synthesis weight or residual-band classification.'
(P/'comparables_report.md').write_text('# NKT comparables - 2026-10-30\n\n'+warnings+'\n\n## Selection\nInitial pool '+str(len(D)-1)+' candidates, Europe-first. Ordered expansion and final constraints in peer_selection.json. Peer scores use eight required weights, pool-only 5/95 clipping and STDEV.S; fundamental growth across target/pool before exclusions. Exact constrained minimum-distance library selection.\n\n'+sel[['ticker','tier','distance','country','financial_period_end','inclusion_reason']].to_markdown(index=False)+'\n\n## Primary and raw/scaled values\n'+S.to_markdown(index=False)+'\n\n## Bridge and fiscal bases\nFY2025 financials at each actual fiscal end (Japan candidates March-end, flagged). Quote prices/cap at 2026-10-30; FX ECB same date (DKK 7.4735; peer conversions via ECB 2026-10-30 rates). EV numerator uses debt incl. leases + NCI book - cash&ST investments; LT investments excluded and flagged (NKT EUR 10m; immaterial). EV-to-common-equity inverts the same construction and removes the EUR 150m equity-classified hybrid claim once. EV/CF uses reported CFO - unlevered/IFRS-vs-GAAP interest differences remain. Target NI/equity use parent-common basis (264 / 2,043) after stripping the hybrid coupon 11 and claim 150.\n\n## Sensitivities\nRaw/scaled p25/median/p75 are peer dispersion, not confidence intervals. Leave-one-out, group-NI, issuer EBITDA 390 and issuer EBIT 257 diagnostics in sensitivities.csv. Vendor betas carry a benchmark/frequency-unavailable flag; distance is driven mainly by size/leverage/margins.\n\n## Benchmarks\nElectrical Equipment / Machinery EUROPE published ratios in industry_benchmarks.json are NOT verified medians; gap checks in qa_results.md. Peer medians versus closest published industry ratios recorded, not "fixed" to match.\n\n## Sources and audit\nCandidate field-level sources in source_log.csv, official identity links in comparables.csv, selection logs and live scores in comparables_audit.xlsx. Three seeded EV arithmetic rows in Peer_Spot_check; human review explicitly pending.\n')
(P/'valuation_summary.md').write_text('# Relative valuation by regression - Europe, NKT.CO, 2026-10-30\n\n## Headline\nDraft '+chosen['model']+' selected by highest eligible published R2 ('+f"{chosen['published_r2']:.3f}"+'), a weaker heuristic rather than adjusted-R2/industry fit.\n\n## Data\nFY2025 uniform vendor inputs cross-checked with issuer annual report. Denmark listing resolves EUROPE exact. Fundamental growth uses closing parent-common ROE '+f"{closing_roe:.4f}"+' x capped retention, explicitly approved substitution for unavailable matching 5Y analyst growth; vendor 5Y beta 0.65 kept (within 0-2.5); no replacement needed.\n\n## Fitted model\n'+pd.DataFrame(preds)[['model','predicted','published_r2','value_per_share','actual','actual_predicted_gap']].to_markdown(index=False)+'\n\n## Diagnostics\nIntegrity findings retained in regression_results.json. GLOBAL PEG/PBV and EM EVEBITDA source anomalies do not affect these EUROPE equations. No n, SEy, adjusted R2, p-values, A/B/C, typicality or D1-D10 available: n/a_published_route. Classification: Not classified (no SEy published).\n\n## Valuation results (sorted from most undervalued to most overvalued)\n'+pd.DataFrame(preds).sort_values('value_per_share',ascending=False)[['model','value_per_share']].to_markdown(index=False)+'\n\n## Robustness\nAll units decimal as approved; EVEBITDA alternative percentage-point DFR/tax prediction saved. Live predictions and price bridges reference Inputs; recalculation validation follows in formula_checks.json. Published EV definition undocumented; hybrid EUR150m removed once from the EV->common bridge.\n\n## Key warnings\n'+warnings+'\n\n## Limitations\nMarket-wide, low-R2 equations not sector fair-value proof. January 2026 vintage ~302 days old at valuation date. File requires analyst 5Y growth, not our substituted sustainable growth; beta benchmark/frequency unspecified for peers. NKT effective tax 6.46% one-off-driven and vendor EBIT basis differs from issuer (578 vs 257) - flagged, not analyst consensus.\n')
print(json.dumps(dict(peers=sel.ticker.tolist(),excluded=excluded,primary_PE=float(primary.value_per_share_mid),regression=chosen),default=str,indent=2))
