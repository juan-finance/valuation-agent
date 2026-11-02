# Verbund (VER.VI)  bucket A: utilities; reporting currency EUR

Status: stage 3 relative_only run 2026-11-02, provisional (QA-C not passed; human Spot_check pending).

## Identity and perimeter (reduced input step)
- Verbund AG, Vienna (vie/VER), ISIN AT0000746409, EUR. 347,415,686 shares; Republic of Austria 51%.
- FY2025 calendar year. Vendor vs issuer: revenue 8,033 vs 8,013.6; EBITDA 2,715 vs 2,737.5; EBIT 2,108 vs 2,112.3; NI 1,489 = Group result; common equity 10,341 (group 11,331.2 incl. NCI 990).
- Austrian windfall-profit levy EUR135.9m inside FY2025 cost base.
- Issuer source: VERBUND integrated annual financial report 2025 (verbund.com), URL in relative_inputs.md.

## Data quirks and source notes
- Vendor beta 0.14 atypically low; used as observed, flagged.
- Consensus growth negative (g_eps -4.51%, g_rev -0.98%) — normalization off 2022-24 price spike; PEG unusable.
- Issuer net debt 2,818.1 vs vendor-derived 2,386 — different perimeter; recorded not mixed.
- Payout: FY2025 declared DPS 2.00/EPS 4.29 = 0.466; cash-paid basis 0.89 (special dividend).

## Latest result pointer
- outputs/VER.VI_2026-10-30/relative/: peer EV/EBITDA mid EUR 77.91; regression PBV EUR 59.61; price EUR 69.50. Provisional.
- Peer pool: EDPRpool cached extracts reused + EVN/TRN/REE/SRG/IG fetched 2026-11-02 into EDPRpool_*.
