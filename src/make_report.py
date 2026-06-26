"""Generate figures + the one-page dashboard PDF from the valuation engine.

Outputs (committed portfolio artefacts):
    outputs/figures/survival_curve.png
    outputs/figures/irr_by_scenario.png
    outputs/figures/valuation_range.png
    outputs/figures/sensitivity_heatmap.png
    outputs/figures/tornado.png
    outputs/dashboard.pdf   (one-page IC summary)

DEAL: an ILLUSTRATIVE distribution-BESS develop-and-flip (RTB) fund, independently
rebuilt from the the manager's projections. All figures are ILLUSTRATIVE — the manager figures
are the manager's claims to verify. Not investment advice.
"""
from __future__ import annotations

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import numpy as np

from src.utils import io
from src import valuation_engine as ve
from src import stage_analysis as sa

FIG = io.PROJECT_ROOT / "outputs" / "figures"
OUT = io.PROJECT_ROOT / "outputs"
NAVY = "#1F3864"
ACCENT = "#2E75B6"
RED = "#C00000"
GREEN = "#548235"
SCEN = ["Conservative", "Base", "Ideal"]


def _style(ax, title):
    ax.set_title(title, fontsize=11, fontweight="bold", color=NAVY)
    ax.spines[["top", "right"]].set_visible(False)
    ax.grid(axis="y", alpha=0.3)


def fig_survival(s):
    sc = s["survival"]
    stages = ["Start", "Approval", "+Connection", "+Sale"]
    surv = [1.0, sc["after_approval"], sc["after_connection"], sc["flip_cumulative"]]
    fig, ax = plt.subplots(figsize=(6, 3.6))
    ax.step(range(len(stages)), surv, where="post", color=NAVY, lw=2.5, marker="o")
    for i, v in enumerate(surv):
        ax.annotate(f"{v:.0%}", (i, v), textcoords="offset points", xytext=(0, 8),
                    ha="center", fontsize=9, color=NAVY)
    da = s["da_base_manager"]
    ax.axhline(da, color=RED, ls="--", lw=1.3, label=f"manager headline {da:.0%} (approval gate ONLY)")
    flip = s["flip_base_manager"]
    ax.axhline(flip, color=GREEN, ls=":", lw=1.5, label=f"true flip success {flip:.0%} (all gates)")
    ax.set_xticks(range(len(stages)))
    ax.set_xticklabels(stages)
    ax.set_ylim(0, 1.08)
    ax.set_ylabel("P(project still alive)")
    ax.legend(fontsize=8)
    _style(ax, "Survival gates — flip success = approval × connection × sale")
    fig.tight_layout()
    fig.savefig(FIG / "survival_curve.png", dpi=150)
    plt.close(fig)


def fig_irr_by_scenario(s):
    rbs = s["returns_by_scenario"]
    vals = [rbs[n]["irr"] for n in SCEN]
    colors = [RED if v < 0 else ACCENT for v in vals]
    fig, ax = plt.subplots(figsize=(6, 3.6))
    bars = ax.bar(SCEN, vals, color=colors)
    ax.axhline(0, color="black", lw=0.8)
    exp = s["first_chicago"]["expected_irr"]
    ax.axhline(exp, color=NAVY, ls="--", lw=1.5, label=f"First-Chicago expected {exp:.1%}")
    for b, v in zip(bars, vals):
        ax.annotate(f"{v:.1%}", (b.get_x() + b.get_width() / 2, v),
                    textcoords="offset points", xytext=(0, 6 if v >= 0 else -14),
                    ha="center", fontsize=9, fontweight="bold")
    ax.set_ylabel("Equity IRR on our shares")
    ax.legend(fontsize=8)
    _style(ax, "Equity IRR on our shares, by scenario")
    fig.tight_layout()
    fig.savefig(FIG / "irr_by_scenario.png", dpi=150)
    plt.close(fig)


def fig_valuation_range(s):
    methods = s["valuation_range"]["methods"]
    labels = list(methods.keys())
    vals = list(methods.values())
    fig, ax = plt.subplots(figsize=(6.5, 3.6))
    y = range(len(labels))
    ax.barh(list(y), vals, color=ACCENT)
    for i, v in enumerate(vals):
        ax.annotate(f"${v:.2f}m", (v, i), textcoords="offset points", xytext=(5, 0),
                    va="center", fontsize=9)
    vr = s["valuation_range"]
    ax.axvline(vr["midpoint"], color=NAVY, ls="--", lw=1.5, label=f"Midpoint ${vr['midpoint']:.2f}m")
    ax.set_yticks(list(y))
    ax.set_yticklabels(labels, fontsize=8)
    ax.set_xlabel("Per-pipeline value today ($m, representative 6 projects)")
    ax.legend(fontsize=8)
    _style(ax, "Per-pipeline value cross-check (three methods)")
    ax.grid(axis="x", alpha=0.3)
    fig.tight_layout()
    fig.savefig(FIG / "valuation_range.png", dpi=150)
    plt.close(fig)


def fig_sensitivity(inp):
    sens = ve.sensitivity_two_way(inp)
    grid = np.array(sens["grid"]) * 100.0   # IRR %
    fig, ax = plt.subplots(figsize=(6, 3.8))
    im = ax.imshow(grid, cmap="RdYlGn", aspect="auto")
    ax.set_xticks(range(len(sens["price_mults"])))
    ax.set_xticklabels([f"{m:.2f}x" for m in sens["price_mults"]])
    ax.set_yticks(range(len(sens["da_rates"])))
    ax.set_yticklabels([f"{p:.0%}" for p in sens["da_rates"]])
    ax.set_xlabel("RTB price multiplier")
    ax.set_ylabel("Development-approval rate (DA gate)")
    for i in range(grid.shape[0]):
        for j in range(grid.shape[1]):
            ax.text(j, i, f"{grid[i, j]:.0f}", ha="center", va="center", fontsize=8)
    _style(ax, "Investor IRR (%): development approval × RTB price")
    ax.grid(False)
    fig.colorbar(im, ax=ax, shrink=0.8, label="IRR %")
    fig.tight_layout()
    fig.savefig(FIG / "sensitivity_heatmap.png", dpi=150)
    plt.close(fig)


def fig_tornado(inp):
    tor = ve.tornado(inp)
    base = tor[0]["base"]
    labels = [t["driver"] for t in tor][::-1]
    lows = [(t["low"] - base) * 100 for t in tor][::-1]
    highs = [(t["high"] - base) * 100 for t in tor][::-1]
    fig, ax = plt.subplots(figsize=(6.5, 3.6))
    y = range(len(labels))
    ax.barh(list(y), lows, color=RED, label="Low")
    ax.barh(list(y), highs, color=GREEN, label="High")
    ax.axvline(0, color="black", lw=0.8)
    ax.set_yticks(list(y))
    ax.set_yticklabels(labels, fontsize=8)
    ax.set_xlabel(f"Investor IRR change vs Base ({base:.1%}), percentage points")
    ax.legend(fontsize=8)
    _style(ax, "Tornado — investor IRR sensitivity to key drivers")
    ax.grid(axis="x", alpha=0.3)
    fig.tight_layout()
    fig.savefig(FIG / "tornado.png", dpi=150)
    plt.close(fig)


def fig_stage_comparison(c):
    """Expected vs downside investor IRR for the value-chain stages."""
    rows = c["rows"]

    def _short(stage):                       # "Stage 1 — Develop & flip (RTB)" -> "Stage 1\nDevelop & flip"
        num, _, rest = stage.partition("—")
        name = rest.split("(")[0].strip()
        return f"{num.strip()}\n{name}"

    labels = [_short(r["stage"]) for r in rows]
    exp = [r["expected_irr"] * 100 for r in rows]
    down = [(0 if r["downside_irr"] != r["downside_irr"] else r["downside_irr"]) * 100 for r in rows]
    x = np.arange(len(labels))
    w = 0.38
    fig, ax = plt.subplots(figsize=(7.5, 3.9))
    b1 = ax.bar(x - w / 2, exp, w, color=ACCENT, label="Expected IRR")
    b2 = ax.bar(x + w / 2, down, w, color=[RED if d < 0 else GREEN for d in down], label="Downside IRR")
    ax.axhline(0, color="black", lw=0.8)
    for bars in (b1, b2):
        for b in bars:
            v = b.get_height()
            ax.annotate(f"{v:.0f}%", (b.get_x() + b.get_width() / 2, v),
                        textcoords="offset points", xytext=(0, 5 if v >= 0 else -12),
                        ha="center", fontsize=8, fontweight="bold")
    ax.set_xticks(x)
    ax.set_xticklabels(labels, fontsize=8)
    ax.set_ylabel("Investor IRR (levered, %)")
    ax.legend(fontsize=8)
    _style(ax, "Risk–return by stage: expected vs downside IRR")
    fig.tight_layout()
    fig.savefig(FIG / "stage_comparison.png", dpi=150)
    plt.close(fig)


def fig_buyer_sizes():
    """Recent BESS deals are large — visualises the 5 MW vs 100 MW+ buyer gap."""
    import csv as _csv
    path = io.DATA_PROCESSED / "deal_sizes.csv"
    rows = []
    with open(path, newline="", encoding="utf-8") as fh:
        for r in _csv.reader(fh):
            if r and not r[0].startswith("#") and r[0] != "project":
                try:
                    rows.append((r[0], float(r[2])))
                except (IndexError, ValueError):
                    pass
    rows.sort(key=lambda x: x[1])
    labels = [p.replace("THIS FUND's project (reference)", "THIS FUND (5 MW)") for p, _ in rows]
    mws = [m for _, m in rows]
    colors = [RED if m <= 5 else ACCENT for m in mws]
    fig, ax = plt.subplots(figsize=(7, 4))
    bars = ax.barh(labels, mws, color=colors)
    for b, m in zip(bars, mws):
        ax.annotate(f"{m:.0f} MW", (m, b.get_y() + b.get_height() / 2),
                    textcoords="offset points", xytext=(4, 0), va="center", fontsize=8)
    ax.set_xlabel("Project / deal size (MW)")
    _style(ax, "Recent Australian BESS deals are large — 5 MW is a different market")
    ax.grid(axis="x", alpha=0.3)
    fig.tight_layout()
    fig.savefig(FIG / "buyer_sizes.png", dpi=150)
    plt.close(fig)


def dashboard_pdf(s):
    inp = s["inputs"]
    fc = s["first_chicago"]
    rbs = s["returns_by_scenario"]
    sc = s["survival"]
    with PdfPages(OUT / "dashboard.pdf") as pdf:
        fig = plt.figure(figsize=(11.69, 8.27))  # A4 landscape
        ct = s["cap_table"]
        fig.suptitle("Illustrative Battery-Developer Startup — Direct-Equity Dashboard",
                     fontsize=16, fontweight="bold", color=NAVY, y=0.97)
        fig.text(0.5, 0.93, "We buy shares in one ~5 MW distribution-BESS develop-and-flip startup (NSW/VIC/SA) • ILLUSTRATIVE • "
                 "founder figures are claims; equity-deal terms are placeholders • Not investment advice", ha="center", fontsize=9, color=RED, style="italic")

        fig.text(0.06, 0.86, "EXPECTED RETURN ON OUR SHARES (First-Chicago)", fontsize=11, fontweight="bold", color=NAVY)
        fig.text(0.06, 0.82, f"IRR {fc['expected_irr']:.1%}   MOIC {fc['expected_moic']:.2f}x", fontsize=18, fontweight="bold", color=NAVY)
        fig.text(0.06, 0.785, f"Scenario IRR range  {fc['min_irr']:.0%}  to  {fc['max_irr']:.0%}", fontsize=10, color=ACCENT)

        fig.text(0.40, 0.86, "SURVIVAL (the key flag)", fontsize=11, fontweight="bold", color=NAVY)
        fig.text(0.40, 0.82, f"True flip {s['flip_base_manager']:.0%}  vs  founder headline DA {s['da_base_manager']:.0%}", fontsize=13, fontweight="bold", color=RED)
        fig.text(0.40, 0.785, "The 65% is the approval gate ALONE — true flip = DA × connection × sale", fontsize=9, color="black")

        fig.text(0.70, 0.86, "OUR STAKE & KEY TERMS (placeholders)", fontsize=11, fontweight="bold", color=NAVY)
        ktxt = (f"${ct['investment']:.0f}m into ${ct['pre_money']:.0f}m pre-money -> {ct['ownership_initial']:.0%} "
                f"({ct['ownership_diluted']:.0%} diluted)\n"
                f"1x liq. preference; exit yr {inp.exit_year:.0f}; exit = fwd-pipeline rNPV (depth {inp.pipeline_depth_at_exit:.0f})\n"
                f"Conservative IRR {rbs['Conservative']['irr']:.0%} (total loss possible)")
        fig.text(0.70, 0.75, ktxt, fontsize=9, color="black", va="top")

        for name, pos in [("survival_curve.png", [0.06, 0.40, 0.40, 0.30]),
                          ("irr_by_scenario.png", [0.55, 0.40, 0.40, 0.30]),
                          ("valuation_range.png", [0.06, 0.06, 0.40, 0.30]),
                          ("tornado.png", [0.55, 0.06, 0.40, 0.30])]:
            img = plt.imread(FIG / name)
            ax = fig.add_axes(pos)
            ax.imshow(img)
            ax.axis("off")
        pdf.savefig(fig)
        plt.close(fig)


def run() -> None:
    FIG.mkdir(parents=True, exist_ok=True)
    s = ve.summary()
    inp = s["inputs"]
    fig_survival(s)
    fig_irr_by_scenario(s)
    fig_valuation_range(s)
    fig_sensitivity(inp)
    fig_tornado(inp)
    fig_stage_comparison(sa.compare())
    fig_buyer_sizes()
    dashboard_pdf(s)
    sa.write_markdown()
    print(f"[make_report] wrote 7 figures to {FIG}, dashboard.pdf to {OUT}, and STAGE_COMPARISON.md")


if __name__ == "__main__":
    run()
