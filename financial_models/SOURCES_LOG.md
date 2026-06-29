# Sources log (model data lineage)

_Auto-generated model output (`src/utils/sources_log.py`) — the full data lineage behind the model. The narrative methods & sources live in [`../IC_MEMO.md`](../IC_MEMO.md) (Appendix A); this file is the machine-generated ledger it points to. Every model input traces to a source + date below. Status shows whether the value was freshly downloaded or fell back to a documented public benchmark to be verified._

_Last updated: 2026-06-26_

| Source | Output | Status | Retrieved | Description |
|---|---|---|---|---|
| [AEMO — Connections Scorecard / Key Connection Information (KCI)](https://www.aemo.com.au/energy-systems/electricity/national-electricity-market-nem/connections) | `data/processed/gate_stats.csv (connection gate)` | 🟡 documented benchmark (verify) | 2026-06-24 | Grid-connection success rate and typical duration -> the connection gate probability and timing. |
| [AEMO — NEM Generation Information](https://www.aemo.com.au/energy-systems/electricity/national-electricity-market-nem/nem-forecasting-and-planning/forecasting-and-planning-data/generation-information) | `data/processed/pipeline.csv, gate_stats.csv (sale gate)` | 🟡 documented benchmark (verify) | 2026-06-24 | Full NEM project list (existing / committed / proposed). Filtered to NSW & VIC batteries to ground the illustrative pipeline, and to measure proposed->committed attrition. |
| [AEMO — Integrated System Plan 2026 (Step Change); pv magazine Australia; RenewEconomy; Energy-Storage.news](https://www.aemo.com.au/energy-systems/major-publications/integrated-system-plan-isp) | `data/processed/market_demand.csv` | 📄 reported (public sources — verify) | 2026-06-26 | Documented public benchmark gathered from named sources; verify. |
| [Energy-Storage.news; pv magazine Australia; power-technology; Quinbrook; Energy Security Corporation](https://www.energy-storage.news/tag/australia/) | `data/processed/deal_sizes.csv` | 📄 reported (public sources — verify) | 2026-06-26 | Documented public benchmark gathered from named sources; verify. |
| [DNSP community-battery programmes (Ausgrid, Endeavour); Energy Networks Australia; AER; ARENA](https://www.energy-storage.news/tag/community-batteries/) | `data/processed/end_use.csv` | 📄 reported (public sources — verify) | 2026-06-26 | Documented public benchmark gathered from named sources; verify. |
| [CSIRO — GenCost (annual, with AEMO)](https://www.csiro.au/en/research/technology-space/energy/energy-data-modelling/gencost) | `data/processed/costs.csv` | 🟡 documented benchmark (verify) | 2026-06-26 | Authoritative Australian battery capital cost ($/kWh, $/kW) by duration. Feeds build-cost inputs. |
| [NSW Planning Portal — Major Projects / Application Tracker](https://www.planningportal.nsw.gov.au/major-projects) | `data/processed/gate_stats.csv (planning gate)` | 🟡 documented benchmark (verify) | 2026-06-24 | BESS major-project applications: name, capacity, status, lodgement & determination dates -> planning approval rate + timeline. Public submissions readable per project. |
| [RBA — Cash Rate Target & Capital Market Yields](https://www.rba.gov.au/statistics/cash-rate/) | `data/processed/rates.csv` | 🟢 live download | 2026-06-24 | Risk-free rate: Australian 10-year Commonwealth Government Securities yield (F2); cash rate (F1.1) as cross-check. Feeds the model discount rate. |
| [Energy trade press — battery M&A / deal comps](https://www.energy-storage.news/tag/australia/) | `data/raw/trade_press_candidates_<date>.csv -> data/processed/rtb_comps.csv` | 🟢 live download | 2026-06-24 | Publicly reported battery deals -> $/MW comps by development stage. Richest databases (BNEF, Enerdatics, Mergermarket) are PAID and out of scope; comps rely on publicly reported deals (stated as a limitation). |

## Status legend

- 🟢 **live download** — file fetched from the source this run.
- 🟡 **documented benchmark (verify)** — source unreachable at run time; the model used a documented public benchmark (from `config/assumptions.yaml` or the extractor). Re-run `make extract` with network access to refresh.
- 📄 **reported (public sources — verify)** — figures compiled from named public reports / trade press (e.g. AEMO ISP, deal announcements); re-verify against the cited source.
- 🔴 **manual download required** — the source needs a manual step (see the extractor's printed instructions).

## Honesty notes

- The valued company is **illustrative (synthetic)**, built from real public project sizes/locations. It is not a real company.
- Comps rely on **publicly reported deals** only. The richest deal databases (BloombergNEF, Enerdatics, Mergermarket) are paid and out of scope — a transparent limitation, not a hidden gap.
- This is an **illustrative** analysis and **not investment advice**; no real company, person or transaction is identified.
