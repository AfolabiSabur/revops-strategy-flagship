import os, base64, pandas as pd
def b64(p):
    with open(p,"rb") as f: return "data:image/png;base64," + base64.b64encode(f.read()).decode()
def fmt_money(x): 
    try: return f"${x:,.0f}"
    except: return "–"
def pct(x):    return f"{x*100:,.1f}%" if pd.notnull(x) else "–"
def months(x): return f"{x:,.1f} mo"   if pd.notnull(x) else "–"
k = pd.read_csv("exports/kpis.csv").iloc[0].to_dict()
revenue_won, win_rate, cac = fmt_money(k.get("revenue_won",0)), pct(k.get("win_rate")), fmt_money(k.get("cac"))
ltv, payback = fmt_money(k.get("ltv_assumption",0)), months(k.get("payback_months"))
coverage_x = f"{k.get('pipeline_coverage_x',0):.2f}×" if pd.notnull(k.get('pipeline_coverage_x')) else "–"
charts=[("Funnel counts","charts/funnel.png"),("Conversion to SQL by channel","charts/conversion_by_channel.png"),("CAC vs LTV by segment (Assumption)","charts/cac_vs_ltv_by_segment.png"),("Pipeline coverage vs target by segment","charts/pipeline_coverage_by_segment.png"),("Cohort realization (lead→win)","charts/cohort_realization_curve.png"),("Revenue projection scenarios","charts/revenue_projection_scenarios.png")]
deal, portfolio = "exports/deal_summary.csv", "exports/portfolio_selection.csv"
sparks=[]
for name,path in [("All wins","charts/sparklines/wins_all.png"),("SMB","charts/sparklines/wins_smb.png"),("Mid-Market","charts/sparklines/wins_mid-market.png"),("Enterprise","charts/sparklines/wins_enterprise.png")]:
    if os.path.exists(path): sparks.append((name,path))
STYLE = """
<!doctype html><meta charset='utf-8'><title>RevOps & Corp Dev Report</title>
<meta name="viewport" content="width=device-width, initial-scale=1"/>
<style>
  body{margin:0;font-family:system-ui,Segoe UI,Roboto,Helvetica,Arial,sans-serif;background:#f3f4f6;color:#0f172a}
  .wrap{max-width:1100px;margin:0 auto;padding:24px}
  .hero{background:#fff;border-radius:16px;padding:24px;box-shadow:0 4px 24px rgba(0,0,0,.08)}
  .hero h1{margin:0 0 4px;font-size:28px}
  .hero p{margin:0;color:#374151}
  .kpis{display:grid;grid-template-columns:repeat(6,1fr);gap:12px;margin-top:16px}
  .tile{background:#fff;border:1px solid #e5e7eb;border-radius:12px;padding:12px}
  .tile .label{font-size:12px;color:#6b7280}
  .tile .value{font-weight:700;font-size:18px;margin-top:2px}
  .bluf{margin:16px 0}
  .callout{background:#fff;border:1px solid #e5e7eb;border-radius:12px;padding:12px}
  .grid{display:grid;grid-template-columns:1fr 1fr;gap:16px;margin-top:16px}
  .card{background:#fff;border:1px solid #e5e7eb;border-radius:12px;padding:12px}
  .card img{width:100%;border-radius:10px;border:1px solid #eee}
  h2{margin:16px 0 8px}
  table{width:100%;border-collapse:collapse;font-size:13px}
  th,td{border:1px solid #e5e7eb;padding:8px;text-align:left}
  th{background:#f8fafc}
  .sparks{display:flex;gap:10px;flex-wrap:wrap;margin-top:8px}
  .spark{background:#fff;border:1px solid #e5e7eb;border-radius:12px;padding:8px}
  .spark img{display:block;width:140px;border-radius:8px}
  #printbtn{position:fixed;right:20px;bottom:20px;padding:10px 14px;border:1px solid #e5e7eb;border-radius:10px;background:#fff;cursor:pointer;box-shadow:0 2px 8px rgba(0,0,0,.08);z-index:9999}
</style>"""
BLUF=["Referral/partner channels show the highest SQL conversion in this synthetic run.",
      "Mid-Market pipeline coverage is below 3×; rebalance quotas/spend or accelerate demand.",
      "CAC (Customer Acquisition Cost) remains below LTV (Lifetime Value) across segments (Assumption: LTV = ACV × 0.75 × 3 yrs).",
      "Assumptions: WACC 10% (Weighted Average Cost of Capital), 25% purchase premium, synergy ramp 2 years, portfolio risk cap 1.2."]
html=[STYLE,"<div class='wrap'>","<div class='hero'>",
      "<h1>RevOps & Corp Dev Report <span style='font-weight:400;color:#6b7280'>(Synthetic)</span></h1>",
      "<p>Data → metrics → scenarios → M&A (Mergers & Acquisitions) → portfolio allocation.</p>",
      "<div class='kpis'>",
      f"<div class='tile'><div class='label'>Revenue (Closed-Won)</div><div class='value'>{revenue_won}</div></div>",
      f"<div class='tile'><div class='label'>Win Rate</div><div class='value'>{win_rate}</div></div>",
      f"<div class='tile'><div class='label'>CAC</div><div class='value'>{cac}</div></div>",
      f"<div class='tile'><div class='label'>LTV (Assumption)</div><div class='value'>{ltv}</div></div>",
      f"<div class='tile'><div class='label'>Payback</div><div class='value'>{payback}</div></div>",
      f"<div class='tile'><div class='label'>Pipeline Coverage</div><div class='value'>{coverage_x}</div></div>","</div>"]
if sparks:
    html+=["<div class='sparks'>"]; 
    for name,path in sparks: html+=[f"<div class='spark'><div style='font-size:12px;color:#6b7280;margin-bottom:4px'>{name}</div><img src='{b64(path)}' alt='{name}'/></div>"]
    html+=["</div>"]
html+=["<div class='bluf'><div class='callout'><b>BLUF</b><ul>"]+[f"<li>{x}</li>" for x in BLUF]+["</ul></div></div></div>",
      "<h2>Dashboards</h2>","<div class='grid'>"]
for title,path in charts:
    if os.path.exists(path): html+=[f"<div class='card'><div style='font-weight:600;margin:4px 0 8px'>{title}</div><img src='{b64(path)}' alt='{title}'/></div>"]
html+=["</div>"]
if os.path.exists(deal): html+=["<h2>Deal Model</h2>","<div class='card'>", pd.read_csv(deal).to_html(index=False), "</div>"]
if os.path.exists(portfolio): html+=["<h2>Portfolio Selection</h2>","<div class='card'>", pd.read_csv(portfolio).to_html(index=False), "</div>"]
html+=["<button id='printbtn' onclick='window.print()'>⤓ Save as PDF</button>","</div>"]
os.makedirs("exports", exist_ok=True)
with open("exports/flagship_strategy_report.html","w",encoding="utf-8") as f: f.write("\n".join(html))
print("Report written (flagship layout).")
