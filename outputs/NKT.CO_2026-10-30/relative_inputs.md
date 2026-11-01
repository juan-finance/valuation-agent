# NKT A/S (NKT.CO): reduced relative-only inputs

Valuation date: 2026-10-30. Accessed: 2026-11-01. Primary listing Nasdaq Copenhagen (CPH:NKT), quoted in DKK; reports in EUR millions. Fiscal year = calendar year; FY2025 = 2025-01-01–2025-12-31; no calendarization or TTM/FY mixing. Denmark added to the dated cache via the NKT.CO top-up (Denmark Aaa, spread 0, CRP 0); DKK FX already cached (7.4735 DKK/EUR, ECB 2026-10-30); no stage-0 rebuild. Standard / published_damodaran / web_minimum / relative_only. User explicitly requests a short PDF despite the standing no-PDF clause. No DCF or stage-4 recommendation.

| Input | Value | Basis |
|---|---:|---|
| Closing share price (Copenhagen) | DKK 839.0 | 2026-10-30 history close; adj. close identical; = EUR 112.26 at ECB 7.4735 |
| Current common shares | 53.45 million | Statistics shares outstanding; FY2025 filing-date count 53.45m; treasury −20 already netted in equity |
| Market capitalization | DKK 44,844m = EUR 6,001m | price × current shares; vendor rounded 44.84B |
| FY2025 revenue | 3,565 | Vendor = issuer reported revenue (exact); issuer also reports revenue at standard metal prices 2,722 (+6% organic) |
| FY2025 EBIT | 578 | Vendor operating income. Issuer EBIT 257 (−55.5% rel. gap): vendor classifies −272 "other non-operating" (incl. metal-price/hedge and project items) below EBIT; pretax 294 matches issuer EBT exactly |
| FY2025 EBITDA | 680 | Vendor income-statement EBITDA = EBIT 578 + D&A-for-EBITDA 102 |
| FY2025 issuer reported EBITDA | 390 | Issuer annual report: operational EBITDA 390, one-off items 0; D&A & impairment −133 → EBIT 257 — not the vendor basis, sensitivity kept |
| FY2025 net income | 275 | Vendor = issuer net result continuing operations (exact; discontinued 0 in FY2025) |
| FY2025 net income to common | 264 | Vendor; after hybrid coupon 11 (EUR 150m 7.24% hybrid, issued Sep 2022, first call 1 Jul 2026; refinanced Mar 2026 by a new EUR 150m 5.00% hybrid) |
| Closing parent common equity | 2,043 | Issuer group equity 2,193 − EUR 150m equity-classified hybrid claim (vendor reports total common equity 2,193 including the hybrid component; flagged) |
| Prior closing group equity | 1,853 | FY2024 (hybrid 150 likewise inside; common basis ≈ 1,703) |
| FY2025 total assets | 5,595 | Closing consolidated (vendor = issuer exact) |
| Total debt incl. leases | 251 | Current LTD 7 + current leases 15 + LT debt 125 + LT leases 104; issuer NIBD −963 net cash reconciles (1,214 − 251 = +963) |
| Cash & equivalents | 1,214 | Cash & ST investments (vendor = issuer cash position inside NIBD −963) |
| Long-term investments | 10 | Small; excluded from EV bridge, flagged |
| NCI | 0 | No minority interest disclosed |
| EV (base bridge) | EUR 5,038m | 6,001 + 251 + 0 − 1,214; hybrid EUR 150m is an additional equity-classified claim (subtract once in the implied-common-equity bridge). Vendor EV 40.43B DKK ≈ EUR 5,411m (~7% higher; different claim perimeter — recorded, not mixed) |
| FY2025 CFO | 499 | Vendor = issuer cash flow from operating activities (exact) |
| FY2025 CapEx | −695 | Vendor capital expenditures = issuer PP&E investments (exact) |
| FY2025 common dividends paid | 11 | Vendor cash flow; payout ratio observed 6.86% vendor stat; dividends/NI-to-common = 4.2% |
| FY2025 pretax income / tax | 294 / 19 | Effective tax rate 6.46% (issuer: reported tax rate 6%) |
| Observed five-year beta | 0.65 | Vendor; plausible, kept |

## EV computation note

Reporting currency EUR; trading currency DKK. Market cap converted at ECB 2026-10-30 reference 7.4735 DKK/EUR (cache/macro/2026-10-30.json). No other FX needed.
- EV (EUR) = 6,001 + 251 + 0 − 1,214 = **EUR 5,038m**; LT investments 10 excluded (immaterial); hybrid EUR 150m is an equity-classified claim deducted once in the EV→common-equity bridge (no automatic 50% rule per sector_adjustments.md).
- Vendor EV ≈ EUR 5,411m differs ~7%: different claim perimeter (likely hybrid and/or other claims). Recorded, not mixed.

## Conflicts and cautions

- EBIT/EBITDA basis is the biggest divergence: vendor EBIT 578 / EBITDA 680 vs issuer EBIT 257 / operational EBITDA 390 (−55.5% / −42.6% rel.): vendor routes −272 of metal-price, hedge and other items below EBIT that the issuer includes above EBIT; pretax 294 matches exactly. Vendor uniform basis kept for peer consistency; issuer basis disclosed; EV/EBIT and EV/EBITDA sensitivities mandatory (they are the ordered cross-checks for the PE primary).
- Hybrid capital: EUR 150m 7.24% (2022, call 1 Jul 2026) + EUR 150m 5.00% (Mar 2026). Equity-classified; coupon 11 in FY2025 strips NI to common 264; common book equity ≈ 2,043. At valuation date both instruments may coexist (2026 issue refinanced the 2022 call) — flagged; bridge uses the FY2025-consistent 150.
- No NCI, no preferreds beyond the hybrid; treasury shares −20 already netted in equity.
- Low effective tax rate 6.46% (issuer: reported tax 6%, one-off-driven) — flagged for regression tax_rate input and peer comparability.
- Order backlog EUR 10,200m disclosed (vendor table) — context for growth; not an input.
- Denmark Aaa/CRP 0 added via top-up (topup_NKT.CO.json); DKK FX already cached; stage 3 does not discount.

## Source lines (reduced step)

- StockAnalysis NKT (CPH) statistics, shares/cap/beta/tax: https://stockanalysis.com/quote/cph/NKT/statistics/ (accessed 2026-11-01)
- StockAnalysis historical close 2026-10-30 (DKK 839.0): https://stockanalysis.com/quote/cph/NKT/history/ (accessed 2026-11-01)
- StockAnalysis income statement FY2025/FY2024, EBITDA bridge, tax: https://stockanalysis.com/quote/cph/NKT/financials/income-statement/ (accessed 2026-11-01)
- StockAnalysis balance sheet FY2025: https://stockanalysis.com/quote/cph/NKT/financials/balance-sheet/ (accessed 2026-11-01)
- StockAnalysis cash flow FY2025: https://stockanalysis.com/quote/cph/NKT/financials/cash-flow-statement/ (accessed 2026-11-01)
- NKT A/S Annual Report 2025 (published 2026-02-25, accessed 2026-11-01): revenue 3,565; operational EBITDA 390; EBIT 257; EBT 294; net result 275; equity 2,193; NIBD −963; CFO 499; PP&E investments −695; reported tax 6%: https://investors.nkt.com/financial-reports/nkt-as-annual-report-2025-6-organic-growth-and-record-high-operational-ebitda/ and https://investors.nkt.com/files/Main/23044/4312549/nkt-annual-report-2025.pdf
- NKT hybrid securities 2022 (EUR 150m, 7.24%, ISIN DK0030510995) and 2026 (EUR 150m, 5.00%): https://investors.nkt.com/bond-investors/hybrid-securities-2022/ and https://investors.nkt.com/bond-investors/hybrid-securities-2026/ (accessed 2026-11-01)
- ECB euro reference rates 2026-10-30 (cache/macro/2026-10-30.json); Denmark top-up cache/market/2026-10-30/topup_NKT.CO.json
