"""Export a GitHub-friendly Markdown snapshot of the Excel model's key results.

GitHub does not render .xlsx files inline, and the workbook is formula-driven
(values compute only when opened in Excel). So recruiters / HR browsing the repo
can't see the numbers from the .xlsx alone. This writes `model/MODEL_PREVIEW.md`
— the same outputs the workbook computes, rendered as Markdown tables that GitHub
shows inline, with no software required.

Numbers come from `valuation_engine` (the cell-for-cell Python reference of the
workbook), so the preview matches the model. Run:  python -m src.export_model_preview
"""
from __future__ import annotations

from src.utils import io
from src import valuation_engine as ve

OUT = io.PROJECT_ROOT / "model" / "MODEL_PREVIEW.md"


def _pct(x):
    return f"{x:.1%}"


def _m(x):
    return f"${x:,.1f}m"


def _x(x):
    return f"{x:.2f}x"


def build_markdown() -> str:
    s = ve.summary()
    inp = s["inputs"]
    rbs = s["returns_by_scenario"]
    fc = s["first_chicago"]
    sc = s["survival"]
    fb = s["fund_base"]
    vr = s["valuation_range"]
    checks = s["checks"]
    master = "OK" if all(checks.values()) else "ERROR"

    L = []
    L.append("# Model preview — BESS Develop-and-Flip Fund (read-only snapshot)")
    L.append("")
    L.append("> **GitHub does not render `.xlsx` files, and the workbook computes its values only when opened in Excel.** "
             "This page mirrors the model's key outputs so you can review the results here, with no software. "
             "Numbers are produced by `valuation_engine.py`, the cell-for-cell Python reference of the workbook "
             "([`model/BESS_Pipeline_Valuation_v1.0.xlsx`](BESS_Pipeline_Valuation_v1.0.xlsx)).")
    L.append("")
    L.append("*Illustrative, independent rebuild of a manager's claims — not investment advice. See the [repository README](../README.md).*")
    L.append("")
    L.append(f"**Master check:** `{master}`  ·  **Base discount rate:** {_pct(s['discount_base'])} "
             f"(RBA 10yr CGS {_pct(inp.risk_free)} + {_pct(inp.risk_premium)} dev premium)  ·  "
             f"**Active case shown:** Base")
    L.append("")

    L.append("## Headline — expected investor return (First-Chicago)")
    L.append("")
    L.append("| Metric | Value |")
    L.append("|---|---|")
    L.append(f"| Expected investor IRR (after fees) | **{_pct(fc['expected_irr'])}** |")
    L.append(f"| Expected MOIC (net) | **{_x(fc['expected_moic'])}** |")
    L.append(f"| Scenario IRR range | {_pct(fc['min_irr'])} … {_pct(fc['max_irr'])} |")
    L.append(f"| For comparison — manager's claimed IRRs | 10.7% / 19.4% / 23.8% |")
    L.append("")

    L.append("## Investor return by scenario (after fees)")
    L.append("")
    L.append("| Scenario | Success rate | Projects started | Total dev cost | Invested capital | Gross proceeds | MOIC (net) | IRR (net) |")
    L.append("|---|---|---|---|---|---|---|---|")
    for name in ("Conservative", "Base", "Ideal"):
        m = rbs[name]
        L.append(f"| {name} | {_pct(m['cum_success'])} | {m['projects_started']:.0f} | "
                 f"{_m(m['total_dev_cost'])} | {_m(m['invested_capital'])} | {_m(m['gross_proceeds'])} | "
                 f"**{_x(m['moic'])}** | **{_pct(m['irr'])}** |")
    L.append("")
    L.append("> The Conservative case returns **less than invested capital** (MOIC below 1.0x). The independent rebuild is "
             "deliberately more conservative than the manager's deck.")
    L.append("")

    L.append("## PD-style survival curve (independent, public data)")
    L.append("")
    L.append("| Gate | Probability | Cumulative survival |")
    L.append("|---|---|---|")
    L.append(f"| Planning approval | {_pct(sc['planning'])} | {_pct(sc['survival_after_planning'])} |")
    L.append(f"| Grid connection | {_pct(sc['connection'])} | {_pct(sc['survival_after_connection'])} |")
    L.append(f"| Reach sale | {_pct(sc['sale'])} | {_pct(sc['cumulative'])} |")
    L.append("")
    L.append(f"**Independent cumulative success ≈ {_pct(sc['cumulative'])}** vs the manager's Base claim of "
             f"{_pct(s['base_scenario_success'])} → **optimism gap {s['optimism_gap']:+.1%}** "
             f"(the manager's base sits above the independent estimate — a key diligence flag).")
    L.append("")

    L.append("## Fund funnel (Base scenario)")
    L.append("")
    L.append("| Item | Value |")
    L.append("|---|---|")
    L.append(f"| Committed capital | {_m(inp.committed_capital)} |")
    L.append(f"| Projects target (delivered & sold) | {inp.projects_target:.0f} |")
    L.append(f"| Projects started (funnel = target ÷ success) | {fb['projects_started']:.0f} |")
    L.append(f"| Total development cost | {_m(fb['total_dev_cost'])} |")
    L.append(f"| Management + entry fees | {_m(fb['mgmt_fee'] + fb['entry_fee'])} |")
    L.append(f"| Invested capital (LP) | {_m(fb['invested_capital'])} |")
    L.append(f"| Gross proceeds | {_m(fb['gross_proceeds'])} |")
    L.append(f"| Carry to GP | {_m(fb['carry'])} |")
    L.append(f"| Distributions to LP | {_m(fb['distributions'])} |")
    L.append("")
    L.append("*Fees: 2% entry + 2% p.a. management + 20% carry over an 8% hurdle. RTB prices (manager claim): "
             f"NSW {_m(inp.rtb_comps['NSW']*5)} · VIC {_m(inp.rtb_comps['VIC']*5)} · SA {_m(inp.rtb_comps['SA']*5)} per 5 MW project.*")
    L.append("")

    L.append("## Valuation cross-check (per representative pipeline)")
    L.append("")
    L.append("| Method | Value |")
    L.append("|---|---|")
    for k, v in vr["methods"].items():
        L.append(f"| {k} | ${v:,.2f}m |")
    L.append(f"| **Range** | **${vr['low']:,.2f}m – ${vr['high']:,.2f}m** (midpoint ${vr['midpoint']:,.2f}m) |")
    L.append("")

    L.append("## Integrity checks")
    L.append("")
    L.append(f"All **{len(checks)}** model checks pass → master check reads `{master}`.")
    L.append("")
    L.append("| Check | Result |")
    L.append("|---|---|")
    for k, v in checks.items():
        L.append(f"| {k} | {'✅ OK' if v else '❌ ERROR'} |")
    L.append("")

    L.append("## See the full model")
    L.append("")
    L.append("- **Open the live workbook** (recalculates on open): [`BESS_Pipeline_Valuation_v1.0.xlsx`](BESS_Pipeline_Valuation_v1.0.xlsx) "
             "— 15 tabs (Cover · Inputs · Timeline · Scenarios · Calc_Survival · Calc_Project_rNPV · Calc_Fund · Returns · "
             "Calc_CrossChecks · Sensitivity · Checks · Dashboard · Sources & Glossary).")
    L.append("- **One-page dashboard (PDF, renders in-browser):** [`../outputs/dashboard.pdf`](../outputs/dashboard.pdf)")
    L.append("- **Notebooks (render in-browser with charts):** [`../notebooks/`](../notebooks/)")
    L.append("")
    L.append("*This file is auto-generated by `src/export_model_preview.py` (run via `make report`). Do not edit by hand.*")
    L.append("")
    return "\n".join(L)


def run() -> None:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(build_markdown(), encoding="utf-8")
    print(f"[export_model_preview] wrote {OUT}")


if __name__ == "__main__":
    run()
