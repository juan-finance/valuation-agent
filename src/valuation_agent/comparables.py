"""Comparable-company mechanics for methodology/comparables_procedure.md (sections 3-6).

Scoring, constrained peer selection, multiple statistics, fundamental adjustments and the EV bridge inverse.
Tier assignment, hard filters, business-description review and the primary-multiple choice remain agent
judgement (recorded in comparables_report.md); this module only does the arithmetic once those are decided.
"""
from __future__ import annotations

import itertools
import math
from typing import Mapping, Sequence

import numpy as np
import pandas as pd

from .regression import percentile_inc, winsorize

# section 4 weights (project rules); change only if the user changes weights, then rerun selection
WEIGHTS: dict[str, float] = {
    "growth": 0.30, "beta": 0.15, "net_debt_ebitda": 0.10, "roe": 0.10,
    "ebitda_margin": 0.10, "payout": 0.075, "capex_sales": 0.075, "ln_mcap": 0.10,
}
SELECTION_CONFIG = dict(n=10, min_n=8, min_tier_1_2=6, max_tier_3=2, relaxed_max_tier_3=4, min_europe=5,
                        score_winsor=(0.05, 0.95), max_missing_dims=2)


# ------------------------------------------------------------------ section 4: similarity score
def similarity_scores(pool: pd.DataFrame, target: Mapping[str, float], weights: Mapping[str, float] = WEIGHTS,
                      winsor: tuple[float, float] = SELECTION_CONFIG["score_winsor"],
                      max_missing: int = SELECTION_CONFIG["max_missing_dims"]) -> tuple[pd.DataFrame, dict]:
    """Distance of each candidate to the target. `pool` = FINAL eligible candidates (target excluded), one column per
    weight key. Steps: winsorise pool at 5/95 (PERCENTILE.INC) -> mean and STDEV.S of the winsorised pool -> z for
    candidates; the TARGET is standardised with the same parameters but NOT clipped (raw z kept) -> weighted Euclidean
    distance over dimensions available for both, weights rescaled to 1 (effective weight coverage reported).
    A zero-SD dimension is removed for the whole pool and weights renormalised (logged separately from missingness).
    A candidate with > max_missing missing dimensions fails; a target missing > max_missing dims raises."""
    dims = list(weights)
    tgt_missing = [d for d in dims if d not in target or target[d] is None or not np.isfinite(float(target[d]))]
    if len(tgt_missing) > max_missing:
        raise ValueError(f"target lacks {len(tgt_missing)} scoring dimensions ({tgt_missing}): stop scoring, do not impute")
    P = pool[dims].apply(pd.to_numeric, errors="coerce")
    log = {"target_missing_dims": tgt_missing, "zero_sd_dims": [], "params": {}}
    z_pool, z_tgt = pd.DataFrame(index=P.index, columns=dims, dtype=float), {}
    for d in dims:
        col = P[d].dropna()
        if len(col) < 2:
            log["zero_sd_dims"].append(d)
            continue
        w, lo, hi = winsorize(col.to_numpy(), *winsor)
        ws = pd.Series(w, index=col.index)
        mean, sd = float(ws.mean()), float(ws.std(ddof=1))
        if not sd > 0:
            log["zero_sd_dims"].append(d)
            continue
        z_pool.loc[ws.index, d] = (ws - mean) / sd
        if d not in tgt_missing:
            z_tgt[d] = (float(target[d]) - mean) / sd           # raw z, no clipping of the target
        log["params"][d] = {"mean": mean, "sd": sd, "p_lo": lo, "p_hi": hi}
    usable = [d for d in dims if d in z_tgt]
    rows = []
    for idx in P.index:
        both = [d for d in usable if pd.notna(z_pool.at[idx, d])]
        missing_cand = [d for d in dims if pd.isna(P.at[idx, d])]
        if len(missing_cand) > max_missing:
            rows.append((idx, np.nan, 0.0, f"fails: {len(missing_cand)} missing dims"))
            continue
        w_sum_all = sum(weights[d] for d in usable)
        w_sum = sum(weights[d] for d in both)
        if w_sum == 0:
            rows.append((idx, np.nan, 0.0, "no common dimensions"))
            continue
        dist = math.sqrt(sum((weights[d] / w_sum) * (z_pool.at[idx, d] - z_tgt[d]) ** 2 for d in both))
        rows.append((idx, dist, w_sum / w_sum_all, "ok" if len(both) == len(usable) else f"rescaled, dropped {sorted(set(usable) - set(both))}"))
    out = pd.DataFrame(rows, columns=["idx", "distance", "weight_coverage", "note"]).set_index("idx")
    return out, log


# ------------------------------------------------------------------ section 3 step 5: constrained selection
def select_peers(scored: pd.DataFrame, n: int = SELECTION_CONFIG["n"], min_tier_1_2: int = SELECTION_CONFIG["min_tier_1_2"],
                 max_tier_3: int = SELECTION_CONFIG["max_tier_3"], min_europe: int = SELECTION_CONFIG["min_europe"]):
    """Minimum-total-score set of n peers satisfying: >= min_tier_1_2 tier-1/2, <= max_tier_3 tier-3 (and <= n-min_tier_1_2),
    >= min_europe Europe-listed. Exact: peers are split into 4 groups (tier12/tier3 x europe/non-europe), the cheapest k per
    group are taken, and all feasible count combinations are compared. This is the 'constrained minimum-total-score
    selection' the procedure accepts as equivalent to its replace-the-worst loop.
    `scored` needs columns: distance, tier (1/2/3), europe (bool), isin. Ties break by tier, European listing, ISIN.
    Returns (selected DataFrame sorted by rank, info dict) or (None, info) when infeasible."""
    df = scored.dropna(subset=["distance"]).copy()
    df["_t3"] = df["tier"].astype(int) >= 3
    df["_eu"] = df["europe"].astype(bool)
    df = df.sort_values(["distance", "tier", "_eu", "isin"], ascending=[True, True, False, True])
    cap3 = min(max_tier_3, n - min_tier_1_2)
    groups = {key: g for key, g in df.groupby(["_t3", "_eu"])}
    avail = {(t3, eu): len(groups.get((t3, eu), [])) for t3 in (False, True) for eu in (False, True)}
    cum = {k: np.concatenate([[0.0], np.cumsum(groups[k]["distance"].to_numpy())]) if k in groups else np.array([0.0]) for k in avail}
    best = None
    for a in range(avail[(False, True)] + 1):          # tier12 Europe
        for b in range(avail[(False, False)] + 1):     # tier12 non-Europe
            if a + b > n:
                break
            for c in range(avail[(True, True)] + 1):   # tier3 Europe
                d = n - a - b - c                       # tier3 non-Europe
                if d < 0 or d > avail[(True, False)]:
                    continue
                if a + b < min_tier_1_2 or c + d > cap3 or a + c < min_europe:
                    continue
                total = cum[(False, True)][a] + cum[(False, False)][b] + cum[(True, True)][c] + cum[(True, False)][d]
                if best is None or total < best[0] - 1e-12:
                    best = (total, a, b, c, d)
    info = {"n_requested": n, "available": {f"{'T3' if k[0] else 'T12'}_{'EU' if k[1] else 'nonEU'}": v for k, v in avail.items()},
            "constraints": {"min_tier_1_2": min_tier_1_2, "max_tier_3": cap3, "min_europe": min_europe}}
    if best is None:
        return None, {**info, "feasible": False}
    _, a, b, c, d = best
    take = [groups[(False, True)].head(a) if a else None, groups[(False, False)].head(b) if b else None,
            groups[(True, True)].head(c) if c else None, groups[(True, False)].head(d) if d else None]
    sel = pd.concat([t for t in take if t is not None]).sort_values(["distance", "tier", "_eu", "isin"], ascending=[True, True, False, True])
    sel = sel.drop(columns=["_t3", "_eu"])
    sel["rank"] = range(1, len(sel) + 1)
    return sel, {**info, "feasible": True, "total_score": best[0], "counts": {"T12_EU": a, "T12_nonEU": b, "T3_EU": c, "T3_nonEU": d}}


def select_with_relaxation(scored_by_step: Sequence[tuple[str, pd.DataFrame, dict]], min_n: int = SELECTION_CONFIG["min_n"]):
    """Apply the documented relaxation ORDER outside this function (a: add World developed-market rows,
    b: size band 0.05-20x, c: tier-3 limit 8), passing each step's rescored frame and select_peers kwargs.
    Tries n=20 first, then 19..min_n only if ALL other constraints hold. Returns (selection, info, step_label)."""
    for label, frame, kw in scored_by_step:
        for n in range(SELECTION_CONFIG["n"], min_n - 1, -1):
            kw2 = {**kw, "n": n}
            sel, info = select_peers(frame, **kw2)
            if sel is not None:
                info["relaxation_step"], info["shortfall"] = label, n < SELECTION_CONFIG["n"]
                return sel, info, label
    return None, {"feasible": False, "note": f"fewer than {min_n} feasible peers: stop this target's comparable valuation"}, None


# ------------------------------------------------------------------ section 5: multiples
def multiple_stats(values: Sequence[float], min_valid: int = 10) -> dict:
    """n_valid, median, mean, PERCENTILE.INC p25/p75. Keep high positive peer multiples (no winsor / PE>100 exclusion).
    Unavailable/NM (NaN, zero or negative denominators) must already be NaN. Flags abs(mean/median-1) > 25%."""
    a = pd.to_numeric(pd.Series(values), errors="coerce").dropna().to_numpy(dtype=float)
    n = len(a)
    if n == 0:
        return {"n_valid": 0, "usable": False}
    med, mean = float(np.median(a)), float(a.mean())
    return {"n_valid": n, "usable": n >= min_valid, "median": med, "mean": mean,
            "p25": percentile_inc(a, .25), "p75": percentile_inc(a, .75),
            "skew_flag": bool(med != 0 and abs(mean / med - 1) > 0.25)}


def scaled_multiple(peer_multiple: Sequence[float], peer_driver: Sequence[float], target_driver: float,
                    driver_scale: float = 1.0, min_valid: int = 10) -> dict:
    """Fundamental adjustment: median(peer multiple / peer driver) x target driver, quartiles from the SAME ratio series.
    PE: driver = 100*g (driver_scale=100); PBV: ROE; PS: net margin; EV/Sales: EBITDA margin. Needs positive meaningful
    drivers for peer and target and >= min_valid scaled observations; otherwise adjustment unavailable."""
    m = pd.to_numeric(pd.Series(peer_multiple), errors="coerce")
    d = pd.to_numeric(pd.Series(peer_driver), errors="coerce") * driver_scale
    ok = m.notna() & d.notna() & (d > 0)
    t = target_driver * driver_scale
    if not (t > 0) or ok.sum() < min_valid:
        return {"available": False, "n_valid": int(ok.sum()), "reason": "target driver not positive or fewer than min_valid scaled peers"}
    ratio = (m[ok] / d[ok]).to_numpy(dtype=float)
    return {"available": True, "n_valid": int(ok.sum()), "median": float(np.median(ratio) * t),
            "p25": percentile_inc(ratio, .25) * t, "p75": percentile_inc(ratio, .75) * t}


# ------------------------------------------------------------------ section 6: bridges
def comparable_ev(mcap: float, debt_incl_leases: float, nci: float, cash: float, associates: float = 0.0) -> float:
    """EV = common equity + debt incl. leases + NCI - cash - nonoperating associates (only if their earnings are
    excluded from the operating denominator)."""
    return mcap + debt_incl_leases + nci - cash - associates


def implied_equity_from_ev(multiple: float, metric: float, debt_incl_leases: float, nci: float, cash: float,
                           associates: float = 0.0) -> float:
    """Invert EXACTLY the numerator construction. Do not also add net-debt cash; a negative result is a
    distress/invalid-method flag, not a negative price."""
    return multiple * metric - debt_incl_leases - nci + cash + associates


def per_share_from_equity_multiple(multiple: float, target_metric_total: float, shares: float) -> float:
    return multiple * target_metric_total / shares


def pence_to_pounds(price_gbx: float) -> float:
    """London quotes are in pence (GBp): divide by 100 before comparing with GBP data."""
    return price_gbx / 100.0
