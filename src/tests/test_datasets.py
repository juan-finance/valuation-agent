import math
import shutil
from pathlib import Path

import pytest

from valuation_agent import datasets as D, mdtables as M, published_regressions as PR

ROOT = Path(__file__).resolve().parents[2] / "data"


def ds(family, **kw):
    r = D.resolve(family, **kw)
    assert r.found, r.message
    return r.dataset


# ------------------------------------------------------------------ markdown parsing
def test_number_and_date_parsing():
    assert M.to_number("33.09%") == (pytest.approx(0.3309), "pct")
    assert M.to_number("$1,252.30") == (pytest.approx(1252.30), "usd")
    assert M.to_number("-$3.70")[0] == pytest.approx(-3.70)
    assert M.to_number("-14594.97%")[0] == pytest.approx(-145.9497)
    assert math.isnan(M.to_number("NA")[0]) and M.to_number("Aa3") is None
    assert M.parse_date("5-ene-26") == ["2026-01-05"] and M.parse_date("1-Jul-26") == ["2026-07-01"]
    assert "2026-07-09" in M.parse_date("corrected on July 9, 2026") and M.parse_date("January 2026") == ["2026-01-01"]


def test_registered_files_match_registry_and_parse():
    rows = D.registry()
    assert {r.family for r in rows} >= {"beta", "capex", "ctryprem", "regressions"}
    for r in rows:
        assert r.abspath(ROOT).exists() and r.status == "parsed_ok"
        assert [f for f in D.check_dataset(r) if f.severity == "error"] == []


# ------------------------------------------------------------------ industry files (values read from the real files)
def test_beta_values_and_internal_consistency():
    b = D.load_industry(ds("beta", country="Spain"))
    assert len(b[~b["is_aggregate"]]) == 94 and b.attrs["marginal_tax_rate_used"] == pytest.approx(0.2471)
    assert D.get_value(b, "beta", "Power", "beta_unlevered_cash_corrected") == pytest.approx(0.45)
    assert D.get_value(b, "beta", "Utility (General)", "beta_unlevered_cash_corrected") == pytest.approx(0.41)
    assert D.get_value(b, "beta", "Green & Renewable Energy", "beta_unlevered_cash_corrected") == pytest.approx(0.46)
    assert D.get_value(b, "beta", "Steel", "de_ratio") == pytest.approx(0.4097)
    t = b.attrs["marginal_tax_rate_used"]
    p = D.industry_row(b, "Power")
    assert p["Beta"] / (1 + (1 - t) * p["D/E Ratio"]) == pytest.approx(p["Unlevered beta"], abs=0.01)
    msgs = [f.message for f in D.check_dataset(ds("beta", country="Spain"))]
    assert any("94/94" in m for m in msgs)


def test_capex_values_and_nonmeaningful_flags():
    c = D.load_industry(ds("capex", country="Italy"))
    assert D.get_value(c, "capex", "Power", "net_capex_to_ebit_1mt") == pytest.approx(0.6629)
    assert D.get_value(c, "capex", "Steel", "net_capex_to_ebit_1mt") == pytest.approx(8.8356)
    assert D.get_value(c, "capex", "Electrical Equipment", "sales_to_invested_capital") == pytest.approx(3.70)
    import numpy as np
    assert np.isnan(D.get_value(c, "capex", "Bank (Money Center)", "net_capex_to_ebit_1mt"))      # 'NA' cell
    warn = [f for f in D.check_dataset(ds("capex", country="Italy")) if f.code == "net_capex_ebit_extreme"]
    assert warn and "Steel" in warn[0].message and "Railroads" in warn[0].message


def test_industry_lookup_is_exact_or_raises_with_suggestions():
    b = D.load_industry(ds("beta", country="Spain"))
    assert D.industry_row(b, "power")["Industry Name"] == "Power"
    with pytest.raises(KeyError, match="Closest"):
        D.industry_row(b, "Electric Utilities")
    with pytest.raises(KeyError):
        D.pick_column(b, "beta", "no_such_logical")


# ------------------------------------------------------------------ risk premiums
def test_country_risk_values():
    rp = D.load_risk_premiums(ds("ctryprem", country="Italy"))
    assert D.mature_erp(rp) == pytest.approx(0.042)
    it = D.country_risk(rp, "Italy")
    assert (it["rating"], it["default_spread"], it["crp"], it["total_erp"]) == ("Baa2", pytest.approx(0.0152), pytest.approx(0.0236), pytest.approx(0.0656))
    assert D.country_risk(rp, "Germany")["crp"] == 0 and D.country_risk(rp, "UK")["rating"] == "Aa3"      # alias
    assert D.country_risk(rp, "PT")["rating"] == "A3"                                                     # ISO2 alias
    fr = D.country_risk(rp, "Russia")
    assert fr["table"] == "frontier" and fr["crp"] == pytest.approx(0.0372) and any("frontier" in w for w in fr["warnings"])
    with pytest.raises(KeyError, match="Close matches"):
        D.country_risk(rp, "Portugall")


def test_risk_premium_integrity_findings_are_clean():
    f = {x.code: x for x in D.check_dataset(ds("ctryprem", country="Spain"))}
    assert "True" in f["default_spread_vs_rating_lookup"].message and f["default_spread_vs_rating_lookup"].severity == "info"
    assert f["total_erp_equals_mature_plus_crp"].severity == "info"
    assert f["crp_equals_spread_times_multiplier"].severity == "info"


# ------------------------------------------------------------------ resolver
UNIVERSE = ["Portugal", "Denmark", "Spain", "Italy", "United Kingdom", "France", "Austria", "Germany", "Sweden", "Finland", "Netherlands",
            "Norway", "Luxembourg", "Switzerland"]


@pytest.mark.parametrize("country", UNIVERSE)
def test_every_universe_country_resolves_to_europe_for_all_families(country):
    for fam in ("beta", "capex", "regressions"):
        r = D.resolve(fam, country=country, valuation_date="2026-10-30")
        assert r.found and r.match_level == "exact" and r.region_used == "EUROPE", (fam, r.summary())
    assert D.resolve("ctryprem", country=country, valuation_date="2026-10-30").dataset.dataset_id == "ctryprem_global_2026-07"


def test_missing_region_gives_actionable_message_not_a_wrong_dataset():
    r = D.resolve("beta", country="Brazil")
    assert not r.found and "datasets add" in r.message and r.requested_chain == ["EM", "GLOBAL"]
    assert not D.resolve("capex", country="Japan").found


def test_lookahead_is_excluded_and_vintage_can_be_pinned():
    r = D.resolve("ctryprem", country="Spain", valuation_date="2026-06-30")
    assert not r.found and any("look-ahead" in t for t in r.tried)
    assert D.resolve("ctryprem", country="Spain", valuation_date="2026-07-09").found
    assert not D.resolve("beta", country="Spain", vintage="2025-01").found
    assert D.resolve("beta", country="Spain", vintage="2026-01").found


def test_unknown_country_and_low_confidence_warnings():
    with pytest.raises(KeyError, match="Close matches"):
        D.resolve("beta", country="Narnia")
    assert any("confidence" in w for w in D.resolve("beta", country="Turkey").warnings)
    assert D.country_info("Canada")["chain"][0] == "ANZCA" and D.country_info("India")["chain"][:2] == ["INDIA", "EM"]
    assert D.country_info("Saudi Arabia")["region_code"] == "GLOBAL" and D.country_info("Brazil")["region_code"] == "EM"


def test_resolve_for_company_lists_material_foreign_revenue():
    out = D.resolve_for_company("beta", "Spain", {"Spain": 0.5, "United Kingdom": 0.3, "Brazil": 0.2})
    assert out["primary"].found and set(out["others"]) == {"United Kingdom"} and "global" in out["note"].lower()


# ------------------------------------------------------------------ extensibility: other regions without code changes
@pytest.fixture()
def lib(tmp_path):
    for n in ("regions.csv", "region_fallbacks.csv", "country_aliases.csv", "column_maps.csv"):
        shutil.copy(ROOT / n, tmp_path / n)
    shutil.copytree(ROOT / "damodaran", tmp_path / "damodaran")
    shutil.copy(ROOT / "registry.csv", tmp_path / "registry.csv")
    return tmp_path


def _variant(tmp_path, name, title, region_label, date="5-Jan-26", base="beta_europe.md", src_lib=None):
    text = (ROOT / "damodaran/2026-01" / base).read_text(encoding="utf-8")
    first = text.splitlines()[0]
    text = text.replace(first, f"# {title}: {region_label}", 1)
    import re
    text = re.sub(r"\*\*Date updated:\*\* [^\n]*", f"**Date updated:** {date}", text)
    p = tmp_path / name
    p.write_text(text + "\n<!-- variant -->\n", encoding="utf-8")
    return p


def test_adding_a_us_and_a_newer_europe_dataset_changes_resolution_without_code(lib, tmp_path):
    us = _variant(tmp_path, "beta-us.md", "Betas and Risk Measures by Industry", "US")
    row, findings = D.add_dataset(us, data_dir=lib)
    assert row.dataset_id == "beta_us_2026-01" and row.status == "parsed_ok"
    assert D.resolve("beta", country="United States", data_dir=lib).dataset.region_code == "US"
    assert D.resolve("beta", country="Spain", data_dir=lib).dataset.region_code == "EUROPE"
    new_eu = _variant(tmp_path, "beta-eu27.md", "Betas and Risk Measures by Industry", "Western Europe", date="4-Jan-27")
    D.add_dataset(new_eu, data_dir=lib)
    assert D.resolve("beta", country="Spain", data_dir=lib).dataset.vintage == "2027-01"                      # newest wins
    assert D.resolve("beta", country="Spain", valuation_date="2026-10-30", data_dir=lib).dataset.vintage == "2026-01"   # unless look-ahead


def test_dedicated_india_dataset_beats_emerging_markets(lib, tmp_path):
    assert not D.resolve("beta", country="India", data_dir=lib).found
    em = _variant(tmp_path, "beta-em.md", "Betas and Risk Measures by Industry", "Emerging Markets")
    D.add_dataset(em, data_dir=lib)
    assert D.resolve("beta", country="India", data_dir=lib).region_used == "EM"
    ind = _variant(tmp_path, "beta-in.md", "Betas and Risk Measures by Industry", "India", date="6-Jan-26")
    D.add_dataset(ind, data_dir=lib)
    assert D.resolve("beta", country="India", data_dir=lib).region_used == "INDIA"
    assert D.resolve("beta", country="Brazil", data_dir=lib).region_used == "EM"


def test_fallback_to_global_is_flagged(lib, tmp_path):
    g = _variant(tmp_path, "beta-global.md", "Betas and Risk Measures by Industry", "Global")
    D.add_dataset(g, data_dir=lib)
    r = D.resolve("beta", country="Brazil", data_dir=lib)
    assert r.found and r.match_level == "fallback" and r.region_used == "GLOBAL" and any("representative" in w for w in r.warnings)


def test_add_rejects_duplicates_undetectable_titles_and_wrong_regions(lib, tmp_path):
    with pytest.raises(ValueError, match="already registered"):
        D.add_dataset(ROOT / "damodaran/2026-01/beta_europe.md", data_dir=lib)
    odd = tmp_path / "odd.md"; odd.write_text("# Something Else\n\n**Date updated:** 5-Jan-26\n")
    with pytest.raises(ValueError, match="cannot detect the family"):
        D.add_dataset(odd, data_dir=lib)
    bad = _variant(tmp_path, "bad.md", "Betas and Risk Measures by Industry", "Atlantis")
    with pytest.raises(ValueError, match="cannot map region"):
        D.add_dataset(bad, data_dir=lib)
    ok = D.add_dataset(bad, region="GLOBAL", data_dir=lib)[0]
    assert ok.region_code == "GLOBAL"
    nodate = tmp_path / "nd.md"; nodate.write_text("# Betas and Risk Measures by Industry: US\n")
    with pytest.raises(ValueError, match="no date"):
        D.add_dataset(nodate, data_dir=lib)


def test_changed_file_is_detected(lib):
    p = lib / "damodaran/2026-01/capex_europe.md"
    p.write_text(p.read_text(encoding="utf-8") + "\nedited\n", encoding="utf-8")
    row = next(r for r in D.registry(lib) if r.family == "capex")
    assert any(f.code == "sha_mismatch" for f in D.check_dataset(row, lib))


def test_column_header_rename_is_a_visible_stop(lib):
    b = D.load_industry(next(r for r in D.registry(lib) if r.family == "beta"), lib)
    b2 = b.rename(columns={"Unlevered beta corrected for cash": "Unlevered beta (cash adj.)"})
    with pytest.raises(KeyError, match="none of"):
        D.pick_column(b2, "beta", "beta_unlevered_cash_corrected", lib)
