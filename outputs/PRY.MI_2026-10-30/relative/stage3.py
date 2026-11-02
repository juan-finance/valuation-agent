"""PRY.MI stage 3 (relative only): comparables (10 peers, primary PE) and published EUROPE regressions.

Route: comparables web_minimum / fundamental growth; regression published_damodaran (decimal units, analyst growth
substituted by fundamental growth, labelled). Arithmetic from src/valuation_agent; judgement (tiers, exclusions) below.
"""
import json
from pathlib import Path

import numpy as np
import pandas as pd

from valuation_agent import comparables as comp
from valuation_agent import datasets, published_regressions as pr
from pool import load, f

P = Path(__file__).resolve().parent
DATE = '2026-10-30'
TARGET = 'PRY.MI'
PRICE, SHARES = 110.40, 292.25          # EUR, m shares (stockanalysis, 2026-10-30)
MCAP = PRICE * SHARES                    # 32,259.99 EUR m
NI, EQ, EQ_PRIOR, SALES, EBIT, EBITDA = 1270.0, 6474.0, 5087.0, 19741.0, 1531.0, 1979.0
DEBT, CASH, NCI = 5227.0, 2025.0, 206.0
ROE = NI / ((EQ + EQ_PRIOR) / 2)        # parent NI / average parent equity (procedure section 4)
PAYOUT = 0.18031496062992125
BETA = 0.92
TAX = 358.0 / 1654.0
ROIC = EBIT * (1 - TAX) / (EQ + DEBT - CASH)
DFR = DEBT / (DEBT + MCAP)
G_FUND = ROE * (1 - PAYOUT)              # fundamental growth ROE x retention (web route rule)
EBITDA_M = EBITDA / SALES
NET_DEBT_EBITDA = (DEBT - CASH) / EBITDA
CAPEX_SALES = 751.0 / SALES
EPS = NI / SHARES

# Business judgement (agent): tier 1 = electrical equipment, cables, grid and electrification; tier 2 = adjacent
# industrial capital goods / power equipment; excluded = oil and gas, utilities and renewable developers, mining,
# metals, chemicals, materials, fuels and businesses below the EUR 3.2bn size band (0.1x target market cap).
TIER = {
    'NEX': (1, 'cables and grid connection systems'), 'NKT': (1, 'power cables and high-voltage systems'),
    'LR': (1, 'electrical infrastructure and connectors'), 'SU': (1, 'electrification, energy management'),
    'ABBN': (1, 'electrification and automation'), 'ENR': (1, 'grid technologies, gas and wind power equipment'),
    'SIE': (2, 'industrial automation with electrification exposure (conglomerate)'),
    'ALFA': (2, 'heat transfer and separation machinery'), 'ATCO.A': (2, 'compressors, industrial tools'),
    'METSO': (2, 'process machinery'), 'ANDR': (2, 'process equipment and hydropower'),
    'G1A': (2, 'process technology'), 'KRN': (2, 'packaging and beverage machinery'),
    'IMI': (2, 'flow control and industrial valves'), 'HLMA': (2, 'safety and environment instrumentation'),
    'SKF.B': (2, 'bearings and seals'), 'SPX': (2, 'steam and electric thermal equipment'),
    'ROR': (2, 'flow control actuators'), 'SUN': (2, 'pumps and turbomachinery services'),
    'BUCN': (2, 'hydraulic and specialised machinery'), 'IP': (2, 'pumps and industrial components'),
    'INDT': (2, 'industrial niche companies'), 'WRT1V': (2, 'marine and energy power equipment'),
    'NDX1': (2, 'wind turbines (power equipment)'), 'VWS': (2, 'wind turbines (power equipment)'),
    'KGX': (3, 'material handling (forklifts)'), 'BCHN': (3, 'compressors, small cap'),
    'EPI.A': (3, 'mining equipment'), 'SAND': (3, 'mining equipment and tools'), 'SMIN': (3, 'industrial and detection products'),
}
EXCLUDED = {  # ticker -> reason
    'OIL_GAS': 'oil, gas and fuels', 'UTIL': 'utility or renewable developer', 'METALS': 'mining, metals, chemicals or materials',
    'OFFSHORE': 'oilfield services', 'FIN': 'financial or holding', 'SIZE': 'market cap below EUR 3.2bn (size band 0.1x)',
    'INCOMPLETE': 'source fields incomplete for scoring',
}
OIL_GAS = ['SHEL', 'TTE', 'BP', 'EQNR', 'ENI', 'REP', 'OMV', 'GALP', 'VAR', 'AKRBP', 'ENOG', 'DNO', 'TGS', 'NESTE', 'ORLEN', 'VARE', 'GENL', 'ITH', 'BWO', 'HFC']
UTIL = ['IBE', 'ENEL', 'ENGI', 'EOAN', 'ELE', 'NG', 'SSE', 'EDP', 'EDPR', 'NTGY', 'REE', 'VER', 'ORSTED', 'FORTUM', 'SRG', 'TRN',
        'IG', 'ANE', 'GRE', 'SLR', 'EKT', 'PNE3', 'ERG', 'A2A', 'RWE', 'SCATC', 'DRX', 'CNA', 'HBR', 'SPM', 'DRAX']
METALS = ['GLEN', 'AAL', 'ANTO', 'RIO', 'BAS', 'NHY', 'YAR', 'BOL', 'MT.AS', 'HEI', 'VOE', 'TKA', 'SZG', 'APAM', 'ACX', 'NDA',
          'ALLEI', 'GRNG', 'BEKB', 'SSAB.A', 'SDF', 'NK', 'OUT1V', 'ERA', 'VBK', 'SMIN', 'WEIR', 'ELM', 'IMO', 'RAA']
OFFSHORE = ['SUBC', 'SBMO', 'TE', 'SAIPEM']
FIN = []


def classify(t):
    if t in TIER:
        return TIER[t][0], None
    if t in OIL_GAS: return None, 'OIL_GAS'
    if t in UTIL: return None, 'UTIL'
    if t in METALS: return None, 'METALS'
    if t in OFFSHORE: return None, 'OFFSHORE'
    return None, 'OTHER'


def main():
    raw = load()
    rows, rejected = [], []
    for t, r in raw.items():
        if t == 'PRY' or t == 'PRY.MI':
            continue
        if f(r['market_cap_eur_m']) != f(r['market_cap_eur_m']) or f(r['market_cap_eur_m']) < 1000:
            rejected.append((t, r['name'], 'EUR1bn minimum or missing market cap')); continue
        tier, why = classify(t)
        mcap = f(r['market_cap_eur_m'])
        if not (0.1 * MCAP <= mcap <= 10 * MCAP):
            rejected.append((t, r['name'], EXCLUDED['SIZE'])); continue
        if t not in TIER:
            rejected.append((t, r['name'], EXCLUDED.get(why, why))); continue
        if t in TIER and any(f(r[c]) != f(r[c]) for c in ['ni', 'sales', 'EBITDA', 'equity', 'growth', 'beta', 'net_debt_ebitda', 'roe', 'ebitda_margin', 'payout', 'capex_sales']):
            rejected.append((t, r['name'], EXCLUDED['INCOMPLETE'])); continue
        rows.append(dict(ticker=t, name=r['name'], country=r['country'], tier=tier, tier_reason=TIER[t][1], europe=True,
                         mcap=mcap, ln_mcap=float(np.log(mcap)), growth=f(r['growth']), beta=f(r['beta']),
                         net_debt_ebitda=f(r['net_debt_ebitda']), roe=f(r['roe']), ebitda_margin=f(r['ebitda_margin']),
                         payout=f(r['payout']), capex_sales=f(r['capex_sales']), pe=f(r['pe']), pbv=f(r['pbv']), ps=f(r['ps']),
                         ev_ebit=f(r['ev_ebit']), ev_ebitda=f(r['ev_ebitda']), ev_cf=f(r['ev_cf']), ev_sales=f(r['ev_sales']),
                         ev_assets=f(r['ev_assets']), net_margin=f(r['net_margin']), ev=f(r['EV_before_associates']),
                         source_urls=r['source_urls'], isin=''))
    pool = pd.DataFrame(rows).set_index('ticker')
    # Pool-wide tier-3 names can stay only if needed; procedure allows max 2 tier 3.
    target = dict(growth=G_FUND, beta=BETA, net_debt_ebitda=NET_DEBT_EBITDA, roe=ROE, ebitda_margin=EBITDA_M,
                  payout=PAYOUT, capex_sales=CAPEX_SALES, ln_mcap=float(np.log(MCAP)))
    dims = list(comp.WEIGHTS)
    scored, log = comp.similarity_scores(pool[dims], target)
    scored = scored.join(pool)
    sel, info = comp.select_peers(scored)
    if sel is None:
        raise SystemExit('infeasible: ' + json.dumps(info, default=str))
    sel.index.name = 'ticker'
    sel.reset_index().to_csv(P / 'peer_selection_raw.csv', index=False)
    pool.assign(in_pool=True).to_csv(P / 'pool_eligible.csv')
    pd.DataFrame(rejected, columns=['ticker', 'name', 'reason']).to_csv(P / 'pool_rejected.csv', index=False)
    (P / 'peer_selection.json').write_text(json.dumps({'selection': info, 'log': str(log),
                                                       'target': {k: float(v) for k, v in target.items()},
                                                       'weights': comp.WEIGHTS}, indent=2, default=str))
    print('selected', list(sel.index))
    print(json.dumps(info, default=str)[:500])


if __name__ == '__main__':
    main()
