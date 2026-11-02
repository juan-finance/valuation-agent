# Prysmian S.p.A. (PRY.MI) - relative valuation, 2026-10-30

Status: provisional - limitations disclosed. QA block C executed once; no FAIL items. Human Spot_check PENDING.

## 1. Valuation summary

| Item | Value |
|---|---|
| Currency / current price | EUR 110.40 |
| Primary multiple (peers) | P/E: median 30.98x (growth/fundamental-scaled); raw median 26.98x; n = 10 |
| Peer value per share: p25 / median / p75 | 111.52 / 134.61 / 178.60 |
| Peer median vs current price | +21.9% |
| Published regression (chosen) | PBV (published R2 0.423): EUR 85.78 |
| Regression vs current price | -22.3% |
| Peer set | 10 peers; Tier 1-2: 10; Tier 3: 0 |

## 2. Peer set and multiples

| # | Ticker | Company | Country | Tier | Mkt cap EURm | P/E | P/BV | EV/EBIT | EV/ EBITDA | Distance |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | VWS | Vestas | Denmark | 2 | 24,772 | 31.84 | 6.41 | 22.28 | 15.84 | 0.56 |
| 2 | ABBN | ABB | Switzerland | 1 | 138,830 | 32.76 | 9.64 | 27.15 | 24.03 | 0.83 |
| 3 | IMI | IMI | United Kingdom | 2 | 8,179 | 22.01 | 6.15 | 16.72 | 13.77 | 0.93 |
| 4 | NEX | Nexans | France | 1 | 5,190 | 14.74 | 2.60 | 11.88 | 8.41 | 0.93 |
| 5 | ALFA | Alfa Laval | Sweden | 2 | 20,542 | 27.26 | 5.20 | 20.32 | 16.96 | 1.03 |
| 6 | NDX1 | Nordex | Germany | 2 | 8,920 | 32.50 | 6.99 | 13.58 | 11.50 | 1.10 |
| 7 | HLMA | Halma | United Kingdom | 2 | 15,615 | 43.93 | 6.86 | 31.98 | 25.55 | 1.20 |
| 8 | G1A | GEA Group | Germany | 2 | 11,050 | 26.69 | 4.50 | 18.14 | 14.04 | 1.21 |
| 9 | WRT1V | Wartsila | Finland | 2 | 15,120 | 24.15 | 5.26 | 16.47 | 14.29 | 1.23 |
| 10 | NKT | NKT | Denmark | 1 | 6,000 | 21.82 | 2.74 | 8.71 | 7.41 | 1.27 |

## 3. Peer-multiple statistics and implied value per share

| Multiple | Basis | n | Median | p25 | p75 | Value p25 | Value mid | Value p75 | Mid vs price |
|---|---|---|---|---|---|---|---|---|---|
| P/E * | scaled | 10 | 30.98x | 25.66x | 41.10x | 111.52 | 134.61 | 178.60 | +21.9% |
| P/BV | scaled | 10 | 5.86x | 4.83x | 6.60x | 107.05 | 129.76 | 146.26 | +17.5% |
| P/S | raw | 10 | 2.10x | 1.41x | 3.17x | 95.10 | 141.77 | 213.96 | +28.4% |
| EV/EBIT | raw | 10 | 17.43x | 14.30x | 21.79x | 63.25 | 79.65 | 102.50 | -27.9% |
| EV/EBITDA | raw | 10 | 14.17x | 12.07x | 16.68x | 70.06 | 84.27 | 101.30 | -23.7% |
| EV/Sales | raw | 10 | 1.95x | 1.30x | 3.40x | 76.19 | 120.32 | 217.91 | +9.0% |

* primary multiple. 'scaled' = growth/fundamental-adjusted multiple; value columns are per share in EUR.

## 4. Published regressions (Damodaran, EUROPE, 2026-01)

| Model | Predicted | Actual | Published R2 | Implied value | vs price |
|---|---|---|---|---|---|
| PE | 22.88x | 25.41x | 0.201 | 99.43 | -9.9% |
| PBV (chosen) | 3.87x | 4.98x | 0.423 | 85.78 | -22.3% |
| EV/EBITDA | 24.74x | 18.03x | 0.262 | 155.87 | +41.2% |

## 5. Company-specific notes

- Primary and range:** P/E is primary per sector_adjustments.md (growth-adjusted median 30.98x, EUR 134.61; IQR EUR 111.52-178.60). EV/EBIT (median 17.43x, EUR 79.65; IQR EUR 63.25-102.50) and EV/EBITDA (median 14.17x, EUR 84.27; IQR EUR 70.06-101.30) are the more comparable cross-check for a levered target. Envelope EUR 63.25-178.60, wide by design; no averaging with the regressions.
- P/E vs EV divergence:** the growth-adjusted P/E sits well above the EV-based values, and both differences push that way: Prysmian carries net debt/EBITDA of 1.62x versus a peer median of 0.16x (net-cash peers such as Wartsila, Nordex and Vestas lower equity value relative to EV), and its effective tax rate of 21.6% versus 26.3% (n = 4 peers) lifts net income relative to operating earnings. P/E stays primary per sector_adjustments.md; the EV multiples are the cleaner like-for-like check.
- Chosen regression below peers:** published P/BV (R2 0.423) implies EUR 85.78, P/E regression EUR 99.43, EV/EBITDA regression EUR 155.87 (low R2 0.262). Published equations are market-wide, about ten months older than the valuation date, with no standard error: a gap to price is not proof of mispricing.
- Sensitivities above 15%:** EV/EBITDA regression with the percent-point units reading of DFR and tax gives EUR 128.18 (-17.8%); raw P/E median without growth scaling -12.9%; adjusted P/E p25 -17.2% and p75 +32.7%. Peer leave-one-out moves stay within +/-2.8%. Tier-1 second peer set (ABBN, ENR, SU, LR, NKT, NEX plus the four lowest-distance remaining candidates): adjusted P/E median unchanged at EUR 134.61 (n=10), EV/EBIT EUR 100.50 (n=8, +26.2%), EV/EBITDA EUR 108.13 (n=8, +28.3%) versus the base rules-based set, which stays the base case.
- Inputs not verified against filings:** StockAnalysis figures for FY2025 (accessed 2026-11-01), no annual-report reconciliation of market cap (internal check 0.0%), associates not collected (pre-associate EV bridge: debt + NCI - cash), growth substituted by fundamental ROE x retention (labelled substituted_input).
- Peer data limits:** peer ISINs pass the check digit but are not verified on the exchange register; Vestas has two cached ISINs with issuer pages unreadable (DK0061539921 kept, DK0010268606 unresolved). Ownership and event evidence per peer is in relative/evidence_review.md.

## 6. Method notes and limitations

- Basis: one uniform vendor data source for the target and every peer, FY2025 figures (no TTM or forward mixing), one price and FX date. Issuer-versus-vendor differences are kept as sensitivities, not switched row by row.
- EV bridge: one rule for target and all peers (debt including leases + minorities and hybrids once - cash; long-term investments and associates not subtracted, equity income left in earnings).
- Peers: ten names chosen by an eight-dimension similarity score; they pass the automated hard filters and carry one ownership/event source line each (evidence_review.md). Full two-way ownership history of the whole candidate pool was not certified.
- Industry ratios from the registered Damodaran files are aggregates, not medians; they are a plausibility check only.
- Published regressions are market-wide, low R-squared, about ten months older than the valuation date, with no standard error: a gap to the market price is not proof of mispricing. The model shown is the one with the highest published R-squared.
- Peer interquartile ranges are dispersion, not confidence intervals. Human Spot_check is PENDING (not performed).
- Academic analysis only; not investment advice.
