"""Normalize the single-source candidate extract, retaining unavailable fields."""
from pathlib import Path
import json,re,io
import numpy as np
import pandas as pd
from lxml import html
from valuation_agent.cachefetch import CachedFetcher,html_tables
from valuation_agent import comparables as comp

P=Path(__file__).resolve().parent;ROOT=P.parents[2];C=ROOT/'cache/market/2026-10-30/candidates'
FX=json.loads((ROOT/'cache/macro/2026-10-30.json').read_text())['fx_ecb_reference']['rates'];FX['EUR']=1
U=pd.read_csv(ROOT/'cache/market/2026-10-30/universe.csv').fillna('')
M=json.loads((P/'candidate_fetch_manifest.json').read_text())
fetch=CachedFetcher(str(ROOT/'cache/web/2026-10-30'),min_delay=1.1,user_agent='ValuationResearchAI/1.0 (educational research; respects robots.txt)')

def number(s):
 s=str(s).replace(',','').replace('−','-').strip()
 if s in ['','-','nan','None','n/a']:return np.nan
 if s.endswith('%'):return float(s[:-1])/100
 for suffix,factor in [('T',1e6),('B',1e3),('M',1),('K',.001)]:
  if s.endswith(suffix):return float(s[:-1])*factor
 try:return float(s)
 except ValueError:return np.nan

def table_fields(ticker,page):
 out={};headers=[]
 for file in sorted(C.glob(f'{ticker}_{page}_[0-9]*.csv')):
  t=pd.read_csv(file).fillna('');headers+=t.columns.tolist()
  for _,r in t.iterrows():out[str(r.iloc[0])]={k:r[k] for k in t.columns[1:]}
 return out,headers

def field(fields,label,column,default=np.nan):
 if label in fields and column in fields[label]:return number(fields[label][column])
 for k,v in fields.items():
  if k.startswith(label+' ') and column in v:return number(v[column])
 return default

UNIVERSE_NAME={'ALFA':'ALFA LAVAL','ATCO.A':'ATLAS COPCO CLASS A','EPI.A':'EPIROC CLASS A','SKF.B':'^SKF B$','WRT1V':'WARTSILA','METSO':'METSO','SUN':'SULZER','ANDR':'ANDRITZ','FLS':'FLSMIDTH','KSB':'KSB','BCHN':'BURCKHARDT','WEIR':'WEIR GROUP','ROR':'ROTORK','IMI':'IMI','SPX':'SPIRAX','SMIN':'SMITHS','IP':'INTERPUMP','BUCN':'BUCHER','KRN':'KRONES','INDT':'INDUTRADE','ABBN':'ABB','RAA':'RATIONAL','KGX':'KION','HLMA':'HALMA','SAND':'SANDVIK','G1A':'GEA'}
US_TICKERS=['XYL','IR','DOV','IEX']

def prepare():
 world_url='https://www.ishares.com/us/products/239696/ishares-msci-world-etf/latest-holdings.csv'
 body=fetch.get(world_url).text();lines=body.splitlines();start=next(i for i,l in enumerate(lines) if l.startswith('Ticker,Name,'));world=pd.read_csv(io.StringIO('\n'.join(lines[start:])),on_bad_lines='skip').fillna('')
 world=world[world['Asset Class'].eq('Equity')]
 world[world.Ticker.isin(US_TICKERS)].to_csv(P/'world_candidate_membership.csv',index=False)
 rows=[]
 for ticker in dict.fromkeys(x['ticker'] for x in M):
  meta=next(x for x in M if x['ticker']==ticker);route=next(x['url'] for x in reversed(M) if x['ticker']==ticker and x['page']=='financials' and x['status']==200)
  r=fetch.get(route);txt=html.fromstring(r.text()).text_content() if r.ok else ''
  unit=re.search(r'Financials in (millions|billions) ([A-Z]{3})',txt)
  if not unit:print('no financial units',ticker);continue
  fccy=unit[2];factor=1000 if unit[1]=='billions' else 1
  fields,cols=table_fields(ticker,'financials');bs,bcols=table_fields(ticker,'financials_balance-sheet');cf,_=table_fields(ticker,'financials_cash-flow-statement');stats,_=table_fields(ticker,'statistics')
  fy='FY 2025';prior='FY 2024'
  # bcols repeats per table; first data column is latest interim/current.
  current=bcols[1]
  member=U[U['name'].str.contains(UNIVERSE_NAME.get(ticker,'^'+re.escape(meta['name'])+'$'),case=False,regex=True)]
  if member.empty:member=U[U.ticker.eq(ticker)]
  europe=ticker not in US_TICKERS
  wm=world[world.Ticker.eq(ticker) & world.Location.eq('United States')]
  qccy=str(member.iloc[0].currency) if len(member) else str(wm.iloc[0]['Market Currency']) if len(wm) else 'USD'
  country=str(member.iloc[0].country_listing) if len(member) else str(wm.iloc[0].Location) if len(wm) else 'unverified'
  financial=lambda label,c=fy:field(fields,label,c)*factor
  balance=lambda label,c=current:field(bs,label,c)*factor
  cashflow=lambda label,c=fy:field(cf,label,c)*factor
  mcap=field(stats,'Market Cap','1');shares=field(stats,'Shares Outstanding','1');beta=field(stats,'Beta (5Y)','1')
  capeur=mcap/FX[qccy];ni=financial('Net Income');sales=financial('Revenue');ebit=financial('Operating Income');da=cashflow('Depreciation & Amortization');ebitda=ebit+da
  eq=balance('Total Common Equity',fy);eqprev=balance('Total Common Equity',prior);roe=ni/((eq+eqprev)/2) if (eq+eqprev)>0 else np.nan
  div=abs(cashflow('Common Dividends Paid'));payout=div/ni if ni>0 else np.nan
  growth=roe*(1-min(payout,1)) if roe>0 and payout>=0 else np.nan
  debt=balance('Total Debt');cash=balance('Cash & Equivalents');nci=balance('Minority Interest')
  capex=abs(cashflow('Capital Expenditures'));cfo=cashflow('Operating Cash Flow');assets=balance('Total Assets',fy)
  base=route.removesuffix('financials/');hu=base+'history/';hr=fetch.get(hu);price=np.nan;pricedate='unavailable'
  if hr.ok:
   for t in html_tables(hr.text()):
    if 'Date' in t.columns and 'Close' in t.columns:
     t=t.astype(str);valid=t[t.Date.str.contains('Oct 30, 2026',regex=False)]
     if len(valid):price=number(valid.iloc[0]['Close']);pricedate='2026-10-30';break
  price_raw=price
  if qccy=='GBP':price=comp.pence_to_pounds(price)
  impliedcap=price*shares;cap_error=impliedcap/mcap-1 if mcap>0 else np.nan
  # EV without associates is a visibly qualified cross-check, not primary valuation.
  market_fin= mcap*FX[fccy]/FX[qccy]
  ev_no_associates=comp.comparable_ev(market_fin,debt,nci,cash,0) if np.isfinite(nci) else np.nan
  row=dict(ticker=ticker,name=meta['name'],tier=meta['tier'],hypothesis=meta['hypothesis'],europe=europe,country=country,quote_currency=qccy,report_currency=fccy,financial_scale_to_millions=factor,valuation_date='2026-10-30',price_date=pricedate,price=price,current_shares_m=shares,market_cap_quote_m=mcap,market_cap_eur_m=capeur,ln_mcap=np.log(capeur),market_cap_check=cap_error,financial_period_end=fields.get('Period Ending',{}).get(fy,''),earnings_basis='FY2025',growth_basis='fundamental positive average-equity ROE times capped retention',ni=ni,sales=sales,EBIT=ebit,DA=da,EBITDA=ebitda,equity=eq,equity_prior=eqprev,assets=assets,debt=debt,cash=cash,NCI=nci,associates=np.nan,EV_before_associates=ev_no_associates,roe=roe,payout=payout,growth=growth,beta=beta,net_debt_ebitda=(debt-cash)/ebitda if ebitda>0 else np.nan,ebitda_margin=ebitda/sales,capex=capex,capex_sales=capex/sales,cfo=cfo,net_margin=ni/sales,pe=market_fin/ni if ni>0 else np.nan,pbv=market_fin/eq if eq>0 else np.nan,ps=market_fin/sales,ev_ebit=ev_no_associates/ebit if ebit>0 else np.nan,ev_ebitda=ev_no_associates/ebitda if ebitda>0 else np.nan,ev_cf=ev_no_associates/cfo if cfo>0 else np.nan,ev_assets=ev_no_associates/assets,ev_sales=ev_no_associates/sales,relative_pe=np.nan,tobins_q=np.nan,membership='IEUR MSCI Europe IMI proxy Oct29; exact large/mid membership not asserted' if len(member) else 'URTH MSCI World proxy Oct29' if ticker in world.Ticker.values else 'unverified',source_urls=f'financials: {route} | balance_sheet: {base}financials/balance-sheet/ | cashflows: {base}financials/cash-flow-statement/ | stats: {base}statistics/ | price: {hu} (accessed 2026-11-01)')
  row['peg']=row['pe']/(100*growth) if growth>0 else np.nan
  row['raw_price']=price_raw
  row['price_unit_conversion']='GBX divided100 to GBP' if qccy=='GBP' else 'none'
  rows.append(row)
  pd.DataFrame([row]).to_csv(C/f'{ticker}.csv',index=False)
  print(ticker,'capEUR',round(capeur),'quote',qccy,'report',fccy,'price',price,'check',round(cap_error,4) if np.isfinite(cap_error) else cap_error,'g',round(growth,4) if np.isfinite(growth) else growth,flush=True)
 raw=pd.DataFrame(rows);raw.to_csv(P/'candidate_raw.csv',index=False)
 return raw

if __name__=='__main__':prepare()
