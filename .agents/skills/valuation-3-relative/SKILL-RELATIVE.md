---
name: valuation-3-relative
description: Stage 3 relative valuation for European energy-transition companies. Selects 10 fundamental comparables per target and separately builds sector and market regressions with live Excel formulas, diagnostics, and one primary multiple per method. Use after the source data pack; compare with the DCF only after independent relative estimates are complete.
---

# Goal and required reading

Run two distinct methods for the targets in [company universe](../../../methodology/company_universe.md):

1. **Comparable-company valuation:** a selected, ranked peer set per target; peer medians, quartiles and fundamental adjustments.
2. **Regression valuation:** a broad, systematically defined market dataset; A within industry, B market with sector dummies, C market without dummies; four multiple models.

Read this skill, [methodology README](../../../methodology/README.md), the full [comparables procedure](../../../methodology/comparables_procedure.md) and [regression procedure](../../../methodology/regression_procedure.md). Also read [data sources](../../../methodology/data_sources.md), [sector adjustments](../../../methodology/sector_adjustments.md), [QA](../../../methodology/qa_checklist.md) and [report template](../../../methodology/report_template.md). These Markdown files contain the execution rules; no separate Word/PDF instruction file is needed. The professor's lecture notes still rank above them (precedence rules: company-valuation skill); if a lecture contradicts a procedure or one of its recorded corrections of the PDFs, follow the lecture and record the conflict in the method report/Log.

Scope depends on how stage 3 is invoked:
- **Called from the company-valuation orchestrator (default for this agent):** ONE company. Run both methods for that target only, write to outputs/<ticker>_<valuation-date>/relative/, and reuse the dated market assets in cache/market/<valuation-date>/ built by stage 0 (never rebuild them inside a company run; if they are missing, follow the orchestrator rule: ask once and stop the affected work). Under route own_estimation these include DATA_BASE_MSCI.xlsx and the regression market is used in full with all 20 target rows retained; under route published_damodaran no market dataset and no DATA_BASE_MSCI.xlsx exist. Only the requested target is valued.
- **Direct request for the whole assignment:** the full 20-company batch, written to outputs/relative_<valuation-date>/.
- **A subset requested directly:** run that subset in batch layout and state it.
Never label a partial run as 200 peer rows or 20 completed targets. Reuse one dated market dataset across targets. The 20 targets, each target's 10 peers and the regression universe are different sets.

# Execution architecture (efficiency; no method change)
The broad market dataset and the A/B/C regression fits do not depend on the target company. They are built ONCE per valuation date by
stage 0 (`valuation-0-market-refresh`) and stored in `cache/market/<valuation date>/`. A company run (this stage, "3B") reads them.

| Work | Where | Frequency |
|---|---|---|
| Market universe, DATA_BASE_MSCI.xlsx, all regression fits, all-target regression predictions, regression_valuation.xlsx, independent LINEST check | stage 0 | once per date |
| Comparable candidate pool and scoring metrics | read from cached DATA_BASE_MSCI.xlsx (collect fresh data only for candidates outside the cache, e.g. World relaxation) | per target, no re-collection |
| Tiers, hard exclusions, similarity scores, constrained selection, multiple statistics, adjustments | `src/valuation_agent/comparables.py` once tiers/exclusions are decided by you | per target |
| Business-description review, ownership/restructuring checks, ISIN verification, pure-play segment test, primary multiple choice, report text | agent judgement, recorded in the method reports | per target |
| Regression deliverable for the target | copy the cached workbook, extract the target's rows into valuation_multiples.csv, apply the target-level pure-play and typicality routing, write valuation_summary.md | per target |

Rules (route `own_estimation`; under `published_damodaran` no regression cache is needed, and comparable-candidate data collected for one target is cached in
`cache/market/<valuation date>/candidates/<ticker>.csv` and reused by the next target): if `cache/market/<valuation date>/MANIFEST.md` is missing, stop the affected work and ask the user once whether to run stage 0 now (default: in
a separate session); never rebuild the market dataset inside a company run. Do NOT re-estimate the regressions in a company run unless the cached fits are missing
or their manifest hash does not match; if you do, say why. Inherit the cache's human-review status (Spot_check pending = draft). In `standard` mode skip the optional
one-driver peer fit and supplementary multiples; `full` mode includes them. Apply the exclusion screens exactly as written unless the user listed an approved
deviation (for example lazy ownership verification) in memory/standing_approvals.md. Read map: AGENTS.md section 3.

# Shared setup

1. Inventory the target list, source data pack, available terminal exports and the existing DCF. There is no group workbook and none will be supplied: do your own research. Build peer candidates from issuer-named competitors, same-industry screens and your own searches as data_sources.md specifies, and cross-check target figures against the annual reports. Do not ask the user for a group workbook and never reconstruct or invent one. The data route is in memory/standing_approvals.md and in the cache manifest; ask only if both are blank. Terminal access in general is not proof that an export exists. Continue dataset/schema preparation while awaiting a required input.
2. Prefer one terminal export; if unavailable, use the specified single-source web route and reduced regression universe. Follow the stage 3 source rules, which override the generic DCF source flexibility for these datasets.
3. Record valuation date, information cutoff, FX convention, fiscal/TTM/forward basis, common share perimeter, raw and normalized units, route and all thresholds before calculations. Default earnings basis is FY2025; keep separately named TTM and forward series. Never combine them in a statistic or equation.
4. Compute ratios from raw fields. Preserve observations and original sources; apply only the documented fallbacks, with original/replacement values logged. Do not impute other missing data or change sources for one web row.
5. Reconcile market cap, quote units, share classes, EV scope, reporting/trading currencies and target annual-report cross-checks. Organize human spot-check evidence and record its pending/verified status.

# Method 1 — comparables

6. Profile each target; construct 20–30 initial candidates and expand as needed. Use the tier, hard-filter, score and composition rules in comparables_procedure.md. Select exactly 10 peers, or 8–9 only with a documented permitted shortfall. Never use the regression market indiscriminately as a peer list.
7. Compute the complete prescribed multiple set with aligned definitions. Keep positive extremes in peer statistics; exclude only unavailable/not-meaningful observations under the rules. Require at least 6 valid observations separately for each raw or scaled multiple used.
8. Show median, mean, p25, p75, unadjusted and permitted fundamental-adjusted values. Select one business-appropriate primary multiple, with the rest as cross-checks; no DCF-dependent weights. Apply the matched EV-to-equity bridge and convert to the target's quote currency.

# Method 2 — regressions

**Route first.** Read `regression_route` in memory/standing_approvals.md. `published_damodaran`: skip steps 9-13 below and follow
[regression_published_route.md](../../../methodology/regression_published_route.md) (equations from the data library via `datasets.equation_for`; no market dataset, no
estimation, no residual bands; unit policy and input definitions per that file). `own_estimation`: steps 9-13 as written. If the field is `TBD`, ask once and write the answer back.

9. Build DATA_BASE_MSCI.xlsx once from the full permitted market; retain all target rows. Do not use the hand-selected peer lists as the estimation sample. Apply model-specific eligibility, beta replacement, 1%/99% continuous-variable winsorization and count gates.
10. Estimate PE, PBV, PS and EVEBITDA in A, B and C wherever valid. B and C must share the same model-specific market rows and transformed continuous data. Follow the Europe-to-World ladder and dummy coding; C never has sector or region dummies.
11. Use live Excel formulas for transformations, OLS statistics, diagnostics and valuations. Extract LINEST coefficients in reverse X order; recalculate and independently check the same fitted design outside Excel. In this route never substitute a published Damodaran equation for estimating these models (the published route is a separate, user-approved route).
12. For each target/model, apply the pure-play, percentile and sector-model-validity tests to select A or B. Rank eligible routed models by adjusted R² under the project's selection rule; output one chosen prediction and the next two eligible alternatives. Show A/B/C predictions for the same chosen multiple and explain differences without claiming they prove causality.
13. Apply residual-band classifications and D1–D10 diagnostics. Keep failed/low-quality models visible but restrict conclusions as required. Run triggered outlier/VIF robustness models separately. Benchmark matching equations against Damodaran; unavailable matching equations remain unavailable.

# Reconciliation and delivery

14. Report comparables and regression point estimates separately, then compare with the existing DCF and current price. Explain differences in earnings basis, universe, margin/growth/risk, EV adjustments and market conditions. Never choose peers, models, multiples or weights because they move a result toward DCF.
15. Preserve peer-set, quartile and multiple sensitivities, distribution/football-field charts and industry discussion from the former skill. Do not average all multiples or rank higher valuations merely because the target is large. A combined final recommendation requires an explicit stage 4 rationale; it does not overwrite either independent method.
16. Run the stage 3 QA checklist (block C, once; items already verified at stage 0 are cited from the cache MANIFEST, not repeated). After delivery update run_state.json, write memory/companies/<ticker>.md and memory/sectors/ entries (peer-set rationale, primary multiple, quirks), append timings to memory/run_log.csv, post the short message and end the session. Stop only the affected work when an input/method is blocked; complete independent work. Do not mark an unrecalculated workbook, unresolved data failure or pending required human review as final/verified.

# Deliverables

Single-target (orchestrator) run: outputs/<ticker>_<valuation-date>/relative/. Batch/subset run: outputs/relative_<valuation-date>/ (repository-relative). Same file names in both layouts (seven under route own_estimation, six under published_damodaran). Preserve stage 1/2 files.

**Comparables — three core files:** comparables.csv, multiples_summary.csv, comparables_report.md.

**Regression — four core files:** DATA_BASE_MSCI.xlsx, regression_valuation.xlsx, valuation_multiples.csv, valuation_summary.md (route `published_damodaran`: three files,
no DATA_BASE_MSCI.xlsx, contents per regression_published_route.md section 7).

The procedures specify exact schemas, workbook sheets, diagnostics and report headings. Put peer-selection audit/Spot_check schedules in DATA_BASE_MSCI.xlsx when both methods run under route own_estimation, separated from regression input (under published_damodaran use the labelled comparables_audit.xlsx, which is not an additional core file); put charts in workbooks. Continue the shared source_log.csv and qa_results.md. These shared audit files are not additional valuation-method outputs. For a comparables-only run, an explicitly labelled comparables_audit.xlsx is permitted to satisfy the audit-sheet requirement; do not create fake regression outputs.

The old relative_model.xlsx, weights_table and relative_decisions.md contract is superseded everywhere in the repository (orchestrator, stage 4, report template, QA): all decisions now live in the method reports and workbook Log. No weights_table, DCF-proximity/size weighting or 30% cap applies. Stage 4 may build its own reasoned synthesis from the preserved estimates (see stage 4). Cite only opened evidence; distinguish assignment thresholds from general valuation theory. Test material calculations and workbook/model equivalence when executing valuations, and report actual results rather than claiming unrun checks.
