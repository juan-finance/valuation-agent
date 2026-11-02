"""Normalize VER.VI candidate pool from cached stockanalysis JSON extracts."""
import json, re, io
from pathlib import Path
import numpy as np
import pandas as pd
from lxml import html
from valuation_agent.cachefetch import CachedFetcher, html_tables
from valuation_agent import comparables as comp
from collect import CANDIDATES

P=Path(__file__).resolve().parent; ROOT=P.parents[2]; C=ROOT/'cache/market/2026-10-30/candidates'
FX=json.loads((ROOT/'cache/macro/2026-10-30.json').read_text())['fx_ecb_reference']['rates']; FX['EUR']=1
U=pd.read_csv(ROOT/'cache/market/2026-10-30/universe.csv').fillna('')
M=json.loads((P/'fetch_manifest.json').read_text())
fetch=CachedFetcher(str(ROOT/'cache/web/2026-10-30'),min_delay=1.1,user_agent='ValuationResearchAI/1.0 (educational research; respects robots.txt)')
EXCH={'lon':'GBP','epa':'EUR','osl':'NOK','bit':'EUR','bme':'EUR','vie':'EUR','eli':'EUR','hel':'EUR','wse':'PLN','asx':'AUD','etr':'EUR','sto':'SEK','cph':'DKK','tsx':'CAD','swx':'CHF','prg':'CZK','US':'USD'}
CTRY={'lon':'United Kingdom','epa':'France','osl':'Norway','bit':'Italy','bme':'Spain','vie':'Austria','eli':'Portugal','hel':'Finland','wse':'Poland','asx':'Australia','etr':'Germany','sto':'Sweden','cph':'Denmark','tsx':'Canada','swx':'Switzerland','prg':'Czech Republic','US':'United States'}

def number(s):
 s=str(s).replace(',','').replace('−','-').strip()
 if s in ['','-','nan','None','n/a']:return np.nan
 if s.endswith('%'):return float(s[:-1])/100
 for suffix,factor in [('T',1e6),('B',1e3),('M',1),('K',.001)]:
  if s.endswith(suffix):return float(s[:-1])*factor
 try:return float(s)
 except ValueError:return np.nan

def fields(ticker,page):
 out={}
 p=C/f'EDPRpool_{ticker}_{page}.json'
 if not p.exists():return out
 for x in json.loads(p.read_text()):
  t=pd.DataFrame(x['data'],columns=[str(c) for c in x['columns']]).fillna('')
  for _,r in t.iterrows():out[str(r.iloc[0])]={k:r[k] for k in t.columns[1:]}
 return out

def field(fields,label,column,default=np.nan):
 if label in fields and column in fields[label]:return number(fields[label][column])
 for k,v in fields.items():
  if k.startswith(label+' ') and column in v:return number(v[column])
 return default

def prepare():
 # MSCI World membership evidence for non-European candidates (URTH tracker proxy).
 world=pd.DataFrame()
 wurl='https://www.ishares.com/us/products/239696/ishares-msci-world-etf/latest-holdings.csv'
 wr=fetch.get(wurl)
 if wr.ok:
  lines=wr.text().splitlines()
  start=next((i for i,l in enumerate(lines) if l.startswith('Ticker,Name,')),None)
  if start is not None:
   world=pd.read_csv(io.StringIO('\n'.join(lines[start:])),on_bad_lines='skip').fillna('')
   world=world[world['Asset Class'].eq('Equity')]
 rows=[]
 for ticker,name,route,tier,reason in CANDIDATES:
  metas=[x for x in M if x['ticker']==ticker]
  if not metas or not any(x['status']==200 for x in metas):
   print('unavailable',ticker);continue
  f=fields(ticker,'financials_income-statement');b=fields(ticker,'financials_balance-sheet');cf=fields(ticker,'financials_cash-flow-statement');s=fields(ticker,'statistics')
  if not f:print('no financials',ticker);continue
  meta=next((x for x in metas if x['units']),None)
  unit=next((x for x in meta['units'] if x.startswith('Financials')),'Financials in millions EUR') if meta else 'Financials in millions EUR'
  fccy=unit.split()[-1];factor=1000 if 'billions' in unit else 1
  fy='FY 2025';prior='FY 2024'
  exchange=route.split('/')[1] if route.startswith('quote') else 'US'
  qccy=EXCH[exchange];country=CTRY[exchange]
  financial=lambda label,c=fy:field(f,label,c)*factor
  balance=lambda label,c=fy:field(b,label,c)*factor
  cashflow=lambda label,c=fy:field(cf,label,c)*factor
  mcap=field(s,'Market Cap','1');shares=field(s,'Shares Outstanding','1');beta=field(s,'Beta (5Y)','1')
  # Oct-30 close from history table
  price=np.nan;pricedate='unavailable'
  for x in json.loads((C/f'EDPRpool_{ticker}_history.json').read_text()):
   t=pd.DataFrame(x['data'],columns=x['columns'])
   if 'Date' in t.columns and 'Close' in t.columns:
    v=t[t.Date.astype(str).str.contains('Oct 30, 2026',regex=False)]
    if len(v):price=number(v.iloc[0]['Close']);pricedate='2026-10-30'
  price_raw=price
  if qccy=='GBP':price=comp.pence_to_pounds(price)
  implied=price*shares if np.isfinite(price*shares) else np.nan
  capchk=implied/mcap-1 if np.isfinite(implied) and mcap>0 else np.nan
  if not np.isfinite(mcap) and np.isfinite(implied):mcap=implied
  capeur=mcap/FX[qccy]
  member=U[(U.ticker.eq(ticker))|(U['name'].str.upper().str.contains(re.escape(name.upper().split(' ')[0]),regex=True,na=False))]
  ni=financial('Net Income to Common');ni=np.nan if not np.isfinite(ni) else ni
  if not np.isfinite(ni):ni=financial('Net Income')
  sales=financial('Revenue');ebit=financial('EBIT');ebitda=financial('EBITDA')
  if not np.isfinite(ebitda) and np.isfinite(ebit) and np.isfinite(cashflow('Depreciation & Amortization')):ebitda=ebit+cashflow('Depreciation & Amortization')
  eq=balance('Total Common Equity');eqp=balance('Total Common Equity',prior)
  roe=ni/((eq+eqp)/2) if np.isfinite(ni) and np.isfinite(eq+eqp) and (eq+eqp)>0 else np.nan
  div=abs(cashflow('Common Dividends Paid'));payout=div/ni if np.isfinite(ni) and ni>0 else np.nan
  growth=roe*(1-min(payout,1)) if np.isfinite(roe) and roe>0 and np.isfinite(payout) and payout>=0 else np.nan
  debt=balance('Total Debt');cash=balance('Cash & Equivalents');nci=balance('Minority Interest')
  assoc=balance('Long-Term Investments')
  capex=abs(cashflow('Capital Expenditures'));cfo=cashflow('Operating Cash Flow');assets=balance('Total Assets')
  market_fin=mcap*FX[fccy]/FX[qccy]
  ev=comp.comparable_ev(market_fin,debt,nci,cash,0) if np.isfinite(market_fin) and np.isfinite(debt) else np.nan
  period=f.get('Period Ending',{}).get(fy,'')
  row=dict(ticker=ticker,name=name,tier=tier,hypothesis=reason,europe=exchange not in ('US','asx','tsx'),country=country,quote_currency=qccy,report_currency=fccy,valuation_date='2026-10-30',price_date=pricedate,price=price,raw_price=price_raw,current_shares_m=shares,market_cap_quote_m=mcap,market_cap_eur_m=capeur,ln_mcap=np.log(capeur) if capeur>0 else np.nan,market_cap_check=capchk,financial_period_end=str(period),earnings_basis='FY2025',growth_basis='fundamental positive average-equity ROE times capped retention',ni=ni,sales=sales,EBIT=ebit,DA=financial('D&A For EBITDA') if np.isfinite(financial('D&A For EBITDA')) else cashflow('Depreciation & Amortization'),EBITDA=ebitda,equity=eq,equity_prior=eqp,assets=assets,debt=debt,cash=cash,NCI=nci,associates=assoc,EV_before_associates=ev,roe=roe,payout=payout,growth=growth,beta=beta,net_debt_ebitda=(debt-cash)/ebitda if np.isfinite(ebitda) and ebitda>0 else np.nan,ebitda_margin=ebitda/sales if np.isfinite(sales) and sales>0 else np.nan,capex=capex,capex_sales=capex/sales if np.isfinite(sales) and sales>0 else np.nan,cfo=cfo,net_margin=ni/sales if np.isfinite(ni) and np.isfinite(sales) and sales>0 else np.nan,tax_rate=financial('Income Tax Expense')/financial('Pretax Income') if np.isfinite(financial('Pretax Income')) and financial('Pretax Income')!=0 else np.nan,g_eps=field(s,'EPS Growth Forecast (3Y)','1'),g_rev=field(s,'Revenue Growth Forecast (3Y)','1'),membership='IEUR MSCI Europe IMI proxy Oct29; exact large/mid membership not asserted' if len(member) else ('URTH MSCI World proxy Oct29' if len(world) and ticker in set(world.Ticker) else 'unverified'),source_urls=' | '.join(x['url'] for x in metas if x['status']==200)+f' (accessed 2026-11-01)')
  for k,den in [('pe',ni),('pbv',eq),('ps',sales)]:row[k]=market_fin/den if np.isfinite(den) and den>0 else np.nan
  for k,den in [('ev_ebit',ebit),('ev_ebitda',ebitda),('ev_cf',cfo),('ev_assets',assets),('ev_sales',sales)]:row[k]=ev/den if np.isfinite(ev) and ev>0 and np.isfinite(den) and den>0 else np.nan
  row['peg']=row['pe']/(100*growth) if np.isfinite(growth) and growth>0 and np.isfinite(row['pe']) else np.nan
  row['relative_pe']=np.nan;row['tobins_q']=np.nan
  rows.append(row)
  pd.DataFrame([row]).to_csv(C/f'EDPRpool_{ticker}.csv',index=False)
  print(ticker,'capEUR',round(capeur) if np.isfinite(capeur) else None,'q',qccy,'r',fccy,'price',price,'chk',None if not np.isfinite(capchk) else round(capchk,4),'g',None if not np.isfinite(growth) else round(growth,4),'member',row['membership'][:20],flush=True)
 pd.DataFrame(rows).to_csv(P/'candidate_raw.csv',index=False)

if __name__=='__main__':prepare()
