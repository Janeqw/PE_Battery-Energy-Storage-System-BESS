"""Extractor: AEMO Connections Scorecard / KCI -> grid-connection gate.

Computes (or falls back to) the grid-connection success probability and typical
duration, staged for gate_statistics.py. The scorecard is published as PDF/XLSX
whose layout varies, so parsing is best-effort with a documented benchmark fallback.
"""
from __future__ import annotations

import re

from src.utils import io
from src.utils import sources_log


def _try_parse_pdf_rate(pdf_path) -> float | None:
    """Best-effort: find a connection-completion percentage in the PDF text."""
    try:
        import pdfplumber

        with pdfplumber.open(pdf_path) as pdf:
            text = "\n".join((page.extract_text() or "") for page in pdf.pages[:20])
        # look for "... connection ... NN%" patterns
        for m in re.finditer(r"(\d{1,3})\s?%", text):
            ctx = text[max(0, m.start() - 60): m.start()].lower()
            if "connect" in ctx or "complet" in ctx or "success" in ctx:
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
