import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
from sklearn.preprocessing import LabelEncoder
import joblib
import shap

# -----------------------------------------
# 1. LOAD DATASET
# -----------------------------------------
df = pd.read_csv(r"C:/Users/USER/Desktop/Football-XAI-suite/data/master_football_xai_dataset.csv")

# -----------------------------------------
# 2. SELECT FEATURES FOR INJURY MODEL
# -----------------------------------------
target = "injury_risk_level"

features = [
    "age", "position", "nationality", "club_name",
    "past_injury_count", "training_load_score",
    "average_distance_covered_km", "recovery_time_hours",
    "muscle_strength_score", "stamina_score",
    "minutes_played", "matches_played"
]

X = df[features]
y = df[target]

# Encode target labels (Low=0, Medium=1, High=2)
label_encoder = LabelEncoder()
y_encoded = label_encoder.fit_transform(y)

# -----------------------------------------
# 3. PREPROCESSING PIPELINE
# -----------------------------------------
numeric_features = [
    "age", "past_injury_count", "training_load_score",
    "average_distance_covered_km", "recovery_time_hours",
    "muscle_strength_score", "stamina_score",
    "minutes_played", "matches_played"
]

categorical_features = ["position", "nationality", "club_name"]

preprocessor = ColumnTransformer(
    transformers=[
        ("num", StandardScaler(), numeric_features),
        ("cat", OneHotEncoder(handle_unknown="ignore"), categorical_features)
    ]
)

# -----------------------------------------
# 4. MODEL PIPELINE
# -----------------------------------------
model = Pipeline(steps=[
    ("preprocessor", preprocessor),
    ("classifier", RandomForestClassifier(
        n_estimators=300,
        max_depth=None,
        random_state=42,
        class_weight="balanced"
    ))
])

# -----------------------------------------
# 5. TRAIN/TEST SPLIT
# -----------------------------------------
X_train, X_test, y_train, y_test = train_test_split(
    X, y_encoded, test_size=0.2, random_state=42, stratify=y_encoded
)

# -----------------------------------------
# 6. TRAIN MODEL
# -----------------------------------------
model.fit(X_train, y_train)

# -----------------------------------------
# 7. EVALUATE MODEL
# -----------------------------------------
y_pred = model.predict(X_test)

print("\nINJURY RISK MODEL PERFORMANCE")
print("------------------------------------")
print(classification_report(y_test, y_pred, target_names=label_encoder.classes_.tolist()))

print("\nConfusion Matrix:")
print(confusion_matrix(y_test, y_pred))

# -----------------------------------------
# 8. SAVE MODEL + LABEL ENCODER
# -----------------------------------------
joblib.dump(model, r"C:/Users/USER/Desktop/Football-XAI-suite/models/injury_risk_model.pkl")
joblib.dump(label_encoder, r"C:/Users/USER/Desktop/Football-XAI-suite/models/injury_label_encoder.pkl")

print("\nSaved: injury_risk_model.pkl")
print("Saved: injury_label_encoder.pkl")

# -----------------------------------------
# 9. SHAP EXPLAINER
# -----------------------------------------
X_processed = model.named_steps["preprocessor"].transform(X_train)

# Convert sparse→dense if required
if hasattr(X_processed, "toarray"):
    X_processed = X_processed.toarray()

explainer = shap.Explainer(model.named_steps["classifier"], X_processed)

joblib.dump(explainer, r"C:/Users/USER/Desktop/Football-XAI-suite/models/shap_explainer_injury.pkl")
print("Saved: shap_explainer_injury.pkl")
