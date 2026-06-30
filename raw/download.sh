#!/usr/bin/env bash
# Re-fetch the official source documents that back data/processed/.
# Run locally (needs internet). AEMO blocks the default curl agent, so we send a
# browser User-Agent. The two large PDFs below are gitignored (not committed) to
# keep the repo lean — this script is how you get local copies. News articles and
# the confidential manager deck are NOT fetched here (see raw/README.md).
set -euo pipefail
cd "$(dirname "$0")"
UA="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124 Safari/537.36"

dl() { echo "-> $2"; curl -fSL --max-time 180 -A "$UA" -o "$2" "$1"; }

# RBA F2 Capital Market Yields - Government Bonds - DAILY -> rates.csv
# (Australian Government 10-year bond; row 17-Jun-2026 = 4.776%). The committed copy
# has RBA's trailing blank padding stripped. Use F2 (daily), NOT F2.1 (monthly) -
# the monthly table cannot show the 17-Jun daily reading.
dl "https://www.rba.gov.au/statistics/tables/csv/f2-data.csv" "rba-cgs-10yr-2026-06.csv"

# CSIRO GenCost 2025-26 consultation draft -> costs.csv / stages.build_cost (2-hr battery)
dl "https://www.csiro.au/-/media/Energy/GenCost-2025-26-Draft/GenCost2025-26ConsultDraft_20251216-FINAL.pdf" "csiro-gencost-2025-26.pdf"

# AEMO 2026 Integrated System Plan -> market_demand.csv (storage capacity, Step Change)
dl "https://www.aemo.com.au/-/media/files/major-publications/isp/2026/2026-integrated-system-plan-isp.pdf" "aemo-2026-isp.pdf"

# Not archived automatically (record URL in SOURCES_LOG; fetch by hand if a file copy is needed):
#  - AEMO generator-registration exemption (sub-5 MW): https://www.aemo.com.au/energy-systems/electricity/national-electricity-market-nem/participate-in-the-market/registration/exemption-from-registering-as-a-generator-in-the-nem
#  - CER connections pipeline (attrition): https://cer.gov.au/markets/reports-and-data
echo "Done. See raw/README.md for items that must be fetched manually."
