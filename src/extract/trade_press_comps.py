"""Extractor: energy trade press -> battery-deal candidate links (for curation).

Comps are SEMI-AUTOMATED by design: we discover keyword-matched article links from
free trade press into a candidates file; a human then curates actual RTB deal
prices/stages into data/processed/rtb_comps_curated.csv (build_comps.py seeds
rtb_comps.csv from documented benchmarks). We never fabricate deal prices from headlines.
"""
from __future__ import annotations

import csv

from src.utils import io
from src.utils import sources_log


def _discover_candidates(feed: dict, keywords: list[str]) -> list[dict]:
    try:
        from bs4 import BeautifulSoup

        sess = io.make_session()
        io.polite_delay()
        resp = sess.get(feed["url"], timeout=io.load_sources()["http"]["timeout_seconds"])
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "lxml")
        out = []
        seen = set()
        for a in soup.find_all("a", href=True):
            title = a.get_text(strip=True)
            href = a["href"]
            if not title or href in seen:
                continue
            low = title.lower()
            matched = [k for k in keywords if k.lower() in low]
            if len(matched) >= 2:  # require >=2 keyword hits to reduce noise
                seen.add(href)
                out.append({
                    "source": feed["name"],
                    "title": title,
                    "url": href if href.startswith("http") else feed["url"].split("/?")[0] + href,
                    "matched_keywords": ";".join(matched),
                })
        return out
    except Exception as exc:  # noqa: BLE001
        print(f"  [feed-fail] {feed['name']}: {exc}")
        return []


def run() -> None:
    print("[extract] Trade-press battery-deal candidates")
    src = io.load_sources()["sources"]["trade_press_comps"]
    keywords = src.get("keywords", [])

    candidates: list[dict] = []
    for feed in src.get("feeds", []):
        rows = _discover_candidates(feed, keywords)
        print(f"    {feed['name']}: {len(rows)} candidate link(s)")
        candidates.extend(rows)

    status = "LIVE" if candidates else "BENCHMARK"
    out = io.DATA_RAW / f"trade_press_candidates_{io.today_str()}.csv"
    with open(out, "w", newline="", encoding="utf-8") as fh:
        w = csv.writer(fh)
        w.writerow(["source", "title", "url", "matched_keywords"])
        for c in candidates:
            w.writerow([c["source"], c["title"], c["url"], c["matched_keywords"]])

    if not candidates:
        io.manual_download_msg(src["name"], src["feeds"][0]["url"] if src.get("feeds") else None, out)
    print(f"  -> wrote {len(candidates)} candidate(s) to {out} [{status}]")
    print("     NOTE: RTB prices require human curation -> data/processed/rtb_comps_curated.csv")

    sources_log.record(
        "trade_press_comps",
        name=src["name"],
        url=src["feeds"][0]["url"] if src.get("feeds") else None,
        output="data/raw/trade_press_candidates_<date>.csv -> data/processed/rtb_comps.csv",
        status=status,
        description=src["description"],
    )


if __name__ == "__main__":
    run()
