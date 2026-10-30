# valuation_agent: tested building blocks

Install once per session: `pip install -r src/requirements.txt` (add `--break-system-packages` where needed) and run scripts with
`PYTHONPATH=src` (or `cd src`). Run the tests only after changing code: `cd src && python -m pytest tests -q` (133 tests).

| Module | Purpose | Procedure it implements |
|---|---|---|
| `dcf.py` | beta/Ke/Kd/WACC, NWC schedule with floor, NCE, FCFF/FCFE, growth-stage heuristic, terminal value, varying-rate discounting, equity bridge, rate x g grid, driver ranking | `dcf_procedure.md` sections 2-10 |
| `regression.py` | PERCENTILE.INC winsorisation, eligibility with first-failure reasons, beta replacement, dummy coding, OLS with Excel-LINEST statistics, `compare_to_linest` (the independent check), typicality, model ranking, residual bands, D1-D9 diagnostics, robustness refits | `regression_procedure.md` sections 3-9 |
| `comparables.py` | similarity score, exact constrained peer selection (verified against an integer-programming solver), relaxation steps, multiple statistics, fundamental adjustments, EV bridge and its inverse | `comparables_procedure.md` sections 3-6 |
| `anomaly.py` | year-on-year and 5-year-average deviation flags, markdown table for `anomaly_report.md` | stage 1 step 5 |
| `sourcelog.py` | 21-field `source_log.csv` writer and validator (stage 3 extra columns preserved) | `data_sources.md` |
| `runstate.py` | `run_state.json` checkpoints, resume point, stage timings, `memory/run_log.csv` | `AGENTS.md` |
| `cachefetch.py` | cached, parallel, per-host throttled fetching with provenance manifest | `AGENTS.md` |
| `mdtables.py`, `datasets.py`, `published_regressions.py` | Markdown dataset parser; registry + resolver (country/region/vintage/valuation-date, fallback chains, look-ahead exclusion), loaders, `add` command, integrity checks; parser, predictor and unit-policy guard for the published Damodaran regressions | `data/README.md`, `methodology/regression_published_route.md` |
| `damodaran.py` (live download of families not in the library) | download and parse Damodaran datasets once per vintage (keeps every column; header found by key) | `data_sources.md` |

What the code does NOT do: choose inputs, assign tiers, decide primary multiples, judge pure-play status, read annual reports, build the
Excel deliverables. Those stay with the agent and the procedures. `example_usage.py` shows a full FCFF chain with illustrative numbers.

Status of the live-data parts: `cachefetch.py` is tested against a local HTTP server; `damodaran.py` is tested on synthetic workbooks.
Neither has been run against the real websites from the build environment. First real use: run
`python -m valuation_agent.damodaran --selftest`, then `--fetch cache/damodaran <vintage>`, read the printed columns, and fix `header_key`
in `DATASETS` if a file differs. Log the outcome in `memory/source_playbook.md`.
