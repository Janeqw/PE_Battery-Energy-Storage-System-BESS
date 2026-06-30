# Sources log (model data lineage)

_Auto-generated model output (`src/utils/sources_log.py`) — the full data lineage behind the model. The narrative methods & sources live in [`../IC_MEMO.md`](../IC_MEMO.md) (Appendix A); this file is the machine-generated ledger it points to. Every model input traces to a source + date below. Status shows whether the value was freshly downloaded or fell back to a documented public benchmark to be verified._

_Last updated: 2026-06-30_

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

## Verification trail (raw documents)

_Each verified figure maps to a raw document in [`../raw/`](../raw/) — open it to check the number at source. **✓** = archived in the repo; **(download.sh)** = a large PDF kept out of the repo to stay lean, fetched locally via [`../raw/download.sh`](../raw/download.sh); **—** = cannot be archived (reason given), so the URL is the click-through. Verified 30 Jun 2026._

| Processed figure | Value | Raw doc | Where in the doc | Source URL | Provenance |
|---|---|---|---|---|---|
| Small-scale storage (2030) | 12 GW / 33 GWh | `raw/aemo-2026-isp.pdf` (download.sh) | Storage capacity, Step Change (consumer/distributed) | [AEMO 2026 ISP](https://www.aemo.com.au/energy-systems/major-publications/integrated-system-plan-isp/2026-integrated-system-plan-isp) | Independent (verified) |
| Grid-scale storage need (2050) | ~40 GW (35 + 5) | `raw/aemo-2026-isp.pdf` (download.sh) | Storage capacity, Step Change | [AEMO 2026 ISP](https://www.aemo.com.au/energy-systems/major-publications/integrated-system-plan-isp/2026-integrated-system-plan-isp) | Independent (verified) |
| Grid-scale storage in connections | ~45 GW of ~67 GW | `raw/aemo-2026-isp.pdf` (download.sh) | Connections / transition outlook | [AEMO 2026 ISP](https://www.aemo.com.au/energy-systems/major-publications/integrated-system-plan-isp/2026-integrated-system-plan-isp) | Independent (verified) |
| 10-year CGS yield | 4.776% (17 Jun 2026) | `raw/rba-cgs-10yr-2026-06.csv` ✓ | column "Australian Government 10 year bond", row 17-Jun-2026 = 4.776 (RBA table F2, daily) | [RBA Statistical Tables](https://www.rba.gov.au/statistics/tables/) | Independent (verified) |
| 2-hour battery build cost | ~$525/kWh (~$1.05m/MW) | `raw/csiro-gencost-2025-26.pdf` (download.sh) | current capital-cost tables, 2-hr battery | [CSIRO GenCost](https://www.csiro.au/en/research/technology-space/energy/energy-data-modelling/gencost) | Independent (verified) |
| Sub-5 MW registration exemption | real (the structural edge) | — (AEMO page 302-redirects; not archived) | generator-registration exemption guidance | [AEMO exemption](https://www.aemo.com.au/energy-systems/electricity/national-electricity-market-nem/participate-in-the-market/registration/exemption-from-registering-as-a-generator-in-the-nem) | Independent (verified) |
| Connection attrition | ~32 GW probable vs 7.3 GW committed | — (CER data file not pinned; fetch locally) | connections / generation pipeline, May 2026 | [CER reports & data](https://cer.gov.au/markets/reports-and-data) | Independent (verified) |
| Summerfield comp | 240 MW / 960 MWh | — (private deal; company release, not archived) | CIP -> Palisade, Origin toll, Apr 2026 | [release / trade press](https://www.energy-storage.news/copenhagen-infrastructure-partners-sells-960mwh-summerfield-battery-to-palisade-in-south-australia/) | Independent (verified) |
| Supernode Stage 1 comp | 260 MW / 619 MWh | — (private deal; company release, not archived) | Quinbrook, Origin 12-yr toll, QLD | [Quinbrook release](https://www.quinbrook.com/news-insights/supernode-stage-1-commences-commercial-operations/) | Independent (verified) |
| Ebor comp | 100 MW / 870 MWh | — (private deal; company release, not archived) | NSW LTESA award, Feb 2026 | [trade press](https://www.pv-magazine-australia.com/2026/02/10/100-mw-870-mwh-ebor-battery-wins-long-storage-nsw-tender/) | Independent (verified) |
| RTB sale price; dev cost | NSW $0.20m/MW; ~$0.5m/project | — (manager deck — confidential, held offline) | n/a | n/a | Proposed (manager) |
| Built-asset value (context) | $1.8m/MW | — (no primary; GenCost cell cost is ~$1.1m/MW) | n/a | n/a | Placeholder `[[TO CONFIRM]]` |

- **Page/table locators** are given by section/figure name, not invented page numbers — open the doc and search the named table.
- **News article text is not copied** into the repo; for private-company deals only the official-release / trade-press URL is recorded (the primary is each company's own release).
- **The manager deck is confidential** and gitignored — it is never committed; its figures stay `Proposed (manager)` and unverifiable by design.

## Status legend

- 🟢 **live download** — file fetched from the source this run.
- 🟡 **documented benchmark (verify)** — source unreachable at run time; the model used a documented public benchmark (from `config/assumptions.yaml` or the extractor). Re-run `make extract` with network access to refresh.
- 📄 **reported (public sources — verify)** — figures compiled from named public reports / trade press (e.g. AEMO ISP, deal announcements); re-verify against the cited source.
- 🔴 **manual download required** — the source needs a manual step (see the extractor's printed instructions).

## Honesty notes

- The valued company is **illustrative (synthetic)**, built from real public project sizes/locations. It is not a real company.
- Comps rely on **publicly reported deals** only. The richest deal databases (BloombergNEF, Enerdatics, Mergermarket) are paid and out of scope — a transparent limitation, not a hidden gap.
- This is an **illustrative** analysis and **not investment advice**; no real company, person or transaction is identified.
