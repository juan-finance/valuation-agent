# Relative valuation by regression — Europe, VWS.CO, 2026-10-30

## Headline
Draft PBV selected by highest eligible published R2 (0.423), a weaker heuristic rather than adjusted-R2/industry fit. No EV/EBIT equation exists. Positive NI and equity make all three models computable.

## Scope
VWS.CO only; no market sample/own estimation/DATA_BASE_MSCI under published route. Other candidates are not additional valuation targets.

## Data
FY2025 uniform vendor inputs cross-checked with issuer Annual Report 2025. Denmark listing resolves EUROPE exact, not GLOBAL fallback; diversified global sales are a limitation, not a reason to average equations. Vendor 3Y analyst consensus g_eps32.41%/g_rev8.34% used and labelled (not 5Y); declared payout ~12.8% (DKK0.74 proposed); closing parent ROE 0.2012 for the equations vs average-equity ROE for peer scoring.

## Fitted model
| model     |   predicted |   published_r2 |   value_per_share |   actual |   actual_predicted_gap |
|:----------|------------:|---------------:|------------------:|---------:|-----------------------:|
| PE        |    29.7003  |          0.201 |           176.529 | 31.84    |              0.0720419 |
| PBV       |     4.25341 |          0.423 |           125.657 |  6.40588 |              0.506057  |
| EV/EBITDA |    21.6888  |          0.262 |           256.317 | 15.8398  |             -0.269679  |

## Diagnostics
Integrity findings retained in regression_results.json. GLOBAL PEG/PBV and EM EVEBITDA source anomalies do not affect these EUROPE equations; those anomalous equations are not used. No n, SEy, adjusted R2, p-values, A/B/C, typicality or D1–D10 available: n/a_published_route. Classification: Not classified (no SEy published).

## Valuation results (sorted from most undervalued to most overvalued)
| model     |   value_per_share |
|:----------|------------------:|
| EV/EBITDA |           256.317 |
| PE        |           176.529 |
| PBV       |           125.657 |

## Robustness
All units decimal as approved; EVEBITDA alternative percentage-point DFR/tax prediction saved. Compare Machinery industry ratio, not median. Published EV excludes associate deduction by convention. Live predictions and price bridges reference Inputs; recalculation validation follows in formula_checks.json. Values converted EUR→DKK at ECB 7.4735.

## Key warnings
DRAFT pending human Spot_check. Primary EV/EBIT per bucket-C mapping is qualified: comparable EV excludes associates only where their income is excluded from the denominator, and peer associate/lease/claim data are not uniformly certified — EV rows and the EV/EBIT estimate remain qualified, not unqualified primary evidence. PE and EV/Sales retained as ordered cross-checks. No DCF, recommendation, synthesis weight or residual-band classification.

## Limitations
Market-wide, low-R2 equations not sector fair-value proof. January2026 vintage ~304 days old at valuation date. File requires analyst 5Y growth; vendor consensus is 3Y and fundamental growth 0.190 differs — definition gap disclosed. Beta benchmark/frequency unspecified. Published EV definition undocumented. No residual dispersion or confidence range invented. Cash partly customer-advance driven; book NCI/dated balance are proxies.

## Sources
source_log.csv; registered regressions_multi_2026-01 SHA a894ea86f209d59c68c57ba5674ee096ee875cf9726af2cfe84ec212af1d9bf5; official annual report in relative_inputs.md.

## Exact equations and t-statistics
See Coefficients_PE/PBV/EV_EBITDA workbook sheets for each coefficient/t statistic and dataset SHA.
$\text{PE} = \underset{(8.29)}{9.72} + \underset{(4.85)}{2.99} \, \text{Beta} + \underset{(11.95)}{49.82} \, g_{\text{EPS}} + \underset{(9.22)}{7.98} \, \text{Payout}$
$\text{PBV} = \underset{(3.70)}{0.73} + \underset{(5.87)}{3.92} \, g_{\text{EPS}} + \underset{(1.38)}{0.13} \, \text{Beta} + \underset{(24.81)}{10.75} \, \text{ROE} - \underset{(2.43)}{0.25} \, \text{Payout Ratio}$
$\text{EV/EBITDA} = \underset{(28.40)}{18.15} + \underset{(13.96)}{35.25} \, g - \underset{(10.65)}{0.11} \, \text{DFR} - \underset{(5.19)}{0.12} \, \text{Tax Rate} + \underset{(5.06)}{2.29} \, \text{ROIC}$
