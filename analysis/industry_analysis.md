# Industry Analysis — Australian Distribution-Network BESS Development Rights (RTB)

**An independent industry analysis of the market the Boman BESS Development Fund actually sells into — shovel-ready (RTB) development rights for standalone ~5 MW distribution-connected batteries across NSW, VIC and SA — read through a *develop-and-flip* lens, to frame an LP commitment by the family trust.**

> *Educational portfolio artefact. Not investment advice (we are not licensed advisers). Figures reflect Australian conditions as at mid-2026 and are illustrative — they must be re-verified before any decision. Every figure attributed to Boman is the manager's own forward-looking projection and is labelled "(Boman claim — verify)"; independent findings are tagged to source (AEMO / CSIRO / RBA / NSW–VIC–SA planning portals). Currency: AUD.*

---

## Contents

1. [Summary + the develop-and-flip reframe](#1-summary--the-develop-and-flip-reframe)
2. [Market boundary — exactly what we're analysing](#2-market-boundary--exactly-what-were-analysing)
3. [Market sizing — top-down, bottom-up, triangulation](#3-market-sizing--top-down-bottom-up-triangulation)
4. [Life cycle — growth stage, and why it's a tailwind here](#4-life-cycle--growth-stage-and-why-its-a-tailwind-here)
5. [Porter's Five Forces — on the RTB market](#5-porters-five-forces--on-the-rtb-market)
6. [PESTLE — policy dependency and the sub-5 MW exemption](#6-pestle--policy-dependency-and-the-sub-5-mw-exemption)
7. [PE / fund screen — adapted for develop-and-flip](#7-pe--fund-screen--adapted-for-develop-and-flip)
8. [Buyer landscape & exit path — the decisive section](#8-buyer-landscape--exit-path--the-decisive-section)
9. [Competitive landscape — who else develops in the 5 MW niche](#9-competitive-landscape--who-else-develops-in-the-5-mw-niche)
10. [Verdict — the single biggest risk](#10-verdict--the-single-biggest-risk)

> **How this fits the repo.** This is the deeper Stage-01 industry-analysis deliverable; the board-facing summary is [`INDUSTRY_REPORT.md`](../INDUSTRY_REPORT.md). The valuation rebuild (rNPV + survival curve + First Chicago) is a separate workstream — see [`model/`](../model/) and the notebooks.

---

## 1. Summary + the develop-and-flip reframe

**What we are analysing.** Not whether to *build and operate* batteries, but whether the family trust should commit as an **LP** to a fund that **develops ~5 MW distribution-connected battery projects to shovel-ready (RTB) and sells the project companies before construction.** The fund never operates an asset, never trades electricity, and is gone before the battery is built.

**The one reframe that decides everything.** The famous problem that sinks BESS on the classic PE screen — *merchant, volatile electricity revenue* — **largely does not apply to this fund**, because it sells before any electricity is traded. **Merchant-price risk passes to the buyer.** That single move changes which risks matter:

| | A normal BESS operator | **The Boman fund (develop-and-flip RTB)** |
|---|---|---|
| What it does | Builds batteries, sells electricity for ~20 years | **Develops** sites to shovel-ready (RTB), then **sells the project companies** |
| Holds the asset? | Yes | **No — sells before construction** |
| Main risk | **Merchant-price risk** (volatile electricity prices) | **Development/approval risk + exit/buyer risk** |
| Who bears merchant risk | The operator | **The buyer** of the RTB project |
| Horizon | 10–15+ years | **2+1 years** |

So the whole analysis below ignores the noise about long-run electricity prices (that's the buyer's problem — though it drives *what the buyer will pay*) and focuses on the fund's *actual* risks: **(1) will projects get approved and grid-connected on time, and (2) will buyers pay the assumed RTB prices, in enough volume, on schedule?**

**The headline view.** The market for shovel-ready ~5 MW distribution BESS development rights across NSW/VIC/SA is **real, structurally growing and policy-backed**, and a develop-and-flip model is **capital-light and well-suited to a ~$25m fund**. The strategy is genuinely investable — **but conditionally.** It lives or dies on two things the deck cannot prove on its own: a **deep, durable RTB buyer pool** and a **realistic success rate.** The single biggest risk is **exit/buyer risk** (a flip with no buyer is a stranded asset), closely followed by **development/approval risk.** And one honest independent flag runs throughout: decomposing success from public data lands at **~45% cumulative**, **between Boman's Conservative (40%) and Base (65%)** cases — i.e. **Boman's Base may be optimistic** unless the sub-5 MW exemption genuinely lifts small-distribution success.

---

## 2. Market boundary — exactly what we're analysing

The CFA's first rule of industry analysis: define the boundary before analysing. "Batteries" is far too broad — the economics, competition and comps for *5 MW distribution development rights* are completely different from *100 MW+ transmission built assets*. The fund's entire edge claim rests on this niche, so we analyse **exactly** this niche.

| Dimension | This fund |
|---|---|
| Asset | Standalone **~5 MW** (2–4 hour) BESS → ~10–20 MWh |
| Grid level | **Distribution network (≈22 kV)** — *not* transmission |
| Product sold | **Development rights / RTB ("shovel-ready", 路条)** — *not* built assets, *not* electricity |
| Geography | **Eastern NEM — NSW, VIC, SA** (three states) |
| Stage | Greenfield development → shovel-ready, **sold before construction** |
| Structure | A **portfolio/pipeline** of many small projects (more saleable and more diversified than one large asset) |

> **Why the 5 MW size is deliberate, not an accident.** Sub-5 MW projects qualify for an **AEMO registration exemption → faster, cheaper approval and connection** *(verify it persists — AER/AEMC)*. The small-distribution niche is the thesis: it is the structural reason for the size, and it underpins both the "white space" claim (§9) and the argument that small-distribution success could beat the large-project benchmark (§10).
>
> **A note on what changed.** An earlier framing of this deal mis-scoped it as 30–100 MW sub-transmission assets sold *construction-ready and contracted* across NSW/VIC only. That is the wrong market. This fund sells **earlier-stage, uncontracted RTB** for **~5 MW distribution** projects across **three** states. The "construction-ready, contracted" market is real — but here it is a *caution* (the stage the broader market increasingly pays up for), not the product (see §8).

---

## 3. Market sizing — top-down, bottom-up, triangulation

**The need.** NSW, VIC and SA carry large, policy-driven storage targets with the **majority not yet funded** — a structural supply gap. AEMO's ISP points to rapid storage growth: *Boman cites ~26% BESS CAGR to 2030, storage capacity ~7× by 2030 and ~16× by 2050 (Boman claim — verify directly against the AEMO ISP 2026 document).*

**Sizing the addressable RTB slice — triangulate two ways:**

| Approach | Method |
|---|---|
| **Top-down** | (NSW + VIC + SA storage target, GWh) × (distribution-side share) × (slice addressable by ~5 MW development) |
| **Bottom-up** | (number of suitable distribution nodes) × (typical project size) × (value per RTB project) |

Both estimates should be produced and the **gap between them** reported as a triangulation check (output: `data/processed/market_size.csv` per the build plan). The defensible claim for the trust is **structural**, not a precise number: the gap between *targeted* and *funded* distribution storage across the three states is large enough that well-located 5 MW projects are genuinely needed — *the precise GWh figure must be re-verified against the latest AEMO ISP.*

> **Boman's pipeline evidence (claims — verify):** screened 35 distribution points and **locked 13**; the funnel needs **48–95 projects** developed to **deliver ~38** and **sell 30–35** (the spread depends on the success rate — see §10). Independent check: does the addressable node count actually support a repeatable ~38-project pipeline, or does the niche fill up as rivals enter? *(AEMO Generation Information grounds the live pipeline.)*

---

## 4. Life cycle — growth stage, and why it's a tailwind here

The industry is firmly **growth-stage**: rapid expansion, evolving rules, heavy new entry, returns not yet competed away.

A prior buyout screen flagged BESS as a growth-stage **"yellow flag"** — **but that flag was for buy-and-hold operators** carrying long merchant exposure into an unstable market. For a **develop-and-flip** play the logic inverts: fast growth is exactly what you want, because **rising demand means more buyers for your projects.** Demand for the *product* (storage) and demand for the *asset* (RTB projects funds can buy) are rising together — the ideal combination for a developer with projects to sell.

| Read of the stage | For a buy-and-hold operator | For this develop-and-flip fund |
|---|---|---|
| Rapid build-out | Merchant prices volatile → yellow flag | More buyers competing for RTB → **tailwind** |
| Evolving rules | Regulatory uncertainty over a 15-yr hold | Exposure only over a 2+1-yr window — but a mid-window change still hits all projects at once (see §6) |
| Heavy new entry | More operators chasing the same revenue | More rivals chasing the same 5 MW nodes → **test the white space** (§9) |

> *Verify the ~26% CAGR against the AEMO ISP; the qualitative "growth-stage" classification is robust regardless of the exact figure.* **Caveat:** the demand is *policy-dependent* — if targets soften, RTB buyer appetite could cool within the fund's short life (see §6 and §10).

---

## 5. Porter's Five Forces — on the RTB market

The subtle, essential move: there are **two different industries** here, and we must analyse the one the fund *sells into*, not the one its buyers operate in.

| Market | Whose concern |
|---|---|
| (a) Electricity / storage operating market (merchant prices) | The **buyer** of the project — *not* the fund |
| (b) **Market for shovel-ready development rights (RTB)** | **The fund** — analyse THIS |

Scored for the **RTB distribution-BESS market** (force / rating / why):

| Force | Assessment | Why |
|---|---|---|
| **New entrants** | **Medium** (Boman claims low) | Large developers focus on 100 MW+ transmission, leaving claimed "white space" in 5 MW distribution. Barriers are site control, DNSP relationships and grid-slot know-how — *verify the gap is real and durable, not just early.* |
| **Buyer power** | **High — the crux** | RTB is bought by a finite pool of IPPs / infra funds / super funds. **Few buyers = high power = price pressure.** Boman's "3 interested buyers" are explicitly non-binding (§8). |
| **Supplier power** | **Medium** | Land, EPC, equipment — battery costs falling (a tailwind for the buyer's economics); **grid-connection slots are the scarce input** — securing them is the real moat. |
| **Substitutes** | **Medium–High** | Buyers can **self-develop**, buy large-scale storage instead, or use demand-response / gas peakers. The live question: *why buy your RTB rather than developing their own?* |
| **Rivalry** | **High** | Other developers chase the same distribution nodes; the niche can fill up. Boman locked 13 of 35 screened points — but others are hunting too. |

> **The two forces that decide this strategy:** **buyer power** (is the RTB pool deep, competitive and durable?) and **new entrants / rivalry** (is the 5 MW niche genuinely under-contested?). Score output: `data/processed/porter_scores.csv`.

---

## 6. PESTLE — policy dependency and the sub-5 MW exemption

| Factor | For this deal |
|---|---|
| **Political** | Net-zero, 82% renewables by 2030, state storage targets, AEMO ISP — a strong tailwind. **The classic risk:** demand depends on policy/subsidy *continuing*; if targets soften, RTB buyer appetite could cool — and a **2+1-year fund is highly exposed to a mid-window change.** |
| **Economic** | Interest rates drive buyers' cost of capital and willingness to pay; the battery-cost trend matters. *Risk-free anchored to RBA 10yr CGS (~4.8%, live).* |
| **Social** | Community acceptance — planning objections can delay or kill DAs (readable in public planning submissions across the three states). |
| **Technological** | Falling battery costs help asset economics **but** mean buyers expect to pay *less* over time — double-edged for RTB pricing. *Cost trend: CSIRO GenCost.* |
| **Legal** | **Sub-5 MW AEMO registration exemption → faster approval — a real regulatory edge** *(verify it persists — AER/AEMC).* State planning/EIA regimes (NSW SSD/IPC, VIC, SA PlanSA) differ materially. |
| **Environmental** | Fire safety, recycling, site environmental approvals — can trigger objections during approval. |

> **Policy dependency is the big PESTLE risk**, and the **sub-5 MW exemption is the flagged opportunity** — it is the structural reason for the 5 MW size and the lever that could lift small-distribution success above the large-project benchmark (§10). Both must be verified, not assumed. Factor output: `data/processed/pestle.csv`.

---

## 7. PE / fund screen — adapted for develop-and-flip

The strategy changes which boxes matter. Most notably, the screen's usual deal-breaker for BESS — *no recurring revenue* — is **sidestepped**, because the fund sells before any revenue exists.

| Criterion | Operator view | **This fund (develop-and-flip RTB)** |
|---|---|---|
| Recurring revenue | ❌ merchant / volatile | **Sidestepped** — fund sells before any revenue; merchant risk passes to the buyer |
| **Clear exit path** | — | ⭐ **THE critical criterion** — is the RTB buyer market deep, competitive and durable? |
| Barriers / white space | — | Claimed: 5 MW niche, grid-slot know-how, DNSP relationships, sub-5 MW exemption — **test** (§9) |
| Low capex *for the fund* | — | ✅ development is capital-light (~$500k/project vs ~$8–10m to build) — a good fit for a ~$25m fund |
| Favourable trends | — | ✅ coal retirement, storage targets, falling build costs |

> **Screen verdict logic:** a flip lives or dies on the **exit row.** If the buyer pool is deep, active and paying good RTB prices, the model can work. If it depends on a few non-binding buyers or a still-forming RTB market, the short 2+1-year timeline is dangerous. Screen output: `data/processed/pe_screen.csv`.

**The economics the screen rests on (Boman's assumptions — find independent comps):**

| Item | Figure | Source / status |
|---|---|---|
| Development cost per project | **~$500k** (site + EIA + grid application + community + overhead) | Boman claim — *verify bottom-up* |
| Built 5 MW / 10 MWh asset cost | **~$8–10m** (≈$1.6–2.0m/MW) | Industry benchmark — *CSIRO GenCost anchors the trend* |
| RTB sale price (the prize) | **~$0.5–1.1m/project** (~$0.10–0.22m/MW) | Boman claim — **find independent comps** |
| RTB as % of built value | **~10–12%** | Derived — *is that the right greenfield→RTB premium?* |

RTB price by state (**Boman claims — verify with comps, not the deck**):

| State | RTB price / 5 MW project | ≈ per MW |
|---|---|---|
| VIC | $0.8m – $1.0m | $160k–200k/MW |
| NSW | $0.9m – $1.1m | $180k–220k/MW |
| SA | $0.5m – $0.7m | $100k–140k/MW |

> **Honest flag:** these are Boman's *own assumed* sale prices. The broader market increasingly rewards *contracted, construction-ready* assets — so selling *earlier-stage, uncontracted RTB* may fetch the lower end, or require a discount, unless the niche is genuinely supply-short. Independent transaction comps (`data/processed/buyer_comps.csv`) are essential, and a 20–30% lower exit price should be stressed in the valuation.

---

## 8. Buyer landscape & exit path — the decisive section

For a develop-and-flip, the **exit market is the whole game** — there must be deep, active, well-funded demand for *RTB projects* in 2–3 years, not just demand for electricity storage in general.

**The buyer pool (categories of real, active Australian battery-asset buyers):**

- **IPPs / developer-operators** acquiring RTB to build out their own portfolios.
- **Infrastructure fund managers** — e.g. Palisade / Intera Renewables, Copenhagen Infrastructure Partners (CIP), Quinbrook.
- **Superannuation funds** — e.g. Aware Super, HESTA (often via platforms).
- **Government green capital** — Clean Energy Finance Corporation (CEFC), Energy Security Corporation (ESC).
- **Energy retailers / utilities** — Origin, AGL, EnergyAustralia (seeking firming capacity).

**The two cautions that dominate this section:**

1. **Bindingness.** Boman's "**3 interested buyers**" are **explicitly non-binding.** Interest is not a contract. The trust must ask what, if anything, is contractual — signed options, MOUs, price terms.
2. **Stage mismatch.** The clearest current market signal is that capital is **"paying for execution-ready, contracted storage, not speculative pipelines."** This fund sells **earlier-stage, uncontracted RTB** — so it must demonstrate that the **RTB buyer market specifically** is deep, or that its projects are de-risked enough (planning + grid secured) to command the assumed price. The CIP→Palisade template — a project sold *underpinned by a long-term tolling agreement* — is exactly the *contracted, construction-ready* profile that this fund's RTB product **does not yet have**, which is precisely why this caution matters.

> **The decisive question:** *Can we name at least 3–4 credible, active, well-funded RTB buyers, and point to recent deals proving they pay the assumed prices for 5 MW distribution RTB specifically?* If yes, the model can work. If the exit rests on a handful of non-binding parties or a still-forming RTB market, the short fund life is the danger. *Sources: energy trade press (Energy-Storage.news, RenewEconomy, pv magazine, AFR); CEFC/ESC announcements — re-verify; richest deal databases (BNEF, Enerdatics, Mergermarket) are paid and out of scope, a transparent limitation.*

---

## 9. Competitive landscape — who else develops in the 5 MW niche

The thesis rests on a genuine **"white space"** claim: large, well-capitalised developers chase **100 MW+ transmission** projects (bigger cheques, bigger margins), leaving **small ~5 MW distribution sites under-contested** — and the **sub-5 MW exemption** lowers the cost of playing there. Combined with DNSP relationships and grid-slot know-how, that is the claimed moat.

**This must be tested, not assumed:**

| Question to test | Why it matters |
|---|---|
| Who else develops ~5 MW distribution BESS in NSW/VIC/SA? | If the niche is crowded, the white space is illusory and RTB prices compress (§5 rivalry). |
| Is the gap structural or just *early*? | A niche that is under-contested today can fill up fast in a growth-stage market (§4). |
| Are grid-connection slots genuinely secured? | Slots are the scarce input — a secured slot is the real, hard-to-replicate moat; a *queuing* slot is not. |
| Can buyers simply self-develop instead? | The substitute threat (§5): if buyers can do it themselves cheaply at 5 MW, the RTB margin is thin. |

> **The honest read:** the white space is *plausible* — the size logic and the exemption are real reasons large developers stay away — but in a fast-growing market an under-contested niche is also the kind that attracts entrants. The diligence job is to confirm the gap is **durable**, and that *this* fund holds the scarce, hard-to-replicate inputs (secured sites, secured slots, DNSP relationships), not just early-mover position. *(Ground against AEMO Generation Information for who is actually developing at this scale.)*

---

## 10. Verdict — the single biggest risk

**Industry verdict.** The market for shovel-ready ~5 MW distribution BESS development rights across NSW/VIC/SA is **real, structurally growing and policy-backed**, and the develop-and-flip model is **capital-light and well-suited to a ~$25m fund**. The strategy is genuinely investable — **but conditionally**, because it lives or dies on two things the deck cannot prove on its own: a **deep, durable RTB buyer pool** and a **realistic success rate.**

**The single biggest risk is exit / buyer risk.** A flip with no buyer is a stranded asset. The buyer pool for Australian battery assets is deep and well-funded, but two cautions dominate: (a) Boman's "3 interested buyers" are **non-binding**; and (b) the market increasingly pays up for *de-risked, contracted, construction-ready* assets, whereas this fund sells *earlier-stage, uncontracted RTB.* **Closely behind sits development / approval risk** — getting planning and grid connection on time across three states. Note what is *not* the main risk: **merchant-price volatility**, which passes to the buyer (the reframe in §1).

**The success-rate optimism finding.** The success rate is the master driver of returns: a lower rate means a bigger starting pipeline is needed to still deliver ~38 projects, raising development cost and cutting IRR. We decompose it as a credit-style survival curve and anchor each gate to independent public data:

`Cumulative P(success) = P(planning approval) × P(grid connection) × P(reach sale)`

| Gate | Independent benchmark (public data) | Typical duration |
|---|---|---|
| Planning approval | ≈ **80%** *(NSW/VIC/SA planning portals)* | ~1.25 yrs |
| Grid connection *(the bottleneck)* | ≈ **70%** *(AEMO Connections Scorecard)* | ~1.50 yrs |
| Reach sale | ≈ **80%** | ~0.50 yrs |
| **Cumulative** | **≈ 45%** | — |

| | Conservative | Base | Ideal |
|---|---|---|---|
| Boman success rate *(claim — verify)* | 40% | **65%** | 80% |
| Boman investor IRR *(claim — rebuild)* | **10.7%** | **19.4%** | **23.8%** |
| Independent decomposition | — | **≈45%** | — |

> **The key DD finding:** the independent decomposition (~45%) lands **between Boman's Conservative (40%) and Base (65%)** — i.e. **Boman's Base case may be optimistic.** *Counter-point to test fairly:* the **sub-5 MW exemption** and small-distribution simplicity could genuinely lift success above the large-project benchmark — so the trust should ask Boman for **sub-5 MW-specific, per-state evidence** rather than accept either number. Either way, the planning and connection statistics must be computed from the NSW/VIC/SA registers, not taken from the deck (outputs: `approval_stats.csv`, `connection_stats.csv` → feed the Stage-02 valuation survival curve).
>
> **Timeline is the enemy of IRR.** Precedents (e.g. PICESS ≈ 8 months for *planning alone*; grid connection can take longer) suggest the 2+1-year window is tight. If approvals slip 6–12 months, IRR drops fast.

**Recommended posture: pursue — conditional on independently verifying** (1) **exit depth & pricing** (≥3–4 credible, active RTB buyers and comps supporting the assumed $/project, anything contractual rather than just "interested"); (2) **the success rate** (sub-5 MW, per-state evidence reconciling Boman's 65% with the independent ~45%); (3) **a survivable downside** (the fee-adjusted Conservative case stressed further for lower price, lower success and slipped timeline, without losing capital); and (4) **alignment** (a transparent rule for how the "keep-best 5–10" projects are selected, so the flip pool is not left the leftovers).

> **The credit-risk edge.** This deal plays to the trust's analytical strength: execution risk = delivery diligence ("can the developer hit its milestones on time?"); the exit/price question = the serviceability instinct ("where's the reliable demand, and is it contracted?"); comps + First Chicago = analytical structuring and downside protection. A renewables enthusiast sees "green + growth = invest"; the trained eye lands on *can they execute, and will someone pay?*
