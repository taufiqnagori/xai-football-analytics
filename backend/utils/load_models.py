import joblib
import backend.config as config
import os

# -----------------------------------------------------------
# FUNCTION: Load a file safely
# -----------------------------------------------------------
def safe_load(filepath, name="file"):
    if not os.path.exists(filepath):
        print(f"❌ ERROR: {name} not found at: {filepath}")
        return None
    print(f"✔ Loaded {name} from: {filepath}")
    return joblib.load(filepath)


# -----------------------------------------------------------
# LOAD ALL MODELS + SHAP EXPLAINERS + LABEL ENCODERS
# -----------------------------------------------------------
def load_all_models():
    print("Loading all models and explainers...")

    # -------------------------------
    # PERFORMANCE MODEL
    # -------------------------------
    performance_model = safe_load(
        config.PERFORMANCE_MODEL_PATH, 
        "Performance Model"
    )

    performance_explainer = safe_load(
        config.PERFORMANCE_EXPLAINER_PATH,
        "Performance SHAP Explainer"
    )

    # -------------------------------
    # INJURY RISK MODEL
    # -------------------------------
    injury_model = safe_load(
        config.INJURY_MODEL_PATH,
        "Injury Risk Model"
    )

    injury_label_encoder = safe_load(
        config.INJURY_LABEL_ENCODER_PATH,
        "Injury Label Encoder"
    )

    injury_explainer = safe_load(
        config.INJURY_EXPLAINER_PATH, 
        "Injury SHAP Explainer"
    )

    # -------------------------------
    # MATCH OUTCOME MODEL
    # -------------------------------
    match_model = safe_load(
        config.MATCH_MODEL_PATH,
        "Match Outcome Model"
    )

    match_label_encoder = safe_load(
        config.MATCH_LABEL_ENCODER_PATH,
        "Match Label Encoder"
    )

    match_explainer = safe_load(
        config.MATCH_EXPLAINER_PATH,
        "Match SHAP Explainer"
    )

    # RETURN EVERYTHING IN ONE OBJECT
    print("✔ All models and explainers loaded successfully")

    return {
        "performance_model": performance_model,
        "performance_explainer": performance_explainer,

        "injury_model": injury_model,
        "injury_label_encoder": injury_label_encoder,
        "injury_explainer": injury_explainer,

        "match_model": match_model,
        "match_label_encoder": match_label_encoder,
        "match_explainer": match_explainer,
    }
