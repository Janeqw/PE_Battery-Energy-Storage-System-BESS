# raw/ — original source documents (verification archive)

Original source documents, downloaded for verification. Each file is mapped to the
processed data it backs in [`../financial_models/SOURCES_LOG.md`](../financial_models/SOURCES_LOG.md) —
open the log, click through to the raw document, and check the number at source.

**Naming convention:** `<publisher>-<topic>-<YYYY-MM>.<ext>`, lowercase, dated.

## Committed here (small, and a rolling source)

| File | Size | Backs | Source |
|---|---|---|---|
| `rba-cgs-10yr-2026-06.csv` | 134 KB | `rates.csv` — 10-yr CGS yield (4.776% on 17 Jun 2026) | RBA Statistical Table F2 (Capital Market Yields – Government Bonds – **daily**) |

Only the RBA CSV is committed. It is small, and F2 is a **rolling daily table** the
RBA overwrites — the live URL no longer shows the 17 Jun 2026 value, so the archived
snapshot is the only way to check it at source. (RBA's monthly table, F2.1, would not
work here: it only carries month-end values, not the 17 Jun daily reading.) RBA's
fixed trailing blank-row padding has been stripped from the committed copy.

## Fetched locally, not committed (large official PDFs)

| File | Size | Backs | Source |
|---|---|---|---|
| `csiro-gencost-2025-26.pdf` | 2.2 MB | `costs.csv` / `stages.build_cost` — 2-hr battery cost | CSIRO GenCost 2025-26 consultation draft |
| `aemo-2026-isp.pdf` | 7.3 MB | `market_demand.csv` — storage capacity (Step Change) | AEMO 2026 Integrated System Plan (141 pp) |

These two PDFs (~9.5 MB) are **gitignored** to keep the repo lean. They are static,
freely-downloadable publications at stable URLs, so the verification trail links
straight to them. Run `bash raw/download.sh` to fetch local copies into this folder
(they will not be committed). If you ever do want them in the repo, use **Git LFS**
rather than committing the blobs to history.

## NOT archived here (and why)

- **AEMO generator-registration exemption** (the sub-5 MW edge) — official page, but
  the download 302-redirects to an HTML page, not a file. Cite the URL in the log;
  fetch via a browser if a file copy is needed.
- **CER connections pipeline** (the 32 GW vs 7.3 GW attrition finding) — the exact
  data file URL was not pinned down here; cite the CER pipeline page in the log and
  attach the file when located locally.
- **Deal comps** (Summerfield, Supernode, Ebor) — these are **private-company**
  transactions, so there is no ASX filing. The primary is each company's own press
  release (a web page), corroborated by trade press. We **do not copy news-article
  text** into the repo; the log records the official company-release / news URLs.
- **Manager deck / Information Memorandum** — the source of the *Proposed (manager)*
  figures (RTB price, dev cost). It is a **confidential third-party document**: held
  offline, **gitignored**, never committed. Logged as "manager deck — confidential,
  held offline."

## Reproduce the archive

Run `bash raw/download.sh` locally (needs internet; uses a browser user-agent —
AEMO blocks the default curl agent). It re-fetches the official documents above.
