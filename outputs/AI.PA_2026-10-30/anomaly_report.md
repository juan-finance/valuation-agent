# Anomaly report — AI.PA, FY2021–FY2025 + interim

Scan: `valuation_agent.anomaly.anomaly_table`, threshold ±30% YoY on all sourced series.
Flags are listed first (raw output: `anomaly_report_raw.md`), then investigated and resolved below.

## Flags (>30% YoY)

| Item | Year | Value (EUR m) | YoY | Dev from avg |
|---|---|---|---|---|
| Cash & equivalents | 2025 | 3,962.0 | +107% | +0.70 |
| Change in WC | 2022 | -396.8 | -205% | -2.57 |
| Change in WC | 2023 | -154.4 | +61% | -0.39 |
| Change in WC | 2025 | -226.0 | -46% | -1.04 |
| Acquisitions | 2022 | -135.8 | +79% | +0.52 |
| Acquisitions | 2024 | -269.0 | -161% | +0.05 |
| Divestitures | 2022 | 61.1 | -53% | -0.63 |
| Divestitures | 2023 | 339.7 | +456% | +1.07 |
| Divestitures | 2024 | 113.0 | -67% | -0.31 |
| Divestitures | 2025 | 177.8 | +57% | +0.08 |
| Buybacks | 2022 | -191.5 | -378% | -0.75 |
| Buybacks | 2023 | -81.9 | +57% | +0.25 |
| Buybacks | 2024 | -230.8 | -182% | -1.10 |
| Buybacks | 2025 | -4.0 | +98% | +0.96 |

## Resolution (kept as reported — none normalized)

- **Cash & equivalents 2025 (+107%)**: real and explained by the FY2025 cash-flow statement: gross borrowings rose €2,060.4m while capex stayed high; net cash build +€2,375.5m. Net debt still fell to €8,415.5m (AR net-debt bridge p.39). Keep.
- **Change in WC**: small absolute swings on a near-zero base; FY2022 -396.8m reflects post-2022 energy-price working-capital normalization, FY2025 -226.0m an increased WCR per AR p.31. Sign instability is mechanical; keep, use a multi-year average in stage 2 rather than a point value.
- **Acquisitions/Divestitures**: lumpy portfolio rotation is normal for Air Liquide (e.g. FY2023 +339.7m disposals incl. financial-asset sales; FY2024 -269.0m acquisitions). Keep; stage 2 should use normalized (average) M&A, not a single year.
- **Buybacks 2025 (-98%)**: treasury purchases paused in 2025 (-4.0m vs -230.8m in 2024) per AR financing section; real, not an error. Keep; dividends are the stable payout channel.

## Notes

- Revenue YoY 2023 (-7.8%) is below the 30% threshold but driven by energy/currency pass-through, not operations (comparable +3.7%); recorded for stage-2 awareness.
- FY2025 "Operating Income" on stockanalysis (5,201) differs from AR OIR (5,581.6) and AR IFRS operating income (5,278.7): aggregator uses its own recurring-profit definition. The AR series is used; see `company_identity.md` discrepancy table.
- FY2021 balance-sheet/OIR items are aggregator-only (status `unverified`/`unavailable` in source_log.csv); FY2022–FY2025 are annual-report sourced.
