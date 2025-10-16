@echo off
setlocal
python -m pip install --upgrade pip >nul 2>&1
python -m pip install -r requirements.txt
python src\generate_data.py
python src\build_charts.py
python src\scenario_planner.py
python src\deal_model.py
python src\portfolio_optimizer.py
python src\compute_kpis.py
python src\build_sparklines.py
python src\build_report.py
python src\build_zip.py
echo Opening report...
powershell -NoProfile -Command "Invoke-Item 'exports\flagship_strategy_report.html'"
