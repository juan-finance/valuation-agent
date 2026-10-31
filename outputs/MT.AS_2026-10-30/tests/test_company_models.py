import importlib.util
import unittest
from pathlib import Path
from openpyxl import load_workbook
from valuation_agent import dcf

P=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('mt_dcf',P/'build_dcf.py')
model=importlib.util.module_from_spec(spec)
spec.loader.exec_module(model)

class CompanyModelTests(unittest.TestCase):
    def test_balance_sheets(self):
        for y in model.H.columns:
            h=model.H[y]
            self.assertAlmostEqual(h.assets,h.liabilities+h.parent_equity+h.NCI_equity)

    def test_geography_complete(self):
        self.assertEqual(sum(x['revenue'] for x in model.georows),61352)

    def test_selected_nwc_matches_sources(self):
        h=model.H['2025']
        self.assertAlmostEqual(model.INPUT['nwc_ratio_company'],dcf.nwc(h.current_assets,h.cash,h.current_liabilities,h.current_debt)/h.revenue)

    def test_terminal_reinvestment(self):
        r=model.calculate()['rows'][-1]
        self.assertAlmostEqual(r['NCE']+r['floor'],r['NOPAT']*.025/.08)

    def test_live_workbook_equivalence(self):
        w=load_workbook(P/'dcf_model.xlsx',data_only=True)
        self.assertAlmostEqual(w['Equity_bridge']['B15'].value,model.calculate()['EUR_per_share'],places=8)

    def test_monotonic_margin(self):
        self.assertLess(model.calculate({'margin_target':.10})['EUR_per_share'],model.calculate()['EUR_per_share'])

    def test_monotonic_discount(self):
        self.assertLess(model.calculate({'WACC_shock':.01})['EUR_per_share'],model.calculate()['EUR_per_share'])

    def test_invalid_perpetuity(self):
        with self.assertRaises(ValueError):dcf.terminal_value(100,.02,.025)

    def test_bridge_no_double_debt(self):
        r=model.calculate()
        self.assertAlmostEqual(r['equity'],r['result']['total']+sum(x[1] for x in r['bridge']))

if __name__=='__main__':unittest.main()
