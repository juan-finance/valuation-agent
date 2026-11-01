"""Published-route calculations; fail closed on unverified comparable evidence."""
import json, random
from pathlib import Path
import numpy as np
import pandas as pd
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill
from openpyxl.utils import get_column_letter
from valuation_agent import comparables as c, datasets, published_regressions as pr
from valuation_agent.sourcelog import SourceLog

P=Path(__file__).resolve().parent;ROOT=P.parents[2];DATE='2026-10-30'
D=pd.read_csv(P/'candidate_raw.csv').set_index('ticker',drop=False);T=D.loc['BP']
FX=json.loads((ROOT/'cache/macro'/f'{DATE}.json').read_text())['fx_ecb_reference']['rates']
X=json.loads((P/'issuer_crosschecks.json').read_text())
M=json.loads((P/'fetch_manifest.json').read_text())
MARKET=T.price*T.current_shares_m*FX['USD']/FX['GBP']
claims=T.NCI+X['balance']['preference_equity_difference']
reg_ev=c.comparable_ev(MARKET,T.debt,claims,T.cash,0)
beta_res=datasets.resolve('beta',country='United Kingdom',valuation_date=DATE)
inputs={'g_eps':0.,'g_rev':0.,'beta':T.beta,'payout':T.payout,'roe':T.ni/T.equity,'dfr':T.debt/(T.debt+MARKET),'tax_rate':T.tax_rate,'roic':T.EBIT*(1-T.tax_rate)/(T.equity+T.debt-T.cash)}

def share(dep,multiple,metric=None,debt=None,nci=None,cash=None):
 if dep=='EV/EBITDA':
  e=c.implied_equity_from_ev(multiple,T.EBITDA if metric is None else metric,T.debt if debt is None else debt,claims if nci is None else nci,T.cash if cash is None else cash,0)
 else:e=multiple*(T.ni if dep=='PE' else T.equity)
 return e/T.current_shares_m*FX['GBP']/FX['USD'] if e>0 else np.nan

def dump(file,data):
 (P/file).write_text(json.dumps(data,indent=2,default=lambda v:v.item() if isinstance(v,np.generic) else str(v))+'\n')

def frame(wb,name,d):
 ws=wb.create_sheet(name);ws.append(list(d.columns))
 for row in d.itertuples(index=False,name=None):
  ws.append([None if pd.isna(v) else v.item() if isinstance(v,np.generic) else v for v in row])
 ws.freeze_panes='A2';ws.auto_filter.ref=ws.dimensions
 for cell in ws[1]:cell.font=Font(bold=True,color='FFFFFF');cell.fill=PatternFill('solid',fgColor='17435A')
 for i in range(1,len(d.columns)+1):ws.column_dimensions[get_column_letter(i)].width=24
 return ws

# Hard evidence gates are not numerical filters. Unverified is not passed.
D['missing_score_dimensions']=D[list(c.WEIGHTS)].isna().sum(axis=1)
D['in_default_size_band']=D.market_cap_eur_m.between(.1*T.market_cap_eur_m,10*T.market_cap_eur_m)&D.market_cap_eur_m.ge(1000)
D['in_relaxed_size_band']=D.market_cap_eur_m.between(.05*T.market_cap_eur_m,20*T.market_cap_eur_m)&D.market_cap_eur_m.ge(1000)
D['currency_cap_gate']=D.market_cap_check.abs().le(.02)&D.price_date.eq(DATE)
D['financial_business_gate']='operating oil/gas/refining, not passive investment holding or financial'
D['membership_evidence']=D.membership
D.loc['VARE','membership_evidence']='VAR in cached IEUR tracker, ticker alias VARE -> VAR'
D['ownership_event_history_gate']='not fully verified; stop before qualified selection'
D['assoc_bridge_gate']='not available uniformly; EV before associates is NOT comparable base EV'
D['qualified']=False
D['rejection_reason']='pending issuer/exchange ownership, events, listing history and bridge evidence; benchmark dataset missing'
D.loc['BP','rejection_reason']='target excluded from candidate selection'
D.loc['ORLEN','rejection_reason']='hard exclusion: Poland emerging MSCI country'
D.loc[D.missing_score_dimensions.gt(2),'rejection_reason']='hard exclusion: >2 missing scoring metrics; no unsupported equity/NCI inference'
D.loc[~D.in_relaxed_size_band,'rejection_reason']='hard exclusion: size outside even relaxed band'
D['isin']='unverified'
identities={
 'BP':('GB0007980591',X['identity']['source']),
 'SHEL':('GB00BP6MXD84','https://www.shell.com/investors/results-and-reporting/annual-report/_jcr_content/root/main/section_2113846431/link_list/links/item6.stream/1773292256746/543dfa9bd532f695e4cc282b0e19080eb2e61f00/additional-information-ar25.pdf'),
 'TTE':('FR0000120271','https://totalenergies.com/sites/g/files/nytnzq121/files/documents/totalenergies-shareholders-guide-2025_2025_en.pdf'),
 'EQNR':('NO0010096985','https://live.euronext.com/en/product/equities/NO0010096985-XOSL'),
 'ENI':('IT0003132476','https://www.eni.com/en-IT/investors/remuneration-policy/share.html'),
 'REP':('ES0173516115','https://www.repsol.com/en/shareholders-and-investors/repsol-on-the-stock-exchange/basic-share-data/index.cshtml'),
 'OMV':('AT0000743059','https://www.omv.com/downloads/2025/05/bc48be36-8192-094a-6f5a-f2c9ffe19d82/Dividendenbekanntmachung_2025.pdf'),
 'GALP':('PTGAL0AM0009','https://live.euronext.com/en/search_instruments/GALP'),
 'AKRBP':('NO0010345853','https://live.euronext.com/en/product/equities/NO0010345853-XOSL')}
for t,(isin,url) in identities.items():D.loc[t,['isin','identity_source']]=[isin,url]
D.loc['AKRBP','ownership_event_history_gate']='issuer FY2025 Aker21%, BP16%: target stake under20%; other gates remain pending'
D.loc['AKRBP','ownership_source']='https://akerbp.com/wp-content/uploads/2026/03/akerbp-annual-report-2025.pdf'
D.loc['EQNR','ownership_source']='https://www.equinor.com/investors/our-shareholders'
D.loc['EQNR','ownership_event_history_gate']='issuer Sep2026 Norway67%; unrelated state owner not a target cross-holding; events/history review incomplete'
D.loc['ENI','ownership_source']='https://www.eni.com/en-IT/governance/shareholding-structure.html'
D.loc['REP','ownership_source']='https://www.repsol.com/en/shareholders-and-investors/repsol-on-the-stock-exchange/shareholder-structure/index.cshtml'
D.loc['GALP','ownership_source']='https://www.galp.com/corp/en/investors/information-to-shareholders/shareholding-structure'
D.to_csv(P/'candidate_gates.csv',index=False)

# Numeric-only funnel is an audit of feasibility, NEVER a qualified peer list.
prospects=D.drop(index=['BP','ORLEN']);prospects=prospects[prospects.missing_score_dimensions.le(2)&prospects.currency_cap_gate]
steps=[];last=None;numeric=None
for label,world,lo,hi,cap in [('Europe',False,.1,10,2),('World',True,.1,10,2),('size',True,.05,20,2),('Tier3',True,.05,20,4)]:
 pool=prospects[prospects.market_cap_eur_m.between(lo*T.market_cap_eur_m,hi*T.market_cap_eur_m)&prospects.market_cap_eur_m.ge(1000)]
 if not world:pool=pool[pool.europe]
 score,log=c.similarity_scores(pool,T);scored=pool.join(score)
 tentative,info=c.select_peers(scored,max_tier_3=cap)
 qualified=pool[pool.qualified].join(score)
 selected,qinfo=c.select_peers(qualified,max_tier_3=cap)
 steps.append(dict(step=label,n_numeric=len(pool),numeric_feasibility=info,qualified_feasibility=qinfo,scoring=log,warning='numeric ranking not membership, ownership, event or accounting approval'))
 last=scored;numeric=tentative
 if selected is not None:raise AssertionError('Unexpected qualified selection')
assert last is not None
for n in (9,8):
 _,info=c.select_peers(last[last.qualified],n=n,max_tier_3=4);steps.append(dict(step=f'qualified_shortfall_{n}',result=info))
last.to_csv(P/'candidate_scores.csv',index=False)
if numeric is not None:numeric.to_csv(P/'numeric_prospects_NOT_QUALIFIED.csv',index=False)
dump('peer_selection.json',dict(status='blocked',qualified_count=0,steps=steps,benchmark_resolution=datasets.resolve('ev_ebitda',country='United Kingdom',valuation_date=DATE).summary()))
cols=['target_ticker','comp_ticker','comp_name','comp_isin','distance_score','inclusion_reason','status']
pd.DataFrame(columns=cols).to_csv(P/'comparables.csv',index=False)
rows=[];diagnostic=[]
mults=['pe','peg','relative_pe','ev_ebit','ev_ebitda','ev_cf','pbv','ev_assets','tobins_q','ps','ev_sales']
for name in mults:
 stats=c.multiple_stats([],min_valid=6)
 driver={'pe':'growth','pbv':'roe','ps':'net_margin','ev_sales':'ebitda_margin'}.get(name)
 scaled=c.scaled_multiple([],[],T[driver],driver_scale=100 if name=='pe' else 1,min_valid=6) if driver else {'available':False,'n_valid':0}
 rows.append(dict(target_ticker='BP.L',multiple=name,**stats,adjusted_multiple=scaled.get('median',np.nan),adjusted_n_valid=scaled['n_valid'],value_per_share_mid=np.nan,value_per_share_low=np.nan,value_per_share_high=np.nan,status='blocked: fewer than8 qualified peers, incomplete bridge/benchmark evidence',basis='FY2025',primary_requested=name=='ev_ebitda'))
 if numeric is not None:
  ds=c.multiple_stats(numeric[name].where(numeric[name].gt(0)),min_valid=6)
  adj=c.scaled_multiple(numeric[name].where(numeric[name].gt(0)),numeric[driver],T[driver],driver_scale=100 if name=='pe' else 1,min_valid=6) if driver else {'available':False,'n_valid':0}
  diagnostic.append(dict(multiple=name,**ds,scaled_median=adj.get('median',np.nan),scaled_n=adj['n_valid'],status='UNQUALIFIED candidate diagnostics, not used in valuation; EV BEFORE associates'))
summary=pd.DataFrame(rows);summary.to_csv(P/'multiples_summary.csv',index=False)
pd.DataFrame(diagnostic).to_csv(P/'candidate_multiple_diagnostics.csv',index=False)

preds=[];res=None
for dep in ['PE','PBV','EV/EBITDA']:
 eq,res,meta=datasets.equation_for('United Kingdom',dep,DATE)
 val=pr.predict(eq,inputs,unit_policy='as_published_note');both=pr.predict_both_policies(eq,inputs)
 actual={'PE':T.pe,'PBV':T.pbv,'EV/EBITDA':reg_ev/T.EBITDA}[dep]
 status='conditional point estimate' if dep=='EV/EBITDA' else 'not selected: near-zero reported NI and extreme payout' if dep=='PE' else 'not valued: negative prediction'
 preds.append(dict(model=dep,predicted=val,published_r2=eq.r2,actual=actual,deviation=actual/val-1 if val>0 else None,value_per_share_gbp=share(dep,val) if val>0 else np.nan,unit_policies=both,status=status,equation=eq.raw,dataset=res.dataset.dataset_id,as_of=str(res.dataset.as_of_date),vintage=res.dataset.vintage,sha256=res.dataset.sha256,region=meta,integrity=[dict(severity=f.severity,code=f.code,message=f.message) for f in datasets.check_dataset(res.dataset)]))
assert res is not None
chosen=next(p for p in preds if p['model']=='EV/EBITDA')
dump('regression_results.json',dict(inputs=inputs,predictions=preds,chosen=chosen['model'],status='provisional',substituted_input='approved fundamental closing-common ROE x capped retention g_eps=0; g_rev=g_eps fallback; 3Y analyst fields retained separately, NOT passed as 5Y'))

reg=Workbook();reg.remove(reg.active)
values={'price_gbp':T.price,'shares_m':T.current_shares_m,'GBP_per_EUR':FX['GBP'],'USD_per_EUR':FX['USD'],'market_equity_usdm':MARKET,'debt':T.debt,'nci':T.NCI,'preference':21.,'cash':T.cash,'ni':T.ni,'equity':T.equity,'EBIT':T.EBIT,'EBITDA':T.EBITDA,'tax_expense':6451.,'pretax':7746.,'dividends':5058.,'beta_u_cash_corrected':.41,'marginal_tax':.2471,**inputs}
IR={k:i for i,k in enumerate(values,2)}
ws=frame(reg,'Inputs',pd.DataFrame([dict(input=k,value=v,basis='USD millions / decimals unless named otherwise; FY2025',source_id='S3_vendor_BP' if k not in ('beta_u_cash_corrected','marginal_tax') else 'S3_beta') for k,v in values.items()]))
ref=lambda k:f'Inputs!B{IR[k]}'
F={'market_equity_usdm':f'={ref("price_gbp")}*{ref("shares_m")}*{ref("USD_per_EUR")}/{ref("GBP_per_EUR")}',
 'payout':f'={ref("dividends")}/{ref("ni")}', 'roe':f'={ref("ni")}/{ref("equity")}',
 'g_eps':f'={ref("roe")}*(1-MIN({ref("payout")},1))','g_rev':f'={ref("g_eps")}',
 'beta':f'={ref("beta_u_cash_corrected")}*(1+(1-{ref("marginal_tax")})*{ref("debt")}/{ref("market_equity_usdm")})',
 'dfr':f'={ref("debt")}/({ref("debt")}+{ref("market_equity_usdm")})',
 'tax_rate':f'={ref("tax_expense")}/{ref("pretax")}',
 'roic':f'={ref("EBIT")}*(1-{ref("tax_rate")})/({ref("equity")}+{ref("debt")}-{ref("cash")})'}
for k,f in F.items():ws.cell(IR[k],2,f)
ps=frame(reg,'Predictions',pd.DataFrame(columns=['model','R2','status','predicted_multiple','alternate_unit_multiple','equity_usdm','GBP_per_share','actual_multiple','deviation']))
for i,p in enumerate(preds,2):
 dep=p['model'];eq,rs,_=datasets.equation_for('United Kingdom',dep,DATE);sn='Coef_'+dep.replace('/','_')
 cf=pd.DataFrame([dict(term='constant',coefficient=eq.constant,published_t=eq.constant_tstat,dataset=rs.dataset.dataset_id,as_of=str(rs.dataset.as_of_date),sha256=rs.dataset.sha256)]+[dict(term=t.variable,coefficient=t.coef,published_t=t.tstat,dataset=rs.dataset.dataset_id,as_of=str(rs.dataset.as_of_date),sha256=rs.dataset.sha256) for t in eq.terms]);frame(reg,sn,cf)
 formula=f'={sn}!B2';alternate=formula
 for j,t in enumerate(eq.terms,3):
  term=ref(t.variable);term=f'LN({term})' if t.transform=='ln' else term
  formula+=f'+{sn}!B{j}*{term}'
  alternate+=f'+{sn}!B{j}*{term}'+('*100' if t.variable in ('dfr','tax_rate') else '')
 if dep=='EV/EBITDA':bridge=f'=D{i}*{ref("EBITDA")}-{ref("debt")}-{ref("nci")}-{ref("preference")}+{ref("cash")}'
 else:bridge=f'=D{i}*{ref("ni" if dep=="PE" else "equity")}'
 ps.append([dep,eq.r2,p['status'],formula,alternate,bridge,f'=F{i}/{ref("shares_m")}*{ref("GBP_per_EUR")}/{ref("USD_per_EUR")}',p['actual'],f'=IF(D{i}>0,H{i}/D{i}-1,NA())'])
frame(reg,'Sources',pd.DataFrame([dict(source_id='S3_vendor_BP',URL=T.source_urls),dict(source_id='S3_beta',URL=beta_res.dataset.path),dict(source_id='S3_equations',URL=res.dataset.path),dict(source_id='S3_bridge',URL=X['balance']['source'])]))
reg.save(P/'regression_valuation.xlsx')

sens=[]
for label,metric in [('EBITDA -20% mechanical stress',T.EBITDA*.8),('base vendor EBITDA',T.EBITDA),('EBITDA +20% mechanical stress',T.EBITDA*1.2),('issuer PBIT + DDA parallel',30464),('issuer impairment-addback parallel',36501)]:
 sens.append(dict(scenario=label,EBITDA_usdm=metric,multiple_held_fixed=chosen['predicted'],GBP_per_share=share('EV/EBITDA',chosen['predicted'],metric),note='mechanical conditional sensitivity, not commodity forecast or peer dispersion'))
sens.append(dict(scenario='full FY decommissioning provision as incremental debt-like claim',EBITDA_usdm=T.EBITDA,multiple_held_fixed=chosen['predicted'],GBP_per_share=share('EV/EBITDA',chosen['predicted'],nci=claims+12253),note='conservative stress only; may double-count operating provision economics, not base'))
sens.append(dict(scenario='percentage-point DFR/tax unit alternative',EBITDA_usdm=T.EBITDA,multiple_held_fixed=chosen['unit_policies']['dfr_tax_percent_points'],GBP_per_share=share('EV/EBITDA',chosen['unit_policies']['dfr_tax_percent_points']),note='not user-approved base; illustrative unit risk'))
S=pd.DataFrame(sens);S.to_csv(P/'sensitivities.csv',index=False)
pd.DataFrame([dict(scenario=s,Brent_USD_bbl=b,Henry_Hub_USD_mmbtu=g,calibration='analyst-set scenario assumptions, not observed prices or forecasts',EBITDA_mapping='not available; no sourced commodity sensitivity model') for s,b,g in [('low',55,2.5),('base',70,4),('high',85,5.5)]]).to_csv(P/'commodity_deck.csv',index=False)

random_tickers=sorted(random.Random(20261030).sample(list(last.index),3))
checks=[]
for t in random_tickers:
 r=last.loc[t];raw=r.pe*r.ni if r.ni>0 else r.market_cap_eur_m*FX[r.report_currency]
 ev=c.comparable_ev(raw,r.debt,r.NCI,r.cash,0)
 checks.append(dict(ticker=t,market_equity_report_m=raw,debt=r.debt,NCI=r.NCI,cash=r.cash,EV_before_associates=ev,recompute_match=bool(np.isclose(ev,r.EV_before_associates,equal_nan=True)),scope='numeric candidates, not selected peers',source=r.source_urls,human_status='pending; not performed',comparable_EV_status='blocked; associates and other claims not harmonized'))
pd.DataFrame(checks).to_csv(P/'EV_spot_checks.csv',index=False)
audit=Workbook();audit.remove(audit.active)
for name,data in [('Candidate_Pool',D.reset_index(drop=True)),('Numeric_Scores',last.reset_index(drop=True)),('Qualified_Peers',pd.DataFrame(columns=cols)),('Multiples',summary),('Sensitivity',S),('EV_check',pd.DataFrame(checks)),('Score_Parameters',pd.DataFrame([dict(metric=k,weight=v,**steps[-3]['scoring']['params'].get(k,{})) for k,v in c.WEIGHTS.items()]))]:frame(audit,name,data)
audit.save(P/'comparables_audit.xlsx')

out=dict(company='BP p.l.c.',ticker='BP.L',isin=X['identity']['isin'],gics_sector='Energy (cached proxy; bucket F is not GICS)',primary_regression='published_damodaran_EUROPE_2026-01',chosen_model='EV/EBITDA',predicted_primary=chosen['predicted'],actual_multiple=chosen['actual'],deviation=chosen['deviation'],published_r2=chosen['published_r2'],implied_value_per_share=chosen['value_per_share_gbp'],currency='GBP',current_price=T.price,upside=chosen['value_per_share_gbp']/T.price-1,classification='Not classified (no SEy published)',units_policy='as_published_note (user-approved decimal)',units_unverified='no (standing approval)',equation_dataset_id=res.dataset.dataset_id,substituted_input='g_eps=0 fundamental closing-common ROE x capped retention; g_rev=g_eps fallback; 3Y consensus not passed as 5Y',second_model='PE',second_predicted=preds[0]['predicted'],second_status=preds[0]['status'],third_model='PBV',third_predicted=preds[1]['predicted'],third_status=preds[1]['status'],damodaran_global='not used until verified: global PBV sign anomaly; no averaging regions',damodaran_western_europe_uk=chosen['predicted'],status='provisional conditional estimate; comparable method blocked',rationale='EVEBITDA is the business-appropriate positive prediction; higher-R2 PBV predicts negative; PE has near-zero earnings and extreme payout. Ranking by published R2 is only a weak project heuristic, no own-estimation diagnostics.',source_urls=T.source_urls)
for k in ['typicality_result','failed_test','adj_r2','predicted_A','predicted_B','predicted_C','residual','std_residual','sector_dummy_coef','SEy','p_values','D1_D10']:out[k]='n/a_published_route'
pd.DataFrame([out]).to_csv(P/'valuation_multiples.csv',index=False)

log=SourceLog(P.parent/'source_log.csv');known={r['url_or_local_file'] for r in log.rows}
sources={x['url']:('StockAnalysis uniform source',DATE,'FY2025 / quote date separately identified') for x in M}
for k in ['income','balance','claims','decommissioning','normalization','identity']:sources[X[k]['source']]=('BP issuer source','2025-12-31',k)
sources[res.dataset.path]=('Damodaran published equations',str(res.dataset.as_of_date),'dataset '+res.dataset.dataset_id+' sha256 '+res.dataset.sha256)
sources[beta_res.dataset.path]=('Damodaran Europe beta',str(beta_res.dataset.as_of_date),'dataset '+beta_res.dataset.dataset_id+' sha256 '+beta_res.dataset.sha256+'; exact Oil/Gas (Integrated); cash corrected unlevered beta .41; metadata marginal tax24.71%')
for t,(isin,url) in identities.items():sources[url]=(t+' issuer/exchange identity',DATE,isin)
for i,(url,(name,asof,note)) in enumerate(sources.items(),1):
 if url in known:continue
 log.add(input_id=f'S3_source_{i}',company='BP / candidate audit',metric='source-level extract',value='see candidate tables / issuer_crosschecks / workbook',unit='mixed',as_of_date=asof,access_date='2026-11-01',source_name=name,url_or_local_file=url,page_note_sheet_cell=note,status='sourced',limitation='one row per source per relative_only deviation; human review not implied')
log.save()

warnings='PROVISIONAL. Comparable valuation BLOCKED: no certified peer panel, missing uniform associate/other-claims adjustments and no registered matching Damodaran industry-median dataset. Human Spot_check pending, never asserted performed. No target peer price or upside is reported. Candidate scores are an audit, not a compliant selected panel.'
(P/'comparables_report.md').write_text('# BP.L comparable method — 2026-10-30\n\n'+warnings+'\n\n## Scope and target profile\nBP is an integrated upstream oil/gas, LNG and downstream group; no single dominant revenue segment was verified. An integrated economic profile, not a fabricated >=50% segment claim, guides Tier1 seeds; E&P/refining Tier2 exposures differ. Initial pool24 plus target; FY2025/Dec31 basis; web_minimum; all data agent-researched. Ordinary-share FX/GBX treatment in input memo. No separate MSCI regression market sample.\n\n## Funnel\nNumeric gates, all rejections, source links and incomplete evidence gates are in candidate_gates.csv. Europe -> World -> 0.05–20 size -> Tier3 cap4; numeric scores recomputed each step; qualified selection attempted at10 then9 then8 after all relaxations. Actual qualified count0: stop below8, never pad. IEUR2026-10-29 holdings are only a dated membership proxy. World membership and remaining ownership/restructuring/listing evidence have not been certified. Raw missing NCI/common equity stays unavailable, not zero.\n\n## Arithmetic and accounting\nEight library weights sum1; pool-only P5/P95, sample SD, raw target z, pairwise renormalization, zero-SD and missing logs in peer_selection.json. Web growth fundamental for whole pool. Full11 multiple rows retained; all qualified n_valid0, no valuation. Candidate diagnostic medians/means/quartiles retained in separate file, NOT used. Positive extremes untrimmed. All candidate EV is BEFORE associates; not comparable base EV. PE growth scaling unavailable for target zero growth. Relative PE lacks matching index PE; Tobin Q lacks replacement cost. EV/CFO is reported CFO, not unlevered cash flow; IFRS/US GAAP interest/lease differences not harmonized. Three reproducible numeric candidate EV checks are not selected-peer verification.\n\n## Stops and remedy\nResolver could not find ev_ebitda industry data; do not invent a Damodaran median or relabel an aggregate. Supply a verified matching Europe industry-median dataset with statistic/period definitions. Finish hard-gate and uniform bridge evidence before resuming selection. A qualified primary EV/EBITDA set cannot be replaced by an attractive PE on BP near-zero NI. Peer-set/quartile sensitivity and required selected-peer ISIN/spot checks remain blocked, not passed.\n\n## Normalization and commodity exposure\nReported base retained. Separate issuer impairments addback and underlying RC reconciliation in issuer_crosschecks.json; no uniform peer normalization invented. commodity_deck.csv explicitly assumed Brent55/70/85 and HH2.5/4/5.5, not price observations; no sourced commodity-to-EBITDA mapping. sensitivities.csv provides mechanical EBITDA and claim tests only.\n\nAcademic analysis only, not investment advice.\n')
headings=['# Relative valuation by regression — BP.L, Europe, 2026-10-30','## Headline','## Data','## Fitted model','## Diagnostics','## Valuation results (sorted from most undervalued to most overvalued)','## Robustness','## Key warnings','## Limitations','## Sources']
contents=['',f'Conditional market-wide EV/EBITDA {chosen["predicted"]:.6f}x, GBP{chosen["value_per_share_gbp"]:.4f}/ordinary share; NOT a recommendation. Published R2 {chosen["published_r2"]:.1%}. Comparable method blocked, so no independent corroboration. The large gap to GBP6.274 is model/definition risk, not evidence of mispricing.', 'Uniform vendor FY2025 fields retained; issuer cross-checks and claim scope separate. Growth substitution is approved fundamental g_eps=0 (closing common ROE x capped retention), g_rev=g_eps fallback; sourced3Y consensus12.99%/2.45% does NOT meet next5Y definition and is not passed as such. Beta negative replaced using resolved cash-corrected unlevered industry beta .41 and source marginal tax24.71%. Payout93.6667 retained; only retention capped. Regression ROE closing common, peer ROE average common. DFR gross debt / debt+current equity. Effective tax expense/pretax. Fiscal bridge frozen at Dec31,2025; quote Oct30,2026, not a current net-debt estimate.', '\n\n'.join(p['equation']+f'\nPublished R2={p["published_r2"]}; status={p["status"]}' for p in preds), 'n/a_published_route: n, SEy, p-values, adjustedR2, A/B/C, typicality, D1–D10, residual classification, own-estimation sample schema and LINEST. Integrity finds EUROPE views agree; flagged GLOBAL PEG sign/identical-t and GLOBAL PBV sign and EM EV/EBITDA sign are NOT used. DFR/tax ambiguity addressed by standing decimal approval, both policies disclosed. Recalculation/library comparison is saved separately.', pd.DataFrame([{k:p[k] for k in ['model','predicted','published_r2','actual','deviation','value_per_share_gbp','status']} for p in preds]).sort_values('value_per_share_gbp',ascending=False,na_position='last').to_markdown(index=False),S.to_markdown(index=False)+'\nAlternative policy numbers in regression_results.json. No fake Global-equation check or robustness refit. Peer plausibility check unavailable because the qualified sector median is blocked; candidate diagnostics explicitly unqualified.', warnings+'\nRegulatory/commodity exposure, extreme payout, tiny NI and high effective tax make extrapolation severe. Negative PBV never clipped to zero. PE considered but not primary for integrated oil earnings distorted by impairments.', 'Equations Jan1,2026 are302 days old, >6months. Market-wide, lowR2, no sector structure or residual dispersion. Approved growth proxy differs from analyst5Y growth. Damodaran EV/invested-capital definitions undocumented. Regression EV retains associates; peer EV removes them only when earnings excluded. Debt72,529 includes leases14,571. NCI20,948 includes hybrid15,955; no double deduction. Preference21 carrying proxy deducted separately. No associates addback in regression inverse. Common equity53,031 excludes preference. Fiscal claims stale vs quote; current bridge and fair values could differ materially. No DCF-proximity tuning, blending, recommendation, stage4 or DATA_BASE_MSCI.xlsx.',T.source_urls+'\n'+X['balance']['source']+'\n'+res.dataset.path+' sha256 '+res.dataset.sha256+'\nSee source_log.csv (one row/source) and issuer_crosschecks.json. Academic analysis only; not investment advice.']
(P/'valuation_summary.md').write_text('\n\n'.join(h+'\n'+v for h,v in zip(headings,contents))+'\n')
print(json.dumps({'qualified_peers':0,'regression':out,'sensitivity':sens},indent=2,default=str))
