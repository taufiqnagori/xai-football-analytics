import pandas as pd
from fastapi import APIRouter, Request

from backend.schemas.performance_request import PerformanceRequest
from backend.utils.shap_helpers import (
    get_shap_top_features,
    format_key_factors,
    extract_feature_importance
)

# --------------------------------------------------
# Router MUST be defined before usage
# --------------------------------------------------
performance_router = APIRouter()


@performance_router.get("/players")
def get_players(request: Request):
    """
    Returns unique player names for dropdown
    """
    df = request.app.state.dataset
    return sorted(df["player_name"].dropna().unique().tolist())


@performance_router.post("/predict")
def predict_performance(payload: PerformanceRequest, request: Request):
    """
    Predicts player performance and returns SHAP explanation
    """
    df = request.app.state.dataset
    model = request.app.state.performance_model
    explainer = request.app.state.performance_explainer

    player_name = payload.player_name
    player = df[df["player_name"] == player_name]

    if player.empty:
        return {"error": "Player not found"}

    # --------------------------------------------------
    # FEATURE PREPARATION (FINAL – SHAP SAFE)
    # --------------------------------------------------
    if hasattr(model, "feature_names_in_"):
        feature_names = [
            col
            for col in model.feature_names_in_
            if col in player.columns and pd.api.types.is_numeric_dtype(player[col])
        ]
    else:
        feature_names = player.select_dtypes(include="number").columns.tolist()

    X = player[feature_names]

    # --------------------------------------------------
    # Prediction
    # --------------------------------------------------
    prediction = float(model.predict(X)[0])

    # --------------------------------------------------
    # SHAP Explanation
    # --------------------------------------------------
    shap_list = get_shap_top_features(
        explainer=explainer,
        model_input=X,
        feature_names=feature_names,
        top_k=5
    )

    return {
        "player": player_name,
        "predicted_performance": prediction,
        "explanation": {
            "top_features": extract_feature_importance(shap_list),
            "key_factors": format_key_factors(shap_list)
        }
    }
