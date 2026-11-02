# SSE (SSE.L)  bucket A: utilities; reporting currency GBP (verified; LSE quote in pence)

Status: relative_only run done_provisional 2026-11-02 (outputs/SSE.L_2026-10-30/). Human Spot_check pending.

## Identity and perimeter (stage 1)
- ISIN GB0007908733, LSE:SSE, single class, GBP; FY ends 31 March (Mar-2025 = FY2025 basis, not calendarized).
- 2026 equity raise: shares ~1.21bn (+7.1% QoQ) — use current count for market value.
- Listed subsidiaries/parent: none; Tier-3 exposure n/a. Segments: SSEN Transmission/Distribution (regulated, ~£12.9bn RAV 100% basis), renewables, thermal/flex, customer solutions.

## Judgement calls and why
- Vendor "Total Debt" 10,712 appears to include equity-classified hybrid capital (73.7 coupon to other equity holders; issuer net debt 9,513.9, adjusted net debt+hybrid 10,186.7). Uniform vendor EV bridge kept across peers; disclosed, not harmonized.
- Payout: declared basis 0.597 (DPS 64.2p x 1,106.3m shares) used for published-route input; CF-paid 0.40 underweights final-dividend timing.
- Vendor EBITDA 2,850 sits between issuer reported 2,738.3 and adjusted 3,349.3 — vendor basis headline, sensitivity retained.
- Peer set (Europe step, no relaxation): RWE, EDP, IBE, ANE, NG, A2A, NTGY, EOAN, ORSTED, TRN. ELE hard-excluded (ENEL subsidiary); CEZ unavailable/EM; ERG/SLR/GRE/SCATC/DRX below €3.80bn band floor.

## Data quirks and source notes
- stockanalysis vendor EBIT = EBITDA − D&A exactly (2,250) vs issuer operating profit 1,962.2 (+14.7% flag; adjusted op profit 2,419.2 recorded).
- Issuer cross-check ties: revenue 10,131.9 and attributable NI 1,189.4 exact (LSE RNS 4968J + sse.com FY25 preliminary PDF, income statement p.46).
- g_eps 15.19% / g_rev 7.71% analyst consensus used in regression (pool scoring uses fundamental growth, uniform rule).
- Mar-year-end vs Dec peers — flagged, not adjusted.

## Latest result pointer
- outputs/SSE.L_2026-10-30/relative_summary.md + relative_report_SSE.L.pdf (2026-11-02).
  EV/EBITDA peer median 11.78x → £19.28 mid vs price £26.27 (−26.6%); published PBV → £22.98 (−12.5%).

## Open questions for the user
- Whether vendor hybrid-in-debt treatment should be harmonized (affects dfr and EV bridge) — currently uniform-vendor.
