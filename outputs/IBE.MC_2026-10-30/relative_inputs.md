# IBE.MC — reduced input step (relative_only deviation)

Valuation date: 2026-10-30. Earnings basis: FY2025 (Dec year-end, IFRS). Reporting = trading currency: EUR. No full stage 1 (no data_pack.xlsx, no anomaly report); one line per source in source_log.csv.

## Identity
- Iberdrola S.A., Bolsa de Madrid (BME:IBE), ISIN ES0144580Y14. Sector: Utilities / integrated utility — regulated networks (Spain/UK/US/Brazil), renewables generation, retail (bucket A). Single share class.
- Shares outstanding: 6,670m (vendor statistics "Current Share Class/Shares Outstanding 6.67B"; issuer: 6,681,227,377 shares at 31.12.2025 — 0.2% gap, consistent after treasury).
- Price 2026-10-30 close: EUR 22.18 (stockanalysis history, BME). Market cap = 22.18 × 6,670m = EUR ~147.9bn (vendor snapshot 147.94B; implied 147,941m within 0.01%).
- Listed subsidiaries relevant to peer rules: Avangrid (US, ~81.6% owned) and Neoenergia (Brazil, ~83.8% owned) — neither is a candidate in the pool; flag only. Endesa (ELE.MC) is ~70% owned by ENEL, a candidate — hard-excluded from the pool.
- FY2025 dividend: EUR 0.68/share DPS (vendor; +6.25% YoY). Iberdrola runs a scrip dividend ("Iberdrola Retribución Flexible") — CF dividends paid 1,275m understates declared; issuance of common stock 5,107m reflects scrip take-up.

## FY2025 figures (EUR millions)

| Field | stockanalysis FY2025 | Iberdrola FY2025 (issuer, CNMV filing) | Note |
|---|---|---|---|
| Revenue | 44,076 | Revenues 45,546.8 | −3.2% gap: issuer line includes other operating income; both recorded, vendor kept uniform |
| EBITDA | 14,700 | Reported EBITDA 16,592.4; adjusted EBITDA 15,684 | vendor excludes ~1.9bn of items issuer includes; reported-basis sensitivity retained |
| EBIT (operating income) | 9,979 | EBIT 10,276.4 | −2.9% gap, flagged |
| D&A | 5,279 (IS) / 4,917 (CF) / 4,721 (D&A for EBITDA) | – | multiple vendor bases recorded |
| Net income to common | 6,055 | Reported net profit 6,285.0 | vendor group NI 6,285 matches issuer exactly; vendor deducts 230 "Preferred Dividends & Other Adjustments" = perpetual subordinated-note (hybrid) coupon — real claim, kept; adjusted NI excl. pipeline charges 6,749 |
| Pretax income / tax | 8,097 / 1,671 | – | effective tax 20.64% (vendor IS); statistics TTM 20.43% — FY basis used |
| Total common equity | 50,068 | Equity 63,419 incl. NCI; NCI 13,351 -> parent 50,068 | exact match |
| Minority interest (NCI) | 13,351 | – | Avangrid/Neoenergia minorities |
| Total debt | 59,407 (gross, incl. leases 5,095) | Net financial debt 51,755; adjusted 50,182 | gross incl. leases vs issuer net basis; both recorded |
| Cash & equivalents | 3,670 | – | |
| Associates / long-term investments | 2,488 | – | proxy for equity-accounted holdings |
| Total assets | 160,762 | 160,762 | exact match |
| CFO | 11,635 | – | |
| CapEx | 8,081 | Gross organic investments 12,563; total investments 14.46bn | issuer basis broader (incl. network investment via associates etc.); vendor CF basis kept |
| Dividends paid (CF) | 1,275 | – | scrip-dividend effect, flagged |
| Beta (5Y) | 0.45 | – | vendor observed; index/frequency unverified |
| Analyst growth | EPS 9.15% (3Y), Revenue 4.05% (3Y) | – | consensus, used for published-route inputs |
| Issuer ROE | – | 12.46% | issuer definition; vendor-derived closing ROE 12.09% |
| Ratings | – | Moody's Baa1 / S&P BBB+ / Fitch BBB+ | from issuer results document |

## Regression (published route) inputs derived
- roe (closing book) = 6,055 / 50,068 = 0.1209 (avg-equity scoring basis 0.1246)
- payout = declared dividend (0.68 × 6,681m = 4,543) / NI to common 6,055 = 0.7504; CF paid basis 1,275/6,055 = 0.21 not used (scrip); vendor payout ratio 72.64% consistent
- dfr = 59,407 / (59,407 + 147,941) = 0.2865
- tax_rate = 0.2064 effective FY2025
- roic = 9,979 × (1 − 0.2064) / (50,068 + 59,407 − 3,670) = 0.0748
- g_eps = 0.0915 consensus; g_rev = 0.0405 consensus (no fundamental substitution needed)
- fundamental scoring growth = 0.1246 × (1 − 0.7504) = 0.0311

## Sources (one line each)
- S1: https://stockanalysis.com/quote/bme/IBE/financials/ + balance-sheet + cash-flow-statement + statistics + history (accessed 2026-11-01, reused EDPR-run dated cache extract EDPRpool_IBE_*) — uniform vendor extract.
- S2: Iberdrola FY2025 results (CNMV filing, "FY 2025 Results", published 2026-02-25): revenues 45,546.8, EBITDA 16,592.4, EBIT 10,276.4, net profit 6,285.0, equity 63,419, net financial debt 51,755, EPS 0.925, ROE 12.46%, ratings: https://www.cnmv.es/webservices/verdocumento/ver?t=%7Bb287d05d-73ce-42dc-87c2-dc6436ec35b4%7D (accessed 2026-11-01)
- S3: Iberdrola press release "Investments of €14.46 billion drive 12% growth in reported Net Profit" (2026-02-25): adjusted EBITDA 15.68bn, adjusted net profit 6,749m, scrip-dividend context: https://www.iberdrola.com/press-room/news/detail/investments-of-14-46-billion-drive-12-percent-growth-in-reported-net-profit (accessed 2026-11-01)
- S4: universe row cache/market/2026-10-30/universe.csv (IEUR proxy membership).
- S5: cache/macro/2026-10-30.json — ECB FX and macro snapshot (EUR = base, no conversion needed).
