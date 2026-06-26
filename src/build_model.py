"""Build the formula-driven Excel valuation model from scratch.

Produces financial_models/BESS_Valuation.xlsx following the FAST/ICAEW/
Macabacus/Operis house rules: Inputs -> Calcs -> Outputs zones, one master
Timeline, a single CHOOSE scenario switch (3 cases) with a live-case row,
one-row-one-calculation, colour coding (blue input / black formula / green
cross-sheet link), and a Checks framework with a master check on the Cover.

DEAL: an ILLUSTRATIVE distribution-network BESS *develop-and-flip* fund (framed
on the an illustrative develop-and-flip battery storage fund — manager claims independently rebuilt). The
fund develops ~5 MW distribution batteries to shovel-ready (RTB / development
rights) and SELLS them before construction: merchant risk passes to the buyer;
the fund's risk is the SURVIVAL CURVE and the RTB EXIT PRICE.

The model is fully LIVE (formula strings) so it recalculates when opened in Excel.
Blue input cells are seeded from the same inputs the Python valuation engine uses,
so the workbook reproduces the engine's numbers (incl. closed-form investor IRR).

Run:  python -m src.build_model
"""
from __future__ import annotations

from openpyxl import Workbook
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter
from openpyxl.formatting.rule import CellIsRule

from src.utils import io
from src.valuation_engine import load_inputs

# ---------------------------------------------------------------------------
# Sheet names (15 tabs)
# ---------------------------------------------------------------------------
COV, CON, CL, INP, TL, SCN = "Cover", "Contents", "Change Log", "Inputs", "Timeline", "Scenarios"
SURV, RNPV, FUND, RET = "Calc_Survival", "Calc_Project_rNPV", "Calc_Fund", "Returns"
CC, SENS, CHK, DSH, SG = "Calc_CrossChecks", "Sensitivity", "Checks", "Dashboard", "Sources & Glossary"
ORDER = [COV, CON, CL, INP, TL, SCN, SURV, RNPV, FUND, RET, CC, SENS, CHK, DSH, SG]
TABCOLOR = {COV: "000000", CON: "808080", CL: "808080", INP: "0070C0", TL: "00B0F0",
            SCN: "7030A0", SURV: "FFFFFF", RNPV: "FFFFFF", FUND: "FFFFFF", RET: "92D050",
            CC: "FFFFFF", SENS: "FFFF00", CHK: "FF0000", DSH: "00B050", SG: "808080"}

# ---------------------------------------------------------------------------
# Styles
# ---------------------------------------------------------------------------
BLUE, BLACK, GREEN, RED, GREY = "0000FF", "000000", "008000", "FF0000", "595959"
F_INPUT = Font(name="Arial", size=10, color=BLUE)
F_FORM = Font(name="Arial", size=10, color=BLACK)
F_LINK = Font(name="Arial", size=10, color=GREEN)
F_LABEL = Font(name="Arial", size=10, color=BLACK)
F_TITLE = Font(name="Arial", size=14, bold=True, color="1F3864")
F_HEAD = Font(name="Arial", size=10, bold=True, color="FFFFFF")
F_SECT = Font(name="Arial", size=10, bold=True, color="1F3864")
F_NOTE = Font(name="Arial", size=9, italic=True, color=GREY)
F_DISC = Font(name="Arial", size=9, italic=True, color=RED)
FILL_HEAD = PatternFill("solid", fgColor="1F3864")
FILL_SECT = PatternFill("solid", fgColor="D9E1F2")
FILL_YEL = PatternFill("solid", fgColor="FFF2CC")
FILL_GREEN = PatternFill("solid", fgColor="C6EFCE")
FILL_RED = PatternFill("solid", fgColor="FFC7CE")
THIN = Side(style="thin", color="BFBFBF")
BORDER = Border(left=THIN, right=THIN, top=THIN, bottom=THIN)

FM = '$#,##0.0;($#,##0.0);"–"'        # $m, 1dp
FM2 = '$#,##0.00;($#,##0.00);"–"'     # $m, 2dp
FMW = '$#,##0.000'                    # $m per MW
FPCT = '0.0%'
FX = '0.00"x"'
FNUM = '#,##0'
FNUM1 = '#,##0.0'
FFAC = '0.000'
FMULT = '0.00'


# ---------------------------------------------------------------------------
# Builder helpers
# ---------------------------------------------------------------------------
class B:
    def __init__(self):
        self.wb = Workbook()
        self.wb.calculation.fullCalcOnLoad = True
        self.wb.remove(self.wb.active)
        self.ws = {name: self.wb.create_sheet(name) for name in ORDER}
        for name, ws in self.ws.items():
            ws.sheet_properties.tabColor = TABCOLOR[name]
            ws.sheet_view.showGridLines = False

    def put(self, sheet, r, c, value, kind="label", fmt=None, fill=None,
            bold=False, align=None, wrap=False, border=False):
        if kind not in ("formula", "link") and isinstance(value, str) and value.startswith("="):
            value = value[1:].lstrip()
        cell = self.ws[sheet].cell(row=r, column=c, value=value)
        font = {"input": F_INPUT, "formula": F_FORM, "link": F_LINK,
                "label": F_LABEL, "title": F_TITLE, "head": F_HEAD,
                "sect": F_SECT, "note": F_NOTE, "disc": F_DISC}[kind]
        if bold and kind in ("label", "formula", "link"):
            font = Font(name="Arial", size=10, bold=True, color=font.color.rgb)
        cell.font = font
        if fmt:
            cell.number_format = fmt
        if kind == "input" and fill is None:
            fill = "yel"
        if fill == "head":
            cell.fill = FILL_HEAD
        elif fill == "sect":
            cell.fill = FILL_SECT
        elif fill == "yel":
            cell.fill = FILL_YEL
        elif fill:
            cell.fill = PatternFill("solid", fgColor=fill)
        if align:
            cell.alignment = Alignment(horizontal=align, wrap_text=wrap, vertical="top")
        elif wrap:
            cell.alignment = Alignment(wrap_text=True, vertical="top")
        if border:
            cell.border = BORDER
        return cell

    def ref(self, sheet, col, row):
        return f"'{sheet}'!${get_column_letter(col)}${row}"

    def rng(self, sheet, c1, r1, c2, r2):
        return f"'{sheet}'!${get_column_letter(c1)}${r1}:${get_column_letter(c2)}${r2}"

    def width(self, sheet, widths):
        for col, w in widths.items():
            self.ws[sheet].column_dimensions[col].width = w

    def header(self, sheet, r, labels, start=1):
        for i, lab in enumerate(labels):
            self.put(sheet, r, start + i, lab, "head", fill="head",
                     align="center", wrap=True, border=True)


def build():
    b = B()
    inp = load_inputs()
    n = len(inp.projects)
    a = io.load_assumptions()
    R = {}

    # =====================================================================
    # INPUTS
    # =====================================================================
    b.width(INP, {"A": 36, "B": 10, "C": 14, "D": 13, "E": 50, "F": 12, "G": 12, "H": 12})
    b.put(INP, 1, 1, "INPUTS — all model assumptions (blue = input cell)", "title")
    b.put(INP, 2, 1, "ILLUSTRATIVE develop-and-flip RTB fund. the manager figures are the manager's CLAIMS — verify. Every input traces to a source.", "note", wrap=True)
    b.header(INP, 3, ["Assumption", "", "Value", "Unit", "Source", "As at", "Status", "Duration (yrs)"])

    def srow(r, label, value, key, fmt, unit, src_key=None, status="BENCHMARK", dur=None):
        b.put(INP, r, 1, label, "label")
        b.put(INP, r, 3, value, "input", fmt=fmt, border=True)
        b.put(INP, r, 4, unit, "label")
        src = inp.sources.get(src_key) if src_key else None
        b.put(INP, r, 5, src[0] if src else "Illustrative / the manager claim (see config)", "note", wrap=True)
        b.put(INP, r, 6, src[1] if src else a["meta"]["as_at"], "note", align="center")
        b.put(INP, r, 7, src[2] if src else status, "note", align="center")
        if dur is not None:
            b.put(INP, r, 8, dur, "input", fmt=FNUM1, border=True)
        if key:
            R[key] = b.ref(INP, 3, r)

    b.put(INP, 4, 1, "Discount rate (rNPV / cross-checks)", "sect", fill="sect")
    srow(5, "Risk-free rate (RBA 10yr CGS)", inp.risk_free, "risk_free", FPCT, "decimal", "risk_free")
    srow(6, "Development risk premium", inp.risk_premium, "risk_premium", FPCT, "decimal")
    b.put(INP, 7, 1, "Base discount rate", "label", bold=True)
    b.put(INP, 7, 3, f"={R['risk_free']}+{R['risk_premium']}", "formula", fmt=FPCT, border=True, bold=True)
    b.put(INP, 7, 4, "decimal", "label")
    R["discount_base"] = b.ref(INP, 3, 7)

    b.put(INP, 8, 1, "Fund structure & fees (the manager claim — verify in IM)", "sect", fill="sect")
    srow(9, "Committed capital", inp.committed_capital, "committed", FM, "$m")
    srow(10, "Projects target (delivered & sold)", inp.projects_target, "target", FNUM, "count")
    srow(11, "Term", inp.term_years, "term", FNUM, "years")
    srow(12, "Entry fee (% of committed)", inp.entry_fee_pct, "entry_pct", FPCT, "decimal")
    srow(13, "Management fee (% p.a.)", inp.mgmt_fee_pct_pa, "mgmt_pct", FPCT, "decimal")
    srow(14, "Carried interest (%)", inp.carry_pct, "carry_pct", FPCT, "decimal")
    srow(15, "Hurdle / preferred return (%)", inp.hurdle_pct, "hurdle_pct", FPCT, "decimal")

    b.put(INP, 16, 1, "Development cost & funnel attrition", "sect", fill="sect")
    srow(17, "Development cost per project", inp.dev_cost_per_project, "dev_cost", FM2, "$m/project", "dev")
    srow(18, "Abandonment fraction (failed projects)", inp.abandonment_fraction, "abandon", FPCT, "decimal")

    b.put(INP, 19, 1, "Build cost CONTEXT (buyer-funded — NOT in margin)", "sect", fill="sect")
    srow(20, "Built-asset cost (context)", inp.built_cost_per_mw, "built_cost", FMW, "$m/MW", "build")

    b.put(INP, 21, 1, "Survival gates — SEPARATE; scenarios move ONLY development approval", "sect", fill="sect")
    srow(22, "Development approval — public benchmark", inp.da_independent, "da_ind", FPCT, "prob", "da", dur=inp.dur_da)
    srow(23, "Grid connection (separate gate)", inp.p_connection, "p_conn", FPCT, "prob", "connection", dur=inp.dur_connection)
    srow(24, "Reach sale — flip exit (separate gate)", inp.p_sale, "p_sale", FPCT, "prob", "sale", dur=inp.dur_sale)

    b.put(INP, 25, 1, "RTB exit price — $/MW by state (the manager claim — verify)", "sect", fill="sect")
    for i, st in enumerate(["NSW", "VIC", "SA"]):
        srow(26 + i, st, float(inp.rtb_comps.get(st, 0.0)), f"rtb_{st}", FMW, "$m/MW", "rtb")
    R["rtb_states"] = b.rng(INP, 1, 26, 1, 28)
    R["rtb_prices"] = b.rng(INP, 3, 26, 3, 28)

    b.put(INP, 29, 1, "VC method", "sect", fill="sect")
    srow(30, "VC target return (cross-check)", inp.vc_target_return, "vc_target", FPCT, "decimal")

    b.put(INP, 31, 1, "Investor cash-flow profile (period 0..3; each sums to 100%)", "sect", fill="sect")
    b.put(INP, 32, 1, "Capital call profile", "label")
    b.put(INP, 33, 1, "Distribution profile", "label")
    for j in range(4):
        b.put(INP, 32, 3 + j, float(inp.call_profile[j]) if j < len(inp.call_profile) else 0.0,
              "input", fmt=FPCT, border=True, align="center")
        b.put(INP, 33, 3 + j, float(inp.dist_profile[j]) if j < len(inp.dist_profile) else 0.0,
              "input", fmt=FPCT, border=True, align="center")
    R["call_profile"] = b.rng(INP, 3, 32, 6, 32)
    R["dist_profile"] = b.rng(INP, 3, 33, 6, 33)

    pr0 = 35
    b.put(INP, 34, 1, "Illustrative pipeline (representative ~5 MW distribution projects)", "sect", fill="sect")
    b.header(INP, pr0, ["Project", "State", "Location", "MW", "Duration (h)", "MWh", "Years to sale"])
    for i, p in enumerate(inp.projects):
        r = pr0 + 1 + i
        b.put(INP, r, 1, p["name"], "input")
        b.put(INP, r, 2, p["state"], "input", align="center")
        b.put(INP, r, 3, p["location"], "input")
        b.put(INP, r, 4, p["mw"], "input", fmt=FNUM, border=True)
        b.put(INP, r, 5, p["duration_h"], "input", fmt=FNUM1, border=True)
        b.put(INP, r, 6, f"=D{r}*E{r}", "formula", fmt=FNUM, border=True)
        b.put(INP, r, 7, p["years_to_sale"], "input", fmt=FNUM1, border=True)
    pr1 = pr0 + n
    R["pipe_name0"] = pr0 + 1
    R["pipe_mw"] = b.rng(INP, 4, pr0 + 1, 4, pr1)
    R["pipe_years"] = b.rng(INP, 7, pr0 + 1, 7, pr1)

    # =====================================================================
    # SCENARIOS (3 cases: Conservative / Base / Ideal)
    # =====================================================================
    b.width(SCN, {"A": 44, "B": 14, "C": 14, "D": 14, "E": 14})
    b.put(SCN, 1, 1, "SCENARIOS — one switch drives the live case (CHOOSE)", "title")
    b.put(SCN, 2, 1, "Scenario switch  (1=Conservative 2=Base 3=Ideal)", "label", bold=True)
    b.put(SCN, 2, 2, inp.switch_default, "input", fmt=FNUM, fill="yel", border=True, align="center")
    R["switch"] = b.ref(SCN, 2, 2)
    b.put(SCN, 3, 1, "Active scenario", "label", bold=True)
    b.put(SCN, 3, 2, f'=CHOOSE({R["switch"]},"Conservative","Base","Ideal")', "formula", bold=True)
    R["scenario_name"] = b.ref(SCN, 2, 3)

    b.header(SCN, 4, ["Driver", "Conservative", "Base", "Ideal", "Live (active)"])
    cases = inp.scenarios  # keyed 1..3
    drivers = [("Development-approval rate (DA gate — the 40/65/80%)", "da_rate", FPCT, "live_da"),
               ("RTB price multiplier", "sale_price_multiplier", FMULT, "live_sale_mult"),
               ("Dev cost multiplier", "dev_cost_multiplier", FMULT, "live_dev_mult")]
    for di, (label, field, fmt, key) in enumerate(drivers):
        r = 5 + di
        b.put(SCN, r, 1, label, "label")
        for ci, cid in enumerate([1, 2, 3]):
            val = cases[cid].get(field)
            val = 0 if val is None else float(val)
            b.put(SCN, r, 2 + ci, val, "input", fmt=fmt, border=True, align="center")
        b.put(SCN, r, 5, f"=CHOOSE({R['switch']},B{r},C{r},D{r})", "formula", fmt=fmt, bold=True, border=True)
        R[key] = b.ref(SCN, 5, r)
    # discount rate is fixed (scenarios move ONLY the DA gate, not the discount rate)
    b.put(SCN, 9, 1, "Live discount rate (= base; scenarios don't move it)", "label", bold=True)
    b.put(SCN, 9, 5, f"={R['discount_base']}", "link", fmt=FPCT, bold=True, border=True)
    R["live_discount"] = b.ref(SCN, 5, 9)
    # scenario-column refs (DA gate by scenario; multipliers)
    R["scn_da"] = {1: b.ref(SCN, 2, 5), 2: b.ref(SCN, 3, 5), 3: b.ref(SCN, 4, 5)}
    R["scn_salemult"] = {1: b.ref(SCN, 2, 6), 2: b.ref(SCN, 3, 6), 3: b.ref(SCN, 4, 6)}
    R["scn_devmult"] = {1: b.ref(SCN, 2, 7), 2: b.ref(SCN, 3, 7), 3: b.ref(SCN, 4, 7)}
    # per-scenario flip success = DA x grid connection x sale  (the corrected logic)
    R["scn_flip"] = {c: f"{R['scn_da'][c]}*{R['p_conn']}*{R['p_sale']}" for c in (1, 2, 3)}

    b.put(SCN, 11, 1, "First-Chicago weights", "sect", fill="sect")
    b.header(SCN, 12, ["", "Conservative", "Base", "Ideal", "Sum"])
    b.put(SCN, 13, 1, "Weight", "label")
    for ci, name in enumerate(["Conservative", "Base", "Ideal"]):
        b.put(SCN, 13, 2 + ci, float(inp.weights[name]), "input", fmt=FPCT, border=True, align="center")
    b.put(SCN, 13, 5, "=SUM(B13:D13)", "formula", fmt=FPCT, bold=True, border=True)
    R["weights"] = b.rng(SCN, 2, 13, 4, 13)
    R["weights_sum"] = b.ref(SCN, 5, 13)
    b.put(SCN, 15, 1, "The 40/65/80% are the DEVELOPMENT-APPROVAL gate ONLY (the manager's deck). True flip success = development "
                      "approval x grid connection x sale — far below 65% (see Calc_Survival). The switch moves ONLY the DA gate; "
                      "connection and sale are fixed public benchmarks. Scenarios are the analyst's to OWN.", "note", wrap=True)

    # =====================================================================
    # TIMELINE
    # =====================================================================
    b.width(TL, {"A": 34, "B": 12, "C": 12, "D": 12, "E": 12})
    nper = 3
    b.put(TL, 1, 1, "TIMELINE — built once; every sheet links here", "title")
    b.put(TL, 2, 1, "Base year", "label")
    b.put(TL, 2, 2, a["meta"]["base_year"], "input", fmt=FNUM, border=True)
    R["base_year"] = b.ref(TL, 2, 2)
    b.put(TL, 3, 1, "Period number", "label")
    for p in range(nper + 1):
        b.put(TL, 3, 2 + p, p, "formula", fmt=FNUM, align="center")
    b.put(TL, 4, 1, "Year", "label")
    for p in range(nper + 1):
        col = 2 + p
        b.put(TL, 4, col, f"=$B$2+{get_column_letter(col)}3", "formula", fmt="0", align="center")
    b.put(TL, 5, 1, "Discount factor @ live discount", "label")
    for p in range(nper + 1):
        col = 2 + p
        cl = get_column_letter(col)
        b.put(TL, 5, col, f"=IFERROR(1/(1+{R['live_discount']})^{cl}3,0)", "formula", fmt=FFAC, align="center")
    R["tl_periods"] = b.rng(TL, 2, 3, 2 + nper, 3)

    # =====================================================================
    # CALC_SURVIVAL (separate gates; flip success = their product)
    # =====================================================================
    b.width(SURV, {"A": 46, "B": 16, "C": 18})
    b.put(SURV, 1, 1, "CALC — SURVIVAL GATES (each separate; flip success = their product)", "title")
    b.put(SURV, 2, 1, "The manager's 40/65/80% are the DEVELOPMENT-APPROVAL gate ONLY. True develop-and-flip success = development "
                      "approval x grid connection x sale — a multi-period survival / probability-of-default curve. The DA gate is LIVE "
                      "from the scenario switch; grid connection and sale are fixed public benchmarks.", "note", wrap=True)
    b.header(SURV, 3, ["Gate", "Probability", "Cumulative survival"])
    gate_rows = [("Development approval (live scenario DA gate)", R["live_da"]),
                 ("Grid connection", R["p_conn"]),
                 ("Reach sale (flip exit)", R["p_sale"])]
    for i, (label, pref) in enumerate(gate_rows):
        r = 4 + i
        b.put(SURV, r, 1, label, "label")
        b.put(SURV, r, 2, f"={pref}", "link", fmt=FPCT, border=True)
        if i == 0:
            b.put(SURV, r, 3, f"=B{r}", "formula", fmt=FPCT, border=True)
        else:
            b.put(SURV, r, 3, f"=C{r-1}*B{r}", "formula", fmt=FPCT, border=True)
    b.put(SURV, 7, 1, "LIVE flip success (DA x connection x sale)", "label", bold=True)
    b.put(SURV, 7, 3, "=C6", "formula", fmt=FPCT, bold=True, border=True, fill="sect")
    R["live_success"] = b.ref(SURV, 3, 7)
    b.put(SURV, 9, 1, "Public-benchmark development approval", "label")
    b.put(SURV, 9, 3, f"={R['da_ind']}", "link", fmt=FPCT, border=True)
    b.put(SURV, 10, 1, "Independent flip success (benchmark DA x conn x sale)", "label", bold=True)
    b.put(SURV, 10, 3, f"=C9*{R['p_conn']}*{R['p_sale']}", "formula", fmt=FPCT, bold=True, border=True)
    R["flip_independent"] = b.ref(SURV, 3, 10)
    b.put(SURV, 12, 1, "Manager's headline DA rate (Base — the '65%')", "label")
    b.put(SURV, 12, 3, f"={R['scn_da'][2]}", "link", fmt=FPCT, border=True)
    b.put(SURV, 13, 1, "True flip success at that DA (DA x conn x sale)", "label", bold=True)
    b.put(SURV, 13, 3, f"={R['scn_flip'][2]}", "formula", fmt=FPCT, bold=True, border=True)
    R["flip_at_base_da"] = b.ref(SURV, 3, 13)
    b.put(SURV, 14, 3, '=IF(C13<C12,"FLAG: 65% is the DA gate only","ok")', "formula", align="center", border=True)
    b.put(SURV, 15, 1, "The 65% headline is the approval gate alone; after grid connection (~70%) and sale (~80%) the true flip success is "
                       "~36%. The DA gate is the master return driver — the scenarios move it 40/65/80%. The sub-5MW AEMO registration "
                       "exemption MAY lift small-distribution success — verify per state.", "note", wrap=True)

    # =====================================================================
    # CALC_PROJECT_rNPV (per-project risk-adjusted NAV — dev cost only)
    # =====================================================================
    b.width(RNPV, {"A": 28, "B": 7, "C": 7, "D": 7, "E": 11, "F": 8, "G": 11, "H": 11,
                   "I": 11, "J": 8, "K": 11, "L": 10, "M": 11, "N": 11})
    b.put(RNPV, 1, 1, "CALC — PER-PROJECT RISK-ADJUSTED NAV (rNPV)", "title")
    b.put(RNPV, 2, 1, "Per project: RTB sale − DEVELOPMENT cost = margin → × cumulative success → discounted. Cost is DEV ONLY "
                      "(the fund sells RTB; the buyer funds construction). All figures AUD $m unless stated.", "note", wrap=True)
    b.header(RNPV, 3, ["Project", "State", "MW", "Years", "RTB $/MW", "Sale mult", "Sale $m",
                       "Dev cost $m", "Margin $m", "Cum P", "Risk-adj $m", "Disc factor", "PV $m", "Sale@1x $m"])
    rv0 = 4
    for i in range(n):
        r = rv0 + i
        ip = R["pipe_name0"] + i
        b.put(RNPV, r, 1, f"={b.ref(INP, 1, ip)}", "link")
        b.put(RNPV, r, 2, f"={b.ref(INP, 2, ip)}", "link", align="center")
        b.put(RNPV, r, 3, f"={b.ref(INP, 4, ip)}", "link", fmt=FNUM, border=True)
        b.put(RNPV, r, 4, f"={b.ref(INP, 7, ip)}", "link", fmt=FNUM1, border=True)
        b.put(RNPV, r, 5, f"=IFERROR(INDEX({R['rtb_prices']},MATCH(B{r},{R['rtb_states']},0)),0)", "formula", fmt=FMW, border=True)
        b.put(RNPV, r, 6, f"={R['live_sale_mult']}", "link", fmt=FMULT, border=True)
        b.put(RNPV, r, 7, f"=C{r}*E{r}*F{r}", "formula", fmt=FM2, border=True)
        b.put(RNPV, r, 8, f"={R['dev_cost']}*{R['live_dev_mult']}", "formula", fmt=FM2, border=True)
        b.put(RNPV, r, 9, f"=G{r}-H{r}", "formula", fmt=FM2, border=True)
        b.put(RNPV, r, 10, f"={R['live_success']}", "link", fmt=FPCT, border=True)
        b.put(RNPV, r, 11, f"=I{r}*J{r}", "formula", fmt=FM2, border=True)
        b.put(RNPV, r, 12, f"=IFERROR(1/(1+{R['live_discount']})^D{r},0)", "formula", fmt=FFAC, border=True)
        b.put(RNPV, r, 13, f"=K{r}*L{r}", "formula", fmt=FM2, border=True)
        b.put(RNPV, r, 14, f"=C{r}*E{r}", "formula", fmt=FM2, border=True)
    rv1 = rv0 + n - 1
    rt = rv1 + 1
    b.put(RNPV, rt, 1, "Pipeline total (representative)", "label", bold=True)
    for col in (3, 7, 8, 13):
        cl = get_column_letter(col)
        b.put(RNPV, rt, col, f"=SUM({cl}{rv0}:{cl}{rv1})", "formula", fmt=(FNUM if col == 3 else FM2), bold=True, border=True)
    R["pipeline_rnpv"] = b.ref(RNPV, 13, rt)
    R["rnpv_mw"] = b.rng(RNPV, 3, rv0, 3, rv1)
    R["rnpv_rtb"] = b.rng(RNPV, 5, rv0, 5, rv1)
    R["rnpv_years"] = b.rng(RNPV, 4, rv0, 4, rv1)
    rbl = rt + 1
    b.put(RNPV, rbl, 1, "Blended RTB sale per project (@1x)", "label", bold=True)
    b.put(RNPV, rbl, 13, f"=AVERAGE({b.rng(RNPV, 14, rv0, 14, rv1)})", "formula", fmt=FM2, bold=True, border=True, fill="sect")
    R["base_blended"] = b.ref(RNPV, 13, rbl)

    # =====================================================================
    # CALC_FUND (the funnel -> fees -> investor IRR/MOIC, live scenario)
    # =====================================================================
    b.width(FUND, {"A": 44, "B": 4, "C": 14, "D": 10, "E": 10, "F": 10})
    b.put(FUND, 1, 1, "CALC — FUND FUNNEL, FEES & INVESTOR RETURN (live scenario)", "title")
    b.put(FUND, 2, 1, "The funnel: projects_started = target ÷ success (widens as success falls). Full dev cost on delivered + "
                      "partial on dropouts. Fees: entry + management + carry over the hurdle. Investor IRR is closed-form over the "
                      "effective hold (so it reproduces in any Excel). All figures AUD $m.", "note", wrap=True)
    b.put(FUND, 4, 1, "Funnel (live scenario)", "sect", fill="sect")
    b.put(FUND, 5, 1, "Live cumulative success", "label")
    b.put(FUND, 5, 3, f"={R['live_success']}", "link", fmt=FPCT, border=True)
    b.put(FUND, 6, 1, "Projects target (delivered & sold)", "label")
    b.put(FUND, 6, 3, f"={R['target']}", "link", fmt=FNUM, border=True)
    b.put(FUND, 7, 1, "Projects started (funnel)", "label")
    b.put(FUND, 7, 3, "=IFERROR(C6/C5,0)", "formula", fmt=FNUM1, border=True)
    b.put(FUND, 8, 1, "Projects failed (dropouts)", "label")
    b.put(FUND, 8, 3, "=C7-C6", "formula", fmt=FNUM1, border=True)
    b.put(FUND, 9, 1, "Dev cost per project (live)", "label")
    b.put(FUND, 9, 3, f"={R['dev_cost']}*{R['live_dev_mult']}", "formula", fmt=FM2, border=True)
    b.put(FUND, 10, 1, "Total development cost", "label", bold=True)
    b.put(FUND, 10, 3, f"=C6*C9+C8*{R['abandon']}*C9", "formula", fmt=FM, border=True)
    R["fund_devcost"] = b.ref(FUND, 3, 10)

    b.put(FUND, 11, 1, "Proceeds & fees", "sect", fill="sect")
    b.put(FUND, 12, 1, "Blended RTB sale per project (live)", "label")
    b.put(FUND, 12, 3, f"={R['base_blended']}*{R['live_sale_mult']}", "formula", fmt=FM2, border=True)
    b.put(FUND, 13, 1, "Gross proceeds", "label", bold=True)
    b.put(FUND, 13, 3, "=C6*C12", "formula", fmt=FM, border=True)
    b.put(FUND, 14, 1, "Entry fee", "label")
    b.put(FUND, 14, 3, f"={R['entry_pct']}*{R['committed']}", "formula", fmt=FM, border=True)
    R["entry_fee"] = b.ref(FUND, 3, 14)
    b.put(FUND, 15, 1, "Management fee (total)", "label")
    b.put(FUND, 15, 3, f"={R['mgmt_pct']}*{R['committed']}*{R['term']}", "formula", fmt=FM, border=True)
    R["mgmt_fee"] = b.ref(FUND, 3, 15)
    b.put(FUND, 16, 1, "Invested capital (LP, called)", "label", bold=True)
    b.put(FUND, 16, 3, "=C10+C14+C15", "formula", fmt=FM, border=True, fill="sect")
    R["fund_invested"] = b.ref(FUND, 3, 16)

    b.put(FUND, 17, 1, "Carry, distributions & return (live)", "sect", fill="sect")
    b.put(FUND, 18, 1, "Profit before carry", "label")
    b.put(FUND, 18, 3, "=C13-C16", "formula", fmt=FM, border=True)
    b.put(FUND, 19, 1, "Hurdle factor = (1+hurdle)^term − 1", "label")
    b.put(FUND, 19, 3, f"=(1+{R['hurdle_pct']})^{R['term']}-1", "formula", fmt=FPCT, border=True)
    R["hfac"] = b.ref(FUND, 3, 19)
    b.put(FUND, 20, 1, "Hurdle amount", "label")
    b.put(FUND, 20, 3, "=C16*C19", "formula", fmt=FM, border=True)
    b.put(FUND, 21, 1, "Carry to GP", "label")
    b.put(FUND, 21, 3, f"={R['carry_pct']}*MAX(0,C18-C20)", "formula", fmt=FM, border=True)
    b.put(FUND, 22, 1, "Distributions to LP", "label", bold=True)
    b.put(FUND, 22, 3, "=C13-C21", "formula", fmt=FM, border=True)
    b.put(FUND, 23, 1, "MOIC (net)", "label", bold=True)
    b.put(FUND, 23, 3, "=IFERROR(C22/C16,0)", "formula", fmt=FX, bold=True, border=True)
    R["moic_live"] = b.ref(FUND, 3, 23)
    b.put(FUND, 24, 1, "Mean distribution period (yrs)", "label")
    b.put(FUND, 24, 3, f"=SUMPRODUCT({R['tl_periods']},{R['dist_profile']})", "formula", fmt=FNUM1, border=True)
    b.put(FUND, 25, 1, "Mean capital-call period (yrs)", "label")
    b.put(FUND, 25, 3, f"=SUMPRODUCT({R['tl_periods']},{R['call_profile']})", "formula", fmt=FNUM1, border=True)
    b.put(FUND, 26, 1, "Effective hold (yrs)", "label")
    b.put(FUND, 26, 3, "=C24-C25", "formula", fmt=FNUM1, border=True)
    R["eff_hold"] = b.ref(FUND, 3, 26)
    b.put(FUND, 27, 1, "Investor IRR (live, closed-form)", "label", bold=True)
    b.put(FUND, 27, 3, "=IFERROR(C23^(1/C26)-1,0)", "formula", fmt=FPCT, bold=True, border=True, fill="sect")
    R["irr_live"] = b.ref(FUND, 3, 27)

    # =====================================================================
    # RETURNS (per-scenario investor IRR/MOIC, First Chicago, valuation range)
    # =====================================================================
    b.width(RET, {"A": 38, "B": 13, "C": 13, "D": 13, "E": 13})
    b.put(RET, 1, 1, "RETURNS — investor IRR & MOIC by scenario, First-Chicago, valuation range", "title")
    b.put(RET, 2, 1, "Each scenario's funnel is computed independently of the switch. Investor IRR is closed-form over the effective hold. "
                     "All figures AUD $m unless stated.", "note", wrap=True)
    b.put(RET, 3, 1, "Investor return by scenario (after fees)", "sect", fill="sect")
    b.header(RET, 4, ["Metric", "Conservative", "Base", "Ideal"])
    scol = {1: "B", 2: "C", 3: "D"}
    metric_rows = [
        (5, "Flip success (DA x conn x sale)", lambda c: f"={R['scn_flip'][c]}", FPCT, "formula"),
        (6, "RTB price multiplier", lambda c: f"={R['scn_salemult'][c]}", FMULT, "link"),
        (7, "Dev cost multiplier", lambda c: f"={R['scn_devmult'][c]}", FMULT, "link"),
        (8, "Dev cost per project", lambda c: f"={R['dev_cost']}*{scol[c]}7", FM2, "formula"),
        (9, "Projects started", lambda c: f"=IFERROR({R['target']}/{scol[c]}5,0)", FNUM1, "formula"),
        (10, "Projects failed", lambda c: f"={scol[c]}9-{R['target']}", FNUM1, "formula"),
        (11, "Total dev cost", lambda c: f"={R['target']}*{scol[c]}8+{scol[c]}10*{R['abandon']}*{scol[c]}8", FM, "formula"),
        (12, "Gross proceeds", lambda c: f"={R['target']}*{R['base_blended']}*{scol[c]}6", FM, "formula"),
        (13, "Invested capital", lambda c: f"={scol[c]}11+{R['mgmt_fee']}+{R['entry_fee']}", FM, "formula"),
        (14, "Profit before carry", lambda c: f"={scol[c]}12-{scol[c]}13", FM, "formula"),
        (15, "Hurdle amount", lambda c: f"={scol[c]}13*{R['hfac']}", FM, "formula"),
        (16, "Carry to GP", lambda c: f"={R['carry_pct']}*MAX(0,{scol[c]}14-{scol[c]}15)", FM, "formula"),
        (17, "Distributions to LP", lambda c: f"={scol[c]}12-{scol[c]}16", FM, "formula"),
        (18, "MOIC (net)", lambda c: f"=IFERROR({scol[c]}17/{scol[c]}13,0)", FX, "formula"),
        (19, "Investor IRR", lambda c: f"=IFERROR({scol[c]}18^(1/{R['eff_hold']})-1,0)", FPCT, "formula"),
    ]
    for r, label, fn, fmt, kind in metric_rows:
        b.put(RET, r, 1, label, "label", bold=(r in (18, 19)))
        for c in (1, 2, 3):
            b.put(RET, r, 1 + c, fn(c), kind, fmt=fmt, border=True, bold=(r in (18, 19)))
    R["irr_by"] = {1: b.ref(RET, 2, 19), 2: b.ref(RET, 3, 19), 3: b.ref(RET, 4, 19)}
    R["moic_by"] = {1: b.ref(RET, 2, 18), 2: b.ref(RET, 3, 18), 3: b.ref(RET, 4, 18)}
    R["ret_irr_rng"] = b.rng(RET, 2, 19, 4, 19)
    R["ret_invested_rng"] = b.rng(RET, 2, 13, 4, 13)

    b.put(RET, 21, 1, "First-Chicago probability-weighted expected return", "sect", fill="sect")
    b.header(RET, 22, ["", "Conservative", "Base", "Ideal", "Expected"])
    b.put(RET, 23, 1, "Weight", "label")
    for ci, name in enumerate(["Conservative", "Base", "Ideal"]):
        b.put(RET, 23, 2 + ci, f"={b.ref(SCN, 2 + ci, 13)}", "link", fmt=FPCT, border=True, align="center")
    b.put(RET, 24, 1, "Investor IRR", "label", bold=True)
    for c in (1, 2, 3):
        b.put(RET, 24, 1 + c, f"={R['irr_by'][c]}", "link", fmt=FPCT, border=True)
    b.put(RET, 24, 5, f"=SUMPRODUCT({R['weights']},B24:D24)", "formula", fmt=FPCT, bold=True, border=True, fill="sect")
    R["expected_irr"] = b.ref(RET, 5, 24)
    b.put(RET, 25, 1, "MOIC (net)", "label")
    for c in (1, 2, 3):
        b.put(RET, 25, 1 + c, f"={R['moic_by'][c]}", "link", fmt=FX, border=True)
    b.put(RET, 25, 5, f"=SUMPRODUCT({R['weights']},B25:D25)", "formula", fmt=FX, bold=True, border=True)
    R["expected_moic"] = b.ref(RET, 5, 25)

    b.put(RET, 27, 1, "Valuation range (per-pipeline asset value — cross-check)", "sect", fill="sect")
    b.put(RET, 27, 3, "Representative 6-project pipeline, NOT the whole fund.", "note")
    vrows = [(28, "rNPV pipeline (Base)", f"={R['pipeline_rnpv']}"),
             (29, "$/MW benchmark (dev value)", None),   # filled after CC built
             (30, "VC method (today value)", None)]
    b.put(RET, 28, 1, vrows[0][1], "label")
    b.put(RET, 28, 3, vrows[0][2], "link", fmt=FM2, border=True)
    # placeholders; CC refs added below once CC cells exist
    R["ret_val_low"] = b.ref(RET, 3, 31)
    R["ret_val_mid"] = b.ref(RET, 3, 32)
    R["ret_val_high"] = b.ref(RET, 3, 33)

    # =====================================================================
    # CALC_CROSSCHECKS ($/MW benchmark, VC method, RTB-as-%-of-built)
    # =====================================================================
    b.width(CC, {"A": 42, "B": 4, "C": 16, "D": 14, "E": 14})
    b.put(CC, 1, 1, "CALC — CROSS-CHECKS: $/MW benchmark, VC method, RTB vs built", "title")
    b.put(CC, 2, 1, "Asset-value cross-checks on the representative pipeline, Base scenario. All figures AUD $m unless stated.", "note", wrap=True)
    base_sale_mult = R["scn_salemult"][2]
    base_dev_mult = R["scn_devmult"][2]
    base_success = R["scn_flip"][2]
    b.put(CC, 3, 1, "$/MW benchmark (Base)", "sect", fill="sect")
    cc = [
        (4, "Total pipeline MW", f"=SUM({R['rnpv_mw']})", FNUM, "formula"),
        (5, "Gross RTB asset value $m", f"=SUMPRODUCT({R['rnpv_mw']},{R['rnpv_rtb']})*{base_sale_mult}", FM, "formula"),
        (6, "Total dev cost $m", f"={R['dev_cost']}*{base_dev_mult}*{n}", FM, "formula"),
        (7, "Average years to sale", f"=AVERAGE({R['rnpv_years']})", FNUM1, "formula"),
        (8, "Flip success (Base, DA x conn x sale)", f"={base_success}", FPCT, "formula"),
        (9, "$/MW implied dev value $m", f"=IFERROR((C5-C6)*C8/(1+{R['discount_base']})^C7,0)", FM2, "formula"),
    ]
    for r, label, val, fmt, kind in cc:
        b.put(CC, r, 1, label, "label")
        b.put(CC, r, 3, val, kind, fmt=fmt, border=True, bold=(r == 9))
    R["dpmw_dev"] = b.ref(CC, 3, 9)

    b.put(CC, 11, 1, "VC method (Base)", "sect", fill="sect")
    vc = [
        (12, "Total RTB sale value $m", f"=SUMPRODUCT({R['rnpv_mw']},{R['rnpv_rtb']})*{base_sale_mult}", FM, "formula"),
        (13, "Total dev cost $m", "=C6", FM, "formula"),
        (14, "Flip success (Base)", "=C8", FPCT, "link"),
        (15, "Exit equity value (expected) $m", "=C14*(C12-C13)", FM2, "formula"),
        (16, "VC target return", f"={R['vc_target']}", FPCT, "link"),
        (17, "Hold horizon (yrs)", f"={R['term']}", FNUM, "link"),
        (18, "VC today value $m", "=IFERROR(C15/(1+C16)^C17,0)", FM2, "formula"),
    ]
    for r, label, val, fmt, kind in vc:
        b.put(CC, r, 1, label, "label")
        b.put(CC, r, 3, val, kind, fmt=fmt, border=True, bold=(r == 18))
    R["vc_today"] = b.ref(CC, 3, 18)

    b.put(CC, 20, 1, "RTB as % of built-asset value (sense-check)", "sect", fill="sect")
    b.header(CC, 21, ["State", "RTB $/MW", "Built $/MW", "RTB % of built"])
    for i, st in enumerate(["NSW", "VIC", "SA"]):
        r = 22 + i
        b.put(CC, r, 1, st, "label")
        b.put(CC, r, 2, f"={R['rtb_' + st]}", "link", fmt=FMW, border=True)
        b.put(CC, r, 3, f"={R['built_cost']}", "link", fmt=FMW, border=True)
        b.put(CC, r, 4, f"=IFERROR(B{r}/C{r},0)", "formula", fmt=FPCT, border=True)
    b.put(CC, 25, 1, "Expect ~10–12% — confirms RTB is the early-stage development slice, not the built asset.", "note", wrap=True)

    # backfill Returns valuation range now that CC refs exist
    b.put(RET, 29, 1, "$/MW benchmark (dev value)", "label")
    b.put(RET, 29, 3, f"={R['dpmw_dev']}", "link", fmt=FM2, border=True)
    b.put(RET, 30, 1, "VC method (today value)", "label")
    b.put(RET, 30, 3, f"={R['vc_today']}", "link", fmt=FM2, border=True)
    b.put(RET, 31, 1, "Low", "label", bold=True)
    b.put(RET, 31, 3, "=MIN(C28:C30)", "formula", fmt=FM2, bold=True, border=True)
    b.put(RET, 32, 1, "Midpoint", "label", bold=True)
    b.put(RET, 32, 3, "=AVERAGE(C28:C30)", "formula", fmt=FM2, bold=True, border=True, fill="sect")
    b.put(RET, 33, 1, "High", "label", bold=True)
    b.put(RET, 33, 3, "=MAX(C28:C30)", "formula", fmt=FM2, bold=True, border=True)

    # =====================================================================
    # SENSITIVITY (investor MOIC: development-approval rate x RTB price)
    # =====================================================================
    b.width(SENS, {"A": 24, "B": 11, "C": 9, "D": 9, "E": 9, "F": 9, "G": 9,
                   "H": 11, "I": 11, "J": 11, "K": 11})
    b.put(SENS, 1, 1, "SENSITIVITY — investor MOIC (net): development approval × RTB price", "title")
    b.put(SENS, 2, 1, "Investor MOIC vs DEVELOPMENT-APPROVAL rate (down) × RTB price multiplier (across); all else at Base. "
                      "Flip success = DA × grid connection × sale, so the funnel widens with the FULL gate chain (not the DA rate alone). "
                      "IRR ≈ MOIC^(1/eff-hold). Live formula grid. All figures AUD $m / x.", "note", wrap=True)
    da_rates = [0.40, 0.55, 0.65, 0.80, 0.95]
    price_mults = [0.70, 0.85, 1.00, 1.15, 1.30]
    GC0 = 3  # grid columns C..G
    # constants
    b.put(SENS, 4, 1, "Carry %", "label"); b.put(SENS, 4, 2, f"={R['carry_pct']}", "link", fmt=FPCT, border=True)
    b.put(SENS, 5, 1, "Hurdle factor", "label"); b.put(SENS, 5, 2, f"={R['hfac']}", "link", fmt=FPCT, border=True)
    b.put(SENS, 6, 1, "Fixed fees (mgmt+entry) $m", "label")
    b.put(SENS, 6, 2, f"={R['mgmt_fee']}+{R['entry_fee']}", "formula", fmt=FM, border=True)
    b.put(SENS, 7, 1, "Conn × sale (flip adj)", "label")
    b.put(SENS, 7, 2, f"={R['p_conn']}*{R['p_sale']}", "formula", fmt=FPCT, border=True)
    R["s_carry"], R["s_hfac"], R["s_fees"] = b.ref(SENS, 2, 4), b.ref(SENS, 2, 5), b.ref(SENS, 2, 6)
    R["s_flipadj"] = b.ref(SENS, 2, 7)
    # price header (row 8) and gross-per-project helper row (row 9)
    b.put(SENS, 8, 2, "Price mult →", "label", bold=True, align="right")
    b.put(SENS, 9, 2, "Gross $m →", "label", bold=True, align="right")
    for j, pm in enumerate(price_mults):
        cl = get_column_letter(GC0 + j)
        b.put(SENS, 8, GC0 + j, pm, "input", fmt=FMULT, fill="yel", align="center", border=True)
        b.put(SENS, 9, GC0 + j, f"={R['target']}*{R['base_blended']}*{cl}8", "formula", fmt=FM, align="center", border=True)
    # header row 10 + helper col labels
    b.put(SENS, 10, 2, "DA gate ↓", "head", fill="head", align="center", border=True)
    for j in range(len(price_mults)):
        b.put(SENS, 10, GC0 + j, "MOIC", "head", fill="head", align="center", border=True)
    for k, lab in enumerate(["Flip succ", "Started", "Total dev", "Invested"]):
        b.put(SENS, 10, 8 + k, lab, "head", fill="head", align="center", wrap=True, border=True)
    for i, da in enumerate(da_rates):
        r = 11 + i
        b.put(SENS, r, 2, da, "input", fmt=FPCT, fill="yel", align="center", border=True)
        b.put(SENS, r, 8, f"=$B{r}*{R['s_flipadj']}", "formula", fmt=FPCT, border=True)
        b.put(SENS, r, 9, f"=IFERROR({R['target']}/H{r},0)", "formula", fmt=FNUM1, border=True)
        b.put(SENS, r, 10, f"={R['target']}*{R['dev_cost']}+(I{r}-{R['target']})*{R['abandon']}*{R['dev_cost']}", "formula", fmt=FM, border=True)
        b.put(SENS, r, 11, f"=J{r}+{R['s_fees']}", "formula", fmt=FM, border=True)
        for j in range(len(price_mults)):
            cl = get_column_letter(GC0 + j)
            # MOIC = (gross - carry) / invested ; carry = carry%*MAX(0,(gross-invested)-invested*hfac)
            f = (f"=IFERROR(({cl}$9-{R['s_carry']}*MAX(0,({cl}$9-$K{r})-$K{r}*{R['s_hfac']}))/$K{r},0)")
            b.put(SENS, r, GC0 + j, f, "formula", fmt=FX, border=True)
    R["sens_grid"] = b.rng(SENS, GC0, 11, GC0 + len(price_mults) - 1, 11 + len(da_rates) - 1)

    # =====================================================================
    # CHECKS
    # =====================================================================
    b.width(CHK, {"A": 54, "B": 12, "C": 38, "D": 4, "E": 9, "F": 9, "G": 9})
    b.put(CHK, 1, 1, "CHECKS — integrity framework (master check feeds the Cover)", "title")
    b.header(CHK, 3, ["Check", "Result", "Note"])
    cr0 = 4
    err_row = cr0 + 13
    fc_row = cr0 + 11   # First-Chicago range check uses E/F/G helpers on its own row
    checks = [
        (f'=IF(AND(MIN({b.rng(INP,3,22,3,24)})>=0,MAX({b.rng(INP,3,22,3,24)})<=1),"OK","ERROR")',
         "Every gate probability ∈ [0,1]", "Gate probs bounded"),
        (f'=IF({R["live_success"]}<=MIN({b.rng(SURV,2,4,2,6)})+0.000001,"OK","ERROR")',
         "Flip success ≤ each gate", "Survival monotonic"),
        (f'=IF(MIN({R["pipe_mw"]})>0,"OK","ERROR")', "All MW positive", "Sign check"),
        (f'=IF(MIN({b.rng(RNPV,7,4,7,4 + n - 1)})>0,"OK","ERROR")', "All RTB sale values positive", "Sign check"),
        (f'=IF({R["dev_cost"]}>0,"OK","ERROR")', "Dev cost positive", "Sign check"),
        (f'=IF(AND({R["switch"]}>=1,{R["switch"]}<=3),"OK","ERROR")', "Scenario switch ∈ {1,2,3}", "Switch valid"),
        (f'=IF(AND({R["scn_da"][1]}<={R["scn_da"][2]},{R["scn_da"][2]}<={R["scn_da"][3]}),"OK","ERROR")',
         "Scenario DA-gate monotonic", "Cons ≤ Base ≤ Ideal"),
        (f'=IF(AND({R["irr_by"][1]}<={R["irr_by"][2]},{R["irr_by"][2]}<={R["irr_by"][3]}),"OK","ERROR")',
         "Investor IRR monotonic", "Cons ≤ Base ≤ Ideal"),
        (f'=IF(ABS({R["weights_sum"]}-1)<0.001,"OK","ERROR")', "Scenario weights sum to 100%", "First-Chicago weights"),
        (f'=IF(ABS(SUM({R["call_profile"]})-1)<0.001,"OK","ERROR")', "Capital-call profile sums to 100%", "Cash-flow profile"),
        (f'=IF(ABS(SUM({R["dist_profile"]})-1)<0.001,"OK","ERROR")', "Distribution profile sums to 100%", "Cash-flow profile"),
        (f'=IF(AND(G{fc_row}>=E{fc_row}-0.0001,G{fc_row}<=F{fc_row}+0.0001),"OK","ERROR")',
         "First-Chicago IRR within scenario range", "Weighting sanity (helpers E:G)"),
        (f'=IF(MIN({R["ret_invested_rng"]})>0,"OK","ERROR")', "Invested capital positive (all scenarios)", "Sign check"),
        (f'=IF(SUM(E{err_row}:G{err_row})=0,"OK","ERROR")', "No error cells in key outputs", "#REF!/#DIV0! scan"),
    ]
    for i, (formula, label, note) in enumerate(checks):
        r = cr0 + i
        b.put(CHK, r, 1, label, "label")
        b.put(CHK, r, 2, formula, "formula", align="center", border=True)
        b.put(CHK, r, 3, note, "note")
    # helpers for the First-Chicago range check (kept short)
    b.put(CHK, fc_row, 5, f"=MIN({R['ret_irr_rng']})", "formula", fmt=FPCT, align="center", border=True)
    b.put(CHK, fc_row, 6, f"=MAX({R['ret_irr_rng']})", "formula", fmt=FPCT, align="center", border=True)
    b.put(CHK, fc_row, 7, f"={R['expected_irr']}", "link", fmt=FPCT, align="center", border=True)
    b.put(CHK, err_row, 5, f"=SUMPRODUCT(--ISERROR({b.rng(RNPV,13,4,13,rt)}))", "formula", align="center", border=True)
    b.put(CHK, err_row, 6, f"=SUMPRODUCT(--ISERROR({R['ret_irr_rng']}))", "formula", align="center", border=True)
    b.put(CHK, err_row, 7, f"=SUMPRODUCT(--ISERROR({R['sens_grid']}))", "formula", align="center", border=True)
    cr1 = cr0 + len(checks) - 1
    rmaster = cr1 + 2
    b.put(CHK, rmaster, 1, "MASTER CHECK", "label", bold=True)
    b.put(CHK, rmaster, 2, f'=IF(COUNTIF(B{cr0}:B{cr1},"ERROR")=0,"OK","ERROR")', "formula", bold=True, align="center", border=True)
    R["master_check"] = b.ref(CHK, 2, rmaster)
    ok_rule = CellIsRule(operator="equal", formula=['"OK"'], fill=FILL_GREEN, font=Font(color="006100"))
    err_rule = CellIsRule(operator="equal", formula=['"ERROR"'], fill=FILL_RED, font=Font(color="9C0006"))
    b.ws[CHK].conditional_formatting.add(f"B{cr0}:B{rmaster}", ok_rule)
    b.ws[CHK].conditional_formatting.add(f"B{cr0}:B{rmaster}", err_rule)

    # =====================================================================
    # DASHBOARD
    # =====================================================================
    b.width(DSH, {"A": 38, "B": 16, "C": 6, "D": 32, "E": 16})
    b.put(DSH, 1, 1, "ILLUSTRATIVE DISTRIBUTION-BESS DEVELOP-AND-FLIP FUND — DASHBOARD", "title")
    b.put(DSH, 2, 1, "Develop ~5 MW distribution BESS to RTB, sell before construction (NSW/VIC/SA). ILLUSTRATIVE — the manager figures are "
                     "manager claims to verify. Not investment advice.", "disc", wrap=True)
    b.put(DSH, 4, 1, "Active scenario", "label", bold=True)
    b.put(DSH, 4, 2, f"={R['scenario_name']}", "link", bold=True)
    b.put(DSH, 4, 4, "Master check", "label", bold=True)
    b.put(DSH, 4, 5, f"={R['master_check']}", "link", bold=True, align="center")
    b.put(DSH, 6, 1, "EXPECTED INVESTOR RETURN (First-Chicago)", "sect", fill="sect")
    b.put(DSH, 6, 4, "LIVE SCENARIO", "sect", fill="sect")
    b.put(DSH, 7, 1, "Expected IRR (after fees)", "label", bold=True)
    b.put(DSH, 7, 2, f"={R['expected_irr']}", "link", fmt=FPCT, bold=True, border=True)
    b.put(DSH, 8, 1, "Expected MOIC", "label")
    b.put(DSH, 8, 2, f"={R['expected_moic']}", "link", fmt=FX, border=True)
    b.put(DSH, 7, 4, "Investor IRR (live)", "label", bold=True)
    b.put(DSH, 7, 5, f"={R['irr_live']}", "link", fmt=FPCT, bold=True, border=True)
    b.put(DSH, 8, 4, "MOIC (live)", "label")
    b.put(DSH, 8, 5, f"={R['moic_live']}", "link", fmt=FX, border=True)
    b.put(DSH, 10, 1, "INVESTOR IRR BY SCENARIO", "sect", fill="sect")
    b.header(DSH, 11, ["Scenario", "Flip succ", "IRR", "MOIC"])
    for i, (name, cid) in enumerate([("Conservative", 1), ("Base", 2), ("Ideal", 3)]):
        r = 12 + i
        b.put(DSH, r, 1, name, "label")
        b.put(DSH, r, 2, f"={R['scn_flip'][cid]}", "formula", fmt=FPCT, border=True)
        b.put(DSH, r, 3, f"={R['irr_by'][cid]}", "link", fmt=FPCT, border=True)
        b.put(DSH, r, 4, f"={R['moic_by'][cid]}", "link", fmt=FX, border=True)
    b.put(DSH, 10, 4, "KEY ASSUMPTIONS & FLAG", "sect", fill="sect")
    ka = [(11, "Committed capital $m", f"={R['committed']}", FM),
          (12, "Projects target", f"={R['target']}", FNUM),
          (13, "Manager headline DA gate (Base)", f"={R['scn_da'][2]}", FPCT),
          (14, "True flip success (Base, DAxconnxsale)", f"={R['flip_at_base_da']}", FPCT),
          (15, "Independent flip success (benchmark)", f"={R['flip_independent']}", FPCT)]
    for r, label, val, fmt in ka:
        b.put(DSH, r, 4, label, "label")
        b.put(DSH, r, 5, val, "link", fmt=fmt, border=True)
    b.put(DSH, 17, 1, "Conclusion (illustrative)", "sect", fill="sect")
    b.put(DSH, 18, 1,
          "A real, policy-backed, capital-light niche with a viable RTB exit — but the develop-and-flip economics are THIN once the gates "
          "are modelled correctly. The manager's 65% is the development-approval gate ALONE; true flip success = approval x grid connection "
          "x sale is ~36% at Base, so the expected investor return is only marginally positive and the Conservative case loses capital. The "
          "single biggest risk is EXIT/BUYER risk, then development/approval. On these numbers the flip is the WEAKEST entry — building or "
          "holding the asset earns far more (see the stage analysis). Pursue only on verified buyer depth, RTB comps and a survivable downside.", "note", wrap=True)
    b.ws[DSH].merge_cells("A18:E23")

    # =====================================================================
    # COVER
    # =====================================================================
    b.width(COV, {"A": 26, "B": 64})
    b.put(COV, 1, 1, "BESS Pipeline Valuation — Develop-and-Flip (RTB)", "title")
    cover = [
        (2, "Subtitle", "Investor (LP) IRR/MOIC of an illustrative distribution-BESS develop-and-flip fund (NSW/VIC/SA)"),
        (3, "Version", "v1.0"),
        (4, "Author", "Portfolio project (independent rebuild of the manager's projections claims)"),
        (5, "Date", a["meta"]["as_at"]),
        (6, "Currency / Units", "AUD, $ millions ($m)"),
    ]
    for r, k, v in cover:
        b.put(COV, r, 1, k, "label", bold=True)
        b.put(COV, r, 2, v, "label", wrap=True)
    b.put(COV, 7, 1, "Active scenario", "label", bold=True)
    b.put(COV, 7, 2, f"={R['scenario_name']}", "link", bold=True)
    b.put(COV, 8, 1, "MASTER CHECK", "label", bold=True)
    b.put(COV, 8, 2, f"={R['master_check']}", "link", bold=True)
    b.ws[COV].conditional_formatting.add("B8", CellIsRule(operator="equal", formula=['"OK"'], fill=FILL_GREEN, font=Font(color="006100")))
    b.ws[COV].conditional_formatting.add("B8", CellIsRule(operator="equal", formula=['"ERROR"'], fill=FILL_RED, font=Font(color="9C0006")))
    b.put(COV, 10, 1, "Decision brief", "sect", fill="sect")
    brief = [
        ("Decision", "Whether the investor should commit as an LP to an (illustrative) develop-and-flip RTB BESS fund, and at what expected return."),
        ("Reframe", "The fund sells RTB before construction — MERCHANT RISK PASSES TO THE BUYER. The fund's risk is the survival curve (approve→connect→sell) + the RTB price."),
        ("Outputs", "Investor IRR & MOIC by scenario, First-Chicago expected return, per-pipeline valuation range, sensitivities."),
        ("Detail / horizon", "Annual, ~2+1-year term, AUD, $m."),
        ("Out of scope", "Post-sale operating/merchant cash flows, construction (buyer-funded), tax structuring, FX, debt."),
    ]
    for i, (k, v) in enumerate(brief):
        r = 11 + i
        b.put(COV, r, 1, k, "label", bold=True)
        b.put(COV, r, 2, v, "label", wrap=True)
    b.put(COV, 17, 1, "Standards followed", "sect", fill="sect")
    b.put(COV, 18, 2, "FAST / ICAEW / Macabacus / Operis: Inputs→Calcs→Outputs zones; one Timeline; one-row-one-calc; no hardcodes in "
                      "formulas; CHOOSE scenario switch + live-case row; checks built alongside; colour code (blue input / black formula / "
                      "green link); INDEX-MATCH not VLOOKUP; IFERROR on division; closed-form IRR (no volatile functions).", "label", wrap=True)
    b.ws[COV].merge_cells("B18:B21")
    b.put(COV, 23, 1, "Judgement inputs to OWN (review pass)", "sect", fill="sect")
    b.put(COV, 24, 2, "Discount rate & premium • the THREE scenario success rates (vs the independent ~45%) • RTB $/MW by state (need "
                      "independent comps) • dev cost per project & abandonment • fees/carry/hurdle • cash-flow profile. the manager's figures are "
                      "CLAIMS to verify — defend your own.", "label", wrap=True)
    b.ws[COV].merge_cells("B24:B27")
    b.put(COV, 29, 1, "TO COMPLETE (analyst review pass)", "sect", fill="sect")
    b.put(COV, 30, 2, "1. Trace every formula + colour audit; confirm master check = OK; stress the switch in all 3 positions.  "
                      "2. Replace 🟡 BENCHMARK / manager-claim inputs with verified independent values (RTB comps, per-state success, dev cost).  "
                      "3. Stress a downside where RTB prices are 20–30% lower and success ≈ the independent ~45%; confirm capital can be lost.", "label", wrap=True)
    b.ws[COV].merge_cells("B30:B33")
    b.put(COV, 35, 1, "DISCLAIMER", "label", bold=True)
    b.put(COV, 35, 2, "ILLUSTRATIVE fund built from public benchmark data; an INDEPENDENT rebuild of the the manager's projections (not an "
                      "endorsement). NOT investment advice. Wholesale-investor context; read the IM. All figures illustrative and must be "
                      "independently verified. Capital is at risk.", "disc", wrap=True)
    b.ws[COV].merge_cells("B35:B38")

    # =====================================================================
    # CONTENTS
    # =====================================================================
    b.width(CON, {"A": 6, "B": 28, "C": 60})
    b.put(CON, 1, 1, "Contents", "title")
    b.header(CON, 3, ["#", "Sheet", "Purpose"])
    purposes = {
        COV: "Title, decision brief, master check, disclaimer", CON: "This page",
        CL: "Version history", INP: "All assumptions + imported data (blue)",
        TL: "Master timeline (built once)", SCN: "Scenarios + switch (DA gate) + live case + weights",
        SURV: "Separate gates; flip success = DA × connection × sale + flag",
        RNPV: "Per-project risk-adjusted NAV (RTB − dev cost)",
        FUND: "Funnel, fees, investor IRR/MOIC (live)",
        RET: "Investor IRR/MOIC by scenario, First-Chicago, valuation range",
        CC: "$/MW benchmark, VC method, RTB vs built",
        SENS: "Investor MOIC grid (development approval × price)",
        CHK: "Integrity checks + master check", DSH: "One-page IC summary", SG: "Sources + glossary",
    }
    for i, name in enumerate(ORDER):
        r = 4 + i
        b.put(CON, r, 1, i + 1, "label", align="center")
        cell = b.put(CON, r, 2, name, "link")
        cell.hyperlink = f"#'{name}'!A1"
        b.put(CON, r, 3, purposes.get(name, ""), "note")

    # =====================================================================
    # CHANGE LOG
    # =====================================================================
    b.width(CL, {"A": 14, "B": 10, "C": 62, "D": 20})
    b.put(CL, 1, 1, "Change Log", "title")
    b.header(CL, 3, ["Date", "Version", "Change", "Author"])
    b.put(CL, 4, 1, a["meta"]["as_at"], "input", align="center")
    b.put(CL, 4, 2, "v1.0", "input", align="center")
    b.put(CL, 4, 3, "Initial build: survival curve, per-project rNPV, fund funnel + fees, investor IRR/MOIC, First-Chicago, cross-checks, sensitivity, checks, dashboard.", "label", wrap=True)
    b.put(CL, 4, 4, "Claude Code (v1 draft)", "input")
    b.put(CL, 5, 3, "[Analyst review pass — record changes here]", "input", wrap=True, fill="yel")

    # =====================================================================
    # SOURCES & GLOSSARY
    # =====================================================================
    b.width(SG, {"A": 40, "B": 14, "C": 14, "D": 50})
    b.put(SG, 1, 1, "Sources & Glossary", "title")
    b.put(SG, 3, 1, "Sources (LIVE = fetched; BENCHMARK = documented public benchmark / the manager claim, verify)", "sect", fill="sect")
    b.header(SG, 4, ["Input", "Status", "As at", "Source"])
    src_rows = [
        ("Risk-free rate (RBA 10yr CGS)", "risk_free"),
        ("Built-cost context (CSIRO GenCost)", "build"),
        ("Dev cost per project", "dev"),
        ("Development-approval prob — public benchmark", "da"),
        ("Grid connection prob (AEMO)", "connection"),
        ("Reach-sale prob (buyer pool / AEMO attrition)", "sale"),
        ("RTB $/MW by state (the manager claim)", "rtb"),
    ]
    rr = 5
    for label, key in src_rows:
        s = inp.sources.get(key)
        b.put(SG, rr, 1, label, "label")
        b.put(SG, rr, 2, s[2] if s else "BENCHMARK", "label", align="center")
        b.put(SG, rr, 3, s[1] if s else "", "label", align="center")
        b.put(SG, rr, 4, s[0] if s else "Illustrative / the manager claim (see config/assumptions.yaml)", "note", wrap=True)
        rr += 1
    b.put(SG, rr + 1, 1, "RTB comps: publicly reported deals only; paid DBs (BNEF, Enerdatics, Mergermarket) out of scope. the manager's prices are claims to verify.", "note", wrap=True)
    gloss_r = rr + 3
    b.put(SG, gloss_r, 1, "Glossary", "sect", fill="sect")
    glossary = [
        ("RTB", "Ready-to-build / development rights — a shovel-ready project sold before construction."),
        ("rNPV", "Risk-adjusted NPV — each cash flow × probability of occurring, then discounted."),
        ("Survival curve / PD", "Cumulative probability a project clears all gates; structurally a multi-period probability-of-default curve."),
        ("Funnel", "projects_started = target ÷ success; you fund dev cost on every started project (full on delivered, partial on dropouts)."),
        ("Carry / hurdle", "GP carried interest (20%) earned only on profit above the LP preferred return (8%)."),
        ("MOIC / IRR", "Multiple on invested capital; annualised return (closed-form over the effective hold)."),
        ("First Chicago", "Probability-weight the scenario returns into a single expected return."),
        ("Develop-and-flip", "Develop, de-risk, then sell RTB — the margin is the value uplift; merchant risk passes to the buyer."),
    ]
    for i, (term, defn) in enumerate(glossary):
        r = gloss_r + 1 + i
        b.put(SG, r, 1, term, "label", bold=True)
        b.put(SG, r, 4, defn, "note", wrap=True)

    # back-to-contents links + freeze panes
    for name in ORDER:
        if name != CON:
            c = b.ws[name].cell(row=1, column=10, value="↩ Contents")
            c.font = F_LINK
            c.hyperlink = f"#'{CON}'!A1"
        b.ws[name].freeze_panes = "A4" if name not in (COV, CON, DSH) else "A2"

    # --- mandatory formula-quality scan (calc + output + control sheets) ---
    import re as _re
    long_hits, nested_hits = [], []
    for name in [TL, SCN, SURV, RNPV, FUND, RET, CC, SENS, CHK]:
        for row in b.ws[name].iter_rows():
            for c in row:
                v = c.value
                if isinstance(v, str) and v.startswith("="):
                    if len(v) > 100:
                        long_hits.append(f"{name}!{c.coordinate} ({len(v)} chars)")
                    if len(_re.findall(r"(?<!ERROR)\bIF\(", v)) >= 2:
                        nested_hits.append(f"{name}!{c.coordinate}")

    out = io.PROJECT_ROOT / "financial_models" / "BESS_Valuation.xlsx"
    out.parent.mkdir(parents=True, exist_ok=True)
    b.wb.save(out)
    print(f"[build_model] wrote {out}")
    if long_hits or nested_hits:
        print(f"[build_model] FORMULA SCAN FAILED — long: {long_hits[:8]}  nested IF: {nested_hits[:8]}")
    else:
        print("[build_model] formula-quality scan PASSED — no long formulas, no nested IFs on any calc sheet")
    return out


if __name__ == "__main__":
    build()
