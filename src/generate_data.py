import os, numpy as np, pandas as pd, datetime as dt
from util_config import load_config
cfg = load_config(); np.random.seed(cfg["seed"]); rng = np.random.default_rng(cfg["seed"])
os.makedirs("data", exist_ok=True)

segments = ["SMB","Mid-Market","Enterprise"]
regions = ["NA","EMEA","APAC","LATAM"]
industries = ["SaaS","FinTech","HealthTech","Ecommerce","AI/ML"]
products = ["Core","Add-on A","Add-on B"]
channels = ["paid_search","paid_social","events","outbound","referral","partner"]
stages = ["MQL","SAL","SQL","Proposal","Commit","Closed-Won","Closed-Lost"]

N = 3200
start = (dt.date.today().replace(day=1) - dt.timedelta(days=400))
dates = pd.date_range(start, periods=N, freq="D")
account_ids = [f"A{str(i).zfill(5)}" for i in rng.integers(1, 1500, size=N)]
segment = rng.choice(segments, size=N, p=[0.45,0.35,0.20])
region  = rng.choice(regions,  size=N, p=[0.45,0.25,0.20,0.10])
industry= rng.choice(industries, size=N)
product = rng.choice(products,  size=N, p=[0.65,0.20,0.15])
channel = rng.choice(channels,  size=N, p=[0.28,0.22,0.10,0.20,0.10,0.10])

spend_base = {"paid_search":(2,150),"paid_social":(2,120),"events":(2,500),"outbound":(2,60),"referral":(1,20),"partner":(1,30)}
ctr = {"paid_search":0.035,"paid_social":0.012,"events":0.0,"outbound":0.0,"referral":0.0,"partner":0.0}
cvr = {"paid_search":0.10,"paid_social":0.05,"events":0.25,"outbound":0.07,"referral":0.22,"partner":0.18}
seg_mult = {"SMB":1.15,"Mid-Market":1.0,"Enterprise":0.8}

spend = np.array([rng.gamma(*spend_base[ch]) for ch in channel])
season = 1 + 0.10*np.sin((pd.to_datetime(dates).month/12)*2*np.pi)
spend = spend * season
impressions = (spend * rng.uniform(8,20,size=N)).astype(int)
clicks = np.array([int(impressions[i]*ctr[channel[i]]) for i in range(N)])
leads = []
for i in range(N):
    p = min(0.9, cvr[channel[i]]*seg_mult[segment[i]])
    trials = max(1, clicks[i] if clicks[i]>0 else int(rng.poisson(2)))
    leads.append(rng.binomial(trials, p))
leads = np.array(leads)

stage = rng.choice(stages, size=N, p=[0.40,0.20,0.15,0.10,0.07,0.05,0.03])
acv_map = {"SMB":8000,"Mid-Market":35000,"Enterprise":120000}
prod_mult = {"Core":1.0,"Add-on A":0.25,"Add-on B":0.4}
acv = np.array([acv_map[s]*prod_mult[p] for s,p in zip(segment,product)])
opportunity_value = acv * rng.uniform(0.8,1.2,size=N)

def seg_mu(s): return 45 if s=="SMB" else 75 if s=="Mid-Market" else 120
cycle_days = np.array([int(np.clip(rng.normal(seg_mu(s),15),10,240)) for s in segment])

status = np.where(np.isin(stage,["Closed-Won","Closed-Lost"]),"closed","open")
renewal_flag = rng.choice([0,1], size=N, p=[0.85,0.15])
expansion_value = opportunity_value * rng.choice([0,0.1,0.2,0.3], size=N, p=[0.7,0.2,0.08,0.02])
rep_id = [f"R{r:03d}" for r in rng.integers(1,45,size=N)]

df = pd.DataFrame({
    "date": pd.to_datetime(dates).date,
    "account_id": account_ids, "segment": segment, "region": region, "industry": industry,
    "product": product, "channel": channel, "spend": np.round(spend,2),
    "impressions": impressions, "clicks": clicks, "leads": leads, "stage": stage,
    "opportunity_value": np.round(opportunity_value,2), "rep_id": rep_id,
    "cycle_days": cycle_days, "status": status, "renewal_flag": renewal_flag,
    "expansion_value": np.round(expansion_value,2)
})
tmp = "data/revops_synthetic.csv.tmp"; df.to_csv(tmp, index=False); os.replace(tmp, "data/revops_synthetic.csv")
print("Wrote data/revops_synthetic.csv", len(df))
