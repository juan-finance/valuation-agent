# Siemens Energy AG (ENR.DE) - relative valuation, 2026-10-30

Status: provisional - limitations disclosed - limitations disclosed. QA block C executed once; items on source certification, benchmarks, EV perimeter and normalization were re-graded PASS-with-note under the approved grading rule (uniform rule applied, limitation disclosed). Details in qa_results.md. Human Spot_check PENDING.

## 1. Valuation summary

| Item | Value |
|---|---|
| Currency / current price | EUR 126.92 |
| Primary multiple (peers) | EV/EBIT: median 21.01x; raw median 21.01x; n = 10 |
| Peer value per share: p25 / median / p75 | 42.87 / 44.18 / 46.12 |
| Peer median vs current price | -65.2% |
| Published regression (chosen) | PBV (published R2 0.423): EUR 35.94 |
| Regression vs current price | -71.7% |
| Peer set | 10 peers; Tier 1-2: 7; Tier 3: 3; Europe-listed: 9 |

## 2. Peer set and multiples

| # | Ticker | Company | Country | Tier | Mkt cap EURm | P/E | P/BV | EV/EBIT | EV/ EBITDA | Distance |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | WRT1V | Wartsila | Finland | 1 | 15,120 | 24.15 | 5.26 | 16.36 | 14.97 | 2.03 |
| 2 | VWS | Vestas | Denmark | 1 | 24,772 | 31.84 | 6.41 | 22.28 | 15.84 | 2.18 |
| 3 | SAND | Sandvik | Sweden | 3 | 41,009 | 30.65 | 4.83 | 23.40 | 18.46 | 2.28 |
| 4 | ETN | Eaton | United States | 2 | 128,625 | 35.16 | 7.40 | 29.00 | 24.37 | 2.34 |
| 5 | SU | Schneider Electric | France | 2 | 133,720 | 32.12 | 5.53 | 21.42 | 18.83 | 2.41 |
| 6 | G1A | GEA | Germany | 3 | 11,050 | 26.69 | 4.50 | 17.64 | 15.05 | 2.65 |
| 7 | LR | Legrand | France | 2 | 34,340 | 27.58 | 4.71 | 21.40 | 18.42 | 2.67 |
| 8 | METSO | Metso | Finland | 3 | 13,890 | 32.84 | 5.22 | 20.62 | 17.46 | 2.69 |
| 9 | ALFA | Alfa Laval | Sweden | 2 | 20,542 | 27.26 | 5.20 | 20.28 | 17.64 | 2.80 |
| 10 | SPX | Spirax | United Kingdom | 2 | 6,620 | 33.78 | 4.52 | 20.34 | 16.43 | 3.00 |

## 3. Peer-multiple statistics and implied value per share

| Multiple | Basis | n | Median | p25 | p75 | Value p25 | Value mid | Value p75 | Mid vs price |
|---|---|---|---|---|---|---|---|---|---|
| EV/EBIT * | raw | 10 | 21.01x | 20.30x | 22.07x | 42.87 | 44.18 | 46.12 | -65.2% |
| P/E * | scaled | 10 | 43.23x | 36.63x | 62.95x | 60.56 | 71.47 | 104.07 | -43.7% |
| PEG | raw | 10 | 2.96x | 2.51x | 4.31x | 60.56 | 71.47 | 104.07 | -43.7% |
| EV/EBITDA | raw | 10 | 17.55x | 15.99x | 18.45x | 55.73 | 60.61 | 63.44 | -52.2% |
| EV/CF | raw | 10 | 22.60x | 15.75x | 24.98x | 112.84 | 159.41 | 175.61 | +25.6% |
| P/BV | scaled | 10 | 4.50x | 3.96x | 4.86x | 47.64 | 54.24 | 58.56 | -57.3% |
| EV/Assets | raw | 10 | 2.26x | 1.83x | 2.43x | 127.12 | 155.11 | 166.46 | +22.2% |
| P/S | scaled | 10 | 1.13x | 0.99x | 1.18x | 45.20 | 51.65 | 53.99 | -59.3% |
| EV/Sales | scaled | 10 | 1.20x | 1.10x | 1.27x | 55.73 | 60.61 | 63.44 | -52.2% |

* primary multiple. 'scaled' = growth/fundamental-adjusted multiple; value columns are per share in EUR.

## 4. Published regressions (Damodaran, EUROPE, 2026-01)

| Model | Predicted | Actual | Published R2 | Implied value | vs price |
|---|---|---|---|---|---|
| PE | 22.09x | 76.78x | 0.201 | 36.52 | -71.2% |
| PBV (chosen) | 2.98x | 10.54x | 0.423 | 35.94 | -71.7% |
| EV/EBITDA | 23.49x | 38.71x | 0.262 | 79.24 | -37.6% |

## 5. Company-specific notes

- ENR equipment/service turnaround: uniform pre-associate EV/EBIT primary EUR44.18 (peer IQR 42.87–46.12) alongside growth-scaled PE EUR71.47 (60.56–104.07); range EUR42.87–104.07, dispersion not confidence. PE is not fallback-only. Published PBV35.94 is separate, not averaged.
- Uniform vendor shares855.34m/cap108560m retained (price126.92 reconciliation0.00023%); issuer850m issued is a +0.628% per-share sensitivity, not an outstanding-share error. ENR FY2025 parentNI1414 differs from group1685 because NCI271.
- Vendor ENR EBIT1569 versus issuer2149 reflects580 equity-accounted income classification; vendor fields kept for every observation, no incremental equity-income strip. Issuer2149 sensitivity at fixed peer median gives EUR58.43 (+32.3%, above15%); no associates/investments deducted from EV; leases/NCI/hybrids counted once using vendor claims with0 incremental unidentified hybrids.
- ENR weak wind margin and portfolio/restructuring offset make reported earnings fragile. Mechanical all-target/all-peer EBIT margin4/6/8/10% sensitivity gives EUR167.07 (+278.2%, above15%); it is algebraic rescaling, not researched normalization or a recovery forecast. FY2025 net specials+6 mask large gross costs/gains.
- Primary peer quartiles materially move value: EV/EBIT-3.0%/+4.4%, PE-15.3%/+45.6% (both PE tails above15%; raw PE31.24x gives EUR51.65 versus scaled EUR71.47 (-27.7%, above15%); EV/EBITDA alternative EUR60.61 is +37.2% versus EV/EBIT, above15%); full multiple alternatives in table.10 peers,7 Tier1/2,3 Tier3,9 Europe: approved cap4 relaxation retained; smaller bolt-ons/restructurings noted, not automatic exclusions.
- FY2025 CFO5821 includes customer advances, not enterprise FCFF; noDCF or Stage4 recommendation. Industry aggregates Electrical Equipment18.94x EV/EBITDA and24.34x EV/EBIT are plausibility only, not medians. Registered published models use labelled fundamental growth rather than analyst forecasts; both unit policies retained. Human Spot_check remains PENDING; academic analysis only, not investment advice.

## 6. Method notes and limitations

- Basis: one uniform vendor data source for the target and every peer, FY2025 figures (no TTM or forward mixing), one price and FX date. Issuer-versus-vendor differences are kept as sensitivities, not switched row by row.
- EV bridge: one rule for target and all peers (debt including leases + minorities and hybrids once - cash; long-term investments and associates not subtracted, equity income left in earnings).
- Peers: ten names chosen by an eight-dimension similarity score; they pass the automated hard filters and carry one ownership/event source line each (evidence_review.md). Full two-way ownership history of the whole candidate pool was not certified.
- Industry ratios from the registered Damodaran files are aggregates, not medians; they are a plausibility check only.
- Published regressions are market-wide, low R-squared, about ten months older than the valuation date, with no standard error: a gap to the market price is not proof of mispricing. The model shown is the one with the highest published R-squared.
- Peer interquartile ranges are dispersion, not confidence intervals. Human Spot_check is PENDING (not performed).
- Academic analysis only; not investment advice.
