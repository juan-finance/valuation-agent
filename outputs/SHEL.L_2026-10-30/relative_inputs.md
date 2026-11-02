# Shell plc (SHEL.L): reduced relative-only inputs

Valuation date: 2026-10-30. Accessed: 2026-11-02. Primary listing London Stock Exchange (LON:SHEL), quoted in GBX (pence; divide by 100 for GBP); consolidated reporting in USD millions. Fiscal year = calendar year; FY2025 = 2025-01-01–2025-12-31; no calendarization or TTM/FY mixing (vendor statistics also carries current/TTM fields — kept separate and unused). United Kingdom/USD/GBP all present in the dated cache (base 2026-10-30 build); no stage-0 rebuild or top-up needed. Standard / published_damodaran / web_minimum / relative_only. User explicitly requests a short PDF despite the standing no-PDF clause. No DCF or stage-4 recommendation.

| Input | Value | Basis |
|---|---:|---|
| Closing share price (London) | GBX 4,036.5 = GBP 40.365 | 2026-10-30 history close; adj. close identical |
| Current common shares | 5,700 million | Statistics current share class / shares outstanding; FY2025 filing-date count 5,661m differs (−6.5% YoY buybacks) — current count used for market cap, FY basis flagged |
| Market capitalization | GBP 230.23bn | price × current shares = 230.08bn; vendor 230.23bn, gap −0.06% <2% |
| Market capitalization | USD 308.5bn | GBP 230.23bn × 1.3399 USD/GBP (ECB ref 2026-10-30: USD 1.1172/EUR, GBP 0.8338/EUR) |
| FY2025 revenue | 266,886 | Vendor income statement. Issuer "Total revenue and other income" 273,731 is a broader aggregate (vendor "Revenue as Reported" field matches it exactly) — recorded, headline figure uses the narrower vendor series kept uniform across peers |
| FY2025 EBIT | 29,834 | Vendor operating income |
| FY2025 EBITDA | 47,658 | Vendor income-statement EBITDA = EBIT 29,834 + D&A-for-EBITDA 17,824. Issuer adjusted EBITDA 56,135 is an APM with different adjustments — disclosed, not used |
| FY2025 net income (shareholders) | 17,837 | Vendor; issuer "Income attributable to Shell plc shareholders" 17,838 (−0.01%, within tolerance) |
| Closing parent common equity | 174,392 | FY2025 vendor balance sheet total common equity |
| Prior closing common equity | 178,307 | FY2024 |
| FY2025 total assets | 370,350 | Closing consolidated |
| Total debt incl. leases | 75,688 | ST debt 506 + current LTD 4,030 + current leases 4,611 + LT debt 42,219 + LT leases 24,322. Issuer total debt 75,643 (−0.06%) and issuer net debt 45,687 vs vendor net 45,472 — definitional perimeter differences recorded, vendor series kept uniform |
| Cash & short-term investments | 30,216 | Cash & equivalents 30,216 |
| Long-term investments | 29,332 | Includes equity-accounted investments (earnings from equity investments 1,618 in EBT); excluded from EV bridge, contribution in denominators flagged |
| NCI | 927 | Closing book proxy = vendor minority interest; fair value unavailable |
| EV (base bridge) | USD 354.9bn / EUR 317.6bn | see EV computation note |
| FY2025 CFO | 42,863 | Vendor = issuer cash flow from operating activities exactly |
| FY2025 CapEx | −18,947 | Capital expenditures (cash flow); issuer cash capital expenditure APM 20,915 differs |
| FY2025 common dividends paid | 8,472 | Cash flow; buybacks 15,179 separate. Declared DPS 1.446 USD = issuer exactly |
| FY2025 pretax income / tax | 29,756 / 11,637 | Effective tax rate 39.11% |
| FY2025 EPS (basic/diluted) | 3.03 / 3.00 USD | Basic EPS = issuer exactly; diluted weighted shares 5,949m |
| Observed five-year beta | −0.19 | Vendor statistics; negative → outside 0–2.5 rule, replaced by bottom-up relevered beta for the published regression (score dimension retained with flag) |

## EV computation note (single FX convention)

ECB 2026-10-30: USD 1.1172 per EUR, GBP 0.8338 per EUR (USD/GBP = 1.3399, GBP/USD = 0.74633).
- Debt incl. leases: USD 75,688m; NCI 927; cash & ST investments 30,216
- EV (USD) = 308,473 + 75,688 + 927 − 30,216 = **USD 354,872m** (= EUR 317.6bn = GBP 264.8bn); long-term investments 29,332 excluded and flagged (equity-accounted earnings remain in denominators — recorded limitation).
- Issuer net debt 45,687 vs vendor net debt 75,688 − 30,216 = 45,472 (−0.5%): issuer nets lease/other perimeter differently. Recorded, not mixed; vendor series kept uniform across peers.
- Vendor quote-side EV 260.91B uses its own cash (27.44B) and debt (57.30B) perimeters — different definitions; recorded, not mixed.

## Conflicts and cautions

- Vendor "Revenue" 266,886 vs issuer "Total revenue and other income" 273,731 (vendor carries the issuer aggregate as "Revenue as Reported" 273,731): the narrower vendor series is kept for uniform peer multiples; the issuer aggregate is recorded.
- Vendor EBITDA 47,658 vs issuer adjusted EBITDA 56,135: APM basis differs — disclosed, not used as base.
- Beta −0.19 (5Y) is negative: kept for peer scoring with flag but replaced in the published regression by the bottom-up relevered Oil/Gas (Integrated) Europe beta (unlevered cash-corrected 0.41 × relever at D/E 0.245, effective tax 39.11% → ~0.47) per the published-route rule.
- Shares: current 5,700m vs FY2025 filing 5,661m and basic weighted 5,891m reflect the 2025–26 buy-back; per-share valuation uses current count.
- Adura JV (Shell/Equinor North Sea) completed December 2025 — deconsolidation/associate perimeter note carried to the EV bridge limitation.
- UK/USD/GBP macro fields already in dated cache; relative stage does not discount.

## Source lines (reduced step)

- StockAnalysis SHEL (LON) statistics, shares/cap/beta/tax: https://stockanalysis.com/quote/lon/SHEL/statistics/ (accessed 2026-11-02)
- StockAnalysis historical close 2026-10-30 (GBX 4,036.5): https://stockanalysis.com/quote/lon/SHEL/history/ (accessed 2026-11-02)
- StockAnalysis income statement FY2025/FY2024, EBITDA bridge, tax: https://stockanalysis.com/quote/lon/SHEL/financials/income-statement/ (accessed 2026-11-02)
- StockAnalysis balance sheet FY2025: https://stockanalysis.com/quote/lon/SHEL/financials/balance-sheet/ (accessed 2026-11-02)
- StockAnalysis cash flow FY2025: https://stockanalysis.com/quote/lon/SHEL/financials/cash-flow-statement/ (accessed 2026-11-02)
- Shell plc Q4 2025 and full-year unaudited results (published 2026-02-05): income attributable to shareholders 17,838; adjusted EBITDA 56,135; CFO 42,863; total debt 75,643; net debt 45,687; DPS 1.446; basic EPS 3.03: https://shell.gcs-web.com/news-releases/news-release-details/shell-plc-4th-quarter-2025-and-full-year-unaudited-results (accessed 2026-11-02)
- Shell consolidated financial statements FY2025 (total revenue and other income 273,731): https://www.shell.com/investors/results-and-reporting/annual-report/ (accessed 2026-11-02)
- ECB euro reference rates 2026-10-30: USD 1.1172, GBP 0.8338 per EUR (cache/macro/2026-10-30.json)
