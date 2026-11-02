# Shell plc (SHEL.L) - relative valuation, 2026-10-30

Status: provisional - limitations disclosed - limitations disclosed. QA block C executed once; items on source certification, benchmarks, EV perimeter and normalization were re-graded PASS-with-note under the approved grading rule (uniform rule applied, limitation disclosed). Details in qa_results.md. Human Spot_check PENDING.

## 1. Valuation summary

| Item | Value |
|---|---|
| Currency / current price | GBP 40.37 |
| Primary multiple (peers) | EV/EBITDA: median 8.43x; raw median 8.43x; n = 10 |
| Peer value per share: p25 / median / p75 | 41.30 / 46.52 / 72.83 |
| Peer median vs current price | +15.2% |
| Published regression (chosen) | PBV (published R2 0.423): GBP 45.27 |
| Regression vs current price | +12.2% |
| Peer set | 10 peers; Tier 1-2: 10; Tier 3: 0; Europe-listed: 5 |

## 2. Peer set and multiples

| # | Ticker | Company | Country | Tier | Mkt cap EURm | P/E | P/BV | EV/EBIT | EV/ EBITDA | Distance |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | TTE | TotalEnergies | France | 1 | 188,520 | 16.04 | 1.83 | 12.44 | 7.49 | 0.36 |
| 2 | XOM | Exxon Mobil | unverified | 1 | 683,665 | 26.48 | 2.94 | 22.91 | 13.65 | 0.55 |
| 3 | COP | ConocoPhillips | unverified | 1 | 165,628 | 23.16 | 2.87 | 16.11 | 8.38 | 0.81 |
| 4 | REP | Repsol | Spain | 1 | 33,040 | 17.40 | 1.31 | 16.69 | 10.26 | 0.95 |
| 5 | EQNR | Equinor | Norway | 1 | 102,793 | 22.77 | 2.84 | 4.80 | 3.59 | 0.95 |
| 6 | VLO | Valero | unverified | 2 | 99,767 | 47.47 | 4.70 | 25.60 | 15.97 | 1.00 |
| 7 | CVX | Chevron | unverified | 1 | 411,296 | 37.36 | 2.46 | 28.68 | 13.44 | 1.08 |
| 8 | ENI | Eni | Italy | 1 | 79,080 | 30.32 | 1.65 | 19.71 | 8.48 | 1.13 |
| 9 | BP | BP | United Kingdom | 1 | 116,287 | 2,362.10 | 2.45 | 12.93 | 6.19 | 1.35 |
| 10 | EOG | EOG Resources | unverified | 1 | 77,721 | 17.44 | 2.91 | 14.26 | 7.90 | 1.46 |

## 3. Peer-multiple statistics and implied value per share

| Multiple | Basis | n | Median | p25 | p75 | Value p25 | Value mid | Value p75 | Mid vs price |
|---|---|---|---|---|---|---|---|---|---|
| P/E | scaled | 10 | 31.67x | 20.50x | 49.23x | 47.87 | 73.97 | 114.97 | +83.2% |
| PEG | raw | 7 | 5.96x | 3.86x | 9.27x | 47.87 | 73.97 | 114.97 | +83.2% |
| EV/EBIT | raw | 10 | 16.40x | 13.26x | 22.11x | 45.72 | 57.98 | 80.29 | +43.6% |
| EV/EBITDA * | raw | 10 | 8.43x | 7.59x | 12.64x | 41.30 | 46.52 | 72.83 | +15.2% |
| EV/CF | raw | 10 | 9.10x | 7.65x | 13.73x | 36.86 | 44.98 | 70.99 | +11.4% |
| P/BV | scaled | 10 | 2.53x | 1.94x | 3.38x | 44.35 | 57.75 | 77.18 | +43.1% |
| EV/Assets | raw | 10 | 1.26x | 0.77x | 1.76x | 31.49 | 55.10 | 79.05 | +36.5% |
| P/S | scaled | 10 | 1.66x | 1.25x | 2.38x | 43.84 | 57.97 | 83.15 | +43.6% |
| EV/Sales | scaled | 10 | 1.50x | 1.36x | 2.26x | 41.30 | 46.52 | 72.83 | +15.2% |

* primary multiple. 'scaled' = growth/fundamental-adjusted multiple; value columns are per share in GBP.

## 4. Published regressions (Damodaran, EUROPE, 2026-01)

| Model | Predicted | Actual | Published R2 | Implied value | vs price |
|---|---|---|---|---|---|
| PE | 17.59x | 17.29x | 0.201 | 41.09 | +1.8% |
| PBV (chosen) | 1.98x | 1.77x | 0.423 | 45.27 | +12.2% |
| EV/EBITDA | 20.16x | 7.45x | 0.262 | 119.75 | +196.7% |

## 5. Company-specific notes

- Uniform pre-associate EV/EBITDA primary: peer median 8.43x on n=10 -> GBP 46.52 mid vs GBP 40.365 quote (+15.2%), IQR GBP 41.30–72.83. One disclosed rule for target and all ten peers: debt incl. leases + NCI - cash; LT investments (SHEL 29,332) not subtracted, equity income (1,618) kept in earnings.
- Cross-method dispersion above 15%: leave-one-out peer sensitivity swings the EV/EBITDA value to GBP 58.88 (+26.6%); peer-IQR high GBP 72.83 is +56.6% over mid. Published regression PBV GBP 45.27 (+12.2%), PE GBP 41.09; the EV/EBITDA equation GBP 119.75 is a market-wide outlier kept only as a diagnostic.
- Market-wide EV/EBITDA equation predicted 20.2x versus SHEL actual 7.4x (-63%): the published equation cannot price oil majors — headline limitation, not a mispricing signal.
- Vendor-vs-issuer basis kept as sensitivities, not switched: issuer adjusted EBITDA 56,135 vs vendor 47,658 lifts the EV/EBITDA value to GBP 55.87 (+20.1%); issuer net debt 45,687 vs vendor 45,472 lowers it by -0.1%. Uniform vendor basis retained for all observations.
- Adura 50/50 JV (Shell + Equinor) completed Dec 2025 is noted on both SHEL and peer EQNR and estimated below the 25%-of-EV exclusion threshold; SHEL vendor beta -0.19 is negative — retained for scoring with flag, replaced by relevered industry beta ~0.47 in the published regression. Fundamental growth 5.37% is a substituted input, not analyst consensus.
- Status provisional - limitations disclosed: the eight prior QA FAILs re-graded PASS-with-note under qa_grading_and_remediation; human Spot_check stays PENDING. Academic analysis only, not investment advice.

## 6. Method notes and limitations

- Basis: one uniform vendor data source for the target and every peer, FY2025 figures (no TTM or forward mixing), one price and FX date. Issuer-versus-vendor differences are kept as sensitivities, not switched row by row.
- EV bridge: one rule for target and all peers (debt including leases + minorities and hybrids once - cash; long-term investments and associates not subtracted, equity income left in earnings).
- Peers: ten names chosen by an eight-dimension similarity score; they pass the automated hard filters and carry one ownership/event source line each (evidence_review.md). Full two-way ownership history of the whole candidate pool was not certified.
- Industry ratios from the registered Damodaran files are aggregates, not medians; they are a plausibility check only.
- Published regressions are market-wide, low R-squared, about ten months older than the valuation date, with no standard error: a gap to the market price is not proof of mispricing. The model shown is the one with the highest published R-squared.
- Peer interquartile ranges are dispersion, not confidence intervals. Human Spot_check is PENDING (not performed).
- Academic analysis only; not investment advice.
