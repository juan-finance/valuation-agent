# Neste Oyj (NESTE.HE): reduced relative-only inputs

Valuation date: 2026-10-30. Accessed: 2026-11-01. Primary listing Nasdaq Helsinki (HEL:NESTE), quoted and reporting in EUR millions. Fiscal year = calendar year; FY2025 = 2025-01-01–2025-12-31; no calendarization or TTM/FY mixing. Finland/EUR present in the dated cache after the NESTE.HE top-up (Finland Aa1, spread 0.22%, CRP 0.34%); no stage-0 rebuild. Standard / published_damodaran / web_minimum / relative_only. User explicitly requests a short PDF despite the standing no-PDF clause. No DCF or stage-4 recommendation.

| Input | Value | Basis |
|---|---:|---|
| Closing share price (Helsinki) | EUR 28.34 | 2026-10-30 history close; adj. close identical |
| Current common shares | 768.28 million | Statistics shares outstanding; FY2025 filing-date count 768.27m (no share-class split; treasury −4m already netted) |
| Market capitalization | EUR 21,772m | price × current shares; vendor rounded 21.77B |
| FY2025 revenue | 19,016 | Vendor operating revenue = issuer reported revenue (exact) |
| FY2025 EBIT | 466 | Vendor operating income. Issuer operating profit 503 (issuer basis, +7.9% rel. gap: vendor excludes other income 125, equity-investment result 7, FX/fair-value −125 netted differently) |
| FY2025 EBITDA | 1,124 | Vendor income-statement EBITDA = EBIT 466 + D&A-for-EBITDA 658 |
| FY2025 issuer reported EBITDA | 1,438 | Issuer financial statements release; comparable EBITDA 1,683 (excl. inventory valuation −69, derivative fair-value changes +25, other adjustments) — not the vendor basis, sensitivity kept |
| FY2025 net income | 144 | Vendor = issuer net profit (exact); no NCI in earnings |
| Closing parent common equity | 7,314 | FY2025 vendor = issuer total equity (exact; no minority interest) |
| Prior closing common equity | 7,417 | FY2024 |
| FY2025 total assets | 15,749 | Closing consolidated |
| Total debt incl. leases | 5,183 | Current LTD 265 + current leases 205 + LT debt 3,973 + LT leases 740 (ST debt 0) |
| Cash & short-term investments | 1,367 | Cash & equivalents only (no ST investments) |
| Long-term investments | 90 | Small; excluded from EV bridge, flagged |
| NCI | 0 | No minority interest on balance sheet |
| EV (base bridge) | EUR 25,586m | 21,772 + 5,183 + 0 − 1,367; vendor EV 24.55B is ~4% lower (different debt/cash perimeter; recorded, not mixed) |
| FY2025 CFO | 1,747 | Issuer and vendor agree |
| FY2025 CapEx | −910 | Vendor capital expenditures; issuer "cash-out investments" 939 (incl. intangibles 12 and other) |
| FY2025 common dividends paid | 154 | Cash flow; issuer-proposed 0.20/share ≈ 154 total (matches) |
| FY2025 DPS / EPS (basic) | 0.20 / 0.19 EUR | Declared DPS vs basic EPS |
| FY2025 pretax income / tax | 199 / 55 | Effective tax rate 27.64% |
| Observed five-year beta | 0.56 | Vendor; plausible, kept |

## EV computation note

All-EUR chain, no FX conversion needed (reports and trades EUR). ECB reference for peer conversions from cache/macro/2026-10-30.json.
- EV (EUR) = 21,772 + 5,183 + 0 − 1,367 = **EUR 25,586m**; LT investments 90 excluded and flagged (composition not material).
- Vendor EV 24.55B differs ~4.1%: vendor debt/cash perimeter not identical (likely excludes some lease/debt lines). Recorded, not mixed.

## Conflicts and cautions

- Issuer operating profit 503 vs vendor EBIT 466 differ 7.9% (>2% rule): vendor EBIT excludes other income (125), equity investments (7) and FX/fair-value lines (−125) netted differently. Vendor uniform basis kept; issuer basis disclosed.
- EBITDA basis is the biggest divergence: vendor 1,124 vs issuer reported 1,438 vs issuer comparable 1,683 (−21.8% / −33.2% rel.): issuer EBITDA includes other income/associates/derivative effects vendor excludes; comparable EBITDA strips inventory valuation and derivative noise. Vendor uniform basis used for peer consistency; EBITDA sensitivities mandatory (primary multiple is EV/EBITDA).
- Payout >1 (declared 154 / NI 144 = 1.069): retention capped at 0 → fundamental growth ≈ 0.19%×0 ≈ 0. This collapses the growth dimension and the g_eps/g_rev substituted inputs; flagged.
- FY2025 ROE only 1.96% (144/avg(7,314,7,417)) — cyclical trough; flagged for PBV equation and peer scoring.
- No NCI, no preferreds, no hybrids; LT investments 90 immaterial. Associates/JVs: share of profit 7 (in EBIT? issuer shows inside operating profit area) — associates excluded from EV bridge, flagged.
- Finland Aa1/CRP 0.34% added via top-up (topup_NESTE.HE.json); EUR risk-free already cached; stage 3 does not discount.

## Source lines (reduced step)

- StockAnalysis NESTE (HEL) statistics, shares/cap/beta/tax: https://stockanalysis.com/quote/hel/NESTE/statistics/ (accessed 2026-11-01; from dated cache)
- StockAnalysis historical close 2026-10-30 (EUR 28.34): https://stockanalysis.com/quote/hel/NESTE/history/ (accessed 2026-11-01; from dated cache)
- StockAnalysis income statement FY2025/FY2024, EBITDA bridge, tax: https://stockanalysis.com/quote/hel/NESTE/financials/income-statement/ (accessed 2026-11-01; from dated cache)
- StockAnalysis balance sheet FY2025: https://stockanalysis.com/quote/hel/NESTE/financials/balance-sheet/ (accessed 2026-11-01; from dated cache)
- StockAnalysis cash flow FY2025: https://stockanalysis.com/quote/hel/NESTE/financials/cash-flow-statement/ (accessed 2026-11-01; from dated cache)
- Neste Financial Statements Release 2025 (published 2026-02-05, accessed 2026-11-01): revenue 19,016; EBITDA 1,438; comparable EBITDA 1,683; operating profit 503; profit before taxes 199; net profit 144; EPS 0.19; equity 7,314; CFO 1,747; leverage 34.3%; dividend proposal 0.20/share ≈ 154: https://www.neste.com/news/nestes-financial-statements-release-2025 and https://www.neste.com/files/pdf/7218DC4287D4BDD7-Neste%20Financial%20Statements%20Release%202025.pdf
- ECB euro reference rates 2026-10-30 (cache/macro/2026-10-30.json); Finland top-up cache/market/2026-10-30/topup_NESTE.HE.json
