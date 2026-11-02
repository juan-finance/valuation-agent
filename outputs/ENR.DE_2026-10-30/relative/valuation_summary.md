# Current remediation disposition

Status: provisional - limitations disclosed. EV/EBIT and growth-scaled PE are co-primary: EUR44.18 and EUR71.47 respectively; combined peer-IQR envelope EUR42.87–104.07 (not confidence bounds). Uniform pre-associate vendor EV bridge in ev_bridge.csv;10 selected source-line qualified peers.855.34m shares base/850m sensitivity; Tier3cap4 retained (3 used/7 Tier1–2/9 Europe). See report_notes.md, peer_qualification.csv and current qa_results.md block. Prior blocking/fallback-only wording below is historical and superseded. Human Spot_check PENDING.

## Historical analysis

# Relative valuation by regression — Europe, ENR.DE, 2026-10-30

## Headline
Draft PBV selected by highest eligible published R2 (0.423), a weaker heuristic rather than adjusted-R2/industry fit. No EV/EBIT equation exists. Positive NI and book make equity models computable but recovery/loss history limits book comparability.

## Scope
ENR.DE only; no market sample/own estimation/DATA_BASE_MSCI under published route. Other candidates are not additional valuation targets.

## Data
FY2025 uniform vendor inputs cross-checked with issuer. Germany listing resolves EUROPE exact, not GLOBAL fallback; diversified global sales are a limitation, not a reason to average equations. Fundamental growth uses closing parent ROE13.73%, explicitly approved substitution for unavailable matching5Y analyst growth; vendor3Y forecasts are not relabelled5Y consensus.

## Fitted model
| model     |   predicted |   published_r2 |   value_per_share |   actual |   actual_predicted_gap |
|:----------|------------:|---------------:|------------------:|---------:|-----------------------:|
| PE        |    22.0902  |          0.201 |           36.5183 |  76.7751 |               2.47553  |
| PBV       |     2.98422 |          0.423 |           35.9395 |  10.5388 |               2.5315   |
| EV/EBITDA |    23.4924  |          0.262 |           79.244  |  38.7086 |               0.647708 |

## Diagnostics
Integrity findings retained in regression_results.json. GLOBAL PEG/PBV and EM EVEBITDA source anomalies do not affect these EUROPE equations; those anomalous equations are not used. No n, SEy, adjusted R2, p-values, A/B/C, typicality or D1–D10 available: n/a_published_route. Classification: Not classified (no SEy published).

## Valuation results (sorted from most undervalued to most overvalued)
| model     |   value_per_share |
|:----------|------------------:|
| EV/EBITDA |           79.244  |
| PE        |           36.5183 |
| PBV       |           35.9395 |

## Robustness
All units decimal as approved; EVEBITDA alternative percentage-point DFR/tax prediction saved. Compare18.94x industry ratio, not median. Published EV excludes associate deduction by convention, so inverse has associates0 consistently. Live predictions and price bridges reference Inputs; recalculation validation follows in formula_checks.json.

## Key warnings
DRAFT pending human Spot_check. Primary PE rather than prescribed EV/EBIT: comparable EV associate values and uniform lease/cash/claim perimeter are unresolved. EV/Sales shares that bridge problem, so next ordered equity cross-check PE is used under comparables procedure section1. EV rows remain qualified pre-associate sensitivities, not compliant comparable EV base. No DCF, recommendation, synthesis weight or residual-band classification.

## Limitations
Market-wide, low-R2 equations not sector fair-value proof. January2026 vintage302 days old at valuation date. File requires analyst5Y growth, not our substituted sustainable growth; beta benchmark/frequency unspecified. Published EV definition undocumented. No residual dispersion or confidence range invented. Cash substantially driven by customer advances; book NCI/dated balance are proxies.

## Sources
source_log.csv; registered regressions_multi_2026-01 SHA a894ea86f209d59c68c57ba5674ee096ee875cf9726af2cfe84ec212af1d9bf5; official annual report in relative_inputs.md.

## Exact equations and t-statistics
See coefficient workbook sheets for each coefficient/t statistic and dataset SHA.
$\text{PE} = \underset{(8.29)}{9.72} + \underset{(4.85)}{2.99} \, \text{Beta} + \underset{(11.95)}{49.82} \, g_{\text{EPS}} + \underset{(9.22)}{7.98} \, \text{Payout}$
$\text{PBV} = \underset{(3.70)}{0.73} + \underset{(5.87)}{3.92} \, g_{\text{EPS}} + \underset{(1.38)}{0.13} \, \text{Beta} + \underset{(24.81)}{10.75} \, \text{ROE} - \underset{(2.43)}{0.25} \, \text{Payout Ratio}$
$\text{EV/EBITDA} = \underset{(28.40)}{18.15} + \underset{(13.96)}{35.25} \, g - \underset{(10.65)}{0.11} \, \text{DFR} - \underset{(5.19)}{0.12} \, \text{Tax Rate} + \underset{(5.06)}{2.29} \, \text{ROIC}$
