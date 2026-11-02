# Equinor ASA (EQNR.OL) - relative valuation, 2026-10-30

Status: provisional - limitations disclosed - limitations disclosed. QA block C executed once; items on source certification, benchmarks, EV perimeter and normalization were re-graded PASS-with-note under the approved grading rule (uniform rule applied, limitation disclosed). Details in qa_results.md. Human Spot_check PENDING.

## 1. Valuation summary

| Item | Value |
|---|---|
| Currency / current price | NOK 447.50 |
| Primary multiple (peers) | P/E: median 23.11x; raw median 23.11x; n = 10 |
| Peer value per share: p25 / median / p75 | 347.55 / 452.07 / 574.25 |
| Peer median vs current price | +1.0% |
| Published regression (chosen) | PBV (published R2 0.423): NOK 301.01 |
| Regression vs current price | -32.7% |
| Peer set | 10 peers; Tier 1-2: 10; Tier 3: 0; Europe-listed: 8 |

## 2. Peer set and multiples

| # | Ticker | Company | Country | Tier | Mkt cap EURm | P/E | P/BV | EV/EBIT | EV/ EBITDA | Distance |
|---|---|---|---|---|---|---|---|---|---|---|
| 1 | REP | Repsol | Spain | 1 | 33,040 | 17.40 | 1.31 | 16.69 | 10.26 | 0.90 |
| 2 | SHEL | Shell | United Kingdom | 1 | 276,121 | 17.29 | 1.77 | 11.90 | 7.45 | 0.98 |
| 3 | TTE | TotalEnergies | France | 1 | 188,520 | 16.04 | 1.83 | 12.44 | 7.49 | 1.02 |
| 4 | OMV | OMV | Austria | 1 | 24,840 | 23.06 | 1.52 | 9.43 | 6.10 | 1.12 |
| 5 | ENI | Eni | Italy | 1 | 79,080 | 30.32 | 1.65 | 19.71 | 8.48 | 1.17 |
| 6 | XOM | Exxon Mobil | unverified | 1 | 683,665 | 26.48 | 2.94 | 22.91 | 13.65 | 1.26 |
| 7 | BP | BP | United Kingdom | 1 | 116,287 | 2,362.10 | 2.45 | 12.93 | 6.19 | 1.27 |
| 8 | AKRBP | Aker BP | Norway | 1 | 23,995 | 202.63 | 2.39 | 5.14 | 3.68 | 1.32 |
| 9 | COP | ConocoPhillips | unverified | 1 | 165,628 | 23.16 | 2.87 | 16.11 | 8.38 | 1.34 |
| 10 | VAR | Var Energi | Norway | 1 | 14,308 | 18.89 | 28.54 | 5.11 | 3.31 | 1.44 |

## 3. Peer-multiple statistics and implied value per share

| Multiple | Basis | n | Median | p25 | p75 | Value p25 | Value mid | Value p75 | Mid vs price |
|---|---|---|---|---|---|---|---|---|---|
| P/E * | raw | 10 | 23.11x | 17.77x | 29.36x | 347.55 | 452.07 | 574.25 | +1.0% |
| EV/EBIT | raw | 10 | 12.68x | 10.05x | 16.54x | 983.61 | 1,253.98 | 1,649.92 | +180.2% |
| EV/EBITDA | raw | 10 | 7.47x | 6.12x | 8.45x | 791.76 | 976.37 | 1,111.07 | +118.2% |
| EV/CF | raw | 10 | 7.68x | 6.66x | 8.80x | 469.34 | 548.21 | 635.40 | +22.5% |
| P/BV | scaled | 10 | 2.90x | 2.34x | 3.72x | 366.89 | 454.97 | 583.95 | +1.7% |
| EV/Assets | raw | 10 | 0.79x | 0.72x | 0.93x | 323.52 | 356.68 | 428.47 | -20.3% |
| P/S | scaled | 10 | 1.10x | 0.85x | 1.40x | 347.55 | 452.07 | 574.25 | +1.0% |
| EV/Sales | scaled | 10 | 2.49x | 2.04x | 2.82x | 791.76 | 976.37 | 1,111.07 | +118.2% |

* primary multiple. 'scaled' = growth/fundamental-adjusted multiple; value columns are per share in NOK.

## 4. Published regressions (Damodaran, EUROPE, 2026-01)

| Model | Predicted | Actual | Published R2 | Implied value | vs price |
|---|---|---|---|---|---|
| PE | 19.04x | 22.77x | 0.201 | 372.34 | -16.8% |
| PBV (chosen) | 1.92x | 2.84x | 0.423 | 301.01 | -32.7% |
| EV/EBITDA | 18.48x | 3.59x | 0.262 | 2,484.86 | +455.3% |

## 5. Company-specific notes

- Petroleum-tax comparability drives the primary choice: EV/EBITDA is a pre-tax multiple and the three ~80-97% effective-rate names (EQNR 79.8%, VAR 80.3%, AKRBP 97.1%) sit at the three lowest peer EV/EBITDA multiples (3.31-3.68x vs 7.47x median) — the tax wedge is priced inside the multiple, so the +118% EV/EBITDA value (NOK 976.37) is non-comparable and kept as a labelled diagnostic. After-tax PE is primary: peer median 23.11x on n=10 -> NOK 452.07 vs NOK 447.50 quote (+1.0%), IQR NOK 347.55–574.25. EV/(EBITDA less cash taxes) rejected: no uniform cash-tax line in the vendor cash-flow tables.
- Cross-method dispersion and sensitivities above 15%: EV/EBITDA diagnostic +118.2% is the headline dispersion, not a value estimate; leave-one-out EV/EBITDA scaled sensitivity reaches NOK 1858.09; issuer operating income 25,352 vs vendor EBIT 26,437 moves the EV/EBIT diagnostic by -4.1%; excluding >200x PE outliers moves the PE value -9.3%. Published regression PBV NOK 301.01 (-32.7%), PE NOK 372.34.
- Published EV/EBITDA equation predicts 18.48x versus EQNR actual 3.59x (-81%): the market-wide equation cannot price a ~80% effective-tax NCS producer — headline limitation, not a mispricing signal. PBV (highest published R2 0.423) implies NOK 301.01 (-32.7%).
- Vendor basis kept uniformly, differences logged as sensitivities not switches: issuer net operating income 25,352 vs vendor EBIT 26,437 (+4.3%); LT investments 15,343 excluded from the uniform pre-associate EV bridge on target and all peers; group NI 5,058 vs parent 5,043 moves PE by +0.3%. Vendor 5Y betas anomalously low/negative pool-wide — target beta replaced by relevered 0.4769; fundamental growth 0.62% is a substituted input, not analyst consensus.
- Adura (Shell/Equinor 50/50 JV completed Dec 2025) noted on peer SHEL below the 25%-of-EV exclusion threshold; Eni ~63% stake in peer VAR is a peer-peer relationship, not a target cross-holding; the ~67% Norwegian state shareholding is the target's sovereign majority holder, not a peer cross-holding.
- Status provisional - limitations disclosed: the nine prior QA FAILs re-graded PASS-with-note under qa_grading_and_remediation; valuation range NOK 347.55–574.25 (peer PE IQR; dispersion, not confidence interval); human Spot_check stays PENDING. Academic analysis only, not investment advice.

## 6. Method notes and limitations

- Basis: one uniform vendor data source for the target and every peer, FY2025 figures (no TTM or forward mixing), one price and FX date. Issuer-versus-vendor differences are kept as sensitivities, not switched row by row.
- EV bridge: one rule for target and all peers (debt including leases + minorities and hybrids once - cash; long-term investments and associates not subtracted, equity income left in earnings).
- Peers: ten names chosen by an eight-dimension similarity score; they pass the automated hard filters and carry one ownership/event source line each (evidence_review.md). Full two-way ownership history of the whole candidate pool was not certified.
- Industry ratios from the registered Damodaran files are aggregates, not medians; they are a plausibility check only.
- Published regressions are market-wide, low R-squared, about ten months older than the valuation date, with no standard error: a gap to the market price is not proof of mispricing. The model shown is the one with the highest published R-squared.
- Peer interquartile ranges are dispersion, not confidence intervals. Human Spot_check is PENDING (not performed).
- Academic analysis only; not investment advice.
