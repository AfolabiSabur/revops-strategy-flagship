import pandas as pd

# Simple, built-in schema checks (no external libraries)
EXPECTED_COLS = [
    "date","account_id","segment","region","industry","product","channel",
    "spend","impressions","clicks","leads","stage","opportunity_value",
    "rep_id","cycle_days","status","renewal_flag","expansion_value"
]

ENUMS = {
    "segment": {"SMB","Mid-Market","Enterprise"},
    "region": {"NA","EMEA","APAC","LATAM"},
    "product": {"Core","Add-on A","Add-on B"},
    "channel": {"paid_search","paid_social","events","outbound","referral","partner"},
    "stage": {"MQL","SAL","SQL","Proposal","Commit","Closed-Won","Closed-Lost"},
    "status": {"open","closed"},
    "renewal_flag": {0,1},
}

NUMERIC_NONNEG = {"spend","impressions","clicks","leads","opportunity_value","cycle_days","expansion_value"}

def validate(df: pd.DataFrame) -> pd.DataFrame:
    # 1) Columns present?
    missing = [c for c in EXPECTED_COLS if c not in df.columns]
    if missing:
        raise ValueError(f"Missing required columns: {missing}")

    # 2) Coerce date
    df["date"] = pd.to_datetime(df["date"], errors="raise")

    # 3) Basic non-negatives
    for c in NUMERIC_NONNEG:
        if (df[c] < 0).any():
            raise ValueError(f"Column '{c}' has negative values.")

    # 4) Enum checks (ignore NaNs)
    for col, allowed in ENUMS.items():
        bad = df[col].dropna().astype(str)
        bad = bad[~bad.isin([str(x) for x in allowed])]
        if len(bad) > 0:
            # Keep going but raise a clear error to help mapping
            sample = list(bad.unique())[:5]
            raise ValueError(f"Unexpected values in '{col}': {sample}. Expected one of {sorted(allowed)}")

    return df
