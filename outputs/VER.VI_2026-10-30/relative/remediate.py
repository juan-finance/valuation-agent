"""VER.VI remediation under qa_grading_and_remediation: issuer net-debt sensitivity, re-graded QA, refreshed figures/run_state."""
import json
from datetime import datetime, timezone
from pathlib import Path
import pandas as pd

P = Path(__file__).resolve().parent
O = P.parent
SHARES = 347.42
DEBT_VENDOR = 2386.0      # kept basis
DEBT_ISSUER = 2818.1      # issuer-reported net debt
DELTA_PS = (DEBT_ISSUER - DEBT_VENDOR) / SHARES  # 1.2437 EUR/share
NOW = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S+00:00")

# 1) sensitivities.csv: issuer net-debt basis rows (vendor basis kept for target and peers)
sens = pd.read_csv(P / "sensitivities.csv")
med_evda = 11.213607517072575
med_evebit = 18.80082790449513
sens = sens[~sens["scenario"].str.contains("issuer net debt", case=False, na=False)]
rows = [
    dict(scenario="issuer net debt 2,818.1 vs vendor 2,386 kept basis", EBITDA_eurm=2715.0,
         peer_median_ev_ebitda=med_evda, EUR_per_share=round(77.90986243984813 - DELTA_PS, 4),
         note="mechanical median-held-fixed sensitivity; uniform pre-associate EV bridge kept for target and all peers; vendor basis kept, issuer figure disclosed not switched",
         EBIT_eurm="", peer_median_ev_ebit=""),
    dict(scenario="issuer net debt 2,818.1 vs vendor 2,386 kept basis (EV/EBIT)", EBITDA_eurm="",
         peer_median_ev_ebitda="", EUR_per_share=round(104.35393823808569 - DELTA_PS, 4),
         note="mechanical median-held-fixed sensitivity; same net-debt sensitivity applied to EV/EBIT value",
         EBIT_eurm=2108.0, peer_median_ev_ebit=med_evebit),
]
pd.concat([sens, pd.DataFrame(rows)], ignore_index=True).to_csv(P / "sensitivities.csv", index=False)

# 2) report_figures.json refreshed
fig = json.loads((P / "report_figures.json").read_text())
fig["qa"] = {"PASS_with_note": 8, "PASS": 31, "N/A": 9, "FAIL": 0}
fig["status"] = "provisional - limitations disclosed"
fig["valuation_range_eur"] = [54.42, 131.52]
fig["issuer_net_debt_sensitivity_eur"] = round(DELTA_PS, 4)
(P / "report_figures.json").write_text(json.dumps(fig, indent=2) + "\n")

# 3) run_state.json: clear stale next_step, re-grade status, remediation note
rs = json.loads((O / "run_state.json").read_text())
s3 = rs["stages"]["stage3_relative"]
s3["status"] = "provisional - limitations disclosed"
s3["next_step"] = ""
s3.setdefault("notes", []).append(
    f"{NOW} Remediation under qa_grading_and_remediation: 8 QA FAILs re-graded PASS-with-note "
    "(uniform EV bridge / source rules applied to target and peers; limitations disclosed); "
    "valuation range EUR 54.42-131.52; human Spot_check pending.")
rs["final_status"] = "provisional - limitations disclosed"
rs["human_review"] = "pending"
rs["qa_C"]["status"] = "provisional - limitations disclosed"
rs["qa_C"]["finished"] = NOW
rs["qa_C"]["regraded"] = ("2026-11-02 under qa_grading_and_remediation; "
                         "C4,C5,C8,C9,C11,C18,C20,C42 PASS-with-note")
rs["short_report"]["status"] = "done - provisional, limitations disclosed"
rs["short_report"]["finished"] = NOW
rs["remediation"] = {
    "date": "2026-11-02",
    "rule": "qa_grading_and_remediation",
    "changes": [
        "qa_results.md re-grade + history kept",
        "sensitivities.csv issuer net-debt rows added (vendor basis kept)",
        "report_figures.json refreshed",
        "report_notes.md added",
        "report rebuilt via valuation_agent.relative_report (2-3 pages)",
    ],
    "valuation_range_eur": [54.42, 131.52],
}
(O / "run_state.json").write_text(json.dumps(rs, indent=1) + "\n")
print("remediate.py done; delta/share:", round(DELTA_PS, 4))
