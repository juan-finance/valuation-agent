<!-- Text-only digest of examples/case_3_nestle_fcfe_2stage/professor_calculation.docx, generated once. Images/screenshots in the original are not captured. METHOD ONLY: never copy numbers, rates or assumptions into a new valuation (dated inputs). Lowest rank in the hierarchy. -->

# case_3_nestle_fcfe_2stage

**Nestle**

Nestlé S.A. is a Swiss multinational nutritional and health-related consumer goods company, with headquarters Switzerland. It is the largest food company in the world measured by revenues. Average figures for the last 5 years exhibit a growth in EPS of 5%, while significant investments (acquisitions) have been undertaken. Consequently analysts expect a growth of about 11% in EPS, which will last for approximately 5 years. In addition, Nestle seems to keep a relatively low Debt ratio equal to 37.6%, which is expected to be the target for the following years. The market value D/E is 0.11 and Nestle pays an effective tax rate equal to 30.95%. Current figures from the latest annual report include the following:

| EPS | 108.88Sfr |
| --- | --- |
| DPS | 38Sfr |
| Revenue/Share | 1820,00Sfr |
| Capital Expenditure/Share | 114.2Sfr |
| Depreciation/Share | 73.8Sfr |
| ROE | 23.63%, expected to drop to 16% after 5y |
| WC/Revenue | 9.30%, expected to be stable and grow with Earnings |
| Net CapEx/Depreciations | Current ratio is expected to drop to 50% after 5y |

Nestle has been a multinational company with operations in the following areas:

| Area | Revenues | Risk Premium |
| --- | --- | --- |
| North America | 17.5 | 4.00% |
| South America | 4.3 | 12.00% |
| Switzerland | 1.1 | 4.00% |
| Germany/France/UK | 18.4 | 4.00% |
| Italy/Spain | 6.4 | 5.50% |
| Asia | 5.8 | 9.00% |
| Rest of W. Europe | 13 | 4.00% |
| Eastern Europe | 4 | 8.00% |

The industry bottom-up (unlevered) beta is 0.79, while the long term government bond rate pays a 4% return. The long term stable growth is expected to reach this level.

- What method would you use for the evaluation?

- What are the expected Cash Flows?

- What is the appropriate discount rate?

- The market price is 2906 Sfr. what investment strategy would you suggest? 

**Solution**

- What method would you use for the evaluation?

Nestle seems to keep low dividend payments compared to available earnings. Consequently a Dividend discount model would probably undervalue the value of equity. In addition, leverage seems to be fairly stable and thus, a FCFE model can be used. Analyst forecast a high growth stage and thus, a 2-stage growth model should be preferred.

- What are the expected Cash Flows?

We should find the FCFE. Considering that Debt ratio is expected to be stable, Nestle finances new projects with both debt and equity. Consequently we can use the following steps to reach FCFE

The inputs for the model can be summarized below:

|  | High Growth (5y) | Stable Growth (>5y) |
| --- | --- | --- |
| Beta (see below for derivation) | 0.85 | 0.85 |
| ROE | 23.63% | 16% |
|  | 34.9% | - |
| RR=1-PBR | 65.1% | - |
| Expected Growth | ROE*RR=0.2363*0.651=15.38% | 4% |
| WC/Rev | 9.30% | 9.30% |
| Debt Ratio | 37.6% | 37.6% |
| Net CapEx/Dep | (114.2-73.8)/73.8=55% | 50% |

Then FCFE can be calculated as follows

| Year | Earningst= Earningst-1(1+g) | (1-DR) | (1-DR)Net Cap Ext= (1-DR) (Cap Ext-1-Dep t-1)(1+g) | (1-DR)ΔNWCt= (1-DR)(ΔRevt)(WC/Rev)= (1-DR)(Revt-1*g)(WC/Rev) | FCFE |
| --- | --- | --- | --- | --- | --- |
| 0 | 108.88 | 0.624 | 25.21 | - |  |
| 1 | 125.63 | 0.624 | 0.624(114.2-73.8)(1.1538) =29.07 | 0.624*(1820*0.1538)0.093 =16.25 | 80.31 |
| 2 | 144.95 | 0.624 | 33.54 | 18.75 | 92.67 |
| 3 | 167.25 | 0.624 | 38.7 | 21.63 | 106.92 |
| 4 | 192.98 | 0.624 | 44.65 | 24.96 | 123.37 |
| 5 | 222.66 | 0.624 | 51.52 | 28.79 | 142.35 |
| Terminal Value | 222.66(1.04) =231.57 | 0.624 | 73.8*(1.1538)5(1.04)(0.5) =78.5*0.624 | 1820(1.1538)5(0.04)(0.093)0.624 =13.85*0.624 | 173.93 |

New CapEx/Dep

An alternative derivation of the FCFE

|  | (1) | (2) | (3) | (4) | (5) | (6) | (7) |  |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| Year | EPSt= EPSt-1* (1+g) | NetCapExt= Dept-1 * (1+g)* NetCapEx/Dep | (1-δ)*NCEt | Salest= Salest-1 * (1+g) | Δsales | WCτ= Δsalesτ * WC/Sales | WC Investment= (1-δ)* WCτ | FCFE= (1)-(3)-(7) |
| 0 | 108.88 | 40.59 | 25.33 | 1820.00 |  |  |  |  |
| 1 | 125.63 | 46.83 | 29.22 | 2099.92 | 279.92 | 26.03 | 16.24 | 80.16 |
| 2 | 144.95 | 54.04 | 33.72 | 2422.88 | 322.97 | 30.04 | 18.74 | 92.49 |
| 3 | 167.24 | 62.35 | 38.90 | 2795.52 | 372.64 | 34.66 | 21.63 | 106.71 |
| 4 | 192.96 | 71.94 | 44.89 | 3225.47 | 429.95 | 39.99 | 24.95 | 123.12 |
| 5 | 222.64 | 83.00 | 51.79 | 3721.55 | 496.08 | 46.14 | 28.79 | 142.06 |
| 6 | 231.54 | 78.47 | 48.97 | 3870.41 | 148.86 | 13.84 | 8.64 | 173.94 |

- What is the appropriate discount rate?

The appropriate discount rate is the cost of equity. For this we need the MRP. Since Nestle is a multinational company, all markets, in which it operates, should be taken into account.

| Area | Revenues | Weight | Risk Premium |
| --- | --- | --- | --- |
| North America | 17.5 | 24.82% | 4.00% |
| South America | 4.3 | 6.10% | 12.00% |
| Switzerland | 1.1 | 1.56% | 4.00% |
| Germany/France/UK | 18.4 | 26.10% | 4.00% |
| Italy/Spain | 6.4 | 9.08% | 5.50% |
| Asia | 5.8 | 8.23% | 9.00% |
| Rest of W. Europe | 13 | 18.44% | 4.00% |
| Eastern Europe | 4 | 5.67% | 8.00% |
| Total | 70.5 | 100% | Avg RP=5.26% |

We assume that Nestle is exposed to country and market risk the same way. You could use λ.

- If the market price in 2001 was 2906 Sfr, what investment strategy would you suggest? 

Given the lower market price a buying strategy should be profitable. Note that we use a higher ROE and high retention ratio. This results in an expected growth rate higher than the one expected by analysts. Judging retrospectively, Nestle has moved aggressively, acquiring many companies (investments) and therefore a higher growth rate might be justified.
