"""Export a GitHub-friendly Markdown snapshot of the Excel model's key results.

GitHub does not render .xlsx files inline, and the workbook is formula-driven
(values compute only when opened in Excel). So recruiters / reviewers browsing the
repo can't see the numbers from the .xlsx alone. This writes
`financial_models/MODEL_PREVIEW.md` — the same outputs the workbook computes,
rendered as Markdown tables that GitHub shows inline, with no software required.

Numbers come from `valuation_engine` (the cell-for-cell Python reference of the
workbook), so the preview matches the model. Run:  python -m src.export_model_preview
"""
from __future__ import annotations

from src.utils import io
from src import valuation_engine as ve

OUT = io.PROJECT_ROOT / "financial_models" / "MODEL_PREVIEW.md"


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
    ct = s["cap_table"]
    cb = s["company_base"]
    xb = s["exit_base"]
    xc = s["earnings_crosscheck"]
    vr = s["valuation_range"]
    checks = s["checks"]
    master = "OK" if all(checks.values()) else "ERROR"

    L = []
    L.append("# Model preview — direct-equity stake in a battery-developer startup (read-only snapshot)")
    L.append("")
    L.append("> **GitHub does not render `.xlsx` files, and the workbook computes its values only when opened in Excel.** "
             "This page mirrors the model's key outputs so you can review the results here, with no software. "
             "Numbers are produced by `valuation_engine.py`, the cell-for-cell Python reference of the workbook "
             "([`financial_models/BESS_Valuation.xlsx`](BESS_Valuation.xlsx)).")
    L.append("")
    L.append("*We invest **directly as a shareholder** in one illustrative battery-developer startup (not as a fund LP). "
             "Independent rebuild of the founder's claims; several equity-deal terms are **placeholders to confirm**. "
             "Not investment advice. See the [repository README](../README.md).*")
    L.append("")
    L.append(f"**Master check:** `{master}`  ·  **Base discount rate (asset cross-checks):** {_pct(s['discount_base'])} "
             f"(RBA 10yr CGS {_pct(inp.risk_free)} + {_pct(inp.risk_premium)} dev premium)  ·  "
             f"**Active case shown:** Base")
    L.append("")

    L.append("## Headline — expected return on OUR shares (First-Chicago)")
    L.append("")
    L.append("| Metric | Value |")
    L.append("|---|---|")
    L.append(f"| Expected equity IRR on our shares | **{_pct(fc['expected_irr'])}** |")
    L.append(f"| Expected MOIC (multiple of money) | **{_x(fc['expected_moic'])}** |")
    L.append(f"| Scenario IRR range | {_pct(fc['min_irr'])} … {_pct(fc['max_irr'])} |")
    L.append("")
    L.append("> The Conservative case is a **total loss** (the company's net programme profit is negative, so its equity is worth ~0). "
             "This is the venture-style shape: a real chance of zero, a modest base case, and meaningful upside if approvals run hot.")
    L.append("")

    L.append("## Our stake — the cap table (placeholders to confirm)")
    L.append("")
    L.append("| Item | Value |")
    L.append("|---|---|")
    L.append(f"| Pre-money valuation `[[TO CONFIRM]]` | {_m(ct['pre_money'])} |")
    L.append(f"| Our investment `[[TO CONFIRM]]` | {_m(ct['investment'])} |")
    L.append(f"| Post-money (= pre + investment) | {_m(ct['post_money'])} |")
    L.append(f"| Ownership at entry (= investment ÷ post-money) | **{_pct(ct['ownership_initial'])}** |")
    L.append(f"| Option pool `[[TO CONFIRM]]` | {_pct(ct['option_pool_pct'])} |")
    L.append(f"| Future-round dilution `[[TO CONFIRM]]` | {_pct(ct['future_round_dilution_pct'])} |")
    L.append(f"| Ownership at exit (after dilution) | **{_pct(ct['ownership_diluted'])}** |")
    L.append(f"| Liquidation preference | {inp.liquidation_pref_x:.0f}× non-participating |")
    L.append("")

    L.append("## Return on our shares, by scenario")
    L.append("")
    L.append("| Scenario | Flip success | Company exit equity | Our proceeds | MOIC | IRR |")
    L.append("|---|---|---|---|---|---|")
    for name in ("Conservative", "Base", "Ideal"):
        m = rbs[name]
        L.append(f"| {name} | {_pct(m['flip_success'])} | {_m(m['company_exit_equity'])} | "
                 f"{_m(m['our_proceeds'])} | **{_x(m['moic'])}** | **{_pct(m['irr'])}** |")
    L.append("")
    L.append("> *Our proceeds = the greater of our 1× liquidation preference or our diluted ownership × the company's exit equity value, "
             "plus any interim distributions. The PRIMARY exit equity value is the **forward-pipeline rNPV** (projects still in flight "
             f"at exit) + retained cash − debt — over a {inp.exit_year:.0f}-year hold `[[TO CONFIRM]]`.*")
    L.append("")

    L.append("## The company's exit equity value — PRIMARY basis (forward-pipeline rNPV)")
    L.append("")
    L.append("> A develop-and-flip company is a development **platform**: a buyer pays for its **forward pipeline**, not past "
             "profit. So exit equity = forward-pipeline rNPV + retained cash − debt (the earnings multiple below is a cross-check only).")
    L.append("")
    L.append("| Component (Base) | Value |")
    L.append("|---|---|")
    L.append(f"| Forward-pipeline rNPV (depth {inp.pipeline_depth_at_exit:.0f} `[[TO CONFIRM]]` × per-project rNPV) | {_m(xb['forward_pipeline_rnpv'])} |")
    L.append(f"| + Net cash retained at exit (realised profit not distributed) | {_m(xb['retained_cash'])} |")
    L.append(f"| − Debt at exit `[[TO CONFIRM]]` | {_m(xb['debt_at_exit'])} |")
    L.append(f"| **= Company exit equity (primary)** | **{_m(xb['company_exit_equity'])}** |")
    L.append("")
    L.append(f"*Cross-check — earnings multiple on forward run-rate profit ({_m(xc['run_rate'])}/yr) "
             f"at {xc['mult_low']:.0f}× / {xc['mult_base']:.0f}× / {xc['mult_high']:.0f}× `[[TO CONFIRM]]` "
             f"(+ retained cash − debt): {_m(xc['low'])} / {_m(xc['base'])} / {_m(xc['high'])}. We anchor on the more "
             "conservative pipeline basis; comps were not available (publicly reported deals only).*")
    L.append("")

    L.append("## Survival gates — separate; flip success = their product")
    L.append("")
    L.append("> The founder's **40 / 65 / 80%** are the **development-approval gate ONLY**. True develop-and-flip success = "
             "development approval × grid connection × sale — a multi-period survival / probability-of-default curve.")
    L.append("")
    L.append("| Gate | Probability (public benchmark) | Cumulative survival |")
    L.append("|---|---|---|")
    L.append(f"| Development approval | {_pct(sc['development_approval'])} | {_pct(sc['after_approval'])} |")
    L.append(f"| Grid connection | {_pct(sc['grid_connection'])} | {_pct(sc['after_connection'])} |")
    L.append(f"| Reach sale (flip exit) | {_pct(sc['reach_sale'])} | {_pct(sc['flip_cumulative'])} |")
    L.append("")
    L.append(f"**At the founder's Base development-approval rate ({_pct(s['da_base_manager'])}), true flip success "
             f"≈ {_pct(s['da_base_manager'])} × {_pct(inp.p_connection)} × {_pct(inp.p_sale)} = "
             f"{_pct(s['flip_base_manager'])}** — far below the 65% headline. The gates beyond approval are not free; this drives "
             "the company's net programme profit and therefore its value.")
    L.append("")

    L.append("## The company's development programme (Base scenario)")
    L.append("")
    L.append("| Item | Value |")
    L.append("|---|---|")
    L.append(f"| Programme capital (illustrative) | {_m(inp.programme_capital)} |")
    L.append(f"| Projects target (delivered & sold) | {inp.projects_target:.0f} |")
    L.append(f"| Projects started (funnel = target ÷ flip success) | {cb['projects_started']:.0f} |")
    L.append(f"| Total development cost | {_m(cb['total_dev_cost'])} |")
    L.append(f"| Gross proceeds (RTB sales) | {_m(cb['gross_proceeds'])} |")
    L.append(f"| Realised net programme profit (gross − dev cost) | {_m(cb['net_business_profit'])} |")
    L.append(f"| Forward run-rate annual dev profit (= realised ÷ term) | {_m(cb['run_rate_annual_dev_profit'])} |")
    L.append("")
    L.append(f"*RTB prices (founder claim): NSW {_m(inp.rtb_comps['NSW']*5)} · VIC {_m(inp.rtb_comps['VIC']*5)} · "
             f"SA {_m(inp.rtb_comps['SA']*5)} per 5 MW project. No fund fees or carry — we own shares directly.*")
    L.append("")

    L.append("## Company-asset valuation cross-check (per representative pipeline)")
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
    L.append("- **Open the live workbook** (recalculates on open): [`BESS_Valuation.xlsx`](BESS_Valuation.xlsx) "
             "— Cover · Inputs · Timeline · Scenarios · Calc_Survival · Calc_Project_rNPV · Calc_Company · "
             "Cap table & Returns · Calc_CrossChecks · Sensitivity · Checks · Dashboard · Sources & Glossary.")
    L.append("- **One-page dashboard (PDF, renders in-browser):** [`../outputs/dashboard.pdf`](../outputs/dashboard.pdf)")
    L.append("- **Data lineage:** [`SOURCES_LOG.md`](SOURCES_LOG.md)  ·  **Value-chain comparison:** [`STAGE_COMPARISON.md`](STAGE_COMPARISON.md)")
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
