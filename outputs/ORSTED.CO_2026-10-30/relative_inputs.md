# Ørsted A/S (ORSTED.CO): reduced relative-only inputs

Valuation date: 2026-10-30. Accessed: 2026-11-02. Primary listing Nasdaq Copenhagen (CPH:ORSTED), quoted in DKK; reports in DKK millions. Fiscal year = calendar year; FY2025 = 2025-01-01–2025-12-31; no calendarization or TTM/FY mixing. Denmark already in the dated cache (NKT.CO top-up: Denmark Aaa, spread 0, CRP 0); DKK FX cached (7.4735 DKK/EUR, ECB 2026-10-30); EUROPE published equations already resolved — no stage-0 rebuild or top-up needed. Standard / published_damodaran / web_minimum / relative_only. User explicitly requests a short PDF despite the standing no-PDF clause. No DCF or stage-4 recommendation.

| Input | Value | Basis |
|---|---:|---|
| Closing share price (Copenhagen) | DKK 131.9 | 2026-10-30 history close; adj. close identical |
| Current common shares | 1,321.06 million | Issuer AR: 1,321,062k outstanding at 2025-12-31 (rights issue Oct 2025, 420,381k + 900,681k new); vendor 1,320m consistent |
| Market capitalization | DKK 174,250m ≈ EUR 23,316m | price × current shares = 174,108; vendor rounded 174.25B (−0.08% gap) |
| FY2025 revenue | 73,244 | Vendor = issuer reported revenue (exact) |
| FY2025 EBITDA | 21,583 | Vendor income-statement EBITDA |
| FY2025 issuer reported EBITDA | 22,448 | Issuer AR; 25,065 excl. new partnerships (−1,255) and cancellation fees (−1,362). Vendor −3.9% vs reported — basis gap recorded, sensitivity kept |
| FY2025 EBIT | 12,495 | Vendor operating income = EBITDA 21,583 − D&A-for-EBITDA 9,088 |
| FY2025 issuer EBIT | 8,620 | Issuer AR: EBITDA 22,448 − D&A 10,195 − impairment 3,633. Vendor excludes impairment below EBIT → +45% gap; pretax basis reconciles (see tax) |
| FY2025 profit for the year | 3,165 | Issuer AR (group, incl. NCI and hybrid coupon effects) |
| FY2025 net income to common | 1,727 | Vendor; after NCI share and equity-classified hybrid coupons. Vendor = issuer-consistent common basis, kept |
| Closing parent common equity | 119,718 | Issuer AR "Shareholders in Ørsted A/S"; group equity 148,941 = shareholders 119,718 + hybrid capital 20,955 + NCI 8,268. Vendor "Total Common Equity" 140,673 includes the hybrid (flagged; common basis = 119,718) |
| Prior closing parent common equity | 62,138 | FY2024 issuer (shareholders' share); group 93,484 |
| FY2025 total assets | 367,922 | Closing consolidated (vendor) |
| Total debt incl. leases | 107,857 | Vendor total debt; issuer NIBD 18,978 is a net figure after the rights-issue cash and other interest-bearing assets — perimeter differs (recorded, not mixed) |
| Cash & equivalents | 53,448 | Vendor cash & equivalents (includes part of the Oct-2025 rights-issue proceeds) |
| Long-term investments | 669 | Small; excluded from EV bridge, flagged |
| NCI | 8,268 | Vendor = issuer non-controlling interests (exact) |
| Hybrid capital | 20,955 | Issuer AR equity line; equity-classified claim deducted once in the EV→common-equity bridge (sector_adjustments.md: no automatic 50% rule) |
| Issuer net interest-bearing debt | 18,978 | Issuer AR (post-rights-issue cash position); vendor-derived net debt 54,409 differs — different claim/asset perimeter, recorded not mixed |
| EV (base bridge) | DKK 236,927m | 174,250 + 107,857 + 8,268 − 53,448; before associates |
| FY2025 CFO | 23,741 | Vendor operating cash flow (issuer free cash flow −18,850 after gross investments −54,976 and divestments +12,385) |
| FY2025 CapEx | −54,776 | Vendor capital expenditures ≈ issuer gross investments 54,976 (−0.4%); very high vs peers (offshore build-out) |
| FY2025 common dividends paid | 0 | Issuer: no ordinary dividend for FY2025 (reinstate from FY2026). Vendor CF "dividends paid" 713 ≈ dividends to NCI; "dividends and hybrid coupons paid" 2,643. Common payout = 0 (vendor 0.41 rejected as common-basis) |
| FY2025 pretax income / tax | 5,988 / 2,823 | Issuer AR; effective tax rate 47% (impairment/non-deductible driven; vendor 0.4714 identical) |
| Observed five-year beta | 0.58 | Vendor; plausible, kept |
| Consensus growth | g_eps 51.15%, g_rev 8.84% | Vendor statistics 3Y forecasts (EPS rebound off impaired FY2025 base — flagged) |

## EV computation note

Reporting and trading currency both DKK; EUR conversion at ECB 2026-10-30 reference 7.4735 DKK/EUR (cache/macro/2026-10-30.json) for pool comparability only.
- EV (DKK) = 174,250 + 107,857 + 8,268 − 53,448 = **DKK 236,927m**; LT investments 669 excluded (immaterial); hybrid 20,955 is an equity-classified claim deducted once in the EV→common-equity bridge.
- Vendor uniform EV basis kept for peer consistency; issuer NIBD 18,978 implies a materially different claim perimeter (rights-issue cash parked) — recorded, not mixed.

## Conflicts and cautions

- EBIT/EBITDA basis: vendor EBITDA 21,583 vs issuer 22,448 reported / 25,065 excl. partnerships+cancellation fees; vendor EBIT 12,495 excludes the 3,633 impairment (issuer EBIT 8,620). Vendor uniform basis kept; EV/EBIT and EV/EBITDA issuer-basis sensitivities mandatory.
- Hybrid capital DKK 20,955m equity-classified (three securities): inside vendor "common equity" 140,673 but not common — common book equity = 119,718; hybrid deducted once in the EV→equity bridge; NI-to-common already reflects hybrid coupons.
- Common payout = 0 for FY2025 (issuer: dividends reinstated from FY2026); vendor's 41.3% "payout" counts NCI/hybrid distributions — rejected for common-basis uses (regression payout input and scaled adjustments).
- Tax rate 47% effective (impairment/non-deductible driven) — flagged for regression tax_rate input and peer comparability.
- g_eps 51.15% analyst consensus is a rebound estimate off the impairment-depressed FY2025 base — flagged as low-comparability growth input.
- Rights issue Oct 2025 (DKK 59.4bn net proceeds) roughly tripled share count to 1,321.1m and left large parked cash — capital structure at the valuation date is transitional (leverage restored later); flagged for scoring and regression DFR.
- No calendarization needed (Dec year-end). Denmark Aaa/CRP 0 already cached; stage 3 does not discount.

## Source lines (reduced step)

- StockAnalysis ORSTED (CPH) statistics, shares/cap/beta/tax/growth: https://stockanalysis.com/quote/cph/ORSTED/statistics/ (accessed 2026-11-01)
- StockAnalysis historical close 2026-10-30 (DKK 131.9): https://stockanalysis.com/quote/cph/ORSTED/history/ (accessed 2026-11-01)
- StockAnalysis income statement FY2025/FY2024: https://stockanalysis.com/quote/cph/ORSTED/financials/income-statement/ (accessed 2026-11-01)
- StockAnalysis balance sheet FY2025: https://stockanalysis.com/quote/cph/ORSTED/financials/balance-sheet/ (accessed 2026-11-01)
- StockAnalysis cash flow FY2025: https://stockanalysis.com/quote/cph/ORSTED/financials/cash-flow-statement/ (accessed 2026-11-01)
- Ørsted A/S Annual Report 2025 (accessed 2026-11-02): revenue 73,244; EBITDA 22,448 (25,065 excl. partnerships/cancellation); D&A 10,195; impairment 3,633; EBIT 8,620; pretax 5,988; tax 2,823 (47%); profit 3,165; equity 148,941 = shareholders 119,718 + hybrid 20,955 + NCI 8,268; NIBD 18,978; shares 1,321,062k; gross investments 54,976; dividends & hybrid coupons paid 2,643; no FY2025 common dividend: https://cdn.orsted.com/-/media/annual-2025/annual-report-2025.pdf
- ECB euro reference rates 2026-10-30 (cache/macro/2026-10-30.json); Denmark coverage via cache/market/2026-10-30/topup_NKT.CO.json
