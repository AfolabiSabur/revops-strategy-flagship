import os, numpy as np, pandas as pd
import matplotlib; matplotlib.use("Agg")
import matplotlib.pyplot as plt
from validate_schema import validate

os.makedirs("charts", exist_ok=True)
df = validate(pd.read_csv("data/revops_synthetic.csv", parse_dates=["date"]))

funnel_order = ["MQL","SAL","SQL","Proposal","Commit","Closed-Won","Closed-Lost"]
stage_counts = df["stage"].value_counts().reindex(funnel_order).fillna(0)
plt.figure(); stage_counts.head(6).plot(kind="bar"); plt.title("Funnel counts"); plt.ylabel("Count"); plt.xlabel("Stage"); plt.tight_layout(); plt.savefig("charts/funnel.png"); plt.close()

by_chan = df.groupby("channel").agg(leads=("leads","sum"), sql=("stage", lambda s: (s=="SQL").sum()))
by_chan["sql_rate"] = by_chan["sql"]/by_chan["leads"].replace(0, np.nan)
plt.figure(); by_chan["sql_rate"].sort_values(ascending=False).plot(kind="bar"); plt.title("Conversion to SQL by channel"); plt.ylabel("SQL / lead"); plt.xlabel("Channel"); plt.tight_layout(); plt.savefig("charts/conversion_by_channel.png"); plt.close()

seg = df.groupby("segment").agg(spend=("spend","sum"), wins=("stage", lambda s: (s=="Closed-Won").sum()), acv=("opportunity_value","mean"))
seg["CAC"] = seg["spend"]/(seg["wins"].replace(0, np.nan))
seg["LTV"] = seg["acv"]*0.75*3
plt.figure(); seg[["CAC","LTV"]].plot(kind="bar"); plt.title("CAC vs LTV by segment"); plt.tight_layout(); plt.savefig("charts/cac_vs_ltv_by_segment.png"); plt.close()

quota = {"SMB":120000,"Mid-Market":300000,"Enterprise":900000}
open_opp = df[df["status"]=="open"]
coverage = open_opp.groupby("segment")["opportunity_value"].sum()
rep_counts = df.groupby("segment")["rep_id"].nunique()
months = df["date"].dt.to_period("M").nunique()
target = pd.Series({k: rep_counts.get(k,0)*quota[k]*months for k in quota})
pipe_cov = (coverage/target).replace([np.inf, np.nan], 0)
plt.figure(); pipe_cov.plot(kind="bar"); plt.title("Pipeline coverage vs target by segment"); plt.ylabel("x coverage"); plt.tight_layout(); plt.savefig("charts/pipeline_coverage_by_segment.png"); plt.close()

df["acq_month"] = df["date"].dt.to_period("M").dt.to_timestamp()
win_by_month = df.groupby("acq_month", group_keys=False)["stage"].apply(lambda s: (s=="Closed-Won").sum())
lead_by_month = df.groupby("acq_month")["leads"].sum()
realization = (win_by_month/lead_by_month.replace(0, np.nan)).fillna(0).sort_index()
plt.figure(); realization.plot(marker="o"); plt.title("Cohort realization: Leads to Wins by acquisition month"); plt.ylabel("Win / Lead"); plt.xlabel("Acquisition month"); plt.tight_layout(); plt.savefig("charts/cohort_realization_curve.png"); plt.close()
print("Charts written.")
