"""Preserve raw vendor fiscal fields; no selective issuer overwrites."""
import json, re
from pathlib import Path
import numpy as np
import pandas as pd
from valuation_agent import comparables as c, datasets
from valuation_agent.regression import replace_beta
from collect import CANDIDATES
P=Path(__file__).resolve().parent; ROOT=P.parents[2]
C=ROOT/'cache/market/2026-10-30/candidates'
FX=json.loads((ROOT/'cache/macro/2026-10-30.json').read_text())['fx_ecb_reference']['rates']|{'EUR':1}
U=pd.read_csv(ROOT/'cache/market/2026-10-30/universe.csv').fillna('')

def num(v):
 s=str(v).replace(',','').replace('−','-').strip()
 if s.endswith('%'):return float(s[:-1])/100
 for a,b in [('T',1e6),('B',1e3),('M',1),('K',.001)]:
  if s.endswith(a):return float(s[:-1])*b
 try:return float(s)
 except ValueError:return np.nan

def fields(ticker,page):
 out={}
 for f in sorted(C.glob(f'BPpool_{ticker}_{page}_*.csv')):
  t=pd.read_csv(f).fillna('')
  for _,r in t.iterrows():out[str(r.iloc[0])]={k:r[k] for k in t.columns[1:]}
 return out

def get(d,k,col='FY 2025'):
 if k not in d:
  k=next((x for x in d if x.startswith(k+' ')),k)
 return num(d.get(k,{}).get(col,np.nan))

def normalize():
 M=json.loads((P/'fetch_manifest.json').read_text());rows=[]
 for ticker,name,route,tier,reason in CANDIDATES:
  meta=next((x for x in M if x['ticker']==ticker and x['page']=='financials/income-statement/'),None)
  if not meta or meta['status']!=200:continue
  f=fields(ticker,'financials_income-statement');b=fields(ticker,'financials_balance-sheet');cf=fields(ticker,'financials_cash-flow-statement');s=fields(ticker,'statistics')
  if not f:continue
  unit=next((x for x in meta['units'] if x.startswith('Financials')),None)
  if not unit:print('NO UNITS',ticker);continue
  fccy=unit.split()[-1];factor=1000 if 'billions' in unit else 1
  financial=lambda k:get(f,k)*factor
  balance=lambda k,col='FY 2025':get(b,k,col)*factor
  cashflow=lambda k:get(cf,k)*factor
  member=U[U.ticker.eq(ticker)]
  # Explicit listing-currency metadata, independent of reporting currency.
  exchange=route.split('/')[1] if route.startswith('quote') else 'US'
  qc={'lon':'GBP','epa':'EUR','osl':'NOK','bit':'EUR','bme':'EUR','vie':'EUR','eli':'EUR','hel':'EUR','wse':'PLN','asx':'AUD','US':'USD'}[exchange]
  country={'lon':'United Kingdom','epa':'France','osl':'Norway','bit':'Italy','bme':'Spain','vie':'Austria','eli':'Portugal','hel':'Finland','wse':'Poland','asx':'Australia','US':'United States'}[exchange]
  if ticker in ('SU','CNQ'):country='Canada'
  price=np.nan
  for path in C.glob(f'BPpool_{ticker}_history_*.csv'):
   h=pd.read_csv(path)
   if 'Date' in h and 'Close' in h:
    x=h[h.Date.eq('Oct 30, 2026')]
    if len(x):price=num(x.iloc[0]['Close'])
  raw_price=price
  if qc=='GBP':price=c.pence_to_pounds(price)
  shares=get(s,'Shares Outstanding','1');vendor_cap=get(s,'Market Cap','1')
  mcap=price*shares;fin_eq=mcap*FX[fccy]/FX[qc]
  ni=financial('Net Income to Common');eq=balance('Total Common Equity');prior=balance('Total Common Equity','FY 2024')
  sales=financial('Revenue');ebit=financial('EBIT');ebitda=financial('EBITDA')
  debt=balance('Total Debt');cash=balance('Cash & Equivalents');nci=balance('Minority Interest')
  div=abs(cashflow('Common Dividends Paid'));payout=div/ni if ni>0 else np.nan
  roe=ni/((eq+prior)/2) if eq+prior>0 else np.nan
  growth=roe*(1-min(payout,1)) if roe>0 and payout>=0 else np.nan
  beta_raw=get(s,'Beta (5Y)','1');beta=beta_raw;beta_note='observed vendor 5Y, index/frequency unavailable'
  if not np.isfinite(beta) or beta<0 or beta>2.5:
   r=datasets.resolve('beta',country=country,valuation_date='2026-10-30');df=datasets.load_industry(r.dataset)
   industry='Oil/Gas (Integrated)' if tier==1 else 'Oil/Gas (Production and Exploration)'
   bu=datasets.get_value(df,'beta',industry,'beta_unlevered_cash_corrected')
   # Registered Europe marginal tax convention, not effective tax rate.
   tax=0.2471  # Resolved beta Europe dataset metadata: Marginal Tax Rate Used, 24.71%.
   beta,_,beta_note=replace_beta(beta_raw,bu,tax,debt/fin_eq)
  capex=abs(cashflow('Capital Expenditures'));cfo=cashflow('Operating Cash Flow');assets=balance('Total Assets')
  ev=c.comparable_ev(fin_eq,debt,nci,cash,0) if np.isfinite(nci) else np.nan
  period=f.get('Period Ending',{}).get('FY 2025','unavailable')
  row=dict(ticker=ticker,name=name,tier=tier,hypothesis=reason,europe=exchange not in ('US','asx'),country=country,quote_currency=qc,report_currency=fccy,valuation_date='2026-10-30',price_date='2026-10-30' if np.isfinite(price) else 'unavailable',price=price,raw_price=raw_price,current_shares_m=shares,market_cap_quote_m=mcap,vendor_market_cap_quote_m=vendor_cap,market_cap_check=mcap/vendor_cap-1,market_cap_eur_m=mcap/FX[qc],ln_mcap=np.log(mcap/FX[qc]),financial_period_end=period,earnings_basis='FY2025',ni=ni,sales=sales,EBIT=ebit,EBITDA=ebitda,DA=financial('D&A For EBITDA'),equity=eq,equity_prior=prior,debt=debt,cash=cash,NCI=nci,associates=np.nan,EV_before_associates=ev,roe=roe,payout=payout,growth=growth,beta=beta,beta_raw=beta_raw,beta_note=beta_note,net_debt_ebitda=(debt-cash)/ebitda if ebitda>0 else np.nan,ebitda_margin=ebitda/sales,capex=capex,capex_sales=capex/sales,cfo=cfo,assets=assets,net_margin=ni/sales,tax_rate=financial('Income Tax Expense')/financial('Pretax Income'),g_eps=get(s,'EPS Growth Forecast (3Y)','1'),g_rev=get(s,'Revenue Growth Forecast (3Y)','1'),source_urls=' | '.join(x['url'] for x in M if x['ticker']==ticker),membership='cached IEUR proxy' if len(member) else 'requires World/listing verification',growth_basis='fundamental ROE x capped retention, average common equity')
  for k,den in [('pe',ni),('pbv',eq),('ps',sales)]:row[k]=fin_eq/den if den>0 else np.nan
  for k,den in [('ev_ebit',ebit),('ev_ebitda',ebitda),('ev_cf',cfo),('ev_assets',assets),('ev_sales',sales)]:row[k]=ev/den if ev>0 and den>0 else np.nan
  row.update(peg=row['pe']/(100*growth) if growth>0 else np.nan,relative_pe=np.nan,tobins_q=np.nan)
  rows.append(row)
  pd.DataFrame([row]).to_csv(C/f'BPpool_{ticker}.csv',index=False)
 D=pd.DataFrame(rows);D.to_csv(P/'candidate_raw.csv',index=False);print(D[['ticker','price','market_cap_check','ni','EBITDA','growth','beta']].to_string(index=False))
 return D
if __name__=='__main__':normalize()
