# NKT A/S (NKT.CO) - short relative-only report (remediated)

Valuation date 2026-10-30 | price date 2026-10-30 | accessed 2026-11-01 | EUR/share unless stated (quote DKK 839.0 = EUR 112.26 at ECB 7.4735).

STATUS: provisional - limitations disclosed. QA-C re-graded under qa_grading_and_remediation: all prior FAILs are PASS-with-note (uniform rules applied, limitations disclosed). Human Spot_check stays PENDING. Not investment advice.

Scope: NKT.CO only; standard / published_damodaran / web_minimum. Stage1/DCF/Stage4 skipped by approved relative_only deviation. Denmark stage-0 top-up only.

1. Valuation range

Primary diagnostic (growth-scaled peer PE): 137.91 EUR (+22.8% vs quote). Published-regression PBV: 102.39 EUR (-8.8%). Valuation range shown as EUR 89.72-137.91/share (spanning the published PE regression and raw peer-PE median at the low end to the scaled primary at the high end); peer-IQR dispersion 95.11-185.83. Diagnostics, not a fair-value point estimate.

2. Financial basis and definitions

FY2025; EURm. Sales 3,565; EBIT 578 / EBITDA 680 vendor basis (issuer EBIT 257 / operational EBITDA 390; pretax 294 exact); NI 275, NI-to-common 264 (hybrid coupon 11 stripped); common equity 2,043 (group 2,193 - EUR 150m hybrid); debt+leases 251; cash&ST 1,214; CFO 499; capex 695; effective tax 6.46% one-off-driven. Hybrids EUR 150m 7.24% (call 1-Jul-2026) + EUR 150m 5.00% (Mar-2026); claim removed once in the EV->common bridge.

Market cap EUR ~6,001m; EV EUR 5,038m (debt+NCI-cash, LT investments excluded, pre-associate basis - one uniform rule for target and peers). Beta 0.65 kept.

3. Peer set and Tier-3 fit

10 peers (8 Tier1/2, 2 Tier3, 10 Europe): G1A, NEX, VWS, ALFA, PRY, SKF.B, IMI, SPX, ANDR, LR. G1A (GEA, process machinery) retained as industrial capital-goods fit. TKA (thyssenkrupp, steel/materials conglomerate) was clearly not cable/electrical-equipment-type and was replaced by next-ranked ALFA (Alfa Laval, heat-transfer/rotating equipment), which passes all automated filters. Hard exclusions: ELHA (MSCI EM), GEV (spin-off + one-off tax), ATCO.A/EPI.A (dual-class cap check >2%). One ownership/events source line per peer in evidence_review.md.

4. Why scaled PE (+22.8%) and published PBV (-8.8%) diverge

The PE diagnostic is peer-relative: NKT fundamental growth 12.4% (ROE 12.9% x capped retention ~96%) exceeds the pool median, so growth-scaling lifts the applied peer median from 26.98x to 27.92x, giving EUR 137.91. The PBV diagnostic is regression-absolute: the published EUROPE equation predicts PBV 2.68 vs NKT actual 2.74 - the market already prices NKT near what its ROE/growth/beta/payout imply, so the residual gap is small and slightly negative. They answer different questions (peer-dispersion pricing vs a market-wide ROE model, published R2 0.423); denominators differ (earnings vs hybrid-stripped book), the substituted fundamental growth feeds the PE scaling far more aggressively than the published equation rewards it, and the vendor-vs-issuer EBIT/NI basis gap inflates the earnings side. Both are labelled diagnostics; neither is proof of mispricing.

5. Published regression detail

PE 18.1656x -> 89.72 EUR; PBV 2.6787x -> 102.39 EUR; EV/EBITDA 23.5097x -> 319.58 EUR (extreme: substituted growth + vendor EBITDA basis; diagnostic only). Decimal DFR/tax policy approved; EV/EBITDA alternative pp-policy 22.3046x. Dataset regressions_multi_2026-01, SHA a894ea86...af1d9bf5, as-of 2026-01-01 (~302 days old). Classification: Not classified (no SEy published).

6. Benchmarks, sensitivities, limits

Electrical Equipment EUROPE industry aggregates: EVEBITDA 18.94x, EVEBIT 24.34x, PBV 5.71 (146 firms); Machinery 14.98x / 4.05. Labelled aggregates, not medians. Sensitivities: LOO, quartiles, group-NI 275 vs common 264, issuer EBITDA 390 / EBIT 257 vs vendor 680/578 - sensitivities.csv. Unresolved (disclosed): source certification of all fields, verified industry medians, uniform one-off normalization, EV claim/lease/LT-investment perimeter, human Spot_check PENDING.

Sources/reproducibility: relative/source_log.csv, evidence_review.md, regression_results.json, formula_checks.json; rebuild via PYTHONPATH=src python outputs/NKT.CO_2026-10-30/relative/build.py. Academic analysis only - not investment advice.
