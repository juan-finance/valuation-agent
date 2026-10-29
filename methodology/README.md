# Valuation methodology

The repository has two folders: skills/ contains agent instructions; methodology/ contains shared definitions and detailed procedures. Stage 2 and stage 3 produce independent estimates before the stage 4 reconciliation. This revision adds relative valuation to the existing DCF workflow.

| Path | Role |
| --- | --- |
| skills/SKILL-DCF.md | Existing stage 2 DCF skill; keep unchanged |
| skills/SKILL-RELATIVE.md | Stage 3 orchestration of comparables and regressions |
| methodology/dcf_procedure.md | Existing complete DCF procedure |
| methodology/comparables_procedure.md | New peer selection, scoring, multiples and valuation procedure |
| methodology/regression_procedure.md | New market dataset, A/B/C regressions, Excel formulas and diagnostics |
| methodology/company_universe.md | Original 20 targets, sector mapping and distinct universe definitions |
| methodology/data_sources.md | Sources, stage-specific acquisition rules and evidence schema |
| methodology/sector_adjustments.md | DCF conventions plus relative primary multiples and bridge checks |
| methodology/qa_checklist.md | Stage-specific completion and validation gates |
| methodology/report_template.md | Integrated report, independent methods and appendix requirements |

## Authority and execution

Use current explicit user/professor instructions first. The detailed Markdown procedures consolidate the supplied instructions and make their mathematical/operational ambiguities explicit. Project thresholds and defaults are labelled as such; do not present them as universal theory or independently verified professor statements. There is no need to open a separate Word/PDF instruction attachment to execute these procedures.

For DCF, use SKILL-DCF.md and dcf_procedure.md. For relative valuation, read SKILL-RELATIVE.md, then BOTH comparables_procedure.md and regression_procedure.md, followed by the shared sources, universe, sector, QA and report files. A newer stage 3 rule supersedes the old relative skill where incompatible; it does not silently change DCF calculations. Record remaining conflicts and concrete limitations in the relevant method report/Log. Continue independent work when one model is blocked; never fabricate missing inputs or label a failed result verified.

Maintain one information cutoff and dated source archive. The default relative assignment uses FY2025; FY, TTM and forward earnings are separate series. DCF may use adjusted trailing earnings while relative analysis uses a consistent reported base: reconcile differences explicitly. Do not substitute DCF inputs for regression-specific definitions of growth, beta, ROE or EV.

## Distinct populations and results

- Targets: the 20 original companies being valued.
- Comparables: up to 20 selected peers per target, chosen under tiers/filters/fundamental scores; generally overlapping across targets.
- Regression market: all eligible companies in the configured MSCI Europe/World universe, not hand-picked peers. Full and web-minimum versions have different coverage and sample thresholds.

Comparable valuation uses one business-appropriate primary multiple with supporting cross-checks. Regression estimates four multiple models in A/B/C and uses the prescribed typicality/adjusted-R² selection for one result per target. Report both estimates independently. Remove the former DCF-proximity and size-based valuation weighting; no 30% weight cap or weights_table applies to the new method. A stage 4 combined recommendation needs its own reasoned decision and must preserve the underlying estimates.

## Outputs and handoff

Repository-relative paths: outputs/, src/, templates/. Stage 1 sourcing and stage 2 DCF continue unchanged. Stage 3's seven core files are comparables.csv, multiples_summary.csv, comparables_report.md, DATA_BASE_MSCI.xlsx, regression_valuation.xlsx, valuation_multiples.csv and valuation_summary.md. Shared source/QA logs continue; embed audit schedules/charts as specified. Stage 4 follows report_template.md. Existing approval of scope/data route is reused; required manual data review is recorded honestly.
