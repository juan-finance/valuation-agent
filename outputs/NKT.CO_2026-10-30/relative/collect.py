"""Small dated extracts, reusing shared candidate tables; no market rebuild."""
import json,re
from pathlib import Path
from lxml import html
from valuation_agent.cachefetch import CachedFetcher,html_tables
P=Path(__file__).resolve().parent; ROOT=P.parents[2]; C=ROOT/'cache/market/2026-10-30/candidates'
CANDIDATES=[
('NKT','NKT','cph/NKT',0,'target'),
('NEX','Nexans','epa/NEX',1,'power grid cables; same main business'),
('PRY','Prysmian','bit/PRY',1,'power grid cables; same main business; universe target'),
('5802','Sumitomo Electric','tyo/5802',1,'power cables; World expansion only'),
('5801','Furukawa Electric','tyo/5801',1,'power cables; World expansion only'),
('ELHA','ElvalHalcor','ath/ELHA',1,'copper/aluminium and Hellenic Cables; Greece market classification screen'),
('ABBN','ABB','swx/ABBN',2,'electrification, drives and industrial automation'),
('SU','Schneider Electric','epa/SU',2,'electrical power management and grid equipment; universe target'),
('LR','Legrand','epa/LR',2,'electrical infrastructure equipment'),
('SIE','Siemens','etr/SIE',2,'industrial electrification and automation'),
('ENR','Siemens Energy','etr/ENR',2,'grid technology and power equipment; universe target'),
('VWS','Vestas','cph/VWS',2,'wind turbines and recurring services; universe target'),
('NDX1','Nordex','etr/NDX1',2,'wind turbines'),
('ETN','Eaton','stocks/etn',2,'power management; World expansion only'),
('GEV','GE Vernova','stocks/gev',2,'power generation, wind and grids; World expansion only; spin-off screen'),
('WRT1V','Wartsila','hel/WRT1V',2,'power generation and marine engines/services'),
('ANDR','Andritz','vie/ANDR',2,'hydropower and industrial process equipment'),
('IMI','IMI','lon/IMI',2,'industrial and power flow control'),
('ROR','Rotork','lon/ROR',2,'energy flow-control actuators'),
('SPX','Spirax','lon/SPX',2,'industrial thermal energy management'),
('SKF.B','SKF','sto/SKF.B',2,'bearings for wind and rotating industrial machinery'),
('SUN','Sulzer','swx/SUN',2,'energy pumps and industrial flow equipment'),
('ALFA','Alfa Laval','sto/ALFA',3,'heat transfer equipment; universe target'),
('ATCO.A','Atlas Copco','sto/ATCO.A',3,'compressors and industrial energy equipment'),
('SAND','Sandvik','sto/SAND',3,'mining and metal cutting equipment; different demand drivers'),
('METSO','Metso','hel/METSO',3,'minerals processing; different end market'),
('WEIR','Weir','lon/WEIR',3,'mining pumps; different end market'),
('G1A','GEA','etr/G1A',3,'food processing equipment; different end market'),
('EPI.A','Epiroc','sto/EPI.A',3,'mining equipment; different end market'),
('SMIN','Smiths','lon/SMIN',3,'diversified technology; portfolio-change screen'),
('TKA','thyssenkrupp','etr/TKA',3,'diversified industrials; restructuring screen'),
]
F=CachedFetcher(ROOT/'cache/web/2026-10-30',min_delay=1.1,user_agent='ValuationResearchAI/1.0 (educational AI research; robots compliant)')
def collect():
 m=[]
 for ticker,name,route,tier,hypothesis in CANDIDATES:
  base='https://stockanalysis.com/'+(route if route.startswith('stocks/') else 'quote/'+route)+'/'
  for page in ['statistics/','financials/','financials/balance-sheet/','financials/cash-flow-statement/','history/','']:
   key=page.strip('/').replace('/','_') or 'profile';u=base+page
   old=list(C.glob(f'{ticker}_{key}_[0-9]*.csv'))
   rec=dict(ticker=ticker,name=name,tier=tier,hypothesis=hypothesis,url=u,page=key,status=200,cache='reused dated parsed extract' if old else 'new extract')
   if not old:
    r=F.get(u);rec['status']=r.status
    if r.ok:
     for i,t in enumerate(html_tables(r.text())):
      if getattr(t.columns,'nlevels',1)>1:t.columns=[str(x[0]) for x in t.columns]
      if page.startswith('financials'):t=t[[t.columns[0]]+[k for k in ['FY 2025','FY 2024'] if k in t.columns]]
      if page=='history/' and 'Date' in t:t=t[t.Date.astype(str).str.contains('Oct 30, 2026')]
      t.to_csv(C/f'{ticker}_{key}_{i}.csv',index=False)
     tree=html.fromstring(r.text());rec['description']=tree.xpath('//meta[@name="description"]/@content');rec['units']=re.findall(r'Financials in (?:millions|billions) [A-Z]{3}',tree.text_content())
  m.append(rec)
 (P/'candidate_fetch_manifest.json').write_text(json.dumps(m,indent=2)+'\n');print(ticker,'done',flush=True)
if __name__=='__main__':collect()
