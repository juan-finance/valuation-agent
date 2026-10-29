---
name: valuation-2-dcf
description: Stage 2 company DCF valuation using the course FCFE or FCFF rule, adjusted trailing earnings, explicit reinvestment, geographic risk, bottom-up beta, and a reconciled common-equity value. Use after the stage 1 data pack is available.
---

# Goal and required reading

Value ONE company using the stage 1 data pack and the supplied course materials. Read [methodology README](../../../methodology/README.md), then the complete [DCF procedure](../../../methodology/dcf_procedure.md) before calculating. The procedure incorporates Steps in Company Valuation.docx and records corrections to its internal inconsistencies. Do not treat unverified examples as current data.

Read [data sources](../../../methodology/data_sources.md), [sector adjustments](../../../methodology/sector_adjustments.md), [company universe](../../../methodology/company_universe.md), [QA checklist](../../../methodology/qa_checklist.md), and [report template](../../../methodology/report_template.md).

# Procedure

1. Fix valuation date, information cutoff, currency, units, historical years and share class. Inventory the stage 1 files; log unavailable inputs. Use five years of history. The Word document's t=2025 and t−1=2024 are worked-period labels, not instructions to roll dates forward silently.
2. Build five-year market and book capital-structure tables. Estimate market debt from fair value, a supported debt valuation or vendor estimate; use book debt only with justification. Use industry ratios as benchmarks, never average a currency amount with a percentage. Select and justify stable/target leverage.
3. Follow the course default: stable debt ratio → FCFE; unstable debt ratio → FCFF. Record stability evidence, funding policy and target path. Exclude dividend models for this nonfinancial universe. An alternative DCF is an optional cross-check.
4. Reconcile reported and company-adjusted EBIT and group net income item by item. Build comparable trailing figures when interim data are available. Review effective taxes over five years, separately from the marginal rate used for financing.
5. Construct recurring net capital expenditure, including PP&E, intangibles and recurring acquisitions where supported by the business model. Match D&A to adjusted earnings; do not capitalize R&D or add lease restatements in the course base case. Benchmark current/prior net capex ratios to industry and justify the selected forecast ratio.
6. Build NWC from balance-sheet components. Benchmark current/prior NWC/Sales to industry, select the documented company/industry average and forecast the NWC balance before its change. Apply the course floor max(raw ΔNWC, 0), retain raw changes and quantify the effect.
7. Calculate FCFF or FCFE explicitly. Reconcile group versus parent scope, reinvestment rates and beginning-book-capital ROE/ROC. Forecast growth from reinvestment × return; compare with analysts, historical extrapolation and the annual-report narrative.
8. Select a single-, two- or three-stage model under the inherited course heuristics; document exceptions. Transition growth, returns, reinvestment, leverage and discount rates consistently. Use only a growing perpetuity for the terminal value, with a coherent year n+1.
9. Build a common currency risk-free rate for Ke and Kd. Use bottom-up cash-corrected unlevered beta, revenue-weighted across businesses, and relever at the applicable market D/E. Compare a regression beta with its index, frequency and window disclosed.
10. Compute geographic revenue-weighted equity CRP. Base case: Ke = Rf + beta × mature ERP + weighted CRP. Show the beta-scaled alternative; use lambda only when exposure data support it. Separate equity CRP from sovereign default spread.
11. Estimate pre-tax Kd from actual rating, synthetic coverage rating and bond-yield checks. Assess any incremental sovereign exposure without double counting. Compute after-tax Kd using the marginal tax rate; construct market-weighted WACC including preferred financing if material.
12. Discount FCFE with Ke or FCFF with WACC. Reconcile operating value to common equity, including cash, debt, nonoperating claims, NCI, preferred securities and hybrids once each. Divide by current shares with an explicit dilution method and compare with the matching price.
13. Run low/base/high scenarios, discount-rate × terminal-growth sensitivities, and sensitivities for key operational assumptions. Rank 3–5 value drivers. Report terminal dependence, DCF-implied multiples, unusual-item effects, and data gaps. Never change assumptions merely to match the share price.
14. Complete stage 2 QA and hand off reproducible outputs to stages 3–4. Unresolved material data or conceptual failures must be labelled provisional, not passed.

# Outputs and implementation

Write under outputs/<ticker>_<valuation-date>/, relative to repository root:

- dcf_model.xlsx: an Inputs sheet for sourced assumptions; separate historical/reconciliation, reinvestment, forecast, discount-rate, equity-bridge, sensitivity and QA schedules. Link formulas to inputs; no embedded valuation assumptions in formulas. Mathematical constants are permitted. Recalculate and check errors.
- dcf_decisions.md: each judgment, alternatives, evidence, chosen method, source locator and value impact; include all course conventions and unresolved conflicts.
- source_log.csv: fields specified in data_sources.md; preserve stage 1 entries.
- qa_results.md: pass/fail/fixed/not applicable, evidence and any outstanding blockers for every applicable checklist item.
- dcf_summary.png: one readable picture of assumptions, growth stages, Ke/Kd/WACC, equity bridge and per-share value.

Use tested functions under src/ if available; create and test missing material valuation functions. Cover FCFE/FCFF signs, NWC floor, tax separation, leverage conversion, discounting, terminal conditions, preferred weights, bridge arithmetic and share units. Do not claim tests ran unless executed. Cite only literature/data actually opened; mark unverifiable references explicitly. The summary picture and report must reconcile to the workbook.
