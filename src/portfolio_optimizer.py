import os, pandas as pd, numpy as np
from util_config import load_config
cfg = load_config()
np.random.seed(9)
plays = pd.DataFrame({
 "play_id":[f"P{i:02d}" for i in range(1,11)],
 "name":["Expand Enterprise Sales","Self-serve Growth","Geographic Expansion","Partner Channel Build","Pricing & Packaging","Reduce Churn Program","New Product A","New Product B","AI Assist for Sales","Marketing Efficiency"],
 "investment":[1.5,0.6,1.0,0.8,0.4,0.5,2.0,1.6,0.7,0.3],
 "npv":[2.4,0.9,1.6,1.2,0.7,0.9,3.2,2.3,1.0,0.5],
 "risk":[0.35,0.20,0.30,0.25,0.20,0.15,0.45,0.40,0.30,0.15]
})
budget = cfg["portfolio"]["budget"]; risk_cap = cfg["portfolio"]["risk_cap"]
plays["ratio"] = plays["npv"]/plays["investment"]
sel=[]; spent=0.0; risk_sum=0.0
for _, r in plays.sort_values("ratio", ascending=False).iterrows():
    if spent + r["investment"] <= budget and risk_sum + r["risk"] <= risk_cap:
        sel.append(r["play_id"]); spent += r["investment"]; risk_sum += r["risk"]
plays["selected"] = plays["play_id"].isin(sel)
os.makedirs("exports", exist_ok=True); plays.to_csv("exports/portfolio_selection.csv", index=False)
print("Portfolio selection saved.")
