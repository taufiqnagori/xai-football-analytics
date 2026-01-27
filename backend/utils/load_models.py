import joblib
import pandas as pd
from pathlib import Path
from backend.config import MODEL_PATHS, DATASET_PATH

def load_all_models(app):
    """
    Load all models, explainers, and dataset into FastAPI app state
    """
    print("Loading dataset and models...")
    
    # Load dataset
    app.state.dataset = pd.read_csv(DATASET_PATH)
    print(f"Dataset loaded: {len(app.state.dataset)} rows")
    
    # Load performance model
    if MODEL_PATHS["performance_model"].exists():
        app.state.performance_model = joblib.load(MODEL_PATHS["performance_model"])
        print("Performance model loaded")
    else:
        raise FileNotFoundError(f"Performance model not found at {MODEL_PATHS['performance_model']}")
    
    # Load performance SHAP explainer
    shap_perf_path = Path(__file__).resolve().parent.parent.parent / "models" / "shap_explainer_performance.pkl"
    if shap_perf_path.exists():
        app.state.performance_explainer = joblib.load(shap_perf_path)
        print("Performance SHAP explainer loaded")
    else:
        app.state.performance_explainer = None
        print("Performance SHAP explainer not found")
    
    # Load performance features
    perf_features_path = Path(__file__).resolve().parent.parent.parent / "models" / "performance_features.pkl"
    if perf_features_path.exists():
        app.state.performance_features = joblib.load(perf_features_path)
    else:
        app.state.performance_features = ["minutes_played", "goals", "assists", "passes", "shots", "tackles", "matches_played", "age"]
    
    # Load injury model
    if MODEL_PATHS["injury_model"].exists():
        app.state.injury_model = joblib.load(MODEL_PATHS["injury_model"])
        print("Injury model loaded")
    else:
        raise FileNotFoundError(f"Injury model not found at {MODEL_PATHS['injury_model']}")
    
    # Load injury SHAP explainer
    shap_injury_path = Path(__file__).resolve().parent.parent.parent / "models" / "shap_explainer_injury.pkl"
    if shap_injury_path.exists():
        app.state.injury_explainer = joblib.load(shap_injury_path)
        print("Injury SHAP explainer loaded")
    else:
        app.state.injury_explainer = None
        print("Injury SHAP explainer not found")
    
    # Load injury features
    injury_features_path = Path(__file__).resolve().parent.parent.parent / "models" / "injury_features.pkl"
    if injury_features_path.exists():
        app.state.injury_features = joblib.load(injury_features_path)
    else:
        app.state.injury_features = ["age", "minutes_played", "matches_played", "injuries_last_season"]
    
    # Load match model
    if MODEL_PATHS["match_model"].exists():
        app.state.match_model = joblib.load(MODEL_PATHS["match_model"])
        print("Match model loaded")
    else:
        raise FileNotFoundError(f"Match model not found at {MODEL_PATHS['match_model']}")
    
    # Load match SHAP explainer
    shap_match_path = Path(__file__).resolve().parent.parent.parent / "models" / "shap_explainer_match.pkl"
    if shap_match_path.exists():
        app.state.match_explainer = joblib.load(shap_match_path)
        print("Match SHAP explainer loaded")
    else:
        app.state.match_explainer = None
        print("Match SHAP explainer not found")
    
    # Load match features
    match_features_path = Path(__file__).resolve().parent.parent.parent / "models" / "match_features.pkl"
    if match_features_path.exists():
        app.state.match_features = joblib.load(match_features_path)
    else:
        app.state.match_features = [
            "team_a_avg_performance", "team_a_avg_injury_risk", "team_a_total_goals",
            "team_a_total_assists", "team_a_total_passes",
            "team_b_avg_performance", "team_b_avg_injury_risk", "team_b_total_goals",
            "team_b_total_assists", "team_b_total_passes"
        ]
    
    print("All models loaded successfully!")
