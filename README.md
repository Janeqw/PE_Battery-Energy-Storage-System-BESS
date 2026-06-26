# Investment Assessment — Direct-Equity Stake in a Distribution-Network Battery "Develop-and-Flip" Startup

> *Educational portfolio artefact — an independent rebuild of an unnamed founder's claims. **Not investment advice; capital is at risk.***

**Headline recommendation: CONDITIONAL, PASS-LEANING — proceed to confirmatory due diligence; do NOT commit on the founders' figures alone.** We buy shares directly in one early-stage battery-developer startup. On our independent rebuild — valuing the company as a development platform on its **forward pipeline** — the deal is materially less attractive than presented and is **value-destructive at the central estimate**.

## At a glance

| Item | Assessment |
|---|---|
| **Expected return on our shares** | First-Chicago IRR ≈ **−2.6%** (MOIC ~0.88×) on our independent rebuild — Base **0.0%** (we get our money back via the 1× liquidation preference), Ideal +4.2%, Conservative **−15%** (a deep loss) |
| **Why so low** | The company is valued on its **forward pipeline** (~$7.2m Base exit equity), *below* the ~$10m post-money we pay — so our stake is under water and the preference merely returns our cost. The earlier ~4× profit multiple ($19.3m) overstated it. |
| **Biggest swing factor** | The **exit assumption** — pipeline depth at exit × discount rate (see the IC memo, Exhibit D) — now bigger than the gate rates |
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
