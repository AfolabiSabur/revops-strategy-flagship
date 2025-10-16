import os, pandas as pd
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from util_config import load_config
cfg = load_config()

df = pd.read_csv("data/revops_synthetic.csv", parse_dates=["date"])
base_rev = df[df["stage"]=="Closed-Won"].groupby(df["date"].dt.to_period("M"))["opportunity_value"].sum().astype(float)
base_rev.index = base_rev.index.to_timestamp()
months = pd.date_range(base_rev.index.min() if len(base_rev)>0 else "2024-01-01", periods=12, freq="MS")
start  = base_rev.reindex(months, fill_value=0).cumsum().iloc[-1] if len(base_rev)>0 else 0.0

def proj(annual_growth):
    vals=[start]
    for _ in range(11): vals.append(vals[-1]*(1+annual_growth/12.0)+1e5)
    return pd.Series(vals, index=months)

bull = proj(cfg["scenarios"]["bull_growth_annual"])
base = proj(cfg["scenarios"]["base_growth_annual"])
bear = proj(cfg["scenarios"]["bear_growth_annual"])

plt.figure(); bull.plot(label="Bull"); base.plot(label="Base"); bear.plot(label="Bear"); plt.legend(); plt.title("Revenue projection scenarios (synthetic)"); plt.tight_layout()
os.makedirs("charts", exist_ok=True); plt.savefig("charts/revenue_projection_scenarios.png"); plt.close()
os.makedirs("exports", exist_ok=True); pd.DataFrame({"bull":bull,"base":base,"bear":bear}).to_csv("exports/revenue_projection_table.csv")
print("Scenarios saved.")
