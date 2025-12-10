import os

# -----------------------------------------------------------
# BASE PROJECT PATH (change this only if your folder moves)
# -----------------------------------------------------------
BASE_DIR = r"C:/Users/USER/Desktop/Football-XAI-suite"

# -----------------------------------------------------------
# DATASET PATH
# -----------------------------------------------------------
DATASET_PATH = os.path.join(BASE_DIR, "data", "master_football_xai_dataset.csv")

# -----------------------------------------------------------
# MODEL PATHS (Performance, Injury, Match)
# -----------------------------------------------------------
PERFORMANCE_MODEL_PATH = os.path.join(BASE_DIR, "models", "performance_model.pkl")
PERFORMANCE_EXPLAINER_PATH = os.path.join(BASE_DIR, "models", "shap_explainer_performance.pkl")

INJURY_MODEL_PATH = os.path.join(BASE_DIR, "models", "injury_risk_model.pkl")
INJURY_LABEL_ENCODER_PATH = os.path.join(BASE_DIR, "models", "injury_label_encoder.pkl")
INJURY_EXPLAINER_PATH = os.path.join(BASE_DIR, "models", "shap_explainer_injury.pkl")

MATCH_MODEL_PATH = os.path.join(BASE_DIR, "models", "match_outcome_model.pkl")
MATCH_LABEL_ENCODER_PATH = os.path.join(BASE_DIR, "models", "match_label_encoder.pkl")
MATCH_EXPLAINER_PATH = os.path.join(BASE_DIR, "models", "shap_explainer_match.pkl")

# -----------------------------------------------------------
# CHECK IF FILES EXIST (Optional but useful)
# -----------------------------------------------------------
def verify_paths():
    required_files = [
        DATASET_PATH,
        PERFORMANCE_MODEL_PATH,
        PERFORMANCE_EXPLAINER_PATH,
        INJURY_MODEL_PATH,
        INJURY_EXPLAINER_PATH,
        INJURY_LABEL_ENCODER_PATH,
        MATCH_MODEL_PATH,
        MATCH_EXPLAINER_PATH,
        MATCH_LABEL_ENCODER_PATH
    ]

    for f in required_files:
        if not os.path.exists(f):
            print(f"❌ MISSING FILE: {f}")
        else:
            print(f"✔ Found: {f}")
