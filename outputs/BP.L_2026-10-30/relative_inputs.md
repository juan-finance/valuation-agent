# BP.L — reduced relative-only input step

Valuation / information cutoff: 2026-10-30. Accessed 2026-11-01. BP p.l.c., London ordinary shares, bucket F; USD reporting, GBP trading (screen quotes GBX; divide by 100). FY2025 = 2025-01-01 through 2025-12-31. No DCF, stage 2, stage 4, data pack or recommendation.

## Uniform StockAnalysis extract

All financial amounts below USD millions; shares millions. Immutable vendor tables and exact URLs in relative/fetch_manifest.json; normalized target in relative/candidate_raw.csv. All multiples calculated, not copied from TTM statistics.

| Input | Value | Basis |
|---|---:|---|
| Closing quote | 627.4 GBX = 6.274 GBP | 2026-10-30 history |
| Current common shares | 15,450 | Vendor rounded; not FY weighted average |
| Price x current shares | GBP 96,933.3m | Vendor cap GBP96,960m; difference -0.0275%, within 2% |
| FY revenue | 187,637 | Uniform vendor revenue excluding some production taxes |
| FY EBIT | 14,446 | Vendor standardized operating income; not issuer reported PBIT |
| FY EBITDA | 30,168 | Vendor EBIT + EBITDA D&A 15,722; not cash-flow D&A |
| FY common NI | 54 | Parent NI 55 less preference dividend 1 |
| FY closing common equity | 53,031 | Vendor common-equity perimeter; hybrid inspection required |
| FY prior common equity | 59,225 | Average equity for peer ROE |
| Debt including leases | 72,529 | FY2025; debt/lease decomposition in balance sheet |
| Cash | 36,556 | FY2025 cash and equivalents, not cash plus investments |
| NCI | 20,948 | FY2025; hybrid/preferred scope requires reconciliation |
| Associates | not available | Long-term investments are not an associates substitute |
| Decommissioning provision | 12,253 | Issuer FY2025 Note 29; separate claim sensitivity, no double deduction |
| CFO / cash capex | 24,493 / 13,221 | FY2025, reported CFO is not DACF or FCFF |
| Common dividends paid | 5,058 | FY2025; payout 93.6667x; never clipped except retention |
| Observed beta | -0.25 | Vendor 5Y, requires approved bottom-up replacement |
| Replacement beta | 0.582381561 | Resolved Europe integrated oil/gas cash-corrected beta .41, dataset marginal tax 24.71%, FY debt / current market equity; library replace_beta |
| Analyst EPS/revenue growth | 12.99% / 2.45% | Vendor 3Y horizon; file asks 5Y, horizon mismatch disclosed |
| Effective tax | 83.2816938% | FY expense 6,451 / pretax 7,746; not marginal tax |

ECB snapshot USD1.1172 and GBP0.8338 per EUR, 2026-10-30. Fundamental growth = positive average-common-equity ROE x (1-min(payout,1)) = 0; actual payout retained. No PEG growth scaling for BP.

## Issuer cross-check and unresolved definitions

Opened FY2025 issuer 20-F income statement: revenue 189,335; PBIT12,642; D&A17,822; parent profit55, tax6,451, pretax7,746. Vendor revenue differs -0.90% (production-tax presentation); parent NI agrees; common NI54 removes preference dividend. Vendor EBIT is 14.27% above issuer PBIT: standardized operating perimeter excludes unusual/nonoperating items and is not a reported IFRS EBIT. Do not silently replace only BP's uniform vendor fields. Raw as-reported and normalized parallels must be separated; source differences prevent an unqualified EV headline without reconciliation. FY net impairments/losses6,037 exceed 10% of issuer PBIT: material normalization sensitivity needed. No invented midcycle earnings.

Issuer September 2026 voting-rights filing reports 15,705.667m non-treasury ordinary shares; vendor15,450m is 1.63% lower (inside 2% tolerance, date differs). Current vendor shares retained consistently for price and per-share calculations, with uncertainty disclosed. Ordinary share ISIN GB0007980591 requires exchange/issuer identity evidence in stage3; ADS is six ordinary shares, never mixed into London price.

Stage0 exception: added only UK and GBP, no universe/candidate rebuild. GBP official latest observation through cutoff is Oct28, not Oct30; see cache manifest. Existing Spot_check pending status inherited.

## Sources (one log row per source)
- Uniform vendor: https://stockanalysis.com/quote/lon/BP/financials/income-statement/ ; https://stockanalysis.com/quote/lon/BP/financials/balance-sheet/ ; https://stockanalysis.com/quote/lon/BP/financials/cash-flow-statement/ ; https://stockanalysis.com/quote/lon/BP/statistics/ ; https://stockanalysis.com/quote/lon/BP/history/
- Issuer FY income: https://www.sec.gov/Archives/edgar/data/313807/000031380726000006/R2.htm
- Issuer decommissioning: https://www.sec.gov/Archives/edgar/data/313807/000031380726000006/R29.htm
- Issuer share perimeter: https://www.sec.gov/Archives/edgar/data/313807/000165495426008723/0001654954-26-008723.txt
- Resolved beta_europe_2026-01; ctryprem_global_2026-07; cache/macro/2026-10-30.json; dated market MANIFEST.

Academic analysis only; not personal investment advice. This is an input checkpoint, not a valuation conclusion.
