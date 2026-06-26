"""Refresh the Excel model's BLUE INPUT cells from the processed CSVs / engine.

This is the fallback to Power Query: it writes input VALUES into
the model's input cells only — it never touches a formula cell (any cell whose
value starts with '=' is skipped). Run after `make transform`:

    python -m src.refresh_model_inputs

If the model file does not exist yet, it is built first.
"""
from __future__ import annotations

from openpyxl import load_workbook

from src.utils import io
from src.valuation_engine import load_inputs
from src import build_model

MODEL = io.PROJECT_ROOT / "financial_models" / "BESS_Valuation.xlsx"

# label substring (on Inputs col A) -> attribute on the Inputs dataclass (col C)
SCALAR_MAP = {
    "Risk-free rate": "risk_free",
    "Development risk premium": "risk_premium",
    "Programme capital": "programme_capital",
    "Projects target": "projects_target",
    "Term": "term_years",
    "Development cost per project": "dev_cost_per_project",
    "Abandonment fraction": "abandonment_fraction",
    "Built-asset cost": "built_cost_per_mw",
    "Development approval": "da_independent",
    "Grid connection": "p_connection",
    "Reach sale": "p_sale",
    "Pre-money valuation": "pre_money",
    "Our investment": "investment_amount",
    "Option pool": "option_pool_pct",
    "Future-round dilution": "future_round_dilution_pct",
    "Liquidation preference": "liquidation_pref_x",
    "Platform exit multiple": "exit_equity_multiple",
    "Exit year": "exit_year",
    "VC target return": "vc_target_return",
}
DURATION_MAP = {"Development approval": "dur_da", "Grid connection": "dur_connection", "Reach sale": "dur_sale"}
STATES = ("NSW", "VIC", "SA")  # exact match on col A -> rtb_comps[state]


def _set_input(ws, row, col, value):
    """Write to an input cell only if it isn't a formula."""
    cell = ws.cell(row=row, column=col)
    if isinstance(cell.value, str) and cell.value.startswith("="):
        return False
    cell.value = value
    return True


def run() -> None:
    if not MODEL.exists():
        print("[refresh] model not found — building it first")
        build_model.build()

    inp = load_inputs()
    wb = load_workbook(MODEL)
    ws = wb["Inputs"]
    n_updated = 0

    for row in ws.iter_rows(min_col=1, max_col=1):
        cell = row[0]
        label = str(cell.value or "").strip()
        r = cell.row
        for key, attr in SCALAR_MAP.items():
            if label.startswith(key):
                if _set_input(ws, r, 3, getattr(inp, attr)):
                    n_updated += 1
                if key in DURATION_MAP:
                    _set_input(ws, r, 8, getattr(inp, DURATION_MAP[key]))
        if label in STATES:  # RTB $/MW by state
            if _set_input(ws, r, 3, float(inp.rtb_comps[label])):
                n_updated += 1
        if label.startswith("Capital call profile"):
            for j, v in enumerate(inp.call_profile[:4]):
                _set_input(ws, r, 3 + j, float(v))
            n_updated += 1
        if label.startswith("Distribution profile"):
            for j, v in enumerate(inp.dist_profile[:4]):
                _set_input(ws, r, 3 + j, float(v))
            n_updated += 1

    # Pipeline table: find header row "Project", write project rows beneath it.
    header_row = None
    for row in ws.iter_rows(min_col=1, max_col=1):
        if str(row[0].value or "").strip() == "Project":
            header_row = row[0].row
            break
    if header_row:
        for i, p in enumerate(inp.projects):
            r = header_row + 1 + i
            _set_input(ws, r, 1, p["name"])
            _set_input(ws, r, 2, p["state"])
            _set_input(ws, r, 3, p["location"])
            _set_input(ws, r, 4, p["mw"])
            _set_input(ws, r, 5, p["duration_h"])
            _set_input(ws, r, 7, p["years_to_sale"])
            n_updated += 1

    wb.calculation.fullCalcOnLoad = True
    wb.save(MODEL)
    print(f"[refresh] updated {n_updated} input cells in {MODEL.name} (formulas untouched)")
    print("          Open in Excel to recalculate (fullCalcOnLoad is set).")


if __name__ == "__main__":
    run()
