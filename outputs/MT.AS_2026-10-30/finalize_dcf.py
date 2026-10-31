"""Extend audit evidence and refresh the summary after workbook recalculation."""
from pathlib import Path
import json
import pandas as pd
from openpyxl import load_workbook
from PIL import Image,ImageDraw,ImageFont
from valuation_agent import dcf
from valuation_agent.sourcelog import SourceLog,validate
from build_dcf import calculate,INPUT,H,ADJ

P=Path(__file__).resolve().parent
o=json.loads((P/'dcf_results.json').read_text());b=o['cases']['base'];rr=b['rows']
wb=load_workbook(P/'dcf_model.xlsx',data_only=True)
errors=[(s.title,c.coordinate,c.value) for s in wb for row in s for c in row if c.data_type=='e']
assert not errors,errors
assert abs(wb['Equity_bridge']['B15'].value-b['EUR_per_share'])<1e-8
assert abs(wb['Sensitivity']['D4'].value-b['EUR_per_share'])<1e-8
assert abs(wb['QA']['C4'].value)<1e-8
checks={'workbook_formula_errors':errors,'library_EUR_per_share':b['EUR_per_share'],'workbook_EUR_per_share':wb['Equity_bridge']['B15'].value,'absolute_difference':abs(wb['Equity_bridge']['B15'].value-b['EUR_per_share']),'terminal_reinvestment_difference':wb['QA']['C4'].value,'checklist_status':'deferred to company end under approved deviation','unresolved':'shares, bond YTM, claim fair values, human spot-check; valuation provisional'}
(P/'model_checks.json').write_text(json.dumps(checks,indent=2)+'\n')
extra={'operating tax20%':{'tax_operating':.20},'operating tax30%':{'tax_operating':.30},'CRP minus1point':{'crp':INPUT['crp']-.01},'CRP plus1point':{'crp':INPUT['crp']+.01},'debt fair proxy minus10%':{'debt_fair_proxy':INPUT['debt_fair_proxy']*.9},'debt fair proxy plus10%':{'debt_fair_proxy':INPUT['debt_fair_proxy']*1.1},'NCI50% of book':{'NCI':1001.5},'NCI150% of book':{'NCI':3004.5},'pension gross not net tax':{'pension_claim_aftertax':2428},'additional provisions1000':{'provision_extra':1000},'no dilution reserve':{'dilution_m':0},'extra shares3m':{'dilution_m':6},'faster3year margin recovery':{}}
rows=[]
for name,changes in extra.items():
 if name.startswith('faster'):continue
 r=calculate(changes);rows.append({'case':name,'EUR_per_share':r['EUR_per_share'],'delta_EUR':r['EUR_per_share']-b['EUR_per_share'],'assumptions':str(changes)})
pd.DataFrame(rows).to_csv(P/'additional_dcf_sensitivities.csv',index=False)
risk=[]
for r in [rr[0],rr[-1]]:
 risk.append({'year':r['year'],'betaL':r['beta'],'Ke_additive':r['Ke'],'Ke_beta_scaled':dcf.ke_beta_scaled(INPUT['rf'],r['beta'],INPUT['erp'],INPUT['crp']),'Kd':r['Kd'],'aftertax_Kd':dcf.kd_after_tax(r['Kd'],INPUT['tax_marginal']),'WACC':r['WACC']})
pd.DataFrame(risk).to_csv(P/'risk_checks.csv',index=False)
with (P/'dcf_decisions.md').open('a') as f:
 f.write('\n## Numerical follow-through\n')
 f.write(f'Exact base EUR{b["EUR_per_share"]:.8f}; equity USD{b["equity"]:.4f}m; operating EV USD{b["result"]["total"]:.4f}m. Gross debt/cash net-debt reconciliation9500 vs mechanical9573 differs by50 restricted and23 held-for-sale cash. First forecast capex including ROU is USD{rr[0]["capex_incl_ROU"]:.1f}m, so it is above calendar2026 cash guidance partly due to date/ROU perimeter, not falsely stated as matching guidance. Additional tax/CRP/bridge/share stresses are in additional_dcf_sensitivities.csv.\n')
 f.write('Growth checks: adjusted EBIT historical linear trend is shown as a poor extrapolation, not a forecast; initial5year forecast CAGR is ' +f'{(rr[4]["EBIT"]/3109)**(.2)-1:.2%}. Current/prior annual intrinsic growth is calculated in workbook Returns_reinvestment. Margin recovery adds growth beyond reinvestment identity and is explicitly uncertain.\n')
 trend=pd.Series(ADJ.adjusted_EBIT.values,index=range(5))
 import numpy as np
 slope,intercept=np.polyfit(trend.index,trend.values,1)
 f.write(f'Five-year adjusted EBIT least-squares trend: intercept{intercept:.2f}, slope{slope:.2f} USDm/year; extrapolated next year{intercept+5*slope:.2f}. Peak-year sensitivity invalidates a positive perpetual extrapolation.\n')
l=SourceLog(P/'source_log.csv')
for key in ['nwc_ratio_company','nwc0']:
 l.add(company='MT.AS',metric='DCF input corrected/'+key,value=INPUT[key],unit='decimal ratio' if 'ratio' in key else 'USD million',currency='USD' if key=='nwc0' else 'n/a',period_end='2026-10-30',as_of_date='2026-10-30',access_date='2026-10-31',source_name='Library-derived source-components identity',url_or_local_file='financials.json',page_note_sheet_cell='annual 2025 NWC_course or latest BS; build_dcf.py INPUT',reported_or_adjusted='derived',consolidation_scope='consolidated',method_or_formula='CA-cash-CL+current financial debt; annual divide by sales where applicable',status='derived',limitation='Supersedes earlier draft DCF input row; no primary financial history changed')
for metric,value,url,loc,status in [('rating_BBB_spread',.0111,'data/damodaran/2026-01/ratings_global.md','Large Non-Financial Service Firms: Baa2/BBB default spread','sourced'),('actual_rating','Baa2/BBB stable','https://corporate.arcelormittal.com/investors/fixed-income-investors/credit-ratings','Current ratings; actions December4,2025 / June9,2025','sourced'),('ECB_historical_FX','see historical_fx.csv','https://data-api.ecb.europa.eu/service/data/EXR/D.USD.EUR.SP00.A?startPeriod=2021-12-20&endPeriod=2025-12-31&format=csvdata','Last available reference observation of each year','sourced'),('annual_historical_closes','26.17/23.17/24.66/21.96/38.83 EUR','https://stockanalysis.com/quote/ams/MT/financials/ratios/','Last Close Price FY2021–25; exact holiday closes use preceding session','sourced')]:
 l.add(company='MT.AS',metric=metric,value=value,unit='as named',currency='n/a',as_of_date='2026-10-30',access_date='2026-10-31',source_name='Opened registered or official/vendor source',url_or_local_file=url,page_note_sheet_cell=loc,reported_or_adjusted='reported',consolidation_scope='company',status=status)
l.save();assert not validate(P/'source_log.csv')
im=Image.new('RGB',(1400,920),'#F4F6FA');d=ImageDraw.Draw(im)
font='/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf';ft=ImageFont.truetype(font,38);fb=ImageFont.truetype(font,26)
d.rectangle((0,0,1400,135),fill='#17324D');d.text((55,40),'ArcelorMittal | FCFF | 30 October 2026',font=ft,fill='white')
lines=[f'Base EUR {b["EUR_per_share"]:.2f} | Price EUR 53.60 | {b["upside"]:+.1%}',f'Low / base / high: EUR {o["cases"]["low"]["EUR_per_share"]:.2f} / {b["EUR_per_share"]:.2f} / {o["cases"]["high"]["EUR_per_share"]:.2f}','5 recovery + 5 transition years; terminal g 2.5%, ROC 8.0%',f'Mid-cycle EBITDA USD {o["midcycle_EBITDA"]:,.0f}m; target margin {o["midcycle_margin"]:.2%}',f'USD Rf 4.72%; CRP {INPUT["crp"]:.2%}; beta U {INPUT["beta_u"]:.3f}',f'Ke {rr[0]["Ke"]:.2%} to {rr[-1]["Ke"]:.2%}; Kd 5.83%; WACC {rr[0]["WACC"]:.2%} to {rr[-1]["WACC"]:.2%}',f'Operating EV USD {b["result"]["total"]:,.0f}m; common equity {b["equity"]:,.0f}m',f'Terminal PV share {b["result"]["tv_share"]:.1%}: HIGH terminal dependence','Cash +4,220; associates +9,937; investments +283 (USDm)','Debt -14,716; NCI -2,003; after-tax pensions -1,821',f'Diluted denominator {b["shares"]:.3f}m (estimate plus 3m reserve)','PROVISIONAL: shares, claim fair values and human review unresolved.']
for i,line in enumerate(lines):d.text((55,175+56*i),line,font=fb,fill='#17324D')
im.save(P/'dcf_summary.png')
for c in P.glob('*.csv'):c.write_text(c.read_text())
print(checks)
