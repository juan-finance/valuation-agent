"""Dated extract manifest for ORSTED.CO relative analysis.

Reuses the shared per-candidate dated extracts collected for the EDPR.LS run
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
 ('ORSTED','Orsted','quote/cph/ORSTED',0,'target'),
 # Tier 1: listed renewable developers / independent power producers
 ('EDPR','EDP Renovaveis','quote/eli/EDPR',1,'renewable developer-operator; also batch target'),
 ('ANE','Acciona Energia','quote/bme/ANE',1,'renewable developer-operator (wind/solar)'),
 ('ERG','ERG','quote/bit/ERG',1,'European wind/solar IPP'),
 ('SLR','Solaria','quote/bme/SLR',1,'Spanish solar PV developer-operator'),
 ('NEOEN','Neoen','quote/epa/NEOEN',1,'French renewables IPP (solar/wind/storage)'),
 ('GRE','Grenergy','quote/bme/GRE',1,'Spanish solar/storage developer'),
 ('SCATC','Scatec','quote/osl/SCATC',1,'Norwegian renewables developer (solar/hydro/wind)'),
 ('EKT','Energiekontor','quote/etr/EKT',1,'German wind/solar project developer-operator'),
 ('PNE3','PNE','quote/etr/PNE3',1,'German wind farm developer'),
 ('OX2','OX2','quote/sto/OX2',1,'Swedish wind/solar developer'),
 ('AY','Atlantica Sustainable','stocks/ay',1,'renewables IPP (World relaxation candidate; US listing)'),
 ('BEPC','Brookfield Renewable Corp','stocks/bepc',1,'global renewables IPP (World relaxation; dedup vs BEP)'),
 ('CWEN','Clearway Energy','stocks/cwen',1,'US renewables IPP (World relaxation)'),
 ('ORA','Ormat Technologies','stocks/ora',1,'geothermal IPP (World relaxation)'),
 ('BLX','Boralex','quote/tsx/BLX',1,'Canadian wind/solar IPP (World relaxation)'),
 ('NPI','Northland Power','quote/tsx/NPI',1,'Canadian offshore/onshore renewables (World relaxation)'),
 ('INE','Innergex','quote/tsx/INE',1,'Canadian hydro/wind/solar IPP (World relaxation)'),
 # Tier 2: integrated European utilities with material renewable fleets
 ('IBE','Iberdrola','quote/bme/IBE',2,'integrated utility, large renewables; batch target'),
 ('ENEL','Enel','quote/bit/ENEL',2,'integrated utility, large renewables; batch target'),
 ('SSE','SSE','quote/lon/SSE',2,'UK utility, wind-heavy; batch target'),
 ('ENGI','ENGIE','quote/epa/ENGI',2,'integrated utility, renewables fleet; batch target'),
 ('VER','Verbund','quote/vie/VER',2,'Austrian hydro/wind utility; batch target'),
 ('RWE','RWE','quote/etr/RWE',2,'German utility, large renewables build-out'),
 ('FORTUM','Fortum','quote/hel/FORTUM',2,'Nordic utility, hydro/nuclear/renewables'),
 ('DRX','Drax','quote/lon/DRX',2,'UK biomass/renewables generator'),
 ('EOAN','E.ON','quote/etr/EOAN',2,'German utility (networks/retail; renewables legacy)'),
 ('ELE','Endesa','quote/bme/ELE',2,'Spanish utility (Enel subsidiary; renewables fleet)'),
 ('NTGY','Naturgy','quote/bme/NTGY',2,'Spanish gas/power utility with renewables'),
 ('CNA','Centrica','quote/lon/CNA',2,'UK utility, generation stake'),
 ('A2A','A2A','quote/bit/A2A',2,'Italian multi-utility with hydro/renewables'),
 ('IREN','Iren','quote/bit/IREN',2,'Italian multi-utility with hydro'),
 ('HERA','Hera','quote/bit/HERA',2,'Italian multi-utility'),
 ('EDP','EDP','quote/eli/EDP',2,'Portuguese integrated utility; EDPR parent (eligible for ORSTED)'),
]

def collect():
 old_manifest={x['ticker']:x for x in json.loads((ROOT/'outputs/EDPR.LS_2026-10-30/relative/fetch_manifest.json').read_text()) if x.get('units')}
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
