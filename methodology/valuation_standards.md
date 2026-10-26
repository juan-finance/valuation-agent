# Valuation standards (house view)

## General
- All 20 companies report under IFRS. Use IFRS 16 consistently:
  if leases are in net debt, EBITDA must be post-IFRS 16.
- Valuation date = date of analysis. State it on page 1.
- Value in the company's reporting currency. Convert to EUR only for display.
- Output is a RANGE (low / base / high) plus a point estimate, never one number.

## DCF
- Explicit forecast: 5 years (utilities and renewables: 7-10 years because of
  long asset lives). Then terminal value.
- FCFF discounted at WACC. EV -> equity bridge: subtract net financial debt,
  hybrids/perpetual bonds (at least 50% or as justified), minorities, pension deficits,
  nuclear/decommissioning provisions where debt-like; add associates and JV stakes.
- Terminal growth: between 1.0% and the long-run nominal growth of the currency
  area, and never above the risk-free rate. Default 1.5-2.0% (EUR).
- Terminal value above 75% of EV must be flagged in the summary.
- Forecast assumptions must be based on company guidance, backlog or capex plans,
  historical trend and sector data. Each assumption needs a one-line reason.

## WACC
- Risk-free: 10-year government yield in the cash-flow currency, averaged
  over the last 5 trading days, with source and date.
- ERP: Damodaran's latest mature-market ERP, plus country risk premium
  weighted by revenue geography.
- Beta: Damodaran's Europe industry unlevered beta, relevered at the company's
  target D/E. Cross-check with a 5-year weekly regression against STOXX Europe 600.
  If the two differ by more than 0.3, explain.
- Cost of debt: from interest expense / average gross debt, cross-checked
  against bond yields where the agent can find them.
- Capital structure: market-value weights; use a target structure for
  utilities and renewables.

## Relative valuation
- Peers within the same bucket only. Minimum 4 peers where possible.
- Multiples: EV/EBITDA, EV/EBIT, P/E for all; plus the sector multiples below.
- Use the median, not the average. Show the range (25th-75th percentile).
- Use the same fiscal period for all peers (LTM and next-12-months where
  forward estimates are available from company guidance). Never mix.
- Without paid data, there is no analyst consensus. Say so and use LTM
  multiples as the primary set.

## Sector rules
- A (utilities): Sum-of-the-parts. Regulated networks via EV/RAB or
  EV/EBITDA, generation via DCF, retail via EV/EBITDA. Watch hybrids and minorities.
- B (renewables): Model capacity additions, load factors, capex per MW and
  asset-rotation gains separately. Check for recent capital increases and use
  the current share count.
- C (equipment makers): Normalize margins to mid-cycle. Model order backlog
  conversion. Treat warranty provisions and quality-cost one-offs explicitly.
- D (stable industrials): Standard DCF. Adjust for restructuring and
  acquisition-related items.
- E (steel): Use mid-cycle EBITDA (average over 5-7 years), P/B and EV/EBITDA.
  Show the DCF as a secondary view. Treat associates and minorities carefully.
- F (oil, gas, fuels): Explicit price deck (low/base/high) for Brent and gas;
  use EV/DACF, P/CF and dividend + buyback yield. Include decommissioning
  provisions. Neste: model refining margins and renewable-fuel margins separately.

## Scenarios and sensitivities
- Bear / base / bull with named drivers per bucket.
- WACC vs terminal growth table, plus one sector-specific table
  (e.g. oil price, power price, steel spread, EBITDA margin).
