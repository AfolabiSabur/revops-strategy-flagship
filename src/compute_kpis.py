import os, numpy as np, pandas as pd
from util_config import load_config
from validate_schema import validate
cfg = load_config()
os.makedirs("exports", exist_ok=True)
df = validate(pd.read_csv("data/revops_synthetic.csv", parse_dates=["date"]))

is_win  = df["stage"].eq("Closed-Won")
is_loss = df["stage"].eq("Closed-Lost")
is_open = df["status"].eq("open")
revenue_won = df.loc[is_win, "opportunity_value"].sum()
wins, losses = is_win.sum(), is_loss.sum()
win_rate = (wins / (wins + losses)) if (wins + losses) else 0.0

seg = df.groupby("segment").agg(spend=("spend","sum"), wins=("stage", lambda s: (s=="Closed-Won").sum()), acv=("opportunity_value","mean"))
overall_cac = (seg["spend"].sum() / seg["wins"].sum()) if seg["wins"].sum() else float("nan")

overall_acv = df.loc[is_win, "opportunity_value"].mean() if wins else df["opportunity_value"].mean()
ltv_assumption = (overall_acv or 0) * cfg["economics"]["ltv_margin"] * cfg["economics"]["ltv_years"]
payback_months = (overall_cac / ((overall_acv or 1) * cfg["economics"]["ltv_margin"] / 12)) if (overall_cac==overall_cac and overall_acv) else float("nan")

quota = cfg["pipeline"]["quota"]
open_val = df.loc[is_open].groupby("segment")["opportunity_value"].sum()
rep_counts = df.groupby("segment")["rep_id"].nunique()
months = df["date"].dt.to_period("M").nunique()
target = pd.Series({k: rep_counts.get(k,0)*quota[k]*months for k in quota})
coverage_ratio = (open_val.sum() / target.sum()) if target.sum() else float("nan")

df["month"] = df["date"].dt.to_period("M").dt.to_timestamp()
wins_by_month_all = df.loc[is_win].groupby("month")["opportunity_value"].sum().reset_index()
wins_by_month_seg = df.loc[is_win].groupby(["segment","month"])["opportunity_value"].sum().reset_index()
pd.DataFrame([{
    "revenue_won": revenue_won,
    "win_rate": win_rate,
    "cac": overall_cac,
    "ltv_assumption": ltv_assumption,
    "payback_months": payback_months,
    "pipeline_coverage_x": coverage_ratio
}]).to_csv("exports/kpis.csv", index=False)
wins_by_month_all.to_csv("exports/wins_by_month_all.csv", index=False)
wins_by_month_seg.to_csv("exports/wins_by_month_seg.csv", index=False)
print("KPIs computed.")
