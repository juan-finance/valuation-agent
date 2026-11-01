# Relative valuation by regression — EUROPE, 2026-10-30 (published_damodaran route)

## Headline
Published EUROPE equations (regressions_multi_2026-01): **PBV chosen** — predicted 2.151x → **€6.95/share** vs price €9.32 (−25.4% rich, deviation actual/predicted −1 = +34.1%). Alternatives: EV/EBITDA predicted 19.41x → €31.81/share; PE predicted 26.07x → €10.41/share. Market-wide equations (low R²), not industry fits; deviation from prediction is not proof of mispricing. The peer method (comparables_report.md) gives EV/EBITDA €17.79/share mid — the two methods bracket the price in opposite directions; both are shown, none reconciled under relative_only.

## Data
Uniform vendor FY2025 inputs (StockAnalysis, accessed 2026-11-01), cross-checked vs Enel FY2025 results press release. Inputs: beta 0.84 (vendor 5Y observed); g_eps 7.63% and g_rev 3.17% analyst consensus 3Y (sourced — no substitution needed; consistent with Enel's 2026-28 plan EPS path ~6% CAGR); roe 0.1235 closing book (NI to common €3,959m / parent equity €32,068m); payout 1.26 (declared €4,982m / NI to common; 1.18 on issuer group NI — flagged, part-funded from reserves); dfr 0.4274; tax_rate 0.3305 effective FY2025; roic 0.0994. Negative inputs absent — all three models eligible.

## Fitted model
Route `published_damodaran`: `datasets.equation_for('Italy', dep, 2026-10-30)` → EUROPE region, regressions_multi_2026-01 (sha256 a894ea86…). Equations and published t-statistics on Coefficients_* sheets of regression_valuation.xlsx; live-formula predictions verified vs `published_regressions.predict` <1e-9 after recalculation. Model choice: highest published R² among eligible → PBV (R²=0.423) over EV/EBITDA (0.262) and PE (0.201); ranking by published R² is a weaker heuristic than own-sample adjusted R².

## Diagnostics
Not available under this route: n, SEy, adjusted R², p-values, A/B/C scopes, typicality routing, D1–D10, robustness refits and residual-band classification (all `n/a_published_route`). Reported instead: predicted multiple, actual multiple, deviation, published R² and t-statistics. Dataset integrity findings from stage 0 retained (GLOBAL anomalies do not affect EUROPE equations).

## Valuation results (sorted from most undervalued to most overvalued)

| model | predicted | published R² | actual | deviation | EUR/share |
|---|---|---|---|---|---|
| EV/EBITDA | 19.41x | 0.262 | 8.43 | −56.6% | €31.81 |
| PE | 26.07x | 0.201 | 23.35 | −10.4% | €10.41 |
| PBV | 2.151x | 0.423 | 2.88 | +34.1% | €6.95 |

## Robustness
Decimal unit policy is user-approved (`damodaran_dfr_tax_units: decimal`); percentage-point alternative for EV/EBITDA shown in regression_results.json `unit_alternative` (19.41x decimal vs 10.83x pp — material 44% gap, decimal policy verified per standing approval). Payout basis sensitivity: 1.26 reported vs 1.18 group-NI basis — direction unchanged. No PS equation exists (documented); supplementary PEG/EV/IC/EV/Sales not used in standard mode.

## Key warnings
Provisional: human Spot_check pending; ownership/event audit incomplete. Payout >100% (dividend part-funded from retained earnings) is an unusual input state for the published equations — flagged, not clipped. The market-wide EV/EBITDA prediction (19.4x) sits far above the European utility peer median (12.6x): sector mix in a market-wide equation is not structure the model can see; peer-method result preferred for the EV/EBITDA view.

## Limitations
Equation vintage Jan-2026 (~10 months > 6-month flag). Market-wide scope — no sector structure; utilities predictions can differ from sector reality (published R² 20–42%). Analyst-growth definition differs from project fundamental growth (consensus used and labelled). Damodaran EV/invested-capital definitions undocumented (leases/NCI/associates treatment may differ). No residual dispersion — deviation is not a residual-band classification. No DATA_BASE_MSCI.xlsx under this route.

## Sources
source_log.csv (S3_* rows); registered regressions_multi_2026-01 via data library; Enel issuer FY2025 press release; stockanalysis uniform extracts; cache/macro/2026-10-30.json FX.
