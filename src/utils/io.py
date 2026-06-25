"""Shared I/O helpers for the data pipeline.

Responsibilities:
  * config loading (sources.yaml / assumptions.yaml)
  * polite, cached, date-stamped downloads to data/raw/
  * landing-page link discovery (try direct URL -> discover -> fail clearly)
  * NEVER fabricate data: every download path either returns a real file or
    returns None and the caller logs a manual-download instruction.
"""
from __future__ import annotations

import datetime as _dt
import re
import time
from pathlib import Path
from urllib.parse import urljoin, urlparse
from urllib.robotparser import RobotFileParser

import yaml

# ----------------------------------------------------------------------------
# Paths
# ----------------------------------------------------------------------------
PROJECT_ROOT = Path(__file__).resolve().parents[2]
CONFIG_DIR = PROJECT_ROOT / "config"
DATA_RAW = PROJECT_ROOT / "data" / "raw"
DATA_PROCESSED = PROJECT_ROOT / "data" / "processed"

for _d in (DATA_RAW, DATA_PROCESSED):
    _d.mkdir(parents=True, exist_ok=True)


def today_str() -> str:
    """Date stamp for raw-file caching, e.g. '20260624'."""
    return _dt.date.today().strftime("%Y%m%d")


# ----------------------------------------------------------------------------
# Config
# ----------------------------------------------------------------------------
def load_yaml(name: str) -> dict:
    path = CONFIG_DIR / name
    with open(path, "r", encoding="utf-8") as fh:
        return yaml.safe_load(fh)


def load_sources() -> dict:
    return load_yaml("sources.yaml")


def load_assumptions() -> dict:
    return load_yaml("assumptions.yaml")


# ----------------------------------------------------------------------------
# HTTP session (lazy import so the rest of the pipeline runs without requests)
# ----------------------------------------------------------------------------
def _http_cfg() -> dict:
    return load_sources().get("http", {})


def make_session():
    import requests

    cfg = _http_cfg()
    sess = requests.Session()
    sess.headers.update({"User-Agent": cfg.get("user_agent", "battery-developer-valuation/1.0")})
    return sess


def _robots_allows(url: str) -> bool:
    """Honour robots.txt when configured to (best-effort; fail-open on error)."""
    if not _http_cfg().get("respect_robots_txt", True):
        return True
    try:
        parts = urlparse(url)
        robots_url = f"{parts.scheme}://{parts.netloc}/robots.txt"
        rp = RobotFileParser()
        rp.set_url(robots_url)
        rp.read()
        return rp.can_fetch(_http_cfg().get("user_agent", "*"), url)
    except Exception:
        return True


def polite_delay() -> None:
    time.sleep(float(_http_cfg().get("request_delay_seconds", 2.0)))


# ----------------------------------------------------------------------------
# Download + cache
# ----------------------------------------------------------------------------
def cached_download(url: str, dest: Path, *, binary: bool = True) -> Path | None:
    """Download `url` to `dest`, idempotently.

    Returns the path on success, or None on any failure (caller handles the
    fallback / manual-download message). Skips the request if `dest` already
    exists (today's cache), making the stage idempotent.
    """
    dest = Path(dest)
    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.exists() and dest.stat().st_size > 0:
        print(f"  [cache] using existing {dest.name}")
        return dest

    if not _robots_allows(url):
        print(f"  [robots] disallowed by robots.txt: {url}")
        return None

    try:
        sess = make_session()
        cfg = _http_cfg()
        polite_delay()
        resp = sess.get(url, timeout=cfg.get("timeout_seconds", 60), allow_redirects=True)
        resp.raise_for_status()
        if binary:
            dest.write_bytes(resp.content)
        else:
            dest.write_text(resp.text, encoding="utf-8")
        print(f"  [ok] downloaded {url} -> {dest.name} ({dest.stat().st_size:,} bytes)")
        return dest
    except Exception as exc:  # noqa: BLE001 — graceful failure is the contract
        print(f"  [fail] could not download {url}: {exc}")
        return None


def discover_file_link(landing_page: str, pattern: str) -> str | None:
    """Scrape `landing_page` for the first <a href> matching `pattern` (regex).

    Returns an absolute URL or None. Used when a source's exact file URL changes
    each release (AEMO, CSIRO) — we discover the current link rather than guess.
    """
    try:
        from bs4 import BeautifulSoup

        sess = make_session()
        cfg = _http_cfg()
        polite_delay()
        resp = sess.get(landing_page, timeout=cfg.get("timeout_seconds", 60))
        resp.raise_for_status()
        soup = BeautifulSoup(resp.text, "lxml")
        rx = re.compile(pattern)
        for a in soup.find_all("a", href=True):
            href = a["href"]
            if rx.search(href):
                return urljoin(landing_page, href)
        print(f"  [discover] no link matching /{pattern}/ on {landing_page}")
        return None
    except Exception as exc:  # noqa: BLE001
        print(f"  [discover-fail] {landing_page}: {exc}")
        return None


def write_stage(name: str, data: dict) -> None:
    """Persist an extractor's intermediate gate metrics for the transforms.

    Staging files live in data/raw (gitignored, regenerated by `make extract`).
    """
    import json

    (DATA_RAW / f"_stage_{name}.json").write_text(json.dumps(data, indent=2), encoding="utf-8")


def read_stage(name: str) -> dict | None:
    import json

    path = DATA_RAW / f"_stage_{name}.json"
    if path.exists():
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            return None
    return None


def manual_download_msg(source_name: str, landing_page: str | None, dest: Path) -> None:
    """Print a clear, actionable manual-download instruction (never fabricate)."""
    print("  " + "-" * 68)
    print(f"  MANUAL DOWNLOAD REQUIRED — {source_name}")
    if landing_page:
        print(f"    1. Open: {landing_page}")
        print("    2. Download the latest data file.")
    print(f"    3. Save it to: {dest}")
    print("    4. Re-run this extractor. (Falling back to documented benchmark.)")
    print("  " + "-" * 68)
