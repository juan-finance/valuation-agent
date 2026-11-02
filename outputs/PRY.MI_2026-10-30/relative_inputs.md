# Prysmian S.p.A. (PRY.MI): reduced relative-only inputs

Valuation date: 2026-10-30. Accessed: 2026-11-01 to 2026-11-02. Listing Borsa Italiana (BIT: PRY), quoted and reported in EUR millions. Fiscal year = calendar year; FY2025 = 2025-12-31 year end; no calendarization or TTM/FY mixing. Italy added to the dated cache by the Italy-only top-up (cache/market/2026-10-30/topup_it.py, MANIFEST). EUR needs no FX. Standard / published_damodaran / web_minimum / relative_only. No DCF or stage-4 recommendation.

| Input | Value | Basis |
|---|---:|---|
| Closing share price (BIT) | EUR 110.40 | StockAnalysis history, close 2026-10-30 |
| Current shares | 292.25 million | StockAnalysis statistics |
| Market capitalization | EUR 32,260m | price x shares = 32,260; vendor 32,260 (check gap 0.0001%) |
| FY2025 revenue | 19,741 | StockAnalysis income statement |
| FY2025 EBITDA | 1,979 | StockAnalysis income statement (EBIT 1,531 + D&A 448) |
| FY2025 EBIT | 1,531 | StockAnalysis income statement |
| FY2025 net income (parent) | 1,270 | StockAnalysis income statement |
| Closing parent equity FY2025 | 6,474 | StockAnalysis balance sheet |
| Prior-year parent equity FY2024 | 5,087 | StockAnalysis balance sheet |
| Total assets FY2025 | 20,190 | StockAnalysis balance sheet |
| Total debt incl. leases | 5,227 | StockAnalysis balance sheet |
| Cash & equivalents | 2,025 | StockAnalysis balance sheet |
| NCI | 206 | StockAnalysis balance sheet |
| Associates | not separately collected | EV before associates (35,668) used; flagged |
| EV before associates | EUR 35,668m | 32,260 + 5,227 + 206 - 2,025 |
| FY2025 CFO | 2,162 | StockAnalysis cash flow |
| FY2025 CapEx | 751 | StockAnalysis cash flow |
| Pretax income / tax | 1,654 / 358 | StockAnalysis (effective tax 21.6%) |
| Observed beta | 0.92 | StockAnalysis statistics |
| Consensus growth | not collected for this run | growth basis: fundamental (ROE x retention, 18.0%), as in the peer pool |

## Conflicts and cautions

- Perimeter: Prysmian's Encore Wire acquisition (July 2024) changes the FY2024/FY2025 perimeter; FY2025 is the first full-year base (flagged in candidate notes).
- Annual-report cross-check of these figures: NOT performed in this session. Treat the figures as StockAnalysis-sourced and unverified against the 2025 annual report until a human check is done.
- Consensus analyst growth (g_eps, g_rev) was not collected for PRY.MI. The published PE/PBV/EV-EBITDA equations use analyst growth; under standing approval published_route_allow_fundamental_growth = yes, the fundamental growth is substituted and labelled.
- Earnings basis FY2025; no TTM or forward series mixed in.

## Source lines

- StockAnalysis PRY (BIT) statistics: https://stockanalysis.com/quote/bit/PRY/statistics/ (accessed 2026-11-01)
- StockAnalysis PRY (BIT) price history 2026-10-30: https://stockanalysis.com/quote/bit/PRY/history/ (accessed 2026-11-01)
- StockAnalysis PRY (BIT) income statement FY2025: https://stockanalysis.com/quote/bit/PRY/financials/income-statement/ (accessed 2026-11-01)
- StockAnalysis PRY (BIT) balance sheet FY2025: https://stockanalysis.com/quote/bit/PRY/financials/balance-sheet/ (accessed 2026-11-01)
- StockAnalysis PRY (BIT) cash flow FY2025: https://stockanalysis.com/quote/bit/PRY/financials/cash-flow-statement/ (accessed 2026-11-01)
- Values originally collected in outputs/ENR.DE_2026-10-30/relative/candidate_raw.csv (row PRY) and source_log.csv (S3_PRY_*).
