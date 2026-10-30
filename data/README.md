# Reference-data library (Damodaran datasets as Markdown)

The agent never guesses a file name. It asks the resolver, which reads `registry.csv` and returns the right dataset for the company's country,
the valuation date and the requested family, or says exactly what is missing.

## Use (agent)
```
cd src && python -m valuation_agent.datasets list                                  # what is registered
python -m valuation_agent.datasets resolve beta --country Spain --date 2026-10-30  # which file, match level, warnings
python -m valuation_agent.datasets check                                           # integrity findings for every dataset
```
In Python: `datasets.resolve(family, country=..., valuation_date=...)`, `load_industry`, `get_value(df, 'beta', 'Power', 'beta_unlevered_cash_corrected')`,
`load_risk_premiums` + `country_risk(rp, 'Italy')`, `equation_for('Spain', 'PE')`. Log in `source_log.csv`: dataset id, vintage, path, sha256 (from the registry),
the logical column used and the actual header (`pick_column`), match level and any warning. Never silently accept a `fallback` match: record why it is representative.

## What is registered (2026-10-30)
| dataset_id | family | region | vintage | as of | contents |
|---|---|---|---|---|---|
| beta_europe_2026-01 | beta | EUROPE (Western Europe) | 2026-01 | 2026-01-05 | 94 industries, unlevered beta corrected for cash, D/E, marginal tax 24.71% |
| capex_europe_2026-01 | capex | EUROPE | 2026-01 | 2026-01-05 | net CapEx/Sales, net CapEx/EBIT(1-t), sales/invested capital, aggregates |
| ctryprem_global_2026-07 | ctryprem | GLOBAL (all countries) | 2026-07 | 2026-07-09 | mature ERP 4.20%, rating spreads, CRP, total ERP, frontier markets |
| regressions_multi_2026-01 | regressions | US, EUROPE, JAPAN, EM, GLOBAL, ANZCA | 2026-01 | 2026-01 | 36 equations: PE, PEG, PBV, EV/IC, EV/Sales, EV/EBITDA |
Still missing for a full stage 2: `dbtfund` (debt ratios) and `wcdata` (working capital) for Europe, and a rating-to-spread (interest coverage) table. Until supplied,
the agent fetches them with `damodaran.py` (see `methodology/data_sources.md`) or asks you.

## How region matching works
1. Country -> canonical region code through `regions.csv` (built from the risk-premium file's Region column; each row has a confidence and a note).
2. Region -> ordered fallback chain through `region_fallbacks.csv` (always ends in GLOBAL; e.g. INDIA|EM|GLOBAL). A country row may override with `preferred_regions`.
3. The first region in the chain with a registered dataset wins; among vintages, the latest whose as-of date is not after the valuation date.
4. Datasets that contain several regions (regressions) declare them in `regions_inside`; the equation is taken for the same chain.
The three file families use different region labels (risk premiums: Western Europe, North America, Asia...; regressions: US, Europe, Japan, Emerging Markets,
Aus NZ & Canada, Global). `regions.csv` is the translation layer; check low-confidence rows (Turkey, Singapore, Hong Kong, Korea, Taiwan, Macao, Canada) before relying on them.

## Add a new region, vintage or dataset (you)
1. Save the Damodaran page/table as Markdown (same layout as the four supplied files) with its title and a `**Date updated:**` line.
2. Give it to the agent, or run `python -m valuation_agent.datasets add <file.md>`. The title decides the family and region
   (`Betas and Risk Measures by Industry: Japan` -> beta/JAPAN). If detection fails, pass `--family` and `--region`.
3. Read the integrity findings it prints. Errors mean the file is unusable; warnings mean verify against the original.
4. For a NEW family (working capital, debt ratios, industry multiples): run `columns <id>`, then add rows to `column_maps.csv` (logical name -> header spellings).
   Do not guess headers; the agent stops when a header is not found.
5. New country or alias: edit `regions.csv` / `country_aliases.csv`. New region code (e.g. BRAZIL): add it to `region_fallbacks.csv` and point countries to it.
6. Same content is rejected as duplicate; a corrected file for the same vintage needs a new vintage or an explicit replace. A file edited after registration fails its sha256 check.
7. Only Markdown tables are supported. A new file layout (xls, different title pattern) needs a small addition to `TITLE_PATTERNS` or the loaders in `datasets.py`;
   the tests in `src/tests/test_datasets.py` show how.

`enterprise_type`: the registry has an `applies_to` column ("all" by default). A future dataset that applies only to financial firms (banks, insurers) can be registered
with `applies_to=financial` and is then only returned when the caller asks for that enterprise type.
