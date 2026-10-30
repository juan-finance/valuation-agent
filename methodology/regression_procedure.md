# Regression-based relative valuation procedure

Build a broad-market dataset and estimate your own regressions. This is separate from selected-peer medians and the optional one-driver peer fit in [comparables procedure](comparables_procedure.md). Do not hand-pick the market sample or replace estimation with published coefficients. The rules here are self-contained; no external instruction attachment is needed.

> **Route note (added 2026-10-30, user decision).** This procedure governs `regression_route: own_estimation`. When `memory/standing_approvals.md` sets `regression_route: published_damodaran`, the regression method follows [regression_published_route.md](regression_published_route.md) instead of sections 2-9, and the registered Damodaran equations are the model rather than a benchmark. The prohibition on replacing estimation with published coefficients applies to the own-estimation route. In both routes the Damodaran benchmark fields of section 10 are filled from the local data library (`data/README.md`), not from a live download.

## Contents

1. Configuration and data universes
2. Master dataset and definitions
3. Validation and cleaning
4. A/B/C specifications and dummy coding
5. Excel workbook and live formulas
6. Typicality and model selection
7. Predictions and classifications
8. Diagnostics and robustness
9. Recalculation, QA and stops
10. Output contracts and report
11. Explicit conflict resolutions and technical references

## 1. Configuration and data universes

Reuse a previously confirmed data route; otherwise establish terminal-export availability before collecting data. Record the selected route in both workbooks and the report. Terminal export → full version; no export → single-source web minimum version. Merely knowing the user has access to Bloomberg does not establish export availability. Continue nondependent preparation while awaiting input.

```yaml
universe_priority: [MSCI Europe, MSCI World]
full_universe: all_nonfinancial_constituents
minimum_universe: [Utilities, Energy, Industrials, Materials]
regressions: [A_sector, B_market_dummies, C_market]
models: [PE, PBV, PS, EVEBITDA]
sector_level_order: [Europe Industry, Europe Industry Group, World Industry, World Industry Group, World Sector]
dummy_base_sector: Industrials
dummy_base_region: Europe
region_dummies: A_and_B_only_when_World_rows_used
energy_transition_dummy: false
exclude: [Banks, Insurance, Other Financials, REITs]
growth: fundamental
rate_units: decimal
earnings_basis: FY2025
valuation_date: required_common_date
min_obs_A: 30
min_obs_BC_Europe_full: 150
min_obs_BC_Europe_minimum: 100
min_obs_BC_World_full: 500
min_obs_BC_World_minimum: 150
max_PE: 100
beta_replacement_upper_bound: 2.5
winsorize_continuous: [0.01, 0.99]
fair_band: 1.0
strong_band: 2.0
significance_level: 0.05
correlation_warn: 0.80
vif_warn: 5
vif_severe: 10
crosscheck_vintage: January_2026_MReg26
```

All thresholds are project settings; disclose overrides. FY2025 is the base fiscal period, not synonymous with TTM. If explicitly using TTM/forward, align every row and predictor period, record the change and keep separate series. No future information beyond the valuation cutoff is allowed.

Include every company in the defined membership universe, then apply rule-based exclusions. Full = all permitted nonfinancial constituents; minimum = only the four specified sectors, explicitly described as a reduced market, not the entire economy. Always retain all 20 target records with is_sample=TRUE, even in single-target (orchestrator) mode, where only the requested target is valued but the market dataset and estimation sample stay identical to the batch run (reuse an existing dated DATA_BASE_MSCI.xlsx for the same cutoff when available), whether or not they are members/eligible; mark out-of-index targets separately so the master membership count remains honest. Apply the guide's target inclusion rule in model universes when scope/eligibility match; retain market-members-only sensitivity if added targets materially affect the fit. Do not drop loss-makers from the master; eligibility differs by model.

For A, choose the first scope in the configured ladder with at least 30 valid rows for that model after cleaning. Never insert Europe Sector earlier in the ladder. If World Sector still fails, A is unavailable and its validity/typicality test fails. For B/C, start with Europe and expand the model's entire market to World when its required clean count fails; both B and C use that same market/row set. If still insufficient, mark that model unavailable, notify the user, and continue valid models. Record every model's geography, GICS level, counts and switch. The base regression is not the 20-company target list or the 20 selected peers.

Use membership dated at the cutoff if available; otherwise disclose membership-vintage/survivorship limitations. ETF holdings are a proxy, not guaranteed exact index constituents: verify tracking index, date, all pages/holdings count and remove cash/derivatives/duplicate listings transparently. Do not invent historical membership. Regression retains parent and listed subsidiary if both are constituents/targets, with dependence flagged; the peer-selection exclusion is method-specific.

## 2. Master dataset and definitions

Create DATA_BASE_MSCI.xlsx with Data, Raw_Inputs, Checks, Spot_check, Universe and Log. The first 18 Data columns, in order, are:

```text
Company Name,beta,D/E,Price,Current PE,Trailing PE,Forward PE,PEG,PBV,PS,EV/EBIT,EV/EBITDA,EV/Sales,Payout ratio,Dividend Yield,g,Return on Equity,Net Profit Margin
```

Append ISIN, Country, Currency, region, GICS Sector, GICS Industry Group, GICS Industry, Market cap (EUR), Operating Margin, Tax Rate, ROIC, DFR, is_sample, cluster, source_urls. Also retain ticker, entity/security IDs, price_ccy, reporting_ccy, price_date, fiscal/TTM period boundaries, export date, membership flags, raw financials and source field IDs. Use the exact first-18 layout even if a Japan-example workbook is absent; do not claim an unseen workbook was matched beyond this documented schema.

Definitions:

- Company Name: Name (Exchange:Ticker). One economic issuer row; sum distinct common share classes in equity capitalization, deduplicate secondary listings/ADRs. If unequal share-class rights make per-share valuation ambiguous, establish the allocation rather than assume equivalence.
- beta: five-year regression beta, consistently sourced/windowed, benchmark index identified (local index under this method). The DCF's preferred bottom-up beta does not automatically replace the relative regression input; only the specified fallback does.
- D/E = total debt including leases / market common equity; use the same debt in DFR and EV. DFR = debt/(debt+market equity).
- Price: normalized quote currency, including GBX/100→GBP. Convert EPS/DPS to that currency before price ratios; convert monetary totals to a common currency before dividing. EUR capitalization is for comparability, not a forced change in final quote currency.
- Current PE = price/FY EPS; Trailing PE = price/TTM EPS; Forward PE = price/next-year consensus EPS. Use NA where the matching series is absent. Configured PE model uses the configured basis (default Current PE/FY2025), never chooses whichever series gives a desired result.
- PEG column preserves the prescribed Trailing PE/(100×g) definition; NA for g<=0 or missing TTM PE. Keep a separately labelled FY PEG if needed for FY peer valuation.
- PBV = market common equity / parent common book equity; PS = market common equity / consolidated sales with perimeter caveat; NI for EPS, ROE and net margin is attributable to parent common shareholders consistently.
- Baseline regression EV = market equity + financial debt including leases + NCI − cash. EV/EBIT, EV/EBITDA and EV/Sales divide by matching operating measures. This differs from comparable EV, which also removes excluded associates; maintain ev_regression and ev_comparables separately and reconcile. Do not add associates in the regression equity bridge unless they were removed in its EV construction. Additional financing claims require uniform explicit expanded definition; do not patch only the target numerator.
- Payout ratio = common dividends/parent common NI, or DPS/EPS with matched share basis. Zero payout is valid; a negative payout ratio is invalid for models using it. Keep observed payout>1 as observed and flag it; only the growth retention calculation caps it.
- g = ROE×(1−MIN(payout,1)), when ROE>0 and payout is valid; otherwise NA. This fundamental proxy is the regression default even if the peer method uses consensus. Do not silently import the DCF's growth estimate. Using last-year profitability as expected growth is a limitation.
- ROE = parent common NI / parent common book equity of the configured fiscal year-end, as specified for this regression. It differs from the DCF's beginning-equity and any peer average-equity convention: keep distinct named fields.
- Net margin = parent common NI/sales. Operating margin = EBIT/sales. Tax rate = income-tax expense/pretax profit. ROIC = EBIT×(1−tax rate)/(book equity+debt−cash). Use a matched consolidated book-capital perimeter including NCI if EBIT includes those operations; log the definition. Nonpositive/near-zero invested capital or pretax earnings requires review/NA, not automatic nonsensical ratios.
- region: Europe, North America, Japan, Pacific ex Japan, Other. Distinguish price currency, incorporation country, MSCI market classification and revenue geography; they are not interchangeable.

Keep raw and transformed columns separate. Missing numbers are NA, never zero; no fabricated estimates, interpolation or mean filling. Permitted bottom-up beta and formula growth are transparent derived fields with sourced inputs, not exceptions allowing arbitrary imputation.

## 3. Validation and cleaning

Use [data sources](data_sources.md) for the route and field-level evidence. Under web collection, use stockanalysis raw financials uniformly; if a company page is unavailable retain the row with missing fields rather than silently source a different vendor. Confirm raw source units; normalize entire known-unit columns to decimals, retaining the original representation. A median>1 is a warning to inspect percent units, not proof: real payout/ROE above 100% is possible, and mixed-unit columns must be resolved from provenance. Do not divide valid decimal payouts by 100 just to satisfy the heuristic.

Validate before estimation:

- Equity capitalization versus class-level price×shares within 2%; resolve GBX, share-class or date differences.
- Recompute all ratios from underlying data; vendor ratios are cross-checks, with >2% differences logged.
- Verify common price/FX date and price freshness (at most five trading days); a freshness pass does not authorize inconsistent dates.
- Flag multiples outside raw 1st/99th percentiles for investigation.
- Compare sector medians of PE/PBV/EVEBITDA with matching regional industry benchmarks. A >50% relative gap blocks final use until data/statistic/basis errors are corrected or a real scope/economic difference is evidenced. Do not manipulate data to match a benchmark.
- Spot_check: all target rows plus 20 randomly selected non-target universe rows, without replacement, reproducible seed and source links. Record user check status. More than two erroneous random rows triggers collection repair and repeat checks before final regression use. Human review cannot be asserted by the agent.

For each model and universe apply the same documented order:

1. Deduplicate by issuer/verified security mapping (retain the first consistent canonical occurrence, log others). Retain raw rows unchanged; share-class aggregation precedes duplicate disposal and must be traceable.
2. Validate units, evidence and apply permitted beta replacement BEFORE final missing-X exclusion. Replace a missing, negative or >2.5 beta with beta_U×[1+(1−T_marg)×market D/E], using region-appropriate/global industry beta and sourced marginal rate/leverage. Record original, replacement, source and formula. Zero or unusually low positive beta is flagged for investigation, not automatically overwritten. A missing fallback component leaves beta missing.
3. Exclude only missing/unsourced/non-numeric fields required for THIS model, invalid price, nonpositive Y or invalid Y denominator. PE excludes EPS<=0 or PE>100; PBV excludes nonpositive common book equity; PS requires positive sales; EVEBITDA requires positive EV and EBITDA. Negative payout fails models that use it. Keep excluded target rows in final target output with a reason; unavailable PE does not exclude a valid PBV model.
4. Flag g<−0.5 or g>1 and observed payout>1. Compute raw-Y Q1/Q3 and flag beyond [Q1−3×IQR,Q3+3×IQR] without deleting in the base case. These pre-winsor flags trigger robustness; preserve them even if clipping later hides extremes.
5. Winsorize each continuous Y and X at 1st/99th percentiles within the model's eligible estimation set using PERCENTILE.INC. Show lower/upper cutoffs and original values. Do NOT winsorize dummy variables or identifiers. B/C for a given model use identical cutoffs and continuous rows. A uses its own scoped set. No additional base-case outlier deletion.
6. Remove constant X columns explicitly, log the structural exception and recompute k. Check full column rank including intercept. Omit redundant reference/empty dummy columns; do not let hidden LINEST collinearity removal silently alter degrees of freedom. Resolve substantive exact dependencies explicitly; if unresolved mark the design not estimable. k counts all retained continuous X and dummy columns, excluding intercept.
7. Apply hard sample minimums in section 1. n<10×k is a separate diagnostic warning (including dummies), not a silently substituted hard minimum. Require df=n−k−1>0 and positive finite residual variance; otherwise standard errors/classifications are undefined and the model is not usable.

Model-specific accounting: every raw row belongs either to the clean estimation partition or to Excluded for that model with one first-failure reason (including out-of-universe); do not add counts from different model partitions. Targets remain visible even when excluded. Loss-makers may still fail PS because the configured fundamental g is unavailable; keeping them in the master does not guarantee eligibility.

## 4. A/B/C specifications and dummy coding

| Model | Y on configured period | Continuous X in this order |
| --- | --- | --- |
| PE | Price/EPS | g, beta, payout |
| PBV | Market common equity/common book equity | ROE, beta, payout |
| PS | Market common equity/sales | net margin, payout, g |
| EVEBITDA | Regression EV/EBITDA | g, DFR, tax rate, ROIC |

Do not add g to PBV; it is already derived from ROE and payout. Run each model wherever data pass; missing one model does not authorize fabricated inputs for it.

- **A:** narrowest valid industry/industry-group/last-resort-sector scope under the exact geography ladder. No industry dummy within one industry; if World rows used, add region dummies.
- **B:** all eligible market rows with one GICS sector dummy per nonbase category. Although sometimes called “industry dummies,” the default is SECTOR dummies. Base = Industrials when present. Merge nonbase sectors with fewer than 10 cleaned companies into Other, log mapping. If base absent choose an observed base explicitly and map target coding; never include a constant-zero reference as if estimated.
- **C:** same market rows, Y and continuous X as B; NO sector OR region dummies, including World runs.

World A/B: Europe is the base region, one dummy per other observed region. Merge nonbase regions with fewer than 10 rows into Other; never silently merge away the required European reference. If Europe itself is sparse flag it; if absent a European prediction cannot be inferred from an unobserved reference, so mark that World specification unusable for the target until resolved. Omit all-zero columns; check rank. If Other remains small, retain it with a small-category warning rather than fabricate members. Count thresholds and category mapping are model-specific after cleaning.

Target dummies must match the saved coding; European targets have zero non-Europe region dummies. Dummy coefficients describe conditional level differences, not causal “sector value.” A−C or A−B differences can also reflect different samples, slopes and transformations; they do not equal B's sector coefficient mechanically.

Energy Transition dummy is OFF unless explicitly requested. If enabled, create a verified GICS-code map across Industry/Sub-Industry levels for renewable electricity, independent power producers, electric utilities, electrical components/equipment and heavy electrical equipment; include the 20 targets as prescribed, log that target-based rule and assess collinearity. Do not match mixed GICS levels by unverified text labels.

## 5. Excel workbook and live formulas

Create regression_valuation.xlsx. Main sheets, in order: README, Raw_Data, Clean_Data, Excluded, Correlations, Regression, Diagnostics, Valuation, Robustness (if triggered), Targets (if extra nonsample targets), Log. The main analytic sheets are indices/summary blocks; append named model sheets such as A_Util_PBV, B_PBV, C_PBV containing each model's clean design, statistics and valuations. Use unique names <=31 characters and a Model_Index mapping. Use worksheet-scoped or model-prefixed named ranges/cells to prevent one model overwriting another's coefficients.

Raw_Data is the immutable received snapshot, including sources and raw observations. Store constants/raw inputs there or in identified configuration cells; derived values elsewhere are live formulas. Stage the underlying raw fields inside the regression workbook so calculation does not depend on a broken external workbook link. Retain a manifest tying this snapshot to DATA_BASE_MSCI.xlsx. Formula-derived master fields must be recomputed from the local raw inputs, not merely pasted into analytical sheets.

For the PE example, Clean_Data core fields are A=company, B=price, C=converted EPS, D=raw computed PE (=B2/C2), E=g, F=beta, G=payout, H=sector. Add separate contiguous estimation-Y and estimation-X columns for the winsorized inputs; Y_range/X_range reference those actual numeric design columns, not the raw D:G block. Other models compute their correct Y; do not apply price/EPS to PBV, PS or EVEBITDA. Row 1 is headers; estimation rows 2 through n+1 match exactly. Preserve raw/clean linkage IDs and formula-based eligibility; when inputs change, filters, row counts and ranges must update or the workbook must visibly demand regeneration before results are used. Prefer dynamic tables/ranges where supported.

Define `L = LINEST(Y_range,X_range,TRUE,TRUE)` as a readable alias; implement it as a named formula, LET binding, or write out the LINEST expression in INDEX formulas. Output is 5×(k+1): row 1 coefficients, row 2 their SEs; coefficients are reversed relative to X column order; intercept is last. Row 3 = R², SEy; row 4 = F, residual df; row 5 = regression SS, residual SS. Other unused row-3–5 positions are documented #N/A.

For continuous/dummy variable j (1-based):

```text
b_j = INDEX(L,1,k-j+1)
se_j = INDEX(L,2,k-j+1)
b0 = INDEX(L,1,k+1)
se0 = INDEX(L,2,k+1)
n = ROWS(Y_range)
k = COLUMNS(X_range)
R2 = INDEX(L,3,1)
SEy = INDEX(L,3,2)
F = INDEX(L,4,1)
df = INDEX(L,4,2)
Adj_R2 = 1-(1-R2)*(n-1)/(n-k-1)
Sig_F = F.DIST.RT(F,k,df)
SS_reg = INDEX(L,5,1)
SS_resid = INDEX(L,5,2)
t_j = b_j/se_j
p_j = T.DIST.2T(ABS(t_j),df)
CI_low_j = b_j-T.INV.2T(0.05,df)*se_j
CI_high_j = b_j+T.INV.2T(0.05,df)*se_j
```

Verify LINEST df equals n−k−1 for the full-rank design. If not, inspect removed columns; do not use original k with changed rank. A zero SE requires diagnosis, not hidden IFERROR-to-zero. Coefficient table includes term, b, SE, t, p, 95% CI, expected sign and Sign OK. Sign check applies only to configured +/- signs; intercept, dummies and ambiguous signs get N/A rather than a false negative.

Correlations: CORREL for Y and each X on the same rows. For nonconstant full-rank X, define corr_X and compute VIF_j = INDEX(MINVERSE(corr_X),j,j); for one X, VIF=1. A singular matrix is a design failure to investigate, not permission to invent VIF. Auxiliary regressions VIF=1/(1−Rj²) are an equivalent check.

Predictions: b0+SUMPRODUCT(ordered_coefficients,matching_X_values), including dummies. Coefficients must first be remapped out of LINEST reverse order. Rates stay in decimals; per-1-percentage-point impact = b×0.01, per-0.1-beta impact = b×0.1. Workbook formulas use English names and commas when written programmatically; locale-specific display is handled by Excel. Do not use static ToolPak output as the model.

Valuation contains target rows; model fit/scatter schedules retain all estimation rows. Add an XY plot of actual (y) versus predicted (x) with a 45° line. Also provide cross-method distribution/football-field charts with current price and DCF markers, without a fabricated weighted average.

## 6. Typicality and model selection

For every target and candidate multiple, evaluate A with these three tests:

1. Pure play: >=50% revenue OR EBITDA in the A scope, supported by segment data. Explain conflicting/negative segment denominators; unavailable evidence fails the test rather than defaulting to true.
2. Typical fundamentals: ROE, beta, payout AND g all within inclusive p10–p90 of the eligible sector pool. Compute these percentiles on valid pre-winsor fundamentals for that A model's scope, using the same documented beta treatment; use actual target fundamentals, not clipped values. Missing any required test input fails typicality, even if that variable is not an X of the candidate model. Record values/cutoffs and which input failed.
3. Valid A for this multiple: n>=30 and Sig_F<0.05, with an estimable design. This is model-specific because significance/eligibility differs across multiples.

Route that target/model to A only if all pass, otherwise B. C is always a reference, not an automatic replacement for invalid B. A whole-company typicality label is a summary of the CHOSEN model's tests; retain the full target-by-model decision matrix.

Eligibility also requires target Y/X meaningful, positive denominators, PE<=100 for PE, and a positive predicted multiple. Extrapolated positive predictions remain flagged/indicative under the diagnostic policy, not silently clipped. Rank eligible routed models by adjusted R²; select the highest and show next two eligible alternatives (NA with reason if fewer). This extends the source's model-specific significance rule coherently when A eligibility differs by multiple. Record actual chosen scope in primary_regression; do not rank first and retroactively change its scope. Ties: smaller finite SEy/median(Y) on positive Y, then configured model order; disclose the deterministic tie policy.

Adjusted R² across different dependent multiples and sample sets is a project selection heuristic, not proof of best price accuracy. Report model n, scope, R², adjusted R², normalized residual dispersion and diagnostics alongside the ranking. Do not replace the assigned heuristic silently with an alternative. If the selected B fails significance, retain its numerical result as non-actionable/diagnostic and state that regression supplies no defensible valuation conclusion; do not silently promote C or force a result toward DCF.

Benchmark the same chosen multiple against the opened January 2026 Global and Western Europe & UK Damodaran equations. Respect each equation's exact variable units and transforms, even if different from our decimal inputs. Record coefficients, vintage, regressors and URLs. If relative prediction difference exceeds 30% against BOTH positive comparable benchmarks, flag it. Retain two separate fields, not an ambiguous pooled number. If an equation/matching input is unavailable or units cannot be verified, report unavailable; don't substitute a different multiple or an invented forecast. January 2026 is the assigned benchmark vintage, not a claim it is always the latest.

Compare A/B/C for the same chosen model, stating unavailable fits rather than fabricating predictions. Discuss conditional sector levels, different slopes, geography and row coverage. Agreement among valid specifications is corroboration, not independent proof of mispricing; they share inputs.

## 7. Predictions and classifications

Maintain two distinct views:

- **Estimation diagnostics:** fitted values and residuals from winsorized Y/X actually used in LINEST; this is what R², SEy and the independent check describe.
- **Target valuation:** apply fitted coefficients to actual sourced target X (with documented permitted beta fallback), use actual un-winsorized target multiple and actual denominator for price conversion. Flag any target X outside estimation MIN/MAX. Show a clipped-X sensitivity if it materially changes the result; do not silently value a fictional clipped target. Record this interpretation explicitly.

For each target: residual = actual multiple−predicted multiple; std_residual = residual/SEy; deviation = actual/predicted−1. SEy must be positive finite. Predicted<=0 → “Not valued (nonpositive prediction)”; missing X → “Not valued — missing data”; PE>100 → “Not valued by PE regression (above 100x)” with other models considered. Do not drop such targets from CSV/report.

| std_residual | Classification |
| --- | --- |
| <−2 | Significantly undervalued |
| >=−2 and <−1 | Moderately undervalued |
| >=−1 and <=1 | Fairly valued |
| >1 and <=2 | Moderately overvalued |
| >2 | Significantly overvalued |

Use named fair_band/strong_band cells (defaults 1/2) in live formulas; guard missing/nonpositive predictions and undefined SEy before classification. “Significantly” is the prescribed residual-band label, not a proven statistical significance test or investment recommendation. These bands omit leverage and parameter-estimation uncertainty and do not automatically represent 95% prediction intervals. Rank targets by ascending std_residual within the chosen model view; disclose that a combined ranking compares heterogeneous models. RANK.EQ ties create legitimate gaps.

For PE/PBV/PS: predicted multiple × actual corresponding target per-share metric, in quote currency. For EVEBITDA baseline: `(prediction×EBITDA−debt−NCI+cash)/shares`. Any expanded EV definition must be inverted identically. Do not automatically import the associates add-back from comparables. Reconcile preferred/hybrid/per-share claims and dilution where relevant. Negative common equity is flagged, not recommended as a negative stock price. Upside = implied/current−1; current price and fair value use identical units/currency/share class.

## 8. Diagnostics and robustness

Run D1–D10 for every fitted model. Statistical warnings are not workbook QA errors: a correctly calculated bad model may be delivered as non-actionable diagnostic evidence, not as a valid conclusion.

| ID | Test and threshold | Required action |
| --- | --- | --- |
| D1 | Sig_F<0.05 | Otherwise headline: no statistically significant explanatory power; classifications cannot be valuation conclusions |
| D2 | R²<0.20 | Warn weak explanation/wide errors; classifications indicative only; also show adjusted R² |
| D3 | Coefficient p<0.05 | Retain theory-configured nonsignificant variables; list them |
| D4 | Coefficient sign | Compare only defined signs; investigate disagreement, especially when significant; never flip/drop to force theory |
| D5 | abs(pairwise r)>0.80 or VIF>5; severe VIF>10 | Flag instability; severe triggers highest-VIF-drop robustness. Predictions are not guaranteed reliable merely because VIF alone concerns coefficients |
| D6 | Prediction<=0 | Target not valued by that fit |
| D7 | Raw Y beyond Q1±3IQR rule | Run outlier-exclusion robustness; preserve full valid base |
| D8 | abs(std_residual)>3 | Flag/check data; do not exclude merely for unusual valuation |
| D9 | n<10×k | Sample-size warning; separate from hard count minimums |
| D10 | Actual target X outside fitted MIN/MAX | Extrapolation flag and reduced confidence, including target rows retained in master but not in that fit |

Expected signs for the configured base models: PE g+, beta−, payout+; PBV ROE+, beta−, payout+; PS net margin+, payout+, g+. Opposite signs can occur empirically; inspect correlated regressors, definitions and model misspecification, not just one presumed cause.

The supplied sign table omits EVEBITDA despite requiring it. Implementation convention: report g+, tax− and ROIC+ as conditional economic hypotheses (other drivers fixed); DFR has no unambiguous universal sign because tax shields and distress/leverage effects compete, so mark DFR “ambiguous, review” rather than invent a directional pass/fail. Intercepts/dummies also have no forced sign. Document this added sign policy. A newly requested variable/model with an unprovided expected sign requires an explicit sign or “ambiguous/no directional test” setting before that sign test, not a silent guess.

Robustness is triggered independently: (a) remove previously flagged raw-Y outliers, refit; (b) if any VIF>10 remove the highest-VIF X, refit. Keep base coefficients/specification unchanged. Retain base winsor cutoffs for these diagnostic refits so the stated deletion is isolated; if recomputed cutoffs are additionally tested, label separately. Recompute n, k, rank and warnings; show coefficients, R²/adjusted R² and every target's changed classification. If a robustness sample no longer meets minimums, mark it infeasible, not a passed test. Do not silently make the robustness model the base or use it to bypass sample rules.

## 9. Recalculation, QA and stops

Recalculate in Excel or a compatible LibreOffice engine; writing formulas with a Python library does not calculate them. Inspect cached numerical results and formula preservation. Permit only documented unused LINEST #N/A positions; unresolved #REF!, #VALUE!, #DIV/0!, #NAME? or unexpected #N/A blocks verified delivery. Missing inputs should display controlled text/status, not hide arbitrary formula failures.

Independently fit OLS outside Excel using EXACTLY the same row IDs/order, winsorized Y/X, intercept, dummies and column removals. Require relative coefficient and R² differences <1e−6 when the reference is nonzero. For abs(reference)<1e−8 use absolute tolerance 1e−8 instead and report that rule; relative error against zero is undefined. Resolve all discrepancies. Recompute three reproducibly selected predictions by hand-equivalent arithmetic. Reconcile model n/k/df and sums of squares. Do not copy independent coefficients into the formula workbook to make it agree.

Append a Log row after each stage: step, operation, model/target, before/after counts, rule, source and reason. Include route choice, mapping, currency/percent normalization, ratios, exclusions, beta fallbacks, clipping, model fits, selection, recalculation, diagnostics, robustness and report/QA results. Raw row count = model Clean_Data + model Excluded with out-of-scope reasons; target-only Valuation count is requested target count, not n_estimation. Record tests performed, software versions and results.

Stop the affected calculation when required field mapping, fiscal basis or units cannot be resolved; counts still fail after authorized geography expansion; rank/df/variance is invalid; recalculation fails; or the independent check mismatch cannot be resolved. Request only the concrete missing input/decision. Do not deliver an unverified workbook as final; preserve reviewable drafts and explain status. A model-specific failure does not cancel independent valid models or comparables. If a target is eligible for none, retain “Not valued by regression” and direct attention to its independently valid comparable valuation, not a fabricated proxy. User-approved small-sample experiments must be separately labelled departures, never presented as the base passing the original rules.

Prepare human-review schedules before asking for spot checks. Until required review is returned or explicitly waived by the user, label deliverables draft/pending human validation. Above two confirmed errors in the random twenty, repair collection and rerun validation. A waived review must remain disclosed; do not claim it was performed.

## 10. Output contracts and report

Exactly four core regression files, plus the existing shared source/QA logs:

1. DATA_BASE_MSCI.xlsx: full master dataset, raw inputs, membership/classification audit, Checks, Spot_check and logs; separate peer-audit sheets if both methods run.
2. regression_valuation.xlsx: live formula model, A/B/C model blocks, target decisions, diagnostics, charts, triggered robustness and audit/recalculation evidence.
3. valuation_multiples.csv: one row per requested target, including unvalued statuses.
4. valuation_summary.md: report below.

Required CSV columns:

```text
company,ticker,isin,gics_sector,typicality_result,failed_test,primary_regression,chosen_model,adj_r2,actual_multiple,predicted_A,predicted_B,predicted_C,predicted_primary,residual,std_residual,classification,implied_value_per_share,current_price,upside,second_model,second_predicted,third_model,third_predicted,damodaran_predicted,sector_dummy_coef,rationale,flags,source_urls
```

Append damodaran_global, damodaran_western_europe_uk, chosen_model_n, chosen_model_sig_f, valuation_status, price_currency, valuation_date, earnings_basis, region_scope, gics_level and review_status. Set the legacy damodaran_predicted field to the Western Europe & UK prediction (or NA), documenting that mapping; never average benchmarks. Keep each alternative's scope/quality in additional fields or a linked workbook matrix. For a base-sector target, sector_dummy_coef=0 is a reference-category convention, not an estimated coefficient. Retain separate chosen_scope and all A/B/C gaps/rationales.

valuation_summary.md headings, in this order:

1. `# Relative valuation by regression — <sample name>, <date>`
2. `## Headline`: quality, R²/Sig_F, most extreme target residuals only where meaningful, and any D1 failure prominently.
3. `## Data`: route, full/minimum universe, geography, basis/date, raw/used/excluded counts PER model, unit mappings and exclusion table; membership/target additions and human-review status.
4. `## Fitted model`: one subsection per fitted specification, equation including dummies, coefficients/SE/t/p/CI/sign table, R²/adjusted R²/SEy/F/Sig_F/n/df; plain-language unit effects.
5. `## Diagnostics`: D1–D10 for every fit and actions.
6. `## Valuation results (sorted from most undervalued to most overvalued)`: required result table; target/model typicality, chosen/next-two models, A/B/C comparison and explanations. Include actual/predicted multiple, std residual, percentage gap, implied/current price, upside, classification and flags. Do not hide unvalued targets.
7. `## Robustness`: triggered alternatives, coefficients/fit/classification changes, or “Not triggered”.
8. `## Key warnings`: all failed/warning checks and implications.
9. `## Limitations`: incomplete variance explained, market-date specificity, fundamental-growth proxy, pooled-market scope, dependence, model selection across different Y, extrapolation and residual-band limitations; cheap versus prediction is not proof of mispricing.
10. `## Sources`: every used link grouped by company plus common membership/FX/model sources; terminal field/export locators when URLs are unavailable.

Render multiples to 1 decimal, coefficients/SE/t to 3 significant figures, p-values to 3 decimals or <0.001, rates to 1 decimal percent. Report values must match recalculated workbook values before rounding. Do not use a PE-only equation template for other dependent multiples.

## 11. Explicit conflict resolutions and technical references

The following are implementation resolutions, not claims that ambiguous instructions were unambiguous. They settle contradictions and ambiguities inside the Agent Instructions PDFs and rank above those PDFs. Only a lecture overrides them: if a lecture addresses the same point, follow the lecture and record the difference in the Log.

- Beta bound 2.5 follows the detailed cleaning step rather than the earlier 3.0 summary; any override is global and logged. Beta repair precedes missing-X exclusion.
- FY2025 configuration governs the base; separate TTM columns remain. The PE model is not silently linked to the TTM column when configured FY.
- Fundamental growth configuration governs regression; generic analyst-growth schema text does not override it. Clipping payout is only for retention, not the observed payout regressor.
- Source-unit evidence overrides the unsafe median>1 percentage heuristic; transformations are disclosed whole-column/mapped-source conversions.
- Separate raw ratios from winsorized estimation columns resolves “Y=price/EPS” versus “winsorize Y.” Dummy variables remain binary.
- A validity/primary scope is tested per model before adjusted-R² ranking. B/C share each model's market row set; C stays dummy-free even on World.
- Companion method outputs total seven core files under route own_estimation (six under published_damodaran, which has no DATA_BASE_MSCI.xlsx), not one workbook and not a weighted aggregate. Spot-check and peer scoring schedules fit in the shared data workbook.
- Structural constant/rank corrections are logged exceptions; an otherwise nonsignificant or wrong-sign X stays in the base model.
- Interpret band labels cautiously; no claim that ±2SEy is an exact 95% interval. A−C is not mechanically the sector dummy coefficient.
- Method-level stop rules protect affected results, while specific fallback/continue rules permit valid other models. Statistical failure restricts conclusions rather than requiring a significant result to be manufactured.

Technical verification accessed 2026-10-29:

- [Microsoft LINEST documentation](https://support.microsoft.com/en-us/excel/functions/linest-function): coefficient order, collinearity handling and degrees-of-freedom behavior.
- [NIST regression diagnostics](https://itl.nist.gov/div898/software/dataplot/refman1/auxillar/regrdiag.htm): distinction between residual/SE scaling, leverage-aware studentization and influence diagnostics.

These references check implementation details; they do not verify any company inputs or replace the project's explicit selection rules.
