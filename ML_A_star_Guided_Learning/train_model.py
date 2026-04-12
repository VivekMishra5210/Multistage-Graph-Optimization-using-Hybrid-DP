import pandas as pd
from sklearn.ensemble import RandomForestRegressor
import joblib


data = pd.read_csv("dataset.csv")
X = data[
    ["stage", "out_degree", "min_edge_weight", "avg_edge_weight"]
]
y = data["target_cost"]

print("Dataset loaded")
print("Total samples:", len(data))

model = RandomForestRegressor(
    n_estimators=200,
    max_depth=20,
    random_state=42
)

print("\nTraining Random Forest model...")
model.fit(X, y)
print("Training complete")
joblib.dump(model, "rf_model.pkl")
print("\nModel saved as rf_model.pkl")