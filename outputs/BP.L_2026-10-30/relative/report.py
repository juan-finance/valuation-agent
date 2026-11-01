"""One shared content stream for the revised BP PDF and plain summary."""
import json
import re
from pathlib import Path
from xml.sax.saxutils import escape

from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.platypus import PageBreak, Paragraph, SimpleDocTemplate

P = Path(__file__).resolve().parent
O = P.parent
U = json.loads((P / "currency_bridge_verification.json").read_text())
V = json.loads((P / "regression_plausibility_repair.json").read_text())
blocks = [
    ("title", "BP.L — relative valuation, 30 October 2026"),
    ("status", "NO USABLE VALUATION RELEASED. Comparable valuation is BLOCKED; regression estimate is NOT USABLE. The prior GBP23.5868 conditional result is withdrawn as a valuation headline. No price target or recommendation is issued."),
    ("h", "1. Scope and basis"),
    ("p", "BP p.l.c., London ordinary GB0007980591. Closing quote627.4GBX = GBP6.274; rounded current ordinary shares15,450million. Quote x shares GBP96,933.3million is0.0275% below vendor GBP96,960million. FY2025 financials, not TTM/forward;30October2026 quote/FX. FY claims remain stale, not October balance sheets. Approved relative_only: no DCF or stage4 recommendation. Human Spot_check remains pending."),
    ("h", "2. Qualification: no certified ten-peer panel"),
    ("p", "Correction: the prior ten names were numerical prospects, not selected qualified peers. Reassessed OXY,HBR,OMV,ENI,NESTE,CVX,EQNR,REP,TTE,VLO; investigated substitutes SHEL,GALP,WDS,AKRBP. Reject OXY (CrownRock2024/OxyChem January2026 perimeter), HBR (Wintershall Dea2024 and LLOG2026), CVX (Hess July2025, partial-year earnings/full closing claims), OMV (Borealis/Borouge disposal and2026 combination). Matching pro formas were not established. Six original prospects and four substitutes remain on hold, not certified."),
    ("p", "Business review distinguishes integrated operators from upstream/LNG and refining/renewables. Neste/Valero are Tier2 refiners, not integrated upstream pure-plays; Woodside/AkerBP are upstream/LNG. Galp's legal holding parent operates a consolidated energy business, not a passive investment vehicle. Unrelated state/BASF/ADNOC ownership does not itself trigger BP cross-holding exclusion. Issuer AkerBP ownership BP16% is below the >20% gate, but does not waive other checks. Complete current bidirectional ownership/history/identity certification remains outstanding where indicated in the audit."),
    ("p", "EQNR/SHEL December2025 Adura deconsolidation requires an operating/associate bridge; ENI Neptune/satellite comparability remains unresolved. No panel is uniform-certified: qualified count0, below the required eight minimum. Geographic/tier feasibility cannot substitute for qualification. All11 multiple rows remain unavailable; no selected-peer quartiles or peer-implied price is asserted. Fourteen source-linked findings are recorded in comparables_audit.xlsx and peer_qualification_repair.csv."),
    ("h", "3. Uniform bridge: reconciliations and remaining blockers"),
    ("p", "Fifteen rows cover BP, all ten prospects and four substitutes: FY2025 balance date,30October2026 price/FX, all component amounts converted to EUR. Required EV includes debt plus ALL leases once, NCI and other non-common claims, less cash and only matched excluded associates. Unknown claims are NA, not zero. Usable EV/inverse fields remain NA: the policy has not yet been satisfied uniformly."),
    ("p", "BP USDmillion debt72,529 = financial debt57,958 + leases14,571; cash36,556; NCI20,948 includes hybrid15,955 ONCE; separate preference carrying proxy21 is not market value. Verified debt including leases: ENI EUR34,202 (leases5,700), EQNR USD31,221 (3,411), Neste EUR5,183 (740, issuer NCI0), Galp EUR4,899 (1,217), Woodside USD13,722 (1,759; NCI3,929). Reconciliation does not certify the operating denominator."),
    ("p", "Chevron USD46,743 already equals issuer debt40,758 + operating leases5,985; finance leases1,445 are already within40,758. Valero USD11,703 already equals debt/finance leases10,619 + operating leases1,084. Do NOT add leases twice. US GAAP operating rent still reduces EBITDA unlike IFRS16. Unresolved vendor/issuer debt differences: Shell USD45, TTE USD388, HBR USD5. Additional carrying claims include OXY preferred8,287, Repsol other equity3,046 and OMV hybrid1,985. TTE perpetual-note claim needs a separate bridge; Harbour2,025 is subordinated investor equity, not ordinary NCI."),
    ("p", "BP vendor/issuer EBIT14,446/12,642 differs14.27%; EBITDA30,168/30,464 differs0.98% on issuer denominator. Neste reported issuer EBITDA1,438 versus vendor1,124 differs21.84%. BP impairment6,037 exceeds10% of EBIT; impairment-addback EBITDA36,501 remains an unharmonized sensitivity, not a base replacement. Associates and transaction/lease denominators remain unresolved; no selective source switching to force agreement."),
    ("h", "4. Regression check — NOT USABLE"),
    ("p", f'EUROPE January2026 equation predicts18.072785x EV/EBITDA, published R-squared26.2%, under approved decimal DFR/tax policy. Qualified-peer median: unavailable. Diagnostic ONLY: ten original unqualified prospects median{V["original_numeric_prospect_diagnostic"]["median"]:.6f}x before associates/other claims; prediction{V["prediction_vs_diagnostic_median"]:.2%} higher. It includes rejected companies and mixed lease EBITDA: NOT a qualified peer median or valuation basis.'),
    ("p", f'New registered January2026 Europe integrated oil/gas industry ratios:5.94x positive-EBITDA firms and5.66x all firms,12 firms.18.072785x is{V["prediction_vs_industry_positive_EBITDA_ratio"]:.2%} above5.94x. Supplied files do not establish genuine medians; no relabelling of an industry ratio as a median. Different benchmark vintage/period also remains. Sector plausibility is not validated.'),
    ("p", f'Currency/share mechanics PASS: USD1.1172 and GBP0.8338 per EUR imply{U["GBP_per_USD"]:.9f} GBP/USD. Historical inverse equity USD{U["inverse_equity_usdm"]:,.6f}million /15,450million ordinary shares = USD{U["mechanical_USD_per_ordinary"]:.9f}/ordinary; x0.8338/1.1172 = GBP{U["mechanical_GBP_per_ordinary"]:.9f}, NOT GBp. No second /100 and no six-for-one ADS adjustment: denominator is London ordinary shares. Correct arithmetic does NOT make GBP23.5868 usable fair value.'),
    ("p", "Historical regression inverse: multiple x EBITDA -debt -NCI -preference +cash; associates retained, no carrying-value addback. Percentage-point DFR/tax alternative4.276716x materially differs: no justified unit change solely to fit sector values. Fundamental growth0 substitutes are not five-year forecasts; effective tax83.281694%, common NI54 and payout93.666667x imply severe extrapolation. PE758.921321x is not selected; negative PBV-22.600011x not valued. No blending, actionable range or upside."),
    ("h", "5. Failed-only QA and provenance"),
    ("p", "QA block C full execution count remains1; only11 previously non-passing items reassessed. C03,C04 PROVISIONAL; C05,C42 FAIL_OPEN; C08,C09,C10,C17,C18,C19,C20 BLOCKED. C18 currency/share subcheck passes, overall uniform bridge does not. C42 is contained by marking NOT USABLE, not falsely passed. Original passing checks were not rerun; human review not performed."),
    ("p", "Accessed1November2026: issuer FY2025 reports for original prospects/substitutes, Chevron Hess completion, BASF Wintershall completion and Valero2026 proxy. Source URLs, PDF hashes, located extracts, reconciliation differences and unresolved gates are in the audit and source schedules. Vendor FY2025 StockAnalysis inputs retained unchanged. Registered industry datasets evebitda_industry_europe_2026-01 and pbv_industry_europe_2026-01 are as-of5January2026; published regressions_multi_2026-01 exact EUROPE. No residual bands, own-estimation diagnostics or confidence intervals invented."),
    ("p", "Academic analysis only; not personal investment advice. No actionable valuation or Buy/Hold/Sell recommendation is supported by this incomplete evidence."),
]
blocks = [(t, re.sub(r"(\d)(?=[A-Za-z])", r"\1 ", re.sub(r"([a-z])(?=\d)", r"\1 ", v))) for t, v in blocks]
plain = "\n\n".join(("# " if t == "title" else "## " if t == "h" else "") + v for t, v in blocks) + "\n"
(O / "relative_summary.md").write_text(plain)
(P / "valuation_summary.md").write_text(plain)
styles = getSampleStyleSheet()
styles.add(ParagraphStyle(name="BodyBP", fontName="Helvetica", fontSize=9.2, leading=12.8, spaceAfter=7, textColor=colors.HexColor("#243746")))
styles.add(ParagraphStyle(name="AlertBP", parent=styles["BodyBP"], fontName="Helvetica-Bold", backColor=colors.HexColor("#FFF0D6"), borderPadding=7, spaceAfter=12))
styles["Title"].fontSize = 19
styles["Title"].leading = 23
styles["Heading2"].fontSize = 11
styles["Heading2"].leading = 14
story = []
for t, v in blocks:
    if t == "h" and v.startswith("4."):
        story.append(PageBreak())
    story.append(Paragraph(escape(v), styles["Title" if t == "title" else "Heading2" if t == "h" else "AlertBP" if t == "status" else "BodyBP"]))


def footer(canvas, doc):
    canvas.saveState()
    canvas.setFont("Helvetica", 8)
    canvas.drawString(38, 24, "BP.L | 2026-10-30 | NO USABLE VALUATION | Academic analysis")
    canvas.drawRightString(A4[0] - 38, 24, str(doc.page))
    canvas.restoreState()


SimpleDocTemplate(str(O / "relative_report_BP.L.pdf"), pagesize=A4, rightMargin=38, leftMargin=38, topMargin=35, bottomMargin=38, title="BP.L relative valuation — regression NOT USABLE", author="Valuation research").build(story, onFirstPage=footer, onLaterPages=footer)
print(O / "relative_report_BP.L.pdf")
