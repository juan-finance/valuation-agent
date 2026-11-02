"""Dated extract manifest for VER.VI relative analysis.

Reuses the shared per-candidate dated extracts collected for the utilities runs
(`cache/market/2026-10-30/candidates/EDPRpool_<ticker>_<page>.json`, accessed
2026-11-01). Fetching is only attempted for a missing page; nothing is
re-collected (AGENTS.md efficiency rule). No market rebuild."""
import json, re
from pathlib import Path
from lxml import html
from valuation_agent.cachefetch import CachedFetcher, html_tables

P=Path(__file__).resolve().parent
ROOT=P.parents[2]
C=ROOT/'cache/market/2026-10-30/candidates'
F=CachedFetcher(ROOT/'cache/web/2026-10-30', min_delay=1.1, user_agent='ValuationResearchAI/1.0 (educational research; respects robots.txt)')
ACCESS='2026-11-02'
PAGES=['financials/income-statement/','financials/balance-sheet/','financials/cash-flow-statement/','statistics/','history/','']
CANDIDATES=[
 ('VER','Verbund','quote/vie/VER',0,'target'),
 # Tier 1: integrated / regulated European utilities
 ('ENEL','Enel','quote/bit/ENEL',1,'integrated utility; batch target'),
 ('IBE','Iberdrola','quote/bme/IBE',1,'integrated utility, networks+renewables; batch target'),
 ('EOAN','E.ON','quote/etr/EOAN',1,'German utility (networks/retail)'),
 ('ENGI','ENGIE','quote/epa/ENGI',1,'integrated utility, gas+renewables; batch target'),
 ('RWE','RWE','quote/etr/RWE',1,'German utility, generation+renewables'),
 ('NTGY','Naturgy','quote/bme/NTGY',1,'Spanish gas/power utility'),
 ('EDP','EDP','quote/eli/EDP',1,'Portuguese integrated utility'),
 ('SSE','SSE','quote/lon/SSE',1,'UK utility, networks+renewables; batch target'),
 ('CNA','Centrica','quote/lon/CNA',1,'UK energy retail/supply utility'),
 ('A2A','A2A','quote/bit/A2A',1,'Italian multi-utility with hydro'),
 ('FORTUM','Fortum','quote/hel/FORTUM',1,'Nordic utility, hydro/nuclear'),
 ('NG','National Grid','quote/lon/NG',1,'UK/US transmission utility (developed market)'),
 ('EVN','EVN','quote/vie/EVN',1,'Austrian multi-utility (power/gas/water); home-market comp'),
 ('CEZ','CEZ','quote/prg/CEZ',1,'Czech utility - EM listing check candidate'),
 # Tier 2: grid operators, renewable IPPs, generators (adjacent economics)
 ('ORSTED','Orsted','quote/cph/ORSTED',2,'offshore wind developer; batch target'),
 ('EDPR','EDP Renovaveis','quote/eli/EDPR',2,'renewable developer-operator; batch target; EDP subsidiary check'),
 ('ERG','ERG','quote/bit/ERG',2,'European wind/solar IPP'),
 ('ANE','Acciona Energia','quote/bme/ANE',2,'renewable developer-operator'),
 ('SLR','Solaria','quote/bme/SLR',2,'Spanish solar PV developer'),
 ('GRE','Grenergy','quote/bme/GRE',2,'Spanish solar/storage developer'),
 ('SCATC','Scatec','quote/osl/SCATC',2,'Norwegian renewables developer (hydro/wind/solar)'),
 ('DRX','Drax','quote/lon/DRX',2,'UK biomass/renewables generator'),
 ('TRN','Terna','quote/bit/TRN',2,'Italian transmission grid operator'),
 ('REE','Redeia','quote/bme/RED',2,'Spanish transmission grid operator'),
 ('SRG','Snam','quote/bit/SRG',2,'Italian gas grid operator'),
 ('IG','Italgas','quote/bit/IG',2,'Italian gas distribution grid'),
 ('AY','Atlantica Sustainable','stocks/ay',2,'renewables IPP (World relaxation; US listing)'),
 ('BEPC','Brookfield Renewable Corp','stocks/bepc',2,'global hydro/renewables IPP (World relaxation)'),
 ('CWEN','Clearway Energy','stocks/cwen',2,'US renewables IPP (World relaxation)'),
 ('ORA','Ormat Technologies','stocks/ora',2,'geothermal IPP (World relaxation)'),
 ('BLX','Boralex','quote/tsx/BLX',2,'Canadian wind/hydro IPP (World relaxation)'),
 ('NPI','Northland Power','quote/tsx/NPI',2,'Canadian renewables (World relaxation)'),
 ('INE','Innergex','quote/tsx/INE',2,'Canadian hydro IPP (World relaxation)'),
 # Tier 3: small developers and diversified infra (cap/size gates expected to bite)
 ('EKT','Energiekontor','quote/etr/EKT',3,'German wind/solar project developer-operator'),
 ('PNE3','PNE','quote/etr/PNE3',3,'German wind farm developer'),
 # hard-exclusion evidence rows
 ('ELE','Endesa','quote/bme/ELE',0,'SUBSIDIARY of ENEL (~70%) -> hard exclusion evidence row'),
]

def collect():
 old_manifest={x['ticker']:x for x in json.loads((ROOT/'outputs/ORSTED.CO_2026-10-30/relative/fetch_manifest.json').read_text()) if x.get('units')}
 manifest=[]
 for ticker,name,route,tier,reason in CANDIDATES:
  for page in PAGES:
   key=(page.strip('/').replace('/','_') or 'profile')
   cached=(C/f'EDPRpool_{ticker}_{key}.json').exists()
   url='https://stockanalysis.com/'+route+'/'+page
   record=dict(ticker=ticker,name=name,route=route,tier=tier,reason=reason,url=url,page=page,status=200 if cached else None,access_date='2026-11-01',cache='reused EDPRpool dated parsed extract' if cached else 'new extract')
   meta=old_manifest.get(ticker)
   if meta:
    record['units']=meta['units'];record['mcap']=meta.get('mcap',[])
   if not cached:
    r=F.get(url);record['status']=r.status;record['access_date']=ACCESS
    if r.ok:
     tables=[]
     for t in html_tables(r.text()):
      if getattr(t.columns,'nlevels',1)>1:t.columns=[str(x[0]) for x in t.columns]
      if page.startswith('financials'):t=t[[t.columns[0]]+[k for k in ['FY 2025','FY 2024'] if k in t.columns]]
      if page=='history/' and 'Date' in t:t=t[t.Date.astype(str).str.contains('Oct 30, 2026')]
      tables.append(t.to_dict(orient='split'))
     (C/f'EDPRpool_{ticker}_{key}.json').write_text(json.dumps(tables,indent=2)+'\n')
     tree=html.fromstring(r.text());[x.drop_tree() for x in tree.xpath('//script|//style')]
     text=re.sub(r'\s+',' ',tree.text_content())
     record['units']=re.findall(r'Financials in (?:millions|billions) [A-Z]{3}|Currency in [A-Z]{3}',text)
     record['mcap']=re.findall(r'Market Cap.{0,12}',text)
   manifest.append(record)
   print(ticker,page,record['status'],record['cache'])
 (P/'fetch_manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')

if __name__=='__main__':
 collect()
