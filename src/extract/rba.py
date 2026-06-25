"""Extractor: RBA risk-free rate -> data/processed/rates.csv

Strategy (verify-then-fallback):
  1. Download RBA F2 (Capital Market Yields) CSV; parse the latest 10yr CGS yield.
  2. Else download F1.1 (cash rate) CSV; parse the latest cash rate.
  3. Else fall back to the documented benchmark in assumptions.yaml (status BENCHMARK).

Output rates.csv columns: metric, value, unit, source, as_at, status
"""
from __future__ import annotations

import csv
import io as _io

from src.utils import io
from src.utils import sources_log


def _parse_rba_csv(text: str, want_keywords: list[str]) -> tuple[float, str] | None:
    """Best-effort parse of an RBA statistical-table CSV.

    RBA CSVs carry several metadata rows, then a header row of series titles,
    a 'Series ID' row, then dated data rows. We find the column whose title
    contains all `want_keywords`, then return (latest_value, latest_date).
    """
    rows = list(csv.reader(_io.StringIO(text)))
    if not rows:
        return None

    # Find the header row: the one containing a cell with all keywords.
    header_idx, col_idx = None, None
    for i, row in enumerate(rows[:30]):
        for j, cell in enumerate(row):
            low = cell.lower()
            if all(k in low for k in want_keywords):
                header_idx, col_idx = i, j
                break
        if header_idx is not None:
            break
    if col_idx is None:
        return None

    # Walk data rows from the bottom up; first parseable number wins (latest).
    for row in reversed(rows[header_idx + 1:]):
        if len(row) <= col_idx:
            continue
        raw = row[col_idx].strip()
        date = row[0].strip() if row else ""
        if not raw:
            continue
        try:
            return float(raw), date
        except ValueError:
            continue
    return None


def run() -> None:
    print("[extract] RBA risk-free rate")
    src = io.load_sources()["sources"]["rba"]
    assum = io.load_assumptions()["discount_rate"]["risk_free"]

    value: float | None = None
    metric = "risk_free_rate_10yr_cgs"
    status = "BENCHMARK"
    as_at = assum["as_at"]
    note = ""

    # 1. F2 -> 10yr Commonwealth Government bond yield
    dest = io.DATA_RAW / f"rba_f2_{io.today_str()}.csv"
    path = io.cached_download(src["url"], dest, binary=False)
    if path:
        parsed = _parse_rba_csv(path.read_text(encoding="utf-8", errors="ignore"),
                                ["10", "year"])
        if parsed:
            value, as_at = parsed[0] / 100.0 if parsed[0] > 1 else parsed[0], parsed[1]
            status, note = "LIVE", "RBA F2 10yr CGS"

    # 2. Fallback to F1.1 cash rate
    if value is None and src.get("fallback_url"):
        dest2 = io.DATA_RAW / f"rba_f11_{io.today_str()}.csv"
        path2 = io.cached_download(src["fallback_url"], dest2, binary=False)
        if path2:
            parsed = _parse_rba_csv(path2.read_text(encoding="utf-8", errors="ignore"),
                                    ["cash", "rate"])
            if parsed:
                value = parsed[0] / 100.0 if parsed[0] > 1 else parsed[0]
                as_at, metric = parsed[1], "cash_rate"
                status, note = "LIVE", "RBA F1.1 cash rate (10yr CGS unavailable)"

    # 3. Documented benchmark
    if value is None:
        io.manual_download_msg(src["name"], src["landing_page"], dest)
        value = float(assum["value"])
        status, note = "BENCHMARK", "documented benchmark (RBA unreachable)"

    out = io.DATA_PROCESSED / "rates.csv"
    with open(out, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["metric", "value", "unit", "source", "as_at", "status"])
        w.writerow([metric, round(value, 5), "decimal", assum["source"], as_at, status])
    print(f"  -> wrote {out} ({metric}={value:.4f}, {status}: {note})")

    sources_log.record(
        "rba",
        name=src["name"],
        url=src["landing_page"],
        output="data/processed/rates.csv",
        status=status,
        description=src["description"],
    )


if __name__ == "__main__":
    run()
