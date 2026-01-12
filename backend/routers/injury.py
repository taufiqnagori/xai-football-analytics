from fastapi import APIRouter, Request, HTTPException
from backend.data_access import get_player_row
from backend.schemas.injury_request import InjuryRequest
from backend.utils.shap_helpers import (
    get_shap_top_features,
    format_key_factors,
    extract_feature_importance
)
import pandas as pd
import numpy as np

router = APIRouter(tags=["Injury"])

@router.get("/players")
def get_players(request: Request):
    """
    Returns unique player names for dropdown
    """
    df = request.app.state.dataset
    return sorted(df["player_name"].dropna().unique().tolist())

@router.post("/predict")
def predict_injury(payload: InjuryRequest, request: Request):
    """
    Predicts injury risk and returns SHAP explanation
    """
    df = request.app.state.dataset
    model = request.app.state.injury_model
    explainer = request.app.state.injury_explainer
    feature_names = request.app.state.injury_features

    player_name = payload.player_name
    player_row = get_player_row(player_name)
    
    if player_row is None:
        raise HTTPException(status_code=404, detail=f"Player '{player_name}' not found")

    # Prepare features
    X = pd.DataFrame([player_row[feature_names]])
    X = X.fillna(0)

    # Prediction
    risk = float(model.predict(X)[0])
    # Ensure risk is between 0 and 1
    risk = max(0.0, min(1.0, risk))
    risk_percentage = round(risk * 100, 2)

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
        "injury_risk": risk,
        "injury_risk_percentage": risk_percentage,
        "explanation": explanation
    }
