# Sector adjustments and conventions (secondary file)
NOTE: The professor's lecture notes and the four stage skills in .agents/skills/ take
precedence. This file supplies only IFRS conventions, equity-bridge items and sector
adjustments. It does not set discount rates, growth rules or valuation methods.

## General conventions
- All 20 companies report under IFRS. Use IFRS 16 consistently: if leases are in net
  debt, EBITDA must be post-IFRS 16.
- State the valuation date on page 1.
- Value in the company's reporting currency. Convert to EUR only for display.
- The result is a range (low / base / high) plus a point estimate.

## Equity bridge items to check (where debt-like or asset-like)
- Subtract: net financial debt, hybrids/perpetual bonds (at least 50%, or as justified),
  minorities, pension deficits, nuclear and decommissioning provisions.
- Add: associates and JV stakes, financial and other non-operating assets.

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

