"""Transform: per-gate survival statistics -> data/processed/gate_stats.csv

Combines the staged outputs of the NSW Planning, AEMO Connections, and AEMO
Generation Information extractors (or documented benchmarks when a source was
unreachable) into the three survival-curve gates. Python computes the RAW
per-gate rates; the Excel model builds the cumulative survival curve from them.

Output columns: gate, probability, duration_years, source, as_at, status
"""
from __future__ import annotations

import csv

from src.utils import io

_GATES = [
    ("planning_approval", "planning", "planning_approval"),
    ("grid_connection", "connection", "grid_connection"),
    ("reach_sale", "sale", "reach_sale"),
]


def run() -> None:
    print("[transform] gate statistics -> gate_stats.csv")
    gates_cfg = io.load_assumptions()["gates"]

    out = io.DATA_PROCESSED / "gate_stats.csv"
    cumulative = 1.0
    rows = []
    for gate_name, stage_key, cfg_key in _GATES:
        stage = io.read_stage(stage_key)
        cfg = gates_cfg[cfg_key]
        if stage:
            prob = float(stage["probability"])
            dur = float(stage["duration_years"])
            status = stage.get("status", "BENCHMARK")
            source = stage.get("source", cfg["source"])
            as_at = stage.get("as_at", cfg["as_at"])
        else:
            prob = float(cfg["probability"])
            dur = float(cfg["duration_years"])
            status = "BENCHMARK"
            source = cfg["source"]
            as_at = cfg["as_at"]
        prob = max(0.0, min(1.0, prob))  # guard [0,1]
        cumulative *= prob
        rows.append([gate_name, round(prob, 4), dur, source, as_at, status])

    with open(out, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["gate", "probability", "duration_years", "source", "as_at", "status"])
        w.writerows(rows)

    print(f"  -> wrote {out}: "
          + ", ".join(f"{r[0]}={r[1]}" for r in rows)
          + f"  | cumulative P(success)={cumulative:.3f}")
    print("     (Excel builds the cumulative survival curve from these per-gate rates.)")


if __name__ == "__main__":
    run()
