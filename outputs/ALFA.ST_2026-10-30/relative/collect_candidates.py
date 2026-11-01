"""Uniform, robots-compliant AI research fetch; cache candidate facts, never a new universe."""
from pathlib import Path
import json
from valuation_agent.cachefetch import CachedFetcher,html_tables

ROOT=Path(__file__).resolve().parents[3]
P=Path(__file__).resolve().parent
C=ROOT/'cache/market/2026-10-30/candidates'
# Name, quote route, tier, source hypothesis (not a peer verdict).
CANDIDATES=[
 ('ALFA','Alfa Laval','sto/ALFA',1,'target'),
 ('G1A','GEA Group','etr/G1A',1,'process engineering/machinery for food & pharma; named ALFA competitor'),
 ('ATCO.A','Atlas Copco A','sto/ATCO.A',1,'compressors/vacuum machinery; sector_adjustments machinery seed'),
 ('EPI.A','Epiroc A','sto/EPI.A',1,'mining/infrastructure equipment machinery'),
 ('SAND','Sandvik','sto/SAND',1,'engineering/machinery (machining, mining equipment)'),
 ('WRT1V','Wartsila','hel/WRT1V',1,'marine/energy machinery; sector_adjustments machinery seed'),
 ('METSO','Metso','hel/METSO',1,'minerals processing machinery'),
 ('SUN','Sulzer','six/SUN',1,'fluid handling pumps/separation machinery'),
 ('ANDR','Andritz','vie/ANDR',1,'process machinery (pulp, separation)'),
 ('FLS','FLSmidth','cph/FLS',1,'cement/minerals process machinery'),
 ('KSB','KSB','etr/KSB',1,'pumps/valves fluid handling machinery'),
 ('BCHN','Burckhardt Compression','six/BCHN',1,'compression machinery'),
 ('WEIR','Weir Group','lon/WEIR',1,'mining/minerals machinery'),
 ('ROR','Rotork','lon/ROR',1,'flow-control actuators machinery'),
 ('IMI','IMI','lon/IMI',1,'precision fluid/motion engineering'),
 ('SPX','Spirax Group','lon/SPX',1,'steam/thermal machinery'),
 ('SMIN','Smiths Group','lon/SMIN',2,'diversified industrial engineering'),
 ('SKF.B','SKF B','sto/SKF.B',2,'bearings/rotating machinery components'),
 ('IP','Interpump','bit/IP',2,'hydraulic/water-jetting machinery'),
 ('BUCN','Bucher Industries','six/BUCN',2,'specialized machinery'),
 ('KRN','Krones','etr/KRN',2,'packaging/process machinery'),
 ('INDT','Indutrade','sto/INDT',2,'industrial components/flow technology'),
 ('ABBN','ABB','six/ABBN',2,'electrification/automation industrial group'),
 ('RAA','Rational','etr/RAA',2,'food-preparation machinery; niche'),
 ('KGX','KION','etr/KGX',3,'industrial trucks/supply chain; tier3 fallback only'),
 ('HLMA','Halma','lon/HLMA',3,'safety/environment technology group; tier3 fallback only'),
 ('XYL','Xylem','stocks/XYL',1,'US water technology/pumps; World relaxation only'),
 ('IR','Ingersoll Rand','stocks/IR',1,'US compressors/fluid machinery; World relaxation only'),
 ('DOV','Dover','stocks/DOV',2,'US diversified industrial machinery; World relaxation only'),
 ('IEX','IDEX','stocks/IEX',1,'US fluidics/precision machinery; World relaxation only'),
]
fetch=CachedFetcher(str(ROOT/'cache/web/2026-10-30'),max_workers=3,min_delay=1.1,user_agent='ValuationResearchAI/1.0 (educational research; respects robots.txt)')
manifest=[]
for ticker,name,route,tier,hypothesis in CANDIDATES:
 base='https://stockanalysis.com/'+(route.lower() if route.startswith('stocks/') else 'quote/'+route)+'/'
 for page in ['statistics/','financials/','financials/balance-sheet/','financials/cash-flow-statement/','']:
  u=base+page;r=fetch.get(u);key=page.strip('/').replace('/','_') or 'profile'
  record=dict(ticker=ticker,name=name,tier=tier,hypothesis=hypothesis,url=u,status=r.status,page=key)
  if r.ok:
   ts=html_tables(r.text())
   for i,t in enumerate(ts):t.to_csv(C/f'{ticker}_{key}_{i}.csv',index=False)
   # Keep short source metadata/descriptions, not a republication of page content.
   import re
   from lxml import html
   tree=html.fromstring(r.text())
   metas=tree.xpath('//meta[@name="description"]/@content')
   record['description']=metas[0] if metas else ''
   record['page_title']=' '.join(tree.xpath('//title/text()'))
   record['headings']=tree.xpath('//h1/text()')
   if key=='profile':
    body=tree.text_content()
    for pattern in [r'Oct(?:ober)?\s+30,?\s+2026',r'(?i)Financials in [A-Za-z ]+',r'(?i)Currency in [A-Z]{3}']:
     record.setdefault('date_currency_matches',[]).extend(re.findall(pattern,body)[:3])
   record['tables']=len(ts)
  manifest.append(record)
 (P/'candidate_fetch_manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
 print(ticker,[(x['page'],x['status'],x.get('tables',0)) for x in manifest if x['ticker']==ticker],flush=True)
print('done',len(manifest))
