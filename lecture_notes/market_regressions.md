# Regressions of Multiples on Fundamentals: Market Wide

**January 2026**

The following regressions were run across five groupings. The first and most comprehensive set of regressions were run across all traded companies in the United States. The second set of regressions were run across all traded companies in Western Europe and the UK. The third set of regressions were run across companies in emerging markets in Asia, Eastern Europe and Latin America. The fourth set of regressions were run across just Japanese companies. The final set is across all companies globally. If a regression yielded a large negative constant, I reran the regression without the constant to reduce the problem of negative predicted values for the multiples. You can find the multiples classified by region as well as by multiple.

| Region | Multiple |
| :--- | :--- |
| 1. United States | 1. PE |
| 2. Europe | 2. PBV |
| 3. Emerging Markets | 3. PEG |
| 4. Japan | 4. EV/Sales |
| 5. Global | 5. EV/IC |
| | 6. EV to EBITDA |

---

### Application Example

Using the regressions should be pretty straightforward, if you can get the data on the independent variables for your company and stay true to decimal format (25% gets entered as $0.25$). 

As an example, assume that you are looking at Disney in January 2022 and decide to use the US market regression for price to book ratio. Here are the inputs:
* $g =$ The analyst estimate of earnings growth rate for the next 5 years is $12\%$ (if you do not have analyst estimates, substitute your own).
* $\text{Payout ratio} = 20\%$
* $\text{ROE} =$ The return on equity last year was $16.2\%$
* $\text{Beta} = 1.10$

Using the PBV regression:
$$\text{PBV for Disney} = 2.10 + 6.07 g_{\text{EPS}} + 0.69 \, \text{Beta} + 5.09 \, \text{ROE} - 0.33 \, \text{Payout Ratio}$$
$$= 2.10 + 6.07(0.12) + 0.69(1.10) + 5.09(0.162) - 0.33(0.20) = 4.35$$

At its actual price to book ratio of $3.90$, Disney is undervalued.

*Note:* The PEG regression uses the natural log of the expected growth rate. Thus, if your expected growth rate is $15\%$, you will use $\ln(0.15) = -1.8971$.

---

## Regressions Classified by Region

### Market-wide Regressions of Multiples: US Companies in January 2026
*T-statistics in brackets below coefficients*

| Regression | $R^2$ |
| :--- | :---: |
| $\text{PE} = \underset{(12.20)}{13.12} + \underset{(10.0)}{10.52} \, \text{Beta} + \underset{(7.70)}{36.47} \, g_{\text{EPS}} + \underset{(6.89)}{8.46} \, \text{Payout}$ | 38.7% |
| $\text{PEG} = \underset{(1.94)}{-0.60} + \underset{(7.62)}{0.56} \, \text{Payout} - \underset{(14.72)}{1.48} \ln(g_{\text{EPS}}) + \underset{(1.86)}{0.23} \, \text{Beta}$ | 41.4% |
| $\text{PBV} = \underset{(3.17)}{-0.79} - \underset{(0.53)}{0.47} \, g_{\text{EPS}} + \underset{(6.76)}{1.49} \, \text{Beta} + \underset{(34.45)}{20.90} \, \text{ROE} + \underset{(1.30)}{0.17} \, \text{Payout Ratio}$ | 66.2% |
| $\text{EV/Invested Capital} = \underset{(82.70)}{5.75} + \underset{(4.16)}{1.12} \, g + \underset{(0.24)}{0.01} \, \text{ROIC} - \underset{(44.71)}{0.06} \, \text{DFR}$ | 49.7% |
| $\text{EV/Sales} = \underset{(32.41)}{6.77} + \underset{(11.21)}{9.51} \, g + \underset{(8.97)}{0.36} \, \text{Oper Margin} - \underset{(6.32)}{0.02} \, \text{DFR} - \underset{(10.58)}{0.12} \, \text{Tax rate}$ | 24.1% |
| $\text{EV/EBITDA} = \underset{(43.19)}{18.82} + \underset{(23.04)}{39.30} \, g - \underset{(14.08)}{0.20} \, \text{DFR} + \underset{(3.19)}{1.77} \, \text{ROIC}$ | 45.9% |

**Variable Definitions:**
* $g_{\text{EPS}} =$ Expected growth rate in EPS for next 5 years (analyst estimates)
* $g =$ Expected growth rate in revenues for next 5 years (if not available, use $g_{\text{EPS}}$)
* $\text{Payout} = \text{Dividends} / \text{Earnings}$
* $\text{ROIC} = \text{Return on capital} = \text{EBIT}(1 - \text{tax rate}) / \text{Invested Capital}$
* $\text{Operating Margin} = \text{Pre-tax Operating Income} / \text{Sales}$
* $\text{Invested Capital} = \text{Book value of equity} + \text{Book value of debt} - \text{Cash}$
* $\text{ROE} = \text{Net Income} / \text{Book value of Equity}$
* $\text{Tax Rate} = \text{Effective tax rate} = \text{Taxes paid} / \text{Taxable Income}$
* $\text{DFR} = \text{Total Debt} / (\text{Total Debt} + \text{Market value of equity})$
* $\text{RIR} = \text{Reinvestment Rate} = (\text{Cap Ex} - \text{Depreciation} + \Delta\text{WC}) / (\text{EBIT}(1 - t))$

---

### Market-wide Regressions of Multiples: European Companies in January 2026
*T-statistics in brackets below coefficients*

| Regression | $R^2$ |
| :--- | :---: |
| $\text{PE} = \underset{(8.29)}{9.72} + \underset{(4.85)}{2.99} \, \text{Beta} + \underset{(11.95)}{49.82} \, g_{\text{EPS}} + \underset{(9.22)}{7.98} \, \text{Payout}$ | 20.1% |
| $\text{PEG} = \underset{(2.77)}{-0.91} + \underset{(3.15)}{0.76} \, \text{Payout} - \underset{(11.09)}{1.57} \ln(g_{\text{EPS}})$ | 30.3% |
| $\text{PBV} = \underset{(3.70)}{0.73} + \underset{(5.87)}{3.92} \, g_{\text{EPS}} + \underset{(1.38)}{0.13} \, \text{Beta} + \underset{(24.81)}{10.75} \, \text{ROE} - \underset{(2.43)}{0.25} \, \text{Payout Ratio}$ | 42.3% |
| $\text{EV/Invested Capital} = \underset{(67.88)}{4.46} + \underset{(2.92)}{0.90} \, g + \underset{(13.63)}{1.50} \, \text{ROIC} - \underset{(42.64)}{0.05} \, \text{DFR}$ | 51.3% |
| $\text{EV/Sales} = \underset{(21.01)}{5.08} + \underset{(5.39)}{4.03} \, g + \underset{(6.95)}{2.99} \, \text{Oper Margin} - \underset{(7.18)}{0.02} \, \text{DFR} - \underset{(12.26)}{0.09} \, \text{Tax rate}$ | 14.2% |
| $\text{EV/EBITDA} = \underset{(28.40)}{18.15} + \underset{(13.96)}{35.25} \, g - \underset{(10.65)}{0.11} \, \text{DFR} - \underset{(5.19)}{0.12} \, \text{Tax Rate} + \underset{(5.06)}{2.29} \, \text{ROIC}$ | 26.2% |

---

### Market-wide Regressions of Multiples: Japanese Companies in January 2026
*T-statistics in brackets below coefficients*

| Regression | $R^2$ |
| :--- | :---: |
| $\text{PE} = \underset{(5.78)}{4.51} + \underset{(3.50)}{4.28} \, \text{Beta} + \underset{(7.32)}{42.26} \, g_{\text{EPS}} + \underset{(9.05)}{10.46} \, \text{Payout}$ | 34.5% |
| $\text{PEG} = \underset{(2.45)}{-0.70} + \underset{(4.81)}{0.35} \, \text{Payout} - \underset{(12.49)}{1.19} \ln(g_{\text{EPS}}) + \underset{(2.68)}{0.23} \, \text{Beta}$ | 32.4% |
| $\text{PBV} = \underset{(2.63)}{-0.55} + \underset{(6.72)}{4.64} \, g_{\text{EPS}} + \underset{(3.84)}{0.38} \, \text{Beta} + \underset{(14.99)}{14.23} \, \text{ROE}$ | 44.1% |
| $\text{EV/Invested Capital} = \underset{(42.62)}{3.01} + \underset{(16.82)}{8.96} \, g + \underset{(4.57)}{0.16} \, \text{ROIC} - \underset{(27.22)}{0.04} \, \text{DFR}$ | 46.9% |
| $\text{EV/Sales} = \underset{(13.12)}{2.48} + \underset{(16.88)}{11.54} \, g + \underset{(6.38)}{0.44} \, \text{Oper Margin} - \underset{(2.90)}{0.01} \, \text{DFR} - \underset{(5.06)}{0.03} \, \text{Tax rate}$ | 24.4% |
| $\text{EV/EBITDA} = \underset{(20.89)}{10.94} + \underset{(8.71)}{35.22} \, g - \underset{(4.25)}{0.05} \, \text{DFR} + \underset{(2.99)}{1.22} \, \text{ROIC}$ | 6.7% |

---

### Market-wide Regressions of Multiples: Emerging Market Companies in January 2026
*T-statistics in brackets below coefficients*

| Regression | $R^2$ |
| :--- | :---: |
| $\text{PE} = \underset{(10.35)}{14.47} - \underset{(1.33)}{0.51} \, \text{Beta} + \underset{(23.99)}{52.25} \, g_{\text{EPS}} + \underset{(3.24)}{2.22} \, \text{Payout}$ | 27.2% |
| $\text{PEG} = \underset{(4.50)}{-0.78} + \underset{(10.65)}{0.82} \, \text{Payout} - \underset{(30.50)}{1.43} \ln(g_{\text{EPS}}) - \underset{(1.95)}{0.09} \, \text{Beta}$ | 51.9% |
| $\text{PBV} = \underset{(14.31)}{1.32} + \underset{(11.36)}{2.73} \, g_{\text{EPS}} + \underset{(8.04)}{0.43} \, \text{Beta} + \underset{(19.16)}{4.53} \, \text{ROE}$ | 26.3% |
| $\text{EV/Invested Capital} = \underset{(98.22)}{3.42} + \underset{(20.69)}{2.74} \, g + \underset{(5.51)}{0.11} \, \text{ROIC} - \underset{(61.47)}{0.04} \, \text{DFR}$ | 48.8% |
| $\text{EV/Sales} = \underset{(33.23)}{4.10} + \underset{(9.48)}{3.17} \, g + \underset{(5.95)}{0.65} \, \text{Oper Margin} - \underset{(3.38)}{0.01} \, \text{DFR} - \underset{(8.02)}{0.03} \, \text{Tax rate}$ | 5.4% |
| $\text{EV/EBITDA} = \underset{(35.57)}{21.24} + \underset{(23.20)}{33.07} \, g - \underset{(14.38)}{0.12} \, \text{DFR} - \underset{(9.41)}{0.19} \, \text{Tax Rate} - \underset{(6.98)}{4.88} \, \text{ROIC}$ | 23.7% |

---

### Market-wide Regressions of Multiples: Global Companies in January 2026
*T-statistics in brackets below coefficients*

| Regression | $R^2$ |
| :--- | :---: |
| $\text{PE} = \underset{(40.64)}{21.11} + \underset{(7.16)}{2.22} \, \text{Beta} + \underset{(18.23)}{21.49} \, g_{\text{EPS}} + \underset{(1.66)}{0.89} \, \text{Payout}$ | 10.3% |
| $\text{PEG} = \underset{(3.73)}{-0.12} + \underset{(1.20)}{0.56} \, \text{Payout} + \underset{(12.83)}{0.48} \ln(g_{\text{EPS}}) - \underset{(12.83)}{0.13} \, \text{Beta}$ | 41.4% |
| $\text{PBV} = \underset{(7.52)}{0.71} + \underset{(6.91)}{1.13} \, g_{\text{EPS}} - \underset{(2.59)}{0.12} \, \text{Beta} + \underset{(64.18)}{16.72} \, \text{ROE} - \underset{(1.86)}{0.11} \, \text{Payout Ratio}$ | 53.8% |
| $\text{EV/Invested Capital} = \underset{(159.95)}{4.67} + \underset{(13.36)}{1.53} \, g + \underset{(2.96)}{0.04} \, \text{ROIC} - \underset{(93.17)}{0.05} \, \text{DFR}$ | 44.5% |
| $\text{EV/Sales} = \underset{(59.84)}{5.44} + \underset{(17.34)}{4.97} \, g + \underset{(16.53)}{0.38} \, \text{Oper Margin} - \underset{(4.36)}{0.01} \, \text{DFR} - \underset{(21.18)}{0.07} \, \text{Tax rate}$ | 13.3% |
| $\text{EV/EBITDA} = \underset{(61.21)}{21.79} + \underset{(36.81)}{30.86} \, g - \underset{(22.87)}{0.13} \, \text{DFR} - \underset{(18.36)}{0.24} \, \text{Tax Rate} + \underset{(9.98)}{2.72} \, \text{ROIC}$ | 36.2% |

---

## Regressions Classified by Multiples

### Market-wide Regressions of Multiples: PE Ratios in January 2026
*T-statistics in brackets below coefficients*

| Regression | $R^2$ | Region |
| :--- | :---: | :--- |
| $\text{PE} = \underset{(12.20)}{13.12} + \underset{(10.0)}{10.52} \, \text{Beta} + \underset{(7.70)}{36.47} \, g_{\text{EPS}} + \underset{(6.89)}{8.46} \, \text{Payout}$ | 38.7% | US |
| $\text{PE} = \underset{(8.29)}{9.72} + \underset{(4.85)}{2.99} \, \text{Beta} + \underset{(11.95)}{49.82} \, g_{\text{EPS}} + \underset{(9.22)}{7.98} \, \text{Payout}$ | 20.1% | Europe |
| $\text{PE} = \underset{(5.78)}{4.51} + \underset{(3.50)}{4.28} \, \text{Beta} + \underset{(7.32)}{42.26} \, g_{\text{EPS}} + \underset{(9.05)}{10.46} \, \text{Payout}$ | 34.5% | Japan |
| $\text{PE} = \underset{(7.27)}{19.38} + \underset{(2.22)}{6.55} \, \text{Payout}$ *(no other variables significant)* | 3.4% | Aus, NZ & Canada |
| $\text{PE} = \underset{(10.35)}{14.47} - \underset{(1.33)}{0.51} \, \text{Beta} + \underset{(23.99)}{52.25} \, g_{\text{EPS}} + \underset{(3.24)}{2.22} \, \text{Payout}$ | 27.2% | Emerging Markets |
| $\text{PE} = \underset{(40.64)}{21.11} + \underset{(7.16)}{2.22} \, \text{Beta} + \underset{(18.23)}{21.49} \, g_{\text{EPS}} + \underset{(1.66)}{0.89} \, \text{Payout}$ | 10.3% | Global |

---

### Market-wide Regressions of Multiples: PEG Ratios in January 2026
*T-statistics in brackets below coefficients*

| Regression | $R^2$ | Region |
| :--- | :---: | :--- |
| $\text{PEG} = \underset{(1.94)}{-0.60} + \underset{(7.62)}{0.56} \, \text{Payout} - \underset{(14.72)}{1.48} \ln(g_{\text{EPS}}) + \underset{(1.86)}{0.23} \, \text{Beta}$ | 41.4% | US |
| $\text{PEG} = \underset{(2.77)}{-0.91} + \underset{(3.15)}{0.76} \, \text{Payout} - \underset{(11.09)}{1.57} \ln(g_{\text{EPS}})$ | 30.3% | Europe |
| $\text{PEG} = \underset{(2.45)}{-0.70} + \underset{(4.81)}{0.35} \, \text{Payout} - \underset{(12.49)}{1.19} \ln(g_{\text{EPS}}) + \underset{(2.68)}{0.23} \, \text{Beta}$ | 32.4% | Japan |
| $\text{PEG} = \underset{(4.50)}{-0.78} + \underset{(10.65)}{0.82} \, \text{Payout} - \underset{(30.50)}{1.43} \ln(g_{\text{EPS}}) - \underset{(1.95)}{0.09} \, \text{Beta}$ | 51.9% | Emerging Markets |
| $\text{PEG} = \underset{(3.33)}{-1.83} + \underset{(3.45)}{0.84} \, \text{Payout} - \underset{(10.76)}{1.74} \ln(g_{\text{EPS}}) + \underset{(2.05)}{0.54} \, \text{Beta}$ | 40.9% | Aus, NZ & Canada |
| $\text{PEG} = \underset{(3.73)}{-0.12} + \underset{(1.20)}{0.56} \, \text{Payout} + \underset{(12.83)}{0.48} \ln(g_{\text{EPS}}) - \underset{(12.83)}{0.13} \, \text{Beta}$ | 41.4% | Global |

---

### Market-wide Regressions of Multiples: PBV Ratios in January 2026
*T-statistics in brackets below coefficients*

| Regression | $R^2$ | Region |
| :--- | :---: | :--- |
| $\text{PBV} = \underset{(3.17)}{-0.79} - \underset{(0.53)}{0.47} \, g_{\text{EPS}} + \underset{(6.76)}{1.49} \, \text{Beta} + \underset{(34.45)}{20.90} \, \text{ROE} + \underset{(1.30)}{0.17} \, \text{Payout Ratio}$ | 66.2% | US |
| $\text{PBV} = \underset{(3.70)}{0.73} + \underset{(5.87)}{3.92} \, g_{\text{EPS}} + \underset{(1.38)}{0.13} \, \text{Beta} + \underset{(24.81)}{10.75} \, \text{ROE} - \underset{(2.43)}{0.25} \, \text{Payout Ratio}$ | 42.3% | Europe |
| $\text{PBV} = \underset{(2.63)}{-0.55} + \underset{(6.72)}{4.64} \, g_{\text{EPS}} + \underset{(3.84)}{0.38} \, \text{Beta} + \underset{(14.99)}{14.23} \, \text{ROE}$ | 44.1% | Japan |
| $\text{PBV} = \underset{(14.31)}{1.32} + \underset{(11.36)}{2.73} \, g_{\text{EPS}} + \underset{(8.04)}{0.43} \, \text{Beta} + \underset{(19.16)}{4.53} \, \text{ROE}$ | 26.3% | Emerging Markets |
| $\text{PBV} = \underset{(69.9)}{2.69} + \underset{(5.52)}{0.83} \, \text{ROE}$ *(other variables were not statistically significant)* | 1.1% | Aus, NZ & Canada |
| $\text{PBV} = \underset{(7.52)}{0.71} + \underset{(6.91)}{1.13} \, g_{\text{EPS}} - \underset{(2.59)}{0.12} \, \text{Beta} + \underset{(64.18)}{16.72} \, \text{ROE} - \underset{(1.86)}{0.11} \, \text{Payout Ratio}$ | 53.8% | Global |

---

### Market-wide Regressions of Multiples: EV to Invested Capital Ratios in January 2026
*T-statistics in brackets below coefficients*

| Regression | $R^2$ | Region |
| :--- | :---: | :--- |
| $\text{EV/Invested Capital} = \underset{(82.70)}{5.75} + \underset{(4.16)}{1.12} \, g + \underset{(0.24)}{0.01} \, \text{ROIC} - \underset{(44.71)}{0.06} \, \text{DFR}$ | 49.7% | US |
| $\text{EV/Invested Capital} = \underset{(67.88)}{4.46} + \underset{(2.92)}{0.90} \, g + \underset{(13.63)}{1.50} \, \text{ROIC} - \underset{(42.64)}{0.05} \, \text{DFR}$ | 51.3% | Europe |
| $\text{EV/Invested Capital} = \underset{(42.62)}{3.01} + \underset{(16.82)}{8.96} \, g + \underset{(4.57)}{0.16} \, \text{ROIC} - \underset{(27.22)}{0.04} \, \text{DFR}$ | 46.9% | Japan |
| $\text{EV/Invested Capital} = \underset{(98.22)}{3.42} + \underset{(20.69)}{2.74} \, g + \underset{(5.51)}{0.11} \, \text{ROIC} - \underset{(61.47)}{0.04} \, \text{DFR}$ | 48.8% | Emerging Markets |
| $\text{EV/Invested Capital} = \underset{(41.62)}{3.82} + \underset{(3.36)}{0.71} \, g + \underset{(1.47)}{0.11} \, \text{ROIC} - \underset{(23.35)}{0.04} \, \text{DFR}$ | 43.5% | Aus, NZ & Canada |
| $\text{EV/Invested Capital} = \underset{(159.95)}{4.67} + \underset{(13.36)}{1.53} \, g + \underset{(2.96)}{0.04} \, \text{ROIC} - \underset{(93.17)}{0.05} \, \text{DFR}$ | 44.5% | Global |

---

### Market-wide Regressions of Multiples: EV to Sales Ratios in January 2026
*T-statistics in brackets below coefficients*

| Regression | $R^2$ | Region |
| :--- | :---: | :--- |
| $\text{EV/Sales} = \underset{(32.41)}{6.77} + \underset{(11.21)}{9.51} \, g + \underset{(8.97)}{0.36} \, \text{Oper Margin} - \underset{(6.32)}{0.02} \, \text{DFR} - \underset{(10.58)}{0.12} \, \text{Tax rate}$ | 24.1% | US |
| $\text{EV/Sales} = \underset{(21.01)}{5.08} + \underset{(5.39)}{4.03} \, g + \underset{(6.95)}{2.99} \, \text{Oper Margin} - \underset{(7.18)}{0.02} \, \text{DFR} - \underset{(12.26)}{0.09} \, \text{Tax rate}$ | 14.2% | Europe |
| $\text{EV/Sales} = \underset{(13.12)}{2.48} + \underset{(16.88)}{11.54} \, g + \underset{(6.38)}{0.44} \, \text{Oper Margin} - \underset{(2.90)}{0.01} \, \text{DFR} - \underset{(5.06)}{0.03} \, \text{Tax rate}$ | 24.4% | Japan |
| $\text{EV/Sales} = \underset{(33.23)}{4.10} + \underset{(9.48)}{3.17} \, g + \underset{(5.95)}{0.65} \, \text{Oper Margin} - \underset{(3.38)}{0.01} \, \text{DFR} - \underset{(8.02)}{0.03} \, \text{Tax rate}$ | 5.4% | Emerging Markets |
| $\text{EV/Sales} = \underset{(7.93)}{2.71} + \underset{(7.70)}{6.07} \, g + \underset{(16.39)}{5.51} \, \text{Oper Margin} - \underset{(1.01)}{0.01} \, \text{DFR} - \underset{(2.06)}{0.02} \, \text{Tax rate}$ | 44.7% | Aus, NZ & Canada |
| $\text{EV/Sales} = \underset{(59.84)}{5.44} + \underset{(17.34)}{4.97} \, g + \underset{(16.53)}{0.38} \, \text{Oper Margin} - \underset{(4.36)}{0.01} \, \text{DFR} - \underset{(21.18)}{0.07} \, \text{Tax rate}$ | 13.3% | Global |

---

### Market-wide Regressions of Multiples: EV to EBITDA Ratios in January 2026
*T-statistics in brackets below coefficients*

| Regression | $R^2$ | Region |
| :--- | :---: | :--- |
| $\text{EV/EBITDA} = \underset{(43.19)}{18.82} + \underset{(23.04)}{39.30} \, g - \underset{(14.08)}{0.20} \, \text{DFR} + \underset{(3.19)}{1.77} \, \text{ROIC}$ | 45.9% | US |
| $\text{EV/EBITDA} = \underset{(28.40)}{18.15} + \underset{(13.96)}{35.25} \, g - \underset{(10.65)}{0.11} \, \text{DFR} - \underset{(5.19)}{0.12} \, \text{Tax Rate} + \underset{(5.06)}{2.29} \, \text{ROIC}$ | 26.2% | Europe |
| $\text{EV/EBITDA} = \underset{(20.89)}{10.94} + \underset{(8.71)}{35.22} \, g - \underset{(4.25)}{0.05} \, \text{DFR} + \underset{(2.99)}{1.22} \, \text{ROIC}$ | 6.7% | Japan |
| $\text{EV/EBITDA} = \underset{(35.57)}{21.24} + \underset{(23.20)}{33.07} \, g - \underset{(14.38)}{0.12} \, \text{DFR} - \underset{(9.41)}{0.19} \, \text{Tax Rate} - \underset{(6.98)}{4.88} \, \text{ROIC}$ | 23.7% | Emerging Markets |
| $\text{EV/EBITDA} = \underset{(12.01)}{19.04} + \underset{(5.66)}{16.95} \, g - \underset{(4.86)}{0.12} \, \text{DFR} - \underset{(2.71)}{0.14} \, \text{Tax Rate} + \underset{(2.03)}{1.43} \, \text{ROIC}$ | 17.9% | Aus, NZ & Canada |
| $\text{EV/EBITDA} = \underset{(61.21)}{21.79} + \underset{(36.81)}{30.86} \, g - \underset{(22.87)}{0.13} \, \text{DFR} - \underset{(18.36)}{0.24} \, \text{Tax Rate} + \underset{(9.98)}{2.72} \, \text{ROIC}$ | 36.2% | Global |

---

### Variable Definitions Reference

* $\text{ERP} =$ Total Equity Risk Premium for country in which company is incorporated
* $g_{\text{EPS}} =$ Expected growth rate in EPS for next 5 years (analyst estimates)
* $g =$ Expected growth rate in revenues for next 5 years (if not available, use $g_{\text{EPS}}$)
* $\text{Payout} = \text{Dividends} / \text{Earnings}$
* $\text{ROIC} = \text{Return on capital} = \text{EBIT}(1 - \text{tax rate}) / \text{Invested Capital}$
* $\text{Operating Margin} = \text{Pre-tax Operating Income} / \text{Sales}$
* $\text{Invested Capital} = \text{Book value of equity} + \text{Book value of debt} - \text{Cash}$
* $\text{ROE} = \text{Net Income} / \text{Book value of Equity}$
* $\text{Tax Rate} = \text{Effective tax rate} = \text{Taxes paid} / \text{Taxable Income}$
* $\text{DFR} = \text{Total Debt} / (\text{Total Debt} + \text{Market value of equity})$
* $\text{RIR} = \text{Reinvestment Rate} = (\text{Cap Ex} - \text{Depreciation} + \Delta\text{WC}) / (\text{EBIT}(1 - t))$
* $\text{WACC} = \text{Cost of capital in US dollars}$