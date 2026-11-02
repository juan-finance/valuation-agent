"""VWS-only published-route valuation; arithmetic delegated to valuation_agent."""
import json,random,math
from pathlib import Path
import numpy as np
import pandas as pd
from openpyxl import Workbook
from valuation_agent import comparables as c,datasets,published_regressions as pr

P=Path(__file__).resolve().parent;ROOT=P.parents[2]
D=pd.read_csv(P/'candidate_raw.csv').set_index('ticker',drop=False);T=D.loc['VWS'].copy()
world=pd.read_csv(P/'world_candidate_membership.csv')
assert 'ETN' in world.Ticker.values
D.loc['ETN','membership']='URTH MSCI World standard ETF proxy, holdings2026-10-29; source latest-holdings.csv cached with date header'
standard={'ENR','VWS','ABBN','SU','LR','PRY','SIE','WRT1V','ALFA','ATCO.A','SAND','METSO','SPX','G1A','SKF.B','SMIN','EPI.A','GEV','ETN'}
for t in D.index:
 if t in standard:D.loc[t,'membership']='URTH World standard dated2026-10-29, entity/name+listing matched; IEUR confirms Europe listing where applicable'
# Interpretation for this run: Europe-listed candidates verified in the dated IEUR MSCI Europe IMI proxy are
# Europe-eligible under the funnel's Europe-first step; URTH standard-index matching is required only for the
# permitted developed-market World expansion (non-European listings). See evidence_review.md.
FX=json.loads((ROOT/'cache/macro/2026-10-30.json').read_text())['fx_ecb_reference']['rates'];FX['EUR']=1
ISIN={'WRT1V':'FI0009003727','ANDR':'AT0000730007','SAND':'SE0000667891','NDX1':'DE000A0D6554','SU':'FR0000121972','ENR':'DE000ENER6Y0','ETN':'IE00B8KQN827','METSO':'FI0009014575','LR':'FR0010307819','IMI':'GB00BGLP8L22','ALFA':'SE0000695876','NKT':'DK0010287663','SUN':'CH0038388911','SPX':'GB00BWFGQN14','WEIR':'GB0009465807','ROR':'GB00BVFBZH21','G1A':'DE0006602006','NEX':'FR0000044448','PRY':'IT0004176001','ATCO.A':'SE0017486889','ABBN':'CH0012221716','SKF.B':'SE0000108227','SMIN':'GB00B1WY2338','EPI.A':'SE0015658109','GEV':'US36828A1014','SIE':'DE0007236101'}
identity={
'WRT1V':'https://live.deutsche-boerse.com/equity/wartsila',
'ANDR':'https://www.andritz.com/group-en/investors/share',
'SAND':'https://www.boerse-frankfurt.de/equity/sandvik-ab?mic=XFRA',
'NDX1':'https://www.nordex-online.com/en/2022/06/nordex-se-nordex-se-resolves-on-capital-increase/',
'SU':'https://www.se.com/ww/en/about-us/investor-relations/share-information/share-price/',
'ENR':'https://www.siemens-energy.com/global/en/home/investor-relations/share.html',
'ETN':'https://www.borsaitaliana.it/borsa/azioni/global-equity-market/listino-ufficiale.html?isin=IE00B8KQN827&lang=en',
'METSO':'https://www.nasdaq.com/press-release/metso-outotec-corporation:-change-of-company-name-and-trading-and-issuer-codes-2023',
'LR':'https://www.legrand.com/en/investors-and-shareholders/shareholders-corner/questions-and-answers',
'IMI':'https://www.londonstockexchange.com/en/news/article/IMI/holding-s-in-company/16933526',
'ALFA':'https://www.boerse-frankfurt.de/aktie/alfa-laval',
'SPX':'https://www.londonstockexchange.com/en/news/article/SPX/change-in-major-shareholding/2666-8e-82-9c-bd-4b7d88',
'G1A':'https://www.gea.com/en/company/investor-relations/share-information/share-price/',
'NKT':'https://nkt.com/investors/share-and-shareholders'}
# Event screens fixed before valuation; unknown evidence is never relabelled as a completed review.
excluded={'SIE':'material FY2024-25 Altair acquisition/India perimeter change makes FY base noncomparable',
'PRY':'material Encore Wire acquisition July2024 changes FY24/25 perimeter',
'ABBN':'FY25 Robotics discontinued-operation/divestment perimeter plus Gamesa Electric acquisition',
'GEV':'FY2024 spin-off; FY25/24 comparability not established',
'SMIN':'FY2025/26 material portfolio disposal programme; no harmonized continuing basis',
'NEX':'Lynxeo/AmerCable FY2025 divestments and discontinued-operation perimeter',
'SKF.B':'announced automotive separation and restructuring; consistent FY base not established'}
for t,r in D.iterrows():
 if t=='VWS':continue
 if abs(r.market_cap_check)>.02:excluded[t]=f'class capitalization reconciliation exceeds2% ({100*r.market_cap_check:.3f}%)'
 if r.market_cap_eur_m<1000:excluded[t]='below EUR1bn'
 if r[list(c.WEIGHTS)].isna().sum()>2:excluded[t]='more than two missing score dimensions'
 if not r.europe and t!='ETN':excluded.setdefault(t,'developed World membership not established')
D['isin']=[ISIN.get(t,'not selected; not verified') for t in D.index]
pool=D.drop(index=['VWS',*excluded.keys()],errors='ignore').copy()
steps=[];sel=None
for label,world,b,cap in [('Europe',False,.1,2),('World',True,.1,2),('size',True,.05,2),('tier3',True,.05,4)]:
 x=pool[(pool.market_cap_eur_m>=T.market_cap_eur_m*b)&(pool.market_cap_eur_m<=T.market_cap_eur_m/b)]
 if not world:x=x[x.europe]
 scores,params=c.similarity_scores(x,T);x=x.join(scores)
 sel,info=c.select_peers(x,max_tier_3=cap)
 steps.append(dict(step=label,n_pool=len(x),band=[b,1/b],selection=info,scoring=params))
 if sel is not None:break
if sel is None:
 for n in [9,8]:
  sel,info=c.select_peers(x,n=n,max_tier_3=4)
  if sel is not None:break
assert sel is not None,'fewer than8 feasible peers: blocked'
sel['target_ticker']='VWS.CO';sel['comp_ticker']=sel.ticker;sel['comp_name']=sel['name'];sel['comp_isin']=sel['isin']
sel['distance_score']=sel.distance;sel['effective_weight_coverage']=sel.weight_coverage;sel['market_cap_eur']=sel.market_cap_eur_m*1e6
sel['inclusion_reason']=sel.hypothesis;sel['source_route']='web_minimum';sel['metric_fallbacks']='fundamental growth, income-statement EBITDA, FY closing EV balances'
sel['identity_source']=[identity.get(t,'pending') for t in sel.ticker]
sel['flags']='DRAFT: human review pending; EV pre-associate qualified only; NCI book proxy; beta benchmark/frequency unavailable; reported FY2025 uncalendarized; IFRS/US GAAP differences'
sel.to_csv(P/'comparables.csv',index=False)
D['gate_result']=[('target' if t=='VWS' else excluded.get(t,'numeric eligible; evidence review detailed in evidence_review.md')) for t in D.index]
D['selected']=D.index.isin(sel.index);D.to_csv(P/'candidate_gates.csv',index=False)
(P/'peer_selection.json').write_text(json.dumps(steps,indent=2,default=str)+'\n')

DKK=FX['DKK']
def value(name,m,metric=None):
 if not np.isfinite(m):return np.nan
 key={'pe':'ni','peg':'ni','pbv':'equity','ps':'sales','ev_ebit':'EBIT','ev_ebitda':'EBITDA','ev_cf':'cfo','ev_assets':'assets','ev_sales':'sales'}.get(name)
 if key is None:return np.nan
 if name=='peg':m*=100*T.growth
 eq=c.implied_equity_from_ev(m,T[key] if metric is None else metric,T.debt,T.NCI,T.cash,0) if name.startswith('ev_') else m*(T[key] if metric is None else metric)
 return eq/T.current_shares_m*DKK if eq>0 else np.nan
summary=[]
for name in ['pe','peg','relative_pe','ev_ebit','ev_ebitda','ev_cf','pbv','ev_assets','tobins_q','ps','ev_sales']:
 vals=sel[name].where(sel[name]>0);stats=c.multiple_stats(vals,min_valid=6)
 driver={'pe':'growth','pbv':'roe','ps':'net_margin','ev_sales':'ebitda_margin'}.get(name)
 adj=c.scaled_multiple(vals,sel[driver],T[driver],driver_scale=100 if name=='pe' else 1,min_valid=6) if driver else dict(available=False,n_valid=0)
 chosen=adj if adj['available'] else stats
 row=dict(target_ticker='VWS.CO',multiple=name,**stats,adjusted_multiple=adj.get('median',np.nan),adjusted_n_valid=adj['n_valid'],currency='DKK',basis='FY2025',is_primary=name=='ev_ebit',status='draft qualified; pre-associate EV only' if name.startswith('ev_') else 'draft' if stats['usable'] else 'unavailable',flags='EV before associates: NOT fully harmonized comparable EV base; bucket-C sector primary per mapping' if name.startswith('ev_') else 'matching index PE unavailable' if name=='relative_pe' else 'replacement costs unavailable' if name=='tobins_q' else '')
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
 spot.append(dict(ticker=t,market_equity_report_m=m,debt=r.debt,nci=r.NCI,cash=r.cash,associates='unavailable; zero only in pre-associate sensitivity',EV_before_associates=ev,stored=r.EV_before_associates,arithmetic_delta=ev-r.EV_before_associates,source=r.source_urls,automated_check='PASS' if np.isfinite(ev) and abs(ev-r.EV_before_associates)<1e-8 else 'UNAVAILABLE',human_review='pending, not performed or waived'))
sheet(wb,'Peer_Spot_check',pd.DataFrame(spot));pd.DataFrame(spot).to_csv(P/'peer_ev_checks.csv',index=False)
# Live score audit uses separate parameter sheet, so no row overlap as pool expands.
dims=list(c.WEIGHTS);par=wb.create_sheet('Score_Params');par.append(['dimension','P05','P95','winsor mean','sample SD','weight','target raw z'])
live=wb.create_sheet('Score_Live');live.append(['ticker',*dims,*['winsor_'+d for d in dims],*['z_'+d for d in dims],'distance'])
from openpyxl.utils import get_column_letter as col
for i,(_,r) in enumerate(x.iterrows(),2):
 live.append([r.ticker,*[float(r[d]) if np.isfinite(r[d]) else None for d in dims]])
 for j,d in enumerate(dims):
  raw=col(j+2);win=col(j+10);z=col(j+18);pi=j+2
  live[f'{win}{i}']=f'=IF(ISNUMBER({raw}{i}),MIN(MAX({raw}{i},Score_Params!B{pi}),Score_Params!C{pi}),"")'
  live[f'{z}{i}']=f'=IF(ISNUMBER({win}{i}),({win}{i}-Score_Params!D{pi})/Score_Params!E{pi},"")'
 live[f'Z{i}']='=SQRT('+ '+'.join(f'{c.WEIGHTS[d]}*({col(j+18)}{i}-Score_Params!G{j+2})^2' for j,d in enumerate(dims))+')'
for j,d in enumerate(dims):
 raw=col(j+2);win=col(j+10);pi=j+2;end=len(x)+1
 par.append([d,f'=PERCENTILE(Score_Live!{raw}2:{raw}{end},0.05)',f'=PERCENTILE(Score_Live!{raw}2:{raw}{end},0.95)',f'=AVERAGE(Score_Live!{win}2:{win}{end})',f'=STDEV(Score_Live!{win}2:{win}{end})',c.WEIGHTS[d],f'=({T[d]}-D{pi})/E{pi}'])
missing=int(x[dims].isna().sum().sum())
qa=wb.create_sheet('QA');qa.append(['Status','Details']);qa.append(['DRAFT',f'Human Spot_check pending. EV associate/lease harmonization incomplete. Missing scoring cells in final pool: {missing}. See qa_results.md.'])
wb.save(P/'comparables_audit.xlsx')

# Published-route regression inputs: vendor 3Y analyst consensus used for g_eps/g_rev (labelled, not 5Y);
# declared FY2025 payout DPS0.10EUR/EPS0.78; closing parent equity ROE per published-route basis.
declared_payout=0.10/T.ni*T.current_shares_m if False else 0.10/0.78  # DKK0.74/EUR7.4735 = EUR0.0991; declared DPS/EPS
closing_roe=T.ni/T.equity;tax=T.tax/T.pretax
inputs={'g_eps':0.3241,'beta':float(T.beta),'roe':closing_roe,'payout':declared_payout,'g_rev':0.0834,'dfr':T.debt/(T.debt+T.price*T.current_shares_m/DKK),'tax_rate':tax,'roic':T.EBIT*(1-tax)/(T.equity+T.debt-T.cash)}
reg=Workbook();w=reg.active;w.title='Inputs';w.append(['Variable','value','definition/source'])
for k,v in inputs.items():w.append([k,float(v),'vendor 3Y analyst consensus (not 5Y); labelled' if k in ['g_eps','g_rev'] else 'vendor FY2025; see relative_inputs.md and source_log.csv'])
for k in ['equity','ni','EBITDA','debt','NCI','cash','current_shares_m']:w.append([k,float(T[k]),'S3_VWS_'+k])
w.append(['fx_dkk_per_eur',DKK,'ECB reference 2026-10-30'])
eqws=reg.create_sheet('Equations');eqws.append(['model','constant','terms','predicted','published R2','DKK/share','dataset','actual','actual/predicted - 1'])
preds=[];checks=[]
for i,dep in enumerate(['PE','PBV','EV/EBITDA'],2):
 eq,res,region=datasets.equation_for('Denmark',dep,'2026-10-30');findings=datasets.check_dataset(res.dataset);checks.append(dict(dataset=res.dataset.dataset_id,findings=[vars(f) for f in findings]))
 assert not any(f.severity=='error' for f in findings)
 pv=pr.predict(eq,inputs,unit_policy='as_published_note');both=pr.predict_both_policies(eq,inputs)
 formula='='+str(eq.constant)
 for term in eq.terms:
  ri=list(inputs).index(term.variable)+2;formula+=f'+({term.coef})*'+(f'LN(Inputs!B{ri})' if term.transform=='ln' else f'Inputs!B{ri}')
 actual={'PE':T.pe,'PBV':T.pbv,'EV/EBITDA':T.ev_ebitda}[dep]
 priceformula=f'=D{i}*Inputs!B11/Inputs!B16*Inputs!B17' if dep=='PE' else f'=D{i}*Inputs!B10/Inputs!B16*Inputs!B17' if dep=='PBV' else f'=(D{i}*Inputs!B12-Inputs!B13-Inputs!B14+Inputs!B15)/Inputs!B16*Inputs!B17'
 eqws.append([dep,eq.constant,str([(a.variable,a.coef) for a in eq.terms]),formula,eq.r2,priceformula,res.dataset.dataset_id,float(actual),f'=H{i}/D{i}-1'])
 sh=value('pe',pv) if dep=='PE' else value('pbv',pv) if dep=='PBV' else value('ev_ebitda',pv)
 preds.append(dict(model=dep,predicted=pv,published_r2=eq.r2,value_per_share=sh,actual=actual,actual_predicted_gap=actual/pv-1,unit_alternative=both,equation=eq.raw,dataset=res.dataset.dataset_id,sha256=res.dataset.sha256,as_of=res.dataset.as_of_date,region=region,match_level=res.match_level,warnings=res.warnings))
 co=reg.create_sheet('Coefficients_'+dep.replace('/','_'));co.append(['term','coefficient','t statistic','dataset','sha256']);co.append(['constant',eq.constant,eq.constant_tstat,res.dataset.dataset_id,res.dataset.sha256])
 for term in eq.terms:co.append([term.variable,term.coef,term.tstat,res.dataset.dataset_id,res.dataset.sha256])
reg.save(P/'regression_valuation.xlsx');chosen=max(preds,key=lambda v:v['published_r2'])
regresult=dict(inputs=inputs,predictions=preds,chosen=chosen['model'],substituted_input='none needed: vendor 3Y analyst consensus used for g_eps/g_rev (3Y not 5Y horizon — labelled definition gap); declared payout basis',status='draft pending human review',dataset_checks=checks)
(P/'regression_results.json').write_text(json.dumps(regresult,indent=2,default=str)+'\n')
row=dict(company='Vestas Wind Systems A/S',ticker='VWS.CO',isin='DK0061539921',gics_sector='not independently verified; internal bucket C not GICS',typicality_result='n/a_published_route',primary_regression='published_damodaran_EUROPE_2026-01',chosen_model=chosen['model'],predicted_primary=chosen['predicted'],actual_multiple=chosen['actual'],published_r2=chosen['published_r2'],implied_value_per_share=chosen['value_per_share'],current_price=T.price,upside=chosen['value_per_share']/T.price-1,classification='Not classified (no SEy published)',units_policy='as_published_note; decimal approved',units_unverified='no; alternative policy disclosed',substituted_input=regresult['substituted_input'],rationale='Highest published R2 chosen; wind/power-equipment recovery margins limit interpretation. No sector EV/EBIT equation.',source_urls=T.source_urls)
for k in ['failed_test','adj_r2','predicted_A','predicted_B','predicted_C','residual','std_residual','damodaran_predicted','sector_dummy_coef']:row[k]='n/a_published_route'
for i,p in enumerate([p for p in preds if p is not chosen],2):row[f'alternative_{i}_model']=p['model'];row[f'alternative_{i}_prediction']=p['predicted']
pd.DataFrame([row]).to_csv(P/'valuation_multiples.csv',index=False)

# Industry rows are published ratios, not an asserted cross-sectional median.
bench=[]
for fam in ['evebitda_industry','pbv_industry']:
 rr=datasets.resolve(fam,country='Denmark',valuation_date='2026-10-30');fr=datasets.load_industry(rr.dataset)
 for ind in ['Machinery','Green & Renewable Energy','Electrical Equipment']:
  br=datasets.industry_row(fr,ind);bench.append(dict(family=fam,industry=ind,values=br.to_dict(),dataset=rr.dataset.dataset_id,sha256=rr.dataset.sha256,as_of=rr.dataset.as_of_date,identity='published industry ratio; NOT verified median'))
(P/'industry_benchmarks.json').write_text(json.dumps(bench,indent=2,default=str)+'\n')

# Full stage3 field schedule; reduced step itself only has one source line per source.
from valuation_agent.sourcelog import SourceLog
log=SourceLog(P/'source_log.csv')
log.rows=[]
for _,r in D.iterrows():
 for k in ['price','current_shares_m','market_cap_quote_m','ni','sales','EBIT','DA','EBITDA','equity','equity_prior','debt','cash','NCI','associates','assets','payout','beta','growth','roe','capex','cfo','pretax','tax']:
  v=r[k];der=k in ['growth','roe','payout']
  base=r.source_urls.split('financials/')[0]
  suffix='history/' if k=='price' else 'statistics/' if k in ['beta','current_shares_m','market_cap_quote_m'] else 'financials/balance-sheet/' if k in ['equity','equity_prior','debt','cash','NCI','associates','assets'] else 'financials/cash-flow-statement/' if k in ['cfo','capex'] else 'financials/income-statement/'
  location=r.source_urls if der else base+suffix
  log.add(input_id=f'S3_{r.ticker}_{k}',company=r['name'],metric=k,value='n/a' if pd.isna(v) else str(v),unit='ratio' if k in ['growth','roe','payout','beta'] else 'currency/share' if k=='price' else 'millions',currency='n/a' if k in ['current_shares_m','growth','roe','payout','beta'] else r.quote_currency if k in ['price','market_cap_quote_m'] else r.report_currency,as_of_date='2026-10-30',access_date='2026-11-02',period_end=r.financial_period_end if k not in ['price','current_shares_m','market_cap_quote_m','beta'] else 'n/a',source_name='StockAnalysis uniform raw fields',url_or_local_file=location,page_note_sheet_cell='candidate_raw.csv '+r.ticker+':'+k,reported_or_adjusted='derived' if der else 'reported',consolidation_scope='parent NI/equity; consolidated operating fields',method_or_formula='normalize.py; uniform FY2025 income-statement EBITDA; average equity for peers, closing equity for published regression',status='unavailable' if pd.isna(v) else 'derived' if der else 'sourced',limitation='FY balance; EV pre-associates only; shares/current FY EPS not substituted',entity_id=r.ticker,price_date=r.price_date,review_status='pending human review')
for b in [*bench,dict(dataset=preds[0]['dataset'],sha256=preds[0]['sha256'],as_of=preds[0]['as_of'],family='regressions',industry='EUROPE PE/PBV/EVEBITDA')]:
 log.add(input_id='dataset_'+b['dataset']+'_'+b['industry'],company='Vestas Wind Systems A/S',metric=b['family'],value=b['industry'],unit='equation or published industry ratio',as_of_date=b['as_of'],access_date='2026-11-02',source_name='registered Damodaran data library',url_or_local_file='data registry '+b['dataset'],dataset_vintage='2026-01',page_note_sheet_cell='industry_benchmarks.json or Coefficients sheets',status='sourced',limitation='sha256 '+b['sha256']+'; industry ratio not verified median')
log.save()

# Sensitivities do not claim issuer-guided normalized forecasts.
sens=[]
for margin in [.04,.06,.08,.10]:
 vals=sel.EV_before_associates/(sel.sales*margin)
 st=c.multiple_stats(vals.where(vals>0),min_valid=6)
 sens.append(dict(sensitivity='common EBIT margin all observations',margin=margin,n_valid=st['n_valid'],multiple_median=st['median'],value_per_share=value('ev_ebit',st['median'],T.sales*margin),qualified='pre-associate EV sensitivity, not primary'))
for t in sel.index:
 a=sel.drop(index=t);ad=c.scaled_multiple(a.pe,a.growth,T.growth,driver_scale=100,min_valid=6)
 sens.append(dict(sensitivity='leave-one-out selected peer',removed=t,value_per_share=value('pe',ad['median']),n_valid=ad['n_valid']))
# Target-only special-item diagnostic: vendor EBIT is already before-special-items; report issuer reported EBIT basis too.
sens.append(dict(sensitivity='target-only issuer reported EBIT1015 (after special items -52); NOT harmonized',value_per_share=value('ev_ebit',S[S.multiple.eq('ev_ebit')].iloc[0]['median'],1015)))
pd.DataFrame(sens).to_csv(P/'sensitivities.csv',index=False)
warnings='DRAFT pending human Spot_check. Primary EV/EBIT per bucket-C mapping is qualified: comparable EV excludes associates only where their income is excluded from the denominator, and peer associate/lease/claim data are not uniformly certified — EV rows and the EV/EBIT estimate remain qualified, not unqualified primary evidence. PE and EV/Sales retained as ordered cross-checks. No DCF, recommendation, synthesis weight or residual-band classification.'
(P/'comparables_report.md').write_text('# Vestas comparables — 2026-10-30\n\n'+warnings+'\n\n## Selection\nInitial pool 26 candidates, Europe-first. Numeric selection has '+str(len(sel))+' peers ('+str(int((sel.tier<=2).sum()))+' Tier1/2, '+str(int((sel.tier==3).sum()))+' Tier3, '+str(int(sel.europe.sum()))+' Europe-listed); ordered steps and pool counts in peer_selection.json. Full screens and unresolved evidence gates in evidence_review.md; do not interpret numeric selection as completed human approval. Peer scores use eight required weights, pool-only 5/95 clipping and STDEV.S; fundamental growth across target/pool before exclusions. Exact constrained minimum-distance library selection.\n\n'+sel[['ticker','tier','distance','country','financial_period_end','inclusion_reason']].to_markdown(index=False)+'\n\n## Primary and raw/scaled values\n'+S.to_markdown(index=False)+'\n\n## Bridge and fiscal bases\nFY2025 financials retained at each actual fiscal end (target December; Siemens Energy September; Smiths July). Quote prices/cap at 2026-10-30; FX ECB same date; DKK 7.4735/EUR for the Copenhagen quote. EV supplementary numerator uses debt including leases + NCI book − cash before associates; inverse adds same cash, no double net debt. Target LT investments 739 (equity-investment earnings 7 remain in denominators) recorded not deducted. EV/CF means reported CFO, not unlevered CFO; US GAAP/IFRS interest/lease differences remain (Eaton). Vendor EBITDA definition gap (−26.9% vs issuer for VWS) favours EV/EBIT over EV/EBITDA here.\n\n## Sensitivities\nRaw/scaled p25/median/p75 are peer dispersion, not confidence intervals. Common 4/6/8/10% EBIT margin sensitivity applied to ALL peers/target. Target-only issuer-reported-EBIT diagnostic shown; individual special items −52 are 4.9% of EBIT (below the 10% normalized-alternative trigger). Leave-one-out PE/growth values in sensitivities.csv. Positive extremes retained.\n\n## Benchmarks\nMachinery is the closest Damodaran mapping for turbine/equipment manufacturing; Green & Renewable Energy and Electrical Equipment are business-mix sensitivities, not alternative selected sectors or GICS. EUROPE industry ratios are published ratios, NOT verified medians. Peer medians versus ratios in industry_benchmarks.json; a >50% gap triggers investigation, not data rewriting.\n\n## Sources and audit\nCandidate field-level sources in source_log.csv, official identity links in comparables.csv, selection logs and live scores in comparables_audit.xlsx. Three seeded EV arithmetic rows in Peer_Spot_check; human review explicitly pending.\n')
(P/'valuation_summary.md').write_text('# Relative valuation by regression — Europe, VWS.CO, 2026-10-30\n\n## Headline\nDraft '+chosen['model']+' selected by highest eligible published R2 ('+f"{chosen['published_r2']:.3f}"+'), a weaker heuristic rather than adjusted-R2/industry fit. No EV/EBIT equation exists. Positive NI and equity make all three models computable.\n\n## Data\nFY2025 uniform vendor inputs cross-checked with issuer Annual Report 2025. Denmark listing resolves EUROPE exact, not GLOBAL fallback; diversified global sales are a limitation, not a reason to average equations. Vendor 3Y analyst consensus g_eps32.41%/g_rev8.34% used and labelled (not 5Y); declared payout ~12.8% (DKK0.74 proposed); closing parent ROE '+f"{closing_roe:.4f}"+' for the equations vs average-equity ROE for peer scoring.\n\n## Fitted model\n'+pd.DataFrame(preds)[['model','predicted','published_r2','value_per_share','actual','actual_predicted_gap']].to_markdown(index=False)+'\n\n## Diagnostics\nIntegrity findings retained in regression_results.json. GLOBAL PEG/PBV and EM EVEBITDA source anomalies do not affect these EUROPE equations; those anomalous equations are not used. No n, SEy, adjusted R2, p-values, A/B/C, typicality or D1–D10 available: n/a_published_route. Classification: Not classified (no SEy published).\n\n## Valuation results (sorted from most undervalued to most overvalued)\n'+pd.DataFrame(preds).sort_values('value_per_share',ascending=False)[['model','value_per_share']].to_markdown(index=False)+'\n\n## Robustness\nAll units decimal as approved; EVEBITDA alternative percentage-point DFR/tax prediction saved. Compare Machinery industry ratio, not median. Published EV excludes associate deduction by convention. Live predictions and price bridges reference Inputs; recalculation validation follows in formula_checks.json. Values converted EUR→DKK at ECB 7.4735.\n\n## Key warnings\n'+warnings+'\n\n## Limitations\nMarket-wide, low-R2 equations not sector fair-value proof. January2026 vintage ~304 days old at valuation date. File requires analyst 5Y growth; vendor consensus is 3Y and fundamental growth 0.190 differs — definition gap disclosed. Beta benchmark/frequency unspecified. Published EV definition undocumented. No residual dispersion or confidence range invented. Cash partly customer-advance driven; book NCI/dated balance are proxies.\n\n## Sources\nsource_log.csv; registered regressions_multi_2026-01 SHA '+preds[0]['sha256']+'; official annual report in relative_inputs.md.\n')
print(json.dumps(dict(peers=sel.ticker.tolist(),primary_EV_EBIT_DKK=float(primary.value_per_share_mid),regression=chosen),default=str,indent=2))
report=P/'comparables_report.md'
text=report.read_text()+'\n## Target versus selected peer medians\n'+pd.DataFrame({'target':T[dims], 'peer_median':sel[dims].median()}).to_markdown()+'\n'
report.write_text(text)
