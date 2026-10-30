# Shared cache: build once per valuation date, reuse for every company

Everything here is independent of which company is being valued. It is produced by
`.agents/skills/valuation-0-market-refresh/SKILL.md` and consumed by stages 1-3. Check this file at the start of every session.

| Path | Contents | Key | Reused by |
|---|---|---|---|
| `damodaran/<vintage>/` (live-fetched families only; the supplied datasets live in the data library `data/`, resolved with `datasets.resolve`) | `dbtfundEurope.csv`, `capexEurope.csv`, `wcdataEurope.csv`, `betaEurope.csv`, `ctryprem.csv`, ratings/spreads table, `manifest.json` (URL, access date, sha256, sheet, header row, all columns) and `COLUMN_NOTES.md` (what each column used means, verified by the agent) | dataset vintage (usually the January or latest update) | stage 1 normalisation, stage 2 benchmarks, stage 3 beta fallback |
| `macro/<valuation_date>.json` | 10-year government yields by currency, sovereign default spreads, mature ERP, ECB FX rates for the date, each with source URL and access date | valuation date | stage 2 (Rf, Kd, CRP), stage 3 (FX) |
| `market/<valuation_date>/` | `DATA_BASE_MSCI.xlsx`, `regression_valuation.xlsx` (all A/B/C models and all 20 targets), `regression_fits.json` (coefficients, n, k, cutoffs, diagnostics per model), `MANIFEST.md` (route, universe counts, software versions, test results, human-review status) | valuation date | stage 3 comparables (candidate pool and scoring metrics) and regression (target valuations) |
| `web/<valuation_date>/` | raw fetched pages from `CachedFetcher` | URL | same-session retries only; git-ignored |

## Rules
1. **Look before you fetch.** If the file exists for the valuation date, use it. Never refetch the same URL for the same date
   (`CachedFetcher` enforces this on disk, but the parsed outputs above are the durable copy).
2. **Date-keyed.** A different valuation date needs a new `macro/` and `market/` folder. Do not reuse a market dataset for another date
   (look-ahead and stale-price problems, see `data_sources.md`). That is why one batch date is set in `memory/standing_approvals.md`.
3. **Never edit cached files by hand.** Corrections are made by re-running the refresh step that produced them, and logged in `MANIFEST.md`.
4. **Provenance travels with the data.** Every file has a manifest row; stage runs cite the cache file and its manifest in `source_log.csv`
   (`url_or_local_file`, `dataset_vintage`, `access_date`).
5. **Partial builds are saved.** The market build writes `market/<date>/partial/` every ~25 companies so an interrupted session resumes.
6. **Human review is not the agent's to claim.** `MANIFEST.md` carries the Spot_check status (`pending`, `verified by <name> <date>`,
   `waived by user <date>`); stage 3 deliverables inherit it and stay labelled draft while it is `pending`.
7. **Raw page caches are not committed** (`.gitignore`). Commit the parsed CSV/XLSX/JSON.
