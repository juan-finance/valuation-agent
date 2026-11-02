# Verbund AG (VER.VI): reduced relative-only inputs

Valuation date: 2026-10-30. Accessed: 2026-11-02. Primary listing Vienna Stock Exchange (VIE:VER), quoted in EUR; consolidated reporting in EUR millions. Fiscal year = calendar year; FY2025 = 2025-01-01–2025-12-31; no calendarization or TTM/FY mixing (vendor statistics carries TTM fields — kept separate and unused). Austria was the only missing country in the dated cache: stage-0 top-up `cache/market/2026-10-30/topup_ver.py` added Austria Aa1 / spread 0.22% / CRP 0.34% from registered ctryprem_global_2026-07 (topup_VER.VI.json); EUR risk-free and ECB FX already present. Standard / published_damodaran / web_minimum / relative_only. User explicitly requests a short PDF despite the standing no-PDF clause. No DCF or stage-4 recommendation.

| Input | Value | Basis |
|---|---:|---|
| Closing share price (Vienna) | EUR 69.50 | 2026-10-30 history close; adj. close identical |
| Current common shares | 347.42 million | Vendor shares outstanding = filing-date count = issuer share capital 347,415,686 no-par shares; Republic of Austria holds 51% (free float ~49%) |
| Market capitalization | EUR 24,145.7m | price × current shares = 24,145.7; vendor 24.15B (−0.02% gap) |
| FY2025 revenue | 8,033 | Vendor income statement; issuer reported revenue 8,013.6 (+0.24% gap, recorded) |
| FY2025 EBIT | 2,108 | Vendor operating income; issuer EBIT 2,112.3 (−0.2%) |
| FY2025 EBITDA | 2,715 | Vendor income-statement EBITDA = EBIT 2,108 + D&A-for-EBITDA 606.89; issuer EBITDA 2,737.5 (−0.8%, recorded) |
| FY2025 net income (group result) | 1,489 | Vendor = issuer Group result 1,489.4 exactly; issuer adjusted Group result 1,472.1 (APM, disclosed not used) |
| Closing parent common equity | 10,341 | Vendor Total Common Equity; issuer equity 11,331.2 = common 10,341 + NCI 990 (reconciles) |
| Prior closing parent common equity | 9,978 | FY2024 vendor (issuer equity FY2024 11,064.8 incl. NCI 1,087) |
| FY2025 total assets | 18,610 | Closing consolidated = issuer 18,609.7 |
| Total debt incl. leases | 2,460 | Vendor total debt (current LTD 494.6 + current leases 15.9 + LT debt 1,729 + LT leases 220.5); issuer net debt 2,818.1 is a net figure — different perimeter, recorded not mixed |
| Cash & equivalents | 72.79 | Vendor cash & equivalents; + ST investments 1.1 |
| Long-term investments | 1,419 | Includes equity investments; earnings on equity investments 92.6 inside EBIT/EBITDA — excluded from EV bridge, flagged |
| NCI | 990.29 | Vendor = issuer non-controlling interests (~990 inside equity 11,331.2) |
| EV (base bridge) | EUR 27,522m | see EV computation note; vendor quote-side EV 28.20B differs (broader cash/other perimeter — recorded, not mixed) |
| FY2025 CFO | 1,919 | Vendor = issuer cash flow from operating activities 1,918.5 |
| FY2025 CapEx | −1,368 | Vendor capital expenditures; issuer additions to PP&E 1,298.1 (cash vs additions basis) |
| FY2025 common dividends paid | −1,329 | Vendor cash flow (incl. special dividend 0.80; DPS FY2025 2.00, proposed incl. special) |
| FY2025 pretax income / tax | 2,116 / 422.65 | Effective tax rate 19.97%; includes Austrian windfall-profit levy expenses €135.9m |
| FY2025 EPS (basic/diluted) | 4.29 / 4.29 EUR | Vendor; 347m weighted |
| Observed five-year beta | 0.14 | Vendor statistics; positive, below 2.5 → used as observed, flagged atypically low |
| Consensus growth (3Y) | g_eps −4.51%, g_rev −0.98% | Vendor statistics analyst forecasts; negative growth → PEG/scaled-PE safeguards apply |

## EV computation note (EUR throughout; no conversion needed)

- EV (EUR) = 24,145.7 + 2,460 + 990.29 − 72.79 − 1.1 = **EUR 27,522m**; long-term investments 1,419 excluded and flagged (equity-investment earnings 92.6 remain in EBIT/EBITDA denominators — recorded limitation).
- Issuer net debt 2,818.1 vs vendor-derived net debt 2,460 − 73.89 = 2,386: issuer nets other interest-bearing assets/receivables not in the vendor cash line — recorded, not mixed; vendor series kept uniform across peers.
- Vendor quote-side EV 28.20B is ~2.5% higher: broader cash/investment perimeter — recorded, not mixed.

## Conflicts and cautions

- Vendor revenue 8,033 vs issuer 8,013.6 (+0.24%): within 2%, vendor uniform basis kept.
- EBITDA/EBIT basis: vendor EBITDA 2,715 vs issuer 2,737.5 (−0.8%); vendor EBIT 2,108 vs issuer 2,112.3 (−0.2%) — small; sensitivities on issuer basis still shown.
- Austrian windfall-profit tax expense €135.9m inside FY2025 cost base depresses EBITDA — sector-specific one-off, flagged for peer comparability.
- Consensus g_eps −4.51% is a normalization forecast off the high-price FY2023–24 base; PEG unusable (negative driver) and growth-scaled PE adjustments invalid — recorded as unavailable, not repaired.
- Beta 0.14 (5Y) is atypically low for a utility; used as observed per published-route rule, flagged.
- Austria Aa1/spread 0.22%/CRP 0.34% added by the VER.VI stage-0 top-up; EUR Bund 3.38% already cached; stage 3 does not discount.

## Source lines (reduced step)

- StockAnalysis VER (VIE) statistics, shares/cap/beta/tax/growth: https://stockanalysis.com/quote/vie/VER/statistics/ (accessed 2026-11-02; TTM fields unused)
- StockAnalysis historical close 2026-10-30 (EUR 69.50): https://stockanalysis.com/quote/vie/VER/history/ (accessed 2026-11-02)
- StockAnalysis income statement FY2025/FY2024, EBITDA bridge, tax: https://stockanalysis.com/quote/vie/VER/financials/income-statement/ (accessed 2026-11-02)
- StockAnalysis balance sheet FY2025: https://stockanalysis.com/quote/vie/VER/financials/balance-sheet/ (accessed 2026-11-02)
- StockAnalysis cash flow FY2025: https://stockanalysis.com/quote/vie/VER/financials/cash-flow-statement/ (accessed 2026-11-02)
- VERBUND integrated annual financial report 2025 (accessed 2026-11-02): revenue 8,013.6; EBITDA 2,737.5; EBIT 2,112.3; Group result 1,489.4 (adjusted 1,472.1); equity 11,331.2; net debt 2,818.1; CFO 1,918.5; PP&E additions 1,298.1; windfall tax expense 135.9; hydro coefficient 0.79: https://www.verbund.com/media/hq2nhfvp/verbund-annual-financial-report-2025-englisch.pdf and press release https://www.verbund.com/en/group/news-press/press-releases/2026/3/18/annual-result-2025
- ECB euro reference rates 2026-10-30 and macro snapshot (cache/macro/2026-10-30.json); Austria coverage via cache/market/2026-10-30/topup_VER.VI.json
