# QA block C — BP.L, 2026-10-30

CURRENT STATUS: see qa_failed_item_recheck.md for the eleven failed-only reassessments. Regression is NOT USABLE, comparable valuation BLOCKED. Original full-block evidence below is historical and retained unchanged; no original passing item was rerun.

Executed once 2026-11-01T14:56:42.846662+00:00

PROVISIONAL / NOT ALL PASS. Comparable method BLOCKED; missing benchmark and hard-gate/bridge evidence require resolution. Do not promote conditional regression output to a verified price target.

### C01 — PASS
Shared data and independence: Scope stated: single target in outputs/<ticker>_<date>/relative/ (orchestrator) or batch in outputs/relative_<date>/. Peer candidates and cross-checks come from the agent's own research (no group workbook). Data route confirmed/reused; full versus minimum universe stated. One valuation/FX date, cutoff and separately named FY/TTM/forward bases recorded.
Evidence: See source_log, inputs, candidate_gates and valuation_summary; published route only.

### C02 — PASS
Shared data and independence: Target list, selected peers and broad regression market remain distinct; internal A–F buckets are not used as unverified GICS sectors.
Evidence: See source_log, inputs, candidate_gates and valuation_summary; published route only.

### C03 — PROVISIONAL
Shared data and independence: Raw financials and class-level market cap reconcile within 2%; price currencies/GBX, reporting currencies, ADRs, share classes and dilution are handled explicitly.
Evidence: Price*shares versus cap <2% all25; GBX/ADR/currencies explicit. EBITDA cross-check difference <1%; EBIT difference14.27% disclosed, full vendor-standardization bridge unresolved. Preference21 carrying proxy not market claim value.

### C04 — PROVISIONAL
Shared data and independence: Field-level sources, membership vintage, exact industry mapping, fallback formulas and all transformations are logged. No unsupported imputation or per-row web-source switching.
Evidence: Sources and fallback formulas retained; missing financials remain NA; remaining membership/hard-gate evidence not certified. Source-level log approved by deviation.

### C05 — FAIL_OPEN
Shared data and independence: >50% benchmark gaps are investigated and resolved; benchmark median/period/industry comparability is verified.
Evidence: No registered ev_ebitda benchmark family or verified matching industry median. Cannot perform/resolve gap test. User-supplied dataset needed; do not use aggregate as median.

### C06 — PASS
Shared data and independence: Human Spot_check status is recorded separately; pending/waived review is never described as performed.
Evidence: EV_spot_checks and report clearly pending, not performed; cached MANIFEST Spot_check remains pending.

### C07 — PASS
Shared data and independence: No DCF-proximity/size-based weighting, generic 30% weight cap, or assumption selection aimed at matching DCF remains in the stage 3 base.
Evidence: See source_log, inputs, candidate_gates and valuation_summary; published route only.

### C08 — BLOCKED
Comparable method: Each target has 10 distinct qualified peers, or 8–9 with an explicit feasible shortfall; below 8 is blocked. Counts/CSV totals reflect actual coverage.
Evidence: Comparable valuation intentionally not released: qualified count0, mandatory evidence missing, no target peer valuation.

### C09 — BLOCKED
Comparable method: All hard filters applied, including developed-market status, financial/holding exclusions, EUR1bn minimum, permitted size band, ownership, restructuring, history and missing metrics.
Evidence: Comparable valuation intentionally not released: qualified count0, mandatory evidence missing, no target peer valuation.

### C10 — BLOCKED
Comparable method: At least 6 Tier 1–2 (8 under the default Tier 3 cap) and 5 Europe-listed peers; Tier 3<=2 unless explicit permitted relaxation to 4, always also <=peer_count−6. No other filter relaxed.
Evidence: Comparable valuation intentionally not released: qualified count0, mandatory evidence missing, no target peer valuation.

### C11 — PASS
Comparable method: 20–30 initial candidate pool, expansions, full rejected/ranked list, score parameters and business-description review are auditable.
Evidence: 24candidates; all numeric-relaxation scores/params in peer_selection; whole-pool web fundamental growth; 11multiple rows with unavailable reasons; required files exist.

### C12 — PASS
Comparable method: Eight score weights sum to one; pool-only 5%/95% clipping, standardization, common metric fallback definitions, missing-dimension renormalization and zero-variance handling are reproducible.
Evidence: 24candidates; all numeric-relaxation scores/params in peer_selection; whole-pool web fundamental growth; 11multiple rows with unavailable reasons; required files exist.

### C13 — PASS
Comparable method: Consensus coverage rule applied before missing-data exclusion; >30% gap switches whole target/pool to fundamental growth, with method labels.
Evidence: 24candidates; all numeric-relaxation scores/params in peer_selection; whole-pool web fundamental growth; 11multiple rows with unavailable reasons; required files exist.

### C14 — PASS
Comparable method: Full required multiple set computed or marked unavailable/NM; positive peer extremes retained. Regression PE cap/clipping are not applied to peer statistics.
Evidence: 24candidates; all numeric-relaxation scores/params in peer_selection; whole-pool web fundamental growth; 11multiple rows with unavailable reasons; required files exist.

### C15 — PASS_SAFETY_ONLY
Comparable method: Every used raw AND scaled multiple has >=6 valid observations. Median/mean/p25/p75 shown; >25% mean–median skew flagged.
Evidence: No unqualified multiple used in valuation. n_valid0/NA main table; candidate-only raw/scaled diagnostics kept separate, positive drivers/PEG units guarded. This is not a completed peer valuation.

### C16 — PASS_SAFETY_ONLY
Comparable method: Raw and adjusted values shown; PEG uses percentage-point growth and matched basis. Positive-driver safeguards and scaled-ratio quartiles applied.
Evidence: No unqualified multiple used in valuation. n_valid0/NA main table; candidate-only raw/scaled diagnostics kept separate, positive drivers/PEG units guarded. This is not a completed peer valuation.

### C17 — BLOCKED
Comparable method: One primary multiple per valued target follows business suitability/ordered fallback. CF and replacement-cost definitions are defensible; limitations explicit.
Evidence: Comparable valuation intentionally not released: qualified count0, mandatory evidence missing, no target peer valuation.

### C18 — BLOCKED
Comparable method: EV-to-equity inverse matches peer numerator, including associates/leases/NCI/other claims once; quote-currency share value and upside reconcile.
Evidence: Comparable valuation intentionally not released: qualified count0, mandatory evidence missing, no target peer valuation.

### C19 — BLOCKED
Comparable method: Three reproducibly random EV calculations checked; all selected ISINs verified and each peer has an economic inclusion reason/source.
Evidence: Comparable valuation intentionally not released: qualified count0, mandatory evidence missing, no target peer valuation.

### C20 — BLOCKED
Comparable method: Peer-set, quartile, multiple and material normalization sensitivities are reported; peer interquartile ranges are not called confidence intervals.
Evidence: Comparable valuation intentionally not released: qualified count0, mandatory evidence missing, no target peer valuation.

### C21 — PASS
Comparable method: comparables.csv, multiples_summary.csv and comparables_report.md exist; scoring/selection/Spot_check audit schedules are provided.
Evidence: 24candidates; all numeric-relaxation scores/params in peer_selection; whole-pool web fundamental growth; 11multiple rows with unavailable reasons; required files exist.

### C22 — N/A_PUBLISHED_ROUTE
Regression method: Master first 18 columns and appended fields match the schema; all targets retained. Complete eligible universe, raw-row count and excluded records reconcile per model.
Evidence: Own-estimation sample/OLS/LINEST/A-B-C diagnostics replaced by published-route requirements below; no fabricated sample.

### C23 — N/A_PUBLISHED_ROUTE
Regression method: Europe/World A ladder and B/C whole-market fallback logged per model. Full/minimum post-clean sample gates respected; losses excluded only from invalid models.
Evidence: Own-estimation sample/OLS/LINEST/A-B-C diagnostics replaced by published-route requirements below; no fabricated sample.

### C24 — PASS
Regression method: Beta replacement uses >2.5/missing/negative rule before final missing-X exclusion; original and sourced replacement logged. Observed payout retained, cap only in growth formula.
Evidence: Target retained; negative PBV not valued; PE distressed-earnings alternative; raw negative beta replaced from resolved beta_europe Oil/Gas (Integrated). Actual payout retained. FY explicitly separate from vendor TTM.

### C25 — PASS
Regression method: Unit conversions follow source metadata; median>1 is only a review trigger. FY and TTM PE not mixed; regression ROE/growth differs explicitly from DCF/peer fields where applicable.
Evidence: Target retained; negative PBV not valued; PE distressed-earnings alternative; raw negative beta replaced from resolved beta_europe Oil/Gas (Integrated). Actual payout retained. FY explicitly separate from vendor TTM.

### C26 — N/A_PUBLISHED_ROUTE
Regression method: Raw ratio formulas retained; estimation Y and continuous X winsorized at 1%/99%, dummies untouched. Raw-IQR flags preserved; B/C use identical model rows/cutoffs.
Evidence: Own-estimation sample/OLS/LINEST/A-B-C diagnostics replaced by published-route requirements below; no fabricated sample.

### C27 — N/A_PUBLISHED_ROUTE
Regression method: PE/PBV/PS/EVEBITDA specs correct; PBV has no extra g. B sector reference and World A/B region coding valid; C has no dummies. ET off unless requested.
Evidence: Own-estimation sample/OLS/LINEST/A-B-C diagnostics replaced by published-route requirements below; no fabricated sample.

### C28 — N/A_PUBLISHED_ROUTE
Regression method: Constant/redundant X handled explicitly; full rank, n, retained k, df and positive SEy verified. Model-specific names/ranges prevent cross-model references.
Evidence: Own-estimation sample/OLS/LINEST/A-B-C diagnostics replaced by published-route requirements below; no fabricated sample.

### C29 — N/A_PUBLISHED_ROUTE
Regression method: Live LINEST, reverse coefficient mapping, SE/t/p/CI/R²/adjusted R²/F/SS/VIF and prediction formulas used; no static ToolPak coefficients or broken external links.
Evidence: Own-estimation sample/OLS/LINEST/A-B-C diagnostics replaced by published-route requirements below; no fabricated sample.

### C30 — PASS
Regression method: Workbook actually recalculated and formulas preserved; only documented unused LINEST error cells remain.
Evidence: All core files exist. LibreOffice recalculation: six predictions match library within1e-9; expected PBV deviation =NA() only.

### C31 — N/A_PUBLISHED_ROUTE
Regression method: Independent OLS on identical transformed rows/design matches at <1e−6 relative difference, with stated near-zero absolute tolerance; three predictions checked.
Evidence: Own-estimation sample/OLS/LINEST/A-B-C diagnostics replaced by published-route requirements below; no fabricated sample.

### C32 — N/A_PUBLISHED_ROUTE
Regression method: Typicality pure-play/ROE-beta-payout-g percentile/valid-A tests recorded per target/model. Routed eligible adjusted-R² ranking and next-two alternatives reproducible.
Evidence: Own-estimation sample/OLS/LINEST/A-B-C diagnostics replaced by published-route requirements below; no fabricated sample.

### C33 — PASS
Regression method: Actual target valuations and clipped estimation diagnostics separate; positive predictions/valid denominators required. Unvalued/excluded targets remain in output.
Evidence: Target retained; negative PBV not valued; PE distressed-earnings alternative; raw negative beta replaced from resolved beta_europe Oil/Gas (Integrated). Actual payout retained. FY explicitly separate from vendor TTM.

### C34 — N/A_PUBLISHED_ROUTE
Regression method: D1–D10 computed with required restrictions. DFR/ambiguous signs not invented; residual bands use exact boundaries and aren't presented as proof of mispricing.
Evidence: Own-estimation sample/OLS/LINEST/A-B-C diagnostics replaced by published-route requirements below; no fabricated sample.

### C35 — N/A_PUBLISHED_ROUTE
Regression method: Triggered outlier/highest-VIF robustness separate from unchanged base; refit infeasibility/changed classifications recorded.
Evidence: Own-estimation sample/OLS/LINEST/A-B-C diagnostics replaced by published-route requirements below; no fabricated sample.

### C36 — N/A_PUBLISHED_ROUTE
Regression method: Same chosen multiple compared across A/B/C; no claim A−C equals a sector dummy. Published Global/Western Europe checks respect equation units and 30% rule or disclose unavailability.
Evidence: Own-estimation sample/OLS/LINEST/A-B-C diagnostics replaced by published-route requirements below; no fabricated sample.

### C37 — N/A_PUBLISHED_ROUTE
Regression method: Spot_check contains targets plus 20 reproducibly random non-target rows; >2 confirmed errors repaired before final use.
Evidence: Own-estimation sample/OLS/LINEST/A-B-C diagnostics replaced by published-route requirements below; no fabricated sample.

### C38 — PASS
Regression method: Four core regression files exist, report headings/values match workbook, one CSV row per requested target, review/model-quality statuses explicit.
Evidence: All core files exist. LibreOffice recalculation: six predictions match library within1e-9; expected PBV deviation =NA() only.

### C39 — PASS
Published-regression route (only when regression_route = published_damodaran): Equation obtained through `datasets.equation_for`; dataset id, vintage, as-of date, region used, match level and warnings recorded. As-of date not after the valuation date; age versus valuation date stated.
Evidence: See source_log, inputs, candidate_gates and valuation_summary; published route only.

### C40 — PASS
Published-regression route (only when regression_route = published_damodaran): Integrity check of the regressions dataset run; every warning (sign anomalies, identical t-statistics, units) addressed; an equation flagged as an anomaly is not used until verified.
Evidence: Dataset check warnings recorded in regression_results; GLOBAL PEG/PBV and EM EV-EBITDA anomalies not used; EUROPE duplicated views agree. No source-flagged equation anomaly used.

### C41 — PASS
Published-regression route (only when regression_route = published_damodaran): Every input follows the FILE's definition (analyst g_eps / g_rev, observed beta, payout >= 0). Any substituted input is labelled `substituted_input` and was approved in standing approvals.
Evidence: See source_log, inputs, candidate_gates and valuation_summary; published route only.

### C42 — FAIL_OPEN
Published-regression route (only when regression_route = published_damodaran): Unit policy handled: both policies computed where DFR or tax rate is used, plausibility check against the sector median recorded, chosen policy justified or `units_unverified` shown.
Evidence: Both policies computed/recalculated. Decimal chosen by standing approval, but sector-median plausibility blocked by absent verified benchmark; conditional estimate only.

### C43 — PASS
Published-regression route (only when regression_route = published_damodaran): No SEy-based output appears: classification, std residual, adjusted R2, p-values, A/B/C and D1-D10 are `n/a_published_route`; deviation and equation R2 shown instead.
Evidence: No SEy-derived classifications. Not-classified label and n/a_published_route fields, equation R2/deviation only; PBV negative unvalued.

### C44 — PASS
Published-regression route (only when regression_route = published_damodaran): Workbook predictions equal `published_regressions.predict` to 1e-9 after recalculation; no PS equation invented; supplementary multiples (PEG, EV/IC, EV/Sales) labelled and not primary.
Evidence: All six predictions, selected and alternative unit policies, match <1e-9 after actual LibreOffice Calc recalculation; no invented PS equation.

### C45 — PASS
Published-regression route (only when regression_route = published_damodaran): Summary states the limitations of section 7 of regression_published_route.md (market-wide scope, low R2, analyst-growth definition, vintage, undocumented EV definition).
Evidence: See source_log, inputs, candidate_gates and valuation_summary; published route only.

### C46 — PASS
Data library (any stage that uses a Damodaran dataset): Dataset chosen by `datasets.resolve`, not by file name; fallback matches justified; vintage not after the valuation date; dataset id and sha256 in `source_log.csv`.
Evidence: See source_log, inputs, candidate_gates and valuation_summary; published route only.

### C47 — PASS
Data library (any stage that uses a Damodaran dataset): Logical-to-actual column mapping recorded; industry mapping uses exact industry names (`industry_row` raised no suggestion error); not-meaningful cells (for example Net CapEx/EBIT(1-t) of Steel and Railroads) not used.
Evidence: beta logical beta_unlevered_cash_corrected maps registered source column; exact Oil/Gas (Integrated), .41; marginal tax24.71% from metadata. Regression resolver mapping/source in JSON.

### C48 — PASS
Data library (any stage that uses a Damodaran dataset): Low-confidence country mappings (`regions.csv`) acknowledged.
Evidence: United Kingdom exact EUROPE route; no low-confidence fallback applied to BP. NonEurope beta absence stays unavailable.

## Failure disposition
No passing QA item rerun. Open failures are data/evidence gates, not arithmetic exceptions; no unsupported numbers inserted to make them pass. User must supply/register the matching industry-median dataset; uniform peer claims and hard-filter evidence need completion. PDF/plaintext are written after this single pass and retain these qualifications.

## Failed-item remediation

2026-11-01T15:32:11+00:00: see qa_failed_item_recheck.md for current findings; original statuses above retained as history. Regression is now NOT USABLE, not a conditional valuation headline. No original passing item rerun.
