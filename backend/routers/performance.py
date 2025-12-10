from fastapi import APIRouter, Request
from pydantic import BaseModel
import pandas as pd

from backend.utils.preprocess import get_player_row, prepare_performance_input
from backend.utils.shap_helpers import get_shap_top_features, format_key_factors


# -----------------------------------------------------------
# ROUTER INITIALIZATION
# -----------------------------------------------------------
performance_router = APIRouter()


# -----------------------------------------------------------
# REQUEST MODEL
# -----------------------------------------------------------
class PerformanceRequest(BaseModel):
    player_name: str


# -----------------------------------------------------------
# API ENDPOINT: PERFORMANCE PREDICTION
# -----------------------------------------------------------
@performance_router.post("/predict")
def predict_performance(request: Request, body: PerformanceRequest):

    # ----------------------------
    # 1. Load dataset and model
    # ----------------------------
    dataset = request.app.state.dataset
    model = request.app.state.performance_model
    explainer = request.app.state.performance_explainer

    player_name = body.player_name

    # ----------------------------
    # 2. Fetch player data
    # ----------------------------
    player_row = get_player_row(player_name, dataset)

    if player_row is None:
        return {
            "status": "error",
            "message": f"Player '{player_name}' not found in dataset."
        }

    # ----------------------------
    # 3. Prepare model input
    # ----------------------------
    model_input = prepare_performance_input(player_row)

    # ----------------------------
    # 4. Make prediction
    # ----------------------------
    predicted_rating = model.predict(model_input)[0]

    # ----------------------------
    # 5. SHAP Explanation
    # ----------------------------
    feature_names = model_input.columns.tolist()

    shap_list = get_shap_top_features(
        explainer=explainer,
        model_input=model_input,
        feature_names=feature_names,
        top_k=5
    )

    key_factors = format_key_factors(shap_list)

    # ----------------------------
    # 6. API RESPONSE
    # ----------------------------
    return {
        "status": "success",
        "player": player_name,
        "predicted_performance_rating": float(predicted_rating),
        "top_factors": key_factors,
        "shap_details": shap_list
    }
