"""Auditable MT.AS FCFF forecast; existing library supplies valuation arithmetic."""
from pathlib import Path
import json
import math
import pandas as pd
from openpyxl import Workbook, load_workbook
from openpyxl.styles import Font, PatternFill
from valuation_agent import datasets as ds, dcf
from valuation_agent.sourcelog import SourceLog

P=Path(__file__).resolve().parent
ROOT=P.parents[1]
F=json.loads((P/'financials.json').read_text())
H=pd.DataFrame(F['annual'])
B=F['latest_bs']
IND=json.loads((P/'industry_resolved.json').read_text())
RP=ds.load_risk_premiums(ds.resolve('ctryprem',country='Luxembourg',valuation_date='2026-10-30').dataset)
GEO={'United States':9184,'Brazil':7121,'Canada':3164,'Mexico':2314,'Argentina':897,'Germany':5704,'Poland':4412,'France':4052,'Spain':3719,'Italy':2655,'Czech Republic':1147,'Turkey':957,'United Kingdom':1568,'Belgium':1474,'Netherlands':1219,'Romania':483,'Ukraine':572,'South Africa':1567,'Morocco':955,'China':1167,'South Korea':261,'India':435}
georows=[]
for country,revenue in GEO.items():
 risk=ds.country_risk(RP,country)
 georows.append(dict(country=country,revenue=revenue,weight=revenue/61352,crp=risk['crp'],default_spread=risk['default_spread'],method='disclosed country'))
for name,revenue,region in [('Other Americas',964,'Central and South America'),('Other Europe',4246,'Western Europe'),('Rest Africa',370,'Africa'),('Rest Asia',745,'Asia')]:
 t=RP['rated'];t=t[t.Region==region]
 georows.append(dict(country=name,revenue=revenue,weight=revenue/61352,crp=float(t['Country Risk Premium (CRP)'].mean()),default_spread=float(t['Rating-based Default Spread'].mean()),method='unweighted disclosed-country regional proxy: '+region))
assert sum(x['revenue'] for x in georows)==61352
geo=pd.DataFrame(georows)
geo.to_csv(P/'geographic_risk.csv',index=False)
CRP=dcf.weighted_average(geo.weight.tolist(),geo.crp.tolist())
BU=dcf.weighted_average([1-1365/61352,1365/61352],[.85,.96])
# Adjustments remove accounting exceptions, not recurring operating inefficiency.
ADJ=pd.DataFrame(index=H.columns)
ADJ['reported_EBIT']=H.loc['reported_EBIT']
ADJ['DA']=H.loc['DA']
ADJ['impairment_adjustment']=H.loc['impairment']
ADJ['disposal_adjustment']=[-104,0,1469,0,0]
ADJ['bargain_gain_adjustment']=[0,-100,0,0,-1858]
ADJ['settlement_adjustment']=[0,0,0,0,420]
ADJ['adjusted_EBIT']=ADJ[['reported_EBIT','impairment_adjustment','disposal_adjustment','bargain_gain_adjustment','settlement_adjustment']].sum(axis=1)
ADJ['adjusted_EBITDA']=ADJ.adjusted_EBIT+ADJ.DA
ADJ['group_NI_reported']=H.loc['group_NI']
ADJ['NI_adjustment_est_tax25pct']=(ADJ.adjusted_EBIT-ADJ.reported_EBIT)*.75
ADJ['associate_impairment_addback_est_tax25pct']=[0,0,1405*.75,0,123*.75]
ADJ['adjusted_group_NI_estimate']=ADJ.group_NI_reported+ADJ.NI_adjustment_est_tax25pct+ADJ.associate_impairment_addback_est_tax25pct
ADJ['effective_tax']=H.loc['effective_tax']
ADJ.to_csv(P/'earnings_reconciliation.csv')
MID=float(ADJ.adjusted_EBITDA.mean())
MARGIN=MID/float(H.loc['revenue'].mean())
INPUT={
 'sales0':62846.,'EBITDA0':6230.,'DA0':3121.,'growth1':.03,'growth_terminal':.025,
 'margin0':6230/62846,'margin_target':MARGIN,'DA_sales':3121/62846,
 'tax_operating':.25,'tax_marginal':.2387,'nce_ratio_explicit':.8,'ROC_terminal':.08,
 'rf':.0472,'erp':.042,'crp':CRP,'beta_u':BU,'corporate_spread':.0111,
 'shares_basic_m':749.710746,'dilution_m':3.,'price_EUR':53.6,'USD_per_EUR':1.1172,
 'debt_fair_proxy':14716.,'debt_book':14421.,'target_delta':.2906,
 'nwc0':dcf.nwc(B['current_assets'],B['cash'],B['current_liabilities'],B['current_debt']),
 'nwc_ratio_company':float(H.loc['NWC_course','2025']/H.loc['revenue','2025']),'nwc_ratio_industry':.1984,
 'excess_cash':4848-628.46,'associates':9937.,'investments':283.,'NCI':2003.,
 'pension_claim_aftertax':2428*.75,'provision_extra':0.,'WACC_shock':0.,
 'explicit_years':10.,'first_stage_years':5.,'early_growth_years':3.,
}

def calculate(overrides=None):
 a={**INPUT,**(overrides or {})}
 shares=a['shares_basic_m']+a['dilution_m']
 E=a['shares_basic_m']*a['price_EUR']*a['USD_per_EUR']
 delta0=a['debt_fair_proxy']/(E+a['debt_fair_proxy'])
 rn=dcf.forecast_nwc_ratio(a['nwc_ratio_company'],a['nwc_ratio_industry'])
 sales=a['sales0'];nwc0=a['nwc0'];rows=[]
 for year in range(1,12):
  growth=a['growth1'] if year<=3 else a['growth_terminal']
  sales*=1+growth
  margin=a['margin0']+(a['margin_target']-a['margin0'])*min(year/5,1)
  da=sales*a['DA_sales'];ebit=sales*margin-da
  nopat=dcf.nopat(ebit,a['tax_operating'])
  nwcr=dcf.nwc_schedule([sales],rn,nwc0)[0]
  nce_terminal=dcf.stable_reinvestment_rate(a['growth_terminal'],a['ROC_terminal'])-nwcr.floored_delta/nopat
  ncer=a['nce_ratio_explicit'] if year<=5 else a['nce_ratio_explicit']+(nce_terminal-a['nce_ratio_explicit'])*min((year-5)/5,1)
  nce=ncer*nopat
  delta=delta0+(a['target_delta']-delta0)*min(year/5,1)
  beta=dcf.relever_beta(a['beta_u'],dcf.de_from_debt_ratio(delta),a['tax_marginal'])
  ke=dcf.ke_additive(a['rf'],beta,a['erp'],a['crp'])
  kd=dcf.kd_pre_tax(a['rf'],a['corporate_spread'],a=0)
  wacc=dcf.wacc(1-delta,delta,ke,kd,a['tax_marginal'])+a['WACC_shock']
  cf=dcf.fcff(ebit,a['tax_operating'],nce,nwcr.floored_delta)
  rows.append(dict(year=year,growth=growth,sales=sales,margin=margin,DA=da,EBIT=ebit,NOPAT=nopat,nce_ratio=ncer,NCE=nce,capex_incl_ROU=nce+da,NWC=nwcr.nwc_balance,raw_delta=nwcr.raw_delta,floor=nwcr.floored_delta,FCFF=cf,delta=delta,beta=beta,Ke=ke,Kd=kd,WACC=wacc))
  nwc0=nwcr.nwc_balance
 r=dcf.value_cash_flows([x['FCFF'] for x in rows[:10]],[x['WACC'] for x in rows[:10]],rows[10]['FCFF'],rows[10]['WACC'],a['growth_terminal'])
 bridge=[('excess cash',a['excess_cash']),('associates',a['associates']),('investments',a['investments']),('financial debt',-a['debt_fair_proxy']),('NCI',-a['NCI']),('pension after tax',-a['pension_claim_aftertax']),('other nonoperating liabilities',-a['provision_extra'])]
 eq,_=dcf.equity_bridge(r.total,bridge)
 ps=dcf.value_per_share(eq,shares)/a['USD_per_EUR']
 floor_cost=sum((x['floor']-x['raw_delta'])*f for x,f in zip(rows[:10],r.factors))/shares/a['USD_per_EUR']
 return dict(rows=rows,result=vars(r),bridge=bridge,equity=eq,EUR_per_share=ps,upside=dcf.upside(ps,a['price_EUR']),floor_cost_EUR=floor_cost,delta0=delta0,nwc_ratio=rn,shares=shares)

def build():
 base=calculate()
 cases={'low':calculate({'margin_target':MARGIN*.75,'growth1':.01,'growth_terminal':.015,'WACC_shock':.01,'ROC_terminal':.065}), 'base':base,'high':calculate({'margin_target':MARGIN*1.15,'growth1':.05,'growth_terminal':.03,'WACC_shock':-.005,'ROC_terminal':.10})}
 shocked={
  'midcycle EBITDA margin −25%/+15%':(calculate({'margin_target':MARGIN*.75})['EUR_per_share'],calculate({'margin_target':MARGIN*1.15})['EUR_per_share']),
  'WACC +1%/−1%':(calculate({'WACC_shock':.01})['EUR_per_share'],calculate({'WACC_shock':-.01})['EUR_per_share']),
  'terminal ROC 6.5%/10%':(calculate({'ROC_terminal':.065})['EUR_per_share'],calculate({'ROC_terminal':.10})['EUR_per_share']),
  'associates −30%/+30%':(calculate({'associates':9937*.7})['EUR_per_share'],calculate({'associates':9937*1.3})['EUR_per_share']),
  'explicit NCE ratio 0.93/0.77':(calculate({'nce_ratio_explicit':.93})['EUR_per_share'],calculate({'nce_ratio_explicit':.77})['EUR_per_share']),
 }
 drivers=dcf.rank_drivers(base['EUR_per_share'],shocked)
 out=dict(inputs=INPUT,cases=cases,drivers=drivers,midcycle_EBITDA=MID,midcycle_margin=MARGIN,geo=georows)
 (P/'dcf_results.json').write_text(json.dumps(out,indent=2)+'\n')
 pd.DataFrame(base['rows']).to_csv(P/'dcf_forecast.csv',index=False)
 wb=Workbook();ws=wb.active;ws.title='Inputs';ws.append(['Assumption','Value','Definition / provenance'])
 ix={}
 for n,v in INPUT.items():
  ws.append([n,v,'See source_log.csv and dcf_decisions.md; all rates decimal'])
  ix[n]=f"Inputs!$B${ws.max_row}"
 ref=lambda n:ix[n]
 ws=wb.create_sheet('Historical')
 ws.append(['metric']+list(H.columns))
 for metric,row in H.iterrows():ws.append([metric]+list(row))
 ws=wb.create_sheet('Capital_structure')
 t=pd.read_csv(P/'capital_structure.csv');ws.append(t.columns.tolist())
 for row in t.itertuples(index=False,name=None):ws.append(list(row))
 ws=wb.create_sheet('Returns_reinvestment');ws.append(['Year','Beginning book operating capital','Adjusted NOPAT25pct','ROC','NCE including ROU','NCE/NOPAT','Signed historical dNWC','Reinvestment rate','Fundamental growth'])
 for year,prior,rou in [('2024','2023',209),('2025','2024',274)]:
  hp=H[prior];hy=H[year];ic=hp.total_debt_incl_leases+hp.parent_equity+hp.NCI_equity-hp.cash-hp.associate_JV-hp.other_investments
  np=dcf.nopat(float(ADJ.loc[year,'adjusted_EBIT']),INPUT['tax_operating']);nc=dcf.nce(hy.capex+rou,hy.DA);dn=hy.NWC_course-hp.NWC_course;roc=dcf.roc(np,ic);rr=dcf.firm_reinvestment_rate(nc,dn,np)
  ws.append([year,ic,np,roc,nc,nc/np,dn,rr,dcf.fundamental_growth(rr,roc)])
 ws.append(['Industry Steel EUROPE Jan2026','Net Cap Ex/EBIT(1-t)',8.8356,'distorted denominator; rejected; current/prior company range used'])
 ws=wb.create_sheet('Earnings_bridge');ws.append(['year']+ADJ.columns.tolist())
 for y,row in ADJ.iterrows():ws.append([y]+list(row))
 ws=wb.create_sheet('Geography');ws.append(geo.columns.tolist())
 for row in geo.itertuples(index=False,name=None):ws.append(list(row))
 ws=wb.create_sheet('Forecast')
 ws.append(['year','sales growth','sales','EBITDA margin','D&A','EBIT','NOPAT','NCE/NOPAT','NCE','capex incl ROU','NWC','raw change','floored change','FCFF','market debt ratio','beta','Ke','Kd','WACC','DF','PV FCFF'])
 for r in range(2,13):
  y=r-1;prev=f'C{r-1}' if r>2 else ref('sales0');prevnw=f'K{r-1}' if r>2 else ref('nwc0')
  formulas=[y,f'=IF(A{r}<={ref("early_growth_years")},{ref("growth1")},{ref("growth_terminal")})',f'={prev}*(1+B{r})',f'={ref("margin0")}+({ref("margin_target")}-{ref("margin0")})*MIN(A{r}/{ref("first_stage_years")},1)',f'=C{r}*{ref("DA_sales")}',f'=C{r}*D{r}-E{r}',f'=F{r}*(1-{ref("tax_operating")})',f'=IF(A{r}<={ref("first_stage_years")},{ref("nce_ratio_explicit")},{ref("nce_ratio_explicit")}+({ref("growth_terminal")}/{ref("ROC_terminal")}-M{r}/G{r}-{ref("nce_ratio_explicit")})*MIN((A{r}-{ref("first_stage_years")})/{ref("first_stage_years")},1))',f'=H{r}*G{r}',f'=I{r}+E{r}',f'=C{r}*({ref("nwc_ratio_company")}+{ref("nwc_ratio_industry")})/2',f'=K{r}-{prevnw}',f'=MAX(L{r},0)',f'=G{r}-I{r}-M{r}',f'=({ref("debt_fair_proxy")}/({ref("debt_fair_proxy")}+{ref("shares_basic_m")}*{ref("price_EUR")}*{ref("USD_per_EUR")}))+({ref("target_delta")}-({ref("debt_fair_proxy")}/({ref("debt_fair_proxy")}+{ref("shares_basic_m")}*{ref("price_EUR")}*{ref("USD_per_EUR")})))*MIN(A{r}/{ref("first_stage_years")},1)',f'={ref("beta_u")}*(1+(1-{ref("tax_marginal")})*O{r}/(1-O{r}))',f'={ref("rf")}+P{r}*{ref("erp")}+{ref("crp")}',f'={ref("rf")}+{ref("corporate_spread")}',f'=(1-O{r})*Q{r}+O{r}*R{r}*(1-{ref("tax_marginal")})+{ref("WACC_shock")}',f'=1/(1+S{r})' if r==2 else f'=T{r-1}/(1+S{r})',f'=N{r}*T{r}']
  ws.append(formulas)
 ws=wb.create_sheet('Equity_bridge');ws.append(['Item','USD million'])
 for label,formula in [('PV explicit','=SUM(Forecast!U2:U11)'),('Terminal value',f'=Forecast!N12/(Forecast!S12-{ref("growth_terminal")})'),('PV terminal','=B3*Forecast!T11'),('Operating EV','=B2+B4')]:ws.append([label,formula])
 for label,key,sign in [('excess cash','excess_cash',1),('associates','associates',1),('investments','investments',1),('financial debt','debt_fair_proxy',-1),('NCI','NCI',-1),('pensions','pension_claim_aftertax',-1),('other liabilities','provision_extra',-1)]:ws.append([label,f'={sign}*{ref(key)}'])
 ws.append(['Common equity','=SUM(B5:B12)']);ws.append(['Diluted shares',f'={ref("shares_basic_m")}+{ref("dilution_m")}']);ws.append(['EUR per share',f'=B13/B14/{ref("USD_per_EUR")}']);ws.append(['Upside',f'=B15/{ref("price_EUR")}-1']);ws.append(['Terminal dependence','=B4/B5']);ws.append(['NWC floor PV cost EUR',f'=SUMPRODUCT(Forecast!M2:M11,Forecast!T2:T11)/B14/{ref("USD_per_EUR")}-SUMPRODUCT(Forecast!L2:L11,Forecast!T2:T11)/B14/{ref("USD_per_EUR")}'])
 ws=wb.create_sheet('Sensitivity');ws.append(['WACC shift / terminal g',.015,.02,.025,.03,.035])
 for rr,shock in enumerate([-.01,-.005,0,.005,.01],start=2):
  ws.cell(rr,1,shock)
  for cc in range(2,7):
   from openpyxl.utils import get_column_letter
   g=f'{get_column_letter(cc)}$1';shift=f'$A{rr}'
   terms=[];den='1'
   for fr in range(2,12):
    den+=f'*(1+Forecast!S{fr}+{shift})';terms.append(f'Forecast!N{fr}/({den})')
   tv=f'(Forecast!G11*(1+{g})*(1-{g}/{ref("ROC_terminal")}))/(Forecast!S12+{shift}-{g})/({den})'
   eq='+' .join(terms)+f'+{tv}+SUM(Equity_bridge!B6:B12)'
   ws.cell(rr,cc,f'=IF(Forecast!S12+{shift}<={g},"invalid",({eq})/Equity_bridge!B14/{ref("USD_per_EUR")})')
 ws=wb.create_sheet('Scenarios');ws.append(['case','EUR/share','upside','terminal dependence'])
 for k,v in cases.items():ws.append([k,v['EUR_per_share'],v['upside'],v['result']['tv_share']])
 ws=wb.create_sheet('Drivers');ws.append(['driver','low EUR','high EUR','swing EUR'])
 for r in drivers:ws.append([r['driver'],r['low'],r['high'],r['swing']])
 ws=wb.create_sheet('QA');ws.append(['Check','Expected','Workbook actual']);ws.append(['EUR/share library',base['EUR_per_share'],'=Equity_bridge!B15']);ws.append(['Difference',None,'=C2-B2']);ws.append(['stable reinvestment consistency',0,f'=Forecast!I12+Forecast!M12-Forecast!G12*{ref("growth_terminal")}/{ref("ROC_terminal")}'])
 for ws in wb:
  ws.freeze_panes='B2';ws.auto_filter.ref=ws.dimensions
  for cell in ws[1]:cell.font=Font(color='FFFFFF',bold=True);cell.fill=PatternFill('solid',fgColor='17324D')
  ws.column_dimensions['A'].width=35
  for col in range(2,ws.max_column+1):
   from openpyxl.utils import get_column_letter
   ws.column_dimensions[get_column_letter(col)].width=20
   for row in range(2,ws.max_row+1):ws.cell(row,col).number_format='#,##0.0000'
 wb.save(P/'dcf_model.xlsx')
 print(json.dumps({k:round(v['EUR_per_share'],2) for k,v in cases.items()}));print('CRP',CRP,'beta_U',BU,'midcycle',MID,'margin',MARGIN,'WACC',base['rows'][0]['WACC'],base['rows'][-1]['WACC'],'terminal share',base['result']['tv_share'])

if __name__=='__main__':build()
