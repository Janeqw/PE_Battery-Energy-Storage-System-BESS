"""Extractor: AEMO Connections Scorecard / KCI -> grid-connection gate.

Computes (or falls back to) the RTB-stage connection-RIGHTS probability and typical
duration, staged for gate_statistics.py. The gate is the development milestone —
securing a connection AGREEMENT + GPS (ready-for-construction) — NOT energisation of
a built battery; the parser rejects commissioning / full-output figures. The
scorecard is published as PDF/XLSX whose layout varies, so parsing is best-effort
with a documented benchmark fallback.
"""
from __future__ import annotations

import re

from src.utils import io
from src.utils import sources_log


def _try_parse_pdf_rate(pdf_path) -> float | None:
    """Best-effort: find the RTB-stage connection-AGREEMENT rate in the Scorecard text.

    The gate is the development milestone — application -> executed connection
    AGREEMENT + GPS (ready-for-construction) — NOT commissioning/energisation. So we
    accept a % only where the context is the agreement/registration stage, and reject
    anything near 'commission' / 'energis' / 'full output' (the downstream, WRONG
    milestone — e.g. the Scorecard's '~75% commissioned to full output').
    """
    try:
        import pdfplumber

        with pdfplumber.open(pdf_path) as pdf:
            text = "\n".join((page.extract_text() or "") for page in pdf.pages[:20])
        WRONG = ("commission", "energis", "energiz", "full output", "full capacity")
        RIGHT = ("connection agreement", "executed connection", "registration",
                 "ready for construction", "ready-to-build", "gps", "generator performance")
        for m in re.finditer(r"(\d{1,3})\s?%", text):
            ctx = text[max(0, m.start() - 80): m.start()].lower()
            if any(w in ctx for w in WRONG):
                continue
            if any(w in ctx for w in RIGHT):
                pct = int(m.group(1))
                if 20 <= pct <= 99:
                    return round(pct / 100.0, 3)
        return None
    except Exception as exc:  # noqa: BLE001
        print(f"  [parse-fail] AEMO connections: {exc}")
        return None


def run() -> None:
    print("[extract] AEMO Connections Scorecard / KCI")
    src = io.load_sources()["sources"]["aemo_connections"]
    conn_cfg = io.load_assumptions()["gates"]["grid_connection"]

    prob = None
    status = "BENCHMARK"

    link = io.discover_file_link(src["landing_page"], src["discover_link_pattern"])
    if link:
        ext = ".pdf" if link.lower().endswith("pdf") else ".xlsx"
        dest = io.DATA_RAW / f"aemo_connections_{io.today_str()}{ext}"
        path = io.cached_download(link, dest, binary=True)
        if path and ext == ".pdf":
            prob = _try_parse_pdf_rate(path)
            if prob is not None:
                status = "LIVE"

    if prob is None:
        io.manual_download_msg(src["name"], src["landing_page"],
                               io.DATA_RAW / "aemo_connections_<date>")
        prob = float(conn_cfg["probability"])

    io.write_stage("connection", {
        "probability": prob,
        "duration_years": float(conn_cfg["duration_years"]),
        "status": status,
        "source": conn_cfg["source"],
        "as_at": conn_cfg["as_at"],
    })
    print(f"  -> connection gate p={prob} [{status}]")

    sources_log.record(
        "aemo_connections",
        name=src["name"],
        url=src["landing_page"],
        output="data/processed/gate_stats.csv (connection gate)",
        status=status,
        description=src["description"],
    )


if __name__ == "__main__":
    run()
