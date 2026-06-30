# =============================================================================
# Battery Developer Valuation — one-command runner
# -----------------------------------------------------------------------------
# Each stage is idempotent and independently runnable.
#   make all  =  extract -> transform -> refresh -> report
# Uses `python` (Windows). On macOS/Linux override:  make PY=python3 all
# =============================================================================

PY ?= python

.PHONY: all install extract transform build-source refresh rebuild-master report test clean help

help:
	@echo "Targets:"
	@echo "  make install         pip install deps (+ playwright browser if used)"
	@echo "  make extract         run src/extract/* -> data/raw + refresh source CSVs"
	@echo "  make transform       clean pipeline, gate statistics, comps -> data/processed"
	@echo "  make build-source    regenerate INPUTS_AND_ASSUMPTIONS.xlsx (Inputs from data/raw, Assumptions from config)"
	@echo "  make refresh         push refreshed CSV inputs into the master's INPUT cells (--write-master)"
	@echo "  make rebuild-master  regenerate the hand-owned master workbook from Python (overwrites it)"
	@echo "  make report          export dashboard.pdf + figures"
	@echo "  make test            pytest (recomputes the numbers + checks the model ties to the engine)"
	@echo "  make all             extract -> transform -> report (master is hand-owned; not touched)"
	@echo "  make clean           remove data/raw and regenerated outputs"
	@echo "  Build order:         extract -> transform -> build-source -> rebuild-master"

install:
	$(PY) -m pip install -r requirements.txt
	-$(PY) -m playwright install chromium

# ---- Phase A: data pipeline -------------------------------------------------
extract:
	$(PY) -m src.extract.rba
	$(PY) -m src.extract.csiro_gencost
	$(PY) -m src.extract.aemo_generation_info
	$(PY) -m src.extract.aemo_connections
	$(PY) -m src.extract.nsw_planning
	$(PY) -m src.extract.trade_press_comps
	$(PY) -m src.extract.market_demand

transform:
	$(PY) -m src.transform.clean_pipeline
	$(PY) -m src.transform.gate_statistics
	$(PY) -m src.transform.build_comps

# ---- Source workbook (change15): the model's Power Query feed --------------
# Regenerate financial_models/INPUTS_AND_ASSUMPTIONS.xlsx — Inputs (sourced, from
# data/raw/) + Assumptions (judgement, from config/assumptions.yaml). The model links
# to it via Power Query; `make rebuild-master` snapshots it into the Raw_* feed tabs.
build-source:
	$(PY) -m src.build_source_workbook

# ---- Phase B: refresh inputs (Excel-first: master is hand-owned) ------------
# Explicitly push the latest processed CSV values into the master's INPUT cells
# (formulas are never touched). Kept OUT of `make all` so the pipeline never
# silently writes the hand-owned master.
refresh:
	$(PY) -m src.refresh_model_inputs --write-master

# Escape hatch: regenerate the hand-owned master from Python (overwrites it).
# Use only to re-baseline the master; normally you edit the master by hand.
rebuild-master:
	$(PY) -m src.build_model --rebuild-master

# ---- Phase C: figures + dashboard + GitHub-friendly model preview ----------
report:
	$(PY) -m src.make_report
	$(PY) -m src.export_model_preview

test:
	$(PY) -m pytest -q

all: extract transform report
	@echo "== make all complete: data extracted & transformed, report exported (master untouched) =="

clean:
	-rm -rf data/raw/*
	-rm -rf outputs/figures/*
	-rm -f outputs/dashboard.pdf
	@echo "Cleaned data/raw and regenerated outputs (processed CSVs and .xlsx kept)."
