"""Valuation engine — the Python reference implementation of the Excel model.

DEAL: an ILLUSTRATIVE distribution-network BESS *develop-and-flip* fund (framed
on the an illustrative develop-and-flip battery storage fund — manager claims independently rebuilt). The
fund develops ~5 MW distribution batteries to shovel-ready (RTB / development
rights) and SELLS them before construction. It never operates the asset, so
merchant-price risk passes to the buyer; the fund's risk is the SURVIVAL CURVE
(approve -> connect -> sell) and the RTB EXIT PRICE.

This module encodes the SAME maths the Excel workbook computes with formulas:
  * the PD-style survival curve (independent cumulative P from public gate data)
  * per-project risk-adjusted NAV (rNPV): RTB sale - dev cost, x cum P, discounted
  * the FUND FUNNEL: projects_started = target / success; dev cost (with
    attrition); fees (entry / management / carry over hurdle); investor IRR & MOIC
  * scenarios (Conservative / Base / Ideal) driven by the success rate, with a
    First-Chicago probability-weighted expected return
  * cross-checks ($/MW benchmark, VC method, RTB-as-%-of-built)

It reads the SAME inputs as the model (config/assumptions.yaml + the processed
CSVs), so its numbers should match the workbook. All figures are ILLUSTRATIVE.
the manager figures are the manager's claims to verify. Not investment advice.
"""
from __future__ import annotations

import csv
from dataclasses import dataclass, field
from pathlib import Path

from src.utils import io

PROJECT_ROOT = io.PROJECT_ROOT
PROCESSED = io.DATA_PROCESSED


# ---------------------------------------------------------------------------
# Input loading (mirrors the model's Inputs tab)
# ---------------------------------------------------------------------------
@dataclass
class Inputs:
    risk_free: float
    risk_premium: float
    vc_target_return: float
    horizon: int
    # development cost
    dev_cost_per_project: float
    abandonment_fraction: float
    built_cost_per_mw: float
    # survival gates (independent public-data decomposition)
    p_planning: float
    p_connection: float
    p_sale: float
    dur_planning: float
    dur_connection: float
    dur_sale: float
    # RTB exit price $/MW by state
    rtb_comps: dict
    # fund structure
    committed_capital: float
    projects_target: float
    term_years: float
    entry_fee_pct: float
    mgmt_fee_pct_pa: float
    carry_pct: float
    hurdle_pct: float
    call_profile: list
    dist_profile: list
    # scenarios
    scenarios: dict
    weights: dict
    switch_default: int
    projects: list = field(default_factory=list)
    sources: dict = field(default_factory=dict)

    @property
    def discount_base(self) -> float:
        return self.risk_free + self.risk_premium

    @property
    def cum_p_independent(self) -> float:
        """Independent bottom-up cumulative success from public gate data (~0.45)."""
        return self.p_planning * self.p_connection * self.p_sale


def _read_csv_rows(path: Path) -> list[dict]:
    with open(path, newline="", encoding="utf-8") as fh:
        rows = [r for r in csv.reader(fh) if r and not r[0].startswith("#")]
    header = rows[0]
    return [dict(zip(header, r)) for r in rows[1:]]


def load_inputs() -> Inputs:
    a = io.load_assumptions()
    sources = {}

    # Risk-free: prefer live rates.csv, else config
    risk_free = float(a["discount_rate"]["risk_free"]["value"])
    rates_csv = PROCESSED / "rates.csv"
    if rates_csv.exists():
        r = _read_csv_rows(rates_csv)[0]
        risk_free = float(r["value"])
        sources["risk_free"] = (r["source"], r["as_at"], r["status"])

    # Costs: prefer costs.csv (dev cost per project + built-cost context)
    dev_cost = float(a["dev_cost"]["per_project_m"]["value"])
    built = float(a["built_cost_context"]["per_mw_m"]["value"])
    costs_csv = PROCESSED / "costs.csv"
    if costs_csv.exists():
        for r in _read_csv_rows(costs_csv):
            if r["item"] == "dev_cost_per_project_m":
                dev_cost = float(r["value"]); sources["dev"] = (r["source"], r["as_at"], r["status"])
            elif r["item"] == "built_cost_context_per_mw_m":
                built = float(r["value"]); sources["build"] = (r["source"], r["as_at"], r["status"])

    # Gates: prefer gate_stats.csv
    g = a["gates"]
    pp, pc, ps = (g["planning_approval"]["probability"], g["grid_connection"]["probability"],
                  g["reach_sale"]["probability"])
    dp, dc, ds = (g["planning_approval"]["duration_years"], g["grid_connection"]["duration_years"],
                  g["reach_sale"]["duration_years"])
    gate_csv = PROCESSED / "gate_stats.csv"
    if gate_csv.exists():
        m = {r["gate"]: r for r in _read_csv_rows(gate_csv)}
        if "planning_approval" in m:
            pp = float(m["planning_approval"]["probability"]); dp = float(m["planning_approval"]["duration_years"])
            sources["p_planning"] = (m["planning_approval"]["source"], m["planning_approval"]["as_at"], m["planning_approval"]["status"])
        if "grid_connection" in m:
            pc = float(m["grid_connection"]["probability"]); dc = float(m["grid_connection"]["duration_years"])
            sources["p_connection"] = (m["grid_connection"]["source"], m["grid_connection"]["as_at"], m["grid_connection"]["status"])
        if "reach_sale" in m:
            ps = float(m["reach_sale"]["probability"]); ds = float(m["reach_sale"]["duration_years"])
            sources["p_sale"] = (m["reach_sale"]["source"], m["reach_sale"]["as_at"], m["reach_sale"]["status"])

    # RTB comps $/MW by state: prefer rtb_comps.csv
    rtb = {k: float(v) for k, v in a["rtb_comps_per_mw_m"].items()
           if k in ("NSW", "VIC", "SA")}
    rtb_csv = PROCESSED / "rtb_comps.csv"
    if rtb_csv.exists():
        for r in _read_csv_rows(rtb_csv):
            try:
                rtb[r["state"]] = float(r["price_per_mw_m"])
            except (KeyError, ValueError):
                pass
        sources["rtb"] = ("RTB $/MW by state (the manager claim — independent comps needed)",
                          a["rtb_comps_per_mw_m"]["as_at"], "BENCHMARK")

    # Pipeline: prefer pipeline.csv
    projects = []
    pipe_csv = PROCESSED / "pipeline.csv"
    if pipe_csv.exists():
        for r in _read_csv_rows(pipe_csv):
            projects.append({
                "name": r["project"], "state": r["state"], "location": r["location"],
                "mw": float(r["mw"]), "duration_h": float(r["duration_h"]),
                "mwh": float(r["mwh"]), "years_to_sale": float(r["years_to_sale"]),
            })
    else:
        for p in a["pipeline"]["projects"]:
            projects.append({**p, "mwh": p["mw"] * p["duration_h"], "years_to_sale": p["years_to_sale"]})

    fund = a["fund"]
    fees = fund["fees"]
    return Inputs(
        risk_free=risk_free,
        risk_premium=float(a["discount_rate"]["risk_premium"]["value"]),
        vc_target_return=float(a["returns"]["vc_target_return"]["value"]),
        horizon=int(a["meta"]["horizon_years"]),
        dev_cost_per_project=dev_cost,
        abandonment_fraction=float(a["dev_cost"]["abandonment_fraction"]["value"]),
        built_cost_per_mw=built,
        p_planning=pp, p_connection=pc, p_sale=ps,
        dur_planning=dp, dur_connection=dc, dur_sale=ds,
        rtb_comps=rtb,
        committed_capital=float(fund["committed_capital_m"]["value"]),
        projects_target=float(fund["projects_target"]["value"]),
        term_years=float(fund["term_years"]["value"]),
        entry_fee_pct=float(fees["entry_fee_pct"]),
        mgmt_fee_pct_pa=float(fees["mgmt_fee_pct_pa"]),
        carry_pct=float(fees["carry_pct"]),
        hurdle_pct=float(fees["hurdle_pct"]),
        call_profile=list(fund["capital_call_profile"]["value"]),
        dist_profile=list(fund["distribution_profile"]["value"]),
        scenarios=a["scenarios"]["cases"], weights=a["scenarios"]["weights"],
        switch_default=int(a["scenarios"]["switch_default"]),
        projects=projects, sources=sources,
    )


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def effective_hold(inp: Inputs) -> float:
    """Cash-weighted hold = mean distribution period - mean call period.

    For profiles calls [0.5,0.5] / dists [0,0,0.5,0.5] this is 2.5 - 0.5 = 2.0,
    so closed-form IRR = MOIC^(1/2)-1 ~= the true multi-period IRR.
    """
    avg_call = sum(t * f for t, f in enumerate(inp.call_profile))
    avg_dist = sum(t * f for t, f in enumerate(inp.dist_profile))
    return avg_dist - avg_call


def survival_curve(inp: Inputs) -> dict:
    """PD-style survival: independent per-gate probs and cumulative survival.

    This is the model's INDEPENDENT bottom-up estimate from public data; the
    scenarios (Conservative/Base/Ideal) set the success rate used in valuation.
    """
    g1, g2, g3 = inp.p_planning, inp.p_connection, inp.p_sale
    return {
        "planning": g1, "connection": g2, "sale": g3,
        "survival_after_planning": g1,
        "survival_after_connection": g1 * g2,
        "cumulative": g1 * g2 * g3,
    }


def discount_rate_for(inp: Inputs, case: dict) -> float:
    ov = case.get("discount_rate_override")
    return float(ov) if ov else inp.discount_base


def _case(inp: Inputs, case: dict | None) -> dict:
    return case if case is not None else inp.scenarios[2]  # 2 = Base


# ---------------------------------------------------------------------------
# Per-project risk-adjusted NAV (rNPV) — RTB, development cost only
# ---------------------------------------------------------------------------
def project_rows(inp: Inputs, case: dict) -> list[dict]:
    """Per-project rNPV rows for a scenario (mirrors Calc_Project_rNPV).

    Cost is DEVELOPMENT cost only — the fund sells RTB and never builds; the
    buyer funds construction.
    """
    cumP = float(case["cum_success"])
    smult = float(case["sale_price_multiplier"])
    dmult = float(case["dev_cost_multiplier"])
    disc = discount_rate_for(inp, case)
    out = []
    for p in inp.projects:
        rtb_per_mw = inp.rtb_comps.get(p["state"], 0.0) * smult
        sale = p["mw"] * rtb_per_mw
        cost = inp.dev_cost_per_project * dmult
        gross_margin = sale - cost
        risk_adj = gross_margin * cumP
        df = 1.0 / (1.0 + disc) ** p["years_to_sale"]
        out.append({
            "name": p["name"], "state": p["state"], "mw": p["mw"],
            "years_to_sale": p["years_to_sale"], "rtb_per_mw": rtb_per_mw,
            "sale_value": sale, "cost": cost, "gross_margin": gross_margin,
            "cumP": cumP, "risk_adj_margin": risk_adj, "df": df, "pv": risk_adj * df,
        })
    return out


def pipeline_rnpv(inp: Inputs, case: dict | None = None) -> float:
    """Risk-adjusted PV of the representative pipeline (sum of per-project PV)."""
    rows = project_rows(inp, _case(inp, case))
    return sum(r["pv"] for r in rows)


def rnpv_per_project(inp: Inputs, case: dict | None = None) -> float:
    rows = project_rows(inp, _case(inp, case))
    return sum(r["pv"] for r in rows) / len(rows) if rows else float("nan")


# ---------------------------------------------------------------------------
# Fund funnel, fees & investor return  (Calc_Fund + Returns)
# ---------------------------------------------------------------------------
def blended_sale_value(inp: Inputs, case: dict) -> float:
    """Average RTB sale value per delivered project across the pipeline mix."""
    smult = float(case["sale_price_multiplier"])
    vals = [p["mw"] * inp.rtb_comps.get(p["state"], 0.0) * smult for p in inp.projects]
    return sum(vals) / len(vals) if vals else 0.0


def fund_metrics(inp: Inputs, case: dict | None = None) -> dict:
    """The funnel -> fees -> investor IRR & MOIC for a scenario."""
    case = _case(inp, case)
    cumP = float(case["cum_success"])
    dmult = float(case["dev_cost_multiplier"])

    target = inp.projects_target
    started = target / cumP if cumP > 0 else float("inf")
    failed = started - target
    C = inp.dev_cost_per_project * dmult
    # stage-weighted attrition: full cost on delivered + partial on the dropouts
    total_dev_cost = target * C + failed * inp.abandonment_fraction * C

    sale_per_project = blended_sale_value(inp, case)
    gross_proceeds = target * sale_per_project

    entry_fee = inp.entry_fee_pct * inp.committed_capital
    mgmt_fee = inp.mgmt_fee_pct_pa * inp.committed_capital * inp.term_years
    invested_capital = total_dev_cost + mgmt_fee + entry_fee

    profit_pre_carry = gross_proceeds - invested_capital
    hurdle_amount = invested_capital * ((1.0 + inp.hurdle_pct) ** inp.term_years - 1.0)
    carry = inp.carry_pct * max(0.0, profit_pre_carry - hurdle_amount)
    distributions = gross_proceeds - carry

    moic = distributions / invested_capital if invested_capital > 0 else float("nan")
    # Investor IRR = closed-form over the effective hold, so the Excel model
    # reproduces it cell-for-cell without relying on Excel's IRR(): the effective
    # hold is the cash-weighted gap between distributions and calls.
    eff_hold = effective_hold(inp)
    fund_irr = moic ** (1.0 / eff_hold) - 1.0 if (moic > 0 and eff_hold > 0) else float("nan")

    return {
        "cum_success": cumP, "projects_target": target, "projects_started": started,
        "projects_failed": failed, "total_dev_cost": total_dev_cost,
        "sale_per_project": sale_per_project, "gross_proceeds": gross_proceeds,
        "entry_fee": entry_fee, "mgmt_fee": mgmt_fee, "invested_capital": invested_capital,
        "profit_pre_carry": profit_pre_carry, "hurdle_amount": hurdle_amount,
        "carry": carry, "distributions": distributions, "net_profit": distributions - invested_capital,
        "moic": moic, "irr": fund_irr, "eff_hold": eff_hold,
    }


def returns_by_scenario(inp: Inputs) -> dict:
    """Investor IRR & MOIC for each scenario."""
    return {c["name"]: fund_metrics(inp, c) for c in inp.scenarios.values()}


def first_chicago(inp: Inputs) -> dict:
    """Probability-weighted (First-Chicago) expected investor IRR & MOIC."""
    rbs = returns_by_scenario(inp)
    exp_irr = sum(rbs[name]["irr"] * w for name, w in inp.weights.items())
    exp_moic = sum(rbs[name]["moic"] * w for name, w in inp.weights.items())
    irrs = [rbs[name]["irr"] for name in inp.weights]
    return {"expected_irr": exp_irr, "expected_moic": exp_moic,
            "min_irr": min(irrs), "max_irr": max(irrs), "by_scenario": rbs}


# ---------------------------------------------------------------------------
# Cross-checks ($/MW benchmark, VC method, RTB-as-%-of-built)
# ---------------------------------------------------------------------------
def dollar_per_mw_benchmark(inp: Inputs, case: dict | None = None) -> dict:
    """Method: total MW x RTB $/MW, less dev cost, risk-adjusted, discounted."""
    case = _case(inp, case)
    cumP = float(case["cum_success"])
    smult = float(case["sale_price_multiplier"])
    dmult = float(case["dev_cost_multiplier"])
    disc = discount_rate_for(inp, case)
    total_mw = sum(p["mw"] for p in inp.projects)
    gross_asset_value = sum(p["mw"] * inp.rtb_comps.get(p["state"], 0.0) for p in inp.projects) * smult
    total_cost = inp.dev_cost_per_project * dmult * len(inp.projects)
    avg_years = sum(p["years_to_sale"] for p in inp.projects) / len(inp.projects)
    dev_value = (gross_asset_value - total_cost) * cumP / (1.0 + disc) ** avg_years
    return {
        "total_mw": total_mw, "gross_asset_value": gross_asset_value,
        "total_cost": total_cost, "implied_dev_value": dev_value, "avg_years": avg_years,
    }


def vc_method(inp: Inputs, case: dict | None = None) -> dict:
    """Work back from the risk-adjusted exit value at the VC target return."""
    case = _case(inp, case)
    cumP = float(case["cum_success"])
    smult = float(case["sale_price_multiplier"])
    dmult = float(case["dev_cost_multiplier"])
    total_sale = sum(p["mw"] * inp.rtb_comps.get(p["state"], 0.0) for p in inp.projects) * smult
    total_cost = inp.dev_cost_per_project * dmult * len(inp.projects)
    exit_equity_value = cumP * (total_sale - total_cost)
    today_value = exit_equity_value / (1.0 + inp.vc_target_return) ** inp.horizon
    return {
        "exit_equity_value": exit_equity_value, "hurdle": inp.vc_target_return,
        "horizon": inp.horizon, "today_value": today_value,
    }


def rtb_vs_built(inp: Inputs) -> dict:
    """Sense-check: RTB price as a % of built-asset value (should be ~10-12%)."""
    out = {}
    for state, rtb in inp.rtb_comps.items():
        built = inp.built_cost_per_mw
        out[state] = {"rtb_per_mw": rtb, "built_per_mw": built,
                      "pct_of_built": rtb / built if built else float("nan")}
    return out


def valuation_range(inp: Inputs) -> dict:
    """Per-pipeline value across three asset-value methods (Base case)."""
    methods = {
        "rNPV pipeline (Base)": pipeline_rnpv(inp),
        "$/MW benchmark (dev value)": dollar_per_mw_benchmark(inp)["implied_dev_value"],
        "VC method (today value)": vc_method(inp)["today_value"],
    }
    vals = list(methods.values())
    return {"methods": methods, "low": min(vals), "high": max(vals),
            "midpoint": sum(vals) / len(vals)}


# ---------------------------------------------------------------------------
# Sensitivity & tornado (success rate x RTB price)
# ---------------------------------------------------------------------------
def sensitivity_two_way(inp: Inputs,
                        successes=(0.35, 0.45, 0.55, 0.65, 0.80),
                        price_mults=(0.70, 0.85, 1.00, 1.15, 1.30)) -> dict:
    """Investor IRR across cumulative success rate x RTB price multiplier."""
    grid = []
    for s in successes:
        row = []
        for pm in price_mults:
            case = {"cum_success": s, "sale_price_multiplier": pm,
                    "dev_cost_multiplier": 1.0, "discount_rate_override": None}
            row.append(fund_metrics(inp, case)["irr"])
        grid.append(row)
    return {"successes": list(successes), "price_mults": list(price_mults), "grid": grid}


def tornado(inp: Inputs) -> list[dict]:
    """Investor-IRR swing from a move in each key driver (around Base)."""
    base = inp.scenarios[2]
    base_irr = fund_metrics(inp, base)["irr"]

    def irr_with(**over) -> float:
        case = {**base, **over}
        return fund_metrics(inp, case)["irr"]

    specs = [
        ("Success rate", {"cum_success": 0.45}, {"cum_success": 0.80}),
        ("RTB price", {"sale_price_multiplier": 0.80}, {"sale_price_multiplier": 1.20}),
        ("Dev cost", {"dev_cost_multiplier": 1.20}, {"dev_cost_multiplier": 0.80}),
    ]
    out = []
    for label, lo, hi in specs:
        out.append({"driver": label, "low": irr_with(**lo), "high": irr_with(**hi),
                    "swing": abs(irr_with(**hi) - irr_with(**lo)), "base": base_irr})
    out.sort(key=lambda d: d["swing"], reverse=True)
    return out


# ---------------------------------------------------------------------------
# Checks (mirror the model's Checks tab)
# ---------------------------------------------------------------------------
def run_checks(inp: Inputs) -> dict:
    sc = survival_curve(inp)
    rbs = returns_by_scenario(inp)
    fc = first_chicago(inp)
    probs = [inp.p_planning, inp.p_connection, inp.p_sale]
    rows = project_rows(inp, inp.scenarios[2])
    irr_c, irr_b, irr_i = rbs["Conservative"]["irr"], rbs["Base"]["irr"], rbs["Ideal"]["irr"]
    return {
        "probabilities in [0,1]": all(0 <= p <= 1 for p in probs),
        "independent cumulative <= each gate": (sc["cumulative"] <= min(probs) + 1e-9),
        "MW positive": all(p["mw"] > 0 for p in inp.projects),
        "RTB sale values positive": all(r["sale_value"] > 0 for r in rows),
        "dev costs positive": all(r["cost"] > 0 for r in rows),
        "switch in 1..3": inp.switch_default in (1, 2, 3),
        "scenario success monotonic": (inp.scenarios[1]["cum_success"] <=
                                       inp.scenarios[2]["cum_success"] <=
                                       inp.scenarios[3]["cum_success"]),
        "investor IRR monotonic (Cons<=Base<=Ideal)": (irr_c <= irr_b <= irr_i),
        "scenario weights sum to 100%": abs(sum(inp.weights.values()) - 1.0) < 1e-6,
        "capital-call profile sums to 100%": abs(sum(inp.call_profile) - 1.0) < 1e-6,
        "distribution profile sums to 100%": abs(sum(inp.dist_profile) - 1.0) < 1e-6,
        "First-Chicago IRR within scenario range": fc["min_irr"] - 1e-9 <= fc["expected_irr"] <= fc["max_irr"] + 1e-9,
        "invested capital positive": all(rbs[n]["invested_capital"] > 0 for n in rbs),
        "every input has a source": len(inp.sources) >= 4,
    }


def summary(inp: Inputs | None = None) -> dict:
    inp = inp or load_inputs()
    rbs = returns_by_scenario(inp)
    fc = first_chicago(inp)
    sc = survival_curve(inp)
    return {
        "inputs": inp,
        "discount_base": inp.discount_base,
        "survival": sc,
        "cum_p_independent": inp.cum_p_independent,
        "base_scenario_success": float(inp.scenarios[2]["cum_success"]),
        "optimism_gap": float(inp.scenarios[2]["cum_success"]) - inp.cum_p_independent,
        "returns_by_scenario": rbs,
        "first_chicago": fc,
        "fund_base": fund_metrics(inp, inp.scenarios[2]),
        "pipeline_rnpv_base": pipeline_rnpv(inp),
        "rnpv_per_project": rnpv_per_project(inp),
        "dollar_per_mw": dollar_per_mw_benchmark(inp),
        "vc": vc_method(inp),
        "rtb_vs_built": rtb_vs_built(inp),
        "valuation_range": valuation_range(inp),
        "checks": run_checks(inp),
    }


if __name__ == "__main__":
    s = summary()
    inp = s["inputs"]
    print("=" * 72)
    print("ILLUSTRATIVE DISTRIBUTION-BESS DEVELOP-AND-FLIP FUND — VALUATION ENGINE")
    print("(independent rebuild; the manager figures are claims to verify — not advice)")
    print("=" * 72)
    print(f"Risk-free (RBA): {inp.risk_free:.3%}  + premium {inp.risk_premium:.1%}"
          f"  => base discount {s['discount_base']:.2%}")
    print(f"Pipeline (representative): {len(inp.projects)} x ~5 MW across NSW/VIC/SA")
    sc = s["survival"]
    print(f"\nSurvival curve (INDEPENDENT, public data): planning {sc['planning']:.0%} "
          f"-> connection {sc['connection']:.0%} -> sale {sc['sale']:.0%}"
          f"  => cumulative {sc['cumulative']:.1%}")
    print(f"   Base scenario success (the manager claim): {s['base_scenario_success']:.0%}"
          f"   => optimism gap {s['optimism_gap']:+.1%}  (Base sits ABOVE independent)")
    print("\nInvestor returns by scenario (after fees):")
    for name in ("Conservative", "Base", "Ideal"):
        m = s["returns_by_scenario"][name]
        print(f"   {name:<13} success {m['cum_success']:.0%}  started {m['projects_started']:.0f}"
              f"  MOIC {m['moic']:.2f}x  IRR {m['irr']:.1%}")
    fc = s["first_chicago"]
    print(f"\nFirst-Chicago expected investor IRR: {fc['expected_irr']:.1%}"
          f"  (MOIC {fc['expected_moic']:.2f}x)   range {fc['min_irr']:.1%} .. {fc['max_irr']:.1%}")
    vr = s["valuation_range"]
    print(f"\nPipeline value cross-check range: ${vr['low']:.1f}m – ${vr['high']:.1f}m "
          f"(midpoint ${vr['midpoint']:.1f}m)")
    print("\nChecks:")
    for k, v in s["checks"].items():
        print(f"   [{'OK ' if v else 'XX '}] {k}")
    print("\n(All figures illustrative — the manager figures are claims to verify. Not investment advice.)")
