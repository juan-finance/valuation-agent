"""Manifest for SSE.L pool; every extract reused from the dated EDPR/ENEL cache (shared market data rule)."""
import json
from pathlib import Path

P=Path(__file__).resolve().parent
ROOT=P.parents[2]
C=ROOT/'cache/market/2026-10-30/candidates'
ACCESS='2026-11-02'
# (ticker, name, route, tier, hypothesis, cache_prefix)
CANDIDATES=[
 ('SSE','SSE','quote/lon/SSE',0,'target','EDPRpool'),
 # Tier 1: integrated / regulated European utilities
 ('IBE','Iberdrola','quote/bme/IBE',1,'integrated utility, networks/renewables/retail; batch target','EDPRpool'),
 ('ENEL','Enel','quote/bit/ENEL',1,'integrated utility, generation+networks+retail; batch target','EDPRpool'),
 ('EOAN','E.ON','quote/etr/EOAN',1,'German utility (networks/retail)','EDPRpool'),
 ('ENGI','ENGIE','quote/epa/ENGI',1,'integrated utility, gas+renewables; batch target','EDPRpool'),
 ('RWE','RWE','quote/etr/RWE',1,'German utility, generation+renewables','EDPRpool'),
 ('NTGY','Naturgy','quote/bme/NTGY',1,'Spanish gas/power utility','EDPRpool'),
 ('EDP','EDP','quote/eli/EDP',1,'Portuguese integrated utility','EDPRpool'),
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
 # hard-exclusion evidence row
 ('ELE','Endesa','quote/bme/ELE',0,'SUBSIDIARY of ENEL (~70% owned by candidate) -> hard exclusion evidence row','EDPRpool'),
]
UNITS={
 'EDPR':'Financials in millions EUR','ORSTED':'Financials in millions DKK','ANE':'Financials in millions EUR',
 'ERG':'Financials in millions EUR','SLR':'Financials in millions EUR','GRE':'Financials in millions EUR',
 'SCATC':'Financials in millions NOK','AY':'Financials in millions USD','BEPC':'Financials in millions USD',
 'CWEN':'Financials in millions USD','ORA':'Financials in millions USD','BLX':'Financials in millions CAD',
 'NPI':'Financials in millions CAD','INE':'Financials in millions CAD','IBE':'Financials in millions EUR',
 'ENEL':'Financials in millions EUR','SSE':'Financials in millions GBP','ENGI':'Financials in millions EUR',
 'VER':'Financials in millions EUR','RWE':'Financials in millions EUR','FORTUM':'Financials in millions EUR',
 'DRX':'Financials in millions GBP','EOAN':'Financials in millions EUR','ELE':'Financials in millions EUR',
 'NTGY':'Financials in millions EUR','CNA':'Financials in millions GBP','A2A':'Financials in millions EUR',
 'EDP':'Financials in millions EUR','IG':'Financials in millions EUR','NG':'Financials in millions GBP',
 'REE':'Financials in millions EUR','SRG':'Financials in millions EUR','TRN':'Financials in millions EUR'}
KEYS=['financials_income-statement','financials_balance-sheet','financials_cash-flow-statement','statistics','history','profile']

def collect():
 manifest=[]
 for ticker,name,route,tier,reason,prefix in CANDIDATES:
  ok=all((C/f'{prefix}_{ticker}_{k}.json').exists() for k in KEYS)
  for page in KEYS:
   manifest.append(dict(ticker=ticker,name=name,route=route,tier=tier,reason=reason,
    url='https://stockanalysis.com/'+route+'/',page=page,status=200 if ok else 404,
    access_date=ACCESS,units=[UNITS[ticker]] if ticker in UNITS and ok else [],cache=f'reused {prefix} extract'))
  print(ticker,'reused' if ok else 'MISSING')
 (P/'fetch_manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')

if __name__=='__main__':
 collect()
