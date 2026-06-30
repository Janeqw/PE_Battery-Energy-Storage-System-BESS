"""change12: assumptions.yaml <-> sources.yaml link integrity.

Every assumption in config/assumptions.yaml carries a `source_key:` that must
resolve to a declared source in config/sources.yaml — a real key, a
`context_only:<name>`, or `none` (analyst judgement / no public source, with
`judgement: true`). This keeps the two files from drifting apart.
"""
from __future__ import annotations

import re
import warnings
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]

# Proper-noun tokens that would imply a declared PUBLIC source backs an input.
PUBLIC_SOURCE_TOKENS = ["RBA", "AEMO", "CSIRO", "GenCost", "Planning Portal", "ISP", "QED"]


def _load(name: str) -> dict:
    return yaml.safe_load((ROOT / "config" / name).read_text(encoding="utf-8"))


def _sourced_nodes(node, path=()):
    """Yield (path, mapping) for every dict that declares a `source_key`."""
    if isinstance(node, dict):
        if "source_key" in node:
            yield path, node
        for k, v in node.items():
            yield from _sourced_nodes(v, path + (str(k),))
    elif isinstance(node, list):
        for i, v in enumerate(node):
            yield from _sourced_nodes(v, path + (str(i),))


def _declared(sources: dict):
    blk = sources["sources"]
    keys = {k for k in blk if k != "context_only"}
    ctx = {e["name"] for e in blk.get("context_only", [])}
    return keys, ctx


def _is_none(sk) -> bool:
    return sk is None or sk == "none"


def test_every_source_key_resolves():
    """Each source_key is a declared key, a context_only:<name>, or none+judgement."""
    a, s = _load("assumptions.yaml"), _load("sources.yaml")
    keys, ctx = _declared(s)
    bad = []
    for path, node in _sourced_nodes(a):
        where = ".".join(path) or "<root>"
        sk = node.get("source_key")
        if _is_none(sk):
            if node.get("judgement") is not True:
                bad.append(f"{where}: source_key 'none' but judgement is not true")
        elif isinstance(sk, str) and sk.startswith("context_only:"):
            name = sk[len("context_only:"):]
            if name not in ctx:
                bad.append(f"{where}: context_only source '{name}' not declared in sources.yaml")
        elif sk not in keys:
            bad.append(f"{where}: source_key '{sk}' is not declared in sources.yaml")
    assert not bad, "unresolved source_key links:\n" + "\n".join(bad)


def test_judgement_inputs_dont_cite_a_public_source():
    """A `source_key: none` input must not name a public source in its prose."""
    a = _load("assumptions.yaml")
    offenders = []
    for path, node in _sourced_nodes(a):
        if not _is_none(node.get("source_key")):
            continue
        text = str(node.get("source", ""))
        hit = [t for t in PUBLIC_SOURCE_TOKENS if re.search(r"\b" + re.escape(t) + r"\b", text)]
        if hit:
            offenders.append(f"{'.'.join(path)}: cites {hit} but source_key=none -> {text!r}")
    assert not offenders, "judgement inputs must not cite a public source:\n" + "\n".join(offenders)


def test_no_dangling_declared_sources():
    """Soft check: warn (do not fail) if a declared source is linked by no assumption
    AND does not feed a committed data/processed CSV (i.e. is truly unused)."""
    a, s = _load("assumptions.yaml"), _load("sources.yaml")
    keys, _ = _declared(s)
    referenced = {node.get("source_key") for _, node in _sourced_nodes(a)}
    feeds_csv = {k for k, v in s["sources"].items()
                 if k != "context_only" and "data/processed/" in str(v.get("output_path", ""))}
    dangling = sorted(keys - referenced - feeds_csv)
    if dangling:
        warnings.warn(
            "declared sources linked by no assumption and not feeding a committed CSV: "
            + ", ".join(dangling)
        )
