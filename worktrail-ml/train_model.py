import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error
import joblib

df = pd.read_csv("worker_features.csv")

# Turn archetype into a numeric target score - this is our "ground truth" for training
df["target_score"] = (
    df["attendance_rate"] * 60 +                          # attendance matters most
    (df["tenure_days"] / df["tenure_days"].max()) * 25 +   # tenure matters some
    (df["num_sites"] / df["num_sites"].max()) * 15         # site diversity matters least
)

feature_cols = ["attendance_rate", "tenure_days", "num_sites", "total_days_logged"]
X = df[feature_cols]          # the inputs
y = df["target_score"]        # what we want to predict

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)
predictions = model.predict(X_test)
mae = mean_absolute_error(y_test, predictions)
print(f"Mean Absolute Error: {mae:.2f}")
joblib.dump(model, "reliability_model.pkl")
print("Model saved to reliability_model.pkl")
import numpy as np

# Sanity check: reliable worker profile
reliable_worker = pd.DataFrame([{
    "attendance_rate": 0.95,
    "tenure_days": 180,
    "num_sites": 3,
    "total_days_logged": 155
}])

# Sanity check: unreliable worker profile
unreliable_worker = pd.DataFrame([{
    "attendance_rate": 0.40,
    "tenure_days": 14,
    "num_sites": 1,
    "total_days_logged": 10
}])

print("Reliable worker predicted score:", model.predict(reliable_worker)[0])
print("Unreliable worker predicted score:", model.predict(unreliable_worker)[0])
importances = pd.Series(model.feature_importances_, index=feature_cols)
print("\nFeature importance:")
print(importances.sort_values(ascending=False))
