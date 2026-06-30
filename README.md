# Investment Assessment — Direct-Equity Stake in a Distribution-Network Battery "Develop-and-Flip" Startup

> *Illustrative analysis — an independent rebuild of an unnamed founder's claims. No real company, person or transaction is identified; all monetary figures are illustrative placeholders. **Not investment advice; capital is at risk.***

**Headline recommendation: CONDITIONAL, PASS-LEANING — proceed to confirmatory due diligence; do NOT commit on the founders' figures alone.** We buy shares directly in one early-stage battery-developer startup. On our independent rebuild — valuing the company as a development platform on its **forward pipeline** — the deal is materially less attractive than presented and is **value-destructive at the central estimate**.

## At a glance

| Item | Assessment |
|---|---|
| **Expected return on our shares** | First-Chicago IRR ≈ **−2.6%** (MOIC ~0.88×) on our independent rebuild — Base **0.0%** (we get our money back via the 1× liquidation preference), Ideal +4.2%, Conservative **−15%** (a deep loss) |
| **Why so low** | The company is valued on its **forward pipeline** (~$7.2m Base exit equity), *below* the ~$10m post-money we pay — so our stake is under water and the preference merely returns our cost. The earlier ~4× profit multiple ($19.3m) overstated it. |
| **Biggest swing factor** | The **exit assumption** — pipeline depth at exit × discount rate (see the IC memo, Exhibit D) — now bigger than the gate rates |
| **When to sell (value ladder)** | **Sell at ready-to-build (R1).** Holding to build/operate grows the company (~$7m → ~$28m equity) but the capital raised dilutes our minority stake away (~14% → ~2%), turning a 21% return into a loss — see the [value ladder](IC_MEMO.md#6-valuation--deal-structure) |
| **Single biggest risk** | **Exit / buyer risk** — a flip with no buyer is stranded capital; buyers transact at 100 MW+, not 5 MW, and the "interested buyers" are non-binding |
| **Status** | Conditional / pass-leaning — commit only if the conditions in the IC memo are evidenced |

**→ [Read the full Investment Committee memo](IC_MEMO.md)** — recommendation, thesis, industry, valuation, returns, risks, exit, conditions, and exhibits.

**▶ Open the interactive model online:** [BESS Pipeline Valuation — live Excel workbook](https://1drv.ms/x/c/4486f9b7c333bd96/IQCSSeOA23OMS4zJdfkVXoeYASG_3AC1gFmTnfmMDz3hXkE?e=JalxsN) (recalculates in your browser) · no-click: [model results preview](financial_models/MODEL_PREVIEW.md) · [one-page dashboard (PDF)](outputs/dashboard.pdf).

## How the headline numbers are derived

Every figure traces input → formula → result inside the Excel model. Full data sourcing is in [IC_MEMO.md, Appendix A](IC_MEMO.md#appendix-a--methods--sources); the inputs (each with a source and a `provenance` tag) are in [`config/assumptions.yaml`](config/assumptions.yaml). The same formulas are reproduced cell-for-cell in [`src/valuation_engine.py`](src/valuation_engine.py) — an independent recomputation used only to **check** the workbook ties, not to produce it. (Function names below point into that reference.)

**Step 1 — Will a project succeed? (the three gates)**

| Result (Base) | Formula | Worked example | Code / source |
|---|---|---|---|
| Whole-funnel flip success ≈ **36.4%** | approval × grid connection × sale | 0.65 × 0.70 × 0.80 | `flip_success()`; `gates`, `scenarios` |
| Independent benchmark ≈ **44.8%** | same, with the public approval rate | 0.80 × 0.70 × 0.80 | `gates.development_approval.independent` |

> The founders' 40 / 65 / 80% are the **development-approval gate only** — not whole-funnel success.

**Step 2 — What % of the company do we get? (the cap table)**

| Result | Formula | Worked example | Code / source |
|---|---|---|---|
| Post-money = **$10.0m** | pre-money + our investment | 8.0 + 2.0 | `post_money`; `equity_deal` |
| Ownership at entry = **20.0%** | investment ÷ post-money | 2.0 ÷ 10.0 | `ownership_initial` |
| Diluted ownership = **14.4%** | entry % × (1 − option pool) × (1 − future-round dilution) | 0.20 × 0.90 × 0.80 | `ownership_diluted` |

**Step 3 — What is the company worth at exit? (forward-pipeline basis)**

| Result | Formula | Worked example | Code / source |
|---|---|---|---|
| Discount rate = **18.8%** | risk-free + risk premium | 0.048 + 0.140 | `discount_base`; live RBA rate (`rates.csv`) + `discount_rate` premium |
| Per-project rNPV | (blended RTB sale − dev cost) × flip success × 1 ÷ (1 + rate)^years | — | `per_project_rnpv_blended()` |
| Forward-pipeline rNPV | pipeline depth at exit × per-project rNPV | 25 × per-project | `forward_pipeline_rnpv()` |
| Company exit equity (Base) ≈ **$7.2m** | forward-pipeline rNPV + retained cash − debt | ≈ 2.4 + 4.8 − 0 | `exit_equity_value()` |

> rNPV = risk-adjusted net present value. "Retained cash" is realised profit not yet paid out — counted once, never at a multiple (the double-count guard).

**Step 4 — What do WE get back? (our shares)**

| Result | Formula | Worked example | Code / source |
|---|---|---|---|
| Our terminal proceeds (Base) | greater of: (1× preference × investment) **or** (diluted % × exit equity) | max(2.0, 0.144 × 7.2) → 2.0 | `investor_return()` |
| Our MOIC (per scenario) | our proceeds ÷ our investment | — | `investor_return()` |
| Our IRR (per scenario) | MOIC ^ (1 ÷ exit year) − 1 | …^(1 ÷ 5) − 1 | `investor_return()` |
| **Expected −2.6% / 0.88×** | First-Chicago: Σ (scenario proceeds × weight) ÷ investment, then annualise | weights 0.30 / 0.50 / 0.20 | `first_chicago()` |

> MOIC = multiple on invested capital. IRR = annualised return. We weight **proceeds**, not IRRs (a total-loss IRR of −100% can't be averaged linearly).

**Three inputs drive the result and are still `[[TO CONFIRM]]` placeholders:** pre-money ($8m), pipeline depth at exit (25 projects), and the interim-distribution fraction (0%). Each materially moves the answer — see [IC_MEMO.md, Exhibit D](IC_MEMO.md#exhibit-d--exit-value-sensitivity).

## The model is the Excel workbook

**The model is [`financial_models/BESS_Valuation.xlsx`](financial_models/BESS_Valuation.xlsx).** Open it and drive it by hand: change the **scenario switch** (`Scenarios` tab — `1` / `2` / `3` for Conservative / Base / Ideal), or edit any **blue** input cell on the **Inputs** tab, and the workbook recalculates. The **Checks** tab must read all-**OK** (the Cover carries the master check); the **Dashboard** tab is the one-page summary.

**Colour convention:** **blue** = an input you can change · **black** = a formula · **green** = a link to another sheet.

### Python is the data layer, not the model

The Python pipeline pulls and checks data; it does **not** own the workbook.

- **Data in** — `src/extract/*` and `src/refresh_model_inputs.py` pull the source inputs (AEMO ISP, CSIRO GenCost, RBA yields) into `data/processed/`, which the modeller links or pastes into the **Inputs** tab.
- **Independent check** — `src/valuation_engine.py` recomputes the same numbers cell-for-cell, used only to **confirm the workbook ties** (`make test`). It does not produce the model.
- **Hand-owned master** — there is **one** model file. A normal Python run writes nothing; Python never overwrites the master. Re-baseline it from Python only with `make rebuild-master`.

```bash
make install      # dependencies
make extract      # refresh source data (AEMO / CSIRO / RBA) -> data/processed/
make transform    # clean pipeline, gate stats, comps
make test         # pytest — recomputes the numbers and checks the master ties
make refresh      # OPTIONAL: push refreshed inputs into the master's blue cells (--write-master)
```

**To change an input:** edit its **blue** cell on the **Inputs** tab (then the workbook recalculates), or run `make extract transform` and copy the refreshed value from `data/processed/` into that cell.
