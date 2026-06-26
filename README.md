# Investment Assessment — Limited-Partner Commitment to a Distribution-Network Battery "Develop-and-Flip" Fund

> *Educational portfolio artefact — an independent rebuild of an unnamed manager's claims. **Not investment advice; capital is at risk.***

**Headline recommendation: CONDITIONAL — proceed to confirmatory due diligence; do NOT commit on the manager's figures alone.** On our independent rebuild the deal is materially less attractive than presented, and the downside can impair capital.

## At a glance

| Item | Assessment |
|---|---|
| **Expected return** | Investor IRR ≈ **0.8%** (MOIC ~1.03×) on our independent rebuild — Base 4.8%, Ideal 18.3%, Conservative **−17.6%** (a capital loss) |
| **Single biggest risk** | **Exit / buyer risk** — a flip with no buyer is stranded capital; buyers transact at 100 MW+, not 5 MW, and the "interested buyers" are non-binding |
| **Status** | Conditional / pass-leaning — commit only if the conditions in the IC memo are evidenced |

**→ [Read the full Investment Committee memo](IC_MEMO.md)** — recommendation, thesis, industry, valuation, returns, risks, exit, conditions, and exhibits.

**▶ Open the interactive model online:** [BESS Pipeline Valuation — live Excel workbook](https://1drv.ms/x/c/4486f9b7c333bd96/IQCSSeOA23OMS4zJdfkVXoeYASG_3AC1gFmTnfmMDz3hXkE?e=JalxsN) (recalculates in your browser) · no-click: [model results preview](financial_models/MODEL_PREVIEW.md) · [one-page dashboard (PDF)](outputs/dashboard.pdf).

## How to reproduce the model

```bash
make install      # pip install -r requirements.txt (+ playwright chromium if used)
make all          # extract -> transform -> refresh model inputs -> export report
make test         # pytest
```

Then open `financial_models/BESS_Valuation.xlsx` (recalculates on open; Cover master check should read **OK**).
