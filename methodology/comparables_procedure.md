# Comparable-company valuation procedure

Select a defensible peer group separately for each target, then value the target using its primary multiple. This method is independent of [market regression valuation](regression_procedure.md). Thresholds, scoring weights, tier limits and scaling rules below are project rules, not universal finance laws.

## Contents

1. Configuration and definitions
2. Data route and validation
3. Selection funnel
4. Similarity score
5. Multiples and fundamental adjustments
6. Valuation and primary multiple
7. Output schemas and audit evidence
8. Stops and explicit interpretations

## 1. Configuration and definitions

Scope follows SKILL-RELATIVE.md: ONE target when called from the company-valuation orchestrator (output in outputs/<ticker>_<date>/relative/); all 20 targets for a direct whole-assignment run (outputs/relative_<date>/); a subset only if explicitly requested. Peer lists are always built per target. Record:

```yaml
comparables_per_target: 10
minimum_comparables_with_reason: 8
min_valid_values_per_multiple: 6
valuation_date: required_common_date
earnings_basis: FY2025
forward_basis: separate_NTM_if_available
comparison_currency: EUR
min_market_cap_eur: 1000000000
size_band: [0.1, 10]
relaxed_size_band: [0.05, 20]
min_tier_1_2: 6        # absolute floor, reached only when the Tier 3 cap is relaxed; with the default cap the effective minimum is comparables_per_target - max_tier_3 = 8
max_tier_3: 2
relaxed_max_tier_3: 4
min_europe_listed: 5
score_winsorization: [0.05, 0.95]
```

The source wording “trailing FY2025” conflates a fiscal-year observation with last-twelve-month earnings. Use FY2025 as the assigned base, label it FY, and store TTM/forward separately. If the user specifies a different basis, apply it consistently to targets and peers. Record actual fiscal start/end dates; calendarize non-December years only from sourced interim data, otherwise use the latest relevant full FY and flag the mismatch. Do not invent calendarized figures.

**Equity value:** sum price × current outstanding common shares across economic share classes, excluding treasury shares; deduplicate dual listings/ADRs. Reconcile EPS/NI to parent common equity and share-class entitlements. Use one disclosed denominator convention consistently; do not silently mix current shares and annual weighted-average EPS shares.

**Comparable EV:** common equity market value + total financial debt including leases + NCI − cash and equivalents − nonoperating equity-accounted associates. Remove associates only when their contribution is excluded from the operating denominator; document value/proxy. Align other material financing/nonoperating claims consistently across peers and target; do not apply a target-only preferred/hybrid adjustment to a peer EV multiple that was constructed differently without reconciliation. If reliable comparable adjustments cannot be made, label the limitation and use another primary multiple.

**EBIT/EBITDA:** as reported base; identify one-offs. If abs(one-off) > 10% of abs(reported EBIT), also record a normalized alternative and flag. Zero/near-zero EBIT requires explicit review rather than division by zero. Keep normalized sensitivities separate and consistent across peers. Do not automatically replace this relative base with the DCF's adjusted earnings.

**Other definitions:** parent common book equity for PBV; sales on the same consolidation perimeter for PS; total book assets for EV/assets (or invested capital if uniformly specified); authentic replacement-cost data for Tobin's Q, not book assets relabelled as replacement cost. Rates stored as decimals; PEG uses growth percentage points: PE/(100×g). Relative PE = company PE / home-market-index PE with matching earnings basis/date. Index PE must be sourced.

## 2. Data route and validation

Follow the stage 3 rules in [data sources](data_sources.md). Confirm availability of a coherent terminal export once; reuse that answer for both methods. Terminal is preferred; otherwise use stockanalysis raw fields for all companies, with the permitted separate identity, classification, FX and beta sources. Competitors named in the target's annual report, same-industry screener results and the agent's own research are starting candidates, not approved peers. No group workbook exists or will be supplied.

Terminal route growth: consensus EPS growth over the same 3–5-year horizon. If more than 30% of a target's initial eligible candidate pool lacks consensus, switch the entire pool AND target to fundamental growth and report it. Measure this missingness before excluding incomplete candidates. Below that threshold the documented individual fallback is allowed, but label mixed provenance and show an all-fundamental scoring sensitivity where material.

Web route growth: use fundamental growth for every target and candidate. Compute g = ROE×(1−payout). For comparability with the shared regression growth policy, use positive, valid ROE; cap payout at one only in the retention calculation; retain actual payout separately. If ROE is nonpositive or the inputs are invalid, growth is unavailable, not a guessed recovery rate. Log this conservative clarification and its effect on candidate coverage. Negative/zero growth cannot support PEG even if otherwise usable for selection.

Before selection/valuation:

- Check equity market value versus class-level price × shares within 2%; flag discrepancies and resolve unit/perimeter errors.
- Use a single valuation date and FX snapshot. A price more than five trading days stale fails freshness; a price within five days is not automatically date-aligned. Retrieve the common-date quote or agree a common historical date; never combine dates silently. Record last-trading-day holiday conventions.
- Compute EV and multiples from raw figures, require positive EV for EV valuation. Keep original raw data and differences versus vendor multiples.
- Cross-check all targets against the FY annual reports and an independent public source; >2% discrepancies require both sources, chosen definition and explanation. Do not replace individual web inputs selectively to force agreement.
- Compare peer median multiples with the best-matching Damodaran Europe industry benchmark (region-appropriate benchmark for material global peers). A >50% relative gap triggers investigation before using the result. Verify the benchmark statistic really is a median, its period and its industry scope; do not compare aggregate ratios as if they were medians. A real economic gap can be retained only after documented resolution, not “fixed” to match.
- Verify every peer ISIN on an exchange, MSCI or issuer IR page. Directory sites can locate candidates but do not replace final verification.
- Prepare source-linked Spot_check rows for every target's selected peers. Record required human review separately from automated checks; do not claim it happened without evidence.

## 3. Selection funnel

1. Profile each target: main activity (at least 50% of revenue or EBITDA), business mix, sub-industry, regulation/contracts/cycle, capital intensity and eight scoring metrics. If no segment reaches 50%, record conglomerate/multi-sector status and justify the economic peer profile; do not invent a dominant business.
2. Start with 20–30 candidates, expanding where needed. Tier 1 = same main business; Tier 2 = adjacent business with similar cash-flow economics; Tier 3 = other nonfinancial firms, only when Tiers 1–2 cannot supply 10 qualified peers. Use MSCI Europe first, verified membership at the cutoff. Permit developed-market MSCI World expansion only under the ordered relaxation below. Include eligible other targets, but never the target itself.
3. Apply hard exclusions: emerging-market classification; bank, insurer or holding company; cap below EUR1bn; cap outside allowed target-relative band; target/parent/subsidiary or ownership above 20% in either direction; merger/spin-off/restructuring in the comparison period (default FY2024–25) that makes figures noncomparable; less than two years trading history; more than two missing scoring dimensions after allowed fallbacks. Do not interpret “holding company” to exclude every operating group with a legal holding parent; distinguish passive investment holdings from consolidated operating businesses and document borderline cases. REITs/other financial businesses are unsuitable for this nonfinancial peer method and must not enter as Tier 3.
4. Score eligible candidates under section 4. Preserve rejected candidates and rule-specific reasons.
5. Choose the lowest-score feasible set of 10, satisfying at least 6 Tier 1–2 (absolute floor), at most 2 Tier 3, and at least 5 Europe-listed. With only these three tiers, the default cap of 2 actually implies at least 8 Tier 1–2 for a set of 10; the floor of 6 only becomes binding once the Tier 3 cap is relaxed to 4. Replace the worst-ranked violating member with the best-ranked eligible replacement; never sacrifice a harder constraint to fix another. A constrained minimum-total-score selection is an equivalent implementation if all constraints are explicit.
6. If 10 cannot be obtained, relax in this order, rechecking feasibility each time: (a) add developed-market MSCI World constituents outside Europe; (b) widen size band to 0.05–20×; (c) increase Tier 3 limit to 4. Keep EUR1bn minimum, at least 6 Tier 1–2, at least 5 Europe-listed and all other hard filters. Recompute pool percentiles/scores after expansion; log membership changes. Do not relax earnings/definition validity or source quality to fill a quota.
7. Read each selected business description. Replace clearly unrelated economic profiles despite numerical similarity; record evidence and next-ranked replacement. Review listing/ownership and index eligibility rather than trusting example names.
8. If 10 remain infeasible but 8–9 satisfy ALL remaining constraints, deliver the documented shortfall. For m peers the Tier 3 cap is also limited by m−6. Below 8, stop that target's comparable valuation; do not pad the list or reuse a company twice. Other targets may continue.

Selection examples and primary multiples are in [sector adjustments](sector_adjustments.md); examples are search seeds requiring current verification.

## 4. Similarity score

| Dimension | Metric | Weight | Allowed fallback |
| --- | --- | ---: | --- |
| Growth | Consensus EPS growth, consistent 3–5-year horizon | 30% | Fundamental ROE×retention under section 2 |
| Market risk | Five-year levered regression beta | 15% | Sourced cash-corrected unlevered industry beta relevered at company market D/E and marginal tax |
| Financial risk | Net debt/EBITDA | 10% | Net debt/equity with disclosed book-equity definition |
| Profitability | ROE | 10% | Parent NI / average parent common equity of last two year-ends |
| Profitability | EBITDA margin | 10% | EBIT margin |
| Reinvestment | Payout | 7.5% | DPS/EPS on matching basis |
| Reinvestment | CapEx/Sales | 7.5% | (CapEx−D&A)/Sales |
| Size | ln(market cap in EUR) | 10% | None; required |

A fallback must not silently compare a different variable with the primary variable. For leverage, margin, CapEx and any changed ROE denominator, use a common fallback definition for the scoring dimension across target/pool where feasible; otherwise treat incomparable cells as missing and renormalize weights. Preserve both raw fields and method labels. Fundamental-versus-consensus growth follows its explicit exception above. A two-to-five-year trading-history company may use the permitted bottom-up beta when the five-year regression beta is unavailable; the two-year minimum itself is never relaxed.

For each target's final eligible candidate pool, excluding the target:

1. Winsorize each continuous scoring metric at PERCENTILE.INC 5% and 95%; retain raw values. These are score inputs, not valuation multiples.
2. Compute pool mean and STDEV.S on the winsorized metric. z = (value−mean)/SD. Standardize target with the same parameters; keep its raw z to reveal atypicality. The source specifies clipping the pool, not the target; do not silently clip target extremes to make it look typical.
3. Distance = sqrt(sum(w_j×(z_candidate,j−z_target,j)^2)). Lower means more similar. Use the weights above; industry remains in tier constraints, not an extra score term.
4. For one/two unavailable dimensions, drop the unavailable pairwise dimensions and rescale remaining weights to one; flag effective weight coverage. More than two missing candidate dimensions fails selection. If the target lacks more than two dimensions or required market cap, stop its scoring rather than impute. A zero-SD dimension contributes no discrimination: remove for the whole pool and renormalize, logging it separately from source missingness.
5. Resolve exact score ties deterministically by tier, European listing then verified ISIN; disclose the tie rule. Record all weights, caps, means, SDs and selected/ranked membership. Rerun selection if the user changes weights.

## 5. Multiples and fundamental adjustments

Compute PE, PEG, relative PE, EV/EBIT, EV/EBITDA, EV/CF, PBV, EV/assets, Tobin's Q where real replacement-cost data exist, PS and EV/Sales. Supplementary EV/RAB, EV/MW, EV/DACF, P/CF or dividend yield may be useful, but require explicit consistent definitions and do not replace the required set silently.

Mark an observation unavailable or NM if source evidence is missing or its denominator is zero/negative. Negative target earnings do not require deleting the company from every peer list: it may still supply usable other multiples and sufficient scoring metrics. Keep high positive peer multiples; do NOT import the regression PE>100 exclusion, 1%/99% winsorization or the old skill's generic trimming into peer aggregation.

For every target/multiple report n_valid, median, mean, PERCENTILE.INC 25% and 75%. At least 6 valid values are needed for use (with a 10-peer set this tolerates at most four missing). With 6–10 observations p25/p75 rest on very few points: say so next to the range. Flag abs(mean/median−1)>25%. These are peer dispersion ranges, not statistical confidence intervals.

Fundamental-adjusted multiples:

| Multiple | Adjusted target multiple |
| --- | --- |
| PE | Median(peer PE/(100×peer g)) × (100×target g) |
| PBV | Median(peer PBV/peer ROE) × target ROE |
| PS | Median(peer PS/peer net margin) × target net margin |
| EV/Sales | Median(peer EV/Sales / peer EBITDA margin) × target EBITDA margin |
| EV/EBITDA, EV/EBIT, EV/CF | Unscaled peer median; compare target growth to peer median growth |

Use the same growth/earnings definition in the scaled series; a TTM PEG cannot adjust FY PE. Each scaled ratio needs a positive meaningful driver for peer and target and at least 6 valid scaled peer observations; otherwise show adjustment unavailable and retain only a valid unadjusted cross-check. Compute low/high adjusted values from p25/p75 of the PE/driver, PBV/driver etc. ratios, multiplied by the target driver. Do not multiply quartiles from different populations or relabel raw quartiles as adjusted ones.

These are prescribed proportional adjustment heuristics, not comprehensive causal corrections. For example PS/net margin effectively behaves like PE when the accounting bases match; EV/Sales divided by EBITDA margin behaves like EV/EBITDA. Show both raw and adjusted values, model limitations and overlap; do not count them as independent evidence. For positive drivers use the adjusted version as the primary-method point estimate when applicable; if invalid, disclose the unadjusted fallback. Do not choose adjusted versus raw according to proximity to DCF.

EV/CF needs a defined cash-flow claim. The supplied rule allows reported operating cash flow or FCFF if available for all peers. Keep the requested reported-CFO comparison separately labelled if used; CFO may include financing interest and differs under IFRS/US GAAP. Use a consistently unlevered operating cash-flow measure or FCFF for an economically matched enterprise valuation when supported for every peer. If unavailable, EV/reported-CFO is a qualified cross-check, not an unqualified primary estimate. Never mix CFO, DACF and FCFF in one statistic or create invented add-backs.

Optional one-driver peer regression: fit the primary multiple on its main driver across the valid selected peers (one X only); show n and diagnostics. It is a peer-set sensitivity, not regression A/B/C and is not subject to the broad-market 30/100/150/500 minimums. Do not use a one-driver fit with insufficient variation/observations or claim equivalence to the full regression method.

## 6. Valuation and primary multiple

For equity multiples: implied common equity = selected multiple × matching target NI/book equity/sales; value per share = that value / consistent shares. Equivalent per-share multiplication is valid when units/perimeters match. Relative PE and PEG are transformed back to a PE before valuing earnings; they are not directly multiplied by EPS as ordinary PE ratios.

For enterprise multiples, invert EXACTLY the numerator construction:

`Implied common equity = selected EV multiple × matching target operating metric − debt including leases − NCI + cash + excluded associates`.

Include any additional claims/assets only through a consistently defined expanded EV and its inverse. Do not subtract net debt and also add the same cash. Do not add associates whose earnings remain in the denominator, and do not remove NCI twice. Use the [sector bridge checks](sector_adjustments.md); explain differences from the DCF bridge. Negative implied common equity is a distress/invalid-method flag, not a negative tradable share-price recommendation.

Convert the final per-share value from comparison EUR into the target's actual quote currency, checking pence/GBP and ADR ratios. All raw values/FX dates remain traceable. Upside = fair value/current comparable price−1; show currency gap too.

Choose one primary multiple using the business mapping in sector_adjustments.md. If its target denominator is nonpositive/near-zero, or fewer than 6 usable peers exist, try the listed cross-checks in order. Define and justify near-zero materiality before viewing valuations. If no suitable multiple passes, mark not valued. Retain other results as cross-checks. Never weight toward DCF, toward higher values for larger firms, or combine mechanically correlated multiples.

## 7. Output schemas and audit evidence

Deliver these three core files. Append fields if needed; do not drop required columns.

**comparables.csv** — one row per target/selected peer (200 only when 20 targets each have 10 peers):

```text
target_ticker,rank,comp_name,comp_ticker,comp_isin,country,tier,distance_score,growth,beta,net_debt_ebitda,roe,ebitda_margin,payout,capex_sales,market_cap_eur,pe,peg,relative_pe,ev_ebit,ev_ebitda,ev_cf,pbv,ev_assets,tobins_q,ps,ev_sales,flags,inclusion_reason,source_urls
```

Append valuation_date, earnings_basis, financial_period_end, source_route, growth_basis, metric_fallbacks, effective_weight_coverage and membership evidence. Keep canonical metric fields faithful: never put EBIT margin in ebitda_margin; append the fallback field/method instead.

**multiples_summary.csv** — one row per target/multiple:

```text
target_ticker,multiple,n_valid,median,mean,p25,p75,adjusted_multiple,value_per_share_low,value_per_share_mid,value_per_share_high,currency,is_primary
```

Append n_valid_adjusted, adjusted_p25, adjusted_p75, unadjusted_value_low/mid/high, adjusted_value_low/mid/high, selected_basis, valuation_status, flags. Main low/mid/high fields use the disclosed selected basis. Maintain unavailable required rows with reasons rather than silently omit them; one valid primary per valued target.

**comparables_report.md** — per target: profile/industry, route/date/basis, selected peers and rationale, primary multiple, value range/point, target fundamentals versus peer medians, raw versus adjusted results, sensitivity to peer composition/quartile/multiple, every exclusion/relaxation/replacement and limitation, market conditions, and exact Sources.

For the joint run (route own_estimation) place Candidate_Pool, Peer_Scores, Peer_Selection, Peer_Multiples, Peer_Spot_check and peer QA sheets in DATA_BASE_MSCI.xlsx as a separate audit section. Under route published_damodaran no DATA_BASE_MSCI.xlsx exists, so these sheets go in the labelled comparables_audit.xlsx (same exception as a standalone comparables run; it is not an additional core file). They must not be pooled into regression Data. Include rejected candidates, formulas, immutable raw inputs, all scores and constraints, and a manual EV recomputation for three reproducibly random selected peers. This reconciles the source's three-file output with its Spot_check-sheet requirement. For standalone comparables use the disclosed audit workbook exception in the skill.

Every figure links field→exact URL and access date, or terminal/ticker/field/export date; each judgment links evidence. Use the shared source log. Include a one-line economic inclusion reason for every peer. For source conflicts >2%, link both and state the resolution.

## 8. Stops and explicit interpretations

Stop the affected target if fewer than 8 compliant peers remain, required data/units cannot be established, no common price date is possible, or fewer than 6 valid observations support every suitable multiple. Do not invent figures. Keep blocked target/status rows and continue other targets. A >30% consensus gap triggers the whole-pool fallback and notification, not abandonment if the fallback is feasible.

Resolve validation gaps before final use. Human Spot_check review is a distinct evidence gate: generate the reviewable schedules first, then request that review if not already provided. Pending review must be visible; it is not automated approval. Final QA applies relaxed Tier 3 limits only where the permitted relaxation was actually invoked; it does not incorrectly reimpose the default cap of two.
