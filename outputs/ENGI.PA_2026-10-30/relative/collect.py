"""Dated, robots-compliant minimal source extracts for ENGI.PA relative analysis.

Reuses the EDPRpool_*/ENELpool_* vendor extracts already cached for this valuation date
(shared market data rule); fetches only candidates missing from the cache."""
import json, re
from pathlib import Path
from valuation_agent.cachefetch import CachedFetcher, html_tables
from lxml import html

P=Path(__file__).resolve().parent
ROOT=P.parents[2]
C=ROOT/'cache/market/2026-10-30/candidates'
F=CachedFetcher(ROOT/'cache/web/2026-10-30', min_delay=1.1, user_agent='ValuationResearchAI/1.0 (educational research; respects robots.txt)')
ACCESS='2026-11-01'
# (ticker, name, route, tier, hypothesis, cache_prefix)
CANDIDATES=[
 ('ENGI','ENGIE','quote/epa/ENGI',0,'target','EDPRpool'),
 ('ENEL','Enel','quote/bit/ENEL',1,'integrated utility, generation+grids+retail; batch target','EDPRpool'),
 ('ELE','Endesa','quote/bme/ELE',1,'Spanish integrated utility (~70% Enel-owned; not a target subsidiary)','EDPRpool'),
 # Tier 1: integrated / regulated European utilities
 ('IBE','Iberdrola','quote/bme/IBE',1,'integrated utility, networks+renewables; batch target','EDPRpool'),
 ('EOAN','E.ON','quote/etr/EOAN',1,'German utility (networks/retail)','EDPRpool'),
 ('RWE','RWE','quote/etr/RWE',1,'German utility, generation+renewables','EDPRpool'),
 ('NTGY','Naturgy','quote/bme/NTGY',1,'Spanish gas/power utility','EDPRpool'),
 ('EDP','EDP','quote/eli/EDP',1,'Portuguese integrated utility','EDPRpool'),
 ('SSE','SSE','quote/lon/SSE',1,'UK utility, networks+renewables; batch target','EDPRpool'),
 ('CNA','Centrica','quote/lon/CNA',1,'UK energy retail/supply utility','EDPRpool'),
 ('A2A','A2A','quote/bit/A2A',1,'Italian multi-utility','EDPRpool'),
 ('VER','Verbund','quote/vie/VER',1,'Austrian hydro utility; batch target','EDPRpool'),
 ('FORTUM','Fortum','quote/hel/FORTUM',1,'Nordic utility, hydro/nuclear','EDPRpool'),
 ('NG','National Grid','quote/lon/NG',1,'UK/US transmission utility (developed market)','ENELpool'),
 ('CEZ','CEZ','quote/prg/CEZ',1,'Czech utility - EM listing check candidate','ENELpool'),
 # Tier 2: renewable IPPs, grid operators, generators (adjacent economics)
 ('ORSTED','Orsted','quote/cph/ORSTED',2,'offshore/onshore wind developer; batch target','EDPRpool'),
 ('EDPR','EDP Renovaveis','quote/eli/EDPR',2,'renewable developer-operator; batch target','EDPRpool'),
 ('ERG','ERG','quote/bit/ERG',2,'European wind/solar IPP','EDPRpool'),
 ('ANE','Acciona Energia','quote/bme/ANE',2,'renewable developer-operator','EDPRpool'),
 ('SLR','Solaria','quote/bme/SLR',2,'Spanish solar PV developer','EDPRpool'),
 ('GRE','Grenergy','quote/bme/GRE',2,'Spanish solar/storage developer','EDPRpool'),
 ('SCATC','Scatec','quote/osl/SCATC',2,'Norwegian renewables developer','EDPRpool'),
 ('DRX','Drax','quote/lon/DRX',2,'UK biomass/renewables generator','EDPRpool'),
 ('TRN','Terna','quote/bit/TRN',2,'Italian transmission grid operator','ENELpool'),
 ('REE','Redeia','quote/bme/RED',2,'Spanish transmission grid operator','ENELpool'),
 ('SRG','Snam','quote/bit/SRG',2,'Italian gas grid operator','ENELpool'),
 ('IG','Italgas','quote/bit/IG',2,'Italian gas distribution grid','ENELpool'),
 ('AY','Atlantica Sustainable','stocks/ay',2,'renewables IPP (World relaxation; US listing)','EDPRpool'),
 ('BEPC','Brookfield Renewable Corp','stocks/bepc',2,'global renewables IPP (World relaxation)','EDPRpool'),
 ('CWEN','Clearway Energy','stocks/cwen',2,'US renewables IPP (World relaxation)','EDPRpool'),
 ('ORA','Ormat Technologies','stocks/ora',2,'geothermal IPP (World relaxation)','EDPRpool'),
 ('BLX','Boralex','quote/tsx/BLX',2,'Canadian renewables IPP (World relaxation)','EDPRpool'),
 ('NPI','Northland Power','quote/tsx/NPI',2,'Canadian renewables (World relaxation)','EDPRpool'),
 ('INE','Innergex','quote/tsx/INE',2,'Canadian IPP (World relaxation)','EDPRpool'),
]

def collect():
 manifest=[]
 for ticker,name,route,tier,reason,prefix in CANDIDATES:
  keys=['financials_income-statement','financials_balance-sheet','financials_cash-flow-statement','statistics','history','profile']
  # reuse dated cache if all page extracts exist under the recorded prefix
  if all((C/f'{prefix}_{ticker}_{k}.json').exists() for k in keys):
   for page in keys:
    manifest.append(dict(ticker=ticker,name=name,route=route,tier=tier,reason=reason,url='https://stockanalysis.com/'+route,page=page,status=200,access_date=ACCESS,units=[],cache=f'reused {prefix} extract'))
   print(ticker,'reused');continue
  for page in ['financials/income-statement/','financials/balance-sheet/','financials/cash-flow-statement/','statistics/','history/','']:
   url='https://stockanalysis.com/'+route+'/'+page
   r=F.get(url)
   record=dict(ticker=ticker,name=name,route=route,tier=tier,reason=reason,url=url,page=page,status=r.status,access_date=ACCESS,cache='ENGIpool')
   if r.ok:
    key=(page.strip('/').replace('/','_') or 'profile')
    tables=[]
    for t in html_tables(r.text()):
     if getattr(t.columns,'nlevels',1)>1:t.columns=[str(x[0]) for x in t.columns]
     if page.startswith('financials'):
      t=t[[t.columns[0]]+[k for k in ['FY 2025','FY 2024'] if k in t.columns]]
     elif page=='history/':
      if 'Date' in t:t=t[t.Date.astype(str).str.contains('Oct 30, 2026')]
     tables.append(t.to_dict(orient='split'))
    (C/f'ENGIpool_{ticker}_{key}.json').write_text(json.dumps(tables,indent=2)+'\n')
    tree=html.fromstring(r.text());[x.drop_tree() for x in tree.xpath('//script|//style')]
    text=re.sub(r'\s+',' ',tree.text_content())
    record['units']=re.findall(r'Financials in (?:millions|billions) [A-Z]{3}|Currency in [A-Z]{3}',text)
    record['mcap']=re.findall(r'Market Cap.{0,12}',text)
   manifest.append(record)
   print(ticker,page,r.status)
 (P/'fetch_manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')

if __name__=='__main__':
 collect()
