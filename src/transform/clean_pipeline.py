"""Transform: build the illustrative project pipeline -> data/processed/pipeline.csv

The pipeline is ILLUSTRATIVE (synthetic) but grounded in real NSW/VIC battery
sizes/locations from the AEMO Generation Information list. Project parameters
come from config/assumptions.yaml so they are documented and tunable.
"""
from __future__ import annotations

import csv

from src.utils import io


def run() -> None:
    print("[transform] illustrative pipeline -> pipeline.csv")
    assum = io.load_assumptions()
    pcfg = assum["pipeline"]
    exit_stage = assum["meta"]["exit_stage"]

    grounded = (io.DATA_RAW / "aemo_nswvic_batteries.csv").exists()
    out = io.DATA_PROCESSED / "pipeline.csv"
    with open(out, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["project", "state", "location", "mw", "duration_h", "mwh",
                    "exit_stage", "years_to_sale", "illustrative"])
        for p in pcfg["projects"]:
            mwh = float(p["mw"]) * float(p["duration_h"])
            w.writerow([p["name"], p["state"], p["location"], p["mw"],
                        p["duration_h"], mwh, exit_stage, p["years_to_sale"], "YES"])

    n = len(pcfg["projects"])
    total_mw = sum(p["mw"] for p in pcfg["projects"])
    total_mwh = sum(p["mw"] * p["duration_h"] for p in pcfg["projects"])
    print(f"  -> wrote {out}: {n} projects, {total_mw} MW / {total_mwh:.0f} MWh "
          f"({'grounded in AEMO list' if grounded else 'config-only, AEMO list not downloaded'})")


if __name__ == "__main__":
    run()
