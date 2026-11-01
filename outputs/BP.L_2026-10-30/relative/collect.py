"""Dated, robots-compliant minimal source extracts for BP relative analysis."""
import json
from pathlib import Path
from valuation_agent.cachefetch import CachedFetcher, html_tables
from lxml import html

P=Path(__file__).resolve().parent
ROOT=P.parents[2]
C=ROOT/'cache/market/2026-10-30/candidates'
F=CachedFetcher(ROOT/'cache/web/2026-10-30', min_delay=1.1, user_agent='ValuationResearchAI/1.0 (educational research; respects robots.txt)')
CANDIDATES=[
 ('BP','BP','quote/lon/BP',1,'target'),
 ('SHEL','Shell','quote/lon/SHEL',1,'integrated oil/gas and LNG'),
 ('TTE','TotalEnergies','quote/epa/TTE',1,'integrated oil/gas and LNG'),
 ('EQNR','Equinor','quote/osl/EQNR',1,'integrated upstream and European gas'),
 ('ENI','Eni','quote/bit/ENI',1,'integrated upstream refining and gas'),
 ('REP','Repsol','quote/bme/REP',1,'integrated oil refining and upstream'),
 ('OMV','OMV','quote/vie/OMV',1,'integrated gas refining chemicals'),
 ('GALP','Galp','quote/eli/GALP',1,'integrated upstream and refining'),
 ('NESTE','Neste','quote/hel/NESTE',2,'renewable/conventional refining'),
 ('ORLEN','Orlen','quote/wse/PKN',2,'integrated European refining and gas; Poland not developed market'),
 ('VARE','Var Energi','quote/osl/VAR',2,'Norwegian upstream'),
 ('AKRBP','Aker BP','quote/osl/AKRBP',2,'Norwegian upstream'),
 ('HBR','Harbour Energy','quote/lon/HBR',2,'upstream oil/gas'),
 ('XOM','Exxon Mobil','stocks/xom',1,'global integrated upstream/refining'),
 ('CVX','Chevron','stocks/cvx',1,'global integrated upstream/refining'),
 ('COP','ConocoPhillips','stocks/cop',2,'large developed-market E&P'),
 ('EOG','EOG Resources','stocks/eog',2,'large developed-market E&P'),
 ('OXY','Occidental','stocks/oxy',2,'large developed-market E&P chemicals'),
 ('SU','Suncor','stocks/su',1,'Canadian integrated oil refining'),
 ('CNQ','Canadian Natural','stocks/cnq',2,'Canadian oil sands and upstream'),
 ('VLO','Valero','stocks/vlo',2,'US refining'),
 ('MPC','Marathon Petroleum','stocks/mpc',2,'US refining'),
 ('PSX','Phillips 66','stocks/psx',2,'US refining and midstream'),
 ('WDS','Woodside Energy','quote/asx/WDS',2,'Australian LNG/upstream'),
 ('STO','Santos','quote/asx/STO',2,'Australian LNG/upstream'),
]

def collect(target_only=False):
 manifest=json.loads((P/'fetch_manifest.json').read_text()) if (P/'fetch_manifest.json').exists() else []
 for ticker,name,route,tier,reason in CANDIDATES[:1] if target_only else CANDIDATES:
  for page in ['financials/income-statement/','financials/balance-sheet/','financials/cash-flow-statement/','statistics/','history/']:
   url='https://stockanalysis.com/'+route+'/'+page
   r=F.get(url)
   record=dict(ticker=ticker,name=name,route=route,tier=tier,reason=reason,url=url,page=page,status=r.status,access_date='2026-11-01')
   if r.ok:
    key=page.strip('/').replace('/','_')
    tables=[]
    for t in html_tables(r.text()):
     if getattr(t.columns,'nlevels',1)>1:t.columns=[str(x[0]) for x in t.columns]
     if page.startswith('financials'):
      t=t[[t.columns[0]]+[k for k in ['FY 2025','FY 2024'] if k in t.columns]]
     elif page=='history/':
      if 'Date' in t:t=t[t.Date.eq('Oct 30, 2026')]
     tables.append(t.to_dict(orient='split'))
    (C/f'BPpool_{ticker}_{key}.json').write_text(json.dumps(tables,indent=2)+'\n')
    tree=html.fromstring(r.text());[x.drop_tree() for x in tree.xpath('//script|//style')]
    text=tree.text_content()
    import re
    record['units']=re.findall(r'Financials in (?:millions|billions) [A-Z]{3}|Currency in [A-Z]{3}',text)
   manifest=[x for x in manifest if x['url']!=url]+[record]
   (P/'fetch_manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
  print(ticker,[(x['page'],x['status']) for x in manifest if x['ticker']==ticker],flush=True)

if __name__=='__main__':
 import sys
 collect('--target' in sys.argv)
