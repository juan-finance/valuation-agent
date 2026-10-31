"""Company-local, reproducible provisional analysis. Never changes source-library code."""
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
D['period_end']=pd.to_datetime(D.financial_period_end.str.extract(r'([A-Z][a-z]{2} \d{1,2}, \d{4})',expand=False),format='%b %d, %Y').dt.strftime('%Y-%m-%d')
D['period_start']=(pd.to_datetime(D.period_end)-pd.DateOffset(years=1)+pd.Timedelta(days=1)).dt.strftime('%Y-%m-%d')
T=D.loc['MT.AS']
FX=1.1172
IDS={'VOE':'AT0000937503','NUE':'US6703461052','STLD':'US8581191009','NHY':'NO0005052605','ANTO':'GB0000456144','HEI':'DE0006047004','YAR':'NO0010208051','BZU':'IT0001347308','FMG':'AU000000FMG4'}
# Gates are fixed before any valuation. Pending human/evidence gates remain explicit failures.
reasons={
 'BHP':'2024 Blackwater/Daunia disposal affects FY24-25 comparability; conservative exclusion',
 'BOL':'2025 acquisition substantially enlarges zinc production',
 'TKA':'TKMS 2025 spinoff and steel restructuring','APAM':'2025 Universal acquisition',
 'ACX':'2024 Haynes acquisition','GLEN':'2024 EVR acquisition','AAL':'2025 platinum demerger',
 'BAS':'2025 coatings discontinued business; restated FY24',
 'CMC':'not in World holdings; 2025 acquisition changes scope',
 '5411':'MSCI deletion Aug31 2026; no current World membership',
 'BSL':'no current World membership evidence','RIO':'unresolved 5.58% class/cap mismatch'}
for ticker in D.index:
 if ticker not in IDS and ticker!='MT.AS' and ticker not in reasons:
  reasons[ticker]='no verified standard Europe/World membership (IMI alone insufficient); size/missingness may also fail'
pool=D.loc[list(IDS)].copy()
pool['isin']=[IDS[t] for t in pool.index]
pool['europe']=pool.europe.astype(bool)
assert (pool.market_cap_check.abs()<=.02).all()
assert (pool.market_cap_eur_m>=1000).all()
assert (pool[list(c.WEIGHTS)].isna().sum(axis=1)<=2).all()
steps=[]
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
sel['target_ticker']='MT.AS'
sel['comp_name']=sel.name
sel['comp_ticker']=sel.ticker
sel['comp_isin']=sel['isin']
sel['distance_score']=sel.distance
sel['market_cap_eur']=sel.market_cap_eur_m*1e6
sel['inclusion_reason']=sel.hypothesis
sel['flags']='provisional ownership/events/classification audit; human Spot_check pending; associates unavailable; non-Dec periods uncalendarized; beta benchmark/frequency unavailable'
sel.to_csv(P/'comparables.csv',index=False)
json.dump(steps,open(P/'peer_selection.json','w'),indent=2)
candidate=D.copy();candidate['gate_result']=[reasons.get(t,'preliminary eligible; audit pending') for t in candidate.index]
candidate.to_csv(P/'candidate_gates.csv',index=False)

def price(multiple, val):
 if not np.isfinite(val):return np.nan
 metric={'pe':'ni','peg':'ni','pbv':'equity','ps':'sales','ev_ebit':'EBIT','ev_ebitda':'EBITDA','ev_cf':'cfo','ev_assets':'assets','ev_sales':'sales'}.get(multiple)
 if not metric:return np.nan
 if multiple=='peg':val*=100*T.growth
 equity=c.implied_equity_from_ev(val,T[metric],T.debt,T.NCI,T.cash,0) if multiple.startswith('ev_') else val*T[metric]
 return equity/T.current_shares_m/FX if equity>0 else np.nan

rows=[]
for name in ['pe','peg','relative_pe','ev_ebit','ev_ebitda','ev_cf','pbv','ev_assets','tobins_q','ps','ev_sales']:
 vals=sel[name].where(sel[name]>0)
 stats=c.multiple_stats(vals,min_valid=6)
 driver={'pe':'growth','pbv':'roe','ps':'net_margin','ev_sales':'ebitda_margin'}.get(name)
 adj=c.scaled_multiple(vals,sel[driver],T[driver],driver_scale=100 if name=='pe' else 1,min_valid=6) if driver else {'available':False,'n_valid':0}
 base=adj if adj['available'] else stats
 usable=stats['usable']
 row={'target_ticker':'MT.AS','multiple':name,**stats,'adjusted_multiple':adj.get('median',np.nan),'adjusted_n_valid':adj['n_valid'],'currency':'EUR','is_primary':name=='pbv','basis':'FY2025','status':'provisional' if usable else 'not valued (<6 valid or unsupported denominator)','flags':'EV before associates; not fully harmonized' if name.startswith('ev_') else 'relative PE/index denominator unavailable' if name=='relative_pe' else 'replacement costs unavailable' if name=='tobins_q' else ''}
 for q,suffix in [('p25','low'),('median','mid'),('p75','high')]:
  row['value_per_share_'+suffix]=price(name,base.get(q,np.nan)) if usable else np.nan
  row['raw_value_'+suffix]=price(name,stats.get(q,np.nan)) if usable else np.nan
 rows.append(row)
summary=pd.DataFrame(rows);summary.to_csv(P/'multiples_summary.csv',index=False)
primary=summary[summary.multiple.eq('pbv')].iloc[0]
assert primary.adjusted_n_valid>=6

def add_frame(wb,name,frame):
 ws=wb.create_sheet(name);ws.append([str(k) for k in frame.columns])
 for r in frame.itertuples(index=False,name=None):
  ws.append([None if pd.isna(v) else v.item() if isinstance(v,np.generic) else v for v in r])
 ws.freeze_panes='A2';ws.auto_filter.ref=ws.dimensions
 return ws
wb=Workbook();wb.remove(wb.active)
add_frame(wb,'Candidate_Pool',candidate.reset_index(drop=True))
add_frame(wb,'Peer_Scores',x.reset_index(drop=True))
sl=wb.create_sheet('Score_Live')
dims=list(c.WEIGHTS);sl.append(['Ticker',*dims,'',*['winsor_'+v for v in dims],'',*['z_'+v for v in dims],'distance'])
assert not x[dims].isna().any().any(), 'This live sheet requires this company pool to have complete scoring inputs'
assert not steps[-1]['scoring']['zero_sd_dims']
sl.append(['MT.AS',*[float(T[v]) for v in dims]])
for i,(_,r) in enumerate(x.iterrows(),3):
 sl.append([r.ticker,*[float(r[v]) for v in dims]])
 for j,d in enumerate(dims):
  raw=col(j+2);win=col(j+11);z=col(j+20)
  sl[f'{win}{i}']=f'=MIN(MAX({raw}{i},{raw}$15),{raw}$16)'
  sl[f'{z}{i}']=f'=({win}{i}-{raw}$17)/{raw}$18'
 sl[f'AB{i}']=f'=SQRT(SUMPRODUCT($B$19:$I$19,(T{i}:AA{i}-$T$2:$AA$2)^2)/SUM($B$19:$I$19))'
end=len(x)+2
for j,d in enumerate(dims):
 raw=col(j+2);win=col(j+11);z=col(j+20)
 sl[f'{raw}15']=f'=PERCENTILE({raw}3:{raw}{end},0.05)'
 sl[f'{raw}16']=f'=PERCENTILE({raw}3:{raw}{end},0.95)'
 sl[f'{raw}17']=f'=AVERAGE({win}3:{win}{end})'
 sl[f'{raw}18']=f'=STDEV({win}3:{win}{end})'
 sl[f'{raw}19']=c.WEIGHTS[d]
 sl[f'{z}2']=f'=({raw}2-{raw}$17)/{raw}$18'
for i,label in [(15,'pool P05'),(16,'pool P95'),(17,'winsor mean'),(18,'winsor SD.S'),(19,'weight')]:sl[f'A{i}']=label
add_frame(wb,'Peer_Selection',sel.reset_index(drop=True))
add_frame(wb,'Peer_Multiples',summary)
add_frame(wb,'Peer_Spot_check',pd.DataFrame({'ticker':sorted(random.Random(20261030).sample(list(sel.ticker),3)),'review_status':'pending human review; no assertion of verification'}))
ws=wb.create_sheet('Live_PBV_ROE');ws.append(['Ticker','market equity (report m)','book','NI','prior book','PBV','ROE','PBV/ROE'])
for i,(_,r) in enumerate(sel.iterrows(),2):
 ws.append([r.ticker,r.pbv*r.equity,r.equity,r.ni,r.equity_prior,f'=B{i}/C{i}',f'=D{i}/AVERAGE(C{i},E{i})',f'=F{i}/G{i}'])
n=len(sel)+1
ws.append(['Target',T.pbv*T.equity,T.equity,T.ni,T.equity_prior,f'=B{n+1}/C{n+1}',f'=D{n+1}/AVERAGE(C{n+1},E{n+1})'])
ws.append(['Implied PBV',f'=MEDIAN(H2:H{n})*G{n+1}'])
ws.append(['EUR/share',f'=B{n+2}*C{n+1}/{T.current_shares_m}/{FX}'])
qa=wb.create_sheet('QA');qa.append(['Status','Evidence']);qa.append(['PROVISIONAL','Ownership/events/classification audit incomplete; industry median unavailable; human review pending'])
wb.save(P/'comparables_audit.xlsx')

# Published FY equity regressions. The EV model is stopped, not supplied an invented FY tax input.
inputs={'g_eps':(T.ni/T.equity)*(1-min(T.payout,1)), 'beta':T.beta,'roe':T.ni/T.equity,'payout':T.payout}
reg=Workbook();ws=reg.active;ws.title='Inputs';ws.append(['Variable','value','source'])
for k,v in inputs.items():ws.append([k,float(v),'StockAnalysis MT FY2025; source_log S3_MT_'+('ni' if k in ['g_eps','roe'] else k)])
ws.append(['book',T.equity,'S3_MT_equity']);ws.append(['NI',T.ni,'S3_MT_ni']);ws.append(['shares',T.current_shares_m,'S3_MT_current_shares_m']);ws.append(['USD/EUR',FX,'existing macro Oct30'])
preds=[];eqws=reg.create_sheet('Equations');eqws.append(['Model','constant','g_eps coef','beta coef','roe coef','payout coef','predicted','published R2','EUR/share','dataset'])
for i,dep in enumerate(['PBV','PE'],2):
 eq,res,region=datasets.equation_for('Netherlands',dep,'2026-10-30')
 check=datasets.check_dataset(res.dataset)
 value=pr.predict(eq,inputs,unit_policy='as_published_note')
 co={t.variable:t.coef for t in eq.terms}
 eqws.append([dep,eq.constant,*[co.get(k,0) for k in inputs],f'=B{i}+C{i}*Inputs!B2+D{i}*Inputs!B3+E{i}*Inputs!B4+F{i}*Inputs!B5',eq.r2,f'=G{i}*Inputs!B{6 if dep=="PBV" else 7}/Inputs!B8/Inputs!B9',res.dataset.dataset_id])
 price_value=value*(T.equity if dep=='PBV' else T.ni)/T.current_shares_m/FX
 preds.append({'model':dep,'predicted':value,'published_r2':eq.r2,'value_per_share':price_value,'actual':T[dep.lower()],'unit_alternative':pr.predict_both_policies(eq,inputs),'equation':eq.raw,'dataset':res.dataset.dataset_id,'region':region,'integrity':check})
 cs=reg.create_sheet('Coefficients_'+dep);cs.append(['Term','coefficient','published t statistic','dataset','as_of','sha256'])
 cs.append(['constant',eq.constant,eq.constant_tstat,res.dataset.dataset_id,str(res.dataset.as_of_date),res.dataset.sha256])
 for term in eq.terms:cs.append([term.variable,term.coef,term.tstat,res.dataset.dataset_id,str(res.dataset.as_of_date),res.dataset.sha256])
 if dep=='PBV':dataset_res=res
reg.save(P/'regression_valuation.xlsx')
json.dump({'inputs':inputs,'predictions':preds,'EVEBITDA':'not valued: matching FY tax/pretax source unavailable; EV associate perimeter incomplete','status':'provisional'},open(P/'regression_results.json','w'),indent=2,default=str)
r={'company':'ArcelorMittal','ticker':'MT.AS','isin':'LU1598757687','gics_sector':'Materials (web mapping)','typicality_result':'n/a_published_route','primary_regression':'published_damodaran_WESTERN_EUROPE_2026-01','chosen_model':'PBV','predicted_primary':preds[0]['predicted'],'actual_multiple':T.pbv,'published_r2':preds[0]['published_r2'],'implied_value_per_share':preds[0]['value_per_share'],'current_price':T.price,'upside':preds[0]['value_per_share']/T.price-1,'second_model':'PE','second_predicted':preds[1]['predicted'],'third_model':'unavailable EVEBITDA (FY input/EV scope)','third_predicted':'n/a_published_route','classification':'Not classified (no SEy published)','units_policy':'as_published_note','units_unverified':'no','substituted_input':'gEPS fundamental closing ROE x retention, not analyst consensus','damodaran_global':'not used until verified (Global PBV beta sign anomaly)','damodaran_western_europe_uk':preds[0]['predicted'],'flags':'old vintage; low R2; unresolved vendor EBIT; human review pending','source_urls':T.source_urls}
for k in ['failed_test','adj_r2','predicted_A','predicted_B','predicted_C','residual','std_residual','damodaran_predicted','sector_dummy_coef']:r[k]='n/a_published_route'
r['rationale']='PBV highest published R2 among eligible equity models; EV stopped for missing matched FY inputs/perimeter'
pd.DataFrame([r]).to_csv(P/'valuation_multiples.csv',index=False)

log=SourceLog(P.parent/'source_log.csv');existing={r['input_id'] for r in log.rows}
if 'S3_equations' not in existing:
 log.add(input_id='S3_equations',company='ArcelorMittal',metric='published PE/PBV equation coefficients',value='see Coefficients sheets',unit='equation',as_of_date=str(dataset_res.dataset.as_of_date),access_date='2026-10-31',source_name='registered Damodaran equations',url_or_local_file=dataset_res.dataset.path,dataset_vintage=dataset_res.dataset.vintage,page_note_sheet_cell='Western Europe & UK PE/PBV; by_multiple agrees with by_region',reported_or_adjusted='reported',consolidation_scope='market-wide regional',method_or_formula='datasets.equation_for(Netherlands,dependent,2026-10-30)',status='sourced',limitation='sha256 '+dataset_res.dataset.sha256+'; about10 months old; Global PBV withheld; decimal units approved')
for _,r in D.iterrows():
 for k in ['price','current_shares_m','ni','sales','EBIT','DA','equity','equity_prior','debt','cash','NCI','associates','payout','beta','growth','roe','capex','cfo']:
  rid=f'S3_{"MT" if r.ticker=="MT.AS" else r.ticker}_{k}'
  if rid in existing:continue
  v=r[k];derived=k in ['payout','growth','roe']
  log.add(input_id=rid,company=r['name'],metric=k,value='n/a' if pd.isna(v) else str(v),unit='ratio' if k in ['payout','beta','growth','roe'] else 'millions' if k!='price' else 'quote currency/share',currency=r.quote_currency if k=='price' else r.report_currency,period_end=r.financial_period_end,as_of_date='2026-10-30',access_date='2026-10-31',source_name='StockAnalysis uniform web route',url_or_local_file=r.source_urls,page_note_sheet_cell='candidate_raw.csv '+r.ticker+':'+k,dataset_vintage='FY2025 / latest balance sheet as labelled',reported_or_adjusted='derived' if derived else 'reported',consolidation_scope='parent common equity/NI; consolidated operating fields',method_or_formula='see prepare_pool.py; average equity for peers; closing equity for published equation',status='unavailable' if pd.isna(v) else 'derived' if derived else 'sourced',limitation='associates missing; uniform vendor conflicts not overwritten',method='stage3',entity_id=r.ticker,price_date=r.price_date,review_status='pending human review')
log.save()
warnings='PROVISIONAL: ownership/event evidence not fully reviewed; human Spot_check pending; Damodaran matching industry MEDIAN unavailable. No replacement-cost Tobin Q or matching home-index PE. All EV ratios are pre-associate qualified cross-checks, never the primary. Vendor FY EBIT1667 versus issuer3628 remains unresolved. No normalization is silently substituted.'
(P/'comparables_report.md').write_text('# ArcelorMittal comparables — 2026-10-30\n\n'+warnings+'\n\n## Selection\nInitial European pool24; World expansion7; BHP excluded for FY24 disposal. Exact10 infeasible after all ordered relaxations; final9 with6 Tier1/2,3 Tier3,6 Europe listings. Tier3 cap4 and 0.05–20x band used only after preceding steps. Score weights, winsor/STDEV.S and library selection logs in peer_selection.json. Preliminary eligibility is not completed evidence review.\n\n'+sel[['ticker','tier','distance','country','financial_period_end']].to_markdown(index=False)+'\n\n## Primary\nEV/EBITDA cannot be harmonized for associates. Prescribed PBV fallback, scaled by positive average-equity ROE with >=6 observations, is primary; not chosen by proximity to DCF. EUR/share p25/median/p75 '+str([primary['value_per_share_'+s] for s in ['low','mid','high']])+'. Quartiles measure peer dispersion, not confidence. Source current shares754.04m, not DCF estimated diluted752.710746m. Book NI contain associates, so PBV requires no separate associate addition.\n\n'+summary.to_markdown(index=False)+'\n\n## Sensitivities and normalization\nRaw PBV versus scaled values are in multiples_summary.csv. Steel cycle-normalized alternative cannot be constructed uniformly for peers from available raw one-off disclosures; not valued, rather than substituting the DCF adjusted denominator. Non-Dec FY2025 is not calendarized without matched interim legs. EV/CFO is levered-CFO cross-check only. Positive extremes retained; mean-median >25% flags shown. Source-linked exclusions and preliminary membership evidence in research_checkpoint.md and candidate_gates.csv.\n')
headings=['# Relative valuation by regression — Western Europe & UK, 2026-10-30','## Headline','## Data','## Fitted model','## Diagnostics','## Valuation results (sorted from most undervalued to most overvalued)','## Robustness','## Key warnings','## Limitations','## Sources']
content=['',f'Provisional PBV prediction {preds[0]["predicted"]:.4f}x; EUR{preds[0]["value_per_share"]:.2f}/share. Market-wide low R2, not a steel fair-value proof.','Uniform target source StockAnalysis FY2025. ROE closing book, versus average book for peer scoring. Fundamental growth substitution approved. gREV unavailable; EV model not used. Listing Netherlands and Luxembourg domicile both EUROPE. Global operating revenues do not justify averaging regional equations.',str(preds),'Not available under this route: n, SEy, adjusted R2, p-values, A/B/C, typicality, D1–D10 and residual classifications. Dataset resolver integrity output saved. Formula/library checks follow recalculation.',pd.DataFrame(preds)[['model','predicted','published_r2','value_per_share']].to_markdown(index=False),'Both policies coincide for PBV/PE (no DFR/tax terms). Approved decimal policy preserved. No invented EV prediction or third eligible model.',warnings,'January2026 equations are about10months old; no residual dispersion; market-wide not industry fit; substituted growth not analyst five-year EPS consensus; Damodaran EV definition undocumented. Global PBV withheld for integrity anomaly. No DATA_BASE_MSCI.xlsx under published route.',T.source_urls+' | Registered regressions_multi_2026-01, resolved via datasets.equation_for; source_log.csv.']
(P/'valuation_summary.md').write_text('\n\n'.join(h+'\n'+v for h,v in zip(headings,content)))
print('PEERS',len(sel),'PRIMARY',primary.value_per_share_mid,'REG',preds[0]['value_per_share'])
