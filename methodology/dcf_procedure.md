# Complete DCF procedure

Read this file in full before executing skills/SKILL-DCF.md. Labels distinguish **Word requirement**, **retained skill convention**, and **technical clarification**. The Word document is the procedural reference; errors and ambiguities are resolved explicitly below rather than silently propagated.

## Contents

1. Scope, dates and capital structure
2. Adjusted earnings and taxes
3. Net capital expenditure
4. Working capital
5. Cash flows, returns and growth
6. Growth stages and terminal value
7. Risk-free rate and cost of equity
8. Cost of debt and WACC
9. Discounting and common-equity bridge
10. Sensitivities and deliverables
11. Conflict register and reference evidence

## 1. Scope, dates and capital structure

**Word requirement.** Use five years wherever a historical trend is requested. Its t=2025 and t−1=2024 refer to annual comparison periods. Record the assigned valuation date separately; build trailing financials only from information available at the cutoff. Confirm company, ISIN, primary exchange, share class, price date, reporting currency and currency units. Do not substitute an ADR price without the ADR ratio.

For each of five year-ends, show market equity E, market debt D (or labelled proxy), D/(D+E), book debt, book equity and the book debt ratio. Align prices, debt dates and units. Use E = price × actual shares outstanding at that date. P/E × earnings is only a cross-check when the earnings period, share class and equity scope match; it is unusable for negative earnings or inconsistent EPS definitions.

Debt hierarchy:

1. Prefer disclosed fair value for the relevant financial-debt perimeter; show book-to-fair-value differences. Compare the resulting debt ratio with the matching Damodaran European industry ratio.
2. If incomplete, use quoted bond prices plus supported values for nontraded borrowings, or estimate debt value by discounting contractual coupons and principal at a current comparable borrowing rate. Document maturity and coupon assumptions.
3. A vendor market-debt estimate can supplement this, with date and perimeter reconciled. Compare like-for-like debt amounts and ratios separately.
4. Use book debt as a proxy if fair value is unavailable and most debt is floating-rate/short-term or bonds are marginal, with a reason and sensitivity if material.

**Technical clarification.** The Word's proposed average of book debt and an industry debt ratio mixes units. Do not implement it literally. Compare the company and industry ratios; if using an industry target delta, a ratio-implied amount is D = delta/(1−delta) × E. Label this a target-derived estimate, not observed market debt. No mechanical averaging is required.

Judge stability from range, year-to-year changes, trend, material acquisitions/disposals and management's leverage/rating policy. No universal numerical stability threshold is provided: state and justify a company-specific criterion. Select a target ratio from company evidence and industry comparisons. If debt is unstable, specify the transition to the long-run target rather than treating unstable historical leverage as constant.

**Word and retained skill rule.** Stable delta → FCFE; unstable delta → FCFF. This is the course default, not a claim that finance theory prohibits other choices. Exclude dividend models for this nonfinancial universe. Document an optional second-method cross-check and any difference.

## 2. Adjusted earnings and taxes

**Word requirement.** Start with the company's adjusted operating profit and adjusted group net income. Show reported figure, each signed adjustment, tax/NCI effect where relevant, and adjusted figure. Use the company's reconciliation: restructuring, impairment, disposal gains and other adjustments must have amounts and page/note references. Investigate recurring costs labelled exceptional; record a separate normalization if justified rather than silently changing the reported reconciliation.

For comparable interim periods:

`Trailing adjusted metric = latest FY adjusted metric − prior-year comparable YTD adjusted metric + current-year YTD adjusted metric`.

Apply to EBIT and NI, using adjusted figures on all three legs and the same consolidation scope. The document's FY2025 − Q1 2025 + Q1 2026 is an example; do not mix reported quarter earnings with adjusted annual earnings. If an adjusted interim bridge is unavailable, use a labelled annual base or transparent estimate and disclose the gap. Align trailing sales and other flow denominators where used. Annual 2025/2024 benchmarking and five-year trend tables should remain separately identifiable.

Begin with consolidated group NI as requested, including NCI. Also reconcile NI attributable to owners of the parent and NI attributable to NCI. A group-wide FCFE cannot be divided directly by parent shares: choose the consistent group valuation/NCI subtraction or parent-only cash-flow route in section 9.

Compute historical effective tax `T_eff = income-tax expense / profit before tax`, over five years. Explain negative/near-zero pretax income, exceptional tax benefits, deferred tax and jurisdictional effects. Benchmark against statutory rates. For FCFF start from a justified effective operating tax rate, labelling use of the P&L ratio as a proxy; forecast loss carryforwards or normalization when material. Do not generate an immediate tax refund on losses without support.

Keep `T_eff` for operating cash flows and `T_marg` for financing/beta separate. Use the home-country marginal corporate rate as the financing default. The Word permits a geographic weighted rate; use it only as an explicitly justified proxy for where interest deductions arise, not because a revenue average necessarily measures the tax shield. Explain limitations, tax-shield availability and any transition. Consistency requires the same T_marg for relevering and after-tax Kd, not forced equality with T_eff.

## 3. Net capital expenditure

**Word requirement.** Build a current/prior-year schedule of PP&E additions, intangible investment, acquisitions and any other proposed reinvestment, with five-year context. Decide each item's inclusion by recurrence and business model. Include recurring acquisitions when acquisition-led growth is forecast; exclude exceptional deals from the recurring base and separately account for already completed transactions. Match acquisition cash outlays, acquired cash, subsequent earnings and financing; do not include purchased growth without its cost.

`NCE = recurring CapEx (including qualifying acquisitions) − consistent consolidated D&A`.

Keep recurring replacement investment in CapEx; do not assume maintenance always equals depreciation. Exclude impairments/write-offs from the D&A add-back if removed from adjusted EBIT. Reconcile adjusted EBIT, CapEx and D&A to a common perimeter and definition. Avoid mixing total cash-flow-statement noncash adjustments with recurring D&A.

Do not capitalize R&D or add analytical lease capitalization/restatements in the course base case. Retain reported IFRS accounting and avoid capitalizing the same leases again. Record the existing lease treatment in EBIT, D&A, investment, debt and payments; see sector_adjustments.md. A material inconsistency is a disclosed limitation, not a reason to hide a second lease adjustment.

Compute `NCE / EBIT(1−T_eff)` for both annual comparison years and the matched European industry. Select one ratio within the observed company/industry range, weighting clean representative years more heavily; do not blindly average. Identify industry, sample/year and source column. Forecast NCE as this ratio × forecast after-tax EBIT. If denominators are nonpositive or distorted, ratios are not meaningful: use a supported sales, capacity or explicit capex schedule, mark the course exception and explain it. An FCFE model can use this operating reinvestment schedule but needs its own equity reinvestment/ROE calculation.

## 4. Working capital

**Word requirement.** Compute and reconcile:

`NWC = (current assets − cash and cash equivalents) − (current liabilities − current financial debt)`.

Specify which current financing items, including lease liabilities where classified as financial debt, are excluded. Identify material nonoperating current assets/liabilities and explain any scope adjustment. Keep historical definitions constant.

Compute annual NWC and NWC/Sales for t and t−1; inspect five years for seasonality and unusual balances. Compare with the matching Damodaran European noncash working-capital-to-sales measure and explain definition differences.

**Operational interpretation of the Word's ambiguous averaging instruction:** select the latest representative company NWC/Sales ratio (normally t, using t−1 if t is distorted) and set forecast ratio `r_NWC = (selected company ratio + industry ratio)/2`. Show both company years, selected year, industry value, average and min/max range. Do not silently use a three-way average. If either input is unavailable or noncomparable, document the fallback.

Forecast sales independently and then:

`NWC_y = r_NWC × Sales_y`

`raw ΔNWC_y = NWC_y − NWC_(y−1)`

`DCF ΔNWC_y = max(raw ΔNWC_y, 0)`.

Use the actual normalized opening NWC in year 1; a target-ratio transition can itself release/invest cash. Do not use NWC/Sales × sales growth without reconciling the opening balance.

The zero floor is a course-specific conservative overlay, not an accounting identity. Preserve the signed historical changes and the raw forecast balances; apply the floor only to the cash-flow deduction. Show the cumulative difference and the per-share impact versus unfloored cash flows. Use the same convention in year n+1. Negative working-capital business models need explicit discussion.

## 5. Cash flows, returns and growth

Use positive amounts for investment, borrowing and repayment; NWC changes are signed before the course floor.

`NOPAT = adjusted EBIT × (1−T_eff)`

`FCFF = NOPAT − NCE − DCF ΔNWC`

`Net borrowing = new borrowing − debt repayments`

`FCFE = adjusted NI − NCE − DCF ΔNWC + net borrowing`.

For a stable financing ratio delta, the simplified reinvestment-funding assumption is `net borrowing = delta × (NCE + DCF ΔNWC)` and `FCFE = NI − (1−delta) × (NCE + DCF ΔNWC)`. Reconcile to planned borrowing; an observed stable market ratio does not automatically prove this funding assumption. Model separately refinancing, distributions or leverage changes that invalidate it. Do not deduct interest again from NI or from FCFF.

`Firm reinvestment rate = (NCE + DCF ΔNWC) / NOPAT`

`Equity reinvestment rate = (NCE + DCF ΔNWC − net borrowing) / NI`

`ROE = adjusted NI / beginning book equity`

`ROC = NOPAT / beginning invested operating capital`

Use beginning BOOK capital for returns, MARKET values for discount-rate weights. For consolidated ROC, define invested capital as book financial debt + total book equity (including NCI) − cash/nonoperating capital excluded from NOPAT. If the equity input is parent-only, add NCI once. Reconcile an operating-assets-minus-operating-liabilities calculation as a check. The Word's two ROC denominators are alternatives requiring a scope bridge, not interchangeable formulas. For group ROE use group NI and total group book equity; for parent ROE use parent NI and parent equity. Align trailing returns to the beginning of the trailing period when possible and label any annual opening-capital proxy.

`Fundamental earnings growth = reinvestment rate × ROE (FCFE) or ROC (FCFF)`.

This identity assumes the return on incremental reinvestment is represented by the selected return; show changes in returns/margins separately. Negative earnings/equity or distorted capital invalidate naive rate multiplication: use explicit operating forecasts and explain the exception. Compare intrinsic growth with verified analyst earnings growth, a linear extrapolation of historical earnings (show period/method), and company narrative. Do not confuse EPS, NI, revenue and EBIT growth. Forecast sales explicitly where NWC is sales-driven. Prefer well-supported intrinsic growth; otherwise explain reliance on external estimates. Do not let a narrative alone override contrary numerical evidence.

## 6. Growth stages and terminal value

**Retained skill convention.** The Word asks for a justified first-stage duration (3 or 5 years) but does not define thresholds. Retain the original heuristic as the default and label it a project assumption:

1. If selected earnings growth exceeds stable growth by MORE THAN 10 percentage points, use three stages: five initial years, five transition years, then perpetuity.
2. Otherwise, if growth is above 7%, use two stages: five explicit years, then perpetuity.
3. Otherwise, consider one stable stage only if growth, returns, financing and reinvestment are already sustainable. Do not use a 7% perpetual rate merely because it passes the heuristic. If the firm is not mature, use a justified explicit transition even below 7%.

Evaluate the three-stage test first. If the Word/project context supports three initial years, document the departure and compare to five. State whether thresholds apply to the selected forecast growth or calculated intrinsic growth; default to selected forecast growth and disclose both if different.

Choose stable g from long-run nominal economic growth/inflation in the valuation currency; 3% is only a candidate, not a universal default. Retain `g <= Rf` as the course safeguard. Require `g < terminal Ke` for FCFE or `g < terminal WACC` for FCFF; never compute a nonpositive perpetuity denominator. For a course-safeguard exception, report the reason and a compliant alternative; no exception permits an invalid denominator.

Transition growth, operating margins, ROE/ROC, reinvestment, leverage and beta consistently. A perpetual growth rate needs sustainable investment: stable firm reinvestment rate = g/ROC and stable equity reinvestment rate = g/ROE, where meaningful. Reconcile these with the NCE/NWC schedules, debt funding and the NWC floor; recalibrate terminal assumptions transparently rather than keeping incompatible ratios. Require finite, economically plausible steady-state returns and cash flows.

`TV_n = FCF_(n+1) / (terminal discount rate − g)`.

Construct year n+1 explicitly from stable assumptions; do not multiply year n cash flow by (1+g) if margins, tax, reinvestment or leverage change. Terminal value is at time n and must be discounted to the valuation date. A one-stage model uses time-1 stable FCF. No exit multiple replaces the perpetuity; multiples are a reasonableness check.

## 7. Risk-free rate and cost of equity

Use one Rf in Ke and Kd, matching cash-flow currency and nominal/real basis. Use a ten-year government benchmark in that currency (e.g., Bund for EUR, Swiss Confederation for CHF, Gilt for GBP, Treasury for USD). Identify the actual issuer; a multinational's domicile does not select the currency benchmark. Check the issuer's rating/default spread as of the cutoff rather than fixing example ratings forever.

`Rf = government yield − issuer sovereign default spread`.

For a default-free benchmark the spread is zero. Use Damodaran's **Adj. Default Spread**, or a justified sovereign CDS measure, not the equity **Country Risk Premium**. Inspect yield history. Use spot as the observed starting point; normalize only with evidence, an explicit window/target and sensitivity, not a generic instruction to avoid spot yields. Match dates and document any mismatch.

**Word requirement.** Base beta is bottom-up:

- Map business segments to European industry unlevered betas corrected for cash; use global data when more representative of a multinational.
- Revenue-weight segment betas using disclosed segment shares; weights must cover 100%. Explain any unallocated business or proxy.
- `D/E = delta/(1−delta)` for the relevant market leverage.
- `beta_L = beta_U × [1+(1−T_marg)×D/E]` under the usual negligible-debt-beta assumption; disclose limitations for distressed/high-risk debt.
- Relever along the financing path if leverage changes. Do not unlever and relever a vendor regression beta without knowing its leverage basis.
- Compare with regression beta; report index, period, frequency, date and, if available, uncertainty. Missing vendor methodology is a data gap. Regression beta is a cross-check, not the default.

Compute weighted equity CRP from geographic revenues:

`weighted CRP = sum(revenue_i / total revenue × equity CRP_i)`.

Use the **Country Risk Premium** column, not **Adj. Default Spread** or total **Equity Risk Premium**. For aggregated geographies use the corresponding documented regional average in the downloadable file, or a transparent disclosed-country proxy with a sensitivity. Do not invent country splits. Weights must sum to one. Revenue is a course exposure proxy; it does not fully capture production, assets or political risk.

Use the mature-market ERP for the chosen dataset vintage. The Word's 4.23% is a January 2026 example. Do not permanently hardcode it or reuse an example US total ERP as a pure mature-market premium.

Calculate:

- Base, approach 1: `Ke = Rf + beta_L × ERP_mature + weighted CRP`.
- Cross-check, approach 2: `Ke = Rf + beta_L × (ERP_mature + weighted CRP)`.
- Optional approach 3: `Ke = Rf + beta_L × ERP_mature + lambda × CRP_reference`, with a consistent reference market and sourced lambda. A revenue proxy is company domestic revenue share / benchmark firms' domestic revenue share. Do not apply this again to an already exposure-weighted CRP without a coherent derivation.

In approach 1, `ERP_mature + weighted CRP` is a useful descriptive total premium but is NOT all multiplied by beta. Regional averaging reduces geographic mismatch; it does not eliminate all exposure-model limitations.

Retain the original market-rate comparison: collect multiple comparable external Ke estimates when available, identify their methodology and dates, and report a mean only after comparability checks. A vendor CAPM estimate is not an independently market-implied rate. Mark unavailable estimates unavailable; never substitute an analyst price target as Ke.

## 8. Cost of debt and WACC

Kd is today's marginal long-term borrowing cost, not the historical interest-expense/book-debt ratio. Prefer comparable ten-year corporate borrowing when available; otherwise disclose maturity/currency differences.

1. Obtain the current actual issuer rating and map it to the applicable Damodaran rating/spread table (large-firm table for appropriate large nonfinancial firms).
2. Compute synthetic coverage `adjusted EBIT / gross interest expense` on a comparable basis and map it to a rating/spread; use as fallback for unrated firms and cross-check otherwise. Do not use net interest income as gross interest expense. Explain losses, zero expense and lease-interest scope.
3. Compare with traded bond YTM (and issuer CDS if supplied). Inspect maturity, liquidity, currency and embedded options. Rating-based and market-implied spreads need not coincide.

`Kd_base = Rf + company default spread`.

If using an observed bond YTM as Kd, do not add Rf to it again. Assess incremental sovereign exposure only where concentration/risk and the chosen corporate-spread construction justify it:

`weighted sovereign spread = sum(revenue_weight_i × sovereign default spread_i)`

`Kd = Rf + company spread + a × weighted sovereign spread`, where `0 <= a <= 1`.

State a, geographic evidence and why the risk is not already captured in the actual rating/yield. Large diversified firms may justify a=0; small concentrated firms may justify more. This is a documented project proxy, not automatic country-risk stacking. Use **Adj. Default Spread** for this debt component, correcting the Word's conflicting references to equity CRP.

`after-tax Kd = Kd × (1−T_marg)`.

Show separately government yield, sovereign spread, Rf, corporate spread, incremental country adjustment, pre-tax Kd, tax rate and after-tax Kd with dates and sources.

For ordinary debt and common equity:

`WACC = E/(D+E) × Ke + D/(D+E) × Kd × (1−T_marg)`.

Use market values, with a documented leverage path where appropriate. Do not use book weights simply because return ratios use book capital.

For preferred equity EP:

`WACC = E/(D+E+EP)×Ke + D/(D+E+EP)×Kd×(1−T_marg) + EP/(D+E+EP)×Kep`

`Kep = annual preferred dividend / market value of preferred equity` (same total/per-security basis).

Do not tax-shield preferred dividends by default. The Word's less-than-5% simplification is a materiality suggestion, not permission to create a tax deduction: show separate treatment or quantify a simplification's effect. Exclude preferred securities from common-share market cap and remove their claim once when bridging to common equity.

For hybrids, inspect contractual coupon, tax treatment, maturity, conversion/write-down triggers and fair value. Allocate economic debt/equity components on supported terms/valuation; do not automatically classify 50% as debt. The Word's CoCo split based only on probability of a share-price rise is not a sufficient pricing model. If a professor explicitly requires it, present that split as a separately labelled course sensitivity with its unsupported probability disclosed, alongside a defensible base treatment. Never invent P. Reconcile financing weights and common-equity claims; an equity-like hybrid is not necessarily existing common shareholders' equity.

## 9. Discounting and common-equity bridge

Use Ke for FCFE and WACC for FCFF. State end-year, midyear or dated discounting; end-year is the default. With varying rates, discount by the product of (1+rate_y) through the relevant period. For fractional/stub years, state timing explicitly and avoid double counting the already elapsed portion of a year.

FCFF discounted value is operating enterprise value, not common equity:

`Common equity = PV(FCFF) + nonoperating assets − market financial debt − nonoperating liabilities − other ownership claims`.

Include excess cash, financial investments and unconsolidated associates/JVs only if their earnings/cash flows are excluded from operations. Subtract NCI for consolidated operations, preferred claims, appropriate hybrid claims, pension deficits and debt-like provisions only to the extent not captured elsewhere. The Word abbreviates nonoperating liabilities as NOL; use NOLiabs in the model to distinguish them from tax net operating losses.

Choose either gross debt plus cash or net debt with its embedded cash; do not add cash again after subtracting net debt. Show bridge item, amount, sign, date, perimeter, source and reason it is not already in cash flows. Use market/fair value for financial claims when available, labelled proxies otherwise.

For FCFE, do not subtract financial debt a second time. If valued group FCFE includes NCI entitlement, remove the fair value of NCI's equity claim once before dividing by parent shares. Alternatively use a fully reconciled parent-attributable NI, reinvestment and borrowing schedule and explain the departure from the Word's group starting point. Do not mix the two routes or mechanically use NCI book value as market value without a stated proxy. Add only nonoperating assets excluded from FCFE, and remove preferred/hybrid claims only if not already provided for.

Confirm current shares outstanding, excluding treasury shares, in the annual report and exchange data, updating for post-report issues, buybacks and splits through the cutoff. Annual weighted-average EPS shares are not the default current denominator. Explicitly handle options, RSUs and convertibles using one consistent dilution/claim method; do not both subtract an option claim and count the same dilution, or remove convertible debt twice. Document strike proceeds/settlement where relevant.

`Value per common share = common equity value / consistent share count`

`Upside/downside = value per share / market price − 1`.

Compute market cap independently from matching price and actual common shares; do not confuse it with DCF intrinsic equity. Align GBP versus GBp, ADR ratios, FX date and financial units.

## 10. Sensitivities and deliverables

Produce low/base/high cases and a two-dimensional terminal g versus Ke/WACC table; label invalid cells where rate <= g. Stress growth duration, investment ratios, margins, returns, leverage, geographic CRP and material bridge claims. Quantify the NWC floor and any material simplifying assumptions. Rank 3–5 drivers by per-share effect over disclosed plausible ranges, not arbitrary equal-size shocks alone.

Report `PV(terminal value) / total discounted operating cash flows` for FCFF and the analogous pre-bridge FCFE ratio; also show common-equity impact if useful. Flag above 75%. A negative or near-zero denominator makes the percentage misleading: state that and show amounts. Compare DCF-implied multiples with same-period peers/history; negative EBITDA makes EV/EBITDA not meaningful.

Follow SKILL-DCF.md for required files and qa_checklist.md for evidence. Preserve anomaly commentary, decision rationale, verified citations, summary image, dated source log and workbook reproducibility. Do not imply that the procedure itself has performed a company valuation.

## 11. Conflict register and reference evidence

| Conflict in supplied material | Implemented treatment |
| --- | --- |
| Old skill excludes all acquisitions; Word includes recurring acquisitions | Include recurring acquisition investment when the growth model depends on it |
| Old maintenance-equals-depreciation shortcut | Forecast recurring CapEx and deduct consistent D&A explicitly |
| Old optional R&D/lease adjustments; Word prohibits them | No additional R&D capitalization or lease restatement in course base case |
| Book debt amount averaged with industry debt ratio | Compare ratios or convert a target ratio to a labelled debt estimate |
| Word alternates sovereign default spread and equity CRP | Separate dataset columns and uses in Rf, Ke and Kd |
| Word implies same tax everywhere but separately calls for effective cash taxes | T_eff for operations; T_marg for debt shield and beta, reconciled explicitly |
| Two ROC denominators | Reconcile scope, cash and NCI; use beginning book operating capital |
| Group NI versus parent shares | Group FCFE/NCI bridge or fully reconciled parent FCFE |
| Word leaves first-stage duration open | Retain original heuristics, disclose duration and maturity exceptions |
| Old fixed 50% hybrid deduction and Word CoCo probability shortcut | Contract-based treatment; unsupported course shortcut only as a labelled variant |
| Geographic weighting claimed to remove all exposure limitations | Treat revenue weighting as a transparent proxy with residual limitations |

External methodological checks accessed 2026-10-28 (these verify definitions, not company inputs):

- Damodaran, [Country Default Spreads and Risk Premiums](https://pages.stern.nyu.edu/adamodar/New_Home_Page/datafile/ctryprem.html): separate sovereign default and equity country-risk columns. Use the dataset vintage appropriate to the valuation cutoff.
- Damodaran, [Financial measures and ratios](https://pages.stern.nyu.edu/~adamodar/New_Home_Page/definitions.html): preferred dividend yield, preferred tax treatment, debt/equity conversion and corporate default-spread definition.
- Damodaran, [Measuring Company Exposure to Country Risk](https://pages.stern.nyu.edu/adamodar/New_Home_Page/valquestions/CountryRisk.htm): alternative country-risk exposure formulations and limitations of beta scaling.

Other additions (scope bridges, denominator guards, terminal consistency and decision logs) are implementation clarifications; they are not presented as verbatim professor requirements. No current company, yield, tax rate, ticker or share-count data were verified as part of this document revision.
