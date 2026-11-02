# Evidence review — VWS.CO relative valuation 2026-10-30

Status: DRAFT. Numeric pipeline complete; source-qualification gates below are not all cleared. Human Spot_check pending; nothing here certifies the selected names as ten fully qualified peers.

## Membership and country

- Europe-listed candidates: verified membership = dated IEUR MSCI Europe IMI proxy holdings file (Oct 29 2026, latest published) in `cache/market/2026-10-30/universe.csv`. This is the cache's established universe evidence; it is a fund-holdings proxy for index membership, labelled as such, not an MSCI constituent file.
- Interpretation recorded for this run (differs from the ENR.DE run): for the funnel's Europe-first step, IEUR IMI membership is accepted as Europe membership evidence for Europe-listed names — including IMI small/mid caps absent from the URTH standard-index proxy (NDX1, NKT, NEX, ANDR, IMI, SUN, WEIR, ROR). The URTH World standard proxy (dated 2026-10-29, `world_candidate_membership.csv` / `world_pool_membership.csv`) is required only for the permitted developed-market World expansion of non-European listings (ETN confirmed; GEV confirmed but event-excluded). No Europe-listed candidate was relaxed to the World step.
- ETN (Eaton, US listing) is the only non-European name retained in the pool; it was not needed — selection completed at the Europe step without World expansion.

## Hard exclusions applied (fixed before valuation)

- SIE Siemens — material FY2024-25 Altair acquisition (~USD10bn announced; https://press.siemens.com/global/en/pressrelease/siemens-strengthens-leadership-industrial-software-and-ai-acquisition-altair) plus India perimeter change; FY base noncomparable.
- PRY Prysmian — Encore Wire acquisition completed July 2024 (https://www.prysmian.com/en/media/press-releases/prysmian-completes-the-acquisition-of-encore-wire); FY24/25 perimeter change.
- ABBN ABB — FY2025 Robotics discontinued-operation/divestment plus Gamesa Electric acquisition (https://global.abb/group/en/investors/overview/acquisitions-and-disposals).
- GEV GE Vernova — FY2024 spin-off; less than two full comparable years (trading history/figure comparability).
- SMIN Smiths — FY2025/26 material portfolio disposal programme; no harmonized continuing basis.
- NEX Nexans — Lynxeo 2025 sale (EV525m, https://www.nexans.com/regulated-informations/nexans-completes-the-sale-of-lynxeo-to-latour-capital/) plus AmerCable divestment; discontinued-operation perimeter.
- SKF.B SKF — announced automotive separation/restructuring; consistent FY base not established.
- ATCO.A Atlas Copco — class capitalization reconciliation +4.25% (>2% tolerance): vendor dual-class perimeter unresolved; excluded, not fixed by raising the threshold.
- EPI.A Epiroc — class capitalization reconciliation +4.75% (>2%); same treatment.
- None below the EUR 1bn minimum; none with >2 missing scoring dimensions in the final pool.

## Selected-peer official ISIN evidence and business review

All selected-peer ISIN URLs below were opened previously during the ENR.DE run (issuer or exchange pages, not directories) and are reused; no new page was opened this run. Economic descriptions originate own business research and vendor profiles. None of the selected names is a Vestas parent/subsidiary or a >20% cross-holder identified; complete two-way ownership/event certification for every candidate has NOT been completed — this remains an open gate, not a waiver.

|Peer|Tier|ISIN|Identity / business evidence|
|---|---|---|---|
|Nordex|1|DE000A0D6554|Direct wind-turbine peer. Acciona 47.08% parent (not VWS-related): https://www.nordex-online.com/en/2022/06/nordex-se-nordex-se-resolves-on-capital-increase/ ; FY2025 report pp105-106/314.|
|Wärtsilä|1|FI0009003727|Power generation/engines/services, substantial marine mix. Investor AB 17.7% FY2025: https://live.deutsche-boerse.com/equity/wartsila ; FY2025 note 6.3: ANCS disposal sales 127m; Gas Solutions announced disposal — small noncore portfolio, materiality judged acceptable.|
|IMI|2|GB00BGLP8L22|Fluid-control valves/actuators. RNS 2025-03-10 Alecta 3.03%: https://www.londonstockexchange.com/en/news/article/IMI/holding-s-in-company/16933526 ; Truflo Marine sale announced Nov 2025 (EV GBP225m, expected 2026) — recorded, not assumed no-event.|
|GEA|3|DE0006602006|Process/food machinery, different end market (Tier 3). 2026 organization change announced FY2025: https://www.gea.com/en/company/investor-relations/share-information/share-price/|
|Alfa Laval|2|SE0000695876|Heat transfer/rotating equipment energy/industry. Winder 29.53% FY2025 governance, independent of VWS: https://www.boerse-frankfurt.de/aktie/alfa-laval|
|Siemens Energy|1|DE000ENER6Y0|Power generation/grids/wind (Gamesa) — batch target used as peer (allowed: eligible other targets, never the target itself). 2023 Siemens spin-off outside FY2024-25 comparison period; FY ends September: https://www.siemens-energy.com/global/en/home/investor-relations/share.html|
|NKT|2|DK0010287663|Power transmission cables; home-market (Copenhagen) comp. Batch target as peer: https://nkt.com/investors/share-and-shareholders|
|Andritz|2|AT0000730007|Hydro/process capital equipment/services. Custos/Leitner 31.5%, listed 2001: https://www.andritz.com/group-en/investors/share ; FY2025 disclosed restructuring recorded, not assumed absent.|
|Legrand|2|FR0010307819|Electrical infrastructure equipment. Seven 2025 bolt-ons ~EUR500m acquired annual sales recorded: https://www.legrand.com/en/group/strategy/targeted-acquisitions|
|Rotork|2|GB00BVFBZH21|Flow-control actuators, energy exposure. UK listing; no target relationship identified.|

## Candidate rejections and nonselected pool

All 26 candidates (plus target) and exact numerical filters are preserved in candidate_gates.csv. Nonselected eligible names (SUN Sulzer, METSO, WEIR, SAND — ranked alternatives; ETN — World-expansion reserve not needed) are not silently deleted. Event-based deferred rows carry conservative unresolved-perimeter exclusions (ABB Robotics/Gamesa, Prysmian Encore, Nexans Lynxeo, Siemens Altair, GE Vernova spin, SKF automotive separation, Smiths disposals), not assertions that all acquisitions inherently disqualify. **No lazy-exclusion approval exists: full ownership/event/history certification for every candidate has not been completed; numeric 10 must not be represented as ten fully qualified peers.**

## Benchmark and unit-policy review

Resolver Denmark→EUROPE exact; industry labels: Machinery (closest, 210 firms), Green & Renewable Energy (60), Electrical Equipment (146). January 2026 files as-of 2026-01-01, ~304 days old. Published ratios, not verified medians — median verification unavailable, benchmark comparison stays qualified. Peer EV/EBIT median 18.96 vs closest published Machinery/Electrical ratios in industry_benchmarks.json. EUROPE PBV equation has no DFR/tax terms (both unit policies identical); PE likewise; EV/EBITDA alternative percent-point policy preserved in regression_results.json — decimal policy approved.

## Review gates

Three reproducibly random EV arithmetic checks (seed 20261030) pass; associates remain unavailable and cash/NCI proxies are not validated fair values. Human Spot_check is **pending**, not performed or waived. Numerical workbook/library agreement cannot certify source qualification. Outstanding: full candidate ownership/event/history certification, authentic matching industry medians, substantiated uniform normalization, peer associate/lease/claim consistency. Do not use numerical prices as an unqualified fair-value conclusion until these evidence gates are cleared.
