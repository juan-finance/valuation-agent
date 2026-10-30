"""Regression engine for methodology/regression_procedure.md (sections 2-8, 9 independent check).

This is the *independent fit outside Excel* required by section 9 and a fast way to estimate
the models once per market dataset. It does NOT replace the live-formula workbook that the
procedure requires as a deliverable: use compare_to_linest() to prove the workbook agrees.
Rates are decimals. Column names are those of the DATA_BASE_MSCI.xlsx 'Data' sheet (section 2).
"""
from __future__ import annotations

from dataclasses import dataclass, field
from typing import Mapping, Sequence

import numpy as np
import pandas as pd
from scipy import stats

# ------------------------------------------------------------------ configuration (project settings, section 1)
CONFIG = dict(
    max_PE=100.0, beta_replacement_upper_bound=2.5, winsorize=(0.01, 0.99),
    fair_band=1.0, strong_band=2.0, significance=0.05, corr_warn=0.80, vif_warn=5.0, vif_severe=10.0,
    min_obs_A=30, min_obs_BC={"Europe_full": 150, "Europe_minimum": 100, "World_full": 500, "World_minimum": 150},
    dummy_base_sector="Industrials", dummy_base_region="Europe", min_dummy_category=10,
)

# Section 4 specification: Y and continuous X in this order, with expected signs (section 8; EVEBITDA sign policy
# is the documented implementation convention: g+, tax-, ROIC+, DFR ambiguous).
MODEL_SPECS: dict[str, dict] = {
    "PE":       {"y": "Current PE", "x": ["g", "beta", "Payout ratio"],
                 "signs": {"g": +1, "beta": -1, "Payout ratio": +1}, "uses_payout": True},
    "PBV":      {"y": "PBV", "x": ["Return on Equity", "beta", "Payout ratio"],
                 "signs": {"Return on Equity": +1, "beta": -1, "Payout ratio": +1}, "uses_payout": True},
    "PS":       {"y": "PS", "x": ["Net Profit Margin", "Payout ratio", "g"],
                 "signs": {"Net Profit Margin": +1, "Payout ratio": +1, "g": +1}, "uses_payout": True},
    "EVEBITDA": {"y": "EV/EBITDA", "x": ["g", "DFR", "Tax Rate", "ROIC"],
                 "signs": {"g": +1, "Tax Rate": -1, "ROIC": +1, "DFR": 0}, "uses_payout": False},
}
MODEL_ORDER = ["PE", "PBV", "PS", "EVEBITDA"]


# ------------------------------------------------------------------ percentile / winsorisation
def percentile_inc(x: Sequence[float], p: float) -> float:
    """Excel PERCENTILE.INC (p in 0..1). numpy's default 'linear' method is identical."""
    return float(np.percentile(np.asarray(x, dtype=float), p * 100, method="linear"))


def winsorize(x: Sequence[float], lo: float = 0.01, hi: float = 0.99):
    """Clip at PERCENTILE.INC lo/hi of the given (eligible) set. Returns (clipped, lower, upper)."""
    a = np.asarray(x, dtype=float)
    lower, upper = percentile_inc(a, lo), percentile_inc(a, hi)
    return np.clip(a, lower, upper), lower, upper


def iqr_outlier_flags(y: Sequence[float], k: float = 3.0) -> np.ndarray:
    """D7: raw Y beyond [Q1 - k*IQR, Q3 + k*IQR] (Q via PERCENTILE.INC). Flag only; do not delete in the base case."""
    a = np.asarray(y, dtype=float)
    q1, q3 = percentile_inc(a, .25), percentile_inc(a, .75)
    iqr = q3 - q1
    return (a < q1 - k * iqr) | (a > q3 + k * iqr)


# ------------------------------------------------------------------ beta replacement (section 3 step 2)
def replace_beta(beta: float | None, beta_u: float | None, t_marg: float | None, de: float | None,
                 upper: float = CONFIG["beta_replacement_upper_bound"]):
    """Replace a missing, negative or >2.5 beta with beta_U x [1 + (1 - T_marg) x D/E].
    Returns (value, replaced: bool, note). A missing fallback component leaves beta missing.
    Zero/unusually low positive beta is flagged, not overwritten."""
    missing = beta is None or (isinstance(beta, float) and np.isnan(beta))
    if not missing and 0 <= beta <= upper:
        note = "flag: zero or very low beta - investigate" if beta < 0.2 else "kept"
        return float(beta), False, note
    reason = "missing" if missing else ("negative" if beta < 0 else f">{upper}")
    comps = (beta_u, t_marg, de)
    if any(c is None or (isinstance(c, float) and np.isnan(c)) for c in comps):
        return float("nan"), False, f"beta {reason}; fallback component missing -> beta stays missing"
    return float(beta_u * (1 + (1 - t_marg) * de)), True, f"beta {reason}; replaced by bottom-up relevered beta"


# ------------------------------------------------------------------ eligibility (section 3 step 3)
def eligibility(df: pd.DataFrame, model: str, max_pe: float = CONFIG["max_PE"],
                extra_invalid: pd.Series | None = None) -> pd.DataFrame:
    """One FIRST-failure reason per excluded row. Returns df with columns ['eligible','reason'].
    extra_invalid: boolean Series (True = invalid) for raw-denominator tests the ratio cannot show, e.g. for
    EVEBITDA positive EV AND positive EBITDA (a ratio of two negatives looks positive), PBV positive book equity."""
    spec = MODEL_SPECS[model]
    cols = [spec["y"]] + spec["x"]
    reason = pd.Series("", index=df.index, dtype=object)

    def mark(mask, text):
        nonlocal reason
        m = mask & (reason == "")
        reason = reason.mask(m, text)

    for c in cols:
        if c not in df.columns:
            raise KeyError(f"required column missing from dataset: {c}")
        num = pd.to_numeric(df[c], errors="coerce")
        mark(num.isna() | ~np.isfinite(num), f"missing_or_non_numeric:{c}")
    y = pd.to_numeric(df[spec["y"]], errors="coerce")
    mark(y <= 0, "nonpositive_Y")
    if model == "PE":
        mark(y > max_pe, f"PE>{max_pe:g}")
    if spec["uses_payout"]:
        mark(pd.to_numeric(df["Payout ratio"], errors="coerce") < 0, "negative_payout")
    if extra_invalid is not None:
        mark(extra_invalid.reindex(df.index).fillna(False).astype(bool), "invalid_denominator")
    out = pd.DataFrame({"eligible": reason == "", "reason": reason}, index=df.index)
    return out


# ------------------------------------------------------------------ dummy coding (section 4)
def build_dummies(df: pd.DataFrame, sector_col: str | None = None, region_col: str | None = None,
                  base_sector: str = CONFIG["dummy_base_sector"], base_region: str = CONFIG["dummy_base_region"],
                  min_cat: int = CONFIG["min_dummy_category"]):
    """Sector (B) and/or region (A/B World rows) dummies. Nonbase categories with < min_cat CLEANED rows merge
    into 'Other'. The base must be present and is chosen explicitly (raises otherwise - never a constant-zero
    reference). All-zero columns are omitted. Returns (dummy DataFrame, mapping log dict). C has NO dummies."""
    parts, log = [], {}
    for col, base, label in ((sector_col, base_sector, "sector"), (region_col, base_region, "region")):
        if col is None:
            continue
        s = df[col].astype(str)
        counts = s.value_counts()
        if base not in counts.index:
            raise ValueError(f"base {label} '{base}' absent from the estimation set: choose an observed base "
                             f"explicitly and map the target coding (do not include a constant-zero reference)")
        small = [c for c, n in counts.items() if c != base and n < min_cat]
        mapped = s.where(~s.isin(small), "Other")
        log[label] = {"base": base, "merged_to_Other": small, "counts_before": counts.to_dict()}
        cats = [c for c in mapped.unique() if c != base]
        d = pd.DataFrame({f"{label}:{c}": (mapped == c).astype(float) for c in sorted(cats)}, index=df.index)
        d = d.loc[:, d.sum() > 0]
        parts.append(d)
    return (pd.concat(parts, axis=1) if parts else pd.DataFrame(index=df.index)), log


# ------------------------------------------------------------------ OLS with Excel-LINEST statistics
@dataclass
class OLSResult:
    names: list[str]             # X names in design order (excluding intercept)
    coef: np.ndarray             # [b1..bk]
    intercept: float
    se: np.ndarray
    se_intercept: float
    t: np.ndarray
    p: np.ndarray
    ci_low: np.ndarray
    ci_high: np.ndarray
    r2: float
    adj_r2: float
    sey: float
    F: float
    sig_f: float
    df: int
    ss_reg: float
    ss_res: float
    n: int
    k: int
    t_intercept: float = float("nan")
    p_intercept: float = float("nan")
    dropped_constant: list[str] = field(default_factory=list)

    def coef_series(self) -> pd.Series:
        return pd.Series([self.intercept, *self.coef], index=["const", *self.names])


def ols(y: Sequence[float], X: pd.DataFrame, alpha: float = CONFIG["significance"]) -> OLSResult:
    """OLS with intercept. Removes constant X columns EXPLICITLY (logged in .dropped_constant), checks full column
    rank, requires df = n-k-1 > 0 and positive finite residual variance, else raises (design not estimable)."""
    y = np.asarray(y, dtype=float)
    Xd = X.copy()
    dropped = [c for c in Xd.columns if np.ptp(Xd[c].to_numpy(dtype=float)) == 0]
    if dropped:
        Xd = Xd.drop(columns=dropped)
    n, k = Xd.shape[0], Xd.shape[1]
    if n != len(y):
        raise ValueError("X and y row counts differ")
    A = np.column_stack([np.ones(n), Xd.to_numpy(dtype=float)])
    if np.linalg.matrix_rank(A) < k + 1:
        raise ValueError("design is not full column rank (exact dependency): resolve explicitly, model not estimable")
    df_ = n - k - 1
    if df_ <= 0:
        raise ValueError(f"df = n-k-1 = {df_} <= 0: model not estimable")
    XtX_inv = np.linalg.inv(A.T @ A)
    beta = XtX_inv @ A.T @ y
    resid = y - A @ beta
    ss_res = float(resid @ resid)
    ss_tot = float(((y - y.mean()) ** 2).sum())
    ss_reg = ss_tot - ss_res
    s2 = ss_res / df_
    if not np.isfinite(s2) or s2 <= 0:
        raise ValueError("residual variance not positive/finite: standard errors undefined")
    se_all = np.sqrt(np.diag(XtX_inv) * s2)
    t_all = beta / se_all
    p_all = 2 * stats.t.sf(np.abs(t_all), df_)
    tcrit = stats.t.ppf(1 - alpha / 2, df_)
    r2 = ss_reg / ss_tot
    F = (ss_reg / k) / s2 if k > 0 else float("nan")
    return OLSResult(
        names=list(Xd.columns), coef=beta[1:], intercept=float(beta[0]), se=se_all[1:], se_intercept=float(se_all[0]),
        t=t_all[1:], p=p_all[1:], ci_low=beta[1:] - tcrit * se_all[1:], ci_high=beta[1:] + tcrit * se_all[1:],
        r2=float(r2), adj_r2=float(1 - (1 - r2) * (n - 1) / (n - k - 1)), sey=float(np.sqrt(s2)), F=float(F),
        sig_f=float(stats.f.sf(F, k, df_)), df=df_, ss_reg=float(ss_reg), ss_res=ss_res, n=n, k=k,
        t_intercept=float(t_all[0]), p_intercept=float(p_all[0]), dropped_constant=dropped)


def vif(X: pd.DataFrame) -> pd.Series:
    """VIF_j = diag(inverse(correlation matrix of X)); 1 for a single X. Singular -> raises (design failure)."""
    if X.shape[1] == 1:
        return pd.Series([1.0], index=X.columns)
    corr = np.corrcoef(X.to_numpy(dtype=float), rowvar=False)
    if np.linalg.matrix_rank(corr) < corr.shape[0]:
        raise ValueError("correlation matrix singular: design failure, do not invent VIF")
    return pd.Series(np.diag(np.linalg.inv(corr)), index=X.columns)


def linest_layout(res: OLSResult) -> np.ndarray:
    """What Excel LINEST(Y,X,TRUE,TRUE) returns: 5 x (k+1); coefficients in REVERSE X order, intercept last.
    Row 3 = R2, SEy; row 4 = F, df; row 5 = SS_reg, SS_resid; unused cells are NaN (documented #N/A)."""
    k = res.k
    out = np.full((5, k + 1), np.nan)
    out[0, :] = [*res.coef[::-1], res.intercept]
    out[1, :] = [*res.se[::-1], res.se_intercept]
    out[2, 0], out[2, 1] = res.r2, res.sey
    out[3, 0], out[3, 1] = res.F, res.df
    out[4, 0], out[4, 1] = res.ss_reg, res.ss_res
    return out


def compare_to_linest(res: OLSResult, excel_linest: np.ndarray, rel_tol: float = 1e-6, abs_tol: float = 1e-8) -> list[str]:
    """Section 9 check: independent fit vs the recalculated workbook's LINEST block.
    Relative difference < 1e-6 where the reference is nonzero; for |reference| < 1e-8 use absolute 1e-8.
    Returns a list of mismatch descriptions (empty list = pass). Never copy these numbers into the workbook."""
    ref, got = linest_layout(res), np.asarray(excel_linest, dtype=float)
    if ref.shape != got.shape:
        return [f"shape mismatch: independent {ref.shape} vs workbook {got.shape} (column removal / df differences?)"]
    problems = []
    for (i, j), r in np.ndenumerate(ref):
        g = got[i, j]
        if np.isnan(r) and np.isnan(g):
            continue
        if np.isnan(r) != np.isnan(g):
            problems.append(f"cell ({i+1},{j+1}): NaN mismatch ref={r} workbook={g}")
            continue
        ok = abs(r - g) < abs_tol if abs(r) < 1e-8 else abs(r - g) / abs(r) < rel_tol
        if not ok:
            problems.append(f"cell ({i+1},{j+1}): ref={r:.12g} workbook={g:.12g}")
    return problems


# ------------------------------------------------------------------ model fitting pipeline
@dataclass
class FitResult:
    model: str
    scope: str
    ols: OLSResult
    design: pd.DataFrame        # winsorised continuous X + dummies actually used
    y: pd.Series                # winsorised Y actually used
    y_raw: pd.Series
    cutoffs: dict               # column -> (lower, upper)
    n_raw: int
    excluded: pd.DataFrame      # index, reason (first failure)
    dummy_log: dict
    outlier_flags_raw_y: pd.Series
    median_y: float


def fit_model(df: pd.DataFrame, model: str, scope: str = "", sector_col: str | None = None,
              region_col: str | None = None, dummies: bool = False, extra_invalid: pd.Series | None = None,
              winsor: tuple[float, float] = CONFIG["winsorize"], fixed_cutoffs: Mapping | None = None,
              drop_x: Sequence[str] = (), exclude_index: Sequence | None = None,
              base_sector: str = CONFIG["dummy_base_sector"], base_region: str = CONFIG["dummy_base_region"]) -> FitResult:
    """eligibility -> winsorise Y and continuous X within the eligible set -> (dummies) -> OLS.
    fixed_cutoffs / drop_x / exclude_index implement the robustness refits of section 8 (base cutoffs retained)."""
    spec = MODEL_SPECS[model]
    elig = eligibility(df, model, extra_invalid=extra_invalid)
    mask = elig["eligible"].copy()
    if exclude_index is not None:
        drop = pd.Index(exclude_index).intersection(df.index)
        elig.loc[drop, "reason"] = elig.loc[drop, "reason"].mask(elig.loc[drop, "reason"] == "", "robustness_exclusion")
        mask.loc[drop] = False
    sub = df[mask]
    xcols = [c for c in spec["x"] if c not in drop_x]
    cut, cols = {}, {}
    for c in [spec["y"], *xcols]:
        vals = pd.to_numeric(sub[c], errors="coerce").to_numpy()
        if fixed_cutoffs and c in fixed_cutoffs:
            lo_, hi_ = fixed_cutoffs[c]
            w = np.clip(vals, lo_, hi_)
        else:
            w, lo_, hi_ = winsorize(vals, *winsor)
        cut[c], cols[c] = (lo_, hi_), w
    Xc = pd.DataFrame({c: cols[c] for c in xcols}, index=sub.index)
    dlog: dict = {}
    if dummies:
        D, dlog = build_dummies(sub, sector_col, region_col, base_sector, base_region)
        Xc = pd.concat([Xc, D], axis=1)
    y_w = pd.Series(cols[spec["y"]], index=sub.index)
    res = ols(y_w.to_numpy(), Xc)
    y_raw = pd.to_numeric(sub[spec["y"]], errors="coerce")
    return FitResult(model, scope, res, Xc.drop(columns=res.dropped_constant), y_w, y_raw, cut, len(df),
                     elig.loc[~mask, ["reason"]], dlog, pd.Series(iqr_outlier_flags(y_raw.to_numpy()), index=sub.index),
                     float(np.median(y_raw)))


def choose_scope_A(candidates: Sequence[tuple[str, pd.DataFrame]], model: str, min_obs: int = CONFIG["min_obs_A"]):
    """Section 1 ladder for A: pass (label, frame) in the configured order (Europe Industry, Europe Industry Group,
    World Industry, World Industry Group, World Sector); returns the first with >= min_obs eligible rows, else None.
    Never insert Europe Sector earlier in the ladder."""
    for label, frame in candidates:
        if int(eligibility(frame, model)["eligible"].sum()) >= min_obs:
            return label, frame
    return None


# ------------------------------------------------------------------ prediction, classification, diagnostics
def design_row(fit: FitResult, x: Mapping[str, float]) -> np.ndarray:
    """Order a target's actual (un-winsorised) X values to the saved design; dummies missing from x default to 0."""
    return np.array([float(x.get(c, 0.0)) for c in fit.design.columns])


def predict(fit: FitResult, x: Mapping[str, float]) -> float:
    """b0 + sum(b_j x_j), coefficients mapped from design order (not LINEST reverse order). Rates in decimals."""
    return float(fit.ols.intercept + design_row(fit, x) @ fit.ols.coef)


def extrapolation_flags(fit: FitResult, x: Mapping[str, float]) -> list[str]:
    """D10: target X outside the fitted MIN/MAX of the estimation design (continuous columns only)."""
    out = []
    for c in fit.design.columns:
        if ":" in c:
            continue
        v = float(x[c])
        lo, hi = fit.design[c].min(), fit.design[c].max()
        if v < lo or v > hi:
            out.append(f"{c}={v:.4g} outside fitted range [{lo:.4g}, {hi:.4g}]")
    return out


def classify_residual(std_resid: float | None, fair: float = CONFIG["fair_band"], strong: float = CONFIG["strong_band"]) -> str:
    """Prescribed residual bands (labels, not statistical tests). Guards missing/invalid input."""
    if std_resid is None or not np.isfinite(std_resid):
        return "Not classified (undefined residual)"
    if std_resid < -strong:
        return "Significantly undervalued"
    if std_resid < -fair:
        return "Moderately undervalued"
    if std_resid <= fair:
        return "Fairly valued"
    if std_resid <= strong:
        return "Moderately overvalued"
    return "Significantly overvalued"


def value_target(fit: FitResult, x: Mapping[str, float], actual_multiple: float, max_pe: float = CONFIG["max_PE"]) -> dict:
    """Target valuation view (section 7): actual X (not clipped) -> predicted multiple; actual multiple for residuals.
    Returns a status instead of silently dropping targets."""
    res = {"model": fit.model, "scope": fit.scope}
    needed = [c for c in fit.design.columns if ":" not in c]
    if any(c not in x or x[c] is None or not np.isfinite(float(x[c])) for c in needed):
        return {**res, "status": "Not valued - missing data"}
    pred = predict(fit, x)
    if fit.model == "PE" and actual_multiple > max_pe:
        return {**res, "status": f"Not valued by PE regression (above {max_pe:g}x)", "predicted": pred}
    if pred <= 0:
        return {**res, "status": "Not valued (nonpositive prediction)", "predicted": pred}
    resid = actual_multiple - pred
    std = resid / fit.ols.sey
    return {**res, "status": "valued", "predicted": pred, "actual": actual_multiple, "residual": resid,
            "std_residual": std, "deviation": actual_multiple / pred - 1, "classification": classify_residual(std),
            "extrapolation": extrapolation_flags(fit, x), "outside_3sd": abs(std) > 3}


def diagnostics(fit: FitResult) -> dict:
    """Mechanical model-level D1-D5, D7, D9 (D6, D8-per-target and D10 are target-level: value_target)."""
    o, spec = fit.ols, MODEL_SPECS[fit.model]
    cont = [c for c in fit.design.columns if ":" not in c]
    out = {"D1_sig_F_below_0.05": o.sig_f < CONFIG["significance"], "D2_r2_below_0.20": o.r2 < 0.20}
    out["D3_nonsignificant_vars"] = [n for n, p in zip(o.names, o.p) if p >= CONFIG["significance"]]
    bad = []
    for n, b in zip(o.names, o.coef):
        s = spec["signs"].get(n)
        if s not in (None, 0) and np.sign(b) != s:
            bad.append(n + (" (significant)" if o.p[o.names.index(n)] < CONFIG["significance"] else ""))
    out["D4_sign_disagreements"] = bad
    if len(cont) > 1:
        corr = fit.design[cont].corr()
        pairs = [(a, b, float(corr.loc[a, b])) for i, a in enumerate(cont) for b in cont[i + 1:]
                 if abs(corr.loc[a, b]) > CONFIG["corr_warn"]]
        v = vif(fit.design[cont])
    else:
        pairs, v = [], vif(fit.design[cont])
    out["D5_high_pairwise_corr"] = pairs
    out["D5_vif"] = v.to_dict()
    out["D5_vif_warn"] = bool((v > CONFIG["vif_warn"]).any())
    out["D5_vif_severe"] = bool((v > CONFIG["vif_severe"]).any())
    out["D5_highest_vif_var"] = v.idxmax()
    out["D7_raw_y_outliers"] = fit.outlier_flags_raw_y[fit.outlier_flags_raw_y].index.tolist()
    out["D8_estimation_abs_std_resid_gt_3"] = None  # needs fitted values: use residuals() below
    out["D9_n_below_10k"] = o.n < 10 * o.k
    return out


def residuals(fit: FitResult) -> pd.Series:
    """Estimation-set residuals from the winsorised Y/X actually used in the fit."""
    fitted = fit.ols.intercept + fit.design.to_numpy(dtype=float) @ fit.ols.coef
    return fit.y - fitted


def typicality_test(pool: pd.DataFrame, target: Mapping[str, float],
                    cols: Sequence[str] = ("Return on Equity", "beta", "Payout ratio", "g")) -> dict:
    """A-scope test 2: target ROE, beta, payout AND g all within inclusive p10-p90 of the eligible sector pool, computed
    on valid PRE-winsor fundamentals with actual (unclipped) target values. Any missing input fails."""
    detail, ok = {}, True
    for c in cols:
        v = target.get(c)
        vals = pd.to_numeric(pool[c], errors="coerce").dropna().to_numpy()
        if v is None or not np.isfinite(float(v)) or len(vals) == 0:
            detail[c] = {"value": v, "pass": False, "reason": "missing"}
            ok = False
            continue
        lo, hi = percentile_inc(vals, .10), percentile_inc(vals, .90)
        passed = lo <= float(v) <= hi
        detail[c] = {"value": float(v), "p10": lo, "p90": hi, "pass": passed}
        ok &= passed
    return {"typical": ok, "detail": detail}


def rank_models(candidates: Sequence[dict]) -> list[dict]:
    """Rank eligible routed models by adjusted R2 (project heuristic). Ties: smaller SEy/median(Y), then MODEL_ORDER.
    Each candidate: {'model','adj_r2','sey','median_y', ...}. Returns the sorted list (first = chosen, next two = alternatives)."""
    def key(c):
        rel = c["sey"] / c["median_y"] if c.get("median_y", 0) > 0 else float("inf")
        return (-round(c["adj_r2"], 12), rel, MODEL_ORDER.index(c["model"]))
    return sorted(candidates, key=key)
