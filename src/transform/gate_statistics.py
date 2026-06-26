"""Transform: per-gate survival statistics -> data/processed/gate_stats.csv

CORRECTED GATE LOGIC: each lifecycle gate is separate. This writes the three
flip gates as independent public-data benchmarks:
  development_approval (the gate the SCENARIOS move; 40/65/80% are the manager's
  claim — here we record the independent ~80% benchmark), grid_connection, and
  reach_sale. The Stage-1 flip success is their PRODUCT (computed downstream),
  NOT the 65% headline.

Output columns: gate, probability, duration_years, source, as_at, status
"""
from __future__ import annotations

import csv

from src.utils import io

# gate_name, staged-json key, config key, config field for the probability
_GATES = [
    ("development_approval", "planning", "development_approval", "independent"),
    ("grid_connection", "connection", "grid_connection", "probability"),
    ("reach_sale", "sale", "reach_sale", "probability"),
]


def run() -> None:
    print("[transform] gate statistics -> gate_stats.csv (separate gates; flip success = their product)")
    gates_cfg = io.load_assumptions()["gates"]

    out = io.DATA_PROCESSED / "gate_stats.csv"
    rows, product = [], 1.0
    for gate_name, stage_key, cfg_key, prob_field in _GATES:
        stage = io.read_stage(stage_key)
        cfg = gates_cfg[cfg_key]
        if stage:
            prob = float(stage["probability"]); dur = float(stage["duration_years"])
            status = stage.get("status", "BENCHMARK"); source = stage.get("source", cfg["source"]); as_at = stage.get("as_at", cfg["as_at"])
        else:
            prob = float(cfg[prob_field]); dur = float(cfg["duration_years"])
            status = "BENCHMARK"; source = cfg["source"]; as_at = cfg["as_at"]
        prob = max(0.0, min(1.0, prob))
        product *= prob
        rows.append([gate_name, round(prob, 4), dur, source, as_at, status])

    with open(out, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["gate", "probability", "duration_years", "source", "as_at", "status"])
        w.writerows(rows)

    print("  -> wrote " + ", ".join(f"{r[0]}={r[1]}" for r in rows))
    print(f"     flip success at the public-benchmark approval rate = {product:.3f} "
          f"(the manager's 65% is the APPROVAL gate alone, not this product)")


if __name__ == "__main__":
    run()
