# Valuation methodology

The repository folders are: .agents/skills/ (agent instructions, one folder per stage plus the company-valuation orchestrator), methodology/ (shared definitions and detailed procedures), lecture_notes/ (the professor's slides, highest authority), method_guides/ (the Word and PDF instruction documents the procedures were built from) and examples/ (worked cases, method only). Stage 2 and stage 3 produce independent estimates before the stage 4 reconciliation. This revision adds relative valuation to the existing DCF workflow.

| Path | Role |
| --- | --- |
| .agents/skills/valuation-2-dcf/SKILL-DCF.md | Existing stage 2 DCF skill; keep unchanged |
| .agents/skills/valuation-3-relative/SKILL-RELATIVE.md | Stage 3 orchestration of comparables and regressions |
| methodology/dcf_procedure.md | Existing complete DCF procedure |
| methodology/comparables_procedure.md | New peer selection, scoring, multiples and valuation procedure |
| methodology/regression_procedure.md | New market dataset, A/B/C regressions, Excel formulas and diagnostics |
| methodology/company_universe.md | Original 20 targets, sector mapping and distinct universe definitions |
| methodology/data_sources.md | Sources, stage-specific acquisition rules and evidence schema |
| methodology/sector_adjustments.md | DCF conventions plus relative primary multiples and bridge checks |
| methodology/qa_checklist.md | Stage-specific completion and validation gates |
| methodology/report_template.md | Integrated report, independent methods and appendix requirements |

## Authority and execution

Precedence (identical to the company-valuation skill, which is the authoritative statement): 1) the professor's lecture notes; 2) these methodology procedures and the stage skills, which consolidate Steps in Company Valuation.docx and the Agent Instructions PDFs (written from the lectures) and record deliberate corrections to them in their conflict registers; those corrections stand unless a lecture says otherwise; 3) the Word/PDF originals in method_guides/, consulted only to settle a doubt the procedures leave open and never to reverse a recorded correction; 4) sector_adjustments.md; 5) worked examples (method only; if one differs from a higher source, follow the higher source, record it in case_summary.md and tell the user, without stopping to ask). In any contradiction with a lecture, the lecture wins and the conflict is recorded. A conflict the hierarchy cannot settle (same rank, equally specific rules, ambiguous lecture) is not chosen silently: the agent asks the user and continues independent work meanwhile ("Conflict handling" in the company-valuation skill). User-supplied run parameters (company, date, data route, scope, files) are inputs and do not change this order unless the user says so explicitly. The detailed Markdown procedures consolidate the supplied instructions and make their mathematical/operational ambiguities explicit. Project thresholds and defaults are labelled as such; do not present them as universal theory or independently verified professor statements. There is no need to open the Word/PDF documents to execute these procedures; open them, and the relevant lecture, only to settle a doubt or a suspected contradiction, and record the outcome.

For DCF, use SKILL-DCF.md and dcf_procedure.md. For relative valuation, read SKILL-RELATIVE.md, then BOTH comparables_procedure.md and regression_procedure.md, followed by the shared sources, universe, sector, QA and report files. A newer stage 3 rule supersedes the old relative skill where incompatible; it does not silently change DCF calculations. Record remaining conflicts and concrete limitations in the relevant method report/Log. Continue independent work when one model is blocked; never fabricate missing inputs or label a failed result verified.

Maintain one information cutoff and dated source archive. The default relative assignment uses FY2025; FY, TTM and forward earnings are separate series. DCF may use adjusted trailing earnings while relative analysis uses a consistent reported base: reconcile differences explicitly. Do not substitute DCF inputs for regression-specific definitions of growth, beta, ROE or EV.

## Distinct populations and results

- Targets: the 20 original companies being valued.
- Comparables: up to 10 selected peers per target, chosen under tiers/filters/fundamental scores; generally overlapping across targets.
- Regression market: all eligible companies in the configured MSCI Europe/World universe, not hand-picked peers. Full and web-minimum versions have different coverage and sample thresholds.

Comparable valuation uses one business-appropriate primary multiple with supporting cross-checks. Regression estimates four multiple models in A/B/C and uses the prescribed typicality/adjusted-R² selection for one result per target. Report both estimates independently. Remove the former DCF-proximity and size-based valuation weighting; no 30% weight cap or weights_table applies to the new method. A stage 4 combined recommendation needs its own reasoned decision and must preserve the underlying estimates.

## Outputs and handoff

Repository-relative paths (no leading slash): a run writes only inside outputs/ (the agent creates the folder; run-level files such as case_summary.md, report_outline.md, qa_results.md and source_log.csv sit in outputs/<ticker>_<date>/). There is no templates/ folder and no group workbook; the agent researches peers, cross-checks and data itself. The src/valuation_agent/ library (tested arithmetic of these procedures), cache/ (shared market assets, built once per valuation date by .agents/skills/valuation-0-market-refresh) and memory/ (facts and lessons, never rules) were added for efficiency and do not change any rule here; if code or memory disagrees with a procedure, the procedure wins. Stage 1 sourcing and stage 2 DCF continue unchanged. Stage 3's core files are comparables.csv, multiples_summary.csv, comparables_report.md, regression_valuation.xlsx, valuation_multiples.csv and valuation_summary.md, plus DATA_BASE_MSCI.xlsx only under regression_route own_estimation: seven files under own_estimation, six under published_damodaran (see regression_published_route.md section 7). Shared source/QA logs continue; embed audit schedules/charts as specified. Scope: the company-valuation orchestrator values ONE company in outputs/<ticker>_<date>/ (stage 3 in its relative/ subfolder); a direct whole-assignment stage 3 run uses outputs/relative_<date>/. There is no relative_model.xlsx; stage 4 and the orchestrator use the core files that the configured regression_route produces. source_log.csv always uses the 21 fields in data_sources.md. Stage 4 follows report_template.md. Existing approval of scope/data route is reused; required manual data review is recorded honestly.
