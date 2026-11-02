# TotalEnergies SE (TTE.PA): reduced relative-only inputs

Valuation date: 2026-10-30. Accessed: 2026-11-02. Primary listing Euronext Paris (EPA:TTE), quoted in EUR; consolidated reporting in USD millions. Fiscal year = calendar year; FY2025 = 2025-01-01–2025-12-31; no calendarization or TTM/FY mixing (vendor statistics also carries current/TTM fields — kept separate and unused). France/USD/EUR all present in the dated cache (base 2026-10-30 build + MT.AS top-up); no stage-0 rebuild or top-up needed. Standard / published_damodaran / web_minimum / relative_only. User explicitly requests a short PDF despite the standing no-PDF clause. No DCF or stage-4 recommendation.

| Input | Value | Basis |
|---|---:|---|
| Closing share price (Paris) | EUR 85.43 | 2026-10-30 history close; adj. close identical |
| Current common shares | 2,210 million | Statistics current share class / shares outstanding; FY2025 filing-date count 2,139m differs (−4.3% YoY buybacks) — current count used for market cap, FY basis flagged |
| Market capitalization | EUR 188.52bn | price × current shares = 188.8bn; vendor 188.52bn, gap −0.15% <2% |
| Market capitalization | USD 210.6bn | EUR 188.52bn × 1.1172 USD/EUR (ECB ref 2026-10-30) |
| FY2025 revenue (revenues from sales) | 182,344 | Vendor income statement = issuer "Revenues from sales" 182,344 exactly; issuer headline "Sales" 201,196 is a different aggregate (recorded, not used) |
| FY2025 EBIT | 19,733 | Vendor operating income. Issuer adjusted net operating income from segments 18,474 (APM, −6.4% rel., disclosed not used) |
| FY2025 EBITDA | 32,770 | Vendor income-statement EBITDA = EBIT 19,733 + D&A-for-EBITDA 13,037. Issuer adjusted EBITDA 40,555 is an APM including equity-affiliate income — different perimeter, disclosed not used |
| FY2025 net income (group share) | 13,127 | Vendor = issuer "Net income (TotalEnergies share)" exactly |
| Closing parent common equity | 114,883 | FY2025 vendor balance sheet = issuer shareholders' equity, TotalEnergies share |
| Prior closing common equity | 117,858 | FY2024 |
| FY2025 total assets | 291,055 | Closing consolidated = issuer |
| Total debt incl. leases | 61,421 | ST debt 7,792 + current LTD 2,758 + current leases 1,876 + LT debt 40,944 + LT leases 8,051. Issuer: current borrowings 10,162 + other current fin. liabilities 388 + non-current financial debt 48,995 + leases 8,567 ≈ 68.1bn? — see EV note (perimeters reconcile to ~61.0bn net of financial assets; 0.6% gap on gross) |
| Cash & short-term investments | 29,214 | Cash 26,202 + ST investments 3,012 |
| Long-term investments | 42,462 | Includes equity affiliates (earnings from equity investments 2,553 in EBIT) — EV bridge removes associates contribution inconsistently; flagged, excluded, sensitivity shown |
| NCI | 2,640 | Closing book proxy = issuer non-controlling interests; fair value unavailable |
| EV (base bridge) | USD 245.5bn / EUR 219.7bn | see EV computation note |
| FY2025 CFO | 27,343 | Vendor = issuer cash flow from operating activities exactly |
| FY2025 CFFO / DACF | 27,839 / 29,255 | Issuer APMs (cash flow excl. working capital; debt-adjusted cash flow) — for EV/DACF supplementary cross-check |
| FY2025 CapEx | −15,756 | Purchases of PP&E/intangibles (cash flow) |
| FY2025 common dividends paid | 8,424 | Cash flow; buybacks 8,853 separate. Declared DPS 3.992 USD |
| FY2025 pretax income / tax | 22,449 / 9,092 | Effective tax rate 40.5% |
| FY2025 EPS (basic/diluted) | 5.99 / 5.78 USD | Diluted weighted shares 2,214m = issuer |
| Observed five-year beta | 0.04 | Vendor statistics; positive, below 2.5 → used as observed but flagged as atypically low for an oil major |

## EV computation note (single FX convention)

ECB 2026-10-30: USD 1.1172 per EUR.
- Debt incl. leases: USD 61,421m; NCI 2,640; cash & ST investments 29,214
- EV (USD) = 210,615 + 61,421 + 2,640 − 29,214 = **USD 245,461m** (= EUR 219,711m); long-term investments 42,462 excluded and flagged (equity-affiliate earnings remain in EBIT/EBITDA denominators — recorded limitation).
- Issuer net debt excl. leases 20,215 + leases 8,567 = 28,782 vs vendor net debt 61,421 − 29,214 = 32,207 (≈12% gap): issuer nets current/non-current financial assets (−3,093/−1,991) not captured in the vendor cash & ST-investment line. Recorded, not mixed; vendor series kept uniform across peers.
- Vendor EV 214.61B (quote-side) is ~13% lower: vendor cash field (33.29B) is broader and its debt perimeter differs. Recorded, not mixed.

## Conflicts and cautions

- Vendor "Revenue" 182,344 = issuer "Revenues from sales" exactly (0.0%); issuer headline "Sales" 201,196 is a broader aggregate — kept separate.
- Vendor EBIT 19,733 vs issuer adjusted net operating income 18,474 (−6.4%): adjusted APM disclosed, reported vendor series kept uniform across peers.
- Vendor EBITDA 32,770 vs issuer adjusted EBITDA 40,555: APM includes income from equity affiliates — different perimeter, not used as base.
- Beta 0.04 (5Y) is plausible-valued but atypically low for an integrated oil major (recent commodity-price driven idiosyncratic correlation); flagged, used as observed per published-route rule.
- Shares: current 2,210m vs FY2025 filing 2,139m and basic weighted 2,191m reflect the 2025–26 buy-back; per-share valuation uses current count, EPS-history comparisons note the difference.
- France Aa3/spread 0.48%/CRP 0.74% and USD Rf (Treasury 4.94%, default-free 4.72%) already in dated cache; relative stage does not discount.

## Source lines (reduced step)

- StockAnalysis TTE (EPA) statistics, shares/cap/beta/tax: https://stockanalysis.com/quote/epa/TTE/statistics/ (accessed 2026-11-02)
- StockAnalysis historical close 2026-10-30 (EUR 85.43): https://stockanalysis.com/quote/epa/TTE/history/ (accessed 2026-11-02)
- StockAnalysis income statement FY2025/FY2024, EBITDA bridge, tax: https://stockanalysis.com/quote/epa/TTE/financials/income-statement/ (accessed 2026-11-02)
- StockAnalysis balance sheet FY2025: https://stockanalysis.com/quote/epa/TTE/financials/balance-sheet/ (accessed 2026-11-02)
- StockAnalysis cash flow FY2025: https://stockanalysis.com/quote/epa/TTE/financials/cash-flow-statement/ (accessed 2026-11-02)
- TotalEnergies Q4/FY2025 results (SEC 6-K exhibit 99.1, filed 2026-02-11): revenues from sales 182,344; NI share 13,127; adjusted EBITDA 40,555; CFO 27,343; CFFO 27,839; DACF 29,255; net debt excl. leases 20,215; equity share 114,883; NCI 2,640: https://www.sec.gov/Archives/edgar/data/879764/000110465926013065/tm265640d1_ex99-1.htm (accessed 2026-11-02)
- ECB euro reference rates 2026-10-30: USD 1.1172 per EUR (cache/macro/2026-10-30.json)
