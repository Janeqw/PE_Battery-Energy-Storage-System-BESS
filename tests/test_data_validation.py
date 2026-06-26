"""Validation tests for the data pipeline and the valuation model.

Covers: processed CSVs exist & are well-formed; gate
probabilities are bounded and the cumulative is monotonic; the pipeline is
positive; the sources log is populated; and the model's check framework passes
(mirrored by the Python engine, plus an optional live Excel recalculation when
the `formulas` library is available).
"""
from __future__ import annotations

import csv
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
PROCESSED = ROOT / "data" / "processed"
MODEL = ROOT / "financial_models" / "BESS_Valuation.xlsx"


def _rows(name):
    with open(PROCESSED / name, newline="", encoding="utf-8") as fh:
        return [r for r in csv.reader(fh) if r and not r[0].startswith("#")]


# --------------------------------------------------------------------------- CSVs
@pytest.mark.parametrize("name", ["pipeline.csv", "costs.csv", "gate_stats.csv", "rtb_comps.csv", "rates.csv",
                                  "end_use.csv", "market_demand.csv", "deal_sizes.csv"])
def test_processed_csv_exists_and_nonempty(name):
    path = PROCESSED / name
    assert path.exists(), f"{name} missing — run `make transform`"
    assert len(_rows(name)) >= 2, f"{name} has no data rows"


def test_rtb_comps_positive_by_state():
    rows = _rows("rtb_comps.csv")
    header = rows[0]
    s_i, p_i = header.index("state"), header.index("price_per_mw_m")
    states = {r[s_i] for r in rows[1:]}
    assert {"NSW", "VIC", "SA"} <= states, "rtb_comps.csv must cover NSW/VIC/SA"
    for r in rows[1:]:
        assert float(r[p_i]) > 0, f"RTB $/MW must be positive: {r}"


def test_pipeline_columns_and_positive():
    rows = _rows("pipeline.csv")
    header = rows[0]
    for col in ("project", "state", "mw", "duration_h", "mwh", "years_to_sale"):
        assert col in header, f"pipeline.csv missing column {col}"
    mw_i, mwh_i = header.index("mw"), header.index("mwh")
    for r in rows[1:]:
        assert float(r[mw_i]) > 0, "MW must be positive"
        assert float(r[mwh_i]) > 0, "MWh must be positive"


def test_gate_stats_prob_and_duration():
    rows = _rows("gate_stats.csv")
    header = rows[0]
    p_i, d_i = header.index("probability"), header.index("duration_years")
    gates = {r[0] for r in rows[1:]}
    assert {"development_approval", "grid_connection", "reach_sale"} <= gates
    for r in rows[1:]:
        p = float(r[p_i])
        assert 0.0 <= p <= 1.0, f"gate probability out of [0,1]: {r}"
        assert float(r[d_i]) > 0, "each gate needs a positive duration"


def test_cumulative_le_each_gate():
    rows = _rows("gate_stats.csv")
    p_i = rows[0].index("probability")
    probs = [float(r[p_i]) for r in rows[1:]]
    cumulative = 1.0
    for p in probs:
        cumulative *= p
    assert cumulative <= min(probs) + 1e-9, "cumulative survival must be <= each gate"


def test_sources_md_populated():
    src = ROOT / "financial_models" / "SOURCES_LOG.md"
    assert src.exists(), "financial_models/SOURCES_LOG.md missing — run an extractor"
    text = src.read_text(encoding="utf-8")
    for token in ("RBA", "AEMO", "CSIRO", "Planning"):
        assert token in text, f"SOURCES_LOG.md should mention {token}"


# --------------------------------------------------------------------------- engine
def test_engine_checks_all_pass():
    from src.valuation_engine import load_inputs, run_checks

    checks = run_checks(load_inputs())
    failed = [k for k, v in checks.items() if not v]
    assert not failed, f"engine checks failed: {failed}"


def test_engine_scenarios_monotonic():
    from src.valuation_engine import load_inputs, returns_by_scenario

    rbs = returns_by_scenario(load_inputs())
    assert rbs["Conservative"]["irr"] <= rbs["Base"]["irr"] <= rbs["Ideal"]["irr"]


def test_first_chicago_within_scenario_range():
    from src.valuation_engine import load_inputs, first_chicago

    fc = first_chicago(load_inputs())
    assert fc["min_irr"] - 1e-9 <= fc["expected_irr"] <= fc["max_irr"] + 1e-9


def test_flip_success_below_manager_headline():
    """The headline DD finding: the manager's 65% is the DEVELOPMENT-APPROVAL gate only.

    True develop-and-flip success = DA x grid connection x sale, which is far below
    the 65% headline (the gates beyond approval are not free)."""
    from src.valuation_engine import load_inputs

    inp = load_inputs()
    base_da = float(inp.scenarios[2]["da_rate"])     # the manager's headline (65%)
    assert inp.flip_base < base_da, "true flip success must be below the DA-gate headline"
    assert abs(inp.flip_base - base_da * inp.p_connection * inp.p_sale) < 1e-9


def test_cap_table_ownership_identity():
    """The classic VC identity: ownership % = our investment / post-money."""
    from src.valuation_engine import load_inputs, cap_table

    inp = load_inputs()
    ct = cap_table(inp)
    assert abs(ct["post_money"] - (inp.pre_money + inp.investment_amount)) < 1e-9
    assert abs(ct["ownership_initial"] - inp.investment_amount / ct["post_money"]) < 1e-9
    assert ct["ownership_diluted"] <= ct["ownership_initial"] + 1e-9, "dilution must not increase ownership"


def test_exit_value_is_pipeline_rnpv_plus_retained_less_debt():
    """change2.md PRIMARY exit basis: exit equity = forward-pipeline rNPV +
    retained cash − debt (not net programme profit × a platform multiple)."""
    from src.valuation_engine import (load_inputs, exit_equity_value,
                                      forward_pipeline_rnpv, company_metrics)

    inp = load_inputs()
    assert inp.exit_basis == "pipeline_rnpv", "the default exit basis must be the pipeline rNPV"
    for case in inp.scenarios.values():
        eqv = exit_equity_value(inp, case)
        fwd = forward_pipeline_rnpv(inp, case)
        realised = company_metrics(inp, case)["net_business_profit"]
        retained = max(0.0, realised) * (1.0 - inp.interim_distribution_fraction)
        expected = max(0.0, fwd + retained - inp.debt_at_exit)
        assert abs(eqv["forward_pipeline_rnpv"] - fwd) < 1e-9
        assert abs(eqv["retained_cash"] - retained) < 1e-9
        assert abs(eqv["company_exit_equity"] - expected) < 1e-9, "exit eq must = fwd + retained − debt"


def test_no_double_count_of_cash():
    """The double-count guard: distributions to all holders + the terminal exit
    equity must not exceed realised profit + forward-pipeline value — no dollar of
    profit is counted both as a distribution and in the terminal sale price."""
    from src.valuation_engine import load_inputs, exit_equity_value, investor_return

    inp = load_inputs()
    for case in inp.scenarios.values():
        eqv = exit_equity_value(inp, case)
        lifetime = max(0.0, eqv["realised_profit"]) + eqv["forward_pipeline_rnpv"]
        assert eqv["distributed_all"] + eqv["company_exit_equity"] <= lifetime + 1e-6
        # and our own draw cannot exceed our diluted share of that lifetime value plus our preference
        r = investor_return(inp, case)
        assert r["interim_distributions"] + r["terminal_proceeds"] <= lifetime + 1e-6


def test_stage_analysis_risk_ladder():
    """The three value-chain stages form a risk ladder: operating is the safest downside."""
    from src.stage_analysis import compare

    c = compare()
    for r in c["rows"]:
        assert r["expected_irr"] == r["expected_irr"], "expected IRR must be a number, not nan"
        assert r["expected_moic"] > 0
    s1, s2, s3 = c["s1"], c["s2"], c["s3"]
    # own-and-operate (contracted) has the safest downside; develop/build can lose capital
    assert s3["downside_irr"] > s1["downside_irr"]
    assert s3["downside_irr"] > s2["downside_irr"]
    assert s3["downside_irr"] >= 0, "contracted operating should stay non-negative in the downside"


def test_valuation_range_is_a_range():
    from src.valuation_engine import load_inputs, valuation_range

    vr = valuation_range(load_inputs())
    assert vr["low"] <= vr["high"], "a development-stage valuation must be a range, not a point"


# --------------------------------------------------------------------------- model
def test_model_exists():
    assert MODEL.exists(), "model .xlsx missing — run `python -m src.build_model`"


def test_model_recalculates_clean():
    """Optional: recalc the workbook and assert master check OK + zero errors."""
    formulas = pytest.importorskip("formulas")
    import re
    import warnings

    warnings.filterwarnings("ignore")
    xl = formulas.ExcelModel().loads(str(MODEL)).finish()
    sol = xl.calculate()
    errors = []
    cells = {}            # (SHEET, CELL) -> value
    master_row = None
    for k, v in sol.items():
        m = re.match(r"'\[.*?\]([^']+)'!([A-Z]+\d+)$", k)
        if not m:
            continue
        sheet, cell = m.group(1).upper(), m.group(2)
        val = v.value
        if hasattr(val, "ravel"):
            val = val.ravel()[0] if val.size else None
        cells[(sheet, cell)] = val
        if isinstance(val, str) and val.startswith("#") and val.endswith(("!", "?")):
            errors.append(f"{sheet}!{cell}={val}")
        if sheet == "CHECKS" and val == "MASTER CHECK":         # locate master dynamically
            master_row = int(re.sub(r"[A-Z]", "", cell))
    assert not errors, f"model has error cells: {errors[:10]}"
    assert master_row, "could not find the MASTER CHECK row on the Checks tab"
    master = cells.get(("CHECKS", f"B{master_row}"))
    assert master == "OK", f"master check is {master!r}, expected OK"
