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
T=D.loc['ALFA']
SEK_PER_EUR=10.978  # ECB reference 2026-10-30 (cache/macro)

ISINS={'G1A':'DE0006602006','ATCO.A':'SE0011166610','EPI.A':'SE0011166933','SAND':'SE0000667891',
 'WRT1V':'FI0009003727','METSO':'FI0009014575','SUN':'CH0038388911','ANDR':'AT0000730007',
 'FLS':'DK0018234467','WEIR':'GB0009465807','ROR':'GB00BVFBZH21','IMI':'GB00BGLP8L22',
 'SPX':'GB00BWFGQN14','SMIN':'GB00B1WY2338','SKF.B':'SE0000108227','IP':'IT0001078911',
 'BUCN':'CH0002432174','KRN':'DE0006335003','INDT':'SE0001515552','ABBN':'CH0012221716',
 'RAA':'DE0007010803','KGX':'DE000KGX8881','HLMA':'GB0004052071','XYL':'US98419M1009',
 'IR':'US45687V1061','DOV':'US2600031080','IEX':'US45167R1041','BCHN':'CH0015536027'}
# Gates are fixed before any valuation. Pending human/evidence gates remain explicit failures.
reasons={
 'KSB':'no verified MSCI Europe/World membership evidence in cached holdings proxies',
 'BCHN':'market cap EUR1.73bn below 0.1x target band (EUR2.05bn); kept in candidate audit',
 'FLS':'3 missing scoring dimensions (growth/roe/payout, negative FY2025 NI); hard filter >2'}
pool=D.loc[[t for t in D.index if t!='ALFA' and t not in reasons]].copy()
pool['isin']=[ISINS.get(t,'unverified') for t in pool.index]
pool['europe']=pool.europe.astype(bool)
assert (pool.market_cap_check.abs()<=.05).all(), 'cap checks beyond flag threshold need review'
assert (pool.market_cap_eur_m>=1000).all()
assert (pool[list(c.WEIGHTS)].isna().sum(axis=1)<=2).all()
steps=[]
sel=None;x=None
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
sel['target_ticker']='ALFA.ST'
sel['comp_name']=sel.name
sel['comp_ticker']=sel.ticker
sel['comp_isin']=sel['isin']
sel['distance_score']=sel.distance
sel['market_cap_eur']=sel.market_cap_eur_m*1e6
sel['inclusion_reason']=sel.hypothesis
sel['flags']='provisional ownership/events/classification audit; human Spot_check pending; associates unavailable; non-Dec periods uncalendarized; beta benchmark/frequency unavailable; ISINs registry-mapped pending issuer verification'
sel.to_csv(P/'comparables.csv',index=False)
json.dump(steps,open(P/'peer_selection.json','w'),indent=2)
candidate=D.copy();candidate['gate_result']=[reasons.get(t,'preliminary eligible; audit pending') if t!='ALFA' else 'target' for t in candidate.index]
candidate.to_csv(P/'candidate_gates.csv',index=False)

def price(multiple, val):
 if not np.isfinite(val):return np.nan
 metric={'pe':'ni','peg':'ni','pbv':'equity','ps':'sales','ev_ebit':'EBIT','ev_ebitda':'EBITDA','ev_cf':'cfo','ev_assets':'assets','ev_sales':'sales'}.get(multiple)
 if not metric:return np.nan
 if multiple=='peg':val*=100*T.growth
 equity=c.implied_equity_from_ev(val,T[metric],T.debt,T.NCI,T.cash,0) if multiple.startswith('ev_') else val*T[metric]
 # target metrics are SEK millions; quote is SEK -> per-share value already in SEK.
 return equity/T.current_shares_m if equity>0 else np.nan

rows=[]
for name in ['pe','peg','relative_pe','ev_ebit','ev_ebitda','ev_cf','pbv','ev_assets','tobins_q','ps','ev_sales']:
 vals=sel[name].where(sel[name]>0)
 stats=c.multiple_stats(vals,min_valid=6)
 driver={'pe':'growth','pbv':'roe','ps':'net_margin','ev_sales':'ebitda_margin'}.get(name)
 adj=c.scaled_multiple(vals,sel[driver],T[driver],driver_scale=100 if name=='pe' else 1,min_valid=6) if driver else {'available':False,'n_valid':0}
 base=adj if adj['available'] else stats
 usable=stats['usable']
 row={'target_ticker':'ALFA.ST','multiple':name,**stats,'adjusted_multiple':adj.get('median',np.nan),'adjusted_n_valid':adj['n_valid'],'currency':'SEK','is_primary':name=='pe','basis':'FY2025','status':'provisional' if usable else 'not valued (<6 valid or unsupported denominator)','flags':'EV before associates; not fully harmonized' if name.startswith('ev_') else 'relative PE/index denominator unavailable' if name=='relative_pe' else 'replacement costs unavailable' if name=='tobins_q' else ''}
 for q,suffix in [('p25','low'),('median','mid'),('p75','high')]:
  row['value_per_share_'+suffix]=price(name,base.get(q,np.nan)) if usable else np.nan
  row['raw_value_'+suffix]=price(name,stats.get(q,np.nan)) if usable else np.nan
 rows.append(row)
summary=pd.DataFrame(rows);summary.to_csv(P/'multiples_summary.csv',index=False)
primary=summary[summary.multiple.eq('pe')].iloc[0]
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
dims=list(c.WEIGHTS)
complete=not x[dims].isna().any().any() and not steps[-1]['scoring']['zero_sd_dims']
if complete:
 sl=wb.create_sheet('Score_Live')
 sl.append(['Ticker',*dims,'',*['winsor_'+v for v in dims],'',*['z_'+v for v in dims],'distance'])
 sl.append(['ALFA',*[float(T[v]) for v in dims]])
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
ws=wb.create_sheet('Live_PE_G');ws.append(['Ticker','market equity (report m)','NI','payout','ROE avg-eq','g=ROE(1-payout)','PE','PE/(100g)'])
for i,(_,r) in enumerate(sel.iterrows(),2):
 ws.append([r.ticker,r.pe*r.ni,r.ni,r.payout,r.roe,r.growth,f'=B{i}/C{i}',f'=G{i}/(100*F{i})'])
n=len(sel)+1
ws.append(['Target',T.pe*T.ni,T.ni,T.payout,T.roe,T.growth,f'=B{n+1}/C{n+1}'])
ws.append(['Implied PE',f'=MEDIAN(H2:H{n})*100*F{n+1}'])
ws.append(['SEK/share',f'=B{n+2}*C{n+1}/{T.current_shares_m}'])
qa=wb.create_sheet('QA');qa.append(['Status','Evidence']);qa.append(['PROVISIONAL','Ownership/events/classification audit incomplete; industry median unavailable; human review pending'])
wb.save(P/'comparables_audit.xlsx')

# Published FY regressions — Sweden lists EUROPE equations via resolver.
tax_rate=0.257  # FY2025 effective: (pretax 11,198 - NI 8,322)/11,198, issuer release
mkt_eq_sek=T.price*T.current_shares_m
dfr=T.debt/(T.debt+mkt_eq_sek)
ic=T.equity+T.debt-T.cash
roic=T.EBIT*(1-tax_rate)/ic
inputs={'g_eps':0.1272,'beta':T.beta,'roe':T.ni/T.equity,'payout':T.payout,'g_rev':0.0941,'dfr':dfr,'tax_rate':tax_rate,'roic':roic}
g_eps_source='analyst consensus 3Y EPS growth forecast 12.72% (stockanalysis statistics, accessed 2026-11-01)'
g_rev_source='analyst consensus 3Y revenue growth forecast 9.41% (same source); else file rule g_eps fallback'
reg=Workbook();ws=reg.active;ws.title='Inputs';ws.append(['Variable','value','source'])
for k,v in inputs.items():
 src={'g_eps':g_eps_source,'g_rev':g_rev_source,'beta':'StockAnalysis Beta(5Y)','roe':'NI/parent common equity FY2025 (closing)','payout':'dividends paid/NI FY2025','dfr':'total debt/(debt+market equity), market equity at 2026-10-30','tax_rate':'FY2025 effective rate per issuer release','roic':'EBIT(1-tax)/(equity+debt-cash)'}[k]
 ws.append([k,float(v),src])
ws.append(['book',T.equity,'S3_ALFA_equity']);ws.append(['NI',T.ni,'S3_ALFA_ni']);ws.append(['EBITDA',T.EBITDA,'S3_ALFA_EBITDA']);ws.append(['debt',T.debt,'S3_ALFA_debt']);ws.append(['NCI',T.NCI,'S3_ALFA_NCI']);ws.append(['cash',T.cash,'S3_ALFA_cash']);ws.append(['shares',T.current_shares_m,'S3_ALFA_current_shares_m'])
preds=[];eqws=reg.create_sheet('Equations');eqws.append(['Model','constant','pred_terms','predicted','published R2','SEK/share','dataset'])
for i,dep in enumerate(['PE','PBV','EV/EBITDA'],2):
 eq,res,region=datasets.equation_for('Sweden',dep,'2026-10-30')
 check=datasets.check_dataset(res.dataset)
 value=pr.predict(eq,inputs,unit_policy='as_published_note')
 # live formula: =constant + SUM(coef * Inputs!B<row>) per published term
 inrow={k:i2 for i2,k in enumerate(inputs.keys(),2)}
 formula='='+str(eq.constant)
 for term in eq.terms:
  if term.variable in inrow:formula+=f'+{term.coef}*Inputs!B{inrow[term.variable]}'
 eqws.append([dep,eq.constant,str([(t.variable,t.coef) for t in eq.terms]),formula,eq.r2,None,res.dataset.dataset_id])
 if dep=='PE': eqv=value*T.ni; share=eqv/T.current_shares_m
 elif dep=='PBV': eqv=value*T.equity; share=eqv/T.current_shares_m
 else:
  ev=value*T.EBITDA
  eqv=c.implied_equity_from_ev(value,T.EBITDA,T.debt,T.NCI,T.cash,0);share=eqv/T.current_shares_m if eqv>0 else np.nan
 eqws.cell(row=i,column=6).value=share
 both=pr.predict_both_policies(eq,inputs)
 preds.append({'model':dep,'predicted':value,'published_r2':eq.r2,'value_per_share':share,'actual':{'PE':T.pe,'PBV':T.pbv,'EV/EBITDA':T.ev_ebitda}[dep],'unit_alternative':both,'equation':eq.raw,'dataset':res.dataset.dataset_id,'region':region,'integrity':check})
 cs=reg.create_sheet('Coefficients_'+dep.replace('/','_'));cs.append(['Term','coefficient','published t statistic','dataset','as_of','sha256'])
 cs.append(['constant',eq.constant,eq.constant_tstat,res.dataset.dataset_id,str(res.dataset.as_of_date),res.dataset.sha256])
 for term in eq.terms:cs.append([term.variable,term.coef,term.tstat,res.dataset.dataset_id,str(res.dataset.as_of_date),res.dataset.sha256])
 dataset_res=res
reg.save(P/'regression_valuation.xlsx')
json.dump({'inputs':inputs,'predictions':preds,'status':'provisional'},open(P/'regression_results.json','w'),indent=2,default=str)
# chosen = highest published R2 among eligible (bucket guidance: PE business-appropriate primary for peer method only)
chosen=max(preds,key=lambda p:p['published_r2'])
r={'company':'Alfa Laval','ticker':'ALFA.ST','isin':'SE0000695876','gics_sector':'Industrials (web mapping)','typicality_result':'n/a_published_route','primary_regression':'published_damodaran_WESTERN_EUROPE_2026-01','chosen_model':chosen['model'],'predicted_primary':chosen['predicted'],'actual_multiple':chosen['actual'],'published_r2':chosen['published_r2'],'implied_value_per_share':chosen['value_per_share'],'current_price':T.price,'upside':chosen['value_per_share']/T.price-1,'second_model':[p['model'] for p in preds if p is not chosen][0],'second_predicted':[p['predicted'] for p in preds if p is not chosen][0],'third_model':[p['model'] for p in preds if p is not chosen][1],'third_predicted':[p['predicted'] for p in preds if p is not chosen][1],'classification':'Not classified (no SEy published)','units_policy':'as_published_note (decimal; user-approved)','units_unverified':'no','substituted_input':'none (sourced analyst consensus g_eps/g_rev used)','damodaran_global':'not used until verified (GLOBAL anomalies recorded at stage 0)','damodaran_western_europe_uk':chosen['predicted'],'flags':'old vintage; low R2; human review pending','source_urls':T.source_urls}
for k in ['failed_test','adj_r2','predicted_A','predicted_B','predicted_C','residual','std_residual','damodaran_predicted','sector_dummy_coef']:r[k]='n/a_published_route'
r['rationale']=f"{chosen['model']} highest published R2 among eligible equity/EV models; peer-method primary PE kept separately in comparables"
pd.DataFrame([r]).to_csv(P/'valuation_multiples.csv',index=False)

log=SourceLog(P.parent/'source_log.csv');existing={r['input_id'] for r in log.rows}
if 'S3_equations' not in existing:
 log.add(input_id='S3_equations',company='Alfa Laval',metric='published PE/PBV/EVEBITDA equation coefficients',value='see Coefficients sheets',unit='equation',as_of_date=str(dataset_res.dataset.as_of_date),access_date='2026-11-01',source_name='registered Damodaran equations',url_or_local_file=dataset_res.dataset.path,dataset_vintage=dataset_res.dataset.vintage,page_note_sheet_cell='Western Europe & UK PE/PBV/EV-EBITDA',reported_or_adjusted='reported',consolidation_scope='market-wide regional',method_or_formula='datasets.equation_for(Sweden,dependent,2026-10-30)',status='sourced',limitation='sha256 '+dataset_res.dataset.sha256+'; about10 months old; decimal units approved')
for _,r in D.iterrows():
 for k in ['price','current_shares_m','ni','sales','EBIT','DA','equity','equity_prior','debt','cash','NCI','associates','payout','beta','growth','roe','capex','cfo']:
  rid=f'S3_{"ALFA" if r.ticker=="ALFA" else r.ticker}_{k}'
  if rid in existing:continue
  v=r[k];derived=k in ['payout','growth','roe']
  log.add(input_id=rid,company=r['name'],metric=k,value='n/a' if pd.isna(v) else str(v),unit='ratio' if k in ['payout','beta','growth','roe'] else 'millions' if k!='price' else 'quote currency/share',currency=r.quote_currency if k=='price' else r.report_currency,period_end=r.financial_period_end,as_of_date='2026-10-30',access_date='2026-11-01',source_name='StockAnalysis uniform web route',url_or_local_file=r.source_urls,page_note_sheet_cell='candidate_raw.csv '+r.ticker+':'+k,dataset_vintage='FY2025 / latest balance sheet as labelled',reported_or_adjusted='derived' if derived else 'reported',consolidation_scope='parent common equity/NI; consolidated operating fields',method_or_formula='see prepare_pool.py; average equity for peers; closing equity for published equation',status='unavailable' if pd.isna(v) else 'derived' if derived else 'sourced',limitation='associates missing; uniform vendor conflicts not overwritten',method='stage3',entity_id=r.ticker,price_date=r.price_date,review_status='pending human review')
log.save()
warnings='PROVISIONAL: ownership/event evidence not fully reviewed; human Spot_check pending; Damodaran matching industry MEDIAN unavailable. No replacement-cost Tobin Q or matching home-index PE. All EV ratios are pre-associate qualified cross-checks, never the primary. Vendor FY EBIT 11,820 vs issuer reported EBIT 11,749 recorded both (0.6% diff, within tolerance). ISINs registry-mapped pending issuer-page verification.'
(P/'comparables_report.md').write_text('# Alfa Laval comparables — 2026-10-30\n\n'+warnings+'\n\n## Selection\nInitial candidate pool 30 (all Europe-first, US machinery as World-relaxation only). Europe step already feasible: '+str(steps[-1]['n_pool'])+' in-band candidates; selected 10 under default caps (Tier3<=2, >=8 Tier1/2, >=5 Europe-listed). Score weights, winsor/STDEV.S and library selection logs in peer_selection.json. Preliminary eligibility is not completed evidence review.\n\n'+sel[['ticker','tier','distance','country','financial_period_end']].to_markdown(index=False)+'\n\n## Primary\nPE is the prescribed bucket-D machinery primary (sector_adjustments: gases/machinery PE, EV/EBIT cross-check); scaled by growth with >=6 observations. SEK/share p25/median/p75 '+str([primary['value_per_share_'+s] for s in ['low','mid','high']])+'. Quartiles measure peer dispersion, not confidence. Target NI per issuer release 8,322 vs vendor 8,272 (0.6% diff; vendor basis retained for uniformity).\n\n'+summary.to_markdown(index=False)+'\n\n## Sensitivities and normalization\nRaw PE versus growth-scaled values are in multiples_summary.csv. EV/EBIT is a qualified cross-check (associates unavailable). No uniform one-off normalization constructed; vendor FY2025 reported bases retained. Positive extremes retained; mean-median >25% flags shown. Source-linked exclusions and preliminary membership evidence in candidate_gates.csv.\n')
headings=['# Relative valuation by regression — Western Europe & UK, 2026-10-30','## Headline','## Data','## Fitted model','## Diagnostics','## Valuation results (sorted from most undervalued to most overvalued)','## Robustness','## Key warnings','## Limitations','## Sources']
content=['',f"Provisional {chosen['model']} prediction {chosen['predicted']:.4f}x; SEK{chosen['value_per_share']:.2f}/share. Market-wide low R2, not a machinery fair-value proof.",'Uniform target source StockAnalysis FY2025 cross-checked vs issuer release. Analyst consensus g_eps 12.72%/g_rev 9.41% (no substitution needed). Beta 0.75 vendor 5Y; payout 42.5%; ROE closing book for equations vs average book for peer scoring. Listing Sweden -> EUROPE region; global revenues do not justify averaging regional equations.',str(preds),'Not available under this route: n, SEy, adjusted R2, p-values, A/B/C, typicality, D1–D10 and residual classifications. Dataset resolver integrity output saved. Formula/library checks follow recalculation.',pd.DataFrame(preds)[['model','predicted','published_r2','value_per_share']].to_markdown(index=False),'Decimal unit policy approved; both policies compared for EVEBITDA (see unit_alternative). Global anomalies recorded at stage 0; EUROPE equations unaffected.',warnings,'January 2026 equations ~10 months old; no residual dispersion; market-wide not industry fit; analyst-growth definition differs from our fundamental metric (consensus used); Damodaran EV definition undocumented. No DATA_BASE_MSCI.xlsx under published route.',T.source_urls+' | Registered regressions_multi_2026-01, resolved via datasets.equation_for; source_log.csv.']
(P/'valuation_summary.md').write_text('\n\n'.join(h+'\n'+v for h,v in zip(headings,content)))
print('PEERS',len(sel),'PRIMARY PE mid',primary.value_per_share_mid,'REG chosen',chosen['model'],chosen['value_per_share'])
