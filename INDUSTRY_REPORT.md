# Industry Analysis — Australian Distribution-Scale Battery "Develop-and-Flip"

### The market behind the Boman BESS Development Fund — an independent assessment for the family trust

*This is the project's single industry write-up. It explains, in plain terms, the market the fund operates in and whether that market supports the fund's plan. It is an educational / due-diligence document, **not investment advice**. Every figure the manager (Boman) has provided is treated as a **claim to be checked**; our own findings come from free public data. The fund is a wholesale-investor product — read the Information Memorandum; capital is at risk. All numbers reflect Australian conditions as at mid-2026 and should be re-verified before any decision.*

---

## What the fund actually does

The fund does not build batteries and sell electricity. It buys small sites, takes them through planning approval and grid connection until they are "shovel-ready" — the industry term is **ready-to-build, or RTB** — and then sells the approved projects to someone else who builds them. Each project is a standalone battery of about **5 megawatts** connected to the local distribution network (the everyday poles-and-wires, not the high-voltage transmission grid), and the projects are spread across New South Wales, Victoria and South Australia. The whole cycle is meant to take two to three years.

This is the most important thing to understand, because it changes which risks matter. A normal battery owner lives or dies on the volatile price of electricity over fifteen or twenty years. This fund is gone before the battery ever switches on, so **that price risk belongs to the buyer, not to us.** Our two real questions are therefore simpler and sharper: **can the fund get its projects approved and connected on time, and will there be buyers willing to pay the assumed prices when it comes time to sell?**

## What the stations are for, who uses them, and how big the market is

*(The committee asked exactly this. Short version: a 5 MW battery is a "community/neighbourhood" battery; the overall storage market is huge, but the 5 MW slice is a distinct, smaller, government-supported segment — and that matters for who will buy it.)*

**What a 5 MW battery does.** A 5 MW distribution-connected battery is, in practice, a **community / neighbourhood battery** — these connect to the local network and are typically up to 5 MW. Its jobs, and who benefits, are:

| What it does | Who uses / benefits |
|---|---|
| Stores the midday rooftop-solar surplus and releases it into the evening peak | Households & local community |
| Supports the local network (voltage, reliability) and defers poles-and-wires upgrades | Distribution network operator (DNSP) |
| Buys power cheap / sells dear (arbitrage) and provides fast frequency services (FCAS) | The wholesale market, via AEMO |
| Firms local solar and wind | Retailers & community |

**Who owns them today — a telling fact.** Almost all existing community/distribution batteries are **owned and operated by the network companies (DNSPs)** or funded by **government programmes** — the federal $200m Community Batteries programme, Victoria's 100 Neighbourhood Batteries, Power Melbourne, and DNSP roll-outs (Ausgrid has commissioned a 5 MW community battery). Most still need a discounted network tariff to stack up financially.

**Is the market big?** Storage demand is large and growing fast — but the 5 MW niche is a *distinct, smaller slice* of it (AEMO 2026 ISP, Step Change scenario):

| Segment | 2026 | 2030 | 2050 |
|---|---|---|---|
| Small-scale / distributed (home + community) | 5 GW | 12 GW | 35 GW |
| Grid-scale (developer-built, ~100 MW+) | ~45 GW in the connections queue | — | ~40 GW of need |

So the demand is real and structural — **but the capital and the deals sit overwhelmingly at the grid-scale (100 MW+) end**, which leads straight to the buyer question below. *(Data stored in [`data/processed/market_demand.csv`](data/processed/market_demand.csv) and [`data/processed/end_use.csv`](data/processed/end_use.csv); sources: AEMO ISP 2026, DNSP/government programmes, trade press — illustrative benchmarks, verify.)*

## Is the market real and growing?

Yes, and for structural rather than fashionable reasons. Australia is closing its ageing coal power stations while adding large amounts of solar and wind. Because solar and wind are intermittent, the grid increasingly needs storage that can deliver power on demand, and batteries are the cheapest and fastest way to provide it for the short durations that matter most today. Governments have backed this with firm targets and subsidy schemes, which turns a physical need into real, financeable demand. Importantly, the amount of storage actually funded still lags well behind the targets, so there is genuine room for new projects.

For a developer who simply wants to build approved projects and sell them, this fast growth is helpful — rising demand means more potential buyers. (The same instability would worry someone planning to own and operate for fifteen years, but that is not this fund.) The one caveat is that the demand rests on government policy, and a two-to-three-year fund is exposed if those policies soften part-way through.

## Is the fund's niche defensible?

Plausibly, but it needs checking. The fund's edge is that it deliberately works on **small ~5 MW projects** that the big developers overlook in favour of large 100 MW-plus transmission projects, which leaves the small end of the market less crowded. There is also a regulatory advantage: projects under 5 MW are exempt from a layer of AEMO registration, which should make approval faster and cheaper. If that exemption holds, and if the fund genuinely has the site access, grid know-how and network-operator relationships it claims, the niche could be defensible. None of that should be taken on trust — it is exactly what diligence must confirm.

## The decisive risk: will there be buyers?

This is the heart of the matter. Because the fund's entire return comes from selling, the strength of the buyer market decides everything. The good news is that the pool of buyers for Australian battery assets is real and well-funded:

- **Independent power producers**, building out their own portfolios
- **Infrastructure funds** — for example Palisade/Intera, Copenhagen Infrastructure Partners, Quinbrook
- **Superannuation funds** — for example Aware Super, HESTA
- **Government green-investment bodies** — the Clean Energy Finance Corporation and the Energy Security Corporation
- **Large energy retailers**, seeking firming capacity

Two cautions dominate, though. First, the fund's "three interested buyers" are **not contractually committed** — interest is not a purchase. Second, and more important, the wider market increasingly pays up for projects that are *further along*, already contracted or construction-ready, whereas this fund sells at the *earlier* RTB stage. So the fund must show either that demand for RTB projects specifically is genuinely deep, or that its projects are de-risked enough to command the assumed prices. The single most useful thing the manager can provide is evidence of real, recent sales of comparable small projects at comparable prices.

**Do buyers actually want 5 MW assets — or do they prefer 100 MW+?** This is the committee's sharpest question, and the recent deal record answers it plainly: **the deep-pocketed buyers transact at scale, not at 5 MW.**

| Recent deal / project | Size | Buyer |
|---|---|---|
| Summerfield BESS (SA) | 240 MW / 960 MWh | Palisade (with CEFC, Aware Super, HESTA) |
| Supernode Stage 1 (QLD) | 260 MW / 619 MWh | Origin (12-year toll) |
| ESC platform (NSW) | 200 MW | Energy Security Corporation |
| Ebor (NSW) | 100 MW / 870 MWh | NSW LTESA tender |
| **A community / distribution battery** | **~5 MW** | **DNSP / government programme / aggregator** |

![Recent BESS deals are large](outputs/figures/buyer_sizes.png)

Infrastructure and super funds say it out loud — Aware Super and HESTA described the 240 MW Summerfield deal as exactly the **"large scale"** infrastructure they want. A single 5 MW project is simply **too small** for them: the due-diligence and management effort is much the same as for a 200 MW asset, so they favour size. The natural buyers of *individual* 5 MW batteries are a **thinner, more specialised, often grant-dependent pool** — DNSPs, government programmes and aggregators.

**The mitigation — and the catch.** The way a small-project developer reaches the big buyers is to **bundle many projects into a portfolio.** The fund's ~35 projects (~175 MW combined) could, aggregated, reach the scale an infrastructure fund wants, and the market increasingly supports aggregation. But that changes the exit: the fund would likely have to **sell the whole portfolio as a single platform** — one large, all-or-nothing transaction — rather than flip 5 MW projects one at a time. That **concentrates** the exit risk rather than removing it, and it only works if the portfolio is deliberately built and marketed as one block. *(Deal data: [`data/processed/deal_sizes.csv`](data/processed/deal_sizes.csv); sources: Energy-Storage.news, pv magazine, Quinbrook, ESC — verify.)*

## Can they execute? The success-rate question

The other make-or-break is whether projects actually clear their hurdles on schedule. We model success as a chain — a project must win planning approval, *then* secure grid connection, *then* find a buyer — and read each step from public data:

| Step | Chance of passing |
|---|---|
| Planning approval | ~80% |
| Grid connection | ~70% |
| Reach a sale | ~80% |
| **All three (multiplied)** | **~45%** |

In other words, only about **45%** of projects started are likely to make it the whole way.

That 45% is the key finding, because the manager's base case assumes **65%**. In plain terms, the fund's central plan looks optimistic on the very variable that matters most, and our independent estimate sits closer to the manager's *conservative* case than its base case. There is a fair counter-argument — the sub-5 MW exemption and the simplicity of small projects might genuinely lift success above the benchmark — so the right response is not to dismiss the fund, but to **ask the manager for project-by-project, state-by-state evidence** of its approval and connection record. Timing is the other enemy: approvals routinely take many months, and if they slip by six to twelve months the returns fall sharply.

## What this means for the returns

(The full figures are in the valuation model; this is the bottom line.) When we rebuild the fund's returns independently — using our own, more cautious success rate and costs — the expected investor return after fees comes out around **13–14%**, below the roughly **18%** the manager's own scenarios imply. More tellingly, the downside is real: in the conservative case the fund can return **less than the money invested**. So the opportunity looks attractive on the manager's numbers and merely adequate on ours, with a genuine risk of loss if execution disappoints.

## Three ways to invest — and which stage to choose

So far this report has assessed **Stage 1 — develop and flip.** But the same projects can be entered at three points on the value chain, and each is a genuinely different investment on a risk ladder: **develop (highest risk) → build (medium) → operate (lowest, if contracted).** Comparing them as risk-adjusted, levered returns on the same ~5 MW asset:

| Stage | Hold | Expected return | Downside | In plain terms |
|---|---|---|---|---|
| 1 — Develop & flip (sell RTB) | ~3 yrs | ~14% | **can lose capital (−3%)** | capital-light, short, but binary |
| 2 — Build & sell | ~1.5 yrs | ~26% | **heavy loss (−18%)** | highest return, but most fragile |
| 3 — Own & operate (contracted) | ~15 yrs | ~8% | **still positive (+4%)** | steady, long, capital-preserving |

![Risk-return by stage](outputs/figures/stage_comparison.png)

**Which stage suits the family trust:**

- **Stage 3 (own & operate, *contracted*) is the natural core.** It is the only stage that stays positive even in its downside — steady, long-dated, capital-preserving yield. It also plays to the trust's credit-risk strength: judging whether the toll/offtake buyer will actually pay is the same as judging whether a borrower can service a loan. Avoid uncontracted, merchant-only assets — that is just betting on electricity prices.
- **Stage 1 (develop & flip) is a smaller, higher-risk satellite** — only on the conditions below.
- **Stage 2 (build & sell) is best skipped on its own.** It shows the highest *expected* return, but it is the most fragile: the profit depends entirely on the finished asset being worth more than it costs to build — a thin, price-dependent margin — and the downside is a heavy loss. It also needs construction expertise the trust does not have.
- **One alignment warning:** the manager keeps "the best 5–10 projects to operate" (Stage 3) and flips the rest, so the flip fund may be left the weaker projects. If the operating economics appeal, ask to **co-invest in the projects they keep.**

*(Full workings — including the levered operating model and merchant-price scenarios — are in [`financial_models/STAGE_COMPARISON.md`](financial_models/STAGE_COMPARISON.md). The figures are illustrative; the Stage 2 result in particular is very sensitive to the build margin.)*

## The verdict

The market is real, growing, policy-supported and well-suited to a small, capital-light fund. The strategy is genuinely investable — **but only conditionally**, because two things the manager's deck cannot prove on its own decide the outcome: a deep and durable pool of buyers for RTB projects, and a realistic success rate. We would not commit on the strength of the deck alone.

Before any commitment, the manager should be asked to provide:

- evidence of **real, recent sales** of comparable small RTB projects at the assumed prices, and whether any of the "interested buyers" are contractually committed;
- its **approval and grid-connection success rates by state**, specifically for sub-5 MW projects, that would reconcile its 65% base case with our ~45% estimate;
- a **bottom-up build-up of the ~$500k development cost** per project;
- the **net-of-all-fees return**, and the gross return behind it;
- what happens to the timeline and returns **if approvals slip by six to twelve months**;
- how the projects it plans to **keep and operate (five to ten of the best)** are chosen, since that affects what is left for investors; and
- the genuine **worst case** — in which scenario could investors lose money?

The single biggest risk is the exit: a project with no buyer is stranded capital. Execution and approval risk come next, and the optimistic success rate compounds both. The thing that usually sinks battery investments — volatile electricity prices — is, for this fund, the buyer's problem rather than ours.

---

## How this assessment was done (methods)

This report uses standard **CFA-curriculum industry-analysis frameworks** alongside the way **private-equity and infrastructure investors screen real deals**. Each conclusion above traces back to one of these methods:

| What we wanted to know | Method used | Where it comes from |
|---|---|---|
| What exactly are we analysing? | Define the industry narrowly *before* analysing it (here: small ~5 MW distribution RTB) | CFA — Industry & Company Analysis |
| Is the industry growing or maturing? | The industry life-cycle model | CFA |
| How tough is the competition? | Porter's Five Forces — applied to the *RTB* market, not electricity | CFA / Michael Porter (Harvard) |
| What outside forces help or hurt? | PESTLE — Political, Economic, Social, Technological, Legal, Environmental | CFA |
| Is this a good *type* of deal? | The PE / VC deal screen — exit path, barriers to entry, capital intensity, recurring revenue | Real-world PE & infrastructure practice |
| Will a project actually succeed? | A survival / "probability-of-default" chain: multiply the chance of clearing each gate | Real-world credit risk (Basel, IFRS 9) |
| What return does it give? | Risk-adjusted NPV, three scenarios weighted (the First-Chicago method), IRR / MOIC | CFA (time value of money, expected value) + PE/VC practice |

In every case the inputs come from **free public data**, and the manager's figures were **re-derived independently** rather than taken on trust. The full quantitative workings are in the [valuation model](financial_models/) and the [README](README.md).

---

*Independent findings draw on free public data (AEMO, CSIRO GenCost, the RBA, and the NSW/VIC/SA planning portals); see [`SOURCES.md`](SOURCES.md). The valuation rebuild that produces the return figures (a survival-curve / risk-adjusted model) lives in [`financial_models/`](financial_models/) and the [`notebooks/`](notebooks/). Manager figures are forward-looking claims and must be independently verified.*
