# Vestas Wind Systems A/S (VWS.CO) - relative valuation, 2026-10-30

Status: provisional - limitations disclosed. QA block C executed once; open FAIL items: C4, C5, C8, C9, C11, C15, C19, C37 (see qa_results.md). Human Spot_check PENDING.

## 1. Valuation summary

| Item | Value |
|---|---|
| Currency / current price | DKK 189.25 |
| Primary multiple (peers) | EV/EBIT: median 18.96x; raw median 18.96x; n = 8 |
| Peer value per share: p25 / median / p75 | 135.86 / 162.16 / 182.41 |
| Peer median vs current price | -14.3% |
| Published regression (chosen) | PBV (published R2 0.423): DKK 125.66 |
| Regression vs current price | -33.6% |
| Peer set | 10 peers; Tier 1-2: 9; Tier 3: 1; Europe-listed: 10 |

## 2. Peer set and multiples

| # | Ticker | Company | Country | Tier | Mkt cap EURm | P/E | P/BV | EV/EBIT | EV/ EBITDA | Distance |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | NDX1 | Nordex | Germany | 1 | 8,920 | 32.50 | 6.99 | 13.58 | 11.50 | 0.76 |
| 2 | WRT1V | Wartsila | Finland | 1 | 15,120 | 24.15 | 5.26 | 16.36 | 14.97 | 1.03 |
| 3 | IMI | IMI | United Kingdom | 2 | 8,179 | 22.01 | 6.15 | n/a | n/a | 1.12 |
| 4 | G1A | GEA | Germany | 3 | 11,050 | 26.69 | 4.50 | 17.64 | 15.05 | 1.20 |
| 5 | ALFA | Alfa Laval | Sweden | 2 | 20,542 | 27.26 | 5.20 | 20.28 | 17.64 | 1.23 |
| 6 | ENR | Siemens Energy | Germany | 1 | 108,560 | 76.78 | 10.54 | 66.12 | 38.71 | 1.28 |
| 7 | NKT | NKT | Denmark | 2 | 6,000 | 21.82 | 2.74 | n/a | n/a | 1.42 |
| 8 | ANDR | Andritz | Austria | 2 | 7,900 | 17.31 | 3.22 | 13.86 | 10.44 | 1.42 |
| 9 | LR | Legrand | France | 2 | 34,340 | 27.58 | 4.71 | 21.40 | 18.42 | 1.56 |
| 10 | ROR | Rotork | United Kingdom | 2 | 4,821 | 34.84 | 6.91 | 21.58 | 20.15 | 1.66 |

## 3. Peer-multiple statistics and implied value per share

| Multiple | Basis | n | Median | p25 | p75 | Value p25 | Value mid | Value p75 | Mid vs price |
|---|---|---|---|---|---|---|---|---|---|
| P/E | scaled | 10 | 42.50x | 32.42x | 57.27x | 192.72 | 252.63 | 340.40 | +33.5% |
| PEG | raw | 10 | 2.23x | 1.70x | 3.01x | 192.72 | 252.63 | 340.40 | +33.5% |
| EV/EBIT * | raw | 8 | 18.96x | 15.73x | 21.44x | 135.86 | 162.16 | 182.41 | -14.3% |
| EV/EBITDA | raw | 8 | 16.34x | 14.11x | 18.85x | 169.37 | 195.03 | 223.76 | +3.1% |
| EV/CF | raw | 8 | 16.20x | 11.04x | 24.90x | 200.45 | 290.56 | 442.43 | +53.5% |
| P/BV | scaled | 10 | 5.61x | 4.63x | 6.03x | 136.71 | 165.71 | 178.07 | -12.4% |
| EV/Assets | raw | 8 | 1.79x | 1.44x | 2.26x | 290.33 | 359.94 | 451.15 | +90.2% |
| P/S | scaled | 10 | 1.12x | 0.93x | 1.29x | 133.99 | 160.34 | 185.87 | -15.3% |
| EV/Sales | scaled | 8 | 1.30x | 1.12x | 1.50x | 169.37 | 195.03 | 223.76 | +3.1% |

* primary multiple. 'scaled' = growth/fundamental-adjusted multiple; value columns are per share in DKK.

## 4. Published regressions (Damodaran, EUROPE, 2026-01)

| Model | Predicted | Actual | Published R2 | Implied value | vs price |
|---|---|---|---|---|---|
| PE | 29.70x | 31.84x | 0.201 | 176.53 | -6.7% |
| PBV (chosen) | 4.25x | 6.41x | 0.423 | 125.66 | -33.6% |
| EV/EBITDA | 21.69x | 15.84x | 0.262 | 256.32 | +35.4% |

## 5. Company-specific notes

- # VWS.CO remediation notes - 2026-11-02
- Primary kept:** EV/EBIT stays the primary multiple on the uniform pre-associate bridge (debt incl. leases + NCI - cash; LT investments and associates not subtracted): peer median 18.96x on 8 valid -> DKK 162.16 mid vs DKK 189.25 quote (-14.3%), IQR 135.86-182.41. IMI and NKT drop out of EV multiples (invalid denominators), n=8 >= 6.
- Share count:** kept at 978.25m current; the 999m weighted-basic average is a sensitivity only and scales every per-share value by 0.9792 (-2.1%, below the 15% flag level).
- Cross-method dispersion above 15%:** the scaled-PE diagnostic implies DKK 252.63 (+55.8% vs the EV/EBIT mid) driven by the high vendor consensus growth; the published PBV regression implies DKK 125.66 (-22.5% vs the mid). The diagnostic range used is DKK 125.66-182.41 (regression low to primary IQR high); the PE value is an upper outlier reflecting a different denominator, not a bound.
- Vendor-vs-issuer bases:** vendor EBITDA 1501 vs issuer 2053 (-26.9% definitional gap) favours EV/EBIT; issuer reported EBIT 1015 vs vendor before-special-items 1067 (special items -52 = 4.9% of EBIT, below the 10% normalization trigger) is a target-only diagnostic, not a uniform normalization.
- Peer caveat:** ENR.DE (Siemens Energy) is in the selected peer set and is itself being remediated in a separate run; its vendor figures here are unchanged and no update was waited for. Europe membership evidence is the dated IEUR MSCI Europe IMI holdings proxy; URTH was required only for the unused non-European World expansion.
- Status:** provisional - limitations disclosed; the eight prior QA FAILs re-graded PASS-with-note under qa_grading_and_remediation; human Spot_check stays PENDING.

## 6. Method notes and limitations

- Basis: one uniform vendor data source for the target and every peer, FY2025 figures (no TTM or forward mixing), one price and FX date. Issuer-versus-vendor differences are kept as sensitivities, not switched row by row.
- EV bridge: one rule for target and all peers (debt including leases + minorities and hybrids once - cash; long-term investments and associates not subtracted, equity income left in earnings).
- Peers: ten names chosen by an eight-dimension similarity score; they pass the automated hard filters and carry one ownership/event source line each (evidence_review.md). Full two-way ownership history of the whole candidate pool was not certified.
- Industry ratios from the registered Damodaran files are aggregates, not medians; they are a plausibility check only.
- Published regressions are market-wide, low R-squared, about ten months older than the valuation date, with no standard error: a gap to the market price is not proof of mispricing. The model shown is the one with the highest published R-squared.
- Peer interquartile ranges are dispersion, not confidence intervals. Human Spot_check is PENDING (not performed).
- Academic analysis only; not investment advice.
