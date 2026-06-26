"""Transform: RTB (development-rights) $/MW by state -> data/processed/rtb_comps.csv

The fund sells shovel-ready (RTB) development rights, so the comp that matters is
the RTB sale price per MW by state. These seed from documented benchmarks that
mirror the MANAGER'S (the manager's) assumed prices — they are CLAIMS to verify with
independent comps. We do NOT scrape prices automatically (RTB pricing needs
judgement); the trade_press extractor only surfaces candidate links for curation.
Any human-curated real deals in data/processed/rtb_comps_curated.csv are appended.

Output columns: state, price_per_mw_m, source, as_at, status
"""
from __future__ import annotations

import csv

from src.utils import io

_STATES = ["NSW", "VIC", "SA"]


def run() -> None:
    print("[transform] RTB $/MW by state -> rtb_comps.csv")
    comps = io.load_assumptions()["rtb_comps_per_mw_m"]

    rows = []
    for state in _STATES:
        rows.append([state, float(comps[state]), comps["source"], comps["as_at"], "BENCHMARK"])

    # Append human-curated real RTB deals if present (status CURATED).
    curated = io.DATA_PROCESSED / "rtb_comps_curated.csv"
    n_curated = 0
    if curated.exists():
        with open(curated, newline="", encoding="utf-8") as fh:
            for rec in csv.DictReader(fh):
                if rec.get("state") and rec.get("price_per_mw_m"):
                    rows.append([rec["state"], float(rec["price_per_mw_m"]),
                                 rec.get("source", "curated"), rec.get("as_at", ""), "CURATED"])
                    n_curated += 1

    out = io.DATA_PROCESSED / "rtb_comps.csv"
    with open(out, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["# RTB / development-rights $/MW by state. the manager's assumed prices "
                    "are CLAIMS; independent comps needed. Paid DBs (BNEF, Enerdatics, "
                    "Mergermarket) out of scope. Values illustrative."])
        w.writerow(["state", "price_per_mw_m", "source", "as_at", "status"])
        w.writerows(rows)
    print(f"  -> wrote {out}: {len(_STATES)} state benchmarks, {n_curated} curated deal(s)")


if __name__ == "__main__":
    run()
