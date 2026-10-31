import json
import unittest
from pathlib import Path
import pandas as pd
from openpyxl import load_workbook
from valuation_agent import comparables as c
from valuation_agent.sourcelog import validate

P=Path(__file__).resolve().parents[1]
R=P/'relative'

class RelativeChecks(unittest.TestCase):
 def test_peer_constraints_and_no_padding(self):
  d=pd.read_csv(R/'comparables.csv')
  self.assertEqual(len(d),9);self.assertEqual(d.comp_ticker.nunique(),9)
  self.assertEqual((d.tier<3).sum(),6);self.assertEqual(d.europe.sum(),6)
  self.assertEqual((d.tier==3).sum(),3)
  self.assertLessEqual(d.market_cap_check.abs().max(),.02)
 def test_no_associate_imputation(self):
  d=pd.read_csv(R/'candidate_raw.csv');self.assertTrue(d.associates.isna().all())
  s=pd.read_csv(R/'multiples_summary.csv');self.assertEqual(s[s.is_primary].multiple.tolist(),['pbv'])
 def test_scaled_primary(self):
  d=pd.read_csv(R/'comparables.csv');t=pd.read_csv(R/'candidate_raw.csv').query('ticker=="MT.AS"').iloc[0]
  v=c.scaled_multiple(d.pbv,d.roe,t.roe,min_valid=6)
  s=pd.read_csv(R/'multiples_summary.csv').query('multiple=="pbv"').iloc[0]
  self.assertTrue(v['available']);self.assertAlmostEqual(v['median'],s.adjusted_multiple)
 def test_published_live_checks(self):
  j=json.loads((R/'model_checks.json').read_text());self.assertEqual(j['formula_errors'],0)
  self.assertLess(max(j['regression_differences']),1e-9);self.assertLess(j['max_score_difference'],1e-9)
 def test_source_schema(self):self.assertEqual(validate(P/'source_log.csv'),[])
 def test_workbook_formulas_retained(self):
  w=load_workbook(R/'regression_valuation.xlsx');self.assertEqual(w['Equations']['G2'].data_type,'f')
  w=load_workbook(R/'comparables_audit.xlsx');self.assertEqual(w['Score_Live']['AB3'].data_type,'f')

if __name__=='__main__':unittest.main()
