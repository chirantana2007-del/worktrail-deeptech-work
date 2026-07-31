import pandas as pd

df = pd.read_csv("synthetic_attendance.csv")

# Group all rows by worker, so we can summarize each worker's history
grouped = df.groupby("worker_id")

# Build each feature as its own small table (one row per worker)
attendance_rate = grouped["status"].apply(lambda x: (x == "present").sum() / len(x))
tenure_days = grouped["date"].agg(lambda x: (pd.to_datetime(x).max() - pd.to_datetime(x).min()).days)
num_sites = grouped["site"].nunique()
total_days_logged = grouped["date"].count()

# worker_name and archetype are the same for every row of a worker,
# so "first" just grabs that one repeated value instead of summarizing
worker_name = grouped["worker_name"].first()
archetype = grouped["archetype"].first()

# Combine all these separate mini-tables into one final table,
# side by side, matched up by worker_id
features = pd.DataFrame({
    "worker_name": worker_name,
    "attendance_rate": attendance_rate,
    "tenure_days": tenure_days,
    "num_sites": num_sites,
    "total_days_logged": total_days_logged,
    "archetype": archetype  # keep for now, to sanity-check the model later
})

features = features.reset_index()  # turns worker_id from an index back into a normal column
features.to_csv("worker_features.csv", index=False)

print(f"Built features for {len(features)} workers.")
print(features.head())