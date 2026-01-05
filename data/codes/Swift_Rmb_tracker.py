import pandas as pd

# 1) Read excel
df_swift = pd.read_excel("swift_rmb_tracker.xlsx", sheet_name="rmb_tracker")

# 2) Standardize column names
df_swift.columns = (
    df_swift.columns.str.strip().str.lower()
      .str.replace(" ", "_").str.replace("-", "_").str.replace(".", "_")
)

# 3) Ensure date is datetime + month-start (YYYY-MM-01)
df_swift["date"] = pd.to_datetime(df_swift["date"], errors="coerce")
df_swift["date"] = df_swift["date"].dt.to_period("M").dt.to_timestamp()  # month-start

# 4) Coerce numerics
for c in ["rmb_global_share_pct", "rmb_international_share_pct", "rmb_global_rank"]:
    df_swift[c] = pd.to_numeric(df_swift[c], errors="coerce")

# 5) Quality checks
assert df_swift["date"].notna().all(), "date içinde NaT var!"
assert (df_swift["date"].dt.is_month_start).all(), "date month-start değil!"
assert df_swift[["rmb_global_share_pct","rmb_international_share_pct","rmb_global_rank"]].notna().all().all(), "numeric alanlarda NaN var!"

# 6) Save clean csv
out_path = "swift_rmb_tracker_clean.csv"
df_swift.to_csv(out_path, index=False)
print("✅ Saved:", out_path)
print("shape:", df_swift.shape)
print(df_swift.head(3))

