import pandas as pd
import joblib
from pathlib import Path

from backend.config import DATASET_PATH, MODEL_DIR, MODEL_PATHS


def load_all_models(app):
    print("🔄 Loading dataset and models...")

    # -----------------------------
    # 1. Load Dataset
    # -----------------------------
    dataset_path = Path(DATASET_PATH)
    if not dataset_path.exists():
        raise FileNotFoundError(f"Dataset not found at: {dataset_path}")

    app.state.dataset = pd.read_csv(dataset_path)

    # -----------------------------
    # 2. Load Performance Model
    # -----------------------------
    app.state.performance_model = joblib.load(
        Path(MODEL_PATHS["performance_model"])
    )
    app.state.performance_explainer = joblib.load(
        Path(MODEL_PATHS["performance_explainer"])
    )

    # -----------------------------
    # 3. Load Injury Model
    # -----------------------------
    app.state.injury_model = joblib.load(
        Path(MODEL_PATHS["injury_model"])
    )
    app.state.injury_explainer = joblib.load(
        Path(MODEL_PATHS["injury_explainer"])
    )
    app.state.injury_label_encoder = joblib.load(
        Path(MODEL_PATHS["injury_label_encoder"])
    )

    # -----------------------------
    # 4. Load Match Model
    # -----------------------------
    app.state.match_model = joblib.load(
        Path(MODEL_PATHS["match_model"])
    )
    app.state.match_explainer = joblib.load(
        Path(MODEL_PATHS["match_explainer"])
    )
    app.state.match_label_encoder = joblib.load(
        Path(MODEL_PATHS["match_label_encoder"])
    )

    print("✅ Dataset, models, and SHAP explainers loaded successfully")
