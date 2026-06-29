"""Three-stage value-chain analysis — where to invest along the chain.

Compares the three ways to put money into the SAME ~5 MW distribution battery,
each as a risk-adjusted LEVERED EQUITY return (IRR / MOIC), so they are directly
comparable as investment choices:

  Stage 1  Develop & flip  — win approvals, sell RTB           (company develop-and-flip business return)
  Stage 2  Build & sell    — buy RTB, construct, sell the asset (construction model + completion risk)
  Stage 3  Own & operate   — own the operating asset ~15 yrs   (levered operating DCF + merchant scenarios)

This is the classic infrastructure risk ladder: development (highest risk) ->
construction (medium) -> operation (lowest, if contracted). All inputs are
ILLUSTRATIVE benchmarks from config/assumptions.yaml (the analyst's to OWN and
verify) — battery revenue and capex are genuinely uncertain and merchant-driven.

Run:  python -m src.stage_analysis      (prints the comparison)
Not investment advice.
"""
from __future__ import annotations

from src.utils import io
from src import valuation_engine as ve


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def irr(cashflows: list[float], lo: float = -0.95, hi: float = 5.0, tol: float = 1e-7) -> float:
    """IRR of annual cash flows by period index 0,1,2,...; nan if no sign change."""
    def npv(r: float) -> float:
        return sum(cf / (1.0 + r) ** t for t, cf in enumerate(cashflows))
    f_lo, f_hi = npv(lo), npv(hi)
    if f_lo == 0:
        return lo
    if f_lo * f_hi > 0:
        return float("nan")
    for _ in range(200):
        mid = (lo + hi) / 2.0
        f_mid = npv(mid)
        if abs(f_mid) < tol:
            return mid
        if f_lo * f_mid < 0:
            hi = mid
        else:
            lo, f_lo = mid, f_mid
    return (lo + hi) / 2.0


def _cagr(moic: float, years: float) -> float:
    return moic ** (1.0 / years) - 1.0 if (moic > 0 and years > 0) else float("nan")


class Stages:
    """Loads the stage inputs (config + reused engine inputs)."""
    def __init__(self):
        a = io.load_assumptions()
        s = a["stages"]
        self.ref = s["ref_project"]
        self.con = s["construction"]
        self.op = s["operating"]
        self.scen = s["operating_scenarios"]
        self.integrated = s.get("integrated", {"dev_to_rtb_years": 1.75})
        self.mw = float(self.ref["mw"])
        self.state = self.ref["state"]
        # engine inputs (RTB price by state; the company's develop-and-flip return for Stage 1)
        self.inp = ve.load_inputs()
        self.rtb_per_mw = float(self.inp.rtb_comps.get(self.state, 0.0))

    @property
    def rtb_value(self) -> float:
        return self.mw * self.rtb_per_mw

    @property
    def build_cost(self) -> float:
        return self.mw * float(self.con["build_cost_per_mw_m"])

    @property
    def total_build(self) -> float:
        return self.rtb_value + self.build_cost


# ---------------------------------------------------------------------------
# Operating asset (used by Stage 3, and to value Stage 2's exit)
# ---------------------------------------------------------------------------
def _project_fcf(st: Stages, mult: float) -> tuple[list[float], float]:
    """Annual project free cash flow (~EBITDA) and the terminal EV at end of life.

    Merchant portion is scaled by `mult`; the contracted portion is stable.
    Simplification: FCF ~ EBITDA (no tax / maintenance capex), flagged in docs.
    """
    op = st.op
    base_rev = st.mw * float(op["revenue_per_mw_yr_m"])
    contracted = base_rev * float(op["contracted_share"])
    merchant0 = base_rev * (1.0 - float(op["contracted_share"]))
    opex = st.mw * float(op["opex_per_mw_yr_m"])
    deg = float(op["degradation_pa"])
    life = int(op["life_years"])
    fcf, ebitda_last = [], 0.0
    for t in range(1, life + 1):
        factor = (1.0 - deg) ** (t - 1)
        revenue = (contracted + merchant0 * mult) * factor
        ebitda = revenue - opex
        fcf.append(ebitda)
        ebitda_last = ebitda
    terminal = ebitda_last * float(op["terminal_ebitda_multiple"])
    return fcf, terminal


def operating_ev(st: Stages, mult: float = 1.0) -> float:
    """Unlevered enterprise value of the operating asset (PV of FCF + terminal)."""
    fcf, terminal = _project_fcf(st, mult)
    r = float(st.op["asset_discount"])
    life = len(fcf)
    return sum(cf / (1.0 + r) ** t for t, cf in enumerate(fcf, start=1)) + terminal / (1.0 + r) ** life


def stage3_scenario(st: Stages, mult: float) -> dict:
    """Levered equity IRR/MOIC for owning the operating asset under a merchant scenario.

    Acquire at the asset's market value (base-case EV); realise cash flows under
    `mult`; amortise project debt straight-line over its tenor; exit at terminal EV.
    """
    op = st.op
    entry_ev = operating_ev(st, 1.0)          # bought at market (base expectations)
    debt0 = float(op["gearing"]) * entry_ev
    equity0 = entry_ev - debt0
    fcf, terminal = _project_fcf(st, mult)
    life = len(fcf)
    tenor = int(op["debt_tenor_years"])
    rate = float(op["debt_rate"])
    principal = debt0 / tenor
    bal = debt0
    eq_cf = []
    for t in range(1, life + 1):
        interest = bal * rate
        prin = principal if t <= tenor else 0.0
        bal = max(0.0, bal - prin)
        eq_cf.append(fcf[t - 1] - interest - prin)
    eq_cf[-1] += terminal - bal               # exit: sell at terminal EV, clear residual debt
    distributions = sum(c for c in eq_cf)
    moic = (distributions + equity0) / equity0 if equity0 > 0 else float("nan")
    # MOIC here = total returned / invested (distributions are net of debt service)
    moic = distributions / equity0 if equity0 > 0 else float("nan")
    return {"mult": mult, "entry_ev": entry_ev, "equity0": equity0,
            "irr": irr([-equity0] + eq_cf), "moic": moic}


def stage3(st: Stages) -> dict:
    """Probability-weighted Stage 3 return across merchant scenarios."""
    sc = st.scen
    w = sc["weights"]
    res = {name: stage3_scenario(st, float(sc[name])) for name in ("low", "base", "high")}
    exp_irr = sum(res[n]["irr"] * float(w[n]) for n in res)
    exp_moic = sum(res[n]["moic"] * float(w[n]) for n in res)
    return {"by_scenario": res, "expected_irr": exp_irr, "expected_moic": exp_moic,
            "downside_irr": res["low"]["irr"], "equity0": res["base"]["equity0"],
            "hold_years": float(st.op["life_years"])}


# ---------------------------------------------------------------------------
# Stage 4 — integrated: develop -> build -> operate the SAME asset
# ---------------------------------------------------------------------------
def _integrated_basis(st: Stages) -> tuple[float, float, float]:
    """Reach-operation probability, grossed development cost, and net equity sunk.

    Development survival for an integrated owner = planning x grid connection
    (the 'reach sale' gate does NOT apply — the asset is kept, not sold), times
    construction completion. Development cost is grossed for the funnel of failed
    attempts; the operating asset is financed at the operating gearing.
    """
    da = float(st.inp.scenarios[2]["da_rate"])                # Base development-approval rate
    p_dev = da * st.inp.p_connection                          # approval x connection (no sale gate — kept)
    reach_op = max(1e-6, p_dev * float(st.con["completion_prob"]))
    abandon = st.inp.abandonment_fraction
    dev_cost = st.inp.dev_cost_per_project
    dev_total = dev_cost * (1.0 + abandon * (1.0 / reach_op - 1.0))   # funnel-grossed
    op_debt = float(st.op["gearing"]) * operating_ev(st, 1.0)
    equity0 = dev_total + st.build_cost - op_debt              # equity sunk to develop + build
    return reach_op, dev_total, equity0


def stage4_scenario(st: Stages, mult: float) -> dict:
    """Levered equity IRR for develop->build->operate under a merchant scenario."""
    reach_op, dev_total, equity0 = _integrated_basis(st)
    op = st.op
    op_debt = float(op["gearing"]) * operating_ev(st, 1.0)
    fcf, terminal = _project_fcf(st, mult)
    life = len(fcf)
    tenor, rate = int(op["debt_tenor_years"]), float(op["debt_rate"])
    principal, bal, eq_cf = op_debt / tenor, op_debt, []
    for t in range(1, life + 1):
        interest = bal * rate
        prin = principal if t <= tenor else 0.0
        bal = max(0.0, bal - prin)
        eq_cf.append(fcf[t - 1] - interest - prin)
    eq_cf[-1] += terminal - bal
    lead = int(round(float(st.integrated["dev_to_rtb_years"]) + float(st.con["build_years"])))
    cf = [-equity0] + [0.0] * (lead - 1) + eq_cf               # equity sunk up front; cash flows after the build lead
    moic = sum(eq_cf) / equity0 if equity0 > 0 else float("nan")
    return {"mult": mult, "irr": irr(cf), "moic": moic, "equity0": equity0, "lead": lead, "life": life}


def stage4(st: Stages) -> dict:
    """Probability-weighted integrated (develop->build->operate) return."""
    sc, w = st.scen, st.scen["weights"]
    res = {n: stage4_scenario(st, float(sc[n])) for n in ("low", "base", "high")}
    exp_irr = sum(res[n]["irr"] * float(w[n]) for n in res)
    exp_moic = sum(res[n]["moic"] * float(w[n]) for n in res)
    reach_op, _, _ = _integrated_basis(st)
    return {"by_scenario": res, "expected_irr": exp_irr, "expected_moic": exp_moic,
            "downside_irr": res["low"]["irr"], "equity0": res["base"]["equity0"],
            "reach_op": reach_op, "hold_years": res["base"]["lead"] + res["base"]["life"]}


# ---------------------------------------------------------------------------
# Stage 2 — build & sell
# ---------------------------------------------------------------------------
def stage2(st: Stages) -> dict:
    """Buy RTB, build (levered), sell the operating asset; risk-adjust for completion."""
    con = st.con
    years = float(con["build_years"])
    gearing = float(con["gearing"])
    total = st.total_build
    debt = gearing * total
    equity = total - debt
    sale_ev = operating_ev(st, 1.0)                 # sell at base operating market value

    proceeds_success = sale_ev - debt
    proceeds_fail = float(con["salvage_on_failure"]) * equity
    p = float(con["completion_prob"])
    exp_proceeds = p * proceeds_success + (1.0 - p) * proceeds_fail
    exp_moic = exp_proceeds / equity if equity > 0 else float("nan")

    # downside: cost overrun (equity-funded) AND sell at the low merchant EV, still completes
    overrun = float(con["cost_overrun_downside"])
    equity_d = (total + st.build_cost * overrun) - debt
    proceeds_d = operating_ev(st, float(st.scen["low"])) - debt
    moic_d = proceeds_d / equity_d if equity_d > 0 else float("nan")

    return {"total_cost": total, "equity0": equity, "sale_ev": sale_ev,
            "expected_moic": exp_moic, "expected_irr": _cagr(exp_moic, years),
            "downside_moic": moic_d, "downside_irr": _cagr(moic_d, years),
            "hold_years": years, "completion_prob": p}


# ---------------------------------------------------------------------------
# Stage 1 — develop & flip (reuse the fund engine)
# ---------------------------------------------------------------------------
def stage1(st: Stages) -> dict:
    # company-level develop-and-flip BUSINESS return (the business model), not our
    # diluted shareholding — so it is comparable to the other stages.
    b = ve.develop_flip_business(st.inp)
    return {"expected_irr": b["expected_irr"], "expected_moic": b["expected_moic"],
            "downside_irr": b["downside_irr"], "downside_moic": b["downside_moic"],
            "hold_years": st.inp.term_years}


# ---------------------------------------------------------------------------
# Comparison
# ---------------------------------------------------------------------------
def compare(st: Stages | None = None) -> dict:
    st = st or Stages()
    s1, s2, s3, s4 = stage1(st), stage2(st), stage3(st), stage4(st)
    rows = [
        {"stage": "Stage 1 — Develop & flip (RTB)",
         "capital": "Low (~$0.5m dev/project; company programme ~$25m)", "hold": f"~{s1['hold_years']:.0f} yrs",
         "expected_irr": s1["expected_irr"], "expected_moic": s1["expected_moic"],
         "downside_irr": s1["downside_irr"],
         "key_risk": "Approvals on time + a buyer pays (can lose capital)"},
        {"stage": "Stage 2 — Build & sell",
         "capital": f"High (~${s2['equity0']:.1f}m equity / ${s2['total_cost']:.1f}m project)",
         "hold": f"~{s2['hold_years']:.1f} yrs",
         "expected_irr": s2["expected_irr"], "expected_moic": s2["expected_moic"],
         "downside_irr": s2["downside_irr"],
         "key_risk": "Construction cost/delay + thin build margin (can lose capital)"},
        {"stage": "Stage 3 — Own & operate",
         "capital": f"Highest (~${s3['equity0']:.1f}m equity), locked up longest",
         "hold": f"~{s3['hold_years']:.0f} yrs",
         "expected_irr": s3["expected_irr"], "expected_moic": s3["expected_moic"],
         "downside_irr": s3["downside_irr"],
         "key_risk": "Merchant price risk (steady if contracted)"},
        {"stage": "Stage 4 — Integrated (develop→build→operate)",
         "capital": f"Highest, longest (~${s4['equity0']:.1f}m equity; only ~{s4['reach_op']:.0%} of starts reach operation)",
         "hold": f"~{s4['hold_years']:.0f} yrs",
         "expected_irr": s4["expected_irr"], "expected_moic": s4["expected_moic"],
         "downside_irr": s4["downside_irr"],
         "key_risk": "ALL risks stacked: development + construction + merchant (but NO buyer/exit risk)"},
    ]
    return {"stages": st, "s1": s1, "s2": s2, "s3": s3, "s4": s4, "rows": rows}


# ---------------------------------------------------------------------------
# Value ladder (change8) — staged exit: sell after approval / construction / operating
# ---------------------------------------------------------------------------
def value_ladder(st: Stages | None = None) -> dict:
    """When should we sell our shares? Company equity and OUR share value if the
    company sells at each rung — R1 after approval (RTB), R2 after construction,
    R3 after operating — under Option A (ownership % held constant) and Option B
    (new equity to build/operate dilutes us). First-Chicago weighted across
    scenarios. Reuses the stage engine; R1 is anchored to the forward-pipeline
    company equity (so it ties to IC_MEMO §6); R2/R3 are illustrative uplifts."""
    st = st or Stages()
    inp = st.inp
    a = io.load_assumptions()
    vl = a["value_ladder"]
    yr1 = float(vl["years_to_r1"]["value"])
    build_years = float(st.con["build_years"])
    ramp = float(vl["operating_ramp_years"]["value"])
    prem = float(vl["stabilised_premium"]["value"])
    dil_r2 = float(vl["equity_dilution_r2"]["value"])
    dil_r3 = float(vl["equity_dilution_r3"]["value"])
    yrs = {"R1": yr1, "R2": yr1 + build_years, "R3": yr1 + build_years + ramp}

    disc = inp.discount_base
    inv = inp.investment_amount
    diluted = inp.ownership_diluted
    pref = inp.liquidation_pref_x * inv
    conn, sale, constr = inp.p_connection, inp.p_sale, float(st.con["completion_prob"])
    dev = inp.dev_cost_per_project
    build = st.build_cost
    merch = {"Conservative": float(st.scen["low"]), "Base": float(st.scen["base"]), "Ideal": float(st.scen["high"])}
    rungs = ("R1", "R2", "R3")

    def df(years):
        return 1.0 / (1.0 + disc) ** years

    # ownership %: A holds it constant; B dilutes for equity raised to build/operate
    dilB = {"R1": diluted, "R2": diluted * (1 - dil_r2), "R3": diluted * (1 - dil_r2) * (1 - dil_r3)}

    per_scn = {}
    for case in inp.scenarios.values():
        name = case["name"]
        da, smult, dmult = float(case["da_rate"]), float(case["sale_price_multiplier"]), float(case["dev_cost_multiplier"])
        rtb = st.mw * st.rtb_per_mw * smult
        devc = dev * dmult
        opev = operating_ev(st, merch[name])
        net_r1_ref = max(1e-9, rtb - devc)
        net_r2 = max(0.0, opev - build - devc)
        net_r3 = max(0.0, opev * (1.0 + prem) - build - devc)
        reach_rtb = da * conn
        p_r1, p_r23 = reach_rtb * sale, reach_rtb * constr
        den = net_r1_ref * p_r1 * df(yrs["R1"])
        # R1 anchored to the forward-pipeline company equity (ties to the memo)
        eq_r1 = ve.exit_equity_value(inp, case)["company_exit_equity"]
        uplift_r2 = (net_r2 * p_r23 * df(yrs["R2"])) / den if den > 0 else 0.0
        uplift_r3 = (net_r3 * p_r23 * df(yrs["R3"])) / den if den > 0 else 0.0
        eqA = {"R1": eq_r1, "R2": eq_r1 * uplift_r2, "R3": eq_r1 * uplift_r3}
        # pref floors our downside but is capped by the equity available (greater-of, as in the main engine)
        ourA = {r: max(min(pref, eqA[r]), diluted * eqA[r]) for r in rungs}
        ourB = {"R1": ourA["R1"],                                       # no new funding at R1
                "R2": dilB["R2"] * eqA["R2"], "R3": dilB["R3"] * eqA["R3"]}  # pref subordinated by new senior money
        per_scn[name] = {"eqA": eqA, "ourA": ourA, "ourB": ourB}

    w = inp.weights

    def fc(key):
        return {r: sum(per_scn[n][key][r] * float(w[n]) for n in per_scn) for r in rungs}
    eqA_fc, ourA_fc, ourB_fc = fc("eqA"), fc("ourA"), fc("ourB")

    def moic(x):
        return x / inv if inv > 0 else float("nan")

    def irr(m, years):
        return m ** (1.0 / years) - 1.0 if (m > 0 and years > 0) else -1.0

    out = {"years": yrs, "diluted_A": diluted, "diluted_B": dilB, "by_scenario": per_scn, "rungs": {}}
    for r in rungs:
        mA, mB = moic(ourA_fc[r]), moic(ourB_fc[r])
        out["rungs"][r] = {"company_equity": eqA_fc[r],
                           "our_share_A": ourA_fc[r], "moic_A": mA, "irr_A": irr(mA, yrs[r]),
                           "our_share_B": ourB_fc[r], "moic_B": mB, "irr_B": irr(mB, yrs[r]),
                           "years": yrs[r]}
    out["best_A"] = max(rungs, key=lambda r: out["rungs"][r]["irr_A"])
    out["best_B"] = max(rungs, key=lambda r: out["rungs"][r]["irr_B"])
    return out


def _pct(x):
    return "n/a" if x != x else f"{x:.1%}"   # x!=x catches nan


STAGE_MD = io.PROJECT_ROOT / "financial_models" / "STAGE_COMPARISON.md"


def write_markdown(path=STAGE_MD) -> None:
    """Write the GitHub-viewable three-stage comparison (tables + recommendation)."""
    c = compare()
    st = c["stages"]
    ev = operating_ev(st)
    mwh = st.mw * float(st.ref["duration_h"])
    s3 = c["s3"]["by_scenario"]
    L = []
    L.append("# Three-stage value-chain analysis — where to invest")
    L.append("")
    L.append("> Comparing the three ways to put money into the **same ~5 MW distribution battery**, each as a "
             "risk-adjusted **levered equity return**. This is the classic infrastructure risk ladder: "
             "**development → construction → operation.** *Illustrative — battery revenue and capex are uncertain "
             "(the analyst's inputs to own and verify); not investment advice.*")
    L.append("")
    L.append(f"**Reference asset:** {st.mw:.0f} MW / {mwh:.0f} MWh ({st.state}) — "
             f"RTB value ${st.rtb_value:.1f}m · build cost ${st.build_cost:.1f}m · operating value (EV) ${ev:.1f}m "
             f"(**build margin ${ev - st.total_build:+.1f}m**).")
    L.append("")
    L.append("## Risk–return by stage")
    L.append("")
    L.append("| Stage | Hold | Capital | Expected IRR | Expected MOIC | Downside IRR | Main risk |")
    L.append("|---|---|---|---|---|---|---|")
    for r in c["rows"]:
        L.append(f"| {r['stage']} | {r['hold']} | {r['capital']} | **{_pct(r['expected_irr'])}** | "
                 f"{r['expected_moic']:.2f}x | **{_pct(r['downside_irr'])}** | {r['key_risk']} |")
    L.append("")
    L.append("![Risk-return by stage](../outputs/figures/stage_comparison.png)")
    L.append("")
    L.append("## Value ladder — our return if we sell at each rung")
    L.append("")
    vl = value_ladder(st)
    L.append("> We own the company and choose **when to sell**: R1 after approval (ready-to-build), R2 after "
             "construction, R3 after operating. **Option A** holds our ownership % constant; **Option B** funds the "
             "climb (new equity dilutes us, debt ranks ahead). First-Chicago weighted; illustrative. R1 ties to "
             "IC_MEMO §7 (0.88x MOIC).")
    L.append("")
    L.append("| Rung — sell after… | Company equity | Our share (A) | MOIC (A) | IRR (A) | Our share (B) | MOIC (B) | IRR (B) | Years |")
    L.append("|---|---|---|---|---|---|---|---|---|")
    labels = {"R1": "R1 approval (RTB)", "R2": "R2 construction", "R3": "R3 operating"}
    for r in ("R1", "R2", "R3"):
        d = vl["rungs"][r]
        L.append(f"| {labels[r]} | ${d['company_equity']:.1f}m | ${d['our_share_A']:.2f}m | {d['moic_A']:.2f}x | "
                 f"{_pct(d['irr_A'])} | ${d['our_share_B']:.2f}m | {d['moic_B']:.2f}x | {_pct(d['irr_B'])} | {d['years']:.1f} |")
    L.append("")
    L.append(f"**Best rung — Option A (no funding): {vl['best_A']}. Option B (realistic, with funding): {vl['best_B']}.** "
             f"Holding longer grows the company's equity but dilutes our slice (A holds {vl['diluted_A']:.1%}; "
             f"B falls to {vl['diluted_B']['R3']:.1%} by R3) — the funding drag. Years, stabilised premium and "
             "equity-raise dilution are placeholders to confirm.")
    L.append("")
    L.append("## Stage 3 (own & operate) by merchant-price scenario")
    L.append("")
    L.append("| Scenario | Merchant revenue | Equity IRR | MOIC |")
    L.append("|---|---|---|---|")
    for n in ("low", "base", "high"):
        r = s3[n]
        L.append(f"| {n.title()} | ×{r['mult']:.2f} | {_pct(r['irr'])} | {r['moic']:.2f}x |")
    L.append("")
    L.append("## What it means — which stage to choose")
    L.append("")
    L.append("- **The development gates apply to Stage 1 only.** The founder's 40/65/80% are the development-approval gate; "
             "true flip success = approval × grid connection × sale ≈ 36% at Base. Stage 2 and Stage 3 buy a project that has "
             "*already* cleared development, at its market price, so they bear construction-completion (~90%) and merchant-price "
             "risk instead — not the development gates. Each stage is priced at its own entry point.")
    L.append("- **Stage 3 (own & operate, *contracted*) — the natural core holding.** It is the only stage that "
             "**stays positive in its downside**, giving steady, long-dated, capital-preserving yield. It also plays to a "
             "credit-risk edge: judging whether the toll/offtake counterparty will pay is *serviceability analysis*. "
             "Avoid uncontracted / merchant-only operating assets.")
    L.append("- **Stage 1 (develop & flip) — a smaller satellite only.** Higher expected return, capital-light and short, "
             "but it can lose capital and rests on optimistic manager assumptions. Suitable for the risk-tolerant slice, "
             "on strict conditions.")
    L.append("- **Stage 2 (build & sell) — skip as a standalone.** It shows the highest *expected* return, but it is the "
             "**most fragile**: it depends entirely on the built asset being worth more than it costs to build (a thin, "
             "merchant-dependent margin), its downside is a heavy loss, and it needs construction expertise. Fine only "
             "inside a managed vehicle.")
    L.append("- **Stage 4 (integrated: develop → build → operate) — for a patient owner-operator, not a passive investor.** "
             "Carrying one project the whole way captures the entire value chain (development + construction margin + "
             "operating yield) and **removes the buyer/exit risk** — you keep the asset, so the 'reach-sale' gate disappears "
             "and development survival is just planning × connection. The trade-offs: the **longest lock-up (~18 years)** and "
             "bearing development + construction + merchant risk together. Only ~50% of started developments reach operation "
             "(development is cheap, so the failures cost little); the downside shown is the low-merchant case *given the "
             "project reaches operation*. Because you build the asset at cost rather than buying it at market, the operating "
             "returns are strong and the downside stays positive — if you have the patience and the operating capability.")
    L.append("- **Watch the alignment trap.** If the company keeps \"the best 5–10 projects to operate\" (Stage 3) and flips "
             "the rest, the develop-and-flip business may be left the weaker projects. If you like the operating economics, ask to "
             "**co-invest in the assets they keep.**")
    L.append("")
    L.append("*Auto-generated by `src/stage_analysis.py` (run via `make report`). Returns are risk-adjusted levered "
             "equity IRRs; the operating model is a simplified levered DCF (FCF ≈ EBITDA, before tax / maintenance capex). "
             "All figures illustrative — verify revenue and capex before any decision.*")
    L.append("")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(L), encoding="utf-8")
    print(f"[stage_analysis] wrote {path}")


if __name__ == "__main__":
    c = compare()
    print("=" * 78)
    print("THREE-STAGE VALUE-CHAIN ANALYSIS — where to invest (per ~5 MW asset)")
    print("(illustrative, risk-adjusted levered equity returns — not investment advice)")
    print("=" * 78)
    hdr = f"{'Stage':<34}{'Hold':<10}{'Exp. IRR':>10}{'Exp. MOIC':>11}{'Downside IRR':>14}"
    print(hdr); print("-" * len(hdr))
    for r in c["rows"]:
        print(f"{r['stage']:<34}{r['hold']:<10}{_pct(r['expected_irr']):>10}"
              f"{r['expected_moic']:>10.2f}x{_pct(r['downside_irr']):>14}")
    print()
    st = c["stages"]
    print(f"Reference asset: {st.mw:.0f} MW / {st.mw*float(st.ref['duration_h']):.0f} MWh ({st.state})")
    print(f"  RTB value ${st.rtb_value:.1f}m · build ${st.build_cost:.1f}m · "
          f"operating EV ${operating_ev(st):.1f}m  (build margin ${operating_ev(st)-st.total_build:+.1f}m)")
    print("\nStage 3 by merchant scenario (IRR):")
    for n in ("low", "base", "high"):
        r = c["s3"]["by_scenario"][n]
        print(f"   {n:<6} merchant x{r['mult']:.2f}  ->  IRR {_pct(r['irr'])}  MOIC {r['moic']:.2f}x")
    print("\n(All figures illustrative; battery revenue/capex are uncertain — verify. Not investment advice.)")
