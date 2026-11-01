# Equinor ASA (EQNR.OL): reduced relative-only inputs

Valuation date: 2026-10-30. Accessed: 2026-11-01. Primary listing Oslo Børs (OSL:EQNR), quoted in NOK; consolidated reporting in USD millions. Fiscal year = calendar year; FY2025 = 2025-01-01–2025-12-31; no calendarization or TTM/FY mixing (TTM Sep-26 exists on the vendor page but is kept separate and unused). Norway/USD/NOK all present in the dated cache after the EQNR top-up; no stage-0 rebuild. Standard / published_damodaran / web_minimum / relative_only. User explicitly requests a short PDF despite the standing no-PDF clause. No DCF or stage-4 recommendation.

| Input | Value | Basis |
|---|---:|---|
| Closing share price (Oslo) | NOK 447.5 | 2026-10-30 history close; adj. close identical |
| Current common shares | 2,380 million | Statistics current share class / shares outstanding (float-identical); FY2025 filing-date count 2,500m differs (−7.4% YoY buybacks) — current count used for market cap, FY basis flagged |
| Market capitalization | NOK 1,065,410m (≈1.06T) | price × current shares; vendor rounded 1.06T |
| Market capitalization | EUR 103,318m | NOK 1,065,410m / 10.312 (ECB ref 2026-10-30) |
| FY2025 revenue | 105,828 | Vendor operating revenue; "Revenue as Reported" 106,462 (incl. other income) |
| FY2025 EBIT | 26,437 | Vendor operating income. Issuer net operating income 25,352 (issuer basis, −4.1% rel.) |
| FY2025 EBITDA | 35,311 | Vendor income-statement EBITDA = EBIT 26,437 + D&A 8,874 |
| FY2025 adjusted operating income | 27,591 | Issuer APM; not used as base, recorded for reconciliation |
| FY2025 parent/common net income | 5,043 | Vendor Net Income to Common; issuer group NI 5,058 − NCI 15 |
| FY2025 group net income | 5,058 | Issuer Q4 report and vendor earnings-from-continuing-operations |
| Closing parent common equity | 40,424 | FY2025 vendor balance sheet |
| Prior closing common equity | 42,342 | FY2024 |
| FY2025 total assets | 131,727 | Closing consolidated |
| Total debt incl. leases | 31,221 | ST 1,711 + current LTD 2,336 + current leases 1,190 + LT debt 23,763 + LT leases 2,221 |
| Cash & short-term investments | 19,333 | Cash 5,036 + ST investments 14,297 (Equinor holds a financial-investment portfolio; long-term investments 15,343 treated separately, flagged) |
| Long-term investments | 15,343 | Mostly financial investments/equity interests; value/proxy unresolved — flag, excluded from EV bridge, sensitivity shown |
| NCI | 74 | Closing book proxy; fair value unavailable |
| EV (base bridge) | NOK 1,175,791m / USD 127,382m | see EV computation note |
| FY2025 CFO | 19,971 | Issuer and vendor agree |
| FY2025 CapEx | −13,994 | Purchases of PP&E/intangibles (cash flow) |
| FY2025 common dividends paid | 4,791 | Cash flow; ordinary + extraordinary; buybacks 5,916 separate |
| FY2025 DPS / EPS (basic) | 1.50 / 1.94 USD | Declared DPS vs basic EPS |
| FY2025 pretax income / tax | 25,088 / 20,030 | Effective tax rate 79.84% (Norwegian petroleum tax regime) |
| Observed five-year beta | −0.65 | Vendor; negative → published-route rule: replace with bottom-up relevered beta, flagged |
## EV computation note (single FX convention)

ECB 2026-10-30: NOK 10.312 per EUR, USD 1.1172 per EUR ⇒ USD→NOK = 10.312/1.1172 = 9.2302.
- Debt incl. leases: 31,221 × 9.2302 = NOK 288,153m; NCI 74 → 683m; cash & ST investments 19,333 → 178,455m
- EV (NOK) = 1,065,410 + 288,153 + 683 − 178,455 = **NOK 1,175,791m** (= USD 127,382m); long-term investments 15,343 excluded and flagged (composition not verified).
- Vendor EV 1.12T NOK is ~5% lower: its "Cash & Cash Equivalents 230.12B NOK" (≈USD24.9bn) is broader than our cash & ST investments (USD19.3bn) — the ~USD5.6bn difference sits in the investments lines. Recorded, not mixed.

## Conflicts and cautions

- Issuer net operating income 25,352 vs vendor EBIT 26,437 differ 4.3% (>2% rule): vendor EBIT excludes "other income" items (gain on sale of assets 465 vs writedowns −2,481 netted differently). Vendor income-statement series kept uniform across all peers; issuer basis disclosed, not overwritten.
- Vendor "Revenue" 105,828 vs "Revenue as Reported" 106,462 (0.6%): other income line; reported figure is issuer-consistent.
- Negative 5Y beta (−0.65): stockanalysis beta for EQNR is implausible (negative); per published route it is replaced by the bottom-up relevered beta and flagged. EUROPE equations unaffected (beta enters PE/PBV only).
- FY2025 effective tax 79.84%: Norwegian offshore tax regime (special petroleum tax); tax_rate input 0.7984 is far above peer European rates — dispersion flagged for the EV/EBITDA equation.
- Shares: current 2,380m vs FY2025 basic weighted 2,593m reflect the 2025–26 buy-back; per-share valuation uses current count, EPS-history comparisons note the difference.
- Norway Aaa/CRP 0 confirmed from registered ctryprem dataset (topup_EQNR.OL.json); no NOK discount rate needed for relative stage.

## Source lines (reduced step)

- StockAnalysis EQNR (OSL) statistics, shares/cap/beta/tax: https://stockanalysis.com/quote/osl/EQNR/statistics/ (accessed 2026-11-01)
- StockAnalysis historical close 2026-10-30 (NOK 447.5): https://stockanalysis.com/quote/osl/EQNR/history/ (accessed 2026-11-01)
- StockAnalysis income statement FY2025/FY2024, EBITDA bridge, tax: https://stockanalysis.com/quote/osl/EQNR/financials/income-statement/ (accessed 2026-11-01)
- StockAnalysis balance sheet FY2025: https://stockanalysis.com/quote/osl/EQNR/financials/balance-sheet/ (accessed 2026-11-01)
- StockAnalysis cash flow FY2025: https://stockanalysis.com/quote/osl/EQNR/financials/cash-flow-statement/ (accessed 2026-11-01)
- Equinor Q4/FY2025 report (SEC 6-K): group NI 5,058, basic EPS 1.94, CFO 19,971, net operating income 25,352, adjusted operating income 27,591: https://www.sec.gov/Archives/edgar/data/1140625/000114062526000003/0001140625-26-000003.txt (published 2026-02-04, accessed 2026-11-01)
- Equinor Q4 2025 press release: https://www.equinor.com/news/equinor-fourth-quarter-and-full-year-2025-results (accessed 2026-11-01)
- ECB euro reference rates 2026-10-30: NOK 10.312, USD 1.1172 per EUR (cache/macro/2026-10-30.json)
