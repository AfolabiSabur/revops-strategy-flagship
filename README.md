# revops-strategy-flagship (synthetic)

https://afolabisabur.github.io/revops-strategy-flagship/

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Release](https://img.shields.io/github/v/release/AfolabiSabur/revops-strategy-flagship?display_name=tag)](../../releases)

 **Downloads:** see the latest [Release](../../releases) or direct ZIP: https://github.com/AfolabiSabur/revops-strategy-flagship/releases/download/v0.1.0/strategy_flagship_pack.zip


End-to-end **Revenue Operations (RevOps)** + **Corporate Development (Corp Dev)** demo:
data → metrics → scenarios → M&A → portfolio → **one-page HTML report**.

All data is synthetic. Assumptions live in `config.yaml`.

## Quick start
<details><summary>Run order (for transparency)</summary>

```bash
pip install -r requirements.txt
python src/generate_data.py
python src/build_charts.py
python src/scenario_planner.py
python src/deal_model.py
python src/portfolio_optimizer.py
python src/compute_kpis.py
python src/build_sparklines.py
python src/build_report.py
python src/build_zip.py


## Screenshots
<p>
  <img src="docs/shot_funnel.png" alt="Funnel counts by stage" width="45%">
  <img src="docs/shot_cac_ltv.png" alt="CAC vs LTV by segment" width="45%">
</p>
<p>
  <img src="docs/shot_scenarios.png" alt="Revenue projection scenarios" width="60%">
</p>



