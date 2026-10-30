# Source playbook: what worked, what failed, what columns mean

Fill after the FIRST real use of each source. Nothing below is assumed to work until a row says `verified`.

| Source / dataset | Exact URL or file | Access result (date) | Verified columns / fields and their meaning | Quirks | Status |
|---|---|---|---|---|---|
| Damodaran dbtfund (Europe) | see methodology/data_sources.md | not supplied, not yet fetched | | | unverified |
| Damodaran wcdata (Europe) | see methodology/data_sources.md | not supplied, not yet fetched | | | unverified |
| Damodaran beta (Western Europe) | data library: beta_europe_2026-01 | supplied by user 2026-10-30, parsed and checked | `Unlevered beta corrected for cash` (column map); internally consistent for 94/94 industries | Relever with company tax, not 24.71% | verified (parse, consistency) |
| Damodaran capex (Europe) | data library: capex_europe_2026-01 | supplied by user 2026-10-30, parsed and checked | `Net Cap Ex / EBIT (1-t)`, `Net Cap Ex / Sales` | Steel and Railroads not meaningful; some `NA` | verified (parse) |
| Damodaran country risk premiums | data library: ctryprem_global_2026-07 | supplied by user 2026-10-30, parsed and checked | `Rating-based Default Spread` (no `Adj. Default Spread` column), `Country Risk Premium (CRP)`, `Total ERP` | as-of 2026-07-09; US row differs; Turkey under Western Europe | verified (parse, arithmetic) |
| Damodaran market regressions | data library: regressions_multi_2026-01 | supplied by user 2026-10-30, parsed and checked | 36 equations, coefficients, t-stats, R2 | no n/SEy; DFR/tax units open; Global PEG anomaly | verified (parse), units unverified |
| stockanalysis.com statistics / statements pages | | not yet used | | | unverified |
| Index holdings file (MSCI Europe / World proxy) | | not yet located | | | unverified |
| ECB reference rates (FX) | | not yet used | | | unverified |
| 10-year government yields (Bund, Gilt, ...) | | not yet used | | | unverified |
