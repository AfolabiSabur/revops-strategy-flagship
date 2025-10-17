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

## Screenshots
<p>
  <img src="docs/shot_funnel.png" width="45%">
  <img src="docs/shot_cac_ltv.png" width="45%">
</p>
<p>
  <img src="docs/shot_scenarios.png" width="60%">
</p>

MIT License

Copyright (c) 2025 Sabur A.

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the “Software”), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED “AS IS”, WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
