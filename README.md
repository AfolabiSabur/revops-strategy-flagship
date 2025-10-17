# revops-strategy-flagship (synthetic)

https://afolabisabur.github.io/revops-strategy-flagship/

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Release](https://img.shields.io/github/v/release/AfolabiSabur/revops-strategy-flagship?display_name=tag)](../../releases)

 **Downloads:** see the latest [Release]https://github.com/AfolabiSabur/revops-strategy-flagship/releases/download/v0.1.0/strategy_flagship_pack.zip

End-to-end **Revenue Operations (RevOps)** + **Corporate Development (Corp Dev)** demo:
data → metrics → scenarios → M&A → portfolio → **one-page HTML report**.

All data is synthetic. Assumptions live in `config.yaml`.

## Quick start
```bash
python run.py


Run order:
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
  <img src="docs/shot_funnel.png" width="45%">
  <img src="docs/shot_cac_ltv.png" width="45%">
</p>
<p>
  <img src="docs/shot_scenarios.png" width="60%">
</p>


