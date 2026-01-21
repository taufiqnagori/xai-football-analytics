from fastapi import APIRouter, Request, HTTPException
from backend.data_access import get_player_row, engineer_features
from backend.schemas.performance_request import PerformanceRequest
import pandas as pd
import numpy as np

router = APIRouter(tags=["Performance"])

def get_feature_importance_explanation(model, feature_names, prediction_value):
    """
    Generate feature importance explanation for XGBoost model
    """
    try:
        # Get feature importance from XGBoost model
        # Check if model is a pipeline or direct model
        if hasattr(model, 'named_steps'):
            xgb_model = model.named_steps['model']
        else:
            xgb_model = model
        feature_importance = xgb_model.feature_importances_
        
        # Create dataframe with importance scores
        importance_df = pd.DataFrame({
            "feature": feature_names,
            "importance": feature_importance
        }).sort_values("importance", ascending=False).head(5)
        
        # Create explanation
        top_features = {row['feature']: round(float(row['importance']), 4) 
                       for _, row in importance_df.iterrows()}
        
        key_factors = [f"{feat}: {imp:.1%} importance" 
                      for feat, imp in top_features.items()]
        
        return {
            "top_features": top_features,
            "key_factors": key_factors,
            "explanation": "Top factors influencing this prediction based on model feature importance"
        }
    except Exception as e:
        return {
            "top_features": {},
            "key_factors": ["Feature importance calculation unavailable"],
            "explanation": f"Error: {str(e)}"
        }

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
    Predicts player performance and returns explanation
    """
    df = request.app.state.dataset
    model = request.app.state.performance_model
    feature_names = request.app.state.performance_features

    player_name = payload.player_name
    player_row = get_player_row(player_name)
    
    if player_row is None:
        raise HTTPException(status_code=404, detail=f"Player '{player_name}' not found")

    # Apply feature engineering
    player_row = engineer_features(player_row)
    
    # Prepare features
    X = pd.DataFrame([player_row[feature_names]])
    X = X.fillna(0)

    # Prediction
    try:
        prediction = float(model.predict(X)[0])
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")

    # Get explanation
    explanation = get_feature_importance_explanation(model, feature_names, prediction)

    return {
        "player": player_name,
        "predicted_performance": round(prediction, 2),
        "explanation": explanation
    }
