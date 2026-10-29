---
name: valuation-3-relative
description: Stage 3 relative valuation for European energy-transition companies. Selects 20 fundamental comparables per target and separately builds sector and market regressions with live Excel formulas, diagnostics, and one primary multiple per method. Use after the source data pack; compare with the DCF only after independent relative estimates are complete.
---

# Goal and required reading

Run two distinct methods for the targets in [company universe](../methodology/company_universe.md):

1. **Comparable-company valuation:** a selected, ranked peer set per target; peer medians, quartiles and fundamental adjustments.
2. **Regression valuation:** a broad, systematically defined market dataset; A within industry, B market with sector dummies, C market without dummies; four multiple models.

Read this skill, [methodology README](../methodology/README.md), the full [comparables procedure](../methodology/comparables_procedure.md) and [regression procedure](../methodology/regression_procedure.md). Also read [data sources](../methodology/data_sources.md), [sector adjustments](../methodology/sector_adjustments.md), [QA](../methodology/qa_checklist.md) and [report template](../methodology/report_template.md). These Markdown files contain the execution rules; no separate Word/PDF instruction file is needed. [Relative change summary](../methodology/RELATIVE_CHANGE_SUMMARY.md) records resolved conflicts.

Default scope is the full 20-company assignment. If the user requests one/subset, run that scope and state it; do not label a partial run as 400 peer rows or 20 completed targets. Reuse one dated market dataset across targets. The 20 targets, each target's 20 peers and the regression universe are different sets.

# Shared setup

1. Inventory the target list, source data pack, group workbook, available terminal exports and existing DCF. Reuse an already agreed data route; otherwise ask whether a terminal export is available before collecting market data. Terminal access in general is not proof that an export exists. Continue dataset/schema preparation while awaiting a required input.
2. Prefer one terminal export; if unavailable, use the specified single-source web route and reduced regression universe. Follow the stage 3 source rules, which override the generic DCF source flexibility for these datasets.
3. Record valuation date, information cutoff, FX convention, fiscal/TTM/forward basis, common share perimeter, raw and normalized units, route and all thresholds before calculations. Default earnings basis is FY2025; keep separately named TTM and forward series. Never combine them in a statistic or equation.
4. Compute ratios from raw fields. Preserve observations and original sources; apply only the documented fallbacks, with original/replacement values logged. Do not impute other missing data or change sources for one web row.
5. Reconcile market cap, quote units, share classes, EV scope, reporting/trading currencies and target annual-report cross-checks. Organize human spot-check evidence and record its pending/verified status.

# Method 1 — comparables

6. Profile each target; construct 40–60 initial candidates and expand as needed. Use the tier, hard-filter, score and composition rules in comparables_procedure.md. Select exactly 20 peers, or 15–19 only with a documented permitted shortfall. Never use the regression market indiscriminately as a peer list.
7. Compute the complete prescribed multiple set with aligned definitions. Keep positive extremes in peer statistics; exclude only unavailable/not-meaningful observations under the rules. Require at least 10 valid observations separately for each raw or scaled multiple used.
8. Show median, mean, p25, p75, unadjusted and permitted fundamental-adjusted values. Select one business-appropriate primary multiple, with the rest as cross-checks; no DCF-dependent weights. Apply the matched EV-to-equity bridge and convert to the target's quote currency.

# Method 2 — regressions

9. Build DATA_BASE_MSCI.xlsx once from the full permitted market; retain all target rows. Do not use the hand-selected peer lists as the estimation sample. Apply model-specific eligibility, beta replacement, 1%/99% continuous-variable winsorization and count gates.
10. Estimate PE, PBV, PS and EVEBITDA in A, B and C wherever valid. B and C must share the same model-specific market rows and transformed continuous data. Follow the Europe-to-World ladder and dummy coding; C never has sector or region dummies.
11. Use live Excel formulas for transformations, OLS statistics, diagnostics and valuations. Extract LINEST coefficients in reverse X order; recalculate and independently check the same fitted design outside Excel. Never substitute a published Damodaran equation for estimating these models.
12. For each target/model, apply the pure-play, percentile and sector-model-validity tests to select A or B. Rank eligible routed models by adjusted R² under the project's selection rule; output one chosen prediction and the next two eligible alternatives. Show A/B/C predictions for the same chosen multiple and explain differences without claiming they prove causality.
13. Apply residual-band classifications and D1–D10 diagnostics. Keep failed/low-quality models visible but restrict conclusions as required. Run triggered outlier/VIF robustness models separately. Benchmark matching equations against Damodaran; unavailable matching equations remain unavailable.

# Reconciliation and delivery

14. Report comparables and regression point estimates separately, then compare with the existing DCF and current price. Explain differences in earnings basis, universe, margin/growth/risk, EV adjustments and market conditions. Never choose peers, models, multiples or weights because they move a result toward DCF.
15. Preserve peer-set, quartile and multiple sensitivities, distribution/football-field charts and industry discussion from the former skill. Do not average all multiples or rank higher valuations merely because the target is large. A combined final recommendation requires an explicit stage 4 rationale; it does not overwrite either independent method.
16. Run the stage 3 QA checklist. Stop only the affected work when an input/method is blocked; complete independent work. Do not mark an unrecalculated workbook, unresolved data failure or pending required human review as final/verified.

# Deliverables

For a batch, use outputs/relative_<valuation-date>/ (repository-relative). A single-target run can use outputs/<ticker>_<valuation-date>/relative/. Preserve stage 1/2 files.

**Comparables — three core files:** comparables.csv, multiples_summary.csv, comparables_report.md.

**Regression — four core files:** DATA_BASE_MSCI.xlsx, regression_valuation.xlsx, valuation_multiples.csv, valuation_summary.md.

The procedures specify exact schemas, workbook sheets, diagnostics and report headings. Put peer-selection audit/Spot_check schedules in DATA_BASE_MSCI.xlsx when both methods run, separated from regression input; put charts in workbooks. Continue the shared source_log.csv and qa_results.md. These shared audit files are not additional valuation-method outputs. For a comparables-only run, an explicitly labelled comparables_audit.xlsx is permitted to satisfy the audit-sheet requirement; do not create fake regression outputs.

The old relative_model.xlsx, weights_table and relative_decisions.md contract is superseded: all decisions now live in the method reports and workbook Log. No weights_table is required. Cite only opened evidence; distinguish assignment thresholds from general valuation theory. Test material calculations and workbook/model equivalence when executing valuations, and report actual results rather than claiming unrun checks.
