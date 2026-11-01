# ENGI.PA — reduced input step (relative_only deviation)

Valuation date: 2026-10-30. Earnings basis: FY2025 (Dec year-end, IFRS). Reporting = trading currency: EUR. No full stage 1 (no data_pack.xlsx, no anomaly report); one line per source in source_log.csv.

## Identity
- ENGIE SA, Euronext Paris, ISIN FR0010208488. Sector: Utilities / integrated utility — networks (grids), renewables & BESS (57.2 GW installed), gas generation, energy supply; Belgian nuclear moved to JV with Belgian State in 2025 (bucket A). Single share class.
- Shares outstanding: 2,432m (vendor statistics "Shares Outstanding 2.43B"; balance-sheet table "Total Common Shares Outstanding 2,432m" FY2025 filing date). Treasury ~30m shares excluded already (2,435m issued).
- Price 2026-10-30 close: EUR 23.43 (stockanalysis history, Euronext Paris). Market cap = 23.43 x 2,432m = EUR ~56.98bn (vendor snapshot 56.98B — exact).
- Corporate events relevant to peer rules: UK Power Networks acquisition (announced FY2025, pending) — target-side event, not a peer disqualifier. Belgian nuclear JV (Tihange 3/Doel 4) affects comparability of Engie's own FY2025 figures, flagged. No listed subsidiary and no >20% cross-holding known within the candidate pool; ownership audit pending (provisional flag).
- FY2025 dividend: EUR 1.35/share proposed (issuer; 67% payout of NRIgs €4.9bn) ≈ EUR ~3,283m.

## FY2025 figures (EUR millions)

| Field | stockanalysis FY2025 | ENGIE FY2025 results (issuer) | Note |
|---|---|---|---|
| Revenue | 71,944 | Revenues 71.9bn | near-exact |
| EBITDA | 13,012 | EBITDA 14,700; EBITDA ex-nuclear 13,400 | vendor scope narrower (excludes items issuer aggregates incl. nuclear contribution); issuer-basis sensitivity retained |
| EBIT (operating income) | 8,339 | EBIT 9,471; EBIT ex-nuclear 8,757 | same scope caveat |
| D&A | 5,151 (CF) / 4,673 (IS "D&A for EBITDA") | – | |
| Net income to common | 3,687 | Net income Group share 3,827; NRIgs 4,900 | vendor "Net Income" 3,827 = issuer NIGs exact; "to Common" deducts further €140m (hybrid/perpetual coupons — Engie has hybrids; flagged, kept for peer comparability); NI to company 4,748 incl. NCI share ~921 |
| Pretax income | 6,318 | – | tax expense 1,570 -> effective 24.85% |
| Total common equity | 32,951 | – | parent basis |
| Minority interest (NCI) | 7,879 | – | |
| Total debt | 55,187 (gross) | Net financial debt 38,900; net economic debt 45,200 | gross vs net basis; both recorded; issuer economic debt incl. pensions/provisions |
| Cash & equivalents | 14,507 | – | |
| Associates / long-term investments | 13,210 | – | proxy for equity-accounted holdings (large for Engie) |
| CFO | -1,476 | CFFO 13,600 | vendor FY2025 CFO negative — Belgian nuclear cash-out and working-capital swings; flagged, EV/CF unusable for target |
| CapEx | 7,267 | – | |
| Dividends paid | 4,529 (CF FY2025 outflow) | FY2025 dividend proposed EUR ~3,283m (1.35/sh, 67% of NRIgs) | paid-cash basis includes prior-year balance timing |
| Beta (5Y) | 0.57 | – | vendor observed; index/frequency unverified |
| Analyst growth | EPS 4.73% (3Y), Revenue 5.60% (3Y) | 2026-28 NRIgs guidance €4.6-5.2bn (2026) | consensus used for published-route inputs |
| Effective tax rate | 24.85% (IS table) | – | FY basis |

## Regression (published route) inputs derived
- roe (closing book) = 3,687 / 32,951 = 0.1119; average-equity alt = 0.1092
- payout = declared dividend 3,283 / NI to common 3,687 = 0.89 reported basis (issuer-stated 67% of NRIgs 4.9bn ≈ 3,283 consistent; paid-cash basis 4,529/3,687 = 1.23 flagged). fundamental growth = ROE x (1 - min(payout,1)) = 0.0123
- dfr = 55,187 / (55,187 + 56,982) = 0.4920
- tax_rate = 0.2485 effective FY2025
- roic = 8,339 x (1 - 0.2485) / (32,951 + 55,187 - 14,507) = 0.0851
- g_eps = 0.0473 consensus; g_rev = 0.0560 consensus (no fundamental substitution needed)

## Sources (one line each)
- S1: https://stockanalysis.com/quote/epa/ENGI/financials/ + balance-sheet + cash-flow-statement + statistics + history (accessed 2026-11-01 via dated cache EDPRpool_ENGI_*, valuation-date cache) — uniform vendor extract.
- S2: https://www.engie.com/app/uploads/2026/03/PR-ENGIE-FY-2025-VDEF.pdf (accessed 2026-11-01) — issuer FY2025 press release: revenue, EBITDA/EBIT (incl. ex-nuclear), NIGs/NRIgs, net financial/economic debt, dividend, UKPN acquisition, Belgian nuclear JV.
- S3: universe row cache/market/2026-10-30/universe.csv (IEUR proxy membership).
- S4: cache/macro/2026-10-30.json — ECB FX and macro snapshot (EUR = base, no conversion needed).
