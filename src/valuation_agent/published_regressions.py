"""Damodaran's published market-wide regressions of multiples (MReg26 style), parsed from the Markdown file.

What the file gives per equation: coefficients, t-statistics (for the constant and each term), R2 and the region.
What it does NOT give: n, residual standard error (SEy), p-values, adjusted R2, sector terms. Therefore this module
produces a point prediction only. It never invents SEy and cannot produce the residual-band classification.
"""
from __future__ import annotations

import math
import re
from dataclasses import dataclass, field

from . import mdtables

# ----------------------------------------------------------------------------- vocabulary
REGION_ALIASES = {  # label in the file -> canonical region code (see data/regions.csv)
    "us": "US", "united states": "US", "europe": "EUROPE", "western europe": "EUROPE",
    "japan": "JAPAN", "emerging markets": "EM", "emerging market": "EM", "global": "GLOBAL",
    "aus, nz & canada": "ANZCA", "australia, nz and canada": "ANZCA", "aus, nz and canada": "ANZCA",
}
VAR_CANON = {  # text inside \text{...} -> canonical variable
    "beta": "beta", "g_eps": "g_eps", "g": "g_rev", "payout": "payout", "payout ratio": "payout", "roe": "roe", "roic": "roic",
    "dfr": "dfr", "oper margin": "oper_margin", "tax rate": "tax_rate",
}
DEPENDENT_CANON = {"PE": "PE", "PEG": "PEG", "PBV": "PBV", "EV/Invested Capital": "EV/IC", "EV/Sales": "EV/Sales",
                   "EV/EBITDA": "EV/EBITDA"}
# published multiple -> multiple name used by regression_procedure.md / valuation_multiples.csv (PS has no published twin)
REPO_MULTIPLE = {"PE": "PE", "PBV": "PBV", "EV/EBITDA": "EVEBITDA"}
VAR_DEFINITIONS = {  # from the file's 'Variable Definitions' blocks
    "beta": "regression beta (levered)", "g_eps": "expected EPS growth, next 5 years (analyst estimates)",
    "g_rev": "expected revenue growth, next 5 years (use g_eps if unavailable)", "payout": "dividends / earnings",
    "roe": "net income / book value of equity", "roic": "EBIT(1-tax rate) / invested capital",
    "dfr": "total debt / (total debt + market value of equity)", "oper_margin": "pre-tax operating income / sales",
    "tax_rate": "effective tax rate = taxes paid / taxable income",
}
# Unit problem: the file says 'stay true to decimal format', but the coefficient scale of DFR and Tax rate (-0.05 ... -0.24
# with t-stats of 4-90) implies percentage points (0-100). Unresolved from the files alone -> predict() demands a policy.
UNIT_POLICIES = {
    "as_published_note": {},                                   # everything decimal, as the file's instruction says
    "dfr_tax_percent_points": {"dfr": 100.0, "tax_rate": 100.0},  # inferred from coefficient scale
}


@dataclass
class Term:
    variable: str          # canonical name, e.g. 'beta'
    coef: float
    tstat: float
    transform: str = ""    # '' or 'ln'


@dataclass
class Equation:
    region: str                    # canonical region code
    region_label: str              # as written in the file
    dependent: str                 # canonical, e.g. 'PE', 'EV/EBITDA'
    constant: float
    constant_tstat: float
    terms: list[Term]
    r2: float
    note: str = ""
    source_section: str = ""
    raw: str = ""

    @property
    def variables(self) -> list[str]:
        return [t.variable for t in self.terms]

    @property
    def repo_multiple(self):
        return REPO_MULTIPLE.get(self.dependent)

    def key(self) -> tuple[str, str]:
        return (self.dependent, self.region)


# ----------------------------------------------------------------------------- parsing
_TERM = re.compile(r"(?P<sign>[+\-−])?\s*\\underset\{\((?P<t>[\d.]+)\)\}\{(?P<c>[+\-−]?[\d.]+)\}\s*(?:\\,)?\s*(?P<var>.*?)(?=\s*[+\-−]\s*\\underset|\s*$)")


def _canon_var(text: str):
    ln = re.search(r"\\ln\((.*)\)", text)
    transform = "ln" if ln else ""
    inner = ln.group(1) if ln else text
    inner = inner.strip()
    m = re.search(r"\\text\{([^}]*)\}", inner)
    name = (m.group(1) if m else inner).strip()
    if re.fullmatch(r"g_\{\\text\{EPS\}\}", inner) or name.upper() == "EPS" and inner.startswith("g_"):
        name = "g_EPS"
    key = name.lower()
    if key not in VAR_CANON:
        raise ValueError(f"unrecognised variable '{text}' (canonical map has: {sorted(VAR_CANON)})")
    return VAR_CANON[key], transform


def parse_equation_cell(cell: str, region_label: str, r2: float, section: str = "") -> Equation:
    note_m = re.search(r"\*\((.*?)\)\*", cell)
    note = note_m.group(1) if note_m else ""
    body = cell.replace("\\_", "_")
    body = re.sub(r"\*\(.*?\)\*", "", body).strip().strip("$").strip()
    lhs, rhs = body.split("=", 1)
    dep_m = re.search(r"\\text\{([^}]*)\}", lhs)
    dep_txt = dep_m.group(1).strip() if dep_m else lhs.strip()
    if dep_txt not in DEPENDENT_CANON:
        raise ValueError(f"unrecognised dependent variable '{dep_txt}'")
    parts = [m for m in _TERM.finditer(rhs.strip())]
    if not parts:
        raise ValueError(f"no terms found in: {cell[:80]}")
    first = parts[0]
    if first.group("var").strip():
        raise ValueError("first term should be the constant")
    sgn = lambda s: -1.0 if s in ("-", "−") else 1.0
    const = sgn(first.group("sign")) * float(first.group("c").replace("−", "-"))
    terms = []
    for m in parts[1:]:
        var, tr = _canon_var(m.group("var"))
        coef = sgn(m.group("sign")) * float(m.group("c").replace("−", "-"))
        terms.append(Term(var, coef, float(m.group("t")), tr))
    label_key = region_label.strip().lower()
    if label_key not in REGION_ALIASES:
        raise ValueError(f"unknown region label '{region_label}'")
    return Equation(REGION_ALIASES[label_key], region_label.strip(), DEPENDENT_CANON[dep_txt], const, float(first.group("t")),
                    terms, r2, note, section, cell)


def _r2(cell: str) -> float:
    v = mdtables.to_number(cell)
    return v[0] if v else math.nan


def load(path) -> dict:
    """Parse the whole file. Returns {'by_multiple': [Equation], 'by_region': [Equation], 'meta': {...}}.
    The file prints every equation twice (classified by region, classified by multiple); both views are parsed so they can
    be cross-checked (see datasets.check_dataset)."""
    text = mdtables.read(path)
    meta = mdtables.extract_meta(text)
    by_mult, by_reg = [], []
    region_titles = {"US Companies": "US", "European Companies": "Europe", "Japanese Companies": "Japan",
                     "Emerging Market Companies": "Emerging Markets", "Global Companies": "Global"}
    for t in mdtables.parse_tables(text):
        if t.header[:2] == ["Regression", "$R^2$"] and len(t.header) == 3 and t.header[2] == "Region":
            for r in t.rows:
                by_mult.append(parse_equation_cell(r[0], r[2], _r2(r[1]), t.context))
        elif t.header[:2] == ["Regression", "$R^2$"] and len(t.header) == 2:
            label = next((v for k, v in region_titles.items() if k in t.context), None)
            if label is None:
                continue                     # legend table or unknown section
            for r in t.rows:
                by_reg.append(parse_equation_cell(r[0], label, _r2(r[1]), t.context))
    return {"by_multiple": by_mult, "by_region": by_reg, "meta": meta}


# ----------------------------------------------------------------------------- prediction
def _units(policy):
    if isinstance(policy, dict):
        return policy
    if policy not in UNIT_POLICIES:
        raise ValueError(f"unit policy must be one of {sorted(UNIT_POLICIES)} or a dict of scale factors; got {policy!r}")
    return UNIT_POLICIES[policy]


def predict(eq: Equation, inputs: dict, unit_policy) -> float:
    """Predicted multiple. `inputs` are DECIMALS (0.25 = 25%), beta as a number, keyed by canonical variable name.
    `unit_policy` is REQUIRED (no default): 'as_published_note' | 'dfr_tax_percent_points' | custom {var: scale}.
    Raises if an input is missing/non-finite or ln() gets a non-positive value. Does not clip or repair anything."""
    scale = _units(unit_policy)
    total = eq.constant
    for t in eq.terms:
        if t.variable not in inputs or inputs[t.variable] is None or not math.isfinite(float(inputs[t.variable])):
            raise ValueError(f"missing input '{t.variable}' ({VAR_DEFINITIONS.get(t.variable, '')})")
        x = float(inputs[t.variable]) * scale.get(t.variable, 1.0)
        if t.transform == "ln":
            if x <= 0:
                raise ValueError(f"ln({t.variable}) needs a positive value (got {x})")
            x = math.log(x)
        total += t.coef * x
    return total


def predict_both_policies(eq: Equation, inputs: dict) -> dict:
    """Predictions under each unit policy. Where they differ materially the unit question matters: record the policy chosen,
    why, and the sector-median plausibility check in the decisions file."""
    out = {name: predict(eq, inputs, name) for name in UNIT_POLICIES}
    vals = list(out.values())
    out["max_abs_difference"] = max(vals) - min(vals)
    out["max_relative_difference"] = (max(vals) - min(vals)) / abs(vals[0]) if vals[0] else math.nan
    out["uses_dfr_or_tax"] = any(v in ("dfr", "tax_rate") for v in eq.variables)
    return out


def peg_to_pe(peg: float, g_eps_decimal: float) -> float:
    """PEG regressions predict PEG = PE / (100 x g). Convert back to a PE before valuing earnings. The 100x convention is the
    repo's PEG definition (comparables_procedure.md); Damodaran's own convention is not stated in the file: confirm."""
    return peg * 100.0 * g_eps_decimal


def to_rows(eqs: list[Equation]):
    """Flat table for audit/printing."""
    rows = []
    for e in eqs:
        rows.append({"dependent": e.dependent, "region": e.region, "r2": e.r2, "n_terms": len(e.terms),
                     "equation": f"{e.constant:+.4g} " + " ".join(f"{t.coef:+.4g}*{('ln(' + t.variable + ')') if t.transform else t.variable}" for t in e.terms),
                     "note": e.note})
    return rows
