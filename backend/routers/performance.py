from fastapi import APIRouter, Request, HTTPException
from backend.data_access import get_player_row
from backend.schemas.performance_request import PerformanceRequest
from backend.utils.shap_helpers import (
    get_shap_top_features,
    format_key_factors,
    extract_feature_importance
)
import pandas as pd
import numpy as np

router = APIRouter(tags=["Performance"])

@router.get("/players")
def get_players(request: Request):
    """
    Returns unique player names for dropdown
    """
    df = request.app.state.dataset
    return sorted(df["player_name"].dropna().unique().tolist())

@router.post("/predict")
def predict_performance(payload: PerformanceRequest, request: Request):
    """
    Predicts player performance and returns SHAP explanation
    """
    df = request.app.state.dataset
    model = request.app.state.performance_model
    explainer = request.app.state.performance_explainer
    feature_names = request.app.state.performance_features

    player_name = payload.player_name
    player_row = get_player_row(player_name)
    
    if player_row is None:
        raise HTTPException(status_code=404, detail=f"Player '{player_name}' not found")

    # Prepare features
    X = pd.DataFrame([player_row[feature_names]])
    X = X.fillna(0)

    # Prediction
    prediction = float(model.predict(X)[0])

    # SHAP Explanation
    explanation = {}
    if explainer is not None:
        try:
            # Transform data through scaler for SHAP (TreeExplainer works on transformed data)
            X_transformed = model.named_steps['scaler'].transform(X)
            
            # Get SHAP values
            shap_list = get_shap_top_features(
                explainer=explainer,
                model_input=X_transformed,
                feature_names=feature_names,
                top_k=5
            )
            
            explanation = {
                "top_features": extract_feature_importance(shap_list),
                "key_factors": format_key_factors(shap_list),
                "shap_values": shap_list
            }
        except Exception as e:
            print(f"⚠️ SHAP explanation error: {e}")
            explanation = {
                "top_features": {},
                "key_factors": ["SHAP explanation unavailable"],
                "shap_values": []
            }
    else:
        explanation = {
            "top_features": {},
            "key_factors": ["SHAP explainer not loaded"],
            "shap_values": []
        }

    return {
        "player": player_name,
        "predicted_performance": round(prediction, 2),
        "explanation": explanation
    }
