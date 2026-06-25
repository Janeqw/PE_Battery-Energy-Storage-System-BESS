# =============================================================================
# Battery Developer Valuation — one-command runner
# -----------------------------------------------------------------------------
# Each stage is idempotent and independently runnable.
#   make all  =  extract -> transform -> refresh -> report
# Uses `python` (Windows). On macOS/Linux override:  make PY=python3 all
# =============================================================================

PY ?= python

.PHONY: all install extract transform refresh report test clean help

help:
	@echo "Targets:"
	@echo "  make install     pip install deps (+ playwright browser if used)"
	@echo "  make extract     run src/extract/* -> data/raw + refresh source CSVs"
	@echo "  make transform   clean pipeline, gate statistics, comps -> data/processed"
	@echo "  make refresh     push processed CSV values into the Excel model inputs"
	@echo "  make report      export dashboard.pdf + figures"
	@echo "  make test        pytest"
	@echo "  make all         extract -> transform -> refresh -> report"
	@echo "  make clean       remove data/raw and regenerated outputs"

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

transform:
	$(PY) -m src.transform.clean_pipeline
	$(PY) -m src.transform.gate_statistics
	$(PY) -m src.transform.build_comps

# ---- Phase B: push inputs into the Excel model ------------------------------
refresh:
	$(PY) -m src.refresh_model_inputs

# ---- Phase C: figures + dashboard + GitHub-friendly model preview ----------
report:
	$(PY) -m src.make_report
	$(PY) -m src.export_model_preview

test:
	$(PY) -m pytest -q

all: extract transform refresh report
	@echo "== make all complete: data extracted, model inputs refreshed, report exported =="

clean:
	-rm -rf data/raw/*
	-rm -rf outputs/figures/*
	-rm -f outputs/dashboard.pdf
	@echo "Cleaned data/raw and regenerated outputs (processed CSVs and .xlsx kept)."
