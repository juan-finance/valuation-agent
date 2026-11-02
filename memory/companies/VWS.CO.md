# Vestas (VWS.CO)  bucket C: equipment makers; reporting currency EUR, quote DKK (Nasdaq Copenhagen)

## Identity and perimeter (stage 1 — reduced input step, 2026-11-02)
- Vestas Wind Systems A/S; ISIN DK0061539921; single share class; FY = calendar year (FY2025 ended 2025-12-31).
- No parent/subsidiary or >20% cross-holder identified among candidates.
- Quote DKK 189.25 (2026-10-30); FX DKK 7.4735/EUR (ECB 2026-10-30). Shares 978.25m current (weighted basic 999m).

## Judgement calls (stage 3, relative_only deviation)
- Primary multiple: EV/EBIT (sector mapping), qualified — pre-associate EV only (peer associate/claim/lease consistency unresolved).
- Declared payout used for regression input (declared DPS DKK 0.74 ≈ EUR 0.10 / EPS 0.78 = 0.128), consistent with VER.VI precedent; consensus 3Y g_eps 32.41%, g_rev 8.34%; ROE on closing equity 20.12%.
- LT investments 739 recorded not deducted (earnings stay in denominators); NCI 14 book proxy.
- Membership interpretation: IEUR MSCI Europe IMI proxy accepted as Europe evidence for Europe-listed names (keeps NDX1/NKT/ANDR/IMI/ROR eligible); URTH required only for non-European World expansion. Deliberate divergence from ENR.DE run (which excluded IMI-only names) — see outputs evidence_review.md.

## Data quirks and source notes
- Vendor EBITDA 1501 vs issuer 2053 (−26.9% definitional gap) — EV/EBIT preferred over EV/EBITDA.
- Vendor EBIT 1067 = issuer EBIT before special items (issuer reported 1015; special −52 = 4.9% EBIT, below 10% normalization trigger).
- IMI and NKT have invalid EV denominators in the vendor data → EV multiples n=8 (still ≥6).
- Final peers (10, all Europe, 9 Tier1/2 + 1 Tier3, no relaxation): NDX1, WRT1V, IMI, G1A, ALFA, ENR, NKT, ANDR, LR, ROR.

## Latest result pointer
- outputs/VWS.CO_2026-10-30/ (relative_inputs.md, relative_summary.md, relative_report_VWS.CO.pdf, relative/*) — PROVISIONAL, QA-C not passed (8 source-qualification fails; Spot_check pending). Stage 3 elapsed ~n min; diagnostics: EV/EBIT mid DKK 162.16 (−14.3%), regression PBV DKK 125.66, PE mid DKK 252.63.

## Open questions for the user
- Acceptable to certify peers via the IEUR IMI proxy plus prior-run ISIN evidence, or is a fresh per-candidate ownership/event pass required before any non-provisional use?
