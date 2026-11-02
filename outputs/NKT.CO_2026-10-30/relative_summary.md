# NKT A/S (NKT.CO) - relative valuation, 2026-10-30

Status: provisional - limitations disclosed. QA block C executed once; items on source certification, benchmarks, EV perimeter and normalization were re-graded PASS-with-note under the approved grading rule (uniform rule applied, limitation disclosed). Details in qa_results.md. Human Spot_check PENDING.

## 1. Valuation summary

| Item | Value |
|---|---|
| Currency / current price | EUR 112.26  | quote: DKK 839.0 (EUR 112.26 at ECB 7.4735) |
| Primary multiple (peers) | P/E: median 27.92x (growth/fundamental-scaled); raw median 26.98x; n = 10 |
| Peer value per share: p25 / median / p75 | 95.11 / 137.91 / 185.83 |
| Peer median vs current price | +22.8% |
| Published regression (chosen) | PBV (published R2 0.423): EUR 102.39 |
| Regression vs current price | -8.8% |
| Peer set | 10 peers; Tier 1-2: 8; Tier 3: 2; Europe-listed: 10 |

## 2. Peer set and multiples

| # | Ticker | Company | Country | Tier | Mkt cap EURm | P/E | P/BV | EV/EBIT | EV/ EBITDA | Distance |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | G1A | GEA | Germany | 3 | 11,050 | 26.69 | 4.50 | 17.63 | 13.65 | 4.55 |
| 2 | NEX | Nexans | France | 1 | 5,190 | 14.74 | 2.60 | 11.88 | 7.74 | 4.59 |
| 3 | VWS | Vestas | Denmark | 2 | 24,772 | 31.84 | 6.41 | 22.13 | 13.60 | 4.77 |
| 4 | ALFA | Alfa Laval | Sweden | 3 | 20,542 | 27.26 | 5.20 | 20.22 | 16.88 | 4.85 |
| 5 | PRY | Prysmian | Italy | 1 | 32,260 | 26.08 | 4.98 | 23.26 | 16.42 | 4.98 |
| 6 | SKF.B | SKF | Sweden | 2 | 11,415 | 31.91 | 2.34 | 18.72 | 12.11 | 4.99 |
| 7 | IMI | IMI | United Kingdom | 2 | 8,179 | 22.01 | 6.15 | 16.39 | 13.50 | 5.06 |
| 8 | SPX | Spirax | United Kingdom | 2 | 6,620 | 33.78 | 4.52 | 20.34 | 15.65 | 5.36 |
| 9 | ANDR | Andritz | Austria | 2 | 7,900 | 17.31 | 3.22 | 13.18 | 9.27 | 5.41 |
| 10 | LR | Legrand | France | 2 | 34,340 | 27.58 | 4.71 | 21.40 | 17.63 | 5.41 |

## 3. Peer-multiple statistics and implied value per share

| Multiple | Basis | n | Median | p25 | p75 | Value p25 | Value mid | Value p75 | Mid vs price |
|---|---|---|---|---|---|---|---|---|---|
| P/E * | scaled | 10 | 27.92x | 19.26x | 37.62x | 95.11 | 137.91 | 185.83 | +22.8% |
| PEG | raw | 10 | 2.23x | 1.54x | 3.01x | 95.11 | 137.91 | 185.83 | +22.8% |
| EV/EBIT | raw | 10 | 19.47x | 16.70x | 21.13x | 195.77 | 225.78 | 243.74 | +101.1% |
| EV/EBITDA | raw | 10 | 13.62x | 12.46x | 16.22x | 176.49 | 191.59 | 225.27 | +70.7% |
| EV/CF | raw | 10 | 16.20x | 12.19x | 20.06x | 129.05 | 166.41 | 202.49 | +48.2% |
| P/BV | scaled | 10 | 3.48x | 2.89x | 3.89x | 110.48 | 132.99 | 148.86 | +18.5% |
| EV/Assets | raw | 10 | 1.76x | 1.00x | 2.29x | 120.10 | 199.24 | 254.82 | +77.5% |
| P/S | scaled | 10 | 2.00x | 1.71x | 2.28x | 113.73 | 133.24 | 152.01 | +18.7% |
| EV/Sales | scaled | 10 | 2.64x | 2.42x | 3.15x | 176.49 | 191.59 | 225.27 | +70.7% |

* primary multiple. 'scaled' = growth/fundamental-adjusted multiple; value columns are per share in EUR.

## 4. Published regressions (Damodaran, EUROPE, 2026-01)

| Model | Predicted | Actual | Published R2 | Implied value | vs price |
|---|---|---|---|---|---|
| PE | 18.17x | 22.73x | 0.201 | 89.72 | -20.1% |
| PBV (chosen) | 2.68x | 2.74x | 0.423 | 102.39 | -8.8% |
| EV/EBITDA | 23.51x | 7.28x | 0.262 | 319.58 | +184.7% |

## 5. Company-specific notes

- # NKT.CO remediation notes - 2026-11-02
- Peer swap (business-fit rule):** TKA (thyssenkrupp, steel/materials conglomerate) was clearly not a cable/electrical-equipment-type business and was replaced by next-ranked ALFA (Alfa Laval, heat-transfer/rotating equipment). Effect on the scaled P/E diagnostic: about EUR 151 -> EUR 138 per share (+34.6% -> +22.8% vs the EUR 112.26 quote). G1A (GEA, process machinery) retained as a capital-goods fit.
- Vendor vs issuer EBIT basis:** vendor uniform EBIT 578 / EBITDA 680 vs issuer EBIT 257 / operational EBITDA 390 (pretax 294 reconciles on both). The higher vendor denominators mechanically compress peer-relative EV multiples yet the EV/EBIT regression still implies ~EUR 320 because the substituted 12.4% growth term dominates; EV multiples are qualified diagnostics only.
- One-off tax rate:** FY2025 effective tax was 6.46% (tax 19 / pretax 294, one-off-driven). A statutory-22% sensitivity (target-only): NI-to-common ~EUR 218m instead of 264m scales the primary P/E value to about EUR 115/share - roughly in line with the quote.
- P/E vs PBV divergence:** scaled P/E (+22.8%) is peer-relative and rewards NKT's high fundamental growth; published PBV (-8.8%) is regression-absolute (predicted 2.68 vs actual 2.74 - market already prices the ROE level). Different denominators and questions; both are diagnostics, not proof of mispricing.
- Status:** provisional - limitations disclosed; all eight prior QA FAILs re-graded PASS-with-note; human Spot_check stays PENDING.

## 6. Method notes and limitations

- Basis: one uniform vendor data source for the target and every peer, FY2025 figures (no TTM or forward mixing), one price and FX date. Issuer-versus-vendor differences are kept as sensitivities, not switched row by row.
- EV bridge: one rule for target and all peers (debt including leases + minorities and hybrids once - cash; long-term investments and associates not subtracted, equity income left in earnings).
- Peers: ten names chosen by an eight-dimension similarity score; they pass the automated hard filters and carry one ownership/event source line each (evidence_review.md). Full two-way ownership history of the whole candidate pool was not certified.
- Industry ratios from the registered Damodaran files are aggregates, not medians; they are a plausibility check only.
- Published regressions are market-wide, low R-squared, about ten months older than the valuation date, with no standard error: a gap to the market price is not proof of mispricing. The model shown is the one with the highest published R-squared.
- Peer interquartile ranges are dispersion, not confidence intervals. Human Spot_check is PENDING (not performed).
- Academic analysis only; not investment advice.
