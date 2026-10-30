---
name: valuation-0-market-refresh
description: Stage 0, run ONCE per valuation date and before any company run. Checks the reference-data library, builds the macro snapshot, and (only for regression_route own_estimation) the MSCI market dataset and all regressions in cache/. Use when cache/ lacks assets for the batch valuation date, when the data library lacks a dataset a company needs, or when the user asks to refresh market data.
---

# Goal
Do the company-independent work one time so that stages 1-3 for each company only read shared files. Nothing here is a judgement about one company.
Rules come from the procedures; this file orders the work and depends on the regression route.

# Before starting
1. Read `AGENTS.md` and `memory/standing_approvals.md`. You need `batch_valuation_date`, `regression_route`, `companies_in_scope` and, for route `own_estimation` or
   candidate-data collection, `data_route_stage3`. Ask once (all questions in one message) for anything `TBD`, and write the answers back.
2. Read `cache/README.md` and `data/README.md`. Skip every step whose output already exists for this date (check `MANIFEST.md`). Resume from `partial/` if present.
3. `pip install -r src/requirements.txt`; use `PYTHONPATH=src`. This stage has no per-company run folder: record timings in `cache/market/<date>/MANIFEST.md` and append to `memory/run_log.csv`.

# Steps (each ends with a commit of its parsed outputs)
**0.1 Data-library check (replaces downloading).** Run `python -m valuation_agent.datasets list` and `check`. For each country in `companies_in_scope` and each family a stage needs
(beta, capex, ctryprem, regressions, plus dbtfund and wcdata for stage 2), run `datasets.resolve(family, country=..., valuation_date=<batch date>)`. Collect everything that is not
found or is a `fallback`, and send the user ONE message listing the exact files to supply (family, region, vintage) and the warnings (look-ahead exclusions, low-confidence country mappings).
Do not download a family the library already has. For families the library lacks and that Damodaran publishes as spreadsheets (debt ratios, working capital), use
`python -m valuation_agent.damodaran --fetch cache/damodaran <vintage>`, print the columns, fix `header_key` if needed, and write `cache/damodaran/<vintage>/COLUMN_NOTES.md`
(exact column used, definition, median or aggregate). Add what you learn to `memory/source_playbook.md` and, if you found new problems in a library file, to `data/damodaran/NOTES.md`.

**0.2 Macro snapshot** `cache/macro/<date>.json`: 10-year government yield per currency in the universe, sovereign default spread of each benchmark issuer
(take it from the library's country-risk dataset, not from memory), mature-market ERP of that dataset (`datasets.mature_erp`), and ECB reference FX rates for the date
(state quotation direction). Each value: source, access date, observation date. Missing = "not available".

**0.3 Route `published_damodaran` (the setting in standing_approvals).** No market sample, no estimation, no DATA_BASE_MSCI.xlsx. Do instead:
- Resolve the published equation for every country in scope and each of PE, PBV, EV/EBITDA (`datasets.equation_for`); run `check_dataset` on the regressions dataset; write the
  findings, the equations used and any anomaly that blocks an equation into `cache/market/<date>/MANIFEST.md`.
- Candidate universe for comparables: obtain ONE dated membership list (MSCI Europe holdings file, plus World only if the relaxation may need it), reconcile counts, label proxy
  coverage, apply the classification and exclusion screens that need no per-company reading. Save as `cache/market/<date>/universe.csv`.
- Candidate data are collected in stage 3B only for the 40-60 candidates of each target, with `CachedFetcher`, and cached in `cache/market/<date>/candidates/<ticker>.csv` so overlapping
  peers of other targets cost nothing.

**0.3 Route `own_estimation`.** Follow `regression_procedure.md` sections 1-4 and 9.
- Terminal export: load the export, map fields to the `Data` columns of section 2, keep raw fields, add the comparables superset (net debt/EBITDA inputs, CapEx/Sales, EBITDA margin,
  associates, ln market cap). Log the mapping.
- Web: universe from a dated holdings file (reconcile counts, label proxy coverage), then ONE uniform source per company with `CachedFetcher(cache/web/<date>, max_workers=4, min_delay>=1)`;
  verify the table identity on the first company by hand, write `partial/` every ~25 companies. Check the site's terms of use first and tell the user if they restrict bulk access.
- Apply, in order, logging counts: dedupe, units, beta replacement (`regression.replace_beta`), eligibility per model (`regression.eligibility`), validation checks of section 3,
  Spot_check lists (targets + 20 reproducible random rows). Keep all 20 targets as `is_sample=TRUE`. Output `cache/market/<date>/DATA_BASE_MSCI.xlsx`.

**0.4 (own_estimation only) Regressions once for all targets.** Fit B and C on the same rows and A by the scope ladder with `regression.fit_model` / `choose_scope_A`; save coefficients, n, k, df, R2,
adjusted R2, SEy, cutoffs and D1-D9 to `regression_fits.json`; compute `regression.value_target` for all 20 targets (typicality and pure-play inputs come in stage 3B).

**0.5 (own_estimation only) Workbook and independent check.** Build `regression_valuation.xlsx` per section 5, recalculate, read every LINEST block and run
`regression.compare_to_linest(fit.ols, excel_block)`: every model must return an empty list. Recompute three predictions by hand.

**0.6 Manifest and hand-off.** Write `cache/market/<date>/MANIFEST.md`: route, library datasets used (ids, vintages), universe counts, exclusions by reason, (own_estimation) per-model n/scope/R2,
software versions, test results, minutes per step, Spot_check status (`pending` until the user returns it), limitations. Update `memory/index.md` and `memory/source_playbook.md`.
Post a short message: what was built, what the user must supply or review, minutes spent.

# Stop rules
`regression_procedure.md` section 9 and `comparables_procedure.md` section 8 for the steps that follow them; `regression_published_route.md` section 8 for the published route.
Do not claim human review. Do not mark the cache final while an independent check or benchmark-gap check is unresolved.
