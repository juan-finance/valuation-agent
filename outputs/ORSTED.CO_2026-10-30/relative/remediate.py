"""ORSTED.CO remediation under qa_grading_and_remediation: fix issuer sensitivities, re-grade QA, refresh figures/notes/run_state."""
import json, time
from pathlib import Path
import pandas as pd

P=Path(__file__).resolve().parent; O=P.parent
FX_DKK=7.4735; SHARES=1321.062; MED=13.011383039271486
# Bridge (DKKm): equity = med*EBITDA - (debt 107,857 + NCI 8,268 - cash 53,448) - hybrid 20,955
BRIDGE=107857+8268-53448+20955
def ps(ebitda_dkkm):
    return (MED*ebitda_dkkm - BRIDGE)/SHARES/FX_DKK
rows=[('vendor FY2025 EBITDA',21583.0),
      ('issuer reported EBITDA',22448.0),
      ('issuer EBITDA excl. new partnerships and cancellation fees',25065.0)]
out=pd.DataFrame([dict(scenario=n,EBITDA_dkkm=v,peer_median_ev_ebitda=MED,DKK_per_share=round((MED*v-BRIDGE)/SHARES,2),EUR_per_share=round(ps(v),2),note='mechanical median-held-fixed sensitivity; vendor vs issuer EBITDA basis (definitions/perimeter differ), no per-row source switching') for n,v in rows])
out.to_csv(P/'sensitivities.csv',index=False)
print(out.to_string(index=False))
