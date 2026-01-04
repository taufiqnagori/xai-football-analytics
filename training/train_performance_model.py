import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_squared_error, r2_score
import joblib
import shap

# ------------------------------
# 1. LOAD DATASET
# ------------------------------
df = pd.read_csv(r"C:/Users/USER/Desktop/Football-XAI-suite/data/master_football_xai_dataset.csv")

# ------------------------------
# 2. SELECT FEATURES
# ------------------------------
target = "overall_rating"

features = [
    "age", "nationality", "club_name", "position",
    "matches_played", "minutes_played",
    "goals", "assists", "shots_on_target",
    "pass_accuracy",
    "dribbles_completed", "dribble_success_rate",
    "tackles", "interceptions",
    "stamina_score", "sprint_speed"
]

X = df[features]
y = df[target]

# ------------------------------
# 3. PREPROCESSING PIPELINE
# ------------------------------
numeric_features = [
    "age", "matches_played", "minutes_played",
    "goals", "assists", "shots_on_target",
    "pass_accuracy",
    "dribbles_completed", "dribble_success_rate",
    "tackles", "interceptions",
    "stamina_score", "sprint_speed"
]

categorical_features = ["nationality", "club_name", "position"]

preprocessor = ColumnTransformer(
    transformers=[
        ("num", StandardScaler(), numeric_features),
        ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_features)
    ]
)

# ------------------------------
# 4. BUILD MODEL PIPELINE
# ------------------------------
model = Pipeline(steps=[
    ("preprocessor", preprocessor),
    ("regressor", RandomForestRegressor(
        n_estimators=250,
        random_state=42
    ))
])

# ------------------------------
# 5. TRAIN/TEST SPLIT
# ------------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

# ------------------------------
# 6. TRAIN MODEL
# ------------------------------
model.fit(X_train, y_train)

# ------------------------------
# 7. EVALUATE MODEL
# ------------------------------
y_pred = model.predict(X_test)

rmse = np.sqrt(mean_squared_error(y_test, y_pred))
r2 = r2_score(y_test, y_pred)

print("\nMODEL PERFORMANCE")
print("----------------------")
print(f"RMSE: {rmse:.2f}")
print(f"R² Score: {r2:.3f}")

# ------------------------------
# 8. SAVE MODEL FILES
# ------------------------------
joblib.dump(model, r"C:/Users/USER/Desktop/Football-XAI-suite/models/performance_model.pkl")
print("Saved: ../models/performance_model.pkl")

# ------------------------------
# 9. SAVE SHAP EXPLAINER
# ------------------------------
preprocessed_X = model.named_steps["preprocessor"].transform(X_train)

# Convert sparse matrix to dense for SHAP
if hasattr(preprocessed_X, "toarray"):
    preprocessed_X = preprocessed_X.toarray()

explainer = shap.Explainer(model.named_steps["regressor"], preprocessed_X)
joblib.dump(explainer, r"C:/Users/USER/Desktop/Football-XAI-suite/models/shap_explainer_performance.pkl")
print("Saved: models/shap_explainer_performance.pkl")
