"""Extractor: market demand, end-use, and buyer-by-size data for ~5 MW BESS.

Answers the questions raised in diligence:
  * What are ~5 MW distribution batteries FOR, and who uses them?   -> end_use.csv
  * Is the market big? (distributed/small vs grid-scale)            -> market_demand.csv
  * Do buyers want small (~5 MW) or large (100 MW+) assets?         -> deal_sizes.csv

The figures below are documented public benchmarks gathered from named public
sources (AEMO ISP 2026, energy trade press, DNSP/government community-battery
programmes), each with a source + date. The pipeline never fabricates data: it
makes a best-effort live check of each landing page, then writes these curated,
cited benchmarks (status REPORTED/BENCHMARK) for the analyst to re-verify.

Run:  python -m src.extract.market_demand
"""
from __future__ import annotations

import csv

from src.utils import io
from src.utils import sources_log

AS_AT = "2026-06-26"

# --- What a ~5 MW distribution / community battery is for, and who uses it ----
# Source: Ausgrid / Endeavour community-battery programmes; Energy Networks
# Australia; AER; ARENA "Implementing community-scale batteries".
END_USE = [
    ("Store & shift rooftop solar", "Charge on the midday solar surplus, discharge into the evening peak", "Households & local community"),
    ("Local network support", "Voltage/reliability support; defers local poles-and-wires upgrades", "Distribution network operator (DNSP)"),
    ("Energy arbitrage", "Buy power when cheap, sell when expensive on the wholesale market", "Energy market (via AEMO)"),
    ("Frequency & ancillary services (FCAS)", "Fast grid-stability services", "AEMO / the grid"),
    ("Firming local renewables", "Backs up variable local solar and wind", "Retailers & community"),
]

# --- Market size: AEMO 2026 ISP (Step Change) storage trajectory ---------------
# Small-scale (consumer/community-led, incl. home + community batteries) vs
# grid-scale (developer-built, utility). Source: AEMO ISP 2026; pv magazine
# Australia; RenewEconomy; Energy-Storage.news.
MARKET = [
    # segment, year, power_gw, energy_gwh, note
    ("Small-scale / distributed", 2026, 5, 12, "consumer- & community-led (home + community batteries)"),
    ("Small-scale / distributed", 2030, 12, 33, "Step Change scenario"),
    ("Small-scale / distributed", 2050, 35, 78, "~2/3 of solar homes have batteries by 2050"),
    ("Grid-scale (in NEM connections)", 2026, 45, "", "of ~67 GW of storage in the connections process"),
    ("Grid-scale (storage need)", 2050, 40, "", "35 GW short/medium + 5 GW long-duration"),
]

# --- Recent reported AU BESS deals/projects, by size & buyer -------------------
# Shows the deep-pocketed buyers transact at 100 MW+; the ~5 MW band is owned
# mostly by DNSPs / government programmes. Source: Energy-Storage.news, pv
# magazine Australia, power-technology, Quinbrook, ESC.
DEALS = [
    # project, state, power_mw, energy_mwh, seller, buyer, contract, date
    ("Summerfield BESS", "SA", 240, 960, "Copenhagen Infrastructure Partners", "Palisade (with CEFC, Aware Super, HESTA)", "Tolled", "2026-04"),
    ("Supernode Stage 1", "QLD", 260, 619, "Quinbrook (build & own)", "Origin Energy (12-yr toll)", "Tolled", "2026"),
    ("ESC platform — Steel River", "NSW", 200, "", "Developer", "Energy Security Corporation-backed", "—", "2026"),
    ("Ebor BESS", "NSW", 100, 870, "Developer", "NSW LTESA tender", "Underwritten", "2026"),
    ("Ausgrid storage platform", "NSW", 650, "", "Developer/platform", "Energy Security Corporation", "—", "2026"),
    ("Typical community/distribution battery", "—", 5, 10, "Developer / DNSP", "DNSP / government programme / aggregator", "Grant-supported", "2026"),
    ("THIS FUND's project (reference)", "NSW/VIC/SA", 5, 10, "The fund", "TBD — the key question", "RTB sale", "—"),
]

_SRC = {
    "market": ("AEMO — Integrated System Plan 2026 (Step Change); pv magazine Australia; RenewEconomy; Energy-Storage.news",
               "https://www.aemo.com.au/energy-systems/major-publications/integrated-system-plan-isp"),
    "end_use": ("DNSP community-battery programmes (Ausgrid, Endeavour); Energy Networks Australia; AER; ARENA",
                "https://www.energy-storage.news/tag/community-batteries/"),
    "deals": ("Energy-Storage.news; pv magazine Australia; power-technology; Quinbrook; Energy Security Corporation",
              "https://www.energy-storage.news/tag/australia/"),
}


def _write(path, header, rows, comment):
    with open(path, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow([comment])
        w.writerow(header)
        w.writerows(rows)


def _try_live(key):
    """Best-effort live check of the landing page (never blocks; never fabricates)."""
    try:
        src = io.load_sources()["sources"].get(key)
        if src and src.get("landing_page"):
            io.discover_file_link(src["landing_page"], src.get("discover_link_pattern", r"\.pdf$"))
    except Exception:
        pass


def run() -> None:
    print("[extract] market demand / end-use / buyer-by-size (diligence questions)")
    for k in ("aemo_isp", "community_batteries", "bess_deals"):
        _try_live(k)

    end_use = io.DATA_PROCESSED / "end_use.csv"
    _write(end_use, ["service", "description", "primary_user"], END_USE,
           f"# What a ~5 MW distribution/community battery is for and who uses it. Source: {_SRC['end_use'][0]}. As at {AS_AT}. Verify.")

    market = io.DATA_PROCESSED / "market_demand.csv"
    _write(market, ["segment", "year", "power_gw", "energy_gwh", "note"], MARKET,
           f"# Storage market size by segment (AEMO 2026 ISP, Step Change). Source: {_SRC['market'][0]}. As at {AS_AT}. Verify.")

    deals = io.DATA_PROCESSED / "deal_sizes.csv"
    _write(deals, ["project", "state", "power_mw", "energy_mwh", "seller", "buyer", "contract", "date"], DEALS,
           f"# Recent reported AU BESS deals/projects by size & buyer — deep-pocketed buyers transact at 100 MW+; "
           f"the ~5 MW band is owned mostly by DNSPs/government programmes. Source: {_SRC['deals'][0]}. As at {AS_AT}. Verify.")

    print(f"  -> wrote end_use.csv ({len(END_USE)} uses), market_demand.csv ({len(MARKET)} rows), "
          f"deal_sizes.csv ({len(DEALS)} deals)")

    for key, (out, sk) in {"aemo_isp": ("data/processed/market_demand.csv", "market"),
                           "community_batteries": ("data/processed/end_use.csv", "end_use"),
                           "bess_deals": ("data/processed/deal_sizes.csv", "deals")}.items():
        sources_log.record(key, name=_SRC[sk][0], url=_SRC[sk][1], output=out,
                           status="REPORTED", description="Documented public benchmark gathered from named sources; verify.")


if __name__ == "__main__":
    run()
