# Standing approvals and run parameters (USER EDITS THIS FILE; the agent only reads it)

The agent must not ask again for anything answered here. Leave a field as `TBD` if you have not decided; the agent will then ask once
and write your answer back here.

## Run parameters
- batch_valuation_date: 2026-10-30     # one common date for all companies, YYYY-MM-DD. Market data is built once per date.
- mode: standard                       # standard | full   (see AGENTS.md section 2)
- regression_route: published_damodaran   # published_damodaran | own_estimation. Set 2026-10-30 at the user's request: use the registered Damodaran equations instead of estimating
                                          # own regressions (methodology/regression_published_route.md). Change to own_estimation to re-enable the full regression procedure.
- published_route_allow_fundamental_growth: yes   # yes | no. The published equations need ANALYST growth (g_eps, g_rev). yes = may substitute our fundamental growth, labelled; no = unavailable.
- damodaran_dfr_tax_units: decimal      # DFR = total debt/(total debt + market equity); tax_rate = effective tax rate. Enter as decimals (30% = 0.30), same as all other inputs (section 3). Basis: Facebook example. Set by user 2026-10-30.
- data_route_stage3: web_minimum       # terminal_export | web_full | web_minimum. Needed for own_estimation and for collecting comparable-candidate data; web_minimum = Utilities, Energy, Industrials, Materials only. Set 2026-10-30: AI.PA is bucket D (industrials), inside web_minimum coverage.
- terminal_export_available: no        # yes/no. If yes, put the export file in cache/market/<date>/export/ and name the terminal below
- terminal_name: n/a                   # Bloomberg | LSEG Workspace | Capital IQ (no terminal export available)
- companies_in_scope: MT.AS  # user confirmed MT.AS-only stage-0 top-up and stages 1-4 on 2026-10-31
- report_language_and_format: English, PDF

## Approvals already given (the agent reuses these instead of asking)
- report_outline: not yet              # approved | approved with changes: <...> | not yet. If approved, the agent builds the report after stage 3.
- scope_one_company_per_run: yes
- proceed_without_waiting_when_non_critical: yes

## Approved deviations from the procedures (each must be explicit; empty = none)
<!-- Example: "lazy_exclusion_check: verify ownership/restructuring exclusions only for candidates that would enter the selected peer set"
     Without an entry here, the agent applies every rule as written. -->
- regression_route: published_damodaran (user request 2026-10-30; replaces own estimation of the regressions, with the limits listed in methodology/regression_published_route.md section 6)
- relative_only: for the remaining companies the DCF is produced outside this project. Run only stage 3 (published_damodaran route, standard mode). Skip stage 2 and stage 4 entirely (no DCF, no recommendation, no PDF report, no report_outline). Replace stage 1 by a reduced input step: collect only the target data stage 3 needs (price, shares and market cap, EV bridge items, FY2025 revenue, EBITDA, EBIT, net income, book equity, currencies, fiscal-year basis) into outputs/<ticker>_<date>/relative_inputs.md with sources; no data_pack.xlsx, no anomaly report, no source_log beyond one line per source. Mark stages 1-2-4 "skipped_by_deviation" in run_state.json. Read only: SKILL-RELATIVE.md, comparables_procedure.md, regression_published_route.md, sector_adjustments.md, company_universe.md, data_sources.md and QA checklist block C. Do not read regression_procedure.md or report_template.md. Pass min_valid=6 to multiple_stats and scaled_multiple.

## Stage 4 calibration (the professor will calibrate later)
- stage4_calibration_notes: TBD

## Authorized extra data the agent may use
- user-attached files: list them here with what they contain (LSEG normalised values, analyst reports, ...)
