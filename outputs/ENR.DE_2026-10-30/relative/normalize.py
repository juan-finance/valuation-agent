"""Uniform FY2025 raw-field extraction, no vendor multiple substitution."""
import json,re,runpy
from pathlib import Path
import numpy as np
import pandas as pd
from valuation_agent import comparables as c
P=Path(__file__).resolve().parent;ROOT=P.parents[2];C=ROOT/'cache/market/2026-10-30/candidates'
helpers=runpy.run_path(str(ROOT/'outputs/ALFA.ST_2026-10-30/relative/prepare_pool.py'))
tables=helpers['table_fields'];field=helpers['field'];number=helpers['number']
cfg=runpy.run_path(str(P/'collect.py')); candidates=cfg['CANDIDATES'];F=cfg['F']
FX=json.loads((ROOT/'cache/macro/2026-10-30.json').read_text())['fx_ecb_reference']['rates'];FX['EUR']=1
U=pd.read_csv(ROOT/'cache/market/2026-10-30/universe.csv').fillna('')
aliases={'ENR':'SIEMENS ENERGY','VWS':'VESTAS','NDX1':'NORDEX','ABBN':'ABB LTD','SU':'SCHNEIDER','LR':'LEGRAND','PRY':'PRYSMIAN','NKT':'NKT','NEX':'NEXANS','SIE':'^SIEMENS N','WRT1V':'WARTSILA','ANDR':'ANDRITZ','SUN':'SULZER','ALFA':'ALFA LAVAL','ATCO.A':'ATLAS COPCO CLASS A','SAND':'SANDVIK','METSO':'METSO','WEIR':'WEIR GROUP','IMI':'^IMI ','ROR':'ROTORK','SPX':'SPIRAX','G1A':'GEA','SKF.B':'^SKF B$','SMIN':'SMITHS','EPI.A':'EPIROC CLASS A'}
rows=[]
for ticker,name,route,tier,reason in candidates:
 income,cols=tables(ticker,'financials');bs,_=tables(ticker,'financials_balance-sheet');cf,_=tables(ticker,'financials_cash-flow-statement');st,_=tables(ticker,'statistics');hist,_=tables(ticker,'history')
 if not income:continue
 member=U[U.name.str.contains(aliases.get(ticker,'^NEVER$'),case=False,regex=True)]
 if ticker=='WEIR':member=U[U.ticker.eq('WEIR')]
 if ticker=='G1A':member=U[U.name.str.match('GEA GROUP',case=False)]
 if len(member)!=1:print('membership',ticker,len(member))
 qccy=member.iloc[0].currency if len(member)==1 else 'USD'
 country=member.iloc[0].country_listing if len(member)==1 else 'United States'
 base='https://stockanalysis.com/'+(route if route.startswith('stocks/') else 'quote/'+route)+'/'
 ir=F.get(base+'financials/income-statement/')
 if ir.ok:
  for i,t in enumerate(helpers['html_tables'](ir.text())):
   if getattr(t.columns,'nlevels',1)>1:
    periods={str(k[0]):str(k[1]) for k in t.columns};t.columns=[str(k[0]) for k in t.columns]
    income['Period Ending']={k:v for k,v in periods.items() if k in ['FY 2025','FY 2024']}
   for _,r in t.iterrows():income[str(r.iloc[0])]={str(k):r[k] for k in t.columns[1:]}
   t=t[[t.columns[0]]+[k for k in ['FY 2025','FY 2024'] if k in t.columns]]
   t.to_csv(C/f'ENRpool_{ticker}_income_{i}.csv',index=False)
 # Existing extracts retain their original units; cached source response supplies metadata only.
 text=F.get(base+'financials/').text();unit=re.search(r'Financials in (millions|billions) ([A-Z]{3})',text)
 if not unit:print('missing units',ticker);continue
 fccy=unit[2];factor=1000 if unit[1]=='billions' else 1
 fy='FY 2025';prev='FY 2024'
 fin=lambda k:field(income,k,fy)*factor
 bal=lambda k,y=fy:field(bs,k,y)*factor
 cashflow=lambda k:field(cf,k,fy)*factor
 ni=fin('Net Income');sales=fin('Revenue');ebit=fin('Operating Income');da=cashflow('Depreciation & Amortization')
 otherda=cashflow('Other Amortization');da=da+(otherda if np.isfinite(otherda) else 0)
 eq=bal('Total Common Equity');eqprev=bal('Total Common Equity',prev);debt=bal('Total Debt');cash=bal('Cash & Equivalents');nci=bal('Minority Interest')
 if not np.isfinite(nci):
  totaleq=bal('Total Equity');nci=totaleq-eq if np.isfinite(totaleq) and np.isfinite(eq) else np.nan
 # Financials label absent dividends with '-' when no payment; verify explicit FY DPS=0 too.
 div=cashflow('Common Dividends Paid');dps=fin('Dividend Per Share')/factor
 if not np.isfinite(div) and dps==0:div=0
 if ticker in ['ENR','NDX1']:div=0 # issuer FY cash distributions: no common payment
 payout=abs(div)/ni if ni>0 else np.nan;roe=ni/((eq+eqprev)/2) if eq+eqprev>0 else np.nan
 growth=roe*(1-min(payout,1)) if roe>0 and payout>=0 else np.nan
 capex=abs(cashflow('Capital Expenditures'));cfo=cashflow('Operating Cash Flow');assets=bal('Total Assets')
 mcap=field(st,'Market Cap','1');shares=field(st,'Shares Outstanding','1');beta=field(st,'Beta (5Y)','1')
 hp=F.get(base+'history/');ht=helpers['html_tables'](hp.text()) if hp.ok else []
 price=np.nan
 for h in ht:
  if 'Date' in h and 'Close' in h:
   match=h[h.Date.astype(str).str.contains('Oct 30, 2026',regex=False)]
   if len(match):price=number(match.iloc[0]['Close']);break
 rawprice=price
 if qccy=='GBP':price=c.pence_to_pounds(price)
 cap_error=price*shares/mcap-1 if mcap>0 else np.nan
 # Uniform class-level capitalization; unresolved vendor dual-class perimeter rejected in gates.
 market_fin=mcap*FX[fccy]/FX[qccy];capeur=mcap/FX[qccy]
 ev=c.comparable_ev(market_fin,debt,nci,cash,0) if np.isfinite(nci) else np.nan
 ebitda=fin('EBITDA');da=fin('D&A For EBITDA')
 row=dict(ticker=ticker,name=name,tier=tier,hypothesis=reason,europe=len(member)==1,country=country,quote_currency=qccy,report_currency=fccy,valuation_date='2026-10-30',price_date='2026-10-30' if np.isfinite(price) else 'unavailable',price=price,raw_price=rawprice,current_shares_m=shares,market_cap_quote_m=mcap,market_cap_eur_m=capeur,ln_mcap=np.log(capeur),market_cap_check=cap_error,financial_period_end=income.get('Period Ending',{}).get(fy,''),earnings_basis='FY2025',growth_basis='fundamental average-parent-equity ROE times capped retention',ni=ni,sales=sales,EBIT=ebit,DA=da,EBITDA=ebitda,equity=eq,equity_prior=eqprev,assets=assets,debt=debt,cash=cash,NCI=nci,associates=np.nan,EV_before_associates=ev,roe=roe,payout=payout,growth=growth,beta=beta,net_debt_ebitda=(debt-cash)/ebitda if ebitda>0 else np.nan,ebitda_margin=ebitda/sales,capex=capex,capex_sales=capex/sales,cfo=cfo,net_margin=ni/sales,pretax=fin('Pretax Income'),tax=fin('Income Tax Expense'),pe=market_fin/ni if ni>0 else np.nan,pbv=market_fin/eq if eq>0 else np.nan,ps=market_fin/sales,ev_ebit=ev/ebit if ebit>0 and ev>0 else np.nan,ev_ebitda=ev/ebitda if ebitda>0 and ev>0 else np.nan,ev_cf=ev/cfo if cfo>0 and ev>0 else np.nan,ev_assets=ev/assets if ev>0 else np.nan,ev_sales=ev/sales if ev>0 else np.nan,relative_pe=np.nan,tobins_q=np.nan,membership='IEUR MSCI Europe IMI proxy Oct29 (not standard index)' if len(member)==1 else 'unverified',source_urls=base+'financials/ | '+base+'financials/balance-sheet/ | '+base+'financials/cash-flow-statement/ | '+base+'statistics/ | '+base+'history/; accessed 2026-11-01')
 row['peg']=row['pe']/(100*growth) if growth>0 else np.nan
 rows.append(row)
pd.DataFrame(rows).to_csv(P/'candidate_raw.csv',index=False)
print(pd.DataFrame(rows)[['ticker','market_cap_eur_m','market_cap_check','financial_period_end','EBIT','ni','payout','growth']].to_string(index=False))
