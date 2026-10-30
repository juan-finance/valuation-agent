# Synthetic Rating & Cost of Debt Estimation

**Date updated:** 5-ene-26

*Reference source for spreads: [BondsOnline](http://www.bondsonline.com)*

> **Instructions & Setup:**
> - Please read the special cases worksheet before using this model.
> - Ensure the **Iteration** checkbox (under Calculation Options in Excel) is enabled.
> - *Troubleshooting note:* If `#REF!` errors appear, set the operating lease commitment question to **No**, and then reset it to **Yes**.

---

## 1. Model Inputs & Outputs

### Inputs

| Input Parameter | Value | Notes / Instructions |
| :--- | :---: | :--- |
| **Type of Firm** | **2** | `1` = Large manufacturing firm (Market cap > $5B)<br>`2` = Smaller or riskier firm (< $5B)<br>`3` = Financial service firm |
| **Operating Lease / Rental Commitments?** | **No** | Yes or No |
| **Current EBIT** | **$50.00** | Add back only long-term interest expense for financial firms |
| **Current Interest Expenses** | **$8.00** | Use only long-term interest expense for financial firms |
| **Long-Term Government Bond Rate** | **3.00%** | Risk-free benchmark rate ($R_f$) |

### Calculated Outputs

| Metric | Result | Calculation / Methodology |
| :--- | :---: | :--- |
| **Interest Coverage Ratio** | **6.25** | $\text{EBIT} / \text{Interest Expense} = \$50.00 / \$8.00$ |
| **Estimated Bond Rating** | **A2/A** | Matched via Type 2 table ($6.00 < 6.25 \le 7.50$) |
| **Estimated Default Spread** | **0.78%** | Default spread corresponding to A2/A rating |
| **Estimated Cost of Debt** | **3.78%** | $\text{Risk-free Rate} + \text{Default Spread} = 3.00\% + 0.78\%$ |

---

## 2. Rating & Default Spread Lookup Tables

### A. Large Non-Financial Service Firms (Type 1: Market Cap > $5 Billion)

| Interest Coverage Ratio ($>$) | Interest Coverage Ratio ($\le$) | Rating | Default Spread |
| :---: | :---: | :---: | :---: |
| $-100,000$ | $0.20$ | D2/D | 19.00% |
| $0.20$ | $0.65$ | C2/C | 16.00% |
| $0.65$ | $0.80$ | Ca2/CC | 12.61% |
| $0.80$ | $1.25$ | Caa/CCC | 8.85% |
| $1.25$ | $1.50$ | B3/B- | 5.09% |
| $1.50$ | $1.75$ | B2/B | 3.21% |
| $1.75$ | $2.00$ | B1/B+ | 2.75% |
| $2.00$ | $2.25$ | Ba2/BB | 1.84% |
| $2.25$ | $2.50$ | Ba1/BB+ | 1.38% |
| $2.50$ | $3.00$ | Baa2/BBB | 1.11% |
| $3.00$ | $4.25$ | A3/A- | 0.89% |
| $4.25$ | $5.50$ | A2/A | 0.78% |
| $5.50$ | $6.50$ | A1/A+ | 0.70% |
| $6.50$ | $8.50$ | Aa2/AA | 0.55% |
| $8.50$ | $100,000$ | Aaa/AAA | 0.40% |

---

### B. Smaller & Riskier Firms (Type 2: Market Cap < $5 Billion)

| Interest Coverage Ratio ($>$) | Interest Coverage Ratio ($\le$) | Rating | Default Spread |
| :---: | :---: | :---: | :---: |
| $-100,000$ | $0.50$ | D2/D | 19.00% |
| $0.50$ | $0.80$ | C2/C | 16.00% |
| $0.80$ | $1.25$ | Ca2/CC | 12.61% |
| $1.25$ | $1.50$ | Caa/CCC | 8.85% |
| $1.50$ | $2.00$ | B3/B- | 5.09% |
| $2.00$ | $2.50$ | B2/B | 3.21% |
| $2.50$ | $3.00$ | B1/B+ | 2.75% |
| $3.00$ | $3.50$ | Ba2/BB | 1.84% |
| $3.50$ | $4.00$ | Ba1/BB+ | 1.38% |
| $4.00$ | $4.50$ | Baa2/BBB | 1.11% |
| $4.50$ | $6.00$ | A3/A- | 0.89% |
| $6.00$ | $7.50$ | A2/A | 0.78% |
| $7.50$ | $9.50$ | A1/A+ | 0.70% |
| $9.50$ | $12.50$ | Aa2/AA | 0.55% |
| $12.50$ | $100,000$ | Aaa/AAA | 0.40% |

---

### C. Financial Service Firms (Type 3: Long-Term Interest Coverage)

| Long-Term Interest Coverage Ratio ($>$) | Long-Term Interest Coverage Ratio ($\le$) | Rating | Default Spread |
| :---: | :---: | :---: | :---: |
| $-100,000$ | $0.05$ | D2/D | 19.00% |
| $0.05$ | $0.10$ | C2/C | 16.00% |
| $0.10$ | $0.20$ | Ca2/CC | 12.61% |
| $0.20$ | $0.30$ | Caa/CCC | 8.85% |
| $0.30$ | $0.40$ | B3/B- | 5.09% |
| $0.40$ | $0.50$ | B2/B | 3.21% |
| $0.50$ | $0.60$ | B1/B+ | 2.75% |
| $0.60$ | $0.75$ | Ba2/BB | 1.84% |
| $0.75$ | $0.90$ | Ba1/BB+ | 1.38% |
| $0.90$ | $1.20$ | Baa2/BBB | 1.11% |
| $1.20$ | $1.50$ | A3/A- | 0.89% |
| $1.50$ | $2.00$ | A2/A | 0.78% |
| $2.00$ | $2.50$ | A1/A+ | 0.70% |
| $2.50$ | $3.00$ | Aa2/AA | 0.55% |
| $3.00$ | $100,000$ | Aaa/AAA | 0.40% |