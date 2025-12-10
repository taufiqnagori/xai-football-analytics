from fastapi import APIRouter, Request
from pydantic import BaseModel

from backend.utils.preprocess import get_player_row, prepare_injury_input
from backend.utils.shap_helpers import get_shap_top_features, format_key_factors



# -----------------------------------------------------------
# ROUTER INITIALIZATION
# -----------------------------------------------------------
injury_router = APIRouter()


# -----------------------------------------------------------
# REQUEST MODEL
# -----------------------------------------------------------
class InjuryRequest(BaseModel):
    player_name: str


# -----------------------------------------------------------
# API ENDPOINT: INJURY RISK PREDICTION
# -----------------------------------------------------------
@injury_router.post("/predict")
def predict_injury_risk(request: Request, body: InjuryRequest):

    # ----------------------------
    # 1. Load dataset and models
    # ----------------------------
    dataset = request.app.state.dataset
    model = request.app.state.injury_model
    explainer = request.app.state.injury_explainer
    label_encoder = request.app.state.injury_label_encoder

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
    model_input = prepare_injury_input(player_row)

    # ----------------------------
    # 4. Predict risk level
    # ----------------------------
    predicted_class = model.predict(model_input)[0]
    predicted_label = label_encoder.inverse_transform([predicted_class])[0]

    # Get probability of predicted class
    proba = model.predict_proba(model_input)[0][predicted_class]
    proba = float(round(proba * 100, 2))  # convert → percentage

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
    # 6. Response JSON
    # ----------------------------
    return {
        "status": "success",
        "player": player_name,
        "predicted_risk_level": predicted_label,
        "risk_probability_percent": proba,
        "top_factors": key_factors,
        "shap_details": shap_list
    }
