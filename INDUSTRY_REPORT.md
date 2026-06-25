# Industry Report — Australian Distribution-Network BESS Development Rights (RTB)

### Prepared for the Board / Investment Committee — evaluating an LP commitment to the **Boman BESS Development Fund**

> An independent industry primer on the market the Boman fund actually sells into: **shovel-ready (RTB) development rights for ~5 MW distribution-connected batteries across NSW, VIC and SA.** It frames *whether that market is real, growing, durable, and — critically — whether there is a deep pool of buyers* — so the Board can pressure-test the manager's deck before committing the family trust as an LP.

**Scope:** standalone ~5 MW (2–4 hr) distribution-network BESS, sold as development rights / RTB, in the eastern NEM (NSW, VIC, SA). **As at:** mid-2026. **Currency:** AUD.

> **Status & integrity note.** This is an **educational / due-diligence framework**, **not investment advice** (we are not licensed advisers). The Boman fund is a **wholesale-investor product**; read the Information Memorandum for actual terms — **capital is at risk**. Crucially: **every figure attributed to Boman is the manager's own forward-looking projection** (their deck says so throughout) and is tagged *"(Boman claim — verify)"*. Independent public-data findings are shown alongside and tagged by source. All figures must be re-verified before any decision.

> **How this fits the repo.** This is the *industry view for the Board*. The deeper analysis deliverable is [`analysis/industry_analysis.md`](analysis/industry_analysis.md); the independent valuation rebuild (rNPV + survival curve + First Chicago) is a separate workstream — see [`model/`](model/) and the notebooks.

---

## Contents

1. [Executive summary](#1-executive-summary)
2. [The deal and the one reframe that changes everything](#2-the-deal-and-the-one-reframe-that-changes-everything)
3. [Market boundary — defining exactly what we're analysing](#3-market-boundary--defining-exactly-what-were-analysing)
4. [Why now — the structural demand drivers](#4-why-now--the-structural-demand-drivers)
5. [Market size and growth](#5-market-size-and-growth)
6. [Industry structure — life cycle, Porter, PESTLE, PE screen](#6-industry-structure--life-cycle-porter-pestle-pe-screen)
7. [Economics — the RTB development margin and the value ladder](#7-economics--the-rtb-development-margin-and-the-value-ladder)
8. [The exit market — buyer landscape and depth (the decisive section)](#8-the-exit-market--buyer-landscape-and-depth-the-decisive-section)
9. [Success probability — the credit-risk survival lens](#9-success-probability--the-credit-risk-survival-lens)
10. [Fund mechanics and headline returns](#10-fund-mechanics-and-headline-returns)
11. [Key risks](#11-key-risks)
12. [Verdict, board posture and questions for the manager](#12-verdict-board-posture-and-questions-for-the-manager)
13. [Data snapshot & sources](#13-data-snapshot--sources)
14. [Disclaimer](#14-disclaimer)

---

## 1. Executive summary

**What we are evaluating.** Not whether to *build and operate* batteries, but whether to commit the family trust as an **LP** to a fund that **develops ~5 MW distribution-connected battery projects to shovel-ready (RTB) and sells the project companies before construction.** The fund never operates an asset.

**The reframe that decides everything.** The famous problem that sinks BESS on the classic PE screen — *merchant, volatile electricity revenue* — **largely does not apply to this fund**, because it sells before any electricity is traded. **Merchant-price risk passes to the buyer.** The fund's real risks are therefore narrower and sharper: **(1) will projects get approved and grid-connected on time, and (2) will buyers pay the assumed RTB prices, in enough volume, on schedule?**

**Is the market real and growing?** Yes — structurally. Coal retirement + record renewables build-out create a large, policy-backed firming need; AEMO's ISP points to rapid storage growth *(Boman cites ~26% BESS CAGR to 2030, storage 7× by 2030 / 16× by 2050 — verify against the ISP)*. The industry is firmly **growth-stage**, which is a **tailwind for a develop-and-flip strategy** (rising demand = more buyers for projects), even though it is a "yellow flag" for a buy-and-hold operator.

**Is the niche defensible?** Plausibly. The thesis rests on a genuine **"white space"**: large developers chase 100 MW+ transmission projects, leaving small 5 MW distribution sites under-contested — and **sub-5 MW projects qualify for an AEMO registration exemption that speeds approval** *(verify it persists)*. That regulatory edge, plus DNSP relationships and grid-slot know-how, is the claimed moat. It must be tested, not assumed.

**Where the real risk sits — the exit.** A flip with no buyer is a stranded asset. The buyer pool for Australian battery assets is deep and well-funded (IPPs, infrastructure funds, super funds), but **two cautions dominate**: (a) Boman's "**3 interested buyers**" are explicitly **non-binding**; and (b) the broader market signal is that capital increasingly pays up for *de-risked, contracted, construction-ready* assets — whereas this fund sells *earlier-stage, uncontracted RTB*. The Board must satisfy itself that the **RTB buyer market specifically** is deep, competitive and durable across the fund's life.

**The honest independent flag.** Decomposing success from independent public data (planning ≈80% × connection ≈70% × sale ≈80% ≈ **45% cumulative**) lands **between Boman's Conservative (40%) and Base (65%) cases** — i.e. **Boman's Base may be optimistic** unless the sub-5 MW exemption genuinely lifts small-distribution success above the large-project benchmark. This single variable is the master driver of returns.

**Board takeaway.** A genuine, policy-backed, capital-light niche with a viable exit channel — **but conditional**. The decision turns on independently verifying the **exit (buyer-pool depth and RTB pricing)** and the **success rate**, then judging whether the **expected, fee-adjusted** return compensates for a real downside. The single biggest risk is **exit/buyer risk**, closely followed by **development/approval risk**.

---

## 2. The deal and the one reframe that changes everything

Before any framework, fix what kind of deal this is — because it flips which risks matter.

| | A normal BESS operator | **The Boman fund (develop-and-flip RTB)** |
|---|---|---|
| What it does | Builds batteries, sells electricity for ~20 years | **Develops** sites to shovel-ready (RTB), then **sells the project companies** |
| Holds the asset? | Yes | **No — sells before construction** |
| Main risk | **Merchant-price risk** (volatile electricity prices) | **Development/approval risk + exit/buyer risk** |
| Who bears merchant risk | The operator | **The buyer** of the RTB project |

> **The key insight:** because the fund never operates the asset, the merchant-revenue problem that fails BESS on the classic PE screen is **sidestepped** — it passes to the buyer. So our due diligence must ignore the noise about long-run electricity prices (that's the buyer's problem, though it drives *what the buyer will pay*) and focus on the fund's *actual* risks: **approvals on time, and buyers paying the assumed prices.**

The two questions this report exists to answer:
1. **Is the market for shovel-ready distribution BESS real, growing and durable — with a deep buyer pool?** *(this report)*
2. **Are the RTB prices and fund returns credible when rebuilt independently?** *(the valuation workstream — see [`model/`](model/))*

---

## 3. Market boundary — defining exactly what we're analysing

The CFA's first rule of industry analysis: define the boundary before analysing. "Batteries" is too broad; the economics, competition and comps for *5 MW distribution development rights* are completely different from *100 MW+ transmission built assets*. The fund's entire edge claim rests on this niche, so we analyse **exactly** this niche.

| Dimension | This fund |
|---|---|
| Asset | Standalone **~5 MW** (2–4 hour) BESS → 10–20 MWh |
| Grid level | **Distribution network (≈22 kV)** — *not* transmission |
| Product sold | **Development rights / RTB ("shovel-ready", 路条)** — *not* built assets, *not* electricity |
| Geography | **Eastern NEM — NSW, VIC, SA** |
| Stage | Greenfield development → shovel-ready, **sold before construction** |
| Structure | A **portfolio/pipeline** of many small projects (more saleable and more diversified than one large asset) |

> Why the 5 MW size is deliberate: **sub-5 MW attracts an AEMO registration exemption** → faster, cheaper approval and connection. The small-distribution niche is the thesis, not an accident.

---

## 4. Why now — the structural demand drivers

Four forces pull the same direction, making this a *structural* growth story, not a cyclical one:

1. **Coal retirement.** Australia's ageing coal fleet is closing, often ahead of schedule, removing dispatchable "firm" capacity that must be replaced.
2. **Renewables penetration → a firming gap.** Solar and wind are now the cheapest new energy but are variable; the more renewables, the larger the need for fast storage to firm them. Batteries are the lowest-cost, fastest-to-build firming technology for the 1–4 hour duration that dominates near-term need.
3. **Policy targets and revenue underwriting.** Net-zero, the 82%-renewables-by-2030 target, state storage targets and AEMO's ISP convert a physical need into **bankable demand** — the thing infrastructure capital requires (see [§6 PESTLE](#6-industry-structure--life-cycle-porter-pestle-pe-screen)).
4. **A funding gap.** Storage *ambition* runs well ahead of storage that has reached FID — the structural opening that well-located small projects fill.

> **The investable point:** demand for the *product* (storage) and demand for the *asset* (RTB projects funds can buy) are rising together — the ideal combination for a developer with projects to sell. **Caveat:** this demand is *policy-dependent*; if targets soften, buyer appetite for RTB could cool within the fund's short life (see risks).

---

## 5. Market size and growth

**The need.** NSW, VIC and SA carry large, policy-driven storage targets with the **majority not yet funded** — a structural supply gap. AEMO's ISP points to rapid growth: *Boman cites ~26% BESS CAGR to 2030, storage capacity ~7× by 2030 and ~16× by 2050 (Boman claim — verify directly against the AEMO ISP 2026 document).*

**Sizing the addressable RTB slice — triangulate two ways:**

- **Top-down:** (NSW + VIC + SA storage target, GWh) × (distribution-side share) × (slice addressable by ~5 MW development).
- **Bottom-up:** (number of suitable distribution nodes) × (typical project size) × (value per RTB project).

The two estimates should be produced and the **gap between them** reported as a triangulation check (output: `data/processed/market_size.csv` per the build plan). The defensible claim for the Board is **structural**: the gap between *targeted* and *funded* distribution storage across the three states is large enough that well-located 5 MW projects are genuinely needed — *the precise GWh figure must be re-verified against the latest ISP.*

> **Boman's pipeline evidence (claims — verify):** screened 35 distribution points and **locked 13**; the funnel needs **48–95 projects** developed to **deliver ~38** and **sell 30–35** (the spread depends on success rate — see §9). Independent check: does the addressable node count actually support a repeatable 38-project pipeline, or does the niche fill up as rivals enter?

---

## 6. Industry structure — life cycle, Porter, PESTLE, PE screen

### 6a. Life-cycle stage — **growth (a tailwind here, not a yellow flag)**

Rapid expansion, evolving rules, heavy new entry, returns not yet competed away. A prior buyout screen flagged BESS as a growth-stage "yellow flag" — **but that was for buy-and-hold operators.** For a **develop-and-flip** play, fast growth is exactly what you want: rising demand means more buyers for your projects. *Verify the ~26% CAGR against the ISP; the qualitative classification is robust.*

### 6b. Porter's Five Forces — on the **RTB market**, not the electricity market

The subtle, essential move: there are two industries here, and we must analyse the one the fund *sells into*.

| Market | Whose concern |
|---|---|
| (a) Electricity / storage operating market (merchant prices) | The **buyer** of the project — *not* the fund |
| (b) **Market for shovel-ready development rights (RTB)** | **The fund** — analyse THIS |

| Force | Assessment for RTB distribution BESS | Why |
|---|---|---|
| **New entrants** | **Medium** (claimed low) | Large developers focus on 100 MW+ transmission, leaving "white space" in 5 MW distribution. Barriers are site control, DNSP relationships, grid-slot know-how — *verify the gap is real and durable, not just early.* |
| **Buyer power** | **High** (the crux) | RTB is bought by a finite pool of IPPs / infra funds / super funds. **Few buyers = high power = price pressure.** Boman's "3 interested buyers" are non-binding. |
| **Supplier power** | **Medium** | Land, EPC, equipment — battery costs falling (tailwind); **grid-connection slots are the scarce input** (securing them = a moat). |
| **Substitutes** | **Medium–High** | Buyers can **self-develop**, buy large-scale storage instead, or use demand-response/gas. *Why buy your RTB vs developing their own?* |
| **Rivalry** | **High** | Other developers chase the same distribution nodes; the niche can fill up. |

> The two forces that decide this strategy: **buyer power** (is the RTB pool deep, competitive and durable?) and **new entrants/rivalry** (is the 5 MW niche genuinely under-contested?).

### 6c. PESTLE — policy dependency is the big one

| Factor | For this deal |
|---|---|
| **Political** | Net-zero, 82% renewables by 2030, state storage targets, AEMO ISP — strong tailwind. **The classic risk:** demand depends on policy/subsidy *continuing*; if targets soften, RTB buyer appetite could cool — and a 2+1-year fund is highly exposed to mid-window change. |
| **Economic** | Interest rates drive buyers' cost of capital and willingness to pay; the battery-cost trend. *Risk-free anchored to RBA 10yr CGS (~4.8%, live).* |
| **Social** | Community acceptance — planning objections can delay or kill DAs (readable in public planning submissions). |
| **Technological** | Falling battery costs help asset economics **but** mean buyers expect to pay *less* over time — a double-edged sword for RTB pricing. *Cost trend: CSIRO GenCost.* |
| **Legal** | **Sub-5 MW AEMO registration exemption → faster approval** — a real regulatory edge (verify it persists). State planning/EIA regimes (NSW / VIC / SA) differ materially. |
| **Environmental** | Fire safety, recycling, site environmental approvals — can trigger objections. |

### 6d. PE / fund screen — adapted for develop-and-flip

| Criterion | Operator view | **This fund (develop-and-flip RTB)** |
|---|---|---|
| Recurring revenue | ❌ merchant / volatile | **Sidestepped** — fund sells before any revenue; merchant risk passes to the buyer |
| **Clear exit path** | — | ⭐ **THE critical question** — is the RTB buyer market deep and durable? |
| Barriers / white space | — | Claimed: 5 MW niche, grid know-how, DNSP relationships, sub-5 MW exemption — **test** |
| Low capex *for the fund* | — | ✅ development is capital-light (~$500k/project vs $8–10m to build) — a good fit for a ~$25m fund |
| Favourable trends | — | ✅ coal retirement, storage targets, falling build costs |

> **Screen verdict logic:** a flip lives or dies on the **exit row.** If the buyer pool is deep, active and paying good RTB prices, the model can work. If it depends on a few non-binding buyers or a still-forming RTB market, the short timeline is dangerous.

---

## 7. Economics — the RTB development margin and the value ladder

The fund's return is the **development margin**: the gap between the cost to take a site to shovel-ready and the price a buyer pays for the RTB project.

| Item | Figure | Source / status |
|---|---|---|
| Development cost per project | **~$500k** (site + EIA + grid application + community + overhead) | Boman claim — *verify bottom-up* |
| Built 5 MW / 10 MWh asset cost | **~$8–10m** (≈$1.6–2.0m/MW) | Industry benchmark — *CSIRO GenCost anchors the trend* |
| RTB sale price (the prize) | **~$0.5–1.1m/project** (~$0.10–0.22m/MW) | Boman assumption — **find independent comps** |
| RTB as % of built value | **~10–12%** | Derived — *is that the right premium for greenfield→RTB?* |
| Risk-free rate (discount base) | **~4.8%** (10yr CGS) | RBA, live |

**RTB price by state (Boman's assumptions — these need independent comps, not the deck's):**

| State | RTB price / 5 MW project | ≈ per MW |
|---|---|---|
| VIC | $0.8m – $1.0m | $160k–200k/MW |
| NSW | $0.9m – $1.1m | $180k–220k/MW |
| SA | $0.5m – $0.7m | $100k–140k/MW |

**How to verify the margin (the value-ladder logic):**
- **Transaction comps** — find *actual* Australian BESS development-rights / RTB sales (trade press, broker talk, the team's own wind precedents like Mt Mercer). Compute $/MW independently.
- **Development-margin sense-check** — is ~10–12% of built value the right premium for taking a project greenfield → shovel-ready? Compare against solar/wind RTB precedents.
- **Direction of travel** — falling battery costs and more developers entering could **compress RTB prices** over the fund's life. Stress a 20–30% lower exit price.

> **Honest flag:** the prices above are Boman's *own assumed* sale prices. The broader market increasingly rewards *contracted, construction-ready* assets — so selling *earlier-stage, uncontracted RTB* may fetch the lower end, or require a price discount, unless the niche is genuinely supply-short. Independent comps are essential.

---

## 8. The exit market — buyer landscape and depth (the decisive section)

For a develop-and-flip, the **exit market is the whole game** — there must be deep, active, well-funded demand for *RTB projects* in 2–3 years, not just demand for electricity storage.

**The buyer pool (categories of real, active Australian battery-asset buyers):**

- **IPPs / developers-operators** acquiring RTB to build out their own portfolios.
- **Infrastructure fund managers** — e.g. Palisade / Intera Renewables, Copenhagen Infrastructure Partners (CIP), Quinbrook.
- **Superannuation funds** — e.g. Aware Super, HESTA (often via platforms).
- **Government green capital** — Clean Energy Finance Corporation (CEFC), Energy Security Corporation (ESC).
- **Energy retailers / utilities** — Origin, AGL, EnergyAustralia (seeking firming capacity).

**The two cautions that dominate this section:**

1. **Bindingness.** Boman's "**3 interested buyers**" are **explicitly non-binding.** Interest is not a contract. The Board must ask what, if anything, is contractual (signed options, MOUs, price terms).
2. **Stage mismatch.** The clearest current market signal is that capital is **"paying for execution-ready, contracted storage, not speculative pipelines."** This fund sells **earlier-stage, uncontracted RTB** — so it must demonstrate that the **RTB buyer market specifically** is deep, or that its projects are de-risked enough (planning + grid secured) to command the assumed price.

> **The decisive question:** *Can we name at least 3–4 credible, active, well-funded RTB buyers, and point to recent deals proving they pay the assumed prices for 5 MW distribution RTB?* If yes, the model can work. If the exit rests on a handful of non-binding parties or a still-forming RTB market, the short fund life is the danger.

---

## 9. Success probability — the credit-risk survival lens

The **success rate is the master driver** of returns: a lower rate means a bigger starting pipeline is needed to still deliver ~38 projects, raising development cost and cutting IRR. Boman models it as three scenarios; we decompose it as a **PD-style survival curve** — the same statistical idea as a multi-period probability-of-default model — and anchor each gate to independent public data.

`Cumulative P(success) = P(planning approval) × P(grid connection) × P(reach sale)`

| Gate | Independent benchmark (public data) | Typical duration |
|---|---|---|
| Planning approval | ≈ **80%** | ~1.25 yrs |
| Grid connection *(the bottleneck)* | ≈ **70%** | ~1.50 yrs |
| Reach sale | ≈ **80%** | ~0.50 yrs |
| **Cumulative** | **≈ 45%** | — |

**Boman's scenarios vs the independent check:**

| | Conservative | Base | Ideal |
|---|---|---|---|
| Boman success rate *(claim)* | 40% | **65%** | 80% |
| Independent decomposition | — | **≈45%** | — |

> **The key DD finding:** the independent decomposition (~45%) lands **between Boman's Conservative (40%) and Base (65%)** — i.e. **Boman's Base case may be optimistic.** *Counter-point to test fairly:* the **sub-5 MW exemption** and small-distribution simplicity could genuinely lift success above the large-project benchmark — so the Board should ask Boman for **sub-5 MW-specific, per-state evidence** rather than accept either number. Either way, the planning and connection statistics must be computed from the NSW / VIC / SA registers, not taken from the deck.

> **Timeline is the enemy of IRR.** Precedents cited (PICESS ≈ 8 months for *planning alone*; grid connection can take longer) suggest the 2+1-year window is tight. If approvals slip 6–12 months, IRR drops fast.

---

## 10. Fund mechanics and headline returns

The Board is committing as an **LP**, so net-of-fees economics and lock-up matter as much as the gross opportunity. *(Full independent rebuild is the valuation workstream; this is the headline only.)*

| Term *(Boman — verify in the IM)* | Detail |
|---|---|
| Fund size | ~$25m (wholesale investors only) |
| Term / liquidity | **2+1 years**, no early redemption (illiquid lock-up) |
| Fees | **2% entry + 2%/yr management + 20% carry over an 8% hurdle** |
| Strategy nuance | Plans to **keep 5–10 of the *best* projects to operate** — an alignment question (does the flip pool get the leftovers, and how are "best" chosen?) |

**Boman's headline investor (net) IRR — three scenarios (claims to rebuild):**

| Scenario | Success rate | Investor IRR |
|---|---|---|
| Conservative | 40% | **10.7%** |
| Base | 65% | **19.4%** |
| Ideal | 80% | **23.8%** |

**First Chicago weighting (illustrative — the Board sets the probabilities; Boman supplies none):**

| Scenario | Investor IRR | Illustrative probability | Weighted |
|---|---|---|---|
| Conservative | 10.7% | 30% | 3.2% |
| Base | 19.4% | 50% | 9.7% |
| Ideal | 23.8% | 20% | 4.8% |
| **Expected IRR** | | **100%** | **≈ 17.7%** |

> **Two judgements for the Board:** (1) does the **expected, fee-adjusted** IRR beat our hurdle for the risk taken? (2) **Can we live with the downside?** The Conservative case is ~10.7% *if Boman's assumptions hold* — stress it further (lower RTB price, success rate near the independent ~45%, fee drag, slipped timeline) and check whether it can go **negative**. The credit lens: the worst case, not the headline, protects capital.

---

## 11. Key risks

| Risk | Severity | Nature |
|---|---|---|
| **Exit / buyer risk** | **High (the #1 risk)** | Will enough buyers pay the assumed RTB prices ($0.5–1.1m/project), in volume, on schedule? The "3 buyers" are non-binding; the market leans toward *contracted* assets, not raw RTB. |
| **Development / approval risk** | **High** | Planning + grid connection on time across NSW/VIC/SA. The master driver of returns via the success rate; timeline slips hit IRR hard. |
| **Success-rate optimism** | **High** | Boman's Base 65% sits above the independent ~45% decomposition; verify with sub-5 MW, per-state evidence. |
| **Policy dependency** | **High** | Buyer appetite rests on net-zero / 82%-by-2030 / state schemes and the sub-5 MW exemption; a mid-window change hits all projects at once. |
| **Concentration / correlation** | **Medium–High** | ~38 projects across 3 states, one strategy — a single policy or rule change is correlated across the whole portfolio. |
| **RTB price compression** | **Medium** | Falling battery costs + new entrants could lower RTB prices over the fund's life. |
| **Fee drag** | **Medium** | 2% entry + 2%/yr + 20% carry over 8% — a meaningful gross-to-net gap over a short hold; confirm the *gross* IRR behind the *net* numbers. |
| **Liquidity** | **Medium** | 2+1-year lock-up, no early redemption. |
| **Alignment** | **Medium** | "Keep the best 5–10" — could leave the flip pool with weaker projects; how is "best" selected? |

> **The single biggest risk is exit/buyer risk** — a flip with no buyer is a stranded asset — **closely followed by development/approval risk.** Note what is *not* the main risk: **merchant-price volatility**, which passes to the buyer (the reframe in §2).

---

## 12. Verdict, board posture and questions for the manager

**Industry verdict.** The market for shovel-ready ~5 MW distribution BESS development rights across NSW/VIC/SA is **real, structurally growing and policy-backed**, and the develop-and-flip model is **capital-light and well-suited to a ~$25m fund**. The strategy is genuinely investable — **but conditionally**, because it lives or dies on two things the deck cannot prove on its own: a **deep, durable RTB buyer pool** and a **realistic success rate.**

**Recommended Board posture: *pursue — conditional on independent verification of* —**
1. **Exit depth & pricing** — ≥3–4 credible, active RTB buyers and independent comps supporting the assumed $/project (anything contractual, not just "interested").
2. **Success rate** — sub-5 MW, per-state approval and connection evidence reconciling Boman's 65% Base with the independent ~45%.
3. **A survivable downside** — the fee-adjusted Conservative case stressed further (lower price, lower success, slipped timeline) without losing capital.
4. **Alignment** — a transparent rule for how the "keep-best 5–10" projects are selected.

**Questions to put to the manager (IC-memo style):**
- What is your historical/expected planning-approval and grid-connection success rate **by state**, with evidence — specifically for **sub-5 MW** projects?
- Of the "3 interested buyers," is anything **contractual**? What price/terms?
- Show the **bottom-up $500k/project** development-cost build-up.
- What **independent comps** support the RTB prices ($0.5–1.1m/project)?
- What is the **net-of-all-fees** IRR, and the **gross** IRR behind it?
- What happens to timeline/IRR if approvals slip **6–12 months**?
- How are the **5–10 "keep" projects** selected, and how does that affect the flip pool?
- What is the genuine downside — **can investors lose capital, and in what scenario?**

> **The credit-risk edge.** This deal plays to the trust's analytical strength: execution risk = delivery diligence ("can the developer hit its milestones on time?"); the exit/price question = the serviceability instinct ("where's the reliable demand, and is it contracted?"); comps + First Chicago = analytical structuring and downside protection. A renewables enthusiast sees "green + growth = invest"; the trained eye lands on *can they execute, and will someone pay?*

---

## 13. Data snapshot & sources

Independent public-data inputs (the verification anchors). Figures are **documented public benchmarks as at mid-2026** unless marked *live*, and **must be re-verified**. Full provenance is logged in [`SOURCES.md`](SOURCES.md).

| Source | What it anchors | Status |
|---|---|---|
| **AEMO ISP 2026** | Storage growth / CAGR; market sizing; life-cycle stage | re-verify |
| **AEMO Generation Information** | Pipeline grounding; proposed→committed attrition | 🟡 benchmark |
| **AEMO Connections Scorecard / KCI** | Grid-connection success rate & duration (the bottleneck) | 🟡 benchmark |
| **NSW / VIC / SA planning portals** | Approval rates & timelines by state → success curve | 🟡 benchmark (NSW computed; VIC/SA to add) |
| **CSIRO GenCost** | Battery build-cost trend (~$8–10m per 5 MW asset) | 🟡 benchmark |
| **RBA** — Capital Market Yields (10yr CGS) | Risk-free / discount-rate base (~4.8%) | 🟢 live |
| **Energy trade press** (Energy-Storage.news, RenewEconomy, pv magazine, AFR) | RTB / development-rights deals; buyer landscape | 🟢 candidate links |
| **AER / AEMC** | Market rules; the sub-5 MW registration exemption | re-verify |

🟢 *live download* · 🟡 *documented benchmark (verify)*. The pipeline **never fabricates data** — where a source blocks automated access it falls back to a documented public benchmark, flagged for re-verification. The richest deal databases (BloombergNEF, Enerdatics, Mergermarket) are **paid and out of scope** — a transparent limitation. **All figures attributed to Boman are the manager's forward-looking projections, presented as claims to verify independently.**

---

## 14. Disclaimer

This report is an **educational / due-diligence framework**, **not investment advice** and not financial product advice; we are not licensed advisers. It analyses industry conditions reflecting Australian conditions **as at mid-2026** and references the **Boman BESS Development Fund**, a **wholesale-investor product** — read the full Information Memorandum for actual terms, fees and risk factors. **Capital is at risk:** a develop-and-flip pipeline can underperform or fail if approvals don't come through or buyers don't pay the assumed prices. Every figure attributed to the manager is its own forward-looking projection and must be **independently verified**; keep independent numbers clearly separate from the manager's in any model. Frameworks used (industry life cycle, Porter's Five Forces, PESTLE, the PE screen) are standard analytical tools applied here through a develop-and-flip lens.
