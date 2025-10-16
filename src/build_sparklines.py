import os, pandas as pd
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
os.makedirs("charts/sparklines", exist_ok=True)
all_ = pd.read_csv("exports/wins_by_month_all.csv", parse_dates=["month"])
seg_ = pd.read_csv("exports/wins_by_month_seg.csv", parse_dates=["month"])
plt.figure(figsize=(3,1.2)); all_.set_index("month")["opportunity_value"].astype(float).plot(); plt.xticks([]); plt.yticks([]); plt.tight_layout(); plt.savefig("charts/sparklines/wins_all.png"); plt.close()
for seg, g in seg_.groupby("segment"):
    plt.figure(figsize=(3,1.2)); g.set_index("month")["opportunity_value"].astype(float).plot(); plt.xticks([]); plt.yticks([]); plt.tight_layout(); plt.savefig(f"charts/sparklines/wins_{seg.replace(' ','_').lower()}.png"); plt.close()
print("Sparklines written.")
