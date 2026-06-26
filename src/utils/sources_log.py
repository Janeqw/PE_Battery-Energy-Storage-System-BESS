"""Sources-log writer — a transparent log of every source the pipeline touched.

Each extractor calls `record(...)` once. Records accumulate to a JSON ledger
(data/processed/_sources_log.json) so re-running one extractor updates only its
own row, then `write_markdown()` renders the committed model output
financial_models/SOURCES_LOG.md (linked from IC_MEMO.md, Appendix A).

This delivers the project's "source honesty": every input traces to a
source + date, and the status column makes clear whether a value is LIVE
(freshly downloaded) or a documented BENCHMARK fallback.
"""
from __future__ import annotations

import datetime as _dt
import json
from pathlib import Path

from .io import DATA_PROCESSED, PROJECT_ROOT

_LEDGER = DATA_PROCESSED / "_sources_log.json"


def _load() -> dict:
    if _LEDGER.exists():
        try:
            return json.loads(_LEDGER.read_text(encoding="utf-8"))
        except Exception:
            return {}
    return {}


def record(
    key: str,
    *,
    name: str,
    url: str | None,
    output: str,
    status: str,
    description: str,
    retrieved: str | None = None,
) -> None:
    """Record one source. `status` in {LIVE, BENCHMARK, REPORTED, MANUAL_REQUIRED}."""
    ledger = _load()
    ledger[key] = {
        "name": name,
        "url": url or "",
        "output": output,
        "status": status,
        "description": description,
        "retrieved": retrieved or _dt.date.today().isoformat(),
    }
    _LEDGER.write_text(json.dumps(ledger, indent=2), encoding="utf-8")
    write_markdown()


_STATUS_BADGE = {
    "LIVE": "🟢 live download",
    "BENCHMARK": "🟡 documented benchmark (verify)",
    "REPORTED": "📄 reported (public sources — verify)",
    "MANUAL_REQUIRED": "🔴 manual download required",
}


def write_markdown() -> None:
    ledger = _load()
    lines: list[str] = []
    lines.append("# Sources log (model data lineage)")
    lines.append("")
    lines.append(
        "_Auto-generated model output (`src/utils/sources_log.py`) — the full data "
        "lineage behind the model. The narrative methods & sources live in "
        "[`../IC_MEMO.md`](../IC_MEMO.md) (Appendix A); this file is the machine-generated "
        "ledger it points to. Every model input traces to a source + date below. Status "
        "shows whether the value was freshly downloaded or fell back to a documented "
        "public benchmark to be verified._"
    )
    lines.append("")
    lines.append(f"_Last updated: {_dt.date.today().isoformat()}_")
    lines.append("")
    lines.append("| Source | Output | Status | Retrieved | Description |")
    lines.append("|---|---|---|---|---|")
    for _key, rec in sorted(ledger.items()):
        badge = _STATUS_BADGE.get(rec["status"], rec["status"])
        url = rec["url"]
        name = f"[{rec['name']}]({url})" if url else rec["name"]
        lines.append(
            f"| {name} | `{rec['output']}` | {badge} | {rec['retrieved']} | {rec['description']} |"
        )
    lines.append("")
    lines.append("## Status legend")
    lines.append("")
    lines.append("- 🟢 **live download** — file fetched from the source this run.")
    lines.append(
        "- 🟡 **documented benchmark (verify)** — source unreachable at run time; the "
        "model used a documented public benchmark (from `config/assumptions.yaml` or the "
        "extractor). Re-run `make extract` with network access to refresh."
    )
    lines.append(
        "- 📄 **reported (public sources — verify)** — figures compiled from named public "
        "reports / trade press (e.g. AEMO ISP, deal announcements); re-verify against the cited source."
    )
    lines.append(
        "- 🔴 **manual download required** — the source needs a manual step "
        "(see the extractor's printed instructions)."
    )
    lines.append("")
    lines.append("## Honesty notes")
    lines.append("")
    lines.append(
        "- The valued company is **illustrative (synthetic)**, built from real public "
        "project sizes/locations. It is not a real company."
    )
    lines.append(
        "- Comps rely on **publicly reported deals** only. The richest deal databases "
        "(BloombergNEF, Enerdatics, Mergermarket) are paid and out of scope — a "
        "transparent limitation, not a hidden gap."
    )
    lines.append(
        "- This is an educational portfolio artefact and **not investment advice**."
    )
    out = PROJECT_ROOT / "financial_models" / "SOURCES_LOG.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
