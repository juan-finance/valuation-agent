"""DCF engine: the arithmetic of methodology/dcf_procedure.md (sections 2-9, 10).

Pure functions, decimals for all rates. Nothing here picks an assumption; callers pass
sourced inputs. Section references are to dcf_procedure.md.
"""
from __future__ import annotations

from dataclasses import dataclass, field
from math import isclose
from typing import Callable, Iterable, Sequence


# --------------------------------------------------------------------------- helpers
def _check_weights(weights: Sequence[float], tol: float = 1e-6) -> None:
    total = sum(weights)
    if not isclose(total, 1.0, abs_tol=tol):
        raise ValueError(f"weights must sum to 1 (got {total:.6f}); explain any unallocated share")


def weighted_average(weights: Sequence[float], values: Sequence[float], tol: float = 1e-6) -> float:
    """Revenue-weighted average (segment betas, geographic CRP, sovereign spread). Weights must cover 100%."""
    if len(weights) != len(values):
        raise ValueError("weights and values differ in length")
    _check_weights(weights, tol)
    return sum(w * v for w, v in zip(weights, values))


# --------------------------------------------------------------------------- section 7: beta, Ke
def de_from_debt_ratio(delta: float) -> float:
    """D/E = delta/(1-delta), delta = D/(D+E) at market values."""
    if not 0 <= delta < 1:
        raise ValueError("debt ratio must be in [0,1)")
    return delta / (1 - delta)


def debt_from_ratio(delta: float, equity: float) -> float:
    """Target-derived debt estimate D = delta/(1-delta) x E. Label it target-derived, not observed."""
    return de_from_debt_ratio(delta) * equity


def relever_beta(beta_u: float, de: float, t_marg: float) -> float:
    """beta_L = beta_U x [1 + (1 - T_marg) x D/E] (negligible debt beta)."""
    return beta_u * (1 + (1 - t_marg) * de)


def unlever_beta(beta_l: float, de: float, t_marg: float) -> float:
    return beta_l / (1 + (1 - t_marg) * de)


def risk_free(gov_yield: float, sovereign_default_spread: float = 0.0) -> float:
    """Rf = government yield - issuer sovereign default spread (Adj. Default Spread, NOT equity CRP)."""
    return gov_yield - sovereign_default_spread


def ke_additive(rf: float, beta_l: float, erp_mature: float, crp_weighted: float) -> float:
    """BASE approach 1: Ke = Rf + beta_L x ERP_mature + weighted CRP (CRP not multiplied by beta)."""
    return rf + beta_l * erp_mature + crp_weighted


def ke_beta_scaled(rf: float, beta_l: float, erp_mature: float, crp_weighted: float) -> float:
    """Cross-check approach 2: Ke = Rf + beta_L x (ERP_mature + weighted CRP)."""
    return rf + beta_l * (erp_mature + crp_weighted)


def ke_lambda(rf: float, beta_l: float, erp_mature: float, lam: float, crp_reference: float) -> float:
    """Optional approach 3: Ke = Rf + beta_L x ERP_mature + lambda x CRP_reference (needs sourced lambda)."""
    return rf + beta_l * erp_mature + lam * crp_reference


# --------------------------------------------------------------------------- section 8: Kd, WACC
def kd_pre_tax(rf: float, company_spread: float, a: float = 0.0, weighted_sovereign_spread: float = 0.0) -> float:
    """Kd = Rf + company spread + a x weighted sovereign spread, 0 <= a <= 1.
    If an observed bond YTM is used as Kd, do NOT call this (never add Rf to a yield again)."""
    if not 0 <= a <= 1:
        raise ValueError("a must be in [0,1]")
    return rf + company_spread + a * weighted_sovereign_spread


def kd_after_tax(kd: float, t_marg: float) -> float:
    return kd * (1 - t_marg)


def kep(preferred_dividend: float, preferred_market_value: float) -> float:
    """Cost of preferred = annual dividend / market value (same total or per-security basis). No tax shield."""
    return preferred_dividend / preferred_market_value


def wacc(E: float, D: float, ke: float, kd: float, t_marg: float, EP: float = 0.0, kep_: float = 0.0) -> float:
    """Market-value WACC, optionally with preferred equity EP (no tax shield on preferred)."""
    V = E + D + EP
    if V <= 0:
        raise ValueError("capital must be positive")
    return E / V * ke + D / V * kd * (1 - t_marg) + EP / V * kep_


# --------------------------------------------------------------------------- section 4: NWC
def nwc(current_assets: float, cash: float, current_liabilities: float, current_fin_debt: float) -> float:
    """NWC = (CA - cash) - (CL - current financial debt)."""
    return (current_assets - cash) - (current_liabilities - current_fin_debt)


def forecast_nwc_ratio(company_ratio: float, industry_ratio: float) -> float:
    """Operational reading of the Word instruction: r_NWC = (selected company ratio + industry ratio) / 2."""
    return (company_ratio + industry_ratio) / 2


@dataclass
class NWCRow:
    year: int
    sales: float
    nwc_balance: float
    raw_delta: float
    floored_delta: float  # max(raw, 0): course floor, applies to forecast cash flows only


def nwc_schedule(sales: Sequence[float], r_nwc: float, nwc_opening: float, first_year: int = 1) -> list[NWCRow]:
    """NWC_y = r_NWC x Sales_y; raw dNWC_y = NWC_y - NWC_(y-1); DCF dNWC = max(raw, 0).
    Year 1 uses the actual normalised opening balance (a transition to the target ratio is itself a cash flow)."""
    rows, prev = [], nwc_opening
    for i, s in enumerate(sales):
        bal = r_nwc * s
        raw = bal - prev
        rows.append(NWCRow(first_year + i, s, bal, raw, max(raw, 0.0)))
        prev = bal
    return rows


# --------------------------------------------------------------------------- section 3/5: cash flows
def nce(recurring_capex: float, da: float) -> float:
    """Net capital expenditure = recurring CapEx (incl. qualifying acquisitions) - consistent D&A."""
    return recurring_capex - da


def nopat(ebit_adjusted: float, t_eff: float) -> float:
    return ebit_adjusted * (1 - t_eff)


def fcff(ebit_adjusted: float, t_eff: float, nce_: float, dnwc_floored: float) -> float:
    """FCFF = NOPAT - NCE - floored dNWC. Interest is never deducted again."""
    return nopat(ebit_adjusted, t_eff) - nce_ - dnwc_floored


def fcfe(ni_adjusted: float, nce_: float, dnwc_floored: float, net_borrowing: float) -> float:
    """FCFE = NI - NCE - floored dNWC + net borrowing."""
    return ni_adjusted - nce_ - dnwc_floored + net_borrowing


def fcfe_stable_leverage(ni_adjusted: float, nce_: float, dnwc_floored: float, delta: float) -> float:
    """Stable debt ratio delta: net borrowing = delta x (NCE + dNWC) so FCFE = NI - (1-delta)(NCE + dNWC)."""
    return ni_adjusted - (1 - delta) * (nce_ + dnwc_floored)


def firm_reinvestment_rate(nce_: float, dnwc_floored: float, nopat_: float) -> float:
    return (nce_ + dnwc_floored) / nopat_


def equity_reinvestment_rate(nce_: float, dnwc_floored: float, net_borrowing: float, ni: float) -> float:
    return (nce_ + dnwc_floored - net_borrowing) / ni


def fundamental_growth(reinvestment_rate: float, return_on_capital: float) -> float:
    """g = reinvestment rate x ROE (FCFE) or ROC (FCFF). Invalid when earnings/capital are negative:
    use an explicit operating forecast and explain the exception instead."""
    return reinvestment_rate * return_on_capital


def stable_reinvestment_rate(g: float, return_on_capital: float) -> float:
    """Stable firm reinvestment = g/ROC (firm) or g/ROE (equity)."""
    return g / return_on_capital


def roe(ni: float, beginning_book_equity: float) -> float:
    return ni / beginning_book_equity


def roc(nopat_: float, beginning_invested_capital: float) -> float:
    return nopat_ / beginning_invested_capital


# --------------------------------------------------------------------------- section 6: stages, TV
def growth_stage_heuristic(selected_growth: float, stable_g: float) -> str:
    """Project heuristic from section 6 (a default, not theory); evaluate the 3-stage test FIRST.
    1) growth > stable g + 10pp -> 'three_stage' (5 initial + 5 transition years)
    2) else growth > 7%          -> 'two_stage'   (5 explicit years)
    3) else                      -> 'one_stage_candidate' (only if growth/returns/financing already sustainable)
    """
    if selected_growth - stable_g > 0.10:
        return "three_stage"
    if selected_growth > 0.07:
        return "two_stage"
    return "one_stage_candidate"


def check_stable_growth(g: float, rf: float, terminal_rate: float) -> list[str]:
    """Return warnings. g<=Rf is the course safeguard (an exception needs a reason and a compliant alternative);
    g < terminal rate is mandatory (raises)."""
    if g >= terminal_rate:
        raise ValueError(f"terminal rate {terminal_rate:.4%} must exceed stable growth {g:.4%}")
    return [] if g <= rf else [f"stable g {g:.4%} exceeds Rf {rf:.4%}: course safeguard exception needs a documented reason"]


def terminal_value(fcf_next: float, rate: float, g: float) -> float:
    """TV_n = FCF_(n+1) / (rate - g). Never computes a nonpositive denominator."""
    if rate <= g:
        raise ValueError(f"rate {rate:.4%} <= g {g:.4%}: invalid perpetuity")
    return fcf_next / (rate - g)


def discount_factors(rates: Sequence[float]) -> list[float]:
    """Cumulative factors 1/prod(1+rate_y); end-year timing. Handles varying rates (three-stage)."""
    out, acc = [], 1.0
    for r in rates:
        acc *= 1 + r
        out.append(1 / acc)
    return out


@dataclass
class DCFResult:
    pv_explicit: float
    tv: float
    pv_tv: float
    total: float            # PV(explicit) + PV(TV): operating value (FCFF) or pre-bridge equity (FCFE)
    tv_share: float | None  # PV(TV)/total, None if total <= 0 (percentage would mislead)
    tv_flag_over_75: bool
    factors: list[float] = field(default_factory=list)


def value_cash_flows(explicit_fcf: Sequence[float], rates: Sequence[float], fcf_terminal_next: float,
                     terminal_rate: float, g: float) -> DCFResult:
    """Discount explicit flows with per-year rates (end-year) and add a growing-perpetuity TV at time n.
    fcf_terminal_next is the EXPLICITLY CONSTRUCTED year n+1 flow (never FCF_n x (1+g) by default).
    `rates` are the per-year discount rates for years 1..n (three-stage: transition rates change)."""
    if len(explicit_fcf) != len(rates):
        raise ValueError("one discount rate per explicit year required")
    f = discount_factors(rates)
    pv_explicit = sum(c * d for c, d in zip(explicit_fcf, f))
    tv = terminal_value(fcf_terminal_next, terminal_rate, g)
    pv_tv = tv * f[-1]
    total = pv_explicit + pv_tv
    share = pv_tv / total if total > 0 else None
    return DCFResult(pv_explicit, tv, pv_tv, total, share, bool(share is not None and share > 0.75), f)


# --------------------------------------------------------------------------- section 9: bridge
def equity_bridge(operating_value: float, items: Iterable[tuple[str, float]]) -> tuple[float, list[tuple[str, float]]]:
    """Common equity = operating value + sum(signed items). Pass each claim ONCE with its sign:
    e.g. ('excess cash', +x), ('financial debt', -d), ('NCI', -n), ('preferred', -p), ('pension deficit', -q).
    Choose gross debt + cash OR net debt - never add cash after subtracting net debt.
    Returns (common equity, itemised list) for the bridge table."""
    items = list(items)
    names = [n.strip().lower() for n, _ in items]
    dups = {n for n in names if names.count(n) > 1}
    if dups:
        raise ValueError(f"bridge items listed twice (double counting?): {sorted(dups)}")
    return operating_value + sum(a for _, a in items), items


def value_per_share(common_equity: float, shares: float) -> float:
    if shares <= 0:
        raise ValueError("share count must be positive (current shares excl. treasury, consistent dilution)")
    return common_equity / shares


def upside(value_ps: float, price: float) -> float:
    return value_ps / price - 1


# --------------------------------------------------------------------------- section 10: sensitivities
def sensitivity_grid(value_fn: Callable[[float, float], float], rates: Sequence[float], gs: Sequence[float]):
    """Two-dimensional table (rows = rate, cols = g). Cells with rate <= g are None (label them invalid)."""
    return [[None if r <= g else value_fn(r, g) for g in gs] for r in rates]


def nwc_floor_impact(rows: Sequence[NWCRow], factors: Sequence[float], shares: float | None = None) -> dict:
    """Value effect of the course floor: PV of (floored - raw) deductions (a cost vs unfloored flows)."""
    if len(rows) != len(factors):
        raise ValueError("rows and factors differ in length")
    pv = sum((r.floored_delta - r.raw_delta) * f for r, f in zip(rows, factors))
    out = {"cumulative_difference": sum(r.floored_delta - r.raw_delta for r in rows), "pv_cost": pv}
    if shares:
        out["per_share"] = pv / shares
    return out


def rank_drivers(base_value: float, shocked: dict[str, tuple[float, float]], top: int = 5):
    """Rank value drivers by per-share swing. shocked = {driver: (value_low_case, value_high_case)}.
    Use plausible disclosed ranges, not equal-size shocks alone."""
    rows = [(k, lo, hi, abs(hi - lo)) for k, (lo, hi) in shocked.items()]
    rows.sort(key=lambda r: r[3], reverse=True)
    return [{"driver": k, "low": lo, "high": hi, "swing": sw, "swing_pct_of_base": sw / base_value if base_value else None}
            for k, lo, hi, sw in rows[:top]]
