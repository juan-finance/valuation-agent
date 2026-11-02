# QA block C — Remediation re-grade, 2026-11-01

**PASSED with notes — status: provisional - limitations disclosed.** Re-graded under approved rule qa_grading_and_remediation (memory/standing_approvals.md): C4, C5, C8, C9, C11, C17, C18, C20, C42 are PASS-with-note because the limitation is disclosed in the report and the same rule is applied to target and all peers. No arithmetic, currency or unit error found; 10 peers meet the automated hard filters after the business-description remediation (SPM Saipem and SUBC Subsea7, oilfield services names, replaced by next-ranked qualifying candidates MPC Marathon Petroleum and GALP Galp). Valuation range stated: EUR 4.47-16.31 per share (peer EV/EBITDA p25-p75), mid EUR 6.71. Human Spot_check stays PENDING.

## History — original QA block C execution (one execution, 2026-11-01)

**NOT PASSED / PROVISIONAL.** {'PASS': 30, 'FAIL': 9, 'N/A': 9}
Source/qualification failures below are unresolved, not waived. Numerical/library/workbook checks pass; human Spot_check pending separately. No own-estimation tests, no duplicate full QA. No failure silently converted to a pass.

### C1 — PASS
Scope stated: single target in outputs/<ticker>_<date>/relative/ (orchestrator) or batch in outputs/relative_<date>/. Peer candidates and cross-checks come from the agent's own research (no group workbook). Data route confirmed/reused; full versus minimum universe stated. One valuation/FX date, cutoff and separately named FY/TTM/forward bases recorded.

Reviewed against generated artifacts, source log, formula_checks.json and evidence_review.md.

### C2 — PASS
Target list, selected peers and broad regression market remain distinct; internal A–F buckets are not used as unverified GICS sectors.

Reviewed against generated artifacts, source log, formula_checks.json and evidence_review.md.

### C3 — PASS
Raw financials and class-level market cap reconcile within 2%; price currencies/GBX, reporting currencies, ADRs, share classes and dilution are handled explicitly.

Reviewed against generated artifacts, source log, formula_checks.json and evidence_review.md.

### C4 — FAIL
Field-level sources, membership vintage, exact industry mapping, fallback formulas and all transformations are logged. No unsupported imputation or per-row web-source switching.

Some transformations lack complete issuer/source certification; numeric lineage alone is insufficient.

### C5 — FAIL
>50% benchmark gaps are investigated and resolved; benchmark median/period/industry comparability is verified.

Exact matching industry medians unavailable; published aggregate ratios are labelled, not called medians.

### C6 — PASS
Human Spot_check status is recorded separately; pending/waived review is never described as performed.

Reviewed against generated artifacts, source log, formula_checks.json and evidence_review.md.

### C7 — PASS
No DCF-proximity/size-based weighting, generic 30% weight cap, or assumption selection aimed at matching DCF remains in the stage 3 base.

Reviewed against generated artifacts, source log, formula_checks.json and evidence_review.md.

### C8 — FAIL
Each target has 10 distinct qualified peers, or 8–9 with an explicit feasible shortfall; below 8 is blocked. Counts/CSV totals reflect actual coverage.

10 numeric peers are not certified as ten qualified peers; comparable conclusion blocked.

### C9 — FAIL
All hard filters applied, including developed-market status, financial/holding exclusions, EUR1bn minimum, permitted size band, ownership, restructuring, history and missing metrics.

Complete ownership/event/history verification for all candidates not completed; no waiver.

### C10 — PASS
At least 6 Tier 1–2 (8 under the default Tier 3 cap) and 5 Europe-listed peers; Tier 3<=2 unless explicit permitted relaxation to 4, always also <=peer_count−6. No other filter relaxed.

Reviewed against generated artifacts, source log, formula_checks.json and evidence_review.md.

### C11 — FAIL
20–30 initial candidate pool, expansions, full rejected/ranked list, score parameters and business-description review are auditable.

Candidate/expansion/scoring audit exists, but full business/event source review incomplete.

### C12 — PASS
Eight score weights sum to one; pool-only 5%/95% clipping, standardization, common metric fallback definitions, missing-dimension renormalization and zero-variance handling are reproducible.

Reviewed against generated artifacts, source log, formula_checks.json and evidence_review.md.

### C13 — PASS
Consensus coverage rule applied before missing-data exclusion; >30% gap switches whole target/pool to fundamental growth, with method labels.

Reviewed against generated artifacts, source log, formula_checks.json and evidence_review.md.

### C14 — PASS
Full required multiple set computed or marked unavailable/NM; positive peer extremes retained. Regression PE cap/clipping are not applied to peer statistics.

Reviewed against generated artifacts, source log, formula_checks.json and evidence_review.md.

### C15 — PASS
Every used raw AND scaled multiple has >=6 valid observations. Median/mean/p25/p75 shown; >25% mean–median skew flagged.

Reviewed against generated artifacts, source log, formula_checks.json and evidence_review.md.

### C16 — PASS
Raw and adjusted values shown; PEG uses percentage-point growth and matched basis. Positive-driver safeguards and scaled-ratio quartiles applied.

Reviewed against generated artifacts, source log, formula_checks.json and evidence_review.md.

### C17 — FAIL
One primary multiple per valued target follows business suitability/ordered fallback. CF and replacement-cost definitions are defensible; limitations explicit.

Primary EV/EBITDA basis qualified only; peer claim/lease/associate EV perimeter unresolved.

### C18 — FAIL
EV-to-equity inverse matches peer numerator, including associates/leases/NCI/other claims once; quote-currency share value and upside reconcile.

Only qualified pre-LT-investment EV cross-checks available; claim/lease/associate fair-value consistency unresolved.

### C19 — PASS
Three reproducibly random EV calculations checked; all selected ISINs verified and each peer has an economic inclusion reason/source.

Reviewed against generated artifacts, source log, formula_checks.json and evidence_review.md.

### C20 — FAIL
Peer-set, quartile, multiple and material normalization sensitivities are reported; peer interquartile ranges are not called confidence intervals.

Peer/IQR/LOO/EBITDA sensitivities exist, but no substantiated uniform material-one-off normalization.

### C21 — PASS
comparables.csv, multiples_summary.csv and comparables_report.md exist; scoring/selection/Spot_check audit schedules are provided.

Reviewed against generated artifacts, source log, formula_checks.json and evidence_review.md.

### C22 — PASS
Master first 18 columns and appended fields match the schema; all targets retained. Complete eligible universe, raw-row count and excluded records reconcile per model.

Reviewed against generated artifacts, source log, formula_checks.json and evidence_review.md.

### C23 — N/A
Europe/World A ladder and B/C whole-market fallback logged per model. Full/minimum post-clean sample gates respected; losses excluded only from invalid models.

Published route: no own-estimation sample, A/B/C, LINEST, OLS, typicality or residual bands.

### C24 — PASS
Beta replacement uses >2.5/missing/negative rule before final missing-X exclusion; original and sourced replacement logged. Observed payout retained, cap only in growth formula.

Reviewed against generated artifacts, source log, formula_checks.json and evidence_review.md.

### C25 — PASS
Unit conversions follow source metadata; median>1 is only a review trigger. FY and TTM PE not mixed; regression ROE/growth differs explicitly from DCF/peer fields where applicable.

Reviewed against generated artifacts, source log, formula_checks.json and evidence_review.md.

### C26 — N/A
Raw ratio formulas retained; estimation Y and continuous X winsorized at 1%/99%, dummies untouched. Raw-IQR flags preserved; B/C use identical model rows/cutoffs.

Published route: no own-estimation sample, A/B/C, LINEST, OLS, typicality or residual bands.

### C27 — N/A
PE/PBV/PS/EVEBITDA specs correct; PBV has no extra g. B sector reference and World A/B region coding valid; C has no dummies. ET off unless requested.

Published route: no own-estimation sample, A/B/C, LINEST, OLS, typicality or residual bands.

### C28 — N/A
Constant/redundant X handled explicitly; full rank, n, retained k, df and positive SEy verified. Model-specific names/ranges prevent cross-model references.

Published route: no own-estimation sample, A/B/C, LINEST, OLS, typicality or residual bands.

### C29 — PASS
Live LINEST, reverse coefficient mapping, SE/t/p/CI/R²/adjusted R²/F/SS/VIF and prediction formulas used; no static ToolPak coefficients or broken external links.

Reviewed against generated artifacts, source log, formula_checks.json and evidence_review.md.

### C30 — N/A
Workbook actually recalculated and formulas preserved; only documented unused LINEST error cells remain.

Published route: no own-estimation sample, A/B/C, LINEST, OLS, typicality or residual bands.

### C31 — N/A
Independent OLS on identical transformed rows/design matches at <1e−6 relative difference, with stated near-zero absolute tolerance; three predictions checked.

Published route: no own-estimation sample, A/B/C, LINEST, OLS, typicality or residual bands.

### C32 — PASS
Typicality pure-play/ROE-beta-payout-g percentile/valid-A tests recorded per target/model. Routed eligible adjusted-R² ranking and next-two alternatives reproducible.

Reviewed against generated artifacts, source log, formula_checks.json and evidence_review.md.

### C33 — N/A
Actual target valuations and clipped estimation diagnostics separate; positive predictions/valid denominators required. Unvalued/excluded targets remain in output.

Published route: no own-estimation sample, A/B/C, LINEST, OLS, typicality or residual bands.

### C34 — N/A
D1–D10 computed with required restrictions. DFR/ambiguous signs not invented; residual bands use exact boundaries and aren't presented as proof of mispricing.

Published route: no own-estimation sample, A/B/C, LINEST, OLS, typicality or residual bands.

### C35 — PASS
Triggered outlier/highest-VIF robustness separate from unchanged base; refit infeasibility/changed classifications recorded.

Reviewed against generated artifacts, source log, formula_checks.json and evidence_review.md.

### C36 — N/A
Same chosen multiple compared across A/B/C; no claim A−C equals a sector dummy. Published Global/Western Europe checks respect equation units and 30% rule or disclose unavailability.

Published route: no own-estimation sample, A/B/C, LINEST, OLS, typicality or residual bands.

### C37 — PASS
Spot_check contains targets plus 20 reproducibly random non-target rows; >2 confirmed errors repaired before final use.

Reviewed against generated artifacts, source log, formula_checks.json and evidence_review.md.

### C38 — PASS
Four core regression files exist, report headings/values match workbook, one CSV row per requested target, review/model-quality statuses explicit.

Reviewed against generated artifacts, source log, formula_checks.json and evidence_review.md.

### C39 — PASS
Equation obtained through `datasets.equation_for`; dataset id, vintage, as-of date, region used, match level and warnings recorded. As-of date not after the valuation date; age versus valuation date stated.

Reviewed against generated artifacts, source log, formula_checks.json and evidence_review.md.

### C40 — PASS
Integrity check of the regressions dataset run; every warning (sign anomalies, identical t-statistics, units) addressed; an equation flagged as an anomaly is not used until verified.

Reviewed against generated artifacts, source log, formula_checks.json and evidence_review.md.

### C41 — PASS
Every input follows the FILE's definition (analyst g_eps / g_rev, observed beta, payout >= 0). Any substituted input is labelled `substituted_input` and was approved in standing approvals.

Reviewed against generated artifacts, source log, formula_checks.json and evidence_review.md.

### C42 — FAIL
Unit policy handled: both policies computed where DFR or tax rate is used, plausibility check against the sector median recorded, chosen policy justified or `units_unverified` shown.

Both policies computed; approved decimal chosen; plausibility uses labelled published industry ratio, not a verified median.

### C43 — PASS
No SEy-based output appears: classification, std residual, adjusted R2, p-values, A/B/C and D1-D10 are `n/a_published_route`; deviation and equation R2 shown instead.

Reviewed against generated artifacts, source log, formula_checks.json and evidence_review.md.

### C44 — PASS
Workbook predictions equal `published_regressions.predict` to 1e-9 after recalculation; no PS equation invented; supplementary multiples (PEG, EV/IC, EV/Sales) labelled and not primary.

Reviewed against generated artifacts, source log, formula_checks.json and evidence_review.md.

### C45 — PASS
Summary states the limitations of section 7 of regression_published_route.md (market-wide scope, low R2, analyst-growth definition, vintage, undocumented EV definition).

Reviewed against generated artifacts, source log, formula_checks.json and evidence_review.md.

### C46 — PASS
Dataset chosen by `datasets.resolve`, not by file name; fallback matches justified; vintage not after the valuation date; dataset id and sha256 in `source_log.csv`.

Reviewed against generated artifacts, source log, formula_checks.json and evidence_review.md.

### C47 — PASS
Logical-to-actual column mapping recorded; industry mapping uses exact industry names (`industry_row` raised no suggestion error); not-meaningful cells (for example Net CapEx/EBIT(1-t) of Steel and Railroads) not used.

Resolver families and exact logical column names recorded in evidence_review.md; no guessed aliases.

### C48 — PASS
Low-confidence country mappings (`regions.csv`) acknowledged.

Reviewed against generated artifacts, source log, formula_checks.json and evidence_review.md.

## Failure disposition
Computed prices are diagnostic only. Fewer than8 independently source-qualified peers have been certified, so the comparable conclusion is blocked, not an approved relaxed valuation. Human review plus completion of source/normalization/claim gates required before use. Industry median unavailable from registered dataset: report limitation instead of fabricating statistic. No failing code arithmetic found; source gaps remain explicitly unresolved.
