# Equinor (EQNR.OL)  bucket F: oil, gas and fuels; reporting currency USD (verified)

Status: stage 3 relative_only run done 2026-11-01 (provisional, QA-C not passed). Stages 1/2/4 skipped by approved deviation.

## Identity and perimeter (stage 3 run facts)
- ISIN NO0010096985; primary listing Oslo (OSL:EQNR); stockanalysis slug `osl/EQNR`. FY = calendar year. Reports USDm, trades NOK. [source: stockanalysis + Equinor SEC 6-K, 2026-11-01; confidence: high]
- Norwegian state (Olje- og energidepartementet) holds ~67%; no listed subsidiary; XOM held ~69.6% of peer candidate IMO (excluded cross-holding). [confidence: medium — verify at next run]

## FY2025 inputs used (USDm; vendor stockanalysis, issuer 6-K cross-checked)
- sales 105828; EBIT 26437 (issuer net operating income 25352 — vendor 4.3% higher, recorded not substituted); EBITDA 35311; CFO 19971; capex 13994; common equity 40424; debt incl leases 31221; cash&ST 19333; NCI 74; LT investments 15343 (excluded from EV, flagged); parent NI 5043 (group 5058 incl NCI15); EPS 1.94 / DPS 1.50; dividends paid 4791.
- Petroleum effective tax 79.84% (tax 20030 / pretax 25088) — far above European peers; keeps regression DFR/tax dispersion material. [confidence: high]
- Market: price 447.5 NOK, shares 2380m, cap NOK 1,065,410m ≈ EUR 102.8bn; USD→NOK 9.2302 (ECB 2026-10-30); EV NOK 1,175,791m.
- Vendor 5Y beta −0.65 (negative, implausible) → replaced by bottom-up relevered 0.4769 (Oil/Gas Integrated EUROPE cash-corrected unlevered 0.41, marginal 40%, market D/E). Peers' vendor betas also anomalous.

## Stage 3 results (diagnostic only; QA-C 30 PASS / 9 FAIL / 9 N/A)
- Peers (all Tier1, 8 Europe): REP SHEL TTE OMV ENI XOM BP AKRBP COP VAR.
- Primary EV/EBITDA unscaled (rule 118): peer median 7.468x → indicative 976.37 NOK (+118% vs 447.5; qualified, not a conclusion). Regression chosen PBV (pub R² 0.423) → 301.01 NOK (−33%).
- Outputs: outputs/EQNR.OL_2026-10-30/relative/ ; report relative_report_EQNR.OL.pdf + relative_summary.md.

## Data quirks and source notes
- stockanalysis slugs: Oslo = `osl/` not `ose/`; Euronext Paris = `epa/`; GALP Lisbon 404 on 2026-11-01.
- 'Total Common Equity' label missing on several oil tickers — fall back to "Shareholders' Equity"; NCI = Shareholders' Equity − Total Common Equity when no Minority Interest line.
- EV bridge: use 'Cash & Short-Term Investments' uniformly; LT investments excluded.

## Latest result pointer
- outputs/EQNR.OL_2026-10-30/relative/valuation_multiples.csv (provisional)

## Open questions for the user
- Resolve human Spot_check + source qualification gates before any qualified comparable conclusion.
