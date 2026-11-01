# ENEL.MI — reduced input step (relative_only deviation)

Valuation date: 2026-10-30. Earnings basis: FY2025 (Dec year-end, IFRS). Reporting = trading currency: EUR. No full stage 1 (no data_pack.xlsx, no anomaly report); one line per source in source_log.csv.

## Identity
- Enel S.p.A., Borsa Italiana (Euronext Milan), ISIN IT0003128367. Sector: Utilities / integrated utility — generation, networks (grids), retail; large renewables fleet via Enel Green Power (bucket A). Single share class.
- Shares outstanding: 9,920m (vendor statistics "Current Share Class/Shares Outstanding 9.92B"; issuer: ~10,166m shares issued less ~188m treasury as of Mar-2026 and ~133.6m at the Jan-2026 record date — consistent).
- Price 2026-10-30 close: EUR 9.32 (stockanalysis history, Borsa Italiana). Market cap = 9.32 x 9,920m = EUR ~92.5bn (vendor snapshot 92.46B; implied 92,454m within 0.01%).
- Listed/controlled subsidiaries relevant to peer rules: Endesa (ELE.MC, ~70% owned) -> hard-excluded from the ENEL peer set (subsidiary of target); Enel Americas/Enel Chile also controlled (not in candidate pool).
- FY2025 dividend: EUR 0.49/share total (interim 0.23 paid Jan-2026; balance 0.26 paid Jul-2026) ≈ EUR 4,982m proposed total.

## FY2025 figures (EUR millions)

| Field | stockanalysis FY2025 | Enel FY2025 results (issuer) | Note |
|---|---|---|---|
| Revenue | 79,394 (as reported: 80,346) | Revenues 80,346 | vendor "Revenue" excludes minor revenue lines; as-reported row matches issuer exactly |
| EBITDA | 20,311 | Ordinary EBITDA 22,874; reported EBITDA 22,073 (FY25 presentation) | vendor excludes ~2.6bn of non-operating/other items issuer includes in ordinary EBITDA; reported-basis sensitivity retained |
| EBIT (operating income) | 14,252 | – | reported base |
| D&A | 6,577 (CF) / 6,059 (IS "D&A for EBITDA") | – | |
| Net income to common | 3,959 | Group net income 4,225 (= vendor "Net Income" row, exact); ordinary 7,011 | vendor deducts a further 266 "Preferred Dividends & Other" (no Enel preferred exists — flagged, kept for peer comparability); issuer group NI used in sensitivity |
| Pretax income | 8,390 | – | tax expense 2,773 -> effective 33.05% |
| Total common equity | 32,068 | Equity incl. NCI 46,805; NCI 14,737 -> parent equity 32,068 | exact match |
| Minority interest (NCI) | 14,737 | 14,737 | exact match |
| Total debt | 69,011 (gross, incl. leases 2,847) | Net financial debt 57,182 (excl. 382 held-for-sale) | gross vs net basis; both recorded |
| Cash & equivalents | 5,065 | – | |
| Associates / long-term investments | 3,000 | – | proxy for equity-accounted holdings |
| CFO | 13,926 | – | |
| CapEx | 8,506 | – | |
| Dividends paid | 6,060 (CF FY2025 outflow) | FY2025 dividend declared EUR 4,982m (0.49/sh) | CF outflow includes timing of prior-year balance; declared basis used for payout |
| Beta (5Y) | 0.84 | – | vendor observed; index/frequency unverified |
| Analyst growth | EPS 7.63% (3Y), Revenue 3.17% (3Y) | Strategic plan EPS ~0.72-0.74 (2026), 0.80-0.82 (2028) | consensus, used for published-route inputs; plan CAGR ~6% EPS consistent |
| Effective tax rate | 33.05% (IS table) / 31.65% (statistics TTM) | – | FY basis 33.05% recorded with flag |

## Regression (published route) inputs derived
- roe (closing book) = 3,959 / 32,068 = 0.1235; alternative on issuer group NI 4,225 / 32,068 = 0.1318
- payout = declared dividend 4,982 / NI to common 3,959 = 1.26 reported basis (4,982 / group NI 4,225 = 1.18; / ordinary NI 7,011 = 0.71). CF paid basis 6,060 / 3,959 = 1.53. >1 payout retained as observed; growth = ROE x (1 - payout capped at 1) = 0 -> fundamental growth unavailable -> published-route uses analyst consensus g_eps per approval.
- dfr = 69,011 / (69,011 + 92,454) = 0.4274
- tax_rate = 0.3305 effective FY2025
- roic = 14,252 x (1 - 0.3305) / (32,068 + 69,011 - 5,065) = 0.0993
- g_eps = 0.0763 consensus; g_rev = 0.0317 consensus (no fundamental substitution needed)

## Sources (one line each)
- S1: https://stockanalysis.com/quote/bit/ENEL/financials/ + balance-sheet + cash-flow-statement + statistics + history (accessed 2026-11-01, cached under EDPR run fetch, manifest EDPRpool_ENEL_*) — uniform vendor extract.
- S2: https://www.enel.com/content/dam/enel-common/press/en/2026-march/Enel%20results%20FY2025.pdf (accessed 2026-11-01) — issuer FY2025 press release: revenues, ordinary/reported EBITDA, group net income, net financial debt, dividend, treasury shares.
- S3: universe row cache/market/2026-10-30/universe.csv (IEUR proxy membership).
- S4: cache/macro/2026-10-30.json — ECB FX and macro snapshot (EUR = base, no conversion needed).
