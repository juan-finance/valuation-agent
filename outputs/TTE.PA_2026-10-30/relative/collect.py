"""Small dated extracts, reusing shared candidate tables; no market rebuild."""
import json,re
from pathlib import Path
from lxml import html
from valuation_agent.cachefetch import CachedFetcher,html_tables
P=Path(__file__).resolve().parent; ROOT=P.parents[2]; C=ROOT/'cache/market/2026-10-30/candidates'
CANDIDATES=[
('TTE','TotalEnergies','epa/TTE',0,'target'),
('SHEL','Shell','lon/SHEL',1,'integrated oil and gas major'),
('BP','BP','lon/BP',1,'integrated oil and gas major'),
('EQNR','Equinor','osl/EQNR',1,'integrated oil and gas major'),
('ENI','Eni','bit/ENI',1,'integrated oil and gas major'),
('REP','Repsol','bme/REP',1,'integrated oil and gas, Iberia'),
('OMV','OMV','vie/OMV',1,'integrated oil, gas and chemicals'),
('AKRBP','Aker BP','osl/AKRBP',1,'Norwegian continental shelf E&P'),
('VAR','Var Energi','osl/VAR',1,'Norwegian continental shelf E&P'),
('HBR','Harbour Energy','lon/HBR',1,'North Sea E&P'),
('ITH','Ithaca Energy','lon/ITH',1,'North Sea E&P'),
('ENOG','Energean','lon/ENOG',1,'Mediterranean gas E&P'),
('DNO','DNO','osl/DNO',1,'North Sea / Middle East E&P'),
('BWO','BW Energy','osl/BWO',1,'offshore E&P'),
('GENL','Genel Energy','lon/GENL',1,'Kurdistan E&P; small-cap screen'),
('TLW','Tullow Oil','lon/TLW',1,'West Africa E&P; small-cap screen'),
('NESTE','Neste','hel/NESTE',2,'renewable fuels and oil refining'),
('SUBC','Subsea 7','osl/SUBC',3,'offshore energy services; not E&P'),
('SPM','Saipem','bit/SPM',3,'oil and gas engineering and drilling services'),
('TE','Technip Energies','epa/TE',3,'LNG/energy engineering services'),
('TGS','TGS','osl/TGS',3,'energy data and seismic services'),
('SBMO','SBM Offshore','ams/SBMO',3,'FPSO leasing and services'),
('AKSO','Aker Solutions','osl/AKSO',3,'oilfield engineering services'),
('XOM','Exxon Mobil','stocks/xom',1,'integrated oil and gas major; World expansion only'),
('CVX','Chevron','stocks/cvx',1,'integrated oil and gas major; World expansion only'),
('COP','ConocoPhillips','stocks/cop',1,'independent E&P; World expansion only'),
('EOG','EOG Resources','stocks/eog',1,'independent E&P; World expansion only'),
('OXY','Occidental','stocks/oxy',1,'E&P and chemicals; World expansion only'),
('CNQ','Canadian Natural Resources','stocks/cnq',1,'oil sands E&P; World expansion only'),
('IMO','Imperial Oil','stocks/imo',1,'integrated oil, Exxon-controlled; World expansion only'),
('PSX','Phillips 66','stocks/psx',2,'refining and midstream; World expansion only'),
('VLO','Valero','stocks/vlo',2,'refining; World expansion only'),
]
F=CachedFetcher(ROOT/'cache/web/2026-10-30',min_delay=1.1,user_agent='ValuationResearchAI/1.0 (educational AI research; robots compliant)')
def collect():
 m=[]
 for ticker,name,route,tier,hypothesis in CANDIDATES:
  base='https://stockanalysis.com/'+(route if route.startswith('stocks/') else 'quote/'+route)+'/'
  for page in ['statistics/','financials/','financials/income-statement/','financials/balance-sheet/','financials/cash-flow-statement/','history/','']:
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
