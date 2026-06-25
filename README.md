# Investment Committee Memo — Proposed LP Commitment to a Distribution-BESS Develop-and-Flip Fund

| | |
|---|---|
| **To** | Investment Committee / Family Trust trustees |
| **From** | Investment Analysis (credit-risk lens) |
| **Date** | 25 June 2026 |
| **Re** | Proposed LP commitment to the **Boman BESS Development Fund** — *independent assessment* |
| **Recommendation** | **CONDITIONAL — proceed to confirmatory due diligence; do NOT commit on the manager's figures alone** |

> **Status & standing.** This is an **educational portfolio artefact** and an **independent rebuild** of the manager's deck — **not investment advice**. Every figure attributed to the manager (Boman) is a forward-looking **claim to verify**; our independent public-data findings sit alongside. The fund and pipeline are treated as **illustrative**. Wholesale-investor context — read the Information Memorandum; **capital is at risk.** All figures must be independently re-verified before any decision. See [Disclaimer](#disclaimer). Methodology and a fully reproducible model sit in the [appendix](#appendix--basis-of-analysis--how-to-reproduce).

---

> **▶ Open the interactive model online:** **[BESS Pipeline Valuation — live Excel workbook](https://1drv.ms/x/c/4486f9b7c333bd96/IQCSSeOA23OMS4zJdfkVXoeYASG_3AC1gFmTnfmMDz3hXkE?e=JalxsN)** — opens in Excel for the web and recalculates in your browser (no download). No-click alternatives: [model results preview](financial_models/MODEL_PREVIEW.md) · [one-page dashboard (PDF)](outputs/dashboard.pdf).

## 1. Recommendation (bottom line up front)

**Conditional. The opportunity is genuine, but on our independent rebuild it is materially less attractive than the manager presents, and the downside can impair capital. Do not commit on the deck.** Proceed to confirmatory due diligence and commit **only if** the manager evidences (1) a deep, contractually-progressing **RTB buyer pool**, (2) **sub-5 MW, per-state success rates** that reconcile our ~45% independent estimate with their 65% base, and (3) a **survivable downside**. Absent those, decline.

| Our independent view | The manager's claim |
|---|---|
| First-Chicago **expected investor IRR ≈ 13.7%** (MOIC ~1.31x) | Headline scenario IRRs **10.7% / 19.4% / 23.8%** |
| **Conservative case loses capital** (IRR −3.3%, MOIC 0.93x) | Conservative case still positive (10.7%) |
| Independent cumulative success **~45%** | Base-case success **65%** |

**Single biggest risk:** *exit / buyer risk* (a flip with no buyer is a stranded asset), followed by *development / approval risk* and *success-rate optimism*.

---

## 2. The opportunity — and the one reframe that changes the risk

The fund **develops ~5 MW distribution-connected (≈22 kV) batteries to shovel-ready (RTB / development rights) and sells them before construction**, across NSW, VIC and SA, over a 2+1-year term. We would participate as a **limited partner**.

**The reframe that decides which risks matter:** because the fund **never operates the asset**, the merchant-price volatility that usually sinks BESS on a PE screen **passes to the buyer**. Our diligence must therefore ignore the long-run electricity-price debate and focus on the fund's *actual* risks — **can projects be approved and grid-connected on time (the survival curve), and will buyers pay the assumed RTB prices, in volume, on schedule (the exit)?**

| | A normal BESS operator | **This fund (develop-and-flip RTB)** |
|---|---|---|
| What it does | Builds + trades electricity ~20 yrs | **Develops to RTB, sells before construction** |
| Main risk | **Merchant-price volatility** | **Development/approval + exit/buyer risk** |
| Return driver | Cash yield + asset value | The **development margin**, captured in 2–3 yrs |

---

## 3. Summary of findings

| # | Finding | Assessment |
|---|---|---|
| 1 | **Market is real, growing and policy-backed.** Coal retirement + renewables build-out create a structural firming gap; growth-stage is a *tailwind* for a develop-and-flip (more buyers), not the buy-and-hold "yellow flag." | ✅ Supportive |
| 2 | **The niche is plausibly defensible.** Large developers chase 100 MW+ transmission, leaving ~5 MW distribution under-contested; **sub-5 MW projects get an AEMO registration exemption** → faster approval. | ⚠️ Verify the white space is durable |
| 3 | **Execution (survival) — the manager's success rate looks optimistic.** Our independent public-data decomposition (planning ≈80% × connection ≈70% × sale ≈80%) = **~45% cumulative**, which sits **below** the manager's 65% base and only just above their 40% conservative case. | 🔴 Key flag |
| 4 | **Exit market is deep but unproven for *this* product.** Buyers (IPPs, infra & super funds, CEFC/ESC, retailers) are active — but the "3 interested buyers" are **non-binding**, and capital increasingly pays for *contracted, construction-ready* assets, whereas this fund sells *earlier-stage, uncontracted RTB*. | 🔴 The decisive risk |
| 5 | **Economics are capital-light and the margin is the de-risking uplift.** RTB is ~10–12% of built-asset value — confirming this is the development premium, not the build. Dev cost ~$0.5m/project; the funnel widens as success falls (`started = target ÷ success`). | ✅ Coherent |
| 6 | **Independent returns are below the manager's, with a real loss case.** Expected IRR ~13.7% vs the deck's ~17.7%; the conservative case can lose capital. | 🔴 Decision-driving |

Supporting visuals (independent model):

![Survival curve — independent vs Boman Base](outputs/figures/survival_curve.png)
![Investor IRR by scenario](outputs/figures/irr_by_scenario.png)

---

## 4. Returns — independent rebuild

Modelled bottom-up from public data (survival curve → fund funnel → fees/carry → investor IRR/MOIC), scenarios driven by the **cumulative success rate** (the master driver) and weighted via the **First-Chicago** method.

| Scenario | Success rate | Projects started* | Investor MOIC (net) | Investor IRR (net) |
|---|---|---|---|---|
| Conservative | 40% | ~88 | **0.93x** | **−3.3%** |
| Base | 65% | ~54 | **1.38x** | **17.5%** |
| Ideal | 80% | ~44 | **1.68x** | **29.7%** |
| **First-Chicago expected** (30/50/20) | — | — | **~1.31x** | **~13.7%** |

\*To deliver the ~35-project target, the starting pipeline must widen as success falls — which is why a lower success rate also raises total development cost.

**Key assumptions** *(manager claims unless noted):*

| Assumption | Value |
|---|---|
| Committed capital | ~$25m |
| Projects delivered / sold | 35 |
| Development cost | ~$0.5m per project (+ partial spend on dropouts) |
| Fund term | 2 + 1 years |
| Entry fee | 2% of committed capital |
| Management fee | 2% p.a. |
| Carry / hurdle | 20% carry over an 8% preferred return |
| Discount rate *(asset cross-checks)* | 18.8% = RBA 10yr CGS 4.8% + 14.0% development premium |

**RTB sale price by state** *(manager claim — needs independent comps):*

| State | Price per 5 MW project |
|---|---|
| NSW | $0.9m – $1.1m |
| VIC | $0.8m – $1.0m |
| SA | $0.5m – $0.7m |

> **Read-through:** our rebuild is deliberately more conservative than the deck (full development spend across the funnel; independent costs/prices; no credit for the optimistic 65% base). The result — **expected return below the manager's, and a downside that can return less than capital** — is the credit-style scepticism this decision requires.

---

## 5. Key risks

| Risk | Severity | Why it matters here |
|---|---|---|
| **Exit / buyer risk** | **High** | The decisive risk. Buyers are non-binding and the market leans to *contracted* assets, not raw RTB. A flip with no buyer is stranded capital. |
| **Development / approval risk** | **High** | Planning + grid connection on time across three states; the master driver of returns via the success rate. |
| **Success-rate optimism** | **High** | The deck's 65% base sits above our ~45% independent estimate; verify with sub-5 MW, per-state evidence. |
| **Policy dependency** | **Medium–High** | Buyer appetite rests on net-zero / state schemes and the sub-5 MW exemption; a mid-window change hits all projects at once. |
| **Concentration** | **Medium** | ~35 projects, one strategy, three states — correlated to a single policy/rule change. |
| **Fees & liquidity** | **Medium** | 2/2/20-over-8% is a meaningful gross-to-net drag; 2+1-year lock-up with no early redemption. |
| **Alignment** | **Medium** | The manager plans to keep the "best" 5–10 projects to operate — confirm how "best" is selected so the flip pool isn't left the weaker assets. |

> Note what is **not** the main risk: **merchant-price volatility**, which passes to the buyer (the reframe in §2).

---

## 6. Conditions to commit & questions for the manager

**Commit only if all of the following are evidenced:**
1. **Exit depth & pricing** — ≥3–4 credible, *contractually-progressing* RTB buyers and **independent comps** supporting the assumed $/project (not merely "interested").
2. **Success rate** — sub-5 MW, per-state planning-approval and grid-connection data reconciling the 65% base with our independent ~45%.
3. **Survivable downside** — the fee-adjusted conservative case stressed further (RTB prices −20–30%, success near ~45%) without impairing capital.
4. **Alignment** — a transparent rule for selecting the "keep-best 5–10" projects.

**Questions for the manager (IC-style):**
- Historical/expected approval and connection success **by state**, specifically for **sub-5 MW** — with evidence?
- Of the "3 interested buyers," what is **contractual** (signed options/MOUs, price/terms)?
- The **bottom-up $0.5m/project** development-cost build-up?
- **Independent comps** behind the RTB prices ($0.5–1.1m/project)?
- The **net-of-all-fees** IRR and the **gross** IRR behind it?
- What happens to timeline/IRR if approvals slip **6–12 months**?
- The genuine downside — **can LPs lose capital, and in which scenario?**

---

## Appendix — basis of analysis & how to reproduce

**Why this exists (portfolio note).** This repository demonstrates two interview-tested skills:

1. **Data engineering** — a config-driven, reproducible Python pipeline over free public Australian data (RBA, CSIRO GenCost, AEMO, NSW/VIC/SA planning, trade press), with verify-then-fallback and full source logging.
2. **Advanced financial modelling** — a formula-driven, institutional-standard Excel model that values the develop-and-flip pipeline and the **investor (LP) return**, via a PD-style survival curve, per-project rNPV, a fund funnel with fees and carry, and First-Chicago scenario weighting.

The headline story: *applying credit-risk (PD / survival) discipline and institutional Excel standards to an infrastructure-development fund — independently rebuilding a manager's claims on fully public data.*

**Methodology (what the model computes).**
1. **PD-style survival curve** — `cumulative P(success) = p(planning) × p(connection) × p(sale)` from public data; the **independent ~45%** is the model's own estimate, with the optimism gap vs the manager's base flagged.
2. **Per-project rNPV** — `RTB sale − development cost = margin`, `× cumulative success`, discounted (development cost only — the buyer funds construction).
3. **Fund funnel → investor return** — `started = target ÷ success`; dev cost (full on delivered + partial on dropouts); fees (entry + management + carry over hurdle); **investor IRR & MOIC** (closed-form over the effective hold).
4. **Scenario / First-Chicago** — Conservative / Base / Ideal, probability-weighted to an expected return.
5. **Cross-checks** — $/MW benchmark, VC method, and RTB-as-%-of-built (~10–12%).

The Python `valuation_engine.py` reproduces the Excel workbook **cell-for-cell** (Base investor IRR 17.5% in both); a `formulas`-library recalc confirms the model's master check reads **OK** with zero error cells.

**Methods & theory (CFA curriculum + real-world practice).** Every result uses a recognised technique, not a bespoke one — in plain terms:

| Technique | What it does (plain English) | Where it comes from |
|---|---|---|
| Life-cycle · Porter's Five Forces · PESTLE | Judge the industry's growth stage, competition and outside forces | CFA — industry analysis |
| PE / VC deal screen | Score the deal like an infra/PE investor: exit path, barriers to entry, capital intensity | Real-world PE practice |
| Discount rate = risk-free + risk premium | Required return = a safe government-bond yield + extra for development risk | CFA — required return / cost of capital |
| Risk-adjusted NPV (rNPV) | Future cash flows × the chance they happen, discounted to today's money | CFA (time value of money, expected value); used in pharma & infrastructure development |
| PD-style survival curve | Multiply the chance of clearing each gate to get the overall success rate | Credit-risk practice (Basel, IFRS 9 probability-of-default) |
| Comparable transactions ($/MW) | Price the asset off what similar projects actually sold for | CFA — relative valuation; M&A practice |
| Scenario analysis + First-Chicago method | Run Conservative/Base/Ideal and weight them by likelihood into one expected number | CFA (scenario analysis); PE/VC practice |
| VC method | Work back from the exit value at a target return to today's value | Real-world VC practice |
| IRR, MOIC, fee & carry waterfall | Investor return after fees and 20%-carry-over-an-8%-hurdle | PE fund economics; CFA return measures |

Everything stays within methods a credit-risk, infrastructure or private-equity interviewer will recognise.

**Quick start.**
```bash
make install      # pip install -r requirements.txt (+ playwright chromium if used)
make all          # extract -> transform -> refresh model inputs -> export report
make test         # pytest
```
Then open `financial_models/BESS_Valuation.xlsx` (recalculates on open; Cover master check should read **OK**). Industry write-up: [`INDUSTRY_REPORT.md`](INDUSTRY_REPORT.md).

**Viewing the model — no software needed.** GitHub does not render `.xlsx` files inline, and the workbook computes its values only when opened in Excel, so clicking the spreadsheet on GitHub offers a download rather than a preview. To review the results in the browser:

- 📄 **Model results as a web page (recommended):** [`financial_models/MODEL_PREVIEW.md`](financial_models/MODEL_PREVIEW.md) — every key output rendered as Markdown tables, GitHub-native, auto-generated to match the workbook.
- 📊 **One-page dashboard (PDF):** [`outputs/dashboard.pdf`](outputs/dashboard.pdf) — GitHub renders PDFs in-browser.
- 📈 **Analysis with charts:** the executed notebooks in [`notebooks/`](notebooks/) render inline on GitHub.
- 🖥️ **Open the live spreadsheet in your browser** (Excel for the web — recalculates, no download): **[BESS Pipeline Valuation — interactive workbook](https://1drv.ms/x/c/4486f9b7c333bd96/IQCSSeOA23OMS4zJdfkVXoeYASG_3AC1gFmTnfmMDz3hXkE?e=JalxsN)**. *(Alternative, once the repo is public: the Microsoft Office viewer on the raw file URL — `https://view.officeapps.live.com/op/view.aspx?src=https://raw.githubusercontent.com/Janeqw/PE_Battery-Energy-Storage-System-BESS/main/financial_models/BESS_Valuation.xlsx`.)*

**Repository structure.**
```
PE_Battery-Energy-Storage-System-BESS/
├── README.md                         # this IC memo
├── INDUSTRY_REPORT.md / SOURCES.md   # the industry analysis + auto-generated source log
├── Makefile / requirements.txt / LICENSE / .gitignore
├── config/                           # sources.yaml + assumptions.yaml (judgement inputs, sourced)
├── src/
│   ├── extract/ transform/ utils/    # the public-data pipeline (verify-then-fallback)
│   ├── valuation_engine.py           # Python reference of the model (validates it; powers figures)
│   ├── build_model.py                # builds the formula-driven .xlsx (15 tabs)
│   ├── refresh_model_inputs.py       # pushes CSV values into the model's input cells
│   └── make_report.py                # figures + dashboard.pdf
├── data/processed/                   # committed clean CSVs (pipeline, gate_stats, rtb_comps, costs, rates)
├── financial_models/BESS_Valuation.xlsx      # THE financial model (+ MODEL_PREVIEW.md)
├── notebooks/                        # 01_industry_analysis, 02_gate_probabilities
├── outputs/                          # dashboard.pdf + figures/
└── tests/test_data_validation.py
```

**Data sources (all free, public).** Logged honestly in [`SOURCES.md`](SOURCES.md): 🟢 *live download* vs 🟡 *documented benchmark / manager claim (verify)*. The pipeline **never fabricates data** — it falls back to a documented benchmark and prints a manual-download instruction. RTB comps rely on publicly reported deals (paid databases — BNEF, Enerdatics, Mergermarket — out of scope) and currently mirror the manager's assumed prices, pending independent comps.

**Excel model standards (house rules followed).** Built to FAST / ICAEW / Macabacus / Operis conventions:

- Inputs → Calcs → Outputs zones; one master Timeline; one row, one calculation
- No hardcoded numbers in formulas; a single `CHOOSE` scenario switch (3 cases) with a live-case row
- Checks built alongside, with a master check on the Cover
- Colour code: blue = input, black = formula, green = cross-sheet link
- `INDEX-MATCH` not `VLOOKUP`; `IFERROR` on division; closed-form IRR (no volatile functions)
- An automated pre-handover scan enforces no long formulas and no nested IFs on calc sheets

**The 15 tabs:** Cover · Contents · Change Log · Inputs · Timeline · Scenarios · Calc_Survival · Calc_Project_rNPV · Calc_Fund · Returns · Calc_CrossChecks · Sensitivity · Checks · Dashboard · Sources & Glossary.

**Who built what (integrity).** This repo is a **v1 draft built by Claude Code** — the pipeline plumbing and the model scaffold (structure, formulas, checks). **The judgement inputs are the analyst's to own and defend**, and the manager's deck figures are claims to verify:

- the three scenario success rates (vs the independent ~45%)
- RTB $/MW by state (need independent comps)
- dev cost per project; fees / carry / hurdle
- discount rate; cash-flow profile

These live in `config/assumptions.yaml` and on the model's Inputs/Scenarios tabs.

**Limitations.**

- Illustrative fund — an independent rebuild of a manager's claims, not an endorsement
- Benchmark fallbacks where a source blocked automated access
- RTB comps are publicly reported deals only
- Representative 6-project pipeline, scaled up by the funnel
- Blended (not per-state) survival curve
- Closed-form investor IRR over an effective hold; annual timing

All deliberately left for the analyst's review pass.

---

## Disclaimer

This repository is an **educational portfolio artefact**. It is **not investment advice** and not financial product advice. It assesses an **illustrative** opportunity and is an **independent rebuild of a third-party manager's forward-looking claims** (the Boman BESS Development Fund), which must be independently verified. The fund context is **wholesale-investor only — read the Information Memorandum; capital is at risk.** Data extraction respects each source's terms of use, `robots.txt`, and rate limits, and prefers official downloads/APIs over scraping. Licensed under MIT (see `LICENSE`).
