"""Uniform, robots-compliant AI research fetch; cache candidate facts, never a new universe."""
from pathlib import Path
import json
from valuation_agent.cachefetch import CachedFetcher,html_tables

ROOT=Path(__file__).resolve().parents[3]
P=Path(__file__).resolve().parent
C=ROOT/'cache/market/2026-10-30/candidates'
# Name, quote route, tier, source hypothesis (not a peer verdict).
CANDIDATES=[
 ('MT.AS','ArcelorMittal','ams/MT',1,'target'),
 ('VOE','voestalpine','vie/VOE',1,'integrated/specialty steel'),
 ('SSAB.A','SSAB','sto/SSAB.A',1,'steel plate and special steels; SSAB annual report peer list'),
 ('OUT1V','Outokumpu','hel/OUT1V',1,'stainless integrated steel'),
 ('SZG','Salzgitter','etr/SZG',1,'integrated steel'),
 ('ALLEI','Alleima','sto/ALLEI',1,'specialty stainless steel'),
 ('BEKB','Bekaert','ebr/BEKB',2,'steel wire downstream; cyclical processing'),
 ('NHY','Norsk Hydro','osl/NHY',2,'aluminium integrated capital-intensive metals'),
 ('NDA','Aurubis','etr/NDA',2,'copper smelting and recycling; processing spread'),
 ('RIO','Rio Tinto','lon/RIO',2,'iron ore and other mining; vertically adjacent'),
 ('ANTO','Antofagasta','lon/ANTO',2,'capital-intensive copper mining; cyclical margins'),
 ('BOL','Boliden','sto/BOL',2,'base metal mining and smelting'),
 ('TKA','thyssenkrupp','etr/TKA',1,'steel plus diversified industrials; review spinoff'),
 ('APAM','Aperam','ams/APAM',1,'stainless; review acquisition'),
 ('ACX','Acerinox','bme/ACX',1,'stainless; review Haynes acquisition'),
 ('GRNG','Granges','sto/GRNG',2,'aluminium rolled products'),
 ('YAR','Yara','osl/YAR',3,'cyclical capital-intensive fertilizers; tier3 fallback only'),
 ('BAS','BASF','etr/BAS',3,'capital-intensive chemicals; tier3 fallback only'),
 ('HEI','Heidelberg Materials','etr/HEI',3,'cyclical construction materials; tier3 fallback only'),
 ('GLEN','Glencore','lon/GLEN',2,'commodity production; review coal acquisition and trading mix'),
 ('AAL','Anglo American','lon/AAL',2,'mining; review platinum spinoff'),
 ('NK','Imerys','epa/NK',2,'industrial mineral extraction/processing'),
 ('BZU','Buzzi','bit/BZU',3,'cyclical cement; tier3 fallback only'),
 ('ERA','Eramet','epa/ERA',2,'mining and ferroalloys; review events/size'),
 ('SDF','K+S','etr/SDF',2,'potash/salt mining; weaker commodity adjacency'),
 ('NUE','Nucor','stocks/NUE',1,'US electric arc steel; World relaxation only'),
 ('STLD','Steel Dynamics','stocks/STLD',1,'US electric arc steel; World relaxation only'),
 ('CMC','Commercial Metals','stocks/CMC',1,'US steel/recycling; World relaxation only'),
 ('5411','JFE Holdings','tyo/5411',1,'Japanese integrated steel; World relaxation only'),
 ('BSL','BlueScope Steel','asx/BSL',1,'Australian flat steel; World relaxation only'),
 ('BHP','BHP','asx/BHP',2,'iron ore/copper mining; additional developed World relaxation'),
 ('FMG','Fortescue','asx/FMG',2,'iron ore upstream of steel; additional developed World relaxation'),
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
