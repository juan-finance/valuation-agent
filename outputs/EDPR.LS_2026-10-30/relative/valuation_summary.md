# Relative valuation by regression — EUROPE, 2026-10-30 (published_damodaran route)

## Headline
Published EUROPE equations (regressions_multi_2026-01): **PBV chosen** — predicted 1.697x → **€16.45/share** vs price €12.50 (+31.6%, deviation actual/predicted −1 = −24%). Alternatives: EV/EBITDA predicted 21.09x → €14.10/share; PE predicted 26.93x → €5.48/share. Market-wide equations (low R²), not industry fits; cheap vs prediction is not proof of mispricing.

## Data
Uniform vendor FY2025 inputs (StockAnalysis, accessed 2026-11-01), cross-checked vs EDPR FY25 Results Report. Inputs: beta 0.72 (vendor 5Y observed); g_eps 20.42% and g_rev 8.51% analyst consensus 3Y (sourced — no substitution needed); roe 0.0210 closing book; payout 0.61 (proposed scrip €132.1m / reported NI €215.8m; 0.40 on recurring NP; paid-cash 0.014 flagged); dfr 0.416; tax_rate 0.3537 effective FY2025; roic 0.0106. Negative/zero inputs absent — all three models eligible.

## Fitted model
Route `published_damodaran`: `datasets.equation_for('Portugal', dep, 2026-10-30)` → EUROPE region, regressions_multi_2026-01 (sha256 a894ea86…). Equations and published t-statistics on Coefficients_* sheets of regression_valuation.xlsx; live-formula predictions verified vs `published_regressions.predict` <1e-9 after recalculation. Model choice: highest published R² among eligible → PBV (R²=0.423) over EV/EBITDA (0.262) and PE (0.201); ranking by published R² is a weaker heuristic than own-sample adjusted R².

## Diagnostics
Not available under this route: n, SEy, adjusted R², p-values, A/B/C scopes, typicality routing, D1–D10, robustness refits and residual-band classification (all `n/a_published_route`). Reported instead: predicted multiple, actual multiple, deviation, published R² and t-statistics. Dataset integrity findings from stage 0 retained (GLOBAL anomalies do not affect EUROPE equations).

## Valuation results (sorted from most undervalued to most overvalued)

| model | predicted | published R² | actual | deviation | EUR/share |
|---|---|---|---|---|---|
| PBV | 1.697x | 0.423 | 1.288 | −24.1% | €16.45 |
| EV/EBITDA | 21.086x | 0.262 | 19.65 | −6.8% | €14.10 |
| PE | 26.93x | 0.201 | 61.4 | +127.9% | €5.48 |

## Robustness
Decimal unit policy is user-approved (`damodaran_dfr_tax_units: decimal`); percentage-point alternative for EV/EBITDA shown in regression_results.json `unit_alternative`. Payout basis sensitivity: recurring-policy 0.40 vs reported 0.61 changes PBV +0.05x and PE −3.3x — direction unchanged. No PS equation exists (documented); supplementary PEG/EV/IC/EV/Sales not used in standard mode.

## Key warnings
Provisional: human Spot_check pending; ownership/event audit incomplete. High effective tax (35.4%) and thin reported ROE (2.1%) drive conservative inputs. EDPR's vendor EBITDA basis omits equity-method/partnership income carried in its EV claims — EV multiples biased low (see comparables_report).

## Limitations
Equation vintage Jan-2026 (~10 months > 6-month flag). Market-wide scope — no sector structure; utilities predictions can differ from sector reality (published R² 20–42%). Analyst-growth definition differs from project fundamental growth (consensus used and labelled). Damodaran EV/invested-capital definitions undocumented (leases/NCI/associates treatment may differ). No residual dispersion — deviation is not a residual-band classification. No DATA_BASE_MSCI.xlsx under this route.

## Sources
source_log.csv (S3_* rows); registered regressions_multi_2026-01 via data library; EDPR issuer FY25 report; stockanalysis uniform extracts; cache/macro/2026-10-30.json FX.
