"""Reference-data library: a registry of Damodaran (and later other) datasets, and a resolver that picks the right one.

Why: the agent must not hard-wire 'the Europe file'. For each need (family = beta, capex, ctryprem, regressions, ...) it asks
`resolve(family, country=..., valuation_date=...)` and gets the best registered dataset, how good the match is (exact or fallback
region), and warnings. Adding a new region or vintage = drop the .md file and run `python -m valuation_agent.datasets add <file>`;
no code change. Mapping tables are CSVs in data/ so they can be edited by hand:
  registry.csv          one row per dataset file (id, family, region, vintage, as_of_date, path, sha256, ...)
  regions.csv           country -> canonical region code (+ confidence and note)
  region_fallbacks.csv  region -> ordered fallback chain (always ends in GLOBAL)
  country_aliases.csv   UK/USA/ISO2 -> the country name used in the files
  column_maps.csv       logical column name -> accepted header spellings per family

CLI: python -m valuation_agent.datasets list | resolve <family> [--country X] [--region R] [--date D] | add <file> | check [id] | columns <id>
"""
from __future__ import annotations

import csv
import difflib
import hashlib
import math
import re
import shutil
import sys
from dataclasses import dataclass, field, asdict
from datetime import date, datetime
from pathlib import Path

import pandas as pd

from . import mdtables, published_regressions as pr

DATA_DIR = Path(__file__).resolve().parents[2] / "data"
REGISTRY_FIELDS = ["dataset_id", "family", "region_code", "regions_inside", "vintage", "as_of_date", "source_title", "source_url",
                   "path", "sha256", "original_filename", "added_on", "applies_to", "status", "notes"]
FAMILIES = {   # what the agent expects to find; add rows to column_maps.csv after verifying real headers of a new family
    "beta": "industry betas and unlevered betas", "capex": "net capex, D&A, sales/invested capital by industry",
    "wcdata": "working capital by industry (expected, not yet supplied)", "dbtfund": "debt ratios by industry (expected, not yet supplied)",
    "ctryprem": "country risk premiums, default spreads, mature ERP", "regressions": "published market-wide multiple regressions",
    "pe_industry": "industry PE statistics (future)", "pbv_industry": "industry PBV statistics (future)",
    "evebitda_industry": "industry EV/EBITDA statistics (future)", "ratings": "rating to spread tables (future)",
}
TITLE_PATTERNS = [   # (regex on the file's '# ' title, family, group index of the region label or None)
    (r"^Betas? and Risk Measures by Industry:\s*(.+)$", "beta", 1),
    (r"^Capital Expenditures.*:\s*(.+)$", "capex", 1),
    (r"^Regressions of Multiples on Fundamentals:\s*(.+)$", "regressions", 1),
    (r"^Country and Equity Risk Premiums", "ctryprem", None),
]
REGION_LABELS = dict(pr.REGION_ALIASES, **{"market wide": "MULTI", "india": "INDIA", "china": "CHINA",
                                            "australia, nz & canada": "ANZCA"})


# ----------------------------------------------------------------------------- tables
def _csv(name: str, data_dir: Path) -> list[dict]:
    p = data_dir / name
    if not p.exists():
        return []
    with open(p, newline="", encoding="utf-8") as fh:
        return list(csv.DictReader(fh))


@dataclass
class DatasetRow:
    dataset_id: str
    family: str
    region_code: str
    regions_inside: str
    vintage: str
    as_of_date: str
    source_title: str
    source_url: str
    path: str
    sha256: str
    original_filename: str
    added_on: str
    applies_to: str
    status: str
    notes: str

    def regions(self) -> set[str]:
        if self.regions_inside.strip().upper() == "ALL":
            return {"ALL"}
        return {r for r in (self.regions_inside or self.region_code).split("|") if r}

    def abspath(self, data_dir: Path) -> Path:
        return (data_dir / self.path)


def registry(data_dir: Path | str | None = None) -> list[DatasetRow]:
    d = Path(data_dir) if data_dir else DATA_DIR
    return [DatasetRow(**{k: r.get(k, "") or "" for k in REGISTRY_FIELDS}) for r in _csv("registry.csv", d)]


def _write_registry(rows: list[DatasetRow], d: Path) -> None:
    with open(d / "registry.csv", "w", newline="", encoding="utf-8") as fh:
        w = csv.DictWriter(fh, fieldnames=REGISTRY_FIELDS, lineterminator="\n")
        w.writeheader()
        for r in sorted(rows, key=lambda x: (x.family, x.region_code, x.as_of_date)):
            w.writerow(asdict(r))


# ----------------------------------------------------------------------------- countries and regions
def _norm(s: str) -> str:
    return re.sub(r"\s+", " ", s.strip().lower())


def country_info(country: str, data_dir: Path | str | None = None) -> dict:
    """Canonical country name, region code, preferred region chain, confidence and warnings."""
    d = Path(data_dir) if data_dir else DATA_DIR
    rows = _csv("regions.csv", d)
    by_name = {_norm(r["country"]): r for r in rows}
    aliases = {_norm(r["alias"]): r["country"] for r in _csv("country_aliases.csv", d)}
    key = _norm(country)
    if key in aliases:
        key = _norm(aliases[key])
    if key not in by_name:
        close = difflib.get_close_matches(key, list(by_name), n=4, cutoff=0.6)
        raise KeyError(f"country '{country}' not found in regions.csv. Close matches: {[by_name[c]['country'] for c in close]}. "
                       f"Use the exact name from the risk-premium file or add an alias to country_aliases.csv.")
    r = by_name[key]
    fb = {x["region_code"]: x["fallback_chain"].split("|") for x in _csv("region_fallbacks.csv", d)}
    chain = r["preferred_regions"].split("|") if r["preferred_regions"] else fb.get(r["region_code"], [r["region_code"], "GLOBAL"])
    warns = [f"{r['country']}: region mapping confidence {r['confidence']}. {r['note']}".strip()] if r["confidence"] != "high" else []
    return {"country": r["country"], "region_code": r["region_code"], "chain": chain, "confidence": r["confidence"],
            "rp_region": r["rp_region"], "warnings": warns}


def region_chain(region: str, data_dir: Path | str | None = None) -> list[str]:
    d = Path(data_dir) if data_dir else DATA_DIR
    fb = {x["region_code"]: x["fallback_chain"].split("|") for x in _csv("region_fallbacks.csv", d)}
    return fb.get(region.upper(), [region.upper(), "GLOBAL"])


# ----------------------------------------------------------------------------- resolver
@dataclass
class Resolution:
    found: bool
    dataset: DatasetRow | None
    region_used: str | None          # region code matched (for multi-region sets: the region inside the set)
    match_level: str                 # exact | fallback | none
    requested_chain: list[str]
    tried: list[str] = field(default_factory=list)
    warnings: list[str] = field(default_factory=list)
    message: str = ""
    path: Path | None = None

    def summary(self) -> str:
        if not self.found:
            return f"NOT FOUND: {self.message}"
        d = self.dataset
        return (f"{d.dataset_id} [{self.match_level}: wanted {self.requested_chain[0]}, got {self.region_used}] "
                f"vintage {d.vintage}, as_of {d.as_of_date}, {d.path}" + (f" | WARN: {'; '.join(self.warnings)}" if self.warnings else ""))


def _to_date(v) -> str | None:
    if v is None or v == "":
        return None
    return v.isoformat() if isinstance(v, (date, datetime)) else str(v)[:10]


def resolve(family: str, country: str | None = None, region: str | None = None, valuation_date=None, vintage: str | None = None,
            enterprise_type: str | None = None, data_dir: Path | str | None = None) -> Resolution:
    """Pick the dataset of `family` that best fits. Order: region chain (exact region first, then fallbacks ending in GLOBAL);
    within a region the LATEST dataset whose as_of_date <= valuation_date (later ones are excluded as look-ahead);
    `vintage` pins a vintage. enterprise_type filters datasets whose applies_to is not 'all'.
    The agent must still decide whether a fallback is acceptable for the company at hand and record that in the decisions file."""
    d = Path(data_dir) if data_dir else DATA_DIR
    warnings: list[str] = []
    if country:
        ci = country_info(country, d)
        chain, warnings = ci["chain"], list(ci["warnings"])
    elif region:
        chain = region_chain(region, d)
    else:
        chain = ["GLOBAL"]
    vd = _to_date(valuation_date)
    tried: list[str] = []
    rows = [r for r in registry(d) if r.family == family]
    if not rows:
        return Resolution(False, None, None, "none", chain, tried, warnings,
                          f"no '{family}' dataset registered. {_how_to_add(family)}")
    ok = []
    for r in rows:
        if vintage and r.vintage != vintage:
            tried.append(f"{r.dataset_id}: skipped (vintage pinned to {vintage})")
        elif r.applies_to not in ("all", "") and enterprise_type and r.applies_to != enterprise_type:
            tried.append(f"{r.dataset_id}: skipped (applies to {r.applies_to}, need {enterprise_type})")
        elif vd and r.as_of_date and r.as_of_date > vd:
            tried.append(f"{r.dataset_id}: excluded, as_of {r.as_of_date} is after valuation date {vd} (look-ahead)")
        else:
            ok.append(r)
    for i, reg in enumerate(chain):
        hits = [r for r in ok if reg in r.regions() or "ALL" in r.regions()]
        if hits:
            best = max(hits, key=lambda r: r.as_of_date)
            level = "exact" if i == 0 else "fallback"
            if level == "fallback":
                warnings.append(f"no '{family}' dataset for {chain[0]}; using {reg}. Decide whether this is representative and record it.")
            if len(hits) > 1:
                tried.append(f"{len(hits)} vintages available in {reg}; latest allowed chosen: {best.vintage}")
            res = Resolution(True, best, "ALL" if "ALL" in best.regions() else reg, level, chain, tried, warnings, "", best.abspath(d))
            return res
        tried.append(f"{reg}: no '{family}' dataset")
    present = sorted({f"{r.region_code}@{r.vintage}" for r in rows})
    return Resolution(False, None, None, "none", chain, tried, warnings,
                      f"no usable '{family}' dataset for regions {chain} as of {vd or 'any date'} (registered: {present}). "
                      f"{_how_to_add(family)}")


def _how_to_add(family: str) -> str:
    return (f"Ask the user to supply the Damodaran '{family}' file for that region (Markdown), then run "
            f"`python -m valuation_agent.datasets add <file>`. Do not substitute another family or an unverified web number.")


def resolve_for_company(family: str, listing_country: str, revenue_by_country: dict | None = None, min_share: float = 0.25,
                        valuation_date=None, data_dir=None) -> dict:
    """Primary resolution for the listing country plus one for every other country holding >= min_share of revenue.
    Gives the agent the options; the choice (listing region, global, or a blend) is a judgement recorded in dcf_decisions.md."""
    out = {"primary": resolve(family, country=listing_country, valuation_date=valuation_date, data_dir=data_dir), "others": {}, "note": ""}
    for c, w in (revenue_by_country or {}).items():
        if w >= min_share and c != listing_country:
            out["others"][c] = resolve(family, country=c, valuation_date=valuation_date, data_dir=data_dir)
    if out["others"]:
        out["note"] = ("Material revenue outside the listing country: dcf_procedure.md section 7 allows global data when more "
                       "representative of a multinational. Compare the options and record the choice.")
    return out


# ----------------------------------------------------------------------------- column maps
def column_map(family: str, data_dir=None) -> dict[str, dict]:
    d = Path(data_dir) if data_dir else DATA_DIR
    return {r["logical_name"]: {"aliases": r["header_aliases"].split("|"), "kind": r["kind"], "note": r["note"]}
            for r in _csv("column_maps.csv", d) if r["family"] == family}


def pick_column(df: pd.DataFrame, family: str, logical: str, data_dir=None) -> str:
    """Actual header of `logical` in df (first alias present). Raises with the available headers if none matches,
    so a renamed header is a visible stop, not a silent wrong column."""
    cm = column_map(family, data_dir)
    if logical not in cm:
        raise KeyError(f"no column map for {family}.{logical}; known: {sorted(cm)}")
    lower = {_norm(c): c for c in df.columns}
    for a in cm[logical]["aliases"]:
        if _norm(a) in lower:
            return lower[_norm(a)]
    raise KeyError(f"none of {cm[logical]['aliases']} found for {family}.{logical}; headers are {list(df.columns)}")


# ----------------------------------------------------------------------------- loaders
def _industry_frame(path: Path):
    text = mdtables.read(path)
    tabs = [t for t in mdtables.parse_tables(text) if t.header and t.header[0] == "Industry Name"]
    if not tabs:
        raise ValueError(f"{path.name}: no table whose first column is 'Industry Name'")
    df, units = mdtables.to_frame(tabs[0])
    df["is_aggregate"] = df["Industry Name"].str.contains("Grand Total|Total Market", regex=True)
    meta = mdtables.extract_meta(text)
    df.attrs.update({"units": units, "meta": meta})
    m = re.search(r"Marginal Tax Rate Used:\*?\*?\s*\$?([\d.]+)\s*\\?%", text.replace("**", ""))
    if m:
        df.attrs["marginal_tax_rate_used"] = float(m.group(1)) / 100.0
    return df


def load_industry(ds: DatasetRow, data_dir=None) -> pd.DataFrame:
    d = Path(data_dir) if data_dir else DATA_DIR
    return _industry_frame(ds.abspath(d))


def industry_row(df: pd.DataFrame, name: str) -> pd.Series:
    """Exact (case-insensitive) match of the industry name; otherwise raises with close matches. Map each business segment to
    its actual industry and record the mapping."""
    names = df["Industry Name"].tolist()
    exact = [n for n in names if _norm(n) == _norm(name)]
    if exact:
        return df[df["Industry Name"] == exact[0]].iloc[0]
    close = difflib.get_close_matches(name, names, n=5, cutoff=0.4)
    raise KeyError(f"industry '{name}' not found. Closest: {close}")


def get_value(df: pd.DataFrame, family: str, industry: str, logical: str, data_dir=None) -> float:
    """Convenience: value of a logical column for an industry, e.g. get_value(beta_df,'beta','Power','beta_unlevered_cash_corrected')."""
    return float(industry_row(df, industry)[pick_column(df, family, logical, data_dir)])


def load_risk_premiums(ds: DatasetRow, data_dir=None) -> dict:
    d = Path(data_dir) if data_dir else DATA_DIR
    text = mdtables.read(ds.abspath(d))
    tabs = mdtables.parse_tables(text)
    out = {"meta": mdtables.extract_meta(text)}
    inp = next(t for t in tabs if t.header[0] == "Parameter")
    params = {}
    for r in inp.rows:
        v = mdtables.to_number(r[1])
        params[r[0]] = {"value": (v[0] if v else r[1]), "text": r[1], "details": r[2]}
    out["inputs"] = params
    rated = next(t for t in tabs if t.header[0] == "Country" and "Region" in t.header)
    frontier = next(t for t in tabs if t.header[0] == "Country" and "PRS Composite Risk Score" in t.header)
    lookup = next(t for t in tabs if t.header[0] == "Moody's Rating")
    out["rated"], out["frontier"], out["rating_spreads"] = (mdtables.to_frame(rated)[0], mdtables.to_frame(frontier)[0],
                                                             mdtables.to_frame(lookup)[0])
    return out


def mature_erp(rp: dict) -> float:
    for k, v in rp["inputs"].items():
        if "mature" in k.lower() and "risk premium" in k.lower():
            return float(v["value"])
    raise KeyError("mature ERP row not found in the inputs table")


def country_risk(rp: dict, country: str, data_dir=None) -> dict:
    """Rating, rating-based default spread, equity CRP and total ERP for a country (decimals), with its source table.
    Use CRP for Ke, the default spread for Rf and Kd, never one for the other (dcf_procedure.md sections 7-8)."""
    ci = country_info(country, data_dir)
    name = ci["country"]
    rated = rp["rated"]
    hit = rated[rated["Country"] == name]
    if len(hit):
        r = hit.iloc[0]
        g = lambda logical: r[pick_column(rated, "ctryprem", logical, data_dir)]
        return {"country": name, "table": "rated", "rating": g("rating"), "default_spread": float(g("default_spread")),
                "crp": float(g("crp")), "total_erp": float(g("total_erp")), "region": g("region"), "warnings": ci["warnings"]}
    fr = rp["frontier"]
    hit = fr[fr["Country"] == name]
    if len(hit):
        r = hit.iloc[0]
        return {"country": name, "table": "frontier", "rating": None, "default_spread": float(r["Default Spread"]), "crp": float(r["CRP"]),
                "total_erp": float(r["ERP"]), "region": None,
                "warnings": ci["warnings"] + ["frontier market: spreads estimated from the PRS score, no sovereign rating"]}
    raise KeyError(f"{name} is in regions.csv but not in the risk-premium tables")


def load_regressions(ds: DatasetRow, data_dir=None) -> dict:
    d = Path(data_dir) if data_dir else DATA_DIR
    return pr.load(ds.abspath(d))


def find_equation(reg: dict, dependent: str, region_code: str):
    for e in reg["by_multiple"]:
        if e.dependent == dependent and e.region == region_code:
            return e
    return None


def equation_for(country: str, dependent: str, valuation_date=None, data_dir=None):
    """Resolve the published equation for a country: regressions dataset + the region inside it (exact, else fallback chain).
    Returns (Equation | None, Resolution, dict(region_used, level))."""
    res = resolve("regressions", country=country, valuation_date=valuation_date, data_dir=data_dir)
    if not res.found:
        return None, res, {}
    reg = load_regressions(res.dataset, data_dir)
    chain = country_info(country, data_dir)["chain"]
    for i, region in enumerate(chain):
        eq = find_equation(reg, dependent, region)
        if eq is not None:
            level = "exact" if i == 0 else "fallback"
            if level == "fallback":
                res.warnings.append(f"no published {dependent} equation for {chain[0]}; using {region}")
            return eq, res, {"region_used": region, "level": level}
    return None, res, {}


# ----------------------------------------------------------------------------- integrity checks
@dataclass
class Finding:
    severity: str   # error | warn | info
    code: str
    message: str


def check_dataset(ds: DatasetRow, data_dir=None) -> list[Finding]:
    """Verify a registered dataset against itself. Errors = unusable; warnings = verify against Damodaran's original before use."""
    d = Path(data_dir) if data_dir else DATA_DIR
    f: list[Finding] = []
    p = ds.abspath(d)
    if not p.exists():
        return [Finding("error", "missing_file", f"{ds.path} does not exist")]
    if hashlib.sha256(p.read_bytes()).hexdigest() != ds.sha256:
        f.append(Finding("error", "sha_mismatch", "file changed since registration (sha256 differs); re-register as a new vintage"))
    try:
        if ds.family in ("beta", "capex"):
            f += _check_industry(ds, d)
        elif ds.family == "ctryprem":
            f += _check_ctryprem(ds, d)
        elif ds.family == "regressions":
            f += _check_regressions(ds, d)
    except Exception as e:  # a parse failure is itself the finding
        f.append(Finding("error", "parse_failed", f"{type(e).__name__}: {e}"))
    return f


def _check_industry(ds, d):
    f = []
    df = load_industry(ds, d)
    names = df["Industry Name"]
    if names.duplicated().any():
        f.append(Finding("error", "duplicate_industries", f"duplicates: {names[names.duplicated()].tolist()}"))
    if not df["is_aggregate"].any():
        f.append(Finding("warn", "no_total_row", "no 'Grand Total' / 'Total Market' row found"))
    for logical in column_map(ds.family, d):
        try:
            col = pick_column(df, ds.family, logical, d)
        except KeyError as e:
            f.append(Finding("warn", "column_not_found", str(e)[:200]))
            continue
        if df.attrs["units"].get(col) == "text":
            f.append(Finding("warn", "column_not_numeric", f"{logical} -> '{col}' did not parse as numeric"))
    if ds.family == "beta":
        t = df.attrs.get("marginal_tax_rate_used")
        if t is None:
            f.append(Finding("warn", "no_marginal_tax", "'Marginal Tax Rate Used' not found: unlevering check skipped"))
        else:
            b, de, u = (pick_column(df, "beta", k, d) for k in ("beta_levered", "de_ratio", "beta_unlevered"))
            cash, uc = pick_column(df, "beta", "cash_firm_value", d), pick_column(df, "beta", "beta_unlevered_cash_corrected", d)
            body = df[~df["is_aggregate"]].dropna(subset=[b, de, u, cash, uc])
            u_calc = body[b] / (1 + (1 - t) * body[de])
            bad_u = body.loc[(u_calc - body[u]).abs() > 0.03, "Industry Name"].tolist()
            uc_calc = body[u] / (1 - body[cash])
            bad_c = body.loc[(uc_calc - body[uc]).abs() > 0.03, "Industry Name"].tolist()
            f.append(Finding("info" if not bad_u else "warn", "unlevering_consistency",
                             f"unlevered beta = beta/(1+(1-{t:.4f})*D/E) within 0.03 for {len(body) - len(bad_u)}/{len(body)} industries; outliers: {bad_u}"))
            f.append(Finding("info" if not bad_c else "warn", "cash_correction_consistency",
                             f"cash-corrected = unlevered/(1-cash/firm value) within 0.03 for {len(body) - len(bad_c)}/{len(body)}; outliers: {bad_c}"))
    if ds.family == "capex":
        c = pick_column(df, "capex", "net_capex_to_ebit_1mt", d)
        ext = df.loc[(df[c].abs() > 5) & ~df["is_aggregate"], ["Industry Name", c]]
        if len(ext):
            f.append(Finding("warn", "net_capex_ebit_extreme", "Net CapEx/EBIT(1-t) beyond +/-500% is not meaningful for: " +
                             "; ".join(f"{n} ({v:.0%})" for n, v in ext.itertuples(index=False)) +
                             ". dcf_procedure.md section 3: distorted denominators, use another supported ratio and say so."))
    return f


def _check_ctryprem(ds, d):
    f = []
    rp = load_risk_premiums(ds, d)
    rated, lookup = rp["rated"], rp["rating_spreads"]
    mat = mature_erp(rp)
    mult = next((v["value"] for k, v in rp["inputs"].items() if "multiplier" in k.lower()), None)
    sp = {r["Moody's Rating"]: r["Default Spread (%)"] for _, r in lookup.iterrows()}
    ds_col, crp_col, erp_col = (pick_column(rated, "ctryprem", k, d) for k in ("default_spread", "crp", "total_erp"))
    rat_col = pick_column(rated, "ctryprem", "rating", d)
    bad_lookup = rated.loc[[abs(r[ds_col] - sp.get(r[rat_col], math.nan)) > 1e-6 for _, r in rated.iterrows()], "Country"].tolist()
    f.append(Finding("error" if bad_lookup else "info", "default_spread_vs_rating_lookup",
                     f"every rated country's default spread equals the rating lookup table: {not bad_lookup}; mismatches: {bad_lookup}"))
    bad_erp = rated.loc[(rated[erp_col] - (mat + rated[crp_col])).abs() > 0.0002, "Country"].tolist()
    f.append(Finding("warn" if bad_erp else "info", "total_erp_equals_mature_plus_crp", f"total ERP = mature ERP ({mat:.2%}) + CRP within 0.02pp; mismatches: {bad_erp}"))
    pos = rated[(rated[ds_col] > 0) & (rated["Country"] != "United States")]
    med = float((pos[crp_col] / pos[ds_col]).median())
    off = pos.loc[(pos[crp_col] - pos[ds_col] * med).abs() > 0.0002, "Country"].tolist()
    f.append(Finding("warn" if off else "info", "crp_equals_spread_times_multiplier",
                     f"CRP = default spread x {med:.3f} (stated multiplier {mult}, rounded) within 0.02pp for {len(pos) - len(off)}/{len(pos)} countries; "
                     f"outliers: {off}. The US row is computed differently in the source (CRP = default spread)."))
    dup = rated["Country"][rated["Country"].duplicated()].tolist()
    if dup:
        f.append(Finding("error", "duplicate_countries", str(dup)))
    return f


def _check_regressions(ds, d):
    f = []
    reg = load_regressions(ds, d)
    A = {e.key(): e for e in reg["by_multiple"]}
    B = {e.key(): e for e in reg["by_region"]}
    f.append(Finding("info", "equation_counts", f"{len(A)} equations in the by-multiple view, {len(B)} in the by-region view"))
    only_a = sorted(set(A) - set(B))
    if only_a:
        f.append(Finding("info", "regions_only_in_one_view", f"in the by-multiple view only: {sorted({k[1] for k in only_a})} (the file's intro lists five groupings)"))
    mism = []
    for k in set(A) & set(B):
        a, b = A[k], B[k]
        sa = (a.constant, a.constant_tstat, a.r2, [(t.variable, t.coef, t.tstat, t.transform) for t in a.terms])
        sb = (b.constant, b.constant_tstat, b.r2, [(t.variable, t.coef, t.tstat, t.transform) for t in b.terms])
        if sa != sb:
            mism.append(k)
    f.append(Finding("error" if mism else "info", "views_agree", f"the two printed views agree for {len(set(A) & set(B)) - len(mism)}/{len(set(A) & set(B))} equations; mismatches: {mism}"))
    for e in A.values():
        if not 0 <= e.r2 <= 1:
            f.append(Finding("error", "r2_range", f"{e.key()} R2={e.r2}"))
        ts = [round(t.tstat, 2) for t in e.terms]
        dups = {x for x in ts if ts.count(x) > 1}
        if dups:
            f.append(Finding("warn", "identical_tstats", f"{e.key()}: identical t-stats {sorted(dups)} on different terms (possible transcription error in the source)"))
    # a coefficient whose sign is opposite to every other region and is itself significant
    by_var: dict[tuple, list] = {}
    for e in A.values():
        for t in e.terms:
            by_var.setdefault((e.dependent, t.variable, t.transform), []).append((e.region, t.coef, t.tstat))
    for (dep, var, tr), lst in by_var.items():
        if len(lst) < 4:
            continue
        for reg_, c, ts_ in lst:
            others = [x[1] for x in lst if x[0] != reg_]
            if abs(ts_) >= 2 and all(o * c < 0 for o in others if o != 0) and sum(1 for o in others if o != 0) >= 3:
                f.append(Finding("warn", "sign_differs_from_all_other_regions",
                                 f"{dep} / {tr + '(' if tr else ''}{var}{')' if tr else ''} in {reg_}: coefficient {c:+.3g} (t={ts_:.1f}) has the opposite sign of all other regions; verify against Damodaran's original before use"))
    r2s: dict = {}
    for e in A.values():
        r2s.setdefault((e.dependent, round(e.r2, 3)), []).append(e.region)
    for (dep, r2), regs in r2s.items():
        if len(regs) > 1:
            f.append(Finding("info", "identical_r2_across_regions", f"{dep}: R2 {r2:.1%} appears for {regs}"))
    f.append(Finding("warn", "units_dfr_tax_unresolved",
                     "DFR and Tax rate coefficients (e.g. -0.11, -0.12, t-stats 5-90) look like percentage points, while the file says decimals. "
                     "predict() requires an explicit unit policy; resolve with Damodaran's variable page and a sector-median plausibility check."))
    f.append(Finding("info", "no_residual_se", "the file publishes coefficients, t-stats and R2 only: no n, SEy or p-values, so residual-band classification and D1-D10 diagnostics are not available"))
    return f


# ----------------------------------------------------------------------------- add / CLI
def _plain_url(s: str) -> str:
    m = re.search(r"\]\((https?://[^)]+)\)", s) or re.search(r"<(https?://[^>]+)>", s) or re.search(r"(https?://\S+)", s)
    return m.group(1) if m else ""


def _detect(meta: dict):
    title = meta["title"]
    for pat, fam, g in TITLE_PATTERNS:
        m = re.search(pat, title)
        if m:
            label = m.group(g).strip() if g else None
            return fam, label
    return None, None


def add_dataset(src: str | Path, family: str | None = None, region: str | None = None, vintage: str | None = None,
                applies_to: str = "all", notes: str = "", data_dir=None, replace: bool = False) -> tuple[DatasetRow, list[Finding]]:
    """Copy a Markdown dataset into data/damodaran/<vintage>/, register it, run the integrity checks, return (row, findings).
    Family/region/vintage are detected from the file's title and dates; pass them explicitly if detection fails."""
    d = Path(data_dir) if data_dir else DATA_DIR
    src = Path(src)
    text = mdtables.read(src)
    meta = mdtables.extract_meta(text)
    fam, label = _detect(meta)
    family = family or fam
    if not family:
        raise ValueError(f"cannot detect the family from title '{meta['title']}'. Pass family=... (known: {sorted(FAMILIES)})")
    if family == "ctryprem":
        region_code, inside = "GLOBAL", "ALL"
    else:
        lab = _norm(region or label or "")
        region_code = REGION_LABELS.get(lab)
        if region_code is None:
            raise ValueError(f"cannot map region label '{region or label}' to a region code. Pass region=... (US, EUROPE, JAPAN, ANZCA, EM, GLOBAL, INDIA, CHINA ...)")
        inside = region_code
    as_of = meta["as_of_date"]
    if not as_of:
        raise ValueError("no date found in the file header; add a '**Date updated:** ...' line or pass vintage")
    vint = vintage or as_of[:7]
    sha = hashlib.sha256(src.read_bytes()).hexdigest()
    rows = registry(d)
    for r in rows:
        if r.sha256 == sha:
            raise ValueError(f"already registered as {r.dataset_id}")
    slug = "multi" if region_code == "MULTI" else region_code.lower()
    ds_id = f"{family}_{slug}_{vint}"
    if any(r.dataset_id == ds_id for r in rows) and not replace:
        raise ValueError(f"{ds_id} already exists with different content: pass a new vintage or replace=True (keeps a record in notes)")
    rel = f"damodaran/{vint}/{family}_{slug}.md"
    dest = d / rel
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(src, dest)
    row = DatasetRow(ds_id, family, region_code, inside, vint, as_of, meta["title"], _plain_url(meta["fields"].get("Data Website", "")), rel, sha, src.name,
                     date.today().isoformat(), applies_to, "registered", notes)
    if family == "regressions":
        regs = sorted({e.region for e in pr.load(dest)["by_multiple"]})
        row.region_code, row.regions_inside = "MULTI", "|".join(regs)
    rows = [r for r in rows if r.dataset_id != ds_id] + [row]
    _write_registry(rows, d)
    findings = check_dataset(row, d)
    row.status = "has_errors" if any(x.severity == "error" for x in findings) else "parsed_ok"
    _write_registry([r if r.dataset_id != ds_id else row for r in rows], d)
    return row, findings


def main(argv=None):
    a = list(sys.argv[1:] if argv is None else argv)
    if not a:
        print(__doc__)
        return 0
    cmd, rest = a[0], a[1:]
    opt = lambda k: rest[rest.index(k) + 1] if k in rest else None
    if cmd == "list":
        for r in registry():
            print(f"{r.dataset_id:34} {r.family:12} {r.region_code:7} inside={r.regions_inside:34} as_of={r.as_of_date} status={r.status}")
    elif cmd == "resolve":
        res = resolve(rest[0], country=opt("--country"), region=opt("--region"), valuation_date=opt("--date"))
        print(res.summary())
        for t in res.tried:
            print("  -", t)
    elif cmd == "add":
        row, findings = add_dataset(rest[0], family=opt("--family"), region=opt("--region"), vintage=opt("--vintage"))
        print("registered", row.dataset_id, row.status)
        for x in findings:
            print(f"  [{x.severity}] {x.code}: {x.message}")
    elif cmd == "check":
        for r in registry():
            if len(rest) and rest[0] != r.dataset_id:
                continue
            print(r.dataset_id)
            for x in check_dataset(r):
                print(f"  [{x.severity}] {x.code}: {x.message}")
    elif cmd == "columns":
        r = next(x for x in registry() if x.dataset_id == rest[0])
        if r.family in ("beta", "capex"):
            print(list(load_industry(r).columns))
        else:
            print("see the file's tables:", [t.header for t in mdtables.parse_tables(mdtables.read(r.abspath(DATA_DIR)))])
    else:
        print("unknown command")
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
