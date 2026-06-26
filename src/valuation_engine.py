"""Valuation engine — Python reference of the Excel model (direct-equity stake).

DEAL: we invest DIRECTLY as a SHAREHOLDER in one ILLUSTRATIVE battery-developer
startup. The company develops ~5 MW distribution batteries to shovel-ready
(ready-to-build, RTB) and SELLS them before construction (merchant risk passes to
the buyer). We are NOT a fund limited partner — we buy shares in the company.

CORRECTED GATE LOGIC (carried over):
  Each lifecycle gate is modelled SEPARATELY. The scenarios move ONLY the
  development-approval (DA) gate (manager/founder claim: 40 / 65 / 80%). A flip
  must clear THREE gates, so true success is the product:
      flip success = DA x grid connection (~70%) x sale (~80%)
  e.g. Base = 0.65 x 0.70 x 0.80 = 0.364 — NOT 65%.

HOW THE EQUITY VALUE IS BUILT:
  1. The company's development programme (the pipeline maths) gives its expected
     NET PROFIT in each scenario; we value the company at exit as a repeatable
     platform = net profit x an exit multiple -> the company's EXIT EQUITY VALUE.
  2. First-Chicago weights the scenarios.
  3. A CAP TABLE turns it into OUR return: ownership = investment / post-money,
     reduced by dilution (option pool + future rounds), then our exit proceeds =
     the GREATER of our 1x liquidation preference or our as-converted share.

All figures illustrative; many equity-deal inputs are [[TO CONFIRM]] placeholders.
Not investment advice.
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
    # company (the startup's development programme)
    programme_capital: float
    projects_target: float
    term_years: float
    call_profile: list
    dist_profile: list
    # direct-equity deal terms (cap table) — placeholders to confirm
    pre_money: float
    investment_amount: float
    option_pool_pct: float
    future_round_dilution_pct: float
    liquidation_pref_x: float
    exit_equity_multiple: float
    exit_year: float
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
        """Flip success = development approval x grid connection x sale."""
        return da * self.p_connection * self.p_sale

    @property
    def flip_independent(self) -> float:
        return self.flip_success(self.da_independent)

    @property
    def flip_base(self) -> float:
        return self.flip_success(float(self.scenarios[2]["da_rate"]))

    # --- cap table ---
    @property
    def post_money(self) -> float:
        return self.pre_money + self.investment_amount

    @property
    def ownership_initial(self) -> float:
        return self.investment_amount / self.post_money if self.post_money > 0 else float("nan")

    @property
    def ownership_diluted(self) -> float:
        return self.ownership_initial * (1.0 - self.option_pool_pct) * (1.0 - self.future_round_dilution_pct)


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

    co, eq = a["company"], a["equity_deal"]
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
        programme_capital=float(co["programme_capital_m"]["value"]),
        projects_target=float(co["projects_target"]["value"]),
        term_years=float(co["term_years"]["value"]),
        call_profile=list(co["capital_call_profile"]["value"]),
        dist_profile=list(co["distribution_profile"]["value"]),
        pre_money=float(eq["pre_money_m"]["value"]),
        investment_amount=float(eq["investment_amount_m"]["value"]),
        option_pool_pct=float(eq["option_pool_pct"]["value"]),
        future_round_dilution_pct=float(eq["future_round_dilution_pct"]["value"]),
        liquidation_pref_x=float(eq["liquidation_preference_x"]["value"]),
        exit_equity_multiple=float(eq["exit_equity_multiple"]["value"]),
        exit_year=float(eq["exit_year"]["value"]),
        scenarios=a["scenarios"]["cases"], weights=a["scenarios"]["weights"],
        switch_default=int(a["scenarios"]["switch_default"]),
        projects=projects, sources=sources,
    )


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def _case(inp: Inputs, case: dict | None) -> dict:
    return case if case is not None else inp.scenarios[2]


def survival_curve(inp: Inputs, da: float | None = None) -> dict:
    """The flip survival chain (development approval -> connection -> sale)."""
    da = inp.da_independent if da is None else da
    s1 = da
    s2 = s1 * inp.p_connection
    s3 = s2 * inp.p_sale
    return {"development_approval": da, "grid_connection": inp.p_connection, "reach_sale": inp.p_sale,
            "after_approval": s1, "after_connection": s2, "flip_cumulative": s3}


def discount_rate_for(inp: Inputs, case: dict) -> float:
    return inp.discount_base   # asset cross-check discount; scenarios don't move it


def cap_table(inp: Inputs) -> dict:
    """Our stake before dilution -> after dilution (option pool + future rounds)."""
    return {"pre_money": inp.pre_money, "investment": inp.investment_amount,
            "post_money": inp.post_money, "ownership_initial": inp.ownership_initial,
            "option_pool_pct": inp.option_pool_pct, "future_round_dilution_pct": inp.future_round_dilution_pct,
            "ownership_diluted": inp.ownership_diluted}


# ---------------------------------------------------------------------------
# Per-project risk-adjusted NAV (rNPV) — company asset cross-check
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
# The company's development programme & exit equity value (per scenario)
# ---------------------------------------------------------------------------
def company_metrics(inp: Inputs, case: dict | None = None) -> dict:
    """The company's own business plan: funnel -> net programme profit -> the
    company's exit equity value (net profit x platform exit multiple)."""
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

    net_business_profit = gross_proceeds - total_dev_cost
    company_exit_equity = max(0.0, net_business_profit) * inp.exit_equity_multiple

    # company-level (business) return on the development programme, over the term
    business_moic = gross_proceeds / total_dev_cost if total_dev_cost > 0 else float("nan")
    business_irr = business_moic ** (1.0 / inp.term_years) - 1.0 if (business_moic > 0 and inp.term_years > 0) else -1.0
    return {"da_rate": da, "flip_success": flip_success, "projects_target": target,
            "projects_started": started, "total_dev_cost": total_dev_cost,
            "sale_per_project": sale_per_project, "gross_proceeds": gross_proceeds,
            "net_business_profit": net_business_profit, "company_exit_equity": company_exit_equity,
            "business_moic": business_moic, "business_irr": business_irr}


# ---------------------------------------------------------------------------
# OUR return as a shareholder (cap table -> dilution -> liquidation preference)
# ---------------------------------------------------------------------------
def investor_return(inp: Inputs, case: dict | None = None) -> dict:
    """Return on OUR shares: diluted ownership of the company's exit equity value,
    floored/greater-of by a 1x non-participating liquidation preference."""
    cm = company_metrics(inp, case)
    inv = inp.investment_amount
    eq = cm["company_exit_equity"]
    diluted = inp.ownership_diluted

    pref_claim = min(inp.liquidation_pref_x * inv, eq)     # preference, capped by what's available
    as_converted = diluted * eq                            # convert to ordinary
    proceeds = max(pref_claim, as_converted)               # 1x non-participating: the greater

    moic = proceeds / inv if inv > 0 else float("nan")
    irr = moic ** (1.0 / inp.exit_year) - 1.0 if (moic > 0 and inp.exit_year > 0) else -1.0
    return {**cm, "ownership_diluted": diluted, "invested_capital": inv,
            "our_proceeds": proceeds, "pref_claim": pref_claim, "as_converted": as_converted,
            "took_preference": pref_claim > as_converted, "moic": moic, "irr": irr,
            "exit_year": inp.exit_year}


def returns_by_scenario(inp: Inputs) -> dict:
    """OUR equity return (on our shares) by scenario."""
    return {c["name"]: investor_return(inp, c) for c in inp.scenarios.values()}


def first_chicago(inp: Inputs) -> dict:
    """Probability-weight OUR proceeds, then derive the expected MOIC/IRR.

    Weighting proceeds (not IRRs) is the correct treatment: a total-loss scenario
    has IRR -100%, which cannot be linearly averaged with positive IRRs."""
    rbs = returns_by_scenario(inp)
    inv = inp.investment_amount
    exp_proceeds = sum(rbs[n]["our_proceeds"] * w for n, w in inp.weights.items())
    exp_moic = exp_proceeds / inv if inv > 0 else float("nan")
    exp_irr = exp_moic ** (1.0 / inp.exit_year) - 1.0 if (exp_moic > 0 and inp.exit_year > 0) else -1.0
    irrs = [rbs[n]["irr"] for n in inp.weights]
    return {"expected_proceeds": exp_proceeds, "expected_moic": exp_moic, "expected_irr": exp_irr,
            "min_irr": min(irrs), "max_irr": max(irrs), "by_scenario": rbs}


def develop_flip_business(inp: Inputs) -> dict:
    """Company-level (business-model) develop-and-flip return — for the value-chain
    comparison (NOT our diluted stake). First-Chicago across scenarios."""
    cms = {c["name"]: company_metrics(inp, c) for c in inp.scenarios.values()}
    exp_moic = sum(cms[n]["business_moic"] * w for n, w in inp.weights.items())
    exp_irr = exp_moic ** (1.0 / inp.term_years) - 1.0 if (exp_moic > 0 and inp.term_years > 0) else -1.0
    return {"by_scenario": cms, "expected_moic": exp_moic, "expected_irr": exp_irr,
            "downside_irr": cms["Conservative"]["business_irr"], "downside_moic": cms["Conservative"]["business_moic"]}


# ---------------------------------------------------------------------------
# Company asset cross-checks (VC method, $/MW) — sense-check the company's value
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
    """OUR equity IRR across development-approval rate x RTB price multiplier."""
    grid = []
    for da in da_rates:
        row = [investor_return(inp, {"da_rate": da, "sale_price_multiplier": pm,
                                     "dev_cost_multiplier": 1.0})["irr"] for pm in price_mults]
        grid.append(row)
    return {"da_rates": list(da_rates), "price_mults": list(price_mults), "grid": grid}


def tornado(inp: Inputs) -> list[dict]:
    """OUR equity-IRR sensitivity to each business driver, swung low<->high around Base."""
    base_case = inp.scenarios[2]
    base_irr = investor_return(inp, base_case)["irr"]

    def irr(da=None, sale=None, dev=None):
        case = {"da_rate": base_case["da_rate"] if da is None else da,
                "sale_price_multiplier": base_case["sale_price_multiplier"] if sale is None else sale,
                "dev_cost_multiplier": base_case["dev_cost_multiplier"] if dev is None else dev}
        return investor_return(inp, case)["irr"]

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
    ct = cap_table(inp)
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
        "ownership = investment / post-money": abs(ct["ownership_initial"] - inp.investment_amount / inp.post_money) < 1e-9,
        "post-money = pre-money + investment": abs(inp.post_money - (inp.pre_money + inp.investment_amount)) < 1e-9,
        "diluted ownership <= initial": ct["ownership_diluted"] <= ct["ownership_initial"] + 1e-9,
        "investor MOIC monotonic": rbs["Conservative"]["moic"] <= rbs["Base"]["moic"] <= rbs["Ideal"]["moic"],
        "weights sum to 100%": abs(sum(inp.weights.values()) - 1.0) < 1e-6,
        "First-Chicago IRR within range": fc["min_irr"] - 1e-9 <= fc["expected_irr"] <= fc["max_irr"] + 1e-9,
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
            "cap_table": cap_table(inp), "company_base": company_metrics(inp, inp.scenarios[2]),
            "returns_by_scenario": rbs, "first_chicago": fc,
            "business_returns": develop_flip_business(inp),
            "pipeline_rnpv_base": pipeline_rnpv(inp),
            "vc": vc_method(inp), "dollar_per_mw": dollar_per_mw_benchmark(inp),
            "rtb_vs_built": rtb_vs_built(inp), "valuation_range": valuation_range(inp),
            "checks": run_checks(inp)}


if __name__ == "__main__":
    s = summary()
    inp = s["inputs"]; ct = s["cap_table"]; fc = s["first_chicago"]
    print("=" * 74)
    print("ILLUSTRATIVE BATTERY-DEVELOPER STARTUP — DIRECT-EQUITY VALUATION ENGINE")
    print("(cap table + First Chicago; founder figures are claims — not advice)")
    print("=" * 74)
    print("\nSURVIVAL GATES (the manager/founder 40/65/80% are the DA gate ONLY):")
    print(f"  Development approval: scenarios 40/65/80%  | public benchmark {inp.da_independent:.0%}")
    print(f"  Grid connection: {inp.p_connection:.0%}   Sale (flip): {inp.p_sale:.0%}")
    print(f"  -> TRUE flip success at Base DA 65%: {inp.flip_base:.1%}  (NOT 65%)")
    print("\nCAP TABLE (PLACEHOLDERS — confirm):")
    print(f"  ${ct['investment']:.1f}m into ${ct['pre_money']:.1f}m pre -> ${ct['post_money']:.1f}m post "
          f"=> {ct['ownership_initial']:.1%} initial, {ct['ownership_diluted']:.1%} after dilution")
    print(f"  Company exit equity = net programme profit x {inp.exit_equity_multiple:.1f} (Base "
          f"${s['company_base']['company_exit_equity']:.1f}m); 1x liq pref; exit yr {inp.exit_year:.0f}")
    print("\nReturn on OUR shares by scenario:")
    for n in ("Conservative", "Base", "Ideal"):
        m = s["returns_by_scenario"][n]
        print(f"  {n:<13} flip {m['flip_success']:.1%}  company exit equity ${m['company_exit_equity']:>5.1f}m  "
              f"our proceeds ${m['our_proceeds']:.2f}m  MOIC {m['moic']:.2f}x  IRR {m['irr']:.1%}")
    print(f"\nFirst-Chicago expected: MOIC {fc['expected_moic']:.2f}x  IRR {fc['expected_irr']:.1%}  "
          f"(range {fc['min_irr']:.0%}..{fc['max_irr']:.0%})")
    print("\nChecks:")
    for k, v in s["checks"].items():
        print(f"  [{'OK ' if v else 'XX '}] {k}")
    print("\n(Illustrative; equity-deal inputs are placeholders to confirm. Not investment advice.)")
