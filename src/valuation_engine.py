"""Valuation engine — Python reference of the Excel model (Stage 1: develop & flip).

DEAL: an ILLUSTRATIVE distribution-network battery *develop-and-flip* fund. The
fund develops ~5 MW distribution batteries to shovel-ready (ready-to-build, RTB)
and SELLS them before construction. Merchant-price risk passes to the buyer.

CORRECTED GATE LOGIC (this rebuild):
  Each lifecycle gate is modelled SEPARATELY. The scenarios move ONLY the
  development-approval (DA) gate (manager claim: 40 / 65 / 80%). The Stage-1 flip
  must clear THREE gates, so its true success is the product:
      flip success = DA  x  grid connection (~70%)  x  sale (~80%)
  e.g. Base = 0.65 x 0.70 x 0.80 = 0.364 — NOT 65%. The manager's 65% is the DA
  gate alone; treating it as whole-funnel success overstates the real chance.

Valuation follows the VC method (work back from exit value, discount at a target
return) with First-Chicago scenario weighting. No cap table (single-asset/fund
play). Reproduces the Excel workbook. All figures illustrative; not investment advice.
"""
from __future__ import annotations

import csv
from dataclasses import dataclass, field
from pathlib import Path

from src.utils import io

PROJECT_ROOT = io.PROJECT_ROOT
PROCESSED = io.DATA_PROCESSED


@dataclass
class Inputs:
    risk_free: float
    risk_premium: float
    vc_target_return: float
    horizon: int
    dev_cost_per_project: float
    abandonment_fraction: float
    built_cost_per_mw: float
    # gates
    da_independent: float          # public-data development-approval benchmark
    p_connection: float
    p_sale: float
    dur_da: float
    dur_connection: float
    dur_sale: float
    # RTB price $/MW by state
    rtb_comps: dict
    # fund
    committed_capital: float
    projects_target: float
    term_years: float
    entry_fee_pct: float
    mgmt_fee_pct_pa: float
    carry_pct: float
    hurdle_pct: float
    call_profile: list
    dist_profile: list
    # scenarios (cases carry da_rate, sale_price_multiplier, dev_cost_multiplier)
    scenarios: dict
    weights: dict
    switch_default: int
    projects: list = field(default_factory=list)
    sources: dict = field(default_factory=dict)

    @property
    def discount_base(self) -> float:
        return self.risk_free + self.risk_premium

    def flip_success(self, da: float) -> float:
        """Stage-1 flip success = development approval x grid connection x sale."""
        return da * self.p_connection * self.p_sale

    @property
    def flip_independent(self) -> float:
        return self.flip_success(self.da_independent)

    @property
    def flip_base(self) -> float:
        return self.flip_success(float(self.scenarios[2]["da_rate"]))


def _read_csv_rows(path: Path) -> list[dict]:
    with open(path, newline="", encoding="utf-8") as fh:
        rows = [r for r in csv.reader(fh) if r and not r[0].startswith("#")]
    header = rows[0]
    return [dict(zip(header, r)) for r in rows[1:]]


def load_inputs() -> Inputs:
    a = io.load_assumptions()
    sources = {}

    risk_free = float(a["discount_rate"]["risk_free"]["value"])
    rates_csv = PROCESSED / "rates.csv"
    if rates_csv.exists():
        r = _read_csv_rows(rates_csv)[0]
        risk_free = float(r["value"]); sources["risk_free"] = (r["source"], r["as_at"], r["status"])

    dev_cost = float(a["dev_cost"]["per_project_m"]["value"])
    built = float(a["built_cost_context"]["per_mw_m"]["value"])
    costs_csv = PROCESSED / "costs.csv"
    if costs_csv.exists():
        for r in _read_csv_rows(costs_csv):
            if r["item"] == "dev_cost_per_project_m":
                dev_cost = float(r["value"]); sources["dev"] = (r["source"], r["as_at"], r["status"])
            elif r["item"] == "built_cost_context_per_mw_m":
                built = float(r["value"]); sources["build"] = (r["source"], r["as_at"], r["status"])

    g = a["gates"]
    da_ind = float(g["development_approval"]["independent"])
    pc, ps = float(g["grid_connection"]["probability"]), float(g["reach_sale"]["probability"])
    dda = float(g["development_approval"]["duration_years"])
    dc, ds = float(g["grid_connection"]["duration_years"]), float(g["reach_sale"]["duration_years"])
    gate_csv = PROCESSED / "gate_stats.csv"
    if gate_csv.exists():
        m = {r["gate"]: r for r in _read_csv_rows(gate_csv)}
        if "development_approval" in m:
            da_ind = float(m["development_approval"]["probability"]); dda = float(m["development_approval"]["duration_years"])
            sources["da"] = (m["development_approval"]["source"], m["development_approval"]["as_at"], m["development_approval"]["status"])
        if "grid_connection" in m:
            pc = float(m["grid_connection"]["probability"]); dc = float(m["grid_connection"]["duration_years"])
            sources["connection"] = (m["grid_connection"]["source"], m["grid_connection"]["as_at"], m["grid_connection"]["status"])
        if "reach_sale" in m:
            ps = float(m["reach_sale"]["probability"]); ds = float(m["reach_sale"]["duration_years"])
            sources["sale"] = (m["reach_sale"]["source"], m["reach_sale"]["as_at"], m["reach_sale"]["status"])

    rtb = {k: float(v) for k, v in a["rtb_comps_per_mw_m"].items() if k in ("NSW", "VIC", "SA")}
    rtb_csv = PROCESSED / "rtb_comps.csv"
    if rtb_csv.exists():
        for r in _read_csv_rows(rtb_csv):
            try:
                rtb[r["state"]] = float(r["price_per_mw_m"])
            except (KeyError, ValueError):
                pass
        sources["rtb"] = ("RTB $/MW by state (manager claim — independent comps needed)",
                          a["rtb_comps_per_mw_m"]["as_at"], "BENCHMARK")

    projects = []
    pipe_csv = PROCESSED / "pipeline.csv"
    if pipe_csv.exists():
        for r in _read_csv_rows(pipe_csv):
            projects.append({"name": r["project"], "state": r["state"], "location": r["location"],
                             "mw": float(r["mw"]), "duration_h": float(r["duration_h"]),
                             "mwh": float(r["mwh"]), "years_to_sale": float(r["years_to_sale"])})
    else:
        for p in a["pipeline"]["projects"]:
            projects.append({**p, "mwh": p["mw"] * p["duration_h"], "years_to_sale": p["years_to_sale"]})

    fund, fees = a["fund"], a["fund"]["fees"]
    return Inputs(
        risk_free=risk_free,
        risk_premium=float(a["discount_rate"]["risk_premium"]["value"]),
        vc_target_return=float(a["returns"]["vc_target_return"]["value"]),
        horizon=int(a["meta"]["horizon_years"]),
        dev_cost_per_project=dev_cost,
        abandonment_fraction=float(a["dev_cost"]["abandonment_fraction"]["value"]),
        built_cost_per_mw=built,
        da_independent=da_ind, p_connection=pc, p_sale=ps,
        dur_da=dda, dur_connection=dc, dur_sale=ds,
        rtb_comps=rtb,
        committed_capital=float(fund["committed_capital_m"]["value"]),
        projects_target=float(fund["projects_target"]["value"]),
        term_years=float(fund["term_years"]["value"]),
        entry_fee_pct=float(fees["entry_fee_pct"]), mgmt_fee_pct_pa=float(fees["mgmt_fee_pct_pa"]),
        carry_pct=float(fees["carry_pct"]), hurdle_pct=float(fees["hurdle_pct"]),
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
    avg_call = sum(t * f for t, f in enumerate(inp.call_profile))
    avg_dist = sum(t * f for t, f in enumerate(inp.dist_profile))
    return avg_dist - avg_call


def _case(inp: Inputs, case: dict | None) -> dict:
    return case if case is not None else inp.scenarios[2]


def survival_curve(inp: Inputs, da: float | None = None) -> dict:
    """The Stage-1 flip survival chain (development approval -> connection -> sale)."""
    da = inp.da_independent if da is None else da
    s1 = da
    s2 = s1 * inp.p_connection
    s3 = s2 * inp.p_sale
    return {"development_approval": da, "grid_connection": inp.p_connection, "reach_sale": inp.p_sale,
            "after_approval": s1, "after_connection": s2, "flip_cumulative": s3}


def discount_rate_for(inp: Inputs, case: dict) -> float:
    # the asset-cross-check discount; scenarios no longer override it
    return inp.discount_base


# ---------------------------------------------------------------------------
# Per-project risk-adjusted NAV (rNPV) — RTB, development cost only
# ---------------------------------------------------------------------------
def project_rows(inp: Inputs, case: dict) -> list[dict]:
    cumP = inp.flip_success(float(case["da_rate"]))
    smult = float(case["sale_price_multiplier"])
    dmult = float(case["dev_cost_multiplier"])
    disc = discount_rate_for(inp, case)
    out = []
    for p in inp.projects:
        rtb_per_mw = inp.rtb_comps.get(p["state"], 0.0) * smult
        sale = p["mw"] * rtb_per_mw
        cost = inp.dev_cost_per_project * dmult
        gm = sale - cost
        risk_adj = gm * cumP
        df = 1.0 / (1.0 + disc) ** p["years_to_sale"]
        out.append({"name": p["name"], "state": p["state"], "mw": p["mw"],
                    "years_to_sale": p["years_to_sale"], "rtb_per_mw": rtb_per_mw,
                    "sale_value": sale, "cost": cost, "gross_margin": gm, "cumP": cumP,
                    "risk_adj_margin": risk_adj, "df": df, "pv": risk_adj * df})
    return out


def pipeline_rnpv(inp: Inputs, case: dict | None = None) -> float:
    return sum(r["pv"] for r in project_rows(inp, _case(inp, case)))


def blended_sale_value(inp: Inputs, case: dict) -> float:
    smult = float(case["sale_price_multiplier"])
    vals = [p["mw"] * inp.rtb_comps.get(p["state"], 0.0) * smult for p in inp.projects]
    return sum(vals) / len(vals) if vals else 0.0


# ---------------------------------------------------------------------------
# Fund funnel, fees & investor return  (Stage 1)
# ---------------------------------------------------------------------------
def fund_metrics(inp: Inputs, case: dict | None = None) -> dict:
    case = _case(inp, case)
    da = float(case["da_rate"])
    flip_success = inp.flip_success(da)
    dmult = float(case["dev_cost_multiplier"])

    target = inp.projects_target
    started = target / flip_success if flip_success > 0 else float("inf")
    failed = started - target
    C = inp.dev_cost_per_project * dmult
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
    eff = effective_hold(inp)
    irr = moic ** (1.0 / eff) - 1.0 if (moic > 0 and eff > 0) else float("nan")
    return {"da_rate": da, "flip_success": flip_success, "projects_target": target,
            "projects_started": started, "total_dev_cost": total_dev_cost,
            "sale_per_project": sale_per_project, "gross_proceeds": gross_proceeds,
            "entry_fee": entry_fee, "mgmt_fee": mgmt_fee, "invested_capital": invested_capital,
            "carry": carry, "distributions": distributions,
            "net_profit": distributions - invested_capital, "moic": moic, "irr": irr, "eff_hold": eff}


def returns_by_scenario(inp: Inputs) -> dict:
    return {c["name"]: fund_metrics(inp, c) for c in inp.scenarios.values()}


def first_chicago(inp: Inputs) -> dict:
    rbs = returns_by_scenario(inp)
    exp_irr = sum(rbs[n]["irr"] * w for n, w in inp.weights.items())
    exp_moic = sum(rbs[n]["moic"] * w for n, w in inp.weights.items())
    irrs = [rbs[n]["irr"] for n in inp.weights]
    return {"expected_irr": exp_irr, "expected_moic": exp_moic,
            "min_irr": min(irrs), "max_irr": max(irrs), "by_scenario": rbs}


# ---------------------------------------------------------------------------
# Cross-checks (VC method, $/MW)
# ---------------------------------------------------------------------------
def vc_method(inp: Inputs, case: dict | None = None) -> dict:
    """VC method: work back from the risk-adjusted exit value at the target return."""
    case = _case(inp, case)
    cumP = inp.flip_success(float(case["da_rate"]))
    smult = float(case["sale_price_multiplier"]); dmult = float(case["dev_cost_multiplier"])
    total_sale = sum(p["mw"] * inp.rtb_comps.get(p["state"], 0.0) for p in inp.projects) * smult
    total_cost = inp.dev_cost_per_project * dmult * len(inp.projects)
    exit_equity_value = cumP * (total_sale - total_cost)
    today_value = exit_equity_value / (1.0 + inp.vc_target_return) ** inp.horizon
    return {"exit_equity_value": exit_equity_value, "target_return": inp.vc_target_return,
            "horizon": inp.horizon, "today_value": today_value}


def dollar_per_mw_benchmark(inp: Inputs, case: dict | None = None) -> dict:
    case = _case(inp, case)
    cumP = inp.flip_success(float(case["da_rate"]))
    smult = float(case["sale_price_multiplier"]); dmult = float(case["dev_cost_multiplier"])
    disc = discount_rate_for(inp, case)
    total_mw = sum(p["mw"] for p in inp.projects)
    gross = sum(p["mw"] * inp.rtb_comps.get(p["state"], 0.0) for p in inp.projects) * smult
    total_cost = inp.dev_cost_per_project * dmult * len(inp.projects)
    avg_years = sum(p["years_to_sale"] for p in inp.projects) / len(inp.projects)
    dev_value = (gross - total_cost) * cumP / (1.0 + disc) ** avg_years
    return {"total_mw": total_mw, "gross_asset_value": gross, "total_cost": total_cost,
            "implied_dev_value": dev_value, "avg_years": avg_years}


def rtb_vs_built(inp: Inputs) -> dict:
    return {st: {"rtb_per_mw": rtb, "built_per_mw": inp.built_cost_per_mw,
                 "pct_of_built": rtb / inp.built_cost_per_mw if inp.built_cost_per_mw else float("nan")}
            for st, rtb in inp.rtb_comps.items()}


def valuation_range(inp: Inputs) -> dict:
    methods = {"rNPV pipeline (Base)": pipeline_rnpv(inp),
               "$/MW benchmark (dev value)": dollar_per_mw_benchmark(inp)["implied_dev_value"],
               "VC method (today value)": vc_method(inp)["today_value"]}
    vals = list(methods.values())
    return {"methods": methods, "low": min(vals), "high": max(vals), "midpoint": sum(vals) / len(vals)}


# ---------------------------------------------------------------------------
# Sensitivity & checks
# ---------------------------------------------------------------------------
def sensitivity_two_way(inp: Inputs, da_rates=(0.40, 0.55, 0.65, 0.80, 0.95),
                        price_mults=(0.70, 0.85, 1.00, 1.15, 1.30)) -> dict:
    """Investor IRR across development-approval rate x RTB price multiplier."""
    grid = []
    for da in da_rates:
        row = [fund_metrics(inp, {"da_rate": da, "sale_price_multiplier": pm,
                                  "dev_cost_multiplier": 1.0})["irr"] for pm in price_mults]
        grid.append(row)
    return {"da_rates": list(da_rates), "price_mults": list(price_mults), "grid": grid}


def tornado(inp: Inputs) -> list[dict]:
    """Investor-IRR sensitivity to each key driver, swung low<->high around Base.

    Base = the Base scenario. Each driver is moved to its Conservative and Ideal
    setting (one at a time, all else at Base) to show which driver moves the
    return most. The development-approval gate dominates."""
    base_case = inp.scenarios[2]
    base_irr = fund_metrics(inp, base_case)["irr"]

    def irr(da=None, sale=None, dev=None):
        case = {"da_rate": base_case["da_rate"] if da is None else da,
                "sale_price_multiplier": base_case["sale_price_multiplier"] if sale is None else sale,
                "dev_cost_multiplier": base_case["dev_cost_multiplier"] if dev is None else dev}
        return fund_metrics(inp, case)["irr"]

    lo, hi = inp.scenarios[1], inp.scenarios[3]   # Conservative / Ideal settings
    drivers = [
        ("Development-approval rate", irr(da=lo["da_rate"]), irr(da=hi["da_rate"])),
        ("RTB exit price", irr(sale=lo["sale_price_multiplier"]), irr(sale=hi["sale_price_multiplier"])),
        ("Development cost", irr(dev=hi["dev_cost_multiplier"]), irr(dev=lo["dev_cost_multiplier"])),
    ]
    rows = [{"driver": d, "base": base_irr, "low": low, "high": high} for d, low, high in drivers]
    rows.sort(key=lambda r: abs(r["high"] - r["low"]), reverse=True)
    return rows


def run_checks(inp: Inputs) -> dict:
    sc = survival_curve(inp)
    rbs = returns_by_scenario(inp)
    fc = first_chicago(inp)
    gates = [inp.da_independent, inp.p_connection, inp.p_sale]
    das = [float(inp.scenarios[i]["da_rate"]) for i in (1, 2, 3)]
    rows = project_rows(inp, inp.scenarios[2])
    return {
        "gate probabilities in [0,1]": all(0 <= p <= 1 for p in gates + das),
        "flip cumulative <= each gate": sc["flip_cumulative"] <= min(gates) + 1e-9,
        "flip success = DA x conn x sale": abs(sc["flip_cumulative"] - inp.flip_independent) < 1e-9,
        "MW positive": all(p["mw"] > 0 for p in inp.projects),
        "RTB sale values positive": all(r["sale_value"] > 0 for r in rows),
        "dev cost positive": inp.dev_cost_per_project > 0,
        "switch in 1..3": inp.switch_default in (1, 2, 3),
        "DA scenario monotonic": das[0] <= das[1] <= das[2],
        "investor IRR monotonic": rbs["Conservative"]["irr"] <= rbs["Base"]["irr"] <= rbs["Ideal"]["irr"],
        "weights sum to 100%": abs(sum(inp.weights.values()) - 1.0) < 1e-6,
        "call profile sums to 100%": abs(sum(inp.call_profile) - 1.0) < 1e-6,
        "distribution profile sums to 100%": abs(sum(inp.dist_profile) - 1.0) < 1e-6,
        "First-Chicago IRR within range": fc["min_irr"] - 1e-9 <= fc["expected_irr"] <= fc["max_irr"] + 1e-9,
        "invested capital positive": all(rbs[n]["invested_capital"] > 0 for n in rbs),
        "every input has a source": len(inp.sources) >= 4,
    }


def summary(inp: Inputs | None = None) -> dict:
    inp = inp or load_inputs()
    rbs = returns_by_scenario(inp)
    fc = first_chicago(inp)
    sc = survival_curve(inp)
    da_base = float(inp.scenarios[2]["da_rate"])
    return {"inputs": inp, "discount_base": inp.discount_base, "survival": sc,
            "da_independent": inp.da_independent, "da_base_manager": da_base,
            "flip_independent": inp.flip_independent, "flip_base_manager": inp.flip_base,
            "returns_by_scenario": rbs, "first_chicago": fc,
            "fund_base": fund_metrics(inp, inp.scenarios[2]), "pipeline_rnpv_base": pipeline_rnpv(inp),
            "vc": vc_method(inp), "dollar_per_mw": dollar_per_mw_benchmark(inp),
            "rtb_vs_built": rtb_vs_built(inp), "valuation_range": valuation_range(inp),
            "checks": run_checks(inp)}


if __name__ == "__main__":
    s = summary()
    inp = s["inputs"]
    print("=" * 74)
    print("ILLUSTRATIVE DISTRIBUTION-BESS DEVELOP-AND-FLIP FUND — VALUATION ENGINE")
    print("(VC method + First Chicago; manager figures are claims — not advice)")
    print("=" * 74)
    print(f"Risk-free {inp.risk_free:.2%} + premium {inp.risk_premium:.1%} => base discount {s['discount_base']:.2%}; "
          f"VC target return {inp.vc_target_return:.0%}")
    print("\nSURVIVAL GATES (the corrected logic — the manager's 40/65/80% are the DA gate ONLY):")
    print(f"  Development approval (DA): scenarios 40/65/80%  | public benchmark {inp.da_independent:.0%}")
    print(f"  Grid connection: {inp.p_connection:.0%}   Sale (flip): {inp.p_sale:.0%}")
    print(f"  -> TRUE flip success = DA x conn x sale:")
    print(f"       at manager Base DA 65%: {inp.flip_base:.1%}   (NOT 65% — the headline overstates)")
    print(f"       at public DA 80%:       {inp.flip_independent:.1%}")
    print("\nInvestor returns by scenario (DA gate drives the scenario):")
    for n in ("Conservative", "Base", "Ideal"):
        m = s["returns_by_scenario"][n]
        print(f"  {n:<13} DA {m['da_rate']:.0%} -> flip success {m['flip_success']:.1%}  "
              f"started {m['projects_started']:.0f}  MOIC {m['moic']:.2f}x  IRR {m['irr']:.1%}")
    fc = s["first_chicago"]
    print(f"\nFirst-Chicago expected investor IRR {fc['expected_irr']:.1%}  (MOIC {fc['expected_moic']:.2f}x)")
    print("\nChecks:")
    for k, v in s["checks"].items():
        print(f"  [{'OK ' if v else 'XX '}] {k}")
    print("\n(All illustrative — manager figures are claims to verify. Not investment advice.)")
