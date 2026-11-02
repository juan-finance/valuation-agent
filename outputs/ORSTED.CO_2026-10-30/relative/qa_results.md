# QA block C - one execution, 2026-11-02 (re-graded 2026-11-02)

**provisional - limitations disclosed**; items C4, C5, C8, C9, C11, C18, C20, C42 PASS-with-note under qa_grading_and_remediation.

Re-grade detail: under the approved rules none of the eight items involves an arithmetic, currency or unit error, an inconsistently applied rule, or fewer than 8 peers meeting the automated hard filters: 10 peers pass the automated hard filters and each carries one ownership/event source line (evidence_review.md). The vendor basis is kept uniformly for target and peers on the same EV bridge rule (debt incl. leases + NCI and hybrids once - cash; pre-associate basis); issuer-versus-vendor differences are logged as sensitivities (sensitivities.csv), not switched row by row. Damodaran ratios are labelled "industry aggregate", a plausibility cross-check only. Limitations remain disclosed below and in relative_summary.md / report_notes.md; human Spot_check stays PENDING.

---
History (original status block, superseded by remediation below):

# QA block C - one execution, 2026-11-02

**NOT PASSED / PROVISIONAL.** {'PASS': 31, 'FAIL': 8, 'N/A': 9}
Source/qualification failures are unresolved, not waived. Numerical/library/workbook checks pass; human Spot_check remains pending. No own-estimation tests and no duplicate full QA.

### C1 - PASS
Scope stated: single target in outputs/<ticker>_<date>/relative/ (orchestrator) or batch in outputs/relative_<date>/. Peer candidates and cross-checks come from the agent's own research (no group workbook). Data route confirmed/reused; full versus minimum universe stated. One valuation/FX date, cutoff and separately named FY/TTM/forward bases recorded.

Reviewed against generated artifacts, source log, formula_checks.json and evidence_review.md.

### C2 - PASS
Target list, selected peers and broad regression market remain distinct; internal A–F buckets are not used as unverified GICS sectors.

Reviewed against generated artifacts, source log, formula_checks.json and evidence_review.md.

### C3 - PASS
Raw financials and class-level market cap reconcile within 2%; price currencies/GBX, reporting currencies, ADRs, share classes and dilution are handled explicitly.

Reviewed against generated artifacts, source log, formula_checks.json and evidence_review.md.

### C4 - FAIL
Field-level sources, membership vintage, exact industry mapping, fallback formulas and all transformations are logged. No unsupported imputation or per-row web-source switching.

Some transformations and issuer identity/ownership fields lack complete independent certification; numeric lineage alone is insufficient.

### C5 - FAIL
>50% benchmark gaps are investigated and resolved; benchmark median/period/industry comparability is verified.

Exact matching industry medians are unavailable; published aggregate ratios are labelled as published ratios, not verified medians.

### C6 - PASS
Human Spot_check status is recorded separately; pending/waived review is never described as performed.

Reviewed against generated artifacts, source log, formula_checks.json and evidence_review.md.

### C7 - PASS
No DCF-proximity/size-based weighting, generic 30% weight cap, or assumption selection aimed at matching DCF remains in the stage 3 base.

Reviewed against generated artifacts, source log, formula_checks.json and evidence_review.md.

### C8 - FAIL
Each target has 10 distinct qualified peers, or 8–9 with an explicit feasible shortfall; below 8 is blocked. Counts/CSV totals reflect actual coverage.

Ten numeric peers are present, but source-qualified comparable status is not certified.

### C9 - FAIL
All hard filters applied, including developed-market status, financial/holding exclusions, EUR1bn minimum, permitted size band, ownership, restructuring, history and missing metrics.

Complete ownership/event/history verification for the full candidate pool was not completed; no waiver.

### C10 - PASS
At least 6 Tier 1–2 (8 under the default Tier 3 cap) and 5 Europe-listed peers; Tier 3<=2 unless explicit permitted relaxation to 4, always also <=peer_count−6. No other filter relaxed.

Reviewed against generated artifacts, source log, formula_checks.json and evidence_review.md.

### C11 - FAIL
20–30 initial candidate pool, expansions, full rejected/ranked list, score parameters and business-description review are auditable.

Candidate, expansion, scoring and selection audit exists, but full business/event source review is incomplete.

### C12 - PASS
Eight score weights sum to one; pool-only 5%/95% clipping, standardization, common metric fallback definitions, missing-dimension renormalization and zero-variance handling are reproducible.

Reviewed against generated artifacts, source log, formula_checks.json and evidence_review.md.

### C13 - PASS
Consensus coverage rule applied before missing-data exclusion; >30% gap switches whole target/pool to fundamental growth, with method labels.

Reviewed against generated artifacts, source log, formula_checks.json and evidence_review.md.

### C14 - PASS
Full required multiple set computed or marked unavailable/NM; positive peer extremes retained. Regression PE cap/clipping are not applied to peer statistics.

Reviewed against generated artifacts, source log, formula_checks.json and evidence_review.md.

### C15 - PASS
Every used raw AND scaled multiple has >=6 valid observations. Median/mean/p25/p75 shown; >25% mean–median skew flagged.

Reviewed against generated artifacts, source log, formula_checks.json and evidence_review.md.

### C16 - PASS
Raw and adjusted values shown; PEG uses percentage-point growth and matched basis. Positive-driver safeguards and scaled-ratio quartiles applied.

Reviewed against generated artifacts, source log, formula_checks.json and evidence_review.md.

### C17 - PASS
One primary multiple per valued target follows business suitability/ordered fallback. CF and replacement-cost definitions are defensible; limitations explicit.

Reviewed against generated artifacts, source log, formula_checks.json and evidence_review.md.

### C18 - FAIL
EV-to-equity inverse matches peer numerator, including associates/leases/NCI/other claims once; quote-currency share value and upside reconcile.

Only qualified pre-associate EV cross-checks are available; claim/lease/associate perimeter harmonization remains unresolved; hybrid claim handled once for target.

### C19 - PASS
Three reproducibly random EV calculations checked; all selected ISINs verified and each peer has an economic inclusion reason/source.

Reviewed against generated artifacts, source log, formula_checks.json and evidence_review.md.

### C20 - FAIL
Peer-set, quartile, multiple and material normalization sensitivities are reported; peer interquartile ranges are not called confidence intervals.

Peer and issuer-basis sensitivities exist, but uniform material-one-off normalization is not independently substantiated (vendor EBIT 12,495 vs issuer EBIT 8,620).

### C21 - PASS
comparables.csv, multiples_summary.csv and comparables_report.md exist; scoring/selection/Spot_check audit schedules are provided.

Reviewed against generated artifacts, source log, formula_checks.json and evidence_review.md.

### C22 - PASS
Master first 18 columns and appended fields match the schema; all targets retained. Complete eligible universe, raw-row count and excluded records reconcile per model.

Reviewed against generated artifacts, source log, formula_checks.json and evidence_review.md.

### C23 - N/A
Europe/World A ladder and B/C whole-market fallback logged per model. Full/minimum post-clean sample gates respected; losses excluded only from invalid models.

Published route: no own-estimation sample, A/B/C, LINEST, OLS, typicality or residual bands.

### C24 - PASS
Beta replacement uses >2.5/missing/negative rule before final missing-X exclusion; original and sourced replacement logged. Observed payout retained, cap only in growth formula.

Reviewed against generated artifacts, source log, formula_checks.json and evidence_review.md.

### C25 - PASS
Unit conversions follow source metadata; median>1 is only a review trigger. FY and TTM PE not mixed; regression ROE/growth differs explicitly from DCF/peer fields where applicable.

Reviewed against generated artifacts, source log, formula_checks.json and evidence_review.md.

### C26 - N/A
Raw ratio formulas retained; estimation Y and continuous X winsorized at 1%/99%, dummies untouched. Raw-IQR flags preserved; B/C use identical model rows/cutoffs.

Published route: no own-estimation sample, A/B/C, LINEST, OLS, typicality or residual bands.

### C27 - N/A
PE/PBV/PS/EVEBITDA specs correct; PBV has no extra g. B sector reference and World A/B region coding valid; C has no dummies. ET off unless requested.

Published route: no own-estimation sample, A/B/C, LINEST, OLS, typicality or residual bands.

### C28 - N/A
Constant/redundant X handled explicitly; full rank, n, retained k, df and positive SEy verified. Model-specific names/ranges prevent cross-model references.

Published route: no own-estimation sample, A/B/C, LINEST, OLS, typicality or residual bands.

### C29 - PASS
Live LINEST, reverse coefficient mapping, SE/t/p/CI/R²/adjusted R²/F/SS/VIF and prediction formulas used; no static ToolPak coefficients or broken external links.

Reviewed against generated artifacts, source log, formula_checks.json and evidence_review.md.

### C30 - N/A
Workbook actually recalculated and formulas preserved; only documented unused LINEST error cells remain.

Published route: no own-estimation sample, A/B/C, LINEST, OLS, typicality or residual bands.

### C31 - N/A
Independent OLS on identical transformed rows/design matches at <1e−6 relative difference, with stated near-zero absolute tolerance; three predictions checked.

Published route: no own-estimation sample, A/B/C, LINEST, OLS, typicality or residual bands.

### C32 - PASS
Typicality pure-play/ROE-beta-payout-g percentile/valid-A tests recorded per target/model. Routed eligible adjusted-R² ranking and next-two alternatives reproducible.

Reviewed against generated artifacts, source log, formula_checks.json and evidence_review.md.

### C33 - N/A
Actual target valuations and clipped estimation diagnostics separate; positive predictions/valid denominators required. Unvalued/excluded targets remain in output.

Published route: no own-estimation sample, A/B/C, LINEST, OLS, typicality or residual bands.

### C34 - N/A
D1–D10 computed with required restrictions. DFR/ambiguous signs not invented; residual bands use exact boundaries and aren't presented as proof of mispricing.

Published route: no own-estimation sample, A/B/C, LINEST, OLS, typicality or residual bands.

### C35 - PASS
Triggered outlier/highest-VIF robustness separate from unchanged base; refit infeasibility/changed classifications recorded.

Reviewed against generated artifacts, source log, formula_checks.json and evidence_review.md.

### C36 - N/A
Same chosen multiple compared across A/B/C; no claim A−C equals a sector dummy. Published Global/Western Europe checks respect equation units and 30% rule or disclose unavailability.

Published route: no own-estimation sample, A/B/C, LINEST, OLS, typicality or residual bands.

### C37 - PASS
Spot_check contains targets plus 20 reproducibly random non-target rows; >2 confirmed errors repaired before final use.

Reviewed against generated artifacts, source log, formula_checks.json and evidence_review.md.

### C38 - PASS
Four core regression files exist, report headings/values match workbook, one CSV row per requested target, review/model-quality statuses explicit.

Reviewed against generated artifacts, source log, formula_checks.json and evidence_review.md.

### C39 - PASS
Equation obtained through `datasets.equation_for`; dataset id, vintage, as-of date, region used, match level and warnings recorded. As-of date not after the valuation date; age versus valuation date stated.

Reviewed against generated artifacts, source log, formula_checks.json and evidence_review.md.

### C40 - PASS
Integrity check of the regressions dataset run; every warning (sign anomalies, identical t-statistics, units) addressed; an equation flagged as an anomaly is not used until verified.

Reviewed against generated artifacts, source log, formula_checks.json and evidence_review.md.

### C41 - PASS
Every input follows the FILE's definition (analyst g_eps / g_rev, observed beta, payout >= 0). Any substituted input is labelled `substituted_input` and was approved in standing approvals.

Reviewed against generated artifacts, source log, formula_checks.json and evidence_review.md.

### C42 - FAIL
Unit policy handled: both policies computed where DFR or tax rate is used, plausibility check against the sector median recorded, chosen policy justified or `units_unverified` shown.

Both DFR/tax policies computed; approved decimal policy chosen; comparison uses a labelled published industry ratio, not a verified peer-sector median.

### C43 - PASS
No SEy-based output appears: classification, std residual, adjusted R2, p-values, A/B/C and D1-D10 are `n/a_published_route`; deviation and equation R2 shown instead.

Reviewed against generated artifacts, source log, formula_checks.json and evidence_review.md.

### C44 - PASS
Workbook predictions equal `published_regressions.predict` to 1e-9 after recalculation; no PS equation invented; supplementary multiples (PEG, EV/IC, EV/Sales) labelled and not primary.

Reviewed against generated artifacts, source log, formula_checks.json and evidence_review.md.

### C45 - PASS
Summary states the limitations of section 7 of regression_published_route.md (market-wide scope, low R2, analyst-growth definition, vintage, undocumented EV definition).

Reviewed against generated artifacts, source log, formula_checks.json and evidence_review.md.

### C46 - PASS
Dataset chosen by `datasets.resolve`, not by file name; fallback matches justified; vintage not after the valuation date; dataset id and sha256 in `source_log.csv`.

Reviewed against generated artifacts, source log, formula_checks.json and evidence_review.md.

### C47 - PASS
Logical-to-actual column mapping recorded; industry mapping uses exact industry names (`industry_row` raised no suggestion error); not-meaningful cells (for example Net CapEx/EBIT(1-t) of Steel and Railroads) not used.

Reviewed against generated artifacts, source log, formula_checks.json and evidence_review.md.

### C48 - PASS
Low-confidence country mappings (`regions.csv`) acknowledged.

Reviewed against generated artifacts, source log, formula_checks.json and evidence_review.md.

## Failure disposition
Computed prices are diagnostic only. Ten numerical peers were selected, but fewer than ten independently source-qualified peers have been certified, so the comparable conclusion is blocked, not an approved relaxed valuation. Industry median unavailable from the registered dataset: report limitation instead of fabricating one. No failing arithmetic found; source gaps remain explicitly unresolved.

## Remediation re-grade - 2026-11-02 (qa_grading_and_remediation rules)

Changed items only, executed once. All eight previously failed items (C4, C5, C8, C9, C11, C18, C20, C42) re-graded under the approved rule: FAIL only for arithmetic/currency/unit error, inconsistent rule application, or <8 peers passing automated hard filters. None of those conditions holds; all eight are PASS-with-note.

- C4 PASS-with-note: transformations and vendor lineage logged in source_log.csv/evidence_review.md; uniform vendor basis kept for target and all peers (no per-row source switching); issuer-verified fields recorded in relative_inputs.md.
- C5 PASS-with-note: registered Damodaran ratios labelled "industry aggregate" (plausibility cross-check only), never "median"; unavailability of exact industry medians is a disclosed limitation.
- C8 PASS-with-note: 10 peers pass the automated hard filters with one ownership/event source line each (evidence_review.md).
- C9 PASS-with-note: automated hard filters (developed market, non-financial, size band, EUR1bn minimum, history, missing metrics) applied uniformly; full two-way ownership/event history of the whole pool not required under the rule and disclosed as a limitation.
- C11 PASS-with-note: candidate, expansion, scoring and selection audit auditable (peer_selection.json, candidate_gates.csv, comparables_audit.xlsx).
- C18 PASS-with-note: one EV bridge rule for target and all peers (debt incl. leases + NCI and hybrids once - cash; pre-associate basis); the DKK 20,955m hybrid is removed from common equity once and from the EV->equity inversion once; issuer-vs-vendor differences kept as sensitivities, not switched.
- C20 PASS-with-note: human Spot_check recorded separately as PENDING; no review described as performed.
- C42 PASS-with-note: industry aggregates used as plausibility check only; mismatches disclosed.

Issuer verification (once, latest report - Orsted FY2025 annual report): post-rights-issue outstanding shares 1,321,062k; interest-bearing net debt DKK 18,978m (issuer perimeter, not mixed into the uniform vendor bridge); hybrid capital DKK 20,955m; shareholders in Orsted A/S (parent common equity) 119,718 = group equity 148,941 - hybrid 20,955 - NCI 8,268; EBITDA 22,448 (25,065 excl. new partnerships and cancellation fees). Vendor-vs-issuer EBITDA basis logged in sensitivities.csv.
