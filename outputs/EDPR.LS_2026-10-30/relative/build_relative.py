"""Company-local, reproducible provisional analysis for EDPR.LS. Never changes source-library code."""
import json, math, random
from pathlib import Path
import numpy as np
import pandas as pd
from openpyxl import Workbook
from openpyxl.utils import get_column_letter as col
from valuation_agent import comparables as c, datasets, published_regressions as pr
from valuation_agent.sourcelog import SourceLog

P=Path(__file__).resolve().parent
ROOT=P.parents[2]
D=pd.read_csv(P/'candidate_raw.csv').set_index('ticker',drop=False)
D['period_end']=pd.to_datetime(D.financial_period_end.astype(str).str.extract(r'([A-Z][a-z]{2} \d{1,2}, \d{4})',expand=False),format='%b %d, %Y').dt.strftime('%Y-%m-%d')
D['period_start']=(pd.to_datetime(D.period_end)-pd.DateOffset(years=1)+pd.Timedelta(days=1)).dt.strftime('%Y-%m-%d')
T=D.loc['EDPR']

ISINS={'EDPR':'ES0127797019','ORSTED':'DK0060094928','ANE':'ES0105563003','ERG':'IT0001157020',
 'SLR':'ES0165386014','GRE':'ES0105079000','SCATC':'NO0010715139','EKT':'DE0005313506',
 'PNE3':'DE000A0JBPG2','OX2':'SE0016070547','AY':'US19508P1075','BEPC':'US16984A1051',
 'CWEN':'US18539C1053','ORA':'US6866881021','BLX':'CA09950M1032','NPI':'CA6665111002',
 'INE':'CA45790E1043','IBE':'ES0144580Y14','ENEL':'IT0003128367','SSE':'GB0007908733',
 'ENGI':'FR0010208488','VER':'AT0000746409','RWE':'DE0007037129','FORTUM':'FI0009007132',
 'DRX':'GB00B1VNSX38','EOAN':'DE000ENAG999','ELE':'ES0130670112','NTGY':'ES0116870314',
 'CNA':'GB00B033F229','A2A':'IT0001233417','IREN':'IT0003027817','HERA':'IT0001250932',
 'NEOEN':'FR0011675362','EDP':'PTEDP0AM0009'}
# Gates fixed before any valuation. EDP is the ~71% parent: hard exclusion.
reasons={
 'EDP':'hard exclusion: parent of EDPR (~71% ownership), comparables procedure section 3',
 'NEOEN':'uniform web source unavailable (404); no per-row source switching',
 'OX2':'uniform web source unavailable (404); no per-row source switching',
 'IREN':'uniform web source unavailable (404); no per-row source switching',
 'HERA':'uniform web source unavailable (404); no per-row source switching',
 'EKT':'market cap EUR0.33bn below EUR1bn minimum',
 'PNE3':'market cap EUR0.42bn below EUR1bn minimum',
 'AY':'no common 2026-10-30 price date (vendor history gap); freshness gate fails',
 'BLX':'no common 2026-10-30 price date (vendor history gap); freshness gate fails',
 'INE':'no common 2026-10-30 price date (vendor history gap); freshness gate fails',
 'ORA':'membership mislabeled by name match; US listed, kept for World relaxation only',
}
pool=D.loc[[t for t in D.index if t not in ('EDPR',)+tuple(reasons)]].copy()
pool['isin']=[ISINS.get(t,'unverified') for t in pool.index]
pool['europe']=pool.europe.astype(bool)
assert (pool.market_cap_check.abs()<=.05).all(), 'cap checks beyond flag threshold need review'
assert (pool.market_cap_eur_m>=1000).all()
assert (pool[list(c.WEIGHTS)].isna().sum(axis=1)<=2).all()
steps=[];sel=None;x=None
for label,world,band,cap in [('Europe',False,.1,2),('World',True,.1,2),('size',True,.05,2),('tier3',True,.05,4)]:
 x=pool[(pool.market_cap_eur_m>=T.market_cap_eur_m*band)&(pool.market_cap_eur_m<=T.market_cap_eur_m/band)]
 if not world:x=x[x.europe]
 scores,log=c.similarity_scores(x,T)
 x=x.join(scores)
 sel,info=c.select_peers(x,max_tier_3=cap)
 steps.append({'step':label,'n_pool':len(x),'selection':info,'scoring':log})
 if sel is not None:break
if sel is None:
 for n in [9,8]:
  sel,info=c.select_peers(x,n=n,max_tier_3=4)
  if sel is not None:break
assert sel is not None
sel['target_ticker']='EDPR.LS'
sel['comp_name']=sel.name
sel['comp_ticker']=sel.ticker
sel['comp_isin']=sel['isin']
sel['distance_score']=sel.distance
sel['market_cap_eur']=sel.market_cap_eur_m*1e6
sel['inclusion_reason']=sel.hypothesis
sel['flags']='provisional ownership/events/classification audit; human Spot_check pending; associates proxied by long-term investments where present; non-Dec periods uncalendarized; beta benchmark/frequency unavailable; ISINs registry-mapped pending issuer verification'
sel.to_csv(P/'comparables.csv',index=False)
json.dump(steps,open(P/'peer_selection.json','w'),indent=2,default=str)
candidate=D.copy();candidate['gate_result']=[reasons.get(t,'preliminary eligible; audit pending') if t!='EDPR' else 'target' for t in candidate.index]
candidate['isin']=[ISINS.get(t,'unverified') for t in candidate.index]
candidate.to_csv(P/'candidate_gates.csv',index=False)

# EV bridge: vendor 'Total Debt' (gross incl. ST; leases not split) + NCI - cash - associates proxy (Long-Term Investments); uniform across pool.
def price(multiple, val):
 if not np.isfinite(val):return np.nan
 metric={'pe':'ni','peg':'ni','pbv':'equity','ps':'sales','ev_ebit':'EBIT','ev_ebitda':'EBITDA','ev_cf':'cfo','ev_assets':'assets','ev_sales':'sales'}.get(multiple)
 if not metric:return np.nan
 if multiple=='peg':val*=100*T.growth
 equity=c.implied_equity_from_ev(val,T[metric],T.debt,T.NCI,T.cash,0) if multiple.startswith('ev_') else val*T[metric]
 return equity/T.current_shares_m if equity>0 else np.nan

rows=[]
for name in ['pe','peg','relative_pe','ev_ebit','ev_ebitda','ev_cf','pbv','ev_assets','tobins_q','ps','ev_sales']:
 vals=sel[name].where(sel[name]>0)
 stats=c.multiple_stats(vals,min_valid=6)
 driver={'pe':'growth','pbv':'roe','ps':'net_margin','ev_sales':'ebitda_margin'}.get(name)
 adj=c.scaled_multiple(vals,sel[driver],T[driver],driver_scale=100 if name=='pe' else 1,min_valid=6) if driver else {'available':False,'n_valid':0}
 base=adj if adj['available'] else stats
 usable=stats['usable']
 row={'target_ticker':'EDPR.LS','multiple':name,**stats,'adjusted_multiple':adj.get('median',np.nan),'adjusted_n_valid':adj['n_valid'],'currency':'EUR','is_primary':name=='ev_ebitda','basis':'FY2025','status':'provisional' if usable else 'not valued (<6 valid or unsupported denominator)','flags':'EV before associates for peers (LT investments proxied for target); not fully harmonized' if name.startswith('ev_') else 'relative PE/index denominator unavailable' if name=='relative_pe' else 'replacement costs unavailable' if name=='tobins_q' else ''}
 for q,suffix in [('p25','low'),('median','mid'),('p75','high')]:
  row['value_per_share_'+suffix]=price(name,base.get(q,np.nan)) if usable else np.nan
  row['raw_value_'+suffix]=price(name,stats.get(q,np.nan)) if usable else np.nan
 rows.append(row)
summary=pd.DataFrame(rows);summary.to_csv(P/'multiples_summary.csv',index=False)
primary=summary[summary.multiple.eq('ev_ebitda')].iloc[0]

def add_frame(wb,name,frame):
 ws=wb.create_sheet(name);ws.append([str(k) for k in frame.columns])
 for r in frame.itertuples(index=False,name=None):
  ws.append([None if pd.isna(v) else v.item() if isinstance(v,np.generic) else v for v in r])
 ws.freeze_panes='A2';ws.auto_filter.ref=ws.dimensions
 return ws
wb=Workbook();wb.remove(wb.active)
add_frame(wb,'Candidate_Pool',candidate.reset_index(drop=True))
add_frame(wb,'Peer_Scores',x.reset_index(drop=True))
dims=list(c.WEIGHTS)
add_frame(wb,'Peer_Selection',sel.reset_index(drop=True))
add_frame(wb,'Peer_Multiples',summary)
add_frame(wb,'Peer_Spot_check',pd.DataFrame({'ticker':sorted(random.Random(20261030).sample(list(sel.ticker),min(3,len(sel)))),'review_status':'pending human review; no assertion of verification'}))
# EV recomputation evidence: three reproducibly random selected peers, EV before associates.
checks=[]
for t in sorted(random.Random(20261030).sample(list(sel.ticker),min(3,len(sel)))):
 r=sel[sel.ticker.eq(t)].iloc[0];raw=r.pe*r.ni if np.isfinite(r.ni) and r.ni>0 else r.market_cap_eur_m
 ev=c.comparable_ev(r.pe*r.ni if np.isfinite(r.ni) and r.ni>0 else np.nan,r.debt,r.NCI,r.cash,0)
 checks.append(dict(ticker=t,debt=r.debt,NCI=r.NCI,cash=r.cash,EV_before_associates=ev,recorded=r.EV_before_associates,recompute_match=bool(np.isfinite(ev) and np.isfinite(r.EV_before_associates) and abs(ev-r.EV_before_associates)<1e-6*max(1,abs(r.EV_before_associates))),human_status='pending; not performed'))
add_frame(wb,'EV_check',pd.DataFrame(checks))
qa=wb.create_sheet('QA');qa.append(['Status','Evidence']);qa.append(['PROVISIONAL','Ownership/events/classification audit incomplete; industry median check pending; human review pending'])
wb.save(P/'comparables_audit.xlsx')

# Published FY regressions — Portugal lists EUROPE equations via resolver.
tax_rate=T.tax_rate  # 0.3537 effective FY2025
mkt_eq=T.market_cap_quote_m  # EUR m, Oct-30 close basis
dfr=T.debt/(T.debt+mkt_eq)
ic=T.equity+T.debt-T.cash
roic=T.EBIT*(1-tax_rate)/ic
inputs={'g_eps':float(T.g_eps),'beta':float(T.beta),'roe':T.ni/T.equity,'payout':132.09152640/215.8,'g_rev':float(T.g_rev),'dfr':dfr,'tax_rate':tax_rate,'roic':roic}
g_eps_source='analyst consensus 3Y EPS growth forecast 20.42% (stockanalysis statistics, accessed 2026-11-01)'
g_rev_source='analyst consensus 3Y revenue growth forecast 8.51% (same source)'
reg=Workbook();ws=reg.active;ws.title='Inputs';ws.append(['Variable','value','source'])
for k,v in inputs.items():
 src={'g_eps':g_eps_source,'g_rev':g_rev_source,'beta':'StockAnalysis Beta(5Y) 0.72','roe':'NI/parent common equity FY2025 (closing)','payout':'proposed scrip dividend 132.09m / reported NI 215.8m = 0.61 (0.40 on recurring NP); paid-cash 3m basis flagged','dfr':'total debt/(debt+market equity) at 2026-10-30','tax_rate':'FY2025 effective 35.37%','roic':'EBIT(1-tax)/(equity+debt-cash)'}[k]
 ws.append([k,float(v),src])
ws.append(['book',T.equity,'S3_EDPR_equity']);ws.append(['NI',T.ni,'S3_EDPR_ni']);ws.append(['EBITDA',T.EBITDA,'S3_EDPR_EBITDA']);ws.append(['debt',T.debt,'S3_EDPR_debt']);ws.append(['NCI',T.NCI,'S3_EDPR_NCI']);ws.append(['cash',T.cash,'S3_EDPR_cash']);ws.append(['associates',T.associates,'S3_EDPR_assoc']);ws.append(['shares',T.current_shares_m,'S3_EDPR_current_shares_m'])
preds=[];eqws=reg.create_sheet('Equations');eqws.append(['Model','constant','pred_terms','predicted','published R2','EUR/share','dataset'])
for i,dep in enumerate(['PE','PBV','EV/EBITDA'],2):
 eq,res,region=datasets.equation_for('Portugal',dep,'2026-10-30')
 check=datasets.check_dataset(res.dataset)
 value=pr.predict(eq,inputs,unit_policy='as_published_note')
 inrow={k:i2 for i2,k in enumerate(inputs.keys(),2)}
 formula='='+str(eq.constant)
 for term in eq.terms:
  if term.variable in inrow:formula+=f'+{term.coef}*Inputs!B{inrow[term.variable]}'
 eqws.append([dep,eq.constant,str([(t.variable,t.coef) for t in eq.terms]),formula,eq.r2,None,res.dataset.dataset_id])
 if dep=='PE': eqv=value*T.ni; share=eqv/T.current_shares_m
 elif dep=='PBV': eqv=value*T.equity; share=eqv/T.current_shares_m
 else:
  eqv=c.implied_equity_from_ev(value,T.EBITDA,T.debt,T.NCI,T.cash,0);share=eqv/T.current_shares_m if eqv>0 else np.nan
 eqws.cell(row=i,column=6).value=share
 both=pr.predict_both_policies(eq,inputs)
 preds.append({'model':dep,'predicted':value,'published_r2':eq.r2,'value_per_share':share,'actual':{'PE':T.pe,'PBV':T.pbv,'EV/EBITDA':T.ev_ebitda}[dep],'deviation':({'PE':T.pe,'PBV':T.pbv,'EV/EBITDA':T.ev_ebitda}[dep]/value-1) if value>0 and np.isfinite({'PE':T.pe,'PBV':T.pbv,'EV/EBITDA':T.ev_ebitda}[dep]) else None,'unit_alternative':both,'equation':eq.raw,'dataset':res.dataset.dataset_id,'region':region,'integrity':[f.message for f in check]})
 cs=reg.create_sheet('Coefficients_'+dep.replace('/','_'));cs.append(['Term','coefficient','published t statistic','dataset','as_of','sha256'])
 cs.append(['constant',eq.constant,eq.constant_tstat,res.dataset.dataset_id,str(res.dataset.as_of_date),res.dataset.sha256])
 for term in eq.terms:cs.append([term.variable,term.coef,term.tstat,res.dataset.dataset_id,str(res.dataset.as_of_date),res.dataset.sha256])
 dataset_res=res
reg.save(P/'regression_valuation.xlsx')
json.dump({'inputs':inputs,'predictions':preds,'status':'provisional'},open(P/'regression_results.json','w'),indent=2,default=str)
chosen=max(preds,key=lambda p:p['published_r2'])
r={'company':'EDP Renovaveis','ticker':'EDPR.LS','isin':'ES0127797019','gics_sector':'Utilities (web mapping)','typicality_result':'n/a_published_route','primary_regression':'published_damodaran_EUROPE_2026-01','chosen_model':chosen['model'],'predicted_primary':chosen['predicted'],'actual_multiple':chosen['actual'],'deviation':chosen['deviation'],'published_r2':chosen['published_r2'],'implied_value_per_share':chosen['value_per_share'],'currency':'EUR','current_price':T.price,'upside':chosen['value_per_share']/T.price-1 if np.isfinite(chosen['value_per_share']) else None,'second_model':[p['model'] for p in preds if p is not chosen][0],'second_predicted':[p['predicted'] for p in preds if p is not chosen][0],'third_model':[p['model'] for p in preds if p is not chosen][1],'third_predicted':[p['predicted'] for p in preds if p is not chosen][1],'classification':'Not classified (no SEy published)','units_policy':'as_published_note (decimal; user-approved)','units_unverified':'no','substituted_input':'none (sourced analyst consensus g_eps/g_rev used)','damodaran_global':'not used until verified (GLOBAL anomalies recorded at stage 0)','damodaran_western_europe_uk':chosen['predicted'],'flags':'old vintage; low R2; human review pending; effective tax 35.4%','source_urls':T.source_urls}
for k in ['failed_test','adj_r2','predicted_A','predicted_B','predicted_C','residual','std_residual','damodaran_predicted','sector_dummy_coef','SEy','p_values','D1_D10']:r[k]='n/a_published_route'
r['rationale']=f"{chosen['model']} highest published R2 among eligible models; peer-method primary EV/EBITDA kept separately in comparables"
pd.DataFrame([r]).to_csv(P/'valuation_multiples.csv',index=False)

# Sensitivities: peer-set composition, quartiles already in summary; EBITDA normalization (issuer recurring EBITDA vs vendor).
sens=[]
for label,metric in [('vendor FY2025 EBITDA',T.EBITDA),('issuer reported EBITDA 1,947',1947),('issuer recurring EBITDA 1,974',1974),('issuer recurring ex-AR 1,855',1855)]:
 med=primary['median']
 eqv=c.implied_equity_from_ev(med,metric,T.debt,T.NCI,T.cash,0)
 sens.append(dict(scenario=label,EBITDA_eurm=metric,peer_median_ev_ebitda=med,EUR_per_share=eqv/T.current_shares_m if eqv>0 else np.nan,note='mechanical median-held-fixed sensitivity; EBITDA definitions differ (vendor excludes equity-method income; issuer includes it)'))
pd.DataFrame(sens).to_csv(P/'sensitivities.csv',index=False)

log=SourceLog(P.parent/'source_log.csv');existing={r['input_id'] for r in log.rows}
if 'S3_equations' not in existing:
 log.add(input_id='S3_equations',company='EDP Renovaveis',metric='published PE/PBV/EVEBITDA equation coefficients',value='see Coefficients sheets',unit='equation',as_of_date=str(dataset_res.dataset.as_of_date),access_date='2026-11-01',source_name='registered Damodaran equations',url_or_local_file=dataset_res.dataset.path,dataset_vintage=dataset_res.dataset.vintage,page_note_sheet_cell='EUROPE PE/PBV/EV-EBITDA',reported_or_adjusted='reported',consolidation_scope='market-wide regional',method_or_formula='datasets.equation_for(Portugal,dependent,2026-10-30)',status='sourced',limitation='sha256 '+dataset_res.dataset.sha256+'; about10 months old; decimal units approved')
for _,r in D.iterrows():
 for k in ['price','current_shares_m','ni','sales','EBIT','EBITDA','equity','equity_prior','debt','cash','NCI','associates','payout','beta','growth','roe','capex','cfo']:
  rid=f'S3_{r.ticker}_{k}'
  if rid in existing:continue
  v=r.get(k);derived=k in ['payout','growth','roe']
  log.add(input_id=rid,company=r['name'],metric=k,value='n/a' if pd.isna(v) else str(v),unit='ratio' if k in ['payout','beta','growth','roe'] else 'millions' if k!='price' else 'quote currency/share',currency=r.quote_currency if k=='price' else r.report_currency,period_end=str(r.financial_period_end),as_of_date='2026-10-30',access_date='2026-11-01',source_name='StockAnalysis uniform web route',url_or_local_file=r.source_urls,page_note_sheet_cell='candidate_raw.csv '+r.ticker+':'+k,dataset_vintage='FY2025 / latest balance sheet as labelled',reported_or_adjusted='derived' if derived else 'reported',consolidation_scope='parent common equity/NI; consolidated operating fields',method_or_formula='see prepare_pool.py; average equity for peers; closing equity for published equation',status='unavailable' if pd.isna(v) else 'derived' if derived else 'sourced',limitation='associates proxied by Long-Term Investments; uniform vendor conflicts not overwritten',method='stage3',entity_id=r.ticker,price_date=r.price_date,review_status='pending human review')
log.save()
print('PEERS',len(sel),'PRIMARY ev_ebitda mid',primary['value_per_share_mid'],'REG chosen',chosen['model'],chosen['value_per_share'])
