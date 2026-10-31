"""Reproduce the primary-report financial pack (USD millions unless stated)."""
from pathlib import Path
import json
import pandas as pd
from valuation_agent.anomaly import anomaly_table, to_markdown
from valuation_agent.sourcelog import SourceLog, validate

P = Path(__file__).resolve().parent
URLS = {'2021':'https://cdn.arcelormittal.com/media/noaafhzd/arcelor-mittal-annual-report-2021.pdf',
        '2023':'https://cdn.arcelormittal.com/media/cncdyomr/annual-report-2023_combined.pdf',
        '2025':'https://cdn.arcelormittal.com/media/g5obzl05/annual-report-2025.pdf',
        'interim':'https://cdn.arcelormittal.com/media/3d0hbxps/half-year-report-30062026.pdf'}
YEARS = ['2021','2022','2023','2024','2025']
DATA = {
 'revenue':[76571,79844,68275,62441,61352],
 'reported_EBIT':[16976,10272,2340,3310,3628],
 'DA':[2523,2580,2675,2632,2945],
 'impairment':[-218,1026,1038,116,204],
 'gross_interest':[357,401,715,510,577],
 'profit_before_tax':[18025,11255,1260,2915,3602],
 'tax_expense':[2460,1717,238,1535,359],
 'group_NI':[15565,9538,1022,1380,3243],
 'parent_NI':[14956,9302,919,1339,3152],
 'NCI_NI':[609,236,103,41,91],
 'capex':[3008,3468,4613,4405,4337],
 'acquisitions_net_cash':[25,939,2524,184,-47],
 'CFO':[9905,10203,7645,4852,4808],
 'cash':[4215,9300,7686,6400,5392],
 'restricted_cash':[156,114,97,84,84],
 'current_assets':[34939,37118,33240,29382,30605],
 'current_liabilities':[24167,22398,21769,21825,22520],
 'current_debt':[1913,2583,2312,2748,2739],
 'total_debt_incl_leases':[8401,11650,10681,11563,13410],
 'assets':[90512,94547,93917,89385,97703],
 'liabilities':[39168,38957,37849,38099,41167],
 'parent_equity':[49106,53152,53961,49223,54466],
 'NCI_equity':[2238,2438,2107,2063,2070],
 'associate_JV':[10319,10765,10078,11420,10393],
 'other_investments':[1146,1119,513,299,353],
 'employee_benefits':[3772,2606,2741,2338,2526],
 'PPE':[30075,30167,33656,33311,41041],
 'intangibles':[4425,4903,5102,4453,5252],
 'inventory':[19858,20087,18759,16501,18589],
 'receivables':[5143,3839,3661,3375,3476],
 'payables':[15093,13532,13605,12921,13008],
 'shares_year_end_m':[910.893202,805.337929,819.271756,768.546622,761.125819],
 'basic_WA_shares_m':[1105,911,842,788,763],
 'diluted_WA_shares_m':[1108,914,845,791,766],
 'buybacks':[5170,2937,1208,1300,262],
 'dividends_paid_group':[572,663,531,580,542],
 'lease_principal_other':[199,160,253,203,234],
}
df = pd.DataFrame(DATA,index=YEARS).T
df.loc['EBITDA_mechanical'] = df.loc['reported_EBIT'] + df.loc['DA']
df.loc['net_debt_mechanical'] = df.loc['total_debt_incl_leases'] - df.loc['cash']
df.loc['NWC_course'] = df.loc['current_assets']-df.loc['cash']-df.loc['current_liabilities']+df.loc['current_debt']
df.loc['effective_tax'] = df.loc['tax_expense']/df.loc['profit_before_tax']
df.loc['NWC_sales'] = df.loc['NWC_course']/df.loc['revenue']
assert ((df.loc['assets']-df.loc['liabilities']-df.loc['parent_equity']-df.loc['NCI_equity']).abs()<.01).all()
flags = anomaly_table(df,flag_on='either')
# Write flags before attaching the investigation and normalization decisions.
(P/'anomaly_report.md').write_text('# Anomaly report — MT.AS\n\nThreshold: ±30% YoY OR deviation from five-year mean. Flags precede investigation.\n\n'+to_markdown(flags))
flags.to_csv(P/'anomaly_checks.csv',index=False)
interim = pd.DataFrame({
 'H1_2025':[30724,2757,1353,194,270,3105,454,2651,2598,53,1853,1062],
 'H1_2026':[32218,1808,1529,0,335,1579,311,1268,1258,10,2373,952]},
 index=['revenue','reported_EBIT','DA','impairment','gross_interest','profit_before_tax','tax_expense','group_NI','parent_NI','NCI_NI','capex','CFO'])
trailing=df.loc[interim.index,'2025']-interim.H1_2025+interim.H1_2026
bs = pd.Series({'cash':4848,'restricted_cash':50,'current_assets':31992,'current_liabilities':22395,'current_debt':2694,
 'total_debt_incl_leases':14421,'assets':99150,'liabilities':42327,'parent_equity':54820,'NCI_equity':2003,
 'associate_JV':9937,'other_investments':283,'employee_benefits':2428,'PPE':41399,'intangibles':5461,
 'receivables':4508,'inventory':19283,'payables':12932,'shares_m':754.041698},name='2026-06-30')
assert bs.assets == bs.liabilities+bs.parent_equity+bs.NCI_equity
log = SourceLog(P/'source_log.csv')
for metric,row in df.iterrows():
 for year,value in row.items():
  report='2025' if int(year)>=2023 else '2023'
  if year=='2021' and metric not in ['revenue','reported_EBIT','DA','impairment','gross_interest','profit_before_tax','tax_expense','group_NI','parent_NI','NCI_NI','capex','CFO','acquisitions_net_cash','buybacks','dividends_paid_group','lease_principal_other','basic_WA_shares_m','diluted_WA_shares_m']:
   report='2021'
  page={'2021':'PDF 242,244,246; notes 6.1/8/11','2023':'PDF 246,248,249,250; notes 6.1/8/11','2025':'PDF 172,174,175,176; notes 4/6/8/11'}[report]
  derived=metric in ['EBITDA_mechanical','net_debt_mechanical','NWC_course','effective_tax','NWC_sales']
  log.add(company='MT.AS',metric=metric,value=value,unit='ratio' if metric in ['effective_tax','NWC_sales'] else 'million',currency='USD' if 'shares' not in metric and metric not in ['effective_tax','NWC_sales'] else 'n/a',period_start=year+'-01-01',period_end=year+'-12-31',as_of_date='2026-10-30',access_date='2026-10-31',source_name='ArcelorMittal consolidated annual report',url_or_local_file=URLS[report],page_note_sheet_cell=page,dataset_vintage=report,reported_or_adjusted='derived' if derived else 'reported',consolidation_scope='parent' if metric.startswith('parent') or 'shares' in metric else 'consolidated',status='derived' if derived else 'sourced',method_or_formula={'EBITDA_mechanical':'EBIT + DA; not issuer adjusted EBITDA','net_debt_mechanical':'financial debt including leases minus cash','NWC_course':'CA-cash-CL+current financial debt','effective_tax':'tax/PBT','NWC_sales':'NWC/revenue'}.get(metric,'report transcription'),cross_check_source='StockAnalysis AMS/MT financials; differing EBIT definitions reconciled in anomaly report',limitation='2021 prepaid classification differs from aggregator; issuer totals retained')
for period,row in interim.items():
 for metric,value in row.items():
  year=period[-4:]
  log.add(company='MT.AS',metric=metric,value=value,unit='million',currency='USD',period_start=year+'-01-01',period_end=year+'-06-30',as_of_date='2026-10-30',access_date='2026-10-31',source_name='ArcelorMittal half year report 2026',url_or_local_file=URLS['interim'],page_note_sheet_cell='PDF 34,38',reported_or_adjusted='reported',consolidation_scope='consolidated',status='sourced')
for metric,value in bs.items():
 log.add(company='MT.AS',metric=metric,value=value,unit='million',currency='USD' if metric!='shares_m' else 'n/a',period_end='2026-06-30',as_of_date='2026-10-30',access_date='2026-10-31',source_name='ArcelorMittal half year report 2026',url_or_local_file=URLS['interim'],page_note_sheet_cell='PDF 30,36; notes 7/9',reported_or_adjusted='reported',consolidation_scope='consolidated',status='sourced')
log.save();assert not validate(P/'source_log.csv'),validate(P/'source_log.csv')
with pd.ExcelWriter(P/'data_pack.xlsx',engine='openpyxl') as w:
 df.to_excel(w,sheet_name='Annual_USDm')
 interim.to_excel(w,sheet_name='Interim_USDm')
 trailing.to_excel(w,sheet_name='TTM_reported')
 bs.to_excel(w,sheet_name='Latest_balance_sheet')
 flags.to_excel(w,sheet_name='Anomalies',index=False)
 pd.DataFrame(log.rows).to_excel(w,sheet_name='Sources',index=False)
 for ws in w.book:
  ws.freeze_panes='B2';ws.column_dimensions['A'].width=35
  for col in ['B','C','D','E','F','G']:ws.column_dimensions[col].width=21
df.to_csv(P/'annual_financials.csv')
interim.to_csv(P/'interim_financials.csv')
bs.to_csv(P/'latest_balance_sheet.csv')
(P/'financials.json').write_text(json.dumps({'annual':df.to_dict(),'interim':interim.to_dict(),'TTM_reported':trailing.to_dict(),'latest_bs':bs.to_dict(),'source_urls':URLS},indent=2)+'\n')
print('Stage 1 pack:',len(log.rows),'source entries;',int(flags.flag.sum()),'flags; balance sheets tie.')
