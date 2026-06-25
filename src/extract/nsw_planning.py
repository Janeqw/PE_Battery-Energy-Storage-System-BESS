"""Extractor: NSW Planning Portal (Major Projects) -> planning-approval gate.

Inspect the Application Tracker for a JSON/REST endpoint first;
else Playwright; else benchmark fallback. Computes the BESS approval rate
(approved / determined) and the lodgement->determination duration.
"""
from __future__ import annotations

import datetime as _dt

from src.utils import io
from src.utils import sources_log

_APPROVED = ("approved", "determined", "granted")
_REJECTED = ("refused", "withdrawn", "rejected", "lapsed")


def _try_api(url: str, query: dict) -> dict | None:
    """Attempt the portal's search API; return parsed gate metrics or None."""
    try:
        sess = io.make_session()
        io.polite_delay()
        resp = sess.get(url, params={"q": "battery energy storage"},
                        timeout=io.load_sources()["http"]["timeout_seconds"])
        resp.raise_for_status()
        data = resp.json()
        records = data if isinstance(data, list) else data.get("results", data.get("items", []))
        approved = rejected = 0
        durations = []
        for rec in records:
            blob = str(rec).lower()
            if "battery" not in blob and "bess" not in blob and "storage" not in blob:
                continue
            status = blob
            if any(s in status for s in _APPROVED):
                approved += 1
            elif any(s in status for s in _REJECTED):
                rejected += 1
            lodged = rec.get("lodgementDate") or rec.get("lodged")
            determined = rec.get("determinationDate") or rec.get("determined")
            if lodged and determined:
                try:
                    d0 = _dt.date.fromisoformat(str(lodged)[:10])
                    d1 = _dt.date.fromisoformat(str(determined)[:10])
                    durations.append((d1 - d0).days / 365.25)
                except Exception:
                    pass
        n = approved + rejected
        if n >= 8:
            return {
                "probability": round(approved / n, 3),
                "duration_years": round(sum(durations) / len(durations), 2) if durations else None,
                "n": n,
            }
        return None
    except Exception as exc:  # noqa: BLE001
        print(f"  [api-fail] NSW Planning: {exc}")
        return None


def run() -> None:
    print("[extract] NSW Planning Portal (Major Projects)")
    src = io.load_sources()["sources"]["nsw_planning"]
    plan_cfg = io.load_assumptions()["gates"]["planning_approval"]

    metrics = None
    status = "BENCHMARK"

    if src.get("url"):
        metrics = _try_api(src["url"], src.get("query", {}))
        if metrics:
            status = "LIVE"

    # (Playwright fallback intentionally not auto-run in the offline build; the
    #  portal is a JS app and needs an interactive session. Message the user.)
    if metrics is None:
        io.manual_download_msg(src["name"], src["landing_page"],
                               io.DATA_RAW / "nsw_planning_<date>.json")
        metrics = {
            "probability": float(plan_cfg["probability"]),
            "duration_years": float(plan_cfg["duration_years"]),
            "n": None,
        }

    duration = metrics["duration_years"] or float(plan_cfg["duration_years"])
    io.write_stage("planning", {
        "probability": metrics["probability"],
        "duration_years": duration,
        "status": status,
        "n": metrics.get("n"),
        "source": plan_cfg["source"],
        "as_at": plan_cfg["as_at"],
    })
    print(f"  -> planning gate p={metrics['probability']} [{status}] (n={metrics.get('n')})")

    sources_log.record(
        "nsw_planning",
        name=src["name"],
        url=src["landing_page"],
        output="data/processed/gate_stats.csv (planning gate)",
        status=status,
        description=src["description"],
    )


if __name__ == "__main__":
    run()
