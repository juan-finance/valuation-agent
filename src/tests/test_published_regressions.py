import math
from pathlib import Path

import pytest

from valuation_agent import datasets as D, published_regressions as PR

REG = D.load_regressions(D.resolve("regressions", country="Spain").dataset)
A = {e.key(): e for e in REG["by_multiple"]}


def test_counts_regions_and_r2():
    assert len(A) == 36 and {k[1] for k in A} == {"US", "EUROPE", "JAPAN", "EM", "GLOBAL", "ANZCA"}
    assert {k[0] for k in A} == {"PE", "PEG", "PBV", "EV/IC", "EV/Sales", "EV/EBITDA"}
    assert A[("PE", "EUROPE")].r2 == pytest.approx(0.201) and A[("EV/Sales", "EUROPE")].r2 == pytest.approx(0.142)


def test_europe_equations_parsed_exactly_as_printed():
    pe = A[("PE", "EUROPE")]
    assert (pe.constant, pe.constant_tstat) == (9.72, 8.29)
    assert [(t.variable, t.coef, t.tstat) for t in pe.terms] == [("beta", 2.99, 4.85), ("g_eps", 49.82, 11.95), ("payout", 7.98, 9.22)]
    pbv = A[("PBV", "EUROPE")]
    assert [(t.variable, t.coef) for t in pbv.terms] == [("g_eps", 3.92), ("beta", 0.13), ("roe", 10.75), ("payout", -0.25)]
    ev = A[("EV/EBITDA", "EUROPE")]
    assert (ev.constant, [(t.variable, t.coef) for t in ev.terms]) == (18.15, [("g_rev", 35.25), ("dfr", -0.11), ("tax_rate", -0.12), ("roic", 2.29)])
    peg = A[("PEG", "EUROPE")]
    assert peg.constant == -0.91 and [(t.variable, t.coef, t.transform) for t in peg.terms] == [("payout", 0.76, ""), ("g_eps", -1.57, "ln")]


def test_negative_constants_notes_and_signs():
    assert A[("PEG", "US")].constant == -0.60 and A[("PBV", "US")].constant == -0.79
    us = A[("PBV", "US")]
    assert [(t.variable, t.coef) for t in us.terms] == [("g_eps", -0.47), ("beta", 1.49), ("roe", 20.90), ("payout", 0.17)]
    assert A[("PE", "ANZCA")].note == "no other variables significant" and len(A[("PE", "ANZCA")].terms) == 1
    assert [t.coef for t in A[("EV/EBITDA", "EM")].terms][-1] == -4.88


def test_both_printed_views_identical():
    B = {e.key(): e for e in REG["by_region"]}
    assert len(B) == 30 and set(B) < set(A)
    for k, b in B.items():
        a = A[k]
        assert (a.constant, a.constant_tstat, a.r2) == (b.constant, b.constant_tstat, b.r2)
        assert [(t.variable, t.coef, t.tstat, t.transform) for t in a.terms] == [(t.variable, t.coef, t.tstat, t.transform) for t in b.terms]


def test_predict_pe_and_pbv_by_hand():
    pe = A[("PE", "EUROPE")]
    x = {"beta": 0.8, "g_eps": 0.06, "payout": 0.5}
    assert PR.predict(pe, x, "as_published_note") == pytest.approx(9.72 + 2.99 * 0.8 + 49.82 * 0.06 + 7.98 * 0.5)
    pbv = A[("PBV", "EUROPE")]
    y = {"g_eps": 0.05, "beta": 0.7, "roe": 0.10, "payout": 0.6}
    assert PR.predict(pbv, y, "as_published_note") == pytest.approx(0.73 + 3.92 * 0.05 + 0.13 * 0.7 + 10.75 * 0.10 - 0.25 * 0.6)


def test_unit_policy_is_mandatory_and_changes_dfr_tax_terms():
    ev = A[("EV/EBITDA", "EUROPE")]
    x = {"g_rev": 0.05, "dfr": 0.30, "tax_rate": 0.20, "roic": 0.08}
    with pytest.raises(TypeError):
        PR.predict(ev, x)                                      # no default policy
    with pytest.raises(ValueError, match="unit policy"):
        PR.predict(ev, x, "whatever")
    dec = PR.predict(ev, x, "as_published_note")
    pct = PR.predict(ev, x, "dfr_tax_percent_points")
    assert dec == pytest.approx(18.15 + 35.25 * 0.05 - 0.11 * 0.30 - 0.12 * 0.20 + 2.29 * 0.08)
    assert pct == pytest.approx(18.15 + 35.25 * 0.05 - 0.11 * 30 - 0.12 * 20 + 2.29 * 0.08)
    both = PR.predict_both_policies(ev, x)
    assert both["uses_dfr_or_tax"] and both["max_abs_difference"] == pytest.approx(dec - pct) and both["max_abs_difference"] > 5
    pe = A[("PE", "EUROPE")]                                    # PE has no DFR/tax: policies agree
    z = PR.predict_both_policies(pe, {"beta": 1, "g_eps": 0.05, "payout": 0.4})
    assert not z["uses_dfr_or_tax"] and z["max_abs_difference"] == 0


def test_predict_refuses_missing_inputs_and_bad_logs():
    pe = A[("PE", "EUROPE")]
    with pytest.raises(ValueError, match="missing input 'payout'"):
        PR.predict(pe, {"beta": 1, "g_eps": 0.05}, "as_published_note")
    with pytest.raises(ValueError, match="missing input"):
        PR.predict(pe, {"beta": 1, "g_eps": float("nan"), "payout": 0.3}, "as_published_note")
    peg = A[("PEG", "EUROPE")]
    with pytest.raises(ValueError, match="ln"):
        PR.predict(peg, {"payout": 0.3, "g_eps": 0.0}, "as_published_note")
    v = PR.predict(peg, {"payout": 0.3, "g_eps": 0.10}, "as_published_note")
    assert v == pytest.approx(-0.91 + 0.76 * 0.3 - 1.57 * math.log(0.10))
    assert PR.peg_to_pe(v, 0.10) == pytest.approx(v * 10)


def test_the_example_in_the_file_is_not_the_2026_us_equation():
    """The file's Disney example (2022 numbers: 2.10 + 6.07g + 0.69beta + 5.09ROE - 0.33payout = 4.35) is stale; the printed 2026 US PBV
    equation gives a different value for the same inputs. Do not copy the example."""
    example = 2.10 + 6.07 * 0.12 + 0.69 * 1.10 + 5.09 * 0.162 - 0.33 * 0.20
    assert example == pytest.approx(4.35, abs=0.01)
    us2026 = PR.predict(A[("PBV", "US")], {"g_eps": 0.12, "beta": 1.10, "roe": 0.162, "payout": 0.20}, "as_published_note")
    assert abs(us2026 - example) > 0.1 and us2026 == pytest.approx(4.2124, abs=1e-3)      # 3% lower, coefficients differ


def test_equation_for_uses_region_chain_and_reports_fallback():
    eq, res, info = D.equation_for("Spain", "PE")
    assert eq.region == "EUROPE" and info == {"region_used": "EUROPE", "level": "exact"} and res.found
    eq, res, info = D.equation_for("Brazil", "PBV")
    assert eq.region == "EM" and info["level"] == "exact"
    eq, res, info = D.equation_for("Saudi Arabia", "EV/EBITDA")
    assert eq.region == "GLOBAL" and any("Global is the fallback" in w for w in res.warnings)      # no Middle East group: warned
    eq, res, info = D.equation_for("Brazil", "PBV")
    assert info["level"] == "exact"
    eq, res, info = D.equation_for("Canada", "PE")
    assert eq.region == "ANZCA"
    assert D.equation_for("Spain", "PS")[0] is None                 # no published price/sales equation
    assert PR.REPO_MULTIPLE == {"PE": "PE", "PBV": "PBV", "EV/EBITDA": "EVEBITDA"}


def test_integrity_findings_surface_the_known_source_anomalies():
    f = D.check_dataset(D.resolve("regressions", country="Spain").dataset)
    msgs = " | ".join(x.message for x in f)
    assert "PEG / ln(g_eps) in GLOBAL" in msgs and "identical t-stats [12.83]" in msgs
    assert "PBV / beta in GLOBAL" in msgs and "EV/EBITDA / roic in EM" in msgs
    codes = {x.code for x in f}
    assert {"units_dfr_tax_unresolved", "no_residual_se", "regions_only_in_one_view"} <= codes
