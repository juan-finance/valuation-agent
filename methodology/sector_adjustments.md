# Sector adjustments and conventions

Use [DCF procedure](dcf_procedure.md) for DCF methods, growth, tax and discount-rate rules. For relative valuation use [comparables procedure](comparables_procedure.md) and [regression procedure](regression_procedure.md), with the additional mapping below. This file adds sector assumptions and claim checks. The two-folder repository uses skills/ and methodology/; do not refer to an assumed .agents/skills/ layout.

## General conventions

State the valuation date, information cutoff, currency and units. Use reporting currency for the base valuation unless the assignment specifies otherwise; discount in the same currency and nominal/real basis. Convert to EUR only for presentation with a dated rate. Present low/base/high and a point estimate.

The supplied universe is intended for IFRS analysis; verify each issuer's reporting basis. Follow the DCF base-case policy: no extra R&D capitalization and no analytical lease restatement. Existing IFRS 16 accounting remains in place. Reconcile lease liabilities, right-of-use additions, lease D&A, interest and principal cash flows within the chosen reported basis. If leases are treated as financing debt, ensure their investment/depreciation and interest/principal treatment are consistent with FCFF/FCFE and avoid subtracting lease principal twice. EBITDA labelled post-IFRS 16 alone is not sufficient evidence of consistency. Record any material unresolved mismatch and its impact.

Recurring acquisitions may be part of reinvestment when supported by the business model; they are not automatically excluded. Match acquisition-related forecast growth to its cash investment and avoid repeating one-off purchase prices.

## Equity bridge checks

Use a gross-debt-plus-excess-cash bridge or a reconciled net-debt bridge, never both. Subtract a claim only once and only if not already captured in the cash flows or another bridge item.

- Debt: financial debt at market/fair value or a justified proxy, with lease perimeter disclosed.
- Preferred securities: separate market-value WACC component where relevant; no automatic preferred-dividend tax shield; remove the preferred claim from common equity once.
- Hybrids/perpetuals: inspect terms and supported debt/equity allocation; remove the old automatic minimum 50% deduction. Equity-like classification does not make a security an existing common share.
- NCI: subtract a supported minority claim from consolidated operations/group FCFE; do not subtract again if forecasts already isolate parent entitlement.
- Pensions, nuclear/decommissioning obligations and other provisions: separate operating expenditure from debt-like claims, including tax and timing as material; do not subtract obligations whose settlement costs have already reduced DCF cash flows.
- Associates/JVs and financial investments: add their standalone value only if associated earnings/distributions have been excluded from operating value. For consolidated subsidiaries keep operations and NCI coherent.
- Cash: add only cash/nonoperating assets not already reflected in operating cash flows or net debt; identify restricted and operationally required cash separately.

## Sector adjustments (buckets in company_universe.md)
- A (utilities): Consider sum-of-the-parts as a cross-check (regulated networks via
  EV/RAB or EV/EBITDA, generation via DCF, retail via EV/EBITDA). Watch hybrids and minorities.
- B (renewables): Model capacity additions, load factors, capex per MW and asset-rotation
  gains separately. Check for recent capital increases and use the current share count.
- C (equipment makers): Normalize margins to mid-cycle. Consider order-backlog conversion.
  Treat warranty provisions and quality-cost one-offs explicitly.
- D (stable industrials): Adjust for restructuring and acquisition-related items.
- E (steel): Use mid-cycle EBITDA (5-7 year average). Treat associates and minorities
  carefully. Few listed peers exist in the universe: say so.
- F (oil, gas, fuels): Use an explicit price deck (low/base/high) for Brent and gas.
  Include decommissioning provisions. Relevant multiples include EV/DACF and P/CF.
  Neste: model refining and renewable-fuel margins separately.

## Scenario drivers by bucket (for stage 4)
- A: power prices, regulated returns. B: capex per MW, power prices. C: margins, order intake.
- D: organic growth, margins. E: steel spreads. F: oil/gas price, refining margin.

## Relative valuation primary multiples

These are project business defaults, not verified current company metrics or universal sector rules. Assess actual denominators and peer coverage before use. Do not claim electrical/cable businesses are all asset-light or that utility RAB equals book equity without company evidence.

| Target business | Comparable-method primary | Ordered cross-checks | Main interpretation |
| --- | --- | --- | --- |
| Renewable power: EDPR, Ørsted | EV/EBITDA | PBV | Depreciation and disposals can distort NI; EBITDA still omits reinvestment |
| Integrated utilities: Iberdrola, Enel, SSE, ENGIE, Verbund | EV/EBITDA | PE, PBV | Assess regulated/merchant mix, leverage and minority interests |
| Wind/power equipment: Vestas, Siemens Energy | EV/EBIT | EV/Sales, PE | Recovery/one-off costs require consistent margin sensitivity |
| Electrical equipment/cables: Schneider, Prysmian, NKT | PE | EV/EBIT | Match earnings quality, product mix and investment intensity |
| Oil/gas: TotalEnergies, Shell, BP, Equinor | EV/EBITDA | EV/CF, PE | Align commodity-cycle assumptions and cash-flow definitions |
| Renewable fuels: Neste | EV/EBITDA | EV/Sales | Separate renewable-fuel/refining economics; verify profitability at cutoff |
| Gases/machinery: Air Liquide, Alfa Laval | PE | EV/EBIT | Match recurring earnings and business-specific margins |
| Steel: ArcelorMittal | EV/EBITDA | PBV | Show cycle-normalized sensitivity separately from common FY base |

If denominator is nonpositive/near-zero or valid peer count<10, try cross-checks in order and document; do not override with an attractive valuation. Regression selection remains its four-model typicality/adjusted-R² procedure and may choose a different multiple from this peer-method default. Keep both results visible.

## Candidate business tiers

| Target business | Tier 1 search seeds | Tier 2 economic extension |
| --- | --- | --- |
| Renewable power | Listed renewable developers/IPPs: Acciona Energía, ERG, Solaria, Brookfield Renewable | Integrated utilities with material renewable fleets |
| Utilities | Integrated/regulated operators: E.ON, EDP, Endesa, Naturgy, Fortum, National Grid | Grid operators such as Terna, Redeia, Elia; developed-market utilities outside Europe |
| Power equipment | Nordex, GE Vernova, Mitsubishi Heavy Industries | Electrical equipment such as ABB, Schneider, Hitachi, Eaton |
| Cables/electrical | Cables: Nexans, Sumitomo Electric, Furukawa Electric; electrical: ABB, Legrand, Eaton | Other electrical product line, then economically similar capital goods |
| Oil/gas | Eni, Repsol, OMV, ExxonMobil, Chevron | Large E&P and LNG |
| Renewable fuels | Darling Ingredients, Valero, Galp, Orlen | Integrated oil with refining exposure |
| Industrial gases | Linde, Air Products, Nippon Sanso | Similar industrial economics |
| Machinery | GEA, Atlas Copco, Wärtsilä, Xylem | Adjacent machinery with matched cyclicality |
| Steel | Nucor, voestalpine, SSAB, thyssenkrupp | Adjacent material businesses with matched cyclicality |

Names are illustrative retrieval seeds, not verified eligible selections. Check index membership, listing history, size, MSCI developed-market classification, restructuring and ownership. A name can be unsuitable for one target but valid for another; never include a target itself. Emerging-market names in earlier peer lists must not be grandfathered in.

## Relative accounting consistency

- Comparable base EV removes nonoperating associates; regression base EV does not. Retain both definitions and invert each consistently in its own equity bridge. Harmonized expanded EV is possible only with explicit uniform data and a reconciliation.
- Match reported EBIT/EBITDA and IFRS 16 debt/lease scope across all observations. For non-European peers, explain IFRS/US GAAP lease and CFO classification differences; irreconcilable data cannot support an unqualified primary comparison.
- Relative base earnings are consistently reported; DCF-adjusted earnings and mid-cycle sector normalizations are separate sensitivities. An exceptional item >10% of abs(EBIT) triggers a normalized parallel field, not an unexplained mix of adjusted and reported figures.
- Growth scaling, margin scaling and ROE scaling require valid positive drivers and sufficient usable peers; they do not correct every business difference.
- EV/CF must identify CFO, unlevered CFO, DACF or FCFF. Reported CFO can be financing-sensitive; no automatic equivalence to enterprise cash flow. Preserve a consistently defined supplemental ratio and qualify its interpretation.
- RAB, MW and replacement costs require comparable definitions (operating versus pipeline capacity, ownership, regulatory perimeter). Tobin's Q is unavailable without genuine replacement-cost evidence.
