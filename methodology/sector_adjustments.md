# Sector adjustments and conventions

Use [DCF procedure](dcf_procedure.md) for valuation methods, growth, tax and discount-rate rules. This file adds sector assumptions and claim checks. The two-folder repository uses skills/ and methodology/; do not refer to an assumed .agents/skills/ layout.

## General conventions

State the valuation date, information cutoff, currency and units. Use reporting currency for the base valuation unless the assignment specifies otherwise; discount in the same currency and nominal/real basis. Convert to EUR only for presentation with a dated rate. Present low/base/high and a point estimate.

The supplied universe is intended for IFRS analysis; verify each issuer's reporting basis. Follow the Word document's base-case instruction: no extra R&D capitalization and no analytical lease restatement. Existing IFRS 16 accounting remains in place. Reconcile lease liabilities, right-of-use additions, lease D&A, interest and principal cash flows within the chosen reported basis. If leases are treated as financing debt, ensure their investment/depreciation and interest/principal treatment are consistent with FCFF/FCFE and avoid subtracting lease principal twice. EBITDA labelled post-IFRS 16 alone is not sufficient evidence of consistency. Record any material unresolved mismatch and its impact.

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
