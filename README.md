# Investment Assessment — Proposed Limited-Partner Commitment to a Distribution-Network Battery Develop-and-Flip Fund

| | |
|---|---|
| **Prepared by** | Investment analysis (credit-risk lens) |
| **Date** | June 2026 |
| **Subject** | Independent assessment of a proposed limited-partner (LP) commitment to an illustrative develop-and-flip battery energy storage system (BESS) fund |
| **Recommendation** | **CONDITIONAL — proceed to confirmatory due diligence; do NOT commit on the manager's figures alone** |

> **Status & standing.** This is an **educational portfolio artefact** and an **independent rebuild** of an (unnamed) fund manager's projections — **not investment advice**. Every figure attributed to the manager is a forward-looking **claim to verify**; our independent public-data findings sit alongside. The fund and pipeline are treated as **illustrative**. Wholesale-investor context — read the Information Memorandum; **capital is at risk.** All figures must be independently re-verified before any decision. See [Disclaimer](#disclaimer). Methodology, data sources, and a fully reproducible model sit in the [appendix](#appendix--basis-of-analysis--how-to-reproduce). *Acronyms are spelled out on first use.*

---

> **▶ Open the interactive model online:** **[BESS Pipeline Valuation — live Excel workbook](https://1drv.ms/x/c/4486f9b7c333bd96/IQCSSeOA23OMS4zJdfkVXoeYASG_3AC1gFmTnfmMDz3hXkE?e=JalxsN)** — opens in Excel for the web and recalculates in your browser (no download). No-click alternatives: [model results preview](financial_models/MODEL_PREVIEW.md) · [one-page dashboard (PDF)](outputs/dashboard.pdf).

## 1. Recommendation (bottom line up front)

**Conditional. The opportunity is genuine, but on our independent rebuild it is materially less attractive than the manager presents, and the downside can impair capital. Do not commit on the projections.** Proceed to confirmatory due diligence and commit **only if** the manager evidences (1) a deep, contractually-progressing pool of buyers for ready-to-build (RTB) projects, (2) sub-5-megawatt (MW), per-state success rates that reconcile our ~45% independent estimate with their 65% base case, and (3) a survivable downside. Absent those, decline.

| Our independent view | The manager's claim |
|---|---|
| First-Chicago **expected investor internal rate of return (IRR) ≈ 13.7%** (multiple on invested capital, MOIC ~1.31×) | Headline scenario IRRs **10.7% / 19.4% / 23.8%** |
| **Conservative case loses capital** (IRR −3.3%, MOIC 0.93×) | Conservative case still positive (10.7%) |
| Independent cumulative success **~45%** | Base-case success **65%** |

*Basis — the full data-source-and-method table is in [`INDUSTRY_REPORT.md`](INDUSTRY_REPORT.md). In brief: the **45%** comes from public planning-approval and grid-connection data via a probability-of-default / survival method (0.80 × 0.70 × 0.80); the **IRRs** come from our model (risk-adjusted net present value + fund funnel + First-Chicago weighting); the manager's figures are stated claims to verify.*

**Stage choice:** the fund offers exposure mainly to *Stage 1 (develop-and-flip)*. On a risk-adjusted basis, the *own-and-operate (contracted)* stage is a better fit for patient private capital — among the standalone entry points it is the only one that stays positive in its downside (the fully-integrated develop-build-operate path also does, but locks capital up ~18 years; see [§5](#5-where-to-invest-across-the-value-chain)).

**Single biggest risk:** *exit / buyer risk* (a flip with no buyer is a stranded asset), followed by *development / approval risk* and *success-rate optimism*.

---

## 2. The opportunity — and the one reframe that changes the risk

The fund **develops ~5 MW distribution-connected (about 22-kilovolt, or 22 kV) batteries to shovel-ready (ready-to-build) status and sells them before construction**, across New South Wales (NSW), Victoria (VIC) and South Australia (SA), over a two-plus-one-year term. An investor would participate as a **limited partner**.

**The reframe that decides which risks matter:** because the fund **never operates the asset**, the merchant-price volatility that usually sinks battery storage on a private-equity (PE) screen **passes to the buyer**. Diligence must therefore ignore the long-run electricity-price debate and focus on the fund's *actual* risks — **can projects be approved and grid-connected on time (the survival curve), and will buyers pay the assumed ready-to-build prices, in volume, on schedule (the exit)?**

| | A normal battery-storage operator | **This fund (develop-and-flip, ready-to-build)** |
|---|---|---|
| What it does | Builds, then trades electricity ~20 years | **Develops to ready-to-build, sells before construction** |
| Main risk | **Merchant-price volatility** | **Development/approval + exit/buyer risk** |
| Return driver | Cash yield + asset value | The **development margin**, captured in 2–3 years |

---

## 3. Summary of findings

| # | Finding | Assessment |
|---|---|---|
| 1 | **Market is real, growing and policy-backed.** Coal retirement plus the renewables build-out create a structural firming gap; the growth stage is a *tailwind* for a develop-and-flip (more buyers), not the buy-and-hold "yellow flag." | ✅ Supportive |
| 2 | **The niche is plausibly defensible.** Large developers chase 100 MW-plus transmission projects, leaving ~5 MW distribution under-contested; sub-5 MW projects get an Australian Energy Market Operator (AEMO) registration exemption → faster approval. | ⚠️ Verify the white space is durable |
| 3 | **Execution (survival) — the manager's success rate looks optimistic.** Our independent public-data decomposition (planning ≈80% × connection ≈70% × sale ≈80%) = **~45% cumulative**, which sits **below** the manager's 65% base case and only just above their 40% conservative case. | 🔴 Key flag |
| 4 | **Exit market is deep but unproven for *this* product — and skewed to scale.** The deep-pocketed buyers (infrastructure funds, superannuation funds, the Clean Energy Finance Corporation/Energy Security Corporation, retailers) transact at **100 MW and above**; a single 5 MW asset is too small for them, so the natural buyers are a thinner pool (network companies, government programmes, aggregators). The "3 interested buyers" are **non-binding**. | 🔴 The decisive risk |
| 5 | **Economics are capital-light; the margin is the de-risking uplift.** Ready-to-build value is ~10–12% of built-asset value — confirming this is the development premium, not the build. Development cost ~$0.5m/project; the funnel widens as success falls (`started = target ÷ success`). | ✅ Coherent |
| 6 | **Independent returns are below the manager's, with a real loss case.** Expected IRR ~13.7% versus the manager's ~17.7%; the conservative case can lose capital. | 🔴 Decision-driving |

*Basis — each finding's data source, method and calculation are tabulated in [`INDUSTRY_REPORT.md`](INDUSTRY_REPORT.md) ("Where every figure comes from"). Headline methods: industry life-cycle model and Porter's Five Forces (Chartered Financial Analyst, or CFA, curriculum); probability-of-default / survival analysis (credit-risk practice) for the 45%; comparable-transactions evidence (energy trade press) for the buyer-size finding.*

Supporting visuals (independent model):

![Survival curve — independent vs the manager's base case](outputs/figures/survival_curve.png)
![Investor internal rate of return by scenario](outputs/figures/irr_by_scenario.png)

---

## 4. Returns — independent rebuild

Modelled bottom-up from public data (survival curve → fund funnel → fees and carried interest → investor IRR and MOIC), with scenarios driven by the **cumulative success rate** (the master driver) and weighted via the **First-Chicago** method.

| Scenario | Success rate | Projects started* | Investor MOIC (net) | Investor IRR (net) |
|---|---|---|---|---|
| Conservative | 40% | ~88 | **0.93×** | **−3.3%** |
| Base | 65% | ~54 | **1.38×** | **17.5%** |
| Ideal | 80% | ~44 | **1.68×** | **29.7%** |
| **First-Chicago expected** (30/50/20 weighting) | — | — | **~1.31×** | **~13.7%** |

\*To deliver the ~35-project target, the starting pipeline must widen as success falls — which is why a lower success rate also raises total development cost.

*Basis — **Data source:** model inputs in [`config/assumptions.yaml`](config/assumptions.yaml) plus the live risk-free rate from the Reserve Bank of Australia (RBA). **Method:** risk-adjusted net present value (rNPV) per project; a fund funnel; fees and carried interest; First-Chicago scenario weighting (CFA scenario analysis + PE/venture-capital practice). **Calculation:** each scenario's after-fee IRR weighted 30% / 50% / 20% → ≈ 13.7%; the conservative case's MOIC of 0.93× (below 1.0×) is a capital loss.*

**Key assumptions** *(manager claims unless noted):*

| Assumption | Value |
|---|---|
| Committed capital | ~$25m |
| Projects delivered / sold | 35 |
| Development cost | ~$0.5m per project (+ partial spend on dropouts) |
| Fund term | 2 + 1 years |
| Entry fee | 2% of committed capital |
| Management fee | 2% per year |
| Carried interest / hurdle | 20% carry over an 8% preferred return |
| Discount rate *(asset cross-checks)* | 18.8% = RBA 10-year Commonwealth Government Securities (CGS) yield 4.8% + 14.0% development risk premium |

**Ready-to-build sale price by state** *(manager claim — needs independent comparables):*

| State | Price per 5 MW project |
|---|---|
| New South Wales | $0.9m – $1.1m |
| Victoria | $0.8m – $1.0m |
| South Australia | $0.5m – $0.7m |

*Basis — the discount rate uses the **build-up method** (required return = risk-free rate + risk premium): the risk-free leg is the live RBA 10-year Commonwealth Government Securities yield (`data/processed/rates.csv`); the 14.0% premium is analyst judgement. All other rows are the manager's projections (claims to verify); the ready-to-build prices need independent comparable-transaction evidence.*

> **Read-through:** our rebuild is deliberately more conservative than the manager's (full development spend across the funnel; independent costs/prices; no credit for the optimistic 65% base). The result — **expected return below the manager's, and a downside that can return less than capital** — is the credit-style scepticism this decision requires.

---

## 5. Where to invest across the value chain

The same projects can be entered at several points on the chain — the standalone entry points along the infrastructure risk ladder (**development → construction → operation**), plus an **integrated** path that carries one project through all three. Compared as risk-adjusted, levered equity returns on one ~5 MW asset:

| Stage | Hold | Expected IRR | Expected MOIC | Downside IRR | Main risk |
|---|---|---|---|---|---|
| 1 — Develop & flip (sell ready-to-build) | ~3 years | **13.7%** | 1.31× | **−3.3%** | approvals + a buyer (can lose capital) |
| 2 — Build & sell | ~1.5 years | **25.9%** | 1.41× | **−18.2%** | construction + thin build margin |
| 3 — Own & operate (contracted) | ~15 years | **8.1%** | 2.41× | **+4.4%** | merchant price (steady if contracted) |
| 4 — Integrated (develop→build→operate) | ~18 years | **12.6%** | 4.57× | **+8.6%** | all risks stacked (development + construction + merchant), but no exit risk |

![Risk-return by stage](outputs/figures/stage_comparison.png)

**Recommendation by stage (for patient private capital):**

- **Stage 3 — own & operate (contracted): the natural core.** The only *standalone* stage positive in its downside; steady, long-dated yield; plays to the credit-risk edge (assessing the offtake counterparty is *serviceability analysis*). Avoid merchant-only operating.
- **Stage 1 — develop & flip: a smaller satellite,** only on the conditions in [§7](#7-conditions-to-commit--questions-for-the-manager).
- **Stage 2 — build & sell: skip as a standalone** — the highest *expected* return but the most fragile (a thin, merchant-dependent build margin; a heavy downside) and it needs construction expertise.
- **Stage 4 — integrated (develop → build → operate): a different business model.** Captures the whole value chain and removes exit risk; because you build at cost, operating returns are strong with a positive downside *if it reaches operation*. But it is the longest lock-up (~18 years), stacks all the risks, and only ~50% of starts reach operation. For a patient owner-operator, not a passive limited partner.
- **Alignment trap:** the manager keeps the best projects to operate and sells the rest — ask to co-invest in the ones they keep.

> **The sale-gated 65% success rate is a Stage-1 number.** The ~45% (independent) / 65% (manager) figure is the chance a project clears planning, connection *and* a sale — so it includes exit risk. Stage 2 and Stage 3 investors buy a project that has *already* cleared development (at market price), so they bear construction-completion (~90%) and merchant-price risk instead. The integrated **Stage 4 also runs development, but without the sale gate** — its survival is planning × connection (≈56%), because it keeps the asset rather than selling it. Each stage is priced at its own entry point, so the comparison stays like-for-like and the manager's 65% drives only the Stage 1 number.

*Basis — **Data source:** [`config/assumptions.yaml`](config/assumptions.yaml) (development cost, construction cost, operating revenue, debt terms) + the RBA risk-free rate. **Method:** levered equity IRR per stage — Stage 1 is the fund funnel; Stage 2 is a build-and-sell model risk-adjusted by completion probability; Stage 3 is a levered operating discounted-cash-flow (DCF) with low/base/high merchant-price scenarios. **Calculation:** full workings in [`financial_models/STAGE_COMPARISON.md`](financial_models/STAGE_COMPARISON.md). Figures are illustrative — the Stage 2 result is highly sensitive to the build margin.*

---

## 6. Key risks

| Risk | Severity | Why it matters here |
|---|---|---|
| **Exit / buyer risk** | **High** | The decisive risk. Buyers are non-binding, transact at 100 MW+ (not 5 MW), and the market leans to *contracted* assets, not raw ready-to-build. A flip with no buyer is stranded capital. |
| **Development / approval risk** | **High** | Planning + grid connection on time across three states; the master driver of returns via the success rate. |
| **Success-rate optimism** | **High** | The manager's 65% base case sits above our ~45% independent estimate; verify with sub-5 MW, per-state evidence. |
| **Policy dependency** | **Medium–High** | Buyer appetite rests on net-zero / state schemes and the sub-5 MW exemption; a mid-window change hits all projects at once. |
| **Concentration** | **Medium** | ~35 projects, one strategy, three states — correlated to a single policy/rule change. |
| **Fees & liquidity** | **Medium** | 2%/2%/20%-over-8% is a meaningful gross-to-net drag; two-plus-one-year lock-up with no early redemption. |
| **Alignment** | **Medium** | The manager plans to keep the "best" 5–10 projects to operate — confirm how "best" is selected so the flip pool isn't left the weaker assets. |

> Note what is **not** the main risk: **merchant-price volatility**, which passes to the buyer (the reframe in §2).

---

## 7. Conditions to commit & questions for the manager

**Commit only if all of the following are evidenced:**
1. **Exit depth & pricing** — at least 3–4 credible, *contractually-progressing* ready-to-build buyers and **independent comparables** supporting the assumed price per project (not merely "interested").
2. **Success rate** — sub-5 MW, per-state planning-approval and grid-connection data reconciling the 65% base case with our independent ~45%.
3. **Survivable downside** — the fee-adjusted conservative case stressed further (ready-to-build prices down 20–30%, success near ~45%) without impairing capital.
4. **Alignment** — a transparent rule for selecting the "keep-best 5–10" projects.

**Questions for the manager:**
- Historical/expected approval and connection success **by state**, specifically for **sub-5 MW** — with evidence?
- Of the "3 interested buyers," what is **contractual** (signed options/memoranda of understanding, price/terms)?
- The **bottom-up ~$0.5m/project** development-cost build-up?
- **Independent comparables** behind the ready-to-build prices ($0.5–1.1m/project)?
- The **net-of-all-fees** IRR and the **gross** IRR behind it?
- What happens to timeline and IRR if approvals slip **6–12 months**?
- The genuine downside — **can limited partners lose capital, and in which scenario?**

---

## Appendix — basis of analysis & how to reproduce

**Why this exists (portfolio note).** This repository demonstrates two interview-tested skills:

1. **Data engineering** — a configuration-driven, reproducible Python pipeline over free public Australian data (Reserve Bank of Australia; the Commonwealth Scientific and Industrial Research Organisation's GenCost report; the Australian Energy Market Operator; New South Wales / Victoria / South Australia planning portals; energy trade press), with verify-then-fallback and full source logging.
2. **Advanced financial modelling** — a formula-driven, institutional-standard Excel model that values the develop-and-flip pipeline and the **investor (limited-partner) return**, via a probability-of-default-style survival curve, per-project risk-adjusted net present value, a fund funnel with fees and carried interest, and First-Chicago scenario weighting.

The headline story: *applying credit-risk (probability-of-default / survival) discipline and institutional Excel standards to an infrastructure-development fund — independently rebuilding a manager's claims on fully public data.*

**Methodology (what the model computes).**
1. **Probability-of-default-style survival curve** — `cumulative probability of success = p(planning) × p(connection) × p(sale)` from public data; the independent ~45% is the model's own estimate, with the optimism gap versus the manager's base case flagged.
2. **Per-project risk-adjusted net present value** — `ready-to-build sale − development cost = margin`, `× cumulative success`, discounted (development cost only — the buyer funds construction).
3. **Fund funnel → investor return** — `started = target ÷ success`; development cost (full on delivered + partial on dropouts); fees (entry + management + carried interest over the hurdle); **investor IRR & MOIC** (closed-form over the effective hold).
4. **Scenario / First-Chicago** — Conservative / Base / Ideal, probability-weighted to an expected return.
5. **Cross-checks** — dollar-per-MW benchmark, venture-capital method, and ready-to-build-as-%-of-built (~10–12%).
6. **Three-stage value-chain comparison** (`src/stage_analysis.py`) — Stage 1 develop-and-flip, Stage 2 build-and-sell (levered, with completion risk), Stage 3 own-and-operate (levered operating discounted-cash-flow with merchant scenarios), each as a risk-adjusted equity return → see §5.

The Python `valuation_engine.py` reproduces the Excel workbook **cell-for-cell** (Base investor IRR 17.5% in both); a `formulas`-library recalculation confirms the model's master check reads **OK** with zero error cells.

**Methods & theory (CFA curriculum + real-world practice).** Every result uses a recognised technique, not a bespoke one — in plain terms:

| Technique | What it does (plain English) | Where it comes from |
|---|---|---|
| Industry life-cycle · Porter's Five Forces · a Political-Economic-Social-Technological-Legal-Environmental (PESTLE) scan | Judge the industry's growth stage, competition and outside forces | CFA — industry analysis |
| Private-equity / venture-capital deal screen | Score the deal like an infrastructure/PE investor: exit path, barriers to entry, capital intensity | Real-world PE practice |
| Discount rate = risk-free rate + risk premium | Required return = a safe government-bond yield + extra for development risk | CFA — required return / cost of capital |
| Risk-adjusted net present value | Future cash flows × the chance they happen, discounted to today's money | CFA (time value of money, expected value); used in pharmaceutical & infrastructure development |
| Probability-of-default-style survival curve | Multiply the chance of clearing each gate to get the overall success rate | Credit-risk practice (Basel framework, International Financial Reporting Standard 9) |
| Comparable transactions (dollar-per-MW) | Price the asset off what similar projects actually sold for | CFA — relative valuation; mergers-and-acquisitions practice |
| Scenario analysis + First-Chicago method | Run Conservative/Base/Ideal and weight them by likelihood into one expected number | CFA (scenario analysis); PE/venture-capital practice |
| Venture-capital method | Work back from the exit value at a target return to today's value | Real-world venture-capital practice |
| IRR, MOIC, fee & carried-interest waterfall | Investor return after fees and 20%-carry-over-an-8%-hurdle | PE fund economics; CFA return measures |

A full "Where every figure comes from (data, method, calculation)" table is in [`INDUSTRY_REPORT.md`](INDUSTRY_REPORT.md). Everything stays within methods a credit-risk, infrastructure or private-equity interviewer will recognise.

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
├── README.md                         # this assessment
├── COMMITTEE_REPORT.md               # formal investment-committee memo (recommendation + exhibits)
├── INDUSTRY_REPORT.md / SOURCES.md   # the industry analysis + auto-generated source log
├── Makefile / requirements.txt / LICENSE / .gitignore
├── config/                           # sources.yaml + assumptions.yaml (judgement inputs, sourced)
├── src/
│   ├── extract/ transform/ utils/    # the public-data pipeline (verify-then-fallback)
│   ├── valuation_engine.py           # Python reference of the model (validates it; powers figures)
│   ├── stage_analysis.py             # three-stage value-chain comparison (develop / build / operate)
│   ├── build_model.py                # builds the formula-driven .xlsx (15 tabs)
│   ├── refresh_model_inputs.py       # pushes CSV values into the model's input cells
│   ├── make_report.py                # figures + dashboard.pdf
│   └── export_model_preview.py       # writes financial_models/MODEL_PREVIEW.md
├── data/processed/                   # committed clean CSVs (pipeline, gate_stats, rtb_comps, costs, rates, market_demand, end_use, deal_sizes)
├── financial_models/BESS_Valuation.xlsx      # THE financial model (+ MODEL_PREVIEW.md, STAGE_COMPARISON.md)
├── notebooks/                        # 01_industry_analysis, 02_gate_probabilities
├── outputs/                          # dashboard.pdf + figures/
└── tests/test_data_validation.py
```

**Data sources (all free, public).** Logged honestly in [`SOURCES.md`](SOURCES.md): 🟢 *live download*, 🟡 *documented benchmark (verify)*, 📄 *reported (public sources — verify)*. The pipeline **never fabricates data** — it falls back to a documented benchmark and prints a manual-download instruction. Ready-to-build comparables rely on publicly reported deals (the richest paid deal databases — BloombergNEF, Enerdatics, Mergermarket — are out of scope) and currently mirror the manager's assumed prices, pending independent comparables.

**Excel model standards (house rules followed).** Built to the FAST / ICAEW / Macabacus / Operis conventions:

- Inputs → Calcs → Outputs zones; one master Timeline; one row, one calculation
- No hardcoded numbers in formulas; a single `CHOOSE` scenario switch (3 cases) with a live-case row
- Checks built alongside, with a master check on the Cover
- Colour code: blue = input, black = formula, green = cross-sheet link
- `INDEX-MATCH` not `VLOOKUP`; `IFERROR` on division; closed-form IRR (no volatile functions)
- An automated pre-handover scan enforces no long formulas and no nested `IF`s on calculation sheets

**The 15 tabs:** Cover · Contents · Change Log · Inputs · Timeline · Scenarios · Calc_Survival · Calc_Project_rNPV · Calc_Fund · Returns · Calc_CrossChecks · Sensitivity · Checks · Dashboard · Sources & Glossary.

**Who built what (integrity).** This repository is a **version-1 draft built by Claude Code** — the pipeline plumbing and the model scaffold (structure, formulas, checks). **The judgement inputs are the analyst's to own and defend**, and the manager's figures are claims to verify:

- the three scenario success rates (versus the independent ~45%)
- ready-to-build dollar-per-MW by state (need independent comparables)
- development cost per project; fees / carried interest / hurdle
- discount rate; cash-flow profile

These live in `config/assumptions.yaml` and on the model's Inputs/Scenarios tabs.

**Limitations.**

- Illustrative fund — an independent rebuild of a manager's claims, not an endorsement
- Benchmark fallbacks where a source blocked automated access
- Ready-to-build comparables are publicly reported deals only
- Representative 6-project pipeline, scaled up by the funnel
- Blended (not per-state) survival curve
- Closed-form investor IRR over an effective hold; annual timing

All deliberately left for the analyst's review pass.

---

## Disclaimer

This repository is an **educational portfolio artefact**. It is **not investment advice** and not financial product advice. It assesses an **illustrative** opportunity and is an **independent rebuild of an unnamed third-party manager's forward-looking claims**, which must be independently verified. The fund context is **wholesale-investor only — read the Information Memorandum; capital is at risk.** Data extraction respects each source's terms of use, `robots.txt`, and rate limits, and prefers official downloads/application programming interfaces over scraping. Licensed under the MIT licence (see `LICENSE`).
