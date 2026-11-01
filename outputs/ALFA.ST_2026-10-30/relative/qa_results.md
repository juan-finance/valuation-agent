# QA block C — ALFA.ST relative valuation (2026-10-30, standard, published_damodaran)

## Shared data and independence
- [x] Scope: single target, `outputs/ALFA.ST_2026-10-30/relative/`. Candidates from own research (no group workbook).
      Route `web_minimum` reused; full universe = IEUR MSCI Europe IMI proxy (labelled). One valuation/FX date
      (2026-10-30, ECB SEK 10.978); FY2025 base, TTM/forward kept separate.
- [x] Target list / selected peers / regression market kept distinct; buckets not used as GICS.
- [~] Cap reconcile: ALFA 0.001%; most peers <0.5%. ATCO.A +4.25% and EPI.A +4.75% flag — explained: dual A/B share
      classes, vendor "Shares Outstanding" counts only A shares while market cap covers both classes; vendor mcap
      retained (correct group total), flag recorded in candidate_gates.csv.
- [x] Field-level sources logged (source_log.csv); membership vintage noted; no per-row source switching.
- [x] >50% benchmark gap: Damodaran Europe "Machinery" industry median not resolvable from registered library
      (industry_row coverage) — limitation recorded, not faked.
- [x] Human Spot_check status: PENDING (recorded as pending, not claimed performed).
- [x] No DCF-proximity/size weighting anywhere (relative_only run; no DCF exists for this target).

## Comparable method
- [x] 10 distinct qualified peers (G1A, ATCO.A, WEIR, ROR, IMI, SMIN, BUCN, KRN, ABBN, HLMA).
- [x] Hard filters: EUR1bn min (all ≥3.4bn), size band 0.1–10x (KSB out on membership, BCHN 1.73bn out on band,
      FLS out on >2 missing dims), developed-market membership via IEUR/URTH proxies; ownership/restructuring
      audit = provisional, flagged not waived.
- [x] Tier composition: 9 Tier1–2 + 1 Tier3 (HLMA); ≥8 T1-2 ✓, T3≤2 ✓, 10/10 Europe-listed (≥5 ✓).
- [x] 30-candidate pool, exclusions + reasons in candidate_gates.csv, scores in peer_selection.json.
- [x] Score weights=8 dims sum 1; pool-only 5/95% winsorization; renormalize on missing dims; zero-variance log.
- [x] Growth: web route fundamental ROE×(1−payout) uniformly (consensus-gap rule n/a on web route).
- [x] Full multiple set computed; relative_pe and tobins_q marked unavailable (no index PE / replacement cost).
- [x] Every used multiple ≥6 valid: pe/pbv/ps n=10, ev_* n=8. Median/mean/p25/p75 in multiples_summary.csv;
      no mean–median skew >25% on primaries (pe 1.5%, pbv 1.5%).
- [x] Raw and adjusted values both shown; PEG uses percentage-point growth on FY basis.
- [x] Primary = PE (growth-scaled, n_adj=10) per gases/machinery mapping; EV/EBIT + others cross-checks.
- [x] EV-to-equity inverse matches numerator (debt incl. leases + NCI − cash; associates=0 flagged);
      SEK/share on 413.33m shares; upside vs 545.60 quote.
- [x] Three reproducibly random EV recomputes (ROR, SMIN, WEIR): manual mcap+debt+NCI−cash == stored EV, exact.
- [x] ISINs registry-mapped; issuer-page verification PENDING (flagged in comparables.csv flags).
- [x] Sensitivities: raw vs scaled per multiple; quartiles labelled peer dispersion, not CIs.
- [x] comparables.csv, multiples_summary.csv, comparables_report.md + comparables_audit.xlsx written.

## Regression method (published_damodaran route)
- [x] Equations via `datasets.equation_for('Sweden', dep, '2026-10-30')` → EUROPE exact match,
      regressions_multi_2026-01, ~10 months older than valuation date (flagged as limitation).
- [x] Integrity check findings recorded (GLOBAL anomalies noted; EUROPE equations unaffected; no anomaly on used eqs).
- [x] Inputs follow file definitions: analyst consensus g_eps 12.72% / g_rev 9.41% (NO fundamental substitution
      needed), observed beta 0.75, payout 0.425≥0, roe closing parent book, dfr/tax_rate decimals (approved),
      roic = EBIT(1−t)/(equity+debt−cash).
- [x] Unit policy: decimal (user-approved). Both policies computed; PE/PBV identical (no dfr/tax terms);
      EV/EBITDA differs 18.3% (>10% → material, decimal policy applied per approval, both recorded).
- [x] No SEy output: classification/adj_r2/p-values/A-B-C/D1-D10 = n/a_published_route; deviation + R2 shown.
- [x] Workbook Equations sheet uses live formulas; independent formula-eval == predict() <1e-9 for all three.
- [x] Chosen model PBV (highest published R2 0.423) → SEK 343.26; alternatives PE 434.06, EV/EBITDA 710.47.
- [x] Limitations section covers market-wide scope, low R2, analyst-growth definition, vintage, undocumented EV
      definition, no residual dispersion.
- [x] valuation_multiples.csv, regression_valuation.xlsx, valuation_summary.md written (no DATA_BASE_MSCI.xlsx
      under this route — stated).

## Data library
- [x] datasets.resolve/equation_for used; no fallback needed (EUROPE exact); sha256 + dataset id in source_log.

STATUS: PROVISIONAL — human Spot_check, ISIN issuer verification, ownership/event audit outstanding.
