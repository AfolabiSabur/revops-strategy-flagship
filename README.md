# revops-strategy-flagship (synthetic)

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
