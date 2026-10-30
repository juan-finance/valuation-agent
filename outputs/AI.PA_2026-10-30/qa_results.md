# QA results — Stage 1 (data sourcing), AI.PA @ 2026-10-30

## Block A — data sourcing

- [x] **Identity confirmed**: Air Liquide, Euronext Paris, ticker AI, EUR, FY-end Dec-31, ISIN FR0000120073, CAC-40 large cap.
- [x] **Financials tie to AR and BS balances**: FY2022–FY2025 sourced from official FY results press releases; TOTAL ASSETS = TOTAL EQUITY AND LIABILITIES each year (48,332.4/49,518.0/51,867.5/51,913.4). FY2021 from stockanalysis only — flagged `unavailable`/`unverified` where definitional; acceptable, recorded.
- [x] **Anomaly flags resolved**: 14 flags, all investigated and kept as reported (see anomaly_report.md); none normalized.
- [x] **Shares exclude treasury, checked vs report and exchange**: 636.47m current shares post Jun-2026 attribution (stockanalysis/Euronext); AR avg FY2025 576.79m and treasury shares -179.6m on BS consistent.
- [x] **Debt/cash reconciled to net debt**: borrowings 12,377.5 − cash 3,962.0 = net debt 8,415.5 exactly as AR; leases 1,259.4, pensions/provisions 2,421.9, NCI 733.3, equity affiliates 174.6 recorded separately for stage-2 bridge per sector_adjustments.
- [x] **Currency/units consistent**: all EUR millions; London-GBp issue n/a; interim values labelled.
- [x] **Every number sourced + dated in source_log.csv**: 130+ rows, `sourcelog.validate` clean (0 problems); sourced rows carry URL/file + page locator.

## Data-quality notes for later stages

1. Damodaran industry data: not needed at this stage; will come via `datasets.resolve` only (route confirmed).
2. Regressions vintage Jan-2026 (~10 months old) — already logged as Limitations item for stage 3.
3. FY2021 column is aggregator-only; if a stage-2 model needs AR-quality FY2021 balance items, fetch the FY2022 press release comparatives (~5 min).
