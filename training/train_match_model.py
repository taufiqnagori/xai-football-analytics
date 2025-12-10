import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder, LabelEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, confusion_matrix
import joblib
import shap

# -----------------------------------------
# 1. LOAD DATASET
# -----------------------------------------
df = pd.read_csv(r"C:/Users/USER/Desktop/Football-XAI-suite/data/master_football_xai_dataset.csv")

# -----------------------------------------
# 2. SELECT FEATURES FOR MATCH OUTCOME MODEL
# -----------------------------------------
target = "match_result"

features = [
    "team_strength_rating",
    "opponent_strength_rating",
    "possession_pct",
    "goals_scored_team",
    "goals_conceded_team"
]

X = df[features]
y = df[target]

# Encode target labels (Loss=0, Draw=1, Win=2)
label_encoder = LabelEncoder()
y_encoded = label_encoder.fit_transform(y)

# -----------------------------------------
# 3. PREPROCESSING PIPELINE
# -----------------------------------------
numeric_features = features  # all features are numeric

preprocessor = ColumnTransformer(
    transformers=[
        ("num", StandardScaler(), numeric_features),
    ]
)

# -----------------------------------------
# 4. MODEL PIPELINE
# -----------------------------------------
model = Pipeline(steps=[
    ("preprocessor", preprocessor),
    ("classifier", RandomForestClassifier(
        n_estimators=300,
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

print("\nMATCH OUTCOME MODEL PERFORMANCE")
print("------------------------------------")
print(classification_report(y_test, y_pred, target_names=label_encoder.classes_.tolist()))

print("\nConfusion Matrix:")
print(confusion_matrix(y_test, y_pred))

# -----------------------------------------
# 8. SAVE MODEL + LABEL ENCODER
# -----------------------------------------
joblib.dump(model, r"C:/Users/USER/Desktop/Football-XAI-suite/models/match_outcome_model.pkl")
joblib.dump(label_encoder, r"C:/Users/USER/Desktop/Football-XAI-suite/models/match_label_encoder.pkl")

print("\nSaved: match_outcome_model.pkl")
print("Saved: match_label_encoder.pkl")

# -----------------------------------------
# 9. SHAP EXPLAINER
# -----------------------------------------
X_processed = model.named_steps["preprocessor"].transform(X_train)

# Convert sparse→dense if required
if hasattr(X_processed, "toarray"):
    X_processed = X_processed.toarray()

explainer = shap.Explainer(model.named_steps["classifier"], X_processed)

joblib.dump(explainer, r"C:/Users/USER/Desktop/Football-XAI-suite/models/shap_explainer_match.pkl")
print("Saved: shap_explainer_match.pkl")
