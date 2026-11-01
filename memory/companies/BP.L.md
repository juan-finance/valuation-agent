# BP (BP.L)  bucket F: oil, gas and fuels; indicative reporting currency USD (verify)

Status: relative-only research; valuation checkpoint and QA limitations in outputs/BP.L_2026-10-30/. Entry format: see memory/README.md.

## Identity and perimeter (stage 1)
- verified ISIN / primary listing / share classes / fiscal year-end:
- listed subsidiaries, parent, >20% stakes (affects peer exclusions):

## Segment-to-Damodaran-industry mapping (stage 2, used for beta, debt, CapEx, NWC)
-

## Judgement calls and why (link to outputs/<ticker>_<date>/dcf_decisions.md)
-

## Data quirks and source notes
-

### FY2025 claim perimeter and earnings (added2026-11-01)
- fact: NCI20,948USDm includes hybrid15,955 and other NCI4,993: deduct once. Parent book53,052 versus common53,031 leaves21preference carrying-equity proxy. FY debt including leases72,529, leases14,571, cash36,556. Decommissioning provision12,253 is an explicit sensitivity, not automatically incremental base debt. Regression base retains associates; comparable EV needs a uniform removal when operating earnings exclude them.
- source: SEC BP2025 filing000031380726000006, R4, R5 and R29; outputs/BP.L_2026-10-30/relative/issuer_crosschecks.json
- confidence: high; status: verified issuer cross-check; valid_until: vintageFY2025, reverify before another valuation date; used for: EV bridge consistency.
- fact: Vendor FY revenue187,637 = issuer189,335 less production tax1,698. Vendor EBIT14,446 differs from issuer12,642; EBITDA30,168 is within1% of issuer PBIT+DDA30,464. Keep fields separate. Impairments6,037 materially distort earnings; underlying RC parentNI7,485 is a separately labelled sensitivity, not reportedNI55 or commonNI54.
- source: same filingR2 and BP fourth-quarter2025 results, source URLs in issuer_crosschecks.json
- confidence: high; status: verified source comparison; valid_until: vintageFY2025; used for: reported versus normalized analysis.
- fact: Ordinary ISIN GB0007980591, LondonGBP/GBX; each USADS six ordinary. AkerBP FY2025 reports BP ownership rounded16%, below the >20% target cross-holding exclusion; other ownership/events gates still need individual verification.
- source: BP issuer share-listing-information; AkerBP annual-report2025, https://akerbp.com/wp-content/uploads/2026/03/akerbp-annual-report-2025.pdf
- confidence: medium; status: sourced; valid_until: ownershipFY2025, identity until changed; used for: class and candidate checks.

## Latest result pointer
- recommendation_summary.csv:   (path, date)

## Open questions for the user
-
