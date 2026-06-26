# Model preview — direct-equity stake in a battery-developer startup (read-only snapshot)

> **GitHub does not render `.xlsx` files, and the workbook computes its values only when opened in Excel.** This page mirrors the model's key outputs so you can review the results here, with no software. Numbers are produced by `valuation_engine.py`, the cell-for-cell Python reference of the workbook ([`financial_models/BESS_Valuation.xlsx`](BESS_Valuation.xlsx)).

*We invest **directly as a shareholder** in one illustrative battery-developer startup (not as a fund LP). Independent rebuild of the founder's claims; several equity-deal terms are **placeholders to confirm**. Not investment advice. See the [repository README](../README.md).*

**Master check:** `OK`  ·  **Base discount rate (asset cross-checks):** 18.8% (RBA 10yr CGS 4.8% + 14.0% dev premium)  ·  **Active case shown:** Base

## Headline — expected return on OUR shares (First-Chicago)

| Metric | Value |
|---|---|
| Expected equity IRR on our shares | **7.6%** |
| Expected MOIC (multiple of money) | **1.44x** |
| Scenario IRR range | -100.0% … 30.2% |

> The Conservative case is a **total loss** (the company's net programme profit is negative, so its equity is worth ~0). This is the venture-style shape: a real chance of zero, a modest base case, and meaningful upside if approvals run hot.

## Our stake — the cap table (placeholders to confirm)

| Item | Value |
|---|---|
| Pre-money valuation `[[TO CONFIRM]]` | $8.0m |
| Our investment `[[TO CONFIRM]]` | $2.0m |
| Post-money (= pre + investment) | $10.0m |
| Ownership at entry (= investment ÷ post-money) | **20.0%** |
| Option pool `[[TO CONFIRM]]` | 10.0% |
| Future-round dilution `[[TO CONFIRM]]` | 20.0% |
| Ownership at exit (after dilution) | **14.4%** |
| Liquidation preference | 1× non-participating |

## Return on our shares, by scenario

| Scenario | Flip success | Company exit equity | Our proceeds | MOIC | IRR |
|---|---|---|---|---|---|
| Conservative | 22.4% | $0.0m | $0.0m | **0.00x** | **-100.0%** |
| Base | 36.4% | $19.3m | $2.8m | **1.39x** | **6.8%** |
| Ideal | 44.8% | $51.9m | $7.5m | **3.74x** | **30.2%** |

> *Our proceeds = the greater of our 1× liquidation preference or our diluted ownership × the company's exit equity value. Company exit equity value = the company's net programme profit × a platform exit multiple (4.0× `[[TO CONFIRM]]`), over a 5-year hold `[[TO CONFIRM]]`.*

## Survival gates — separate; flip success = their product

> The founder's **40 / 65 / 80%** are the **development-approval gate ONLY**. True develop-and-flip success = development approval × grid connection × sale — a multi-period survival / probability-of-default curve.

| Gate | Probability (public benchmark) | Cumulative survival |
|---|---|---|
| Development approval | 80.0% | 80.0% |
| Grid connection | 70.0% | 56.0% |
| Reach sale (flip exit) | 80.0% | 44.8% |

**At the founder's Base development-approval rate (65.0%), true flip success ≈ 65.0% × 70.0% × 80.0% = 36.4%** — far below the 65% headline. The gates beyond approval are not free; this drives the company's net programme profit and therefore its value.

## The company's development programme (Base scenario)

| Item | Value |
|---|---|
| Programme capital (illustrative) | $25.0m |
| Projects target (delivered & sold) | 35 |
| Projects started (funnel = target ÷ flip success) | 96 |
| Total development cost | $26.7m |
| Gross proceeds (RTB sales) | $31.5m |
| Net programme profit (gross − dev cost) | $4.8m |
| → Company exit equity value (× 4.0 platform multiple) | $19.3m |

*RTB prices (founder claim): NSW $1.0m · VIC $0.9m · SA $0.6m per 5 MW project. No fund fees or carry — we own shares directly.*

## Company-asset valuation cross-check (per representative pipeline)

| Method | Value |
|---|---|
| rNPV pipeline (Base) | $0.58m |
| $/MW benchmark (dev value) | $0.58m |
| VC method (today value) | $0.45m |
| **Range** | **$0.45m – $0.58m** (midpoint $0.53m) |

## Integrity checks

All **15** model checks pass → master check reads `OK`.

| Check | Result |
|---|---|
| gate probabilities in [0,1] | ✅ OK |
| flip cumulative <= each gate | ✅ OK |
| flip success = DA x conn x sale | ✅ OK |
| MW positive | ✅ OK |
| RTB sale values positive | ✅ OK |
| dev cost positive | ✅ OK |
| switch in 1..3 | ✅ OK |
| DA scenario monotonic | ✅ OK |
| ownership = investment / post-money | ✅ OK |
| post-money = pre-money + investment | ✅ OK |
| diluted ownership <= initial | ✅ OK |
| investor MOIC monotonic | ✅ OK |
| weights sum to 100% | ✅ OK |
| First-Chicago IRR within range | ✅ OK |
| every input has a source | ✅ OK |

## See the full model

- **Open the live workbook** (recalculates on open): [`BESS_Valuation.xlsx`](BESS_Valuation.xlsx) — Cover · Inputs · Timeline · Scenarios · Calc_Survival · Calc_Project_rNPV · Calc_Company · Cap table & Returns · Calc_CrossChecks · Sensitivity · Checks · Dashboard · Sources & Glossary.
- **One-page dashboard (PDF, renders in-browser):** [`../outputs/dashboard.pdf`](../outputs/dashboard.pdf)
- **Data lineage:** [`SOURCES_LOG.md`](SOURCES_LOG.md)  ·  **Value-chain comparison:** [`STAGE_COMPARISON.md`](STAGE_COMPARISON.md)
- **Notebooks (render in-browser with charts):** [`../notebooks/`](../notebooks/)

*This file is auto-generated by `src/export_model_preview.py` (run via `make report`). Do not edit by hand.*
