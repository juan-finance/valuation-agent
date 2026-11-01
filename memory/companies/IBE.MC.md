# Iberdrola (IBE.MC)  bucket A: utilities; reporting currency EUR

Status: relative_only run done 2026-11-01 (provisional). Entry format: see memory/README.md.

## Identity and perimeter (stage 1)
- ISIN ES0144580Y14 (registry-mapped, issuer-page verification pending); BME listing, EUR, Dec year-end; shares 6,681,227,377 at 31.12.2025 (vendor: 6,670m).
- Key listed-subsidiary relation: Endesa ~70% owned by peer candidate ENEL (not by Iberdrola) — hard exclusion. Avangrid/Neoenergia/ScottishPower are consolidated subsidiaries, no separately listed peer risk.
- Ratings: Moody's Baa1 / S&P BBB+ / Fitch BBB+ (issuer FY2025 release).
- Source: Iberdrola FY2025 CNMV filing + press release 2026-02-25; confidence high.

## FY2025 fundamentals (two bases — definitions differ, keep both)
- Vendor (stockanalysis, FY2025, EUR m): revenue 44,076; EBITDA 14,700; EBIT 9,979; NI to common 6,055; equity 50,068; NCI 13,351; debt 59,407 (incl. leases 5,095); cash 3,670; CFO 11,635; capex 8,081; beta 0.45; g_eps 9.15%, g_rev 4.05%.
- Issuer: revenues 45,546.8; EBITDA 16,592.4 reported / 15,684 adjusted; EBIT 10,276.4; net profit 6,285.0 / adjusted 6,749; equity 63,419; net fin debt 51,755 (adj 50,182); EPS 0.925; ROE 12.46%.
- Vendor NI-to-common 6,055 = reported 6,285 − 230 hybrid-coupon deduction (perpetual subordinated notes) — a REAL claim on common, not an error. [confidence: high]
- SCRIP DIVIDEND ("Retribución Flexible"): CF dividends paid only 1,275 (payout 0.21) — do NOT use as payout. Declared basis = DPS 0.68 × 6,681m ≈ 4,543 → payout 0.75. [confidence: high]
- Source: outputs/IBE.MC_2026-10-30/relative_inputs.md; 2026-11-01.

## Judgement calls (relative run 2026-11-01)
- PE regression payout input = declared-dividend basis 0.75 (economically meaningful under scrip); CF-paid basis flagged.
- Regression chosen model PBV (highest published R2 0.423) → EUR 16.96; peer EV/EBITDA median 12.56x → EUR 17.32 mid; price 22.18. Both read ~22-24% rich.
- IBE trades at premium on all headline multiples (EV/EBITDA 14.8x vs 12.6x peers) — consistent with higher growth 9.8% vs ~3%, ROE 12.1% vs ~10.6%, lower leverage 3.8x vs ~5.0x.
- Source: outputs/IBE.MC_2026-10-30/relative/; confidence medium.

## Data quirks and source notes
- stockanalysis slug bme/IBE. Vendor EBITDA ≈11-13% below issuer adjusted/reported (definition scope); sensitivity retained.
- Spain was missing from the 2026-10-30 dated cache → country-only top-up (Spain A3: spread 0.95%, CRP 1.48%, total ERP 5.68%, EUROPE equations). Other EU targets reuse same top-up.

## Latest result pointer
- outputs/IBE.MC_2026-10-30/relative_report_IBE.MC.pdf + relative_summary.md (2026-11-01, provisional — human Spot_check pending)

## Open questions for the user
- None.
