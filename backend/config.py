import os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

DATASET_PATH = os.path.join(BASE_DIR, "data", "master_football_xai_dataset.csv")

MODEL_DIR = os.path.join(BASE_DIR, "models")

# -----------------------------------------------------------
# MODEL PATHS (Performance, Injury, Match)
# -----------------------------------------------------------
MODEL_PATHS = {
    "performance_model": "models/performance_model.pkl",
    "performance_explainer": "models/shap_explainer_performance.pkl",

    "injury_model": "models/injury_risk_model.pkl",
    "injury_label_encoder": "models/injury_label_encoder.pkl",
    "injury_explainer": "models/shap_explainer_injury.pkl",

    "match_model": "models/match_outcome_model.pkl",
    "match_label_encoder": "models/match_label_encoder.pkl",
    "match_explainer": "models/shap_explainer_match.pkl",
}

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
