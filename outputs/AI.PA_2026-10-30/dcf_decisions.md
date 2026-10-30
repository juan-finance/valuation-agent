# DCF decisions — AI.PA @ 2026-10-30 (standard mode)

## Model choice: FCFF (two-stage, 5y explicit + growing perpetuity)

**FCFE vs FCFF — course rule (stable debt ratio → FCFE; unstable → FCFF).**
Judged UNSTABLE → **FCFF**. Evidence: gross borrowings were stable (€12.2/10.8/11.1/12.4bn FY22–25, market δ ~10.6%),
but the announced acquisition of DIG Airgas (South Korea; Moody's credit opinion 27-Aug-2025) raised interim debt to
€17.3bn at Jun-2026 — a ~40% step-up. A transition to the company's A-rating policy leverage is expected
(Moody's expects deleveraging within 12–18 months), but the ratio is not constant through the window, so FCFF is the
defensible route. Alternative FCFE cross-check: not run (standard mode; recorded as optional item skipped).

## Key assumptions

| Input | Value | Basis |
|---|---|---|
| Currency/units | EUR millions | reporting currency |
| Adjusted EBIT | OIR €5,581.6m (FY2025) | company recurring metric; IFRS op. income 5,278.7 reconciled |
| T_eff | 25.24% | FY2025 tax 1,230.5 / PBT 4,874.9; 5y range 23.4–25.7% |
| T_marg | 25.0% | France statutory CIT (incl. surcharges ~25.8% noted, 25% used) |
| Sales growth | 4%/yr explicit | organic + price; S&P expects ~5% in 2025; conservative vs history |
| OIR margin | 20.72% flat | FY2025 actual; margin trend +ve but not extrapolated |
| NCE/NOPAT | 38% | company FY25 38.8%, FY24 34.9%; industry weighted ~38.5% (capex_europe_2026-01) |
| NWC/Sales forecast | 7.74% | course avg: company −0.585% (FY25) + industry 16.07% /2 |
| Selected NI/EBIT growth | ~5% | fundamental 4.9% (reinv 37.5% × ROE 13.1%) vs historical ~8% vs analyst ~6% |
| Stage choice | two-stage | three-stage test first: 5% − 3% < 10pp; 5% < 7% → one-stage candidate, but mature-firm condition fails (5%>3%) → justified explicit transition |
| Stable g | 3.0% | ≤ Rf 3.38% safeguard; EUR long-run nominal growth proxy |
| Stable ROC | 10.7% | FY25 NOPAT/beginning invested capital = company ROCE 10.7% → stable reinvestment 28.0% |

## Discount rates

- **Rf = 3.38%** (Bund 10y, BBSIS obs 2026-10-30; Germany Aaa → sovereign spread 0).
- **Bottom-up beta**: segment-weighted cash-corrected unlevered (beta_europe_2026-01): LI→Chem Basic 0.50 (26.4%), IM→Chem Specialty 1.01 (45.0%), Healthcare→Healthcare Products 1.13 (16.3%), Electronics→Electronics General 1.04 (9.2%), E&T/other→Engineering/Construction 0.80 (3.2%) → βU 0.891. Relevered at market D/E 11.85% → **βL 0.970**. Regression beta (stockanalysis 5Y) 0.61 — materially lower; disclosed as cross-check only (vendor methodology unavailable = data gap).
- **Weighted CRP 0.79%**: Americas 39.7%×US 0.00% + EMEA 40.7%×1.36% (0.75×Western-Europe-avg 0.92% + 0.25×ME&A proxy avg 2.99%: Saudi/UAE/Egypt/S.Africa/Qatar) + AsiaPac 19.6%×1.03% (9-country avg: CN/JP/KR/TW/AU/SG/IN/MY/TH). Proxies — country splits not disclosed in PR; sensitivity shown.
- **Ke = 8.24%** (base, additive CRP); beta-scaled cross-check 8.22%. Lambda approach: not run (standard mode).
- **Kd = 4.16%** pre-tax: Rf + A2/A spread 0.78% (actual ratings S&P A / Moody's A2 / Scope A, all stable). Synthetic coverage cross-check: EBIT 5,278.7/interest ~454 ≈ 11.6 → Aaa/AAA 0.40% — company spread chosen over synthetic (rating precedence per procedure). a=0 for incremental sovereign (diversified large cap; French exposure already in rating).
- **WACC = 7.70%**: E 89.4% / D 10.6% market weights; Kd after-tax 3.12%. No preferred/hybrids.

## Conventions and judgment calls

- **Market debt**: book proxy €13,636.9m (borrowings + lease liabilities); IG bonds near par; labelled proxy, ±1pp WACC sensitivity covers.
- **NWC**: FY25 NWC −157.7 (−0.58% of sales) — company runs near-zero/slightly negative operating WC; course-mandated forecast ratio 7.74% forces a €2,327m year-1 WC build. Course floor max(Δ,0) applied; raw changes all positive → floor non-binding this run (PV cost €0).
- **Bridge**: operating EV − debt+leases + cash 3,962 + associates 175 (book proxy; earnings below EBIT so excluded from ops) − NCI 733 (book proxy) − pensions/provisions 2,422 (debt-like claim; conservative — settlement partially already in cash flows; flagged limitation).
- **Leases**: IFRS16 kept as reported (no restatement); lease liabilities inside financial debt; D&A/interest consistent.
- **Shares**: 636.47m post Jun-2026 1:10 free-share attribution; treasury excluded; no material options/RSU dilution identified — disclosed.
- **Conflicts found**: none requiring lecture override; Word-document ambiguities handled per section-11 register.

## Result

EV €64.5bn → equity €51.8bn → **€81.4/share** vs price ~€181 (−55%). PV(TV) share 85.7% (flagged >75%).
Scenarios: LOW €58.1 / BASE €81.4 / HIGH €113.4. Driver ranking: WACC ±0.5pp (±€23), OIR margin ±1pp (±€10),
sales growth ±1pp (±€9), terminal g (±€7), NCE/NOPAT ±5pp (±€3).
Implied market view: at €181 the market prices either much lower WACC (~5.5%) or sustained higher growth/margins —
DCF does not support the price on course-standard assumptions; flagged as a stage-4 discussion item, not tuned.

Data gaps: FY2021 AR column (aggregator-only), option/RSU dilution detail, fair-value debt split, true country revenue mix, vendor Ke estimates (unavailable), regression-beta methodology.
