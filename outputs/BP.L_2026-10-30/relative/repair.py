"""Remediate failed BP checks without rerunning the original QA block.

Issuer observations supplement, never overwrite, immutable vendor inputs.
Unresolved perimeters are explicit rejection gates, not assumed zero claims.
"""
import json
import math
import re
import hashlib
import sys
from datetime import datetime, timezone
from pathlib import Path

import pandas as pd
from openpyxl import load_workbook
from valuation_agent import comparables as c, datasets
from valuation_agent.sourcelog import SourceLog

P = Path(__file__).resolve().parent
ROOT = P.parents[2]
STAMP = datetime.now(timezone.utc).isoformat(timespec="seconds")
D = pd.read_csv(P / "candidate_raw.csv").set_index("ticker", drop=False)
FX = json.loads((ROOT / "cache/macro/2026-10-30.json").read_text())["fx_ecb_reference"]["rates"]
FX["EUR"] = 1.0
J = json.loads((P / "regression_results.json").read_text())
E = next(x for x in J["predictions"] if x["model"] == "EV/EBITDA")
ORIGINAL = pd.read_csv(P / "numeric_prospects_NOT_QUALIFIED.csv").ticker.tolist()
SUBSTITUTES = ["SHEL", "GALP", "WDS", "AKRBP"]

# These are case-specific issuer findings, not a reusable eligibility whitelist.
REVIEWS = {
    "OXY": ("reject", "Upstream/midstream operator, Tier2; not an integrated pure-play. CrownRock closed August2024; OxyChem disposed January2026. No matching pro-forma denominator/claim bridge established. Berkshire preferred claim omitted from prior candidate EV.", "https://www.sec.gov/Archives/edgar/data/797468/000162828025036189/oxy-20250728.htm", "https://www.oxy.com/siteassets/documents/investors/2025-annual-report.pdf"),
    "HBR": ("reject", "Operating upstream company, Tier2, not passive holding. Wintershall Dea September2024 transaction transformed scale; first full enlarged year2025, not comparable to FY2024 growth. BASF39.6% is unrelated to BP, not itself a target cross-holding. LLOG February2026 further breaks quote/FY perimeter. Subordinated notes are not ordinary NCI.", "https://www.basf.com/global/en/media/news-releases/2024/09/p-24-273", "https://www.harbourenergy.com/media/a11hxbdn/harbour-energy-annual-report-accounts-2025_web.pdf"),
    "OMV": ("reject", "Integrated fuels/gas/chemicals operating group, Tier1, not passive holding. OBAG31.5% and ADNOC24.9% are unrelated controlling investors. Borealis disposal group and Borouge combination (announced2025, closed March2026) prevent matching current cap to unadjusted FY denominator. Hybrid capital1985 is separate from NCI.", "https://www.omv.com/en/investors/omv-on-the-capital-markets/more-insights/shareholder-structure", "https://www.omv.com/en/media/press-releases/2026/260331-omv-and-xrg-complete-transactions-to-create-borouge-international-boosting-global-chemicals-leadership"),
    "ENI": ("hold", "Integrated operating group, Tier1, not passive holding. Neptune2024 and satellite transactions require comparison-period bridge review. Eni-controlled Var Energi must not be selected alongside Eni. No BP >20% link identified in reviewed material; not certified as a complete bidirectional ownership test.", "https://www.eni.com/en-IT/governance/shareholding-structure.html", "https://report.eni.com/annual-report-2025/en/_assets/downloads/entire-eni-ar25.pdf"),
    "NESTE": ("hold", "Renewable/oil-products refiner, Tier2, not integrated upstream pure-play; business difference retained rather than falsely called Tier1. Finland44.22% is unrelated to BP. Issuer confirms zero NCI. Reported EBITDA1438 versus vendor1124 differs materially; no uniform operating/lease denominator bridge established.", "https://www.neste.com/investors/share-and-shareholders", "https://www.neste.com/files/pdf/7218DC4287D4BDD7-Neste%20Financial%20Statements%20Release%202025.pdf"),
    "CVX": ("reject", "Integrated operator, Tier1. Hess closed July2025: year-end claims and share count include all Hess but FY earnings only post-acquisition. No full-year matching pro forma supplied; cannot pass restructuring gate merely because vendor figures are numeric.", "https://www.chevron.com/newsroom/2025/q3/chevron-completes-acquisition-of-hess-corporation", "https://www.sec.gov/Archives/edgar/data/93410/000009341026000078/cvx-20251231.htm"),
    "EQNR": ("hold", "Operating upstream/gas group, Tier1. Norway67% is unrelated state ownership. Adura50/50 with Shell completed December2025; UK assets deconsolidated, equity-accounted investment8504. Requires FY operating contribution/associate adjustment; partnership is not 50% cross-ownership of Shell itself.", "https://www.equinor.com/investors/our-shareholders", "https://www.equinor.com/news/20251201-equinor-and-shell-complete-formation-of-adura"),
    "REP": ("hold", "Integrated operating group, Tier1, not passive holding; shareholder structure reviewed separately. Other equity instruments3046 are non-common claims, missing from old numeric EV. Financial liabilities include non-debt items; debt13246 must not be replaced by total liabilities13428. Associate and hybrid inverse unresolved.", "https://www.repsol.com/en/shareholders-and-investors/repsol-on-the-stock-exchange/shareholder-structure/index.cshtml", "https://www.repsol.com/content/dam/repsol-corporate/en_gb/accionistas-e-inversores/informes-anuales/2025/consolidated-annual-financial-report-2025.pdf"),
    "TTE": ("hold", "Integrated operator, Tier1. Annual report shareholder and business-combination schedules reviewed, but complete bidirectional BP holding exclusion not certified. Equity-classified perpetual notes are additional claims: prior EV does not establish their treatment. Debt61421 versus continuing balance61033 includes perimeter difference388; unresolved against denominator.", "https://totalenergies.com/system/files/documents/totalenergies_universal-registration-document-2025_2026_en.pdf", "https://totalenergies.com/investors/publications-and-regulated-information/regulated-information/annual-financial-reports"),
    "VLO": ("hold", "Operating refiner/renewable-diesel/ethanol manufacturer, Tier2, not integrated upstream pure-play. DGD is consolidated: NCI2880 retained once, not treated as excluded associate. Proxy beneficial-owner schedule is the ownership source, not a directory. Vendor debt11703 already includes1084 operating leases; do NOT add them twice. US GAAP operating rent still reduces EBITDA, unlike IFRS16; denominator not uniform.", "https://www.sec.gov/Archives/edgar/data/1035002/000162828026019806/vlo-20260318.htm", "https://www.sec.gov/Archives/edgar/data/1035002/000162828026011499/vlo-20251231.htm"),
    "SHEL": ("hold", "Integrated operating group, Tier1; BP bid denied June2025, not evidence of ownership or acquisition. AduraDecember2025 deconsolidation requires operating associate bridge. Vendor debt75688 versus continuing balance75643 differs45; no automatic zero adjustment. Not a certified substitute.", "https://www.shell.com/news-and-insights/newsroom/news-and-media-releases/2025/shell-plc-statement-re-bp-plc.html", "https://www.shell.com/news-and-insights/newsroom/news-and-media-releases/2025/shell-and-equinor-complete-formation-of-adura.html"),
    "GALP": ("hold", "Consolidated oil/gas/refining operator, Tier1; legal SGPS parent is NOT a passive holding exclusion. FY upstream RCA EBITDA1682/3039 exceeds50%; earnings are not exclusively upstream. Associates118 versus vendor missing; denominator contribution must be traced before deduction. Ownership/ISIN evidence carried from prior audit but not certified current bidirectional exclusion.", "https://www.galp.com/corp/Portals/0/Recursos/Investidores/IMR2025/ConsolidatedandIndividualFinancialStatements.pdf", "https://www.galp.com/corp/Portals/0/Recursos/Inv_4Q25/4Q25%20Report.pdf"),
    "WDS": ("hold", "Upstream/LNG operator, Tier2, not integrated refining pure-play. BHP petroleum merger2022 outside comparison window; Tellurian and ammonia acquisitions2024 and Louisiana LNG minority sell-down2025 require reconciliation. NCI3929 includes project minority funding; retain once. Not certified as a substitute.", "https://www.woodside.com/docs/default-source/investor-documents/major-reports-(static-pdfs)/2025-annual-report/annual-report-2025.pdf", "https://www.sec.gov/Archives/edgar/data/844551/000162828026010858/wds-20251231.htm"),
    "AKRBP": ("hold", "Upstream pure-play, Tier2. Issuer BP16%, Aker21%, Nemesia14%: BP holding below >20% gate; do not reject merely for name or association. Equity11226.2 is consolidated, not yet reconciled to vendor common-equity missing field. Leases included; complete metric/claim and ISIN checks still required.", "https://akerbp.com/wp-content/uploads/2026/03/akerbp-annual-report-2025.pdf", "https://akerbp.com/en/investor/reports-and-presentations/"),
}

# Sourced reconciliation components in reporting-currency millions. None means
# unresolved, never a presumed absent financing/nonoperating claim.
COMPONENTS = {
    "BP": (57958, 14571, 72529, 20948, 21, "issuer R5/R4; hybrid15955 already within NCI20948"),
    "OXY": (22396, 955, 23351, 564, 8287, "issuer balance debt1773+20623; operating leases350+605; preferred carrying8287"),
    "HBR": (5151, 634, 5785, None, 2025, "issuer borrowings4915+236; leases466+168; vendor NCI2025 is subordinated-notes investor equity, not ordinary NCI; vendor debt5790 differs5"),
    "OMV": (None, 1143, None, 6235, 1985, "issuer lease878+265; hybrid1985 separate; disposal-group debt mapping unresolved"),
    "ENI": (28502, 5700, 34202, 4847, None, "issuer short4929+current3434+long20139, leases1263+4437; other claims not certified absent"),
    "NESTE": (4443, 740, 5183, 0, None, "issuer interest-bearing4713+470 includes leases740; NCI explicitly0, not imputed"),
    "CVX": (39313, 7430, 46743, 5726, None, "issuer debt40758 includes finance leases1445; add operating5985 ONCE; debt excluding ALL leases39313"),
    "EQNR": (27810, 3411, 31221, 74, None, "issuer debt23763+4047, leases2221+1190"),
    "REP": (10352, 2894, 13246, 2478, 3046, "issuer leases2340+554; vendor debt reconciles financing debt+leases, other equity3046 carrying proxy"),
    "TTE": (None, None, 61033, 2640, None, "issuer continuing debt48995+12038; includes leases; vendor61421 differs388; perpetual equity claim unresolved"),
    "VLO": (None, None, 11703, 2880, None, "issuer949+9670 debt/finance leases +1084 operating leases =11703; finance lease detail in R56; rent/EBITDA harmonization unresolved"),
    "SHEL": (None, None, 75643, 927, None, "issuer66515+9128 incl leases; vendor75688 differs45; Adura associate contribution unresolved"),
    "GALP": (3682, 1217, 4899, 761, None, "issuer debt3075+607; leases1003+214; associate/JV118 not automatically deducted"),
    "WDS": (11963, 1759, 13722, 3929, None, "issuer debt782+11181, leases159+1600; NCI3929"),
    "AKRBP": (None, None, None, None, None, "issuer equity11226.2 and debt/lease notes sourced; exact current/noncurrent debt and NCI/common split not reconciled"),
}


def dump(name, value):
    (P / name).write_text(json.dumps(value, indent=2, default=str) + "\n")


def sheet(wb, name, data):
    if name in wb:
        del wb[name]
    ws = wb.create_sheet(name)
    ws.append(list(data.columns))
    for row in data.itertuples(index=False, name=None):
        ws.append([None if pd.isna(x) else x for x in row])
    ws.freeze_panes = "A2"
    ws.auto_filter.ref = ws.dimensions


def main():
    if (P / "qa_failed_item_recheck.md").exists():
        raise SystemExit("Repair already executed; reassess only after a new evidence change.")
    review = []
    for ticker, (decision, finding, owner, event) in REVIEWS.items():
        review.append(dict(ticker=ticker, role="original numeric prospect NOT selected" if ticker in ORIGINAL else "substitute investigated", decision=decision, pure_play_and_exclusion_finding=finding, qualified=False, ownership_source=owner, event_business_source=event, access_date=STAMP[:10], remaining_gate="uniform operating/associate/claim perimeter, bidirectional ownership/history/identity certification where unresolved"))
    Q = pd.DataFrame(review)
    Q.to_csv(P / "peer_qualification_repair.csv", index=False)
    bridges = []
    for ticker, (debt_ex, leases, debt, nci, other, explanation) in COMPONENTS.items():
        r = D.loc[ticker]
        equity_eur = r.price * r.current_shares_m / FX[r.quote_currency]
        rate = FX[r.report_currency]
        # One clearly labelled diagnostic only; unverified associates and claims
        # cannot enter the usable EV column or a fair-value conclusion.
        diagnostic_nci = r.NCI if nci is None else nci
        diagnostic = c.comparable_ev(equity_eur * rate, r.debt, diagnostic_nci, r.cash, 0)
        bridges.append(dict(ticker=ticker, financial_date="2025-12-31", financial_basis="FY2025", price_date="2026-10-30", fx_date="2026-10-30", comparison_currency="EUR", reporting_currency=r.report_currency, current_shares_m=r.current_shares_m, price_actual_quote=r.price, quote_currency=r.quote_currency, market_equity_eur_m=equity_eur, vendor_debt_report_m=r.debt, issuer_debt_ex_all_leases_report_m=debt_ex, issuer_leases_report_m=leases, issuer_debt_including_leases_report_m=debt, debt_reconciliation_difference=None if debt is None else r.debt-debt, cash_report_m=r.cash, issuer_NCI_report_m=nci, other_claim_carrying_proxy_report_m=other, associates_exclusion_report_m=None, usable_EV_eur_m=None, usable_inverse_equity_eur_m=None, diagnostic_EV_before_associates_other_claims_eur_m=diagnostic/rate, diagnostic_multiple_not_valuation=diagnostic/r.EBITDA, EBITDA_vendor_report_m=r.EBITDA, debt_eur_m=None if debt is None else debt/rate, cash_eur_m=r.cash/rate, NCI_eur_m=None if nci is None else nci/rate, uniform_status="NOT UNIFORM: no usable peer valuation", findings=explanation, source_urls=r.source_urls + " | " + (REVIEWS[ticker][3] if ticker in REVIEWS else "https://www.sec.gov/Archives/edgar/data/313807/000031380726000006/R5.htm"), access_date=STAMP[:10]))
    B = pd.DataFrame(bridges)
    B.to_csv(P / "uniform_bridge_repair.csv", index=False)
    diagnostic = B[B.ticker.isin(ORIGINAL)].diagnostic_multiple_not_valuation
    stats = c.multiple_stats(diagnostic, min_valid=6)
    # Diagnostic is deliberately NOT a qualified-peer median.
    market_usd = D.loc["BP", "price"] * D.loc["BP", "current_shares_m"] * FX["USD"] / FX["GBP"]
    T = D.loc["BP"]
    equity_usd = c.implied_equity_from_ev(E["predicted"], T.EBITDA, T.debt, T.NCI+21, T.cash, 0)
    per_share_usd = equity_usd/T.current_shares_m
    per_share_gbp = per_share_usd*FX["GBP"]/FX["USD"]
    assert math.isclose(per_share_gbp, E["value_per_share_gbp"], abs_tol=1e-9)
    assert math.isclose(T.raw_price/100, T.price, abs_tol=1e-12)
    unit = dict(status="PASS arithmetic only; estimate NOT USABLE", USD_per_EUR=FX["USD"], GBP_per_EUR=FX["GBP"], GBP_per_USD=FX["GBP"]/FX["USD"], raw_close_GBX=T.raw_price, close_GBP=T.price, current_ordinary_shares_m=T.current_shares_m, market_equity_usdm=market_usd, inverse_equity_usdm=equity_usd, mechanical_USD_per_ordinary=per_share_usd, mechanical_GBP_per_ordinary=per_share_gbp, ADS_ordinary_ratio=6, ADS_ratio_applied=False, double_pence_conversion=False, note="USD million / million current London ordinary shares = USD/ordinary; multiply GBP_per_EUR / USD_per_EUR. Neither divide by100 again nor multiply/divide by6. Historical arithmetic, withdrawn as valuation.")
    dump("currency_bridge_verification.json", unit)
    bench = datasets.resolve("evebitda_industry", country="United Kingdom", valuation_date="2026-10-30")
    assert bench.dataset is not None
    sector = datasets.industry_row(datasets.load_industry(bench.dataset), "Oil/Gas (Integrated)")
    sector_values = {str(k): str(v) for k, v in sector.items()}
    benchmark_value = float(sector["EV/EBITDA (Pos. EBITDA)"])
    plausibility = dict(status="NOT USABLE", qualified_peer_median=None, reason="No certified uniform peer panel; a numeric-prospect median cannot be promoted to a peer median.", original_numeric_prospect_diagnostic=stats, diagnostic_members=ORIGINAL, diagnostic_limit="Contains excluded companies, before associates and other claims, mixed IFRS/US GAAP lease EBITDA. NOT valuation evidence.", published_prediction=E["predicted"], prediction_vs_diagnostic_median=E["predicted"]/stats["median"]-1, benchmark_dataset=bench.dataset.dataset_id, benchmark_sha256=bench.dataset.sha256, benchmark_match=bench.summary(), industry_row=sector_values, benchmark_statistic="Industry multiple; median NOT established by supplied file", prediction_vs_industry_positive_EBITDA_ratio=E["predicted"]/benchmark_value-1, alternative_unit_policy=E["unit_policies"]["dfr_tax_percent_points"], conclusion="Large unexplained level and material unit ambiguity; no currency/per-share error found. No evidence supports changing approved decimal policy to force agreement. Withdraw regression point estimate rather than headline it.")
    dump("regression_plausibility_repair.json", plausibility)
    J["status"] = "not_usable"
    J["chosen"] = None
    J["remediation"] = plausibility
    E["status"] = "NOT USABLE: failed economic plausibility; arithmetic only, not price target"
    dump("regression_results.json", J)
    for filename in ["valuation_multiples.csv", "sensitivities.csv"]:
        df = pd.read_csv(P / filename)
        df["decision_use_status"] = "NOT USABLE: withdrawn regression valuation; historical arithmetic only"
        df.to_csv(P / filename, index=False)
    reg = load_workbook(P / "regression_valuation.xlsx")
    for row in reg["Predictions"].iter_rows(min_row=2):
        if row[0].value == "EV/EBITDA":
            row[2].value = E["status"]
    reg.save(P / "regression_valuation.xlsx")
    wb = load_workbook(P / "comparables_audit.xlsx")
    sheet(wb, "Qualification_Repair", Q)
    sheet(wb, "Uniform_Bridge_Repair", B)
    sheet(wb, "Currency_Repair", pd.DataFrame([unit]))
    # The original numeric-prospect worksheet is retained as historical evidence.
    sheet(wb, "Plausibility_Repair", pd.DataFrame([dict(item=k, value=json.dumps(v, default=str)) for k, v in plausibility.items()]))
    wb.save(P / "comparables_audit.xlsx")
    revised = {
        "C03": ("PROVISIONAL", "USD-to-GBP and current ordinary-share conversion PASS, no GBp/ADR error. New issuer reconciliations reveal Neste EBITDA1438 vs vendor1124, unresolved BP EBIT14.27%, preferred/hybrid claim proxies; raw comparability still fails."),
        "C04": ("PROVISIONAL", "Fourteen source-linked qualification findings and fifteen uniform bridge attempts added. All unresolved claims/associate adjustments remain NA, not zero. Complete membership/ownership/history certification not achieved."),
        "C05": ("FAIL_OPEN", "Both supplied industry datasets registered and UK exact-region resolution confirmed. EV/EBITDA industry ratio5.94 (positive EBITDA) /5.66 (all) is NOT proven to be a median. Qualified-peer median remains unavailable; genuine median/period verification still fails."),
        "C08": ("BLOCKED", "Correction: previous ten were numeric prospects, not ten selected peers. Four exclusions (OXY,HBR,OMV,CVX), six held; four substitutes investigated but none uniform-certified. No ten or feasible eight certified peers; no padded selection."),
        "C09": ("BLOCKED", "Ownership/restructuring and operating-business evidence added for original ten and four substitutes. Rejection/hold findings now explicit. Complete bidirectional ownership, history, identity and operating perimeter checks not passed for a panel."),
        "C10": ("BLOCKED", "No compliant panel available; geographic/tier feasibility cannot substitute for hard-filter and bridge approval."),
        "C17": ("BLOCKED", "EV/EBITDA still unsuitable for release without six valid uniform selected-peer observations. No suitable alternative primary multiple certified."),
        "C18": ("BLOCKED", "All fifteen rows use FY2025 financial date and common quote/FX date2026-10-30 with EUR comparison units. Borrowings/leases/NCI/claims reconciliations logged, but associate contributions, hybrid claims and US GAAP operating-rent EBITDA remain unresolved. Usable EV/inverse deliberately NA."),
        "C19": ("BLOCKED", "No selected panel exists for selected-ISIN verification or three random selected-peer checks. Prior random numeric-candidate checks are historical only, not selected-peer certification. Human review remains pending."),
        "C20": ("BLOCKED", "No qualified-peer quartile/set/multiple sensitivity. Prior conditional regression sensitivities retained as withdrawn arithmetic, not valuation ranges."),
        "C42": ("FAIL_OPEN", "Currency/share arithmetic verified.18.072785x materially exceeds original prospect diagnostic and supplied industry ratio5.94; alternate unit policy4.276716x materially differs. No justified economic/perimeter fix; estimate explicitly NOT USABLE. Unit/sector plausibility gate not passed."),
    }
    original_qa = (P / "qa_results.md").read_text()
    assert "## Failed-item remediation" not in original_qa, "Do not execute this remediation twice"
    sections = re.split(r"(?=### C\d+)", original_qa)
    for item in revised:
        prior = next(s for s in sections if s.startswith("### " + item))
        assert any(x in prior.splitlines()[0] for x in ["PROVISIONAL", "FAIL_OPEN", "BLOCKED"])
    repair_qa = "# Failed-item remediation — BP.L\n\n" + STAMP + "\n\nOnly the eleven previously non-passing items below were reassessed. Original full block C execution count remains1. Passing items and published-route N/A checks were not rerun.\n\n" + "\n\n".join(f"### {k} — {v[0]}\n{v[1]}" for k, v in revised.items()) + "\n"
    (P / "qa_failed_item_recheck.md").write_text(repair_qa)
    (P / "qa_results.md").write_text(original_qa + "\n## Failed-item remediation\n\n" + STAMP + ": see qa_failed_item_recheck.md for current findings; original statuses above retained as history. Regression is now NOT USABLE, not a conditional valuation headline. No original passing item rerun.\n")
    dump("repair_result.json", dict(timestamp=STAMP, original_prospects=ORIGINAL, substitutes=SUBSTITUTES, reviewed=14, rejected=Q[Q.decision.eq("reject")].ticker.tolist(), qualified_count=0, bridge_rows=len(B), regression_status="not_usable", full_QA_executions=1, failed_items_rechecked=list(revised), current_statuses={k:v[0] for k,v in revised.items()}))
    print(json.dumps({"diagnostic":stats,"currency":unit,"statuses":{k:v[0] for k,v in revised.items()}}, indent=2))


if __name__ == "__main__":
    if len(sys.argv) == 3 and sys.argv[1] == "--evidence-dir":
        directory = Path(sys.argv[2])
        urls = json.loads((directory / "urls.json").read_text())
        evidence = []
        anchors = [r"[Bb]orrowings.*[0-9]", r"[Ff]inance debt.*[0-9]", r"[Ll]ease (?:liabilities|debt).*[0-9]", r"[Hh]ybrid capital.*[0-9]", r"[Pp]referred stock,", r"[Nn]on.controlling interests.*[0-9]", r"[Pp]erpetual.*[0-9]", r"[Oo]ther equity instruments.*[0-9]", r"[Ss]ubordinated notes.*[0-9]", r"[Ss]tate of Finland", r"[Ss]tate of Norway", r"[Mm]ajor shareholders", r"[Bb]eneficial [Oo]wners", r"CrownRock", r"Adura", r"Neptune", r"Borealis", r"Wintershall", r"Tellurian"]
        for ticker, url in urls.items():
            path = directory / (ticker + ".txt")
            if not path.exists():
                continue
            snippets = []
            for anchor in anchors:
                found = 0
                for page_number, page in enumerate(path.read_text().split("\f"), start=1):
                    lines = page.splitlines()
                    for i, line in enumerate(lines):
                        if re.search(anchor, line):
                            snippets.append(dict(anchor=anchor, PDF_page_number=page_number, quote="\n".join(lines[max(0, i-1):i+4])))
                            found += 1
                            if found == 2:
                                break
                    if found == 2:
                        break
            evidence.append(dict(ticker=ticker, source_url=url, access_date=STAMP[:10], PDF_sha256=hashlib.sha256((directory / (ticker + ".pdf")).read_bytes()).hexdigest(), extracts=snippets, limitation="Located issuer evidence, not blanket certification of every hard filter or current ownership. PDF page number includes covers."))
        dump("issuer_evidence_repair.json", evidence)
        log = SourceLog(P.parent / "source_log.csv")
        for item in evidence:
            input_id = "BP_repair_issuer_" + item["ticker"]
            if any(row["input_id"] == input_id for row in log.rows):
                continue
            pages = sorted({x["PDF_page_number"] for x in item["extracts"]})
            log.add(input_id=input_id, company=item["ticker"], metric="FY2025 bridge/ownership/event issuer evidence", value="Located extracts and SHA256 in relative/issuer_evidence_repair.json", unit="reporting-currency millions or shares/ownership as labelled", period_end="2025-12-31", as_of_date="2026-10-30", access_date=STAMP[:10], source_name="issuer published report", url_or_local_file=item["source_url"], page_note_sheet_cell="PDF pages " + str(pages), dataset_vintage="FY2025", reported_or_adjusted="reported; adjustments not silently applied", consolidation_scope="issuer consolidated unless extract states otherwise", status="sourced", limitation=item["limitation"])
        log.save()
    else:
        main()
