import os, numpy as np, pandas as pd
np.random.seed(7)
companies=[f"Co{i}" for i in range(1,11)]
segments=["SMB","Mid-Market","Enterprise"]
seg = np.random.choice(segments, size=10, p=[0.4,0.4,0.2])
rev = np.random.uniform(50,600,size=10)*1e6
ev_rev = np.random.uniform(2.0,7.0,size=10)
ev = ev_rev*rev
comp = pd.DataFrame({"company":companies,"segment":seg,"revenue":rev,"ev":ev,"ev_rev":ev_rev})
os.makedirs("exports", exist_ok=True); comp.to_csv("exports/comp_table.csv", index=False)

acq = comp.sample(1, random_state=1).iloc[0]
tgt = comp.sample(1, random_state=2).iloc[0]
purchase_premium, revenue_synergy, cost_synergy, integration_cost, wacc = 0.25, 0.04, 0.02, 0.08, 0.10
combined_rev = acq["revenue"] + tgt["revenue"]
synergy_cashflows=[]
for year in range(1,6):
    cf = combined_rev*(revenue_synergy+cost_synergy)
    if year==1: cf *= 0.6
    if year==2: cf *= 0.85
    if year<=2: cf -= tgt["revenue"]*integration_cost/2.0
    synergy_cashflows.append(cf)
npv = sum(cf/((1+wacc)**i) for i, cf in enumerate(synergy_cashflows, start=1))
purchase_price = tgt["ev"]*(1+purchase_premium)
deal_npv = npv - purchase_price
pd.DataFrame({"metric":["Acquirer_rev","Target_rev","Combined_rev","Purchase_price","Synergy_NPV","Deal_NPV"],"value":[acq["revenue"],tgt["revenue"],combined_rev,purchase_price,npv,deal_npv]}).to_csv("exports/deal_summary.csv", index=False)
print("Deal summary saved.")
