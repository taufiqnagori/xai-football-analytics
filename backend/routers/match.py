from fastapi import APIRouter, Request
from pydantic import BaseModel

from backend.utils.preprocess import prepare_match_input
from backend.utils.shap_helpers import get_shap_top_features, format_key_factors



# -----------------------------------------------------------
# ROUTER INITIALIZATION
# -----------------------------------------------------------
match_router = APIRouter()


# -----------------------------------------------------------
# REQUEST MODEL
# -----------------------------------------------------------
class MatchRequest(BaseModel):
    team_a: list[str]
    team_b: list[str]


# -----------------------------------------------------------
# API ENDPOINT: MATCH OUTCOME PREDICTION
# -----------------------------------------------------------
@match_router.post("/predict")
def predict_match_outcome(request: Request, body: MatchRequest):

    dataset = request.app.state.dataset
    model = request.app.state.match_model
    explainer = request.app.state.match_explainer
    label_encoder = request.app.state.match_label_encoder

    team_a = body.team_a
    team_b = body.team_b

    # ----------------------------
    # 1. Prepare input for model
    # ----------------------------
    match_input, missing_players = prepare_match_input(team_a, team_b, dataset)

    if match_input is None:
        return {
            "status": "error",
            "message": "Match input could not be created.",
            "missing_players": missing_players
        }

    if len(missing_players) > 0:
        return {
            "status": "error",
            "message": "Some players were not found.",
            "missing_players": missing_players
        }

    # ----------------------------
    # 2. Predict Match Result
    # ----------------------------
    predicted_class = model.predict(match_input)[0]
    predicted_label = label_encoder.inverse_transform([predicted_class])[0]

    # Probability distribution (Win/Draw/Loss)
    probabilities = model.predict_proba(match_input)[0]
    prob_dict = {
        label_encoder.inverse_transform([i])[0]: float(round(probabilities[i] * 100, 2))
        for i in range(len(probabilities))
    }

    # ----------------------------
    # 3. SHAP Explanation
    # ----------------------------
    feature_names = match_input.columns.tolist()

    shap_list = get_shap_top_features(
        explainer=explainer,
        model_input=match_input,
        feature_names=feature_names,
        top_k=5
    )

    key_factors = format_key_factors(shap_list)

    # ----------------------------
    # 4. Return JSON Response
    # ----------------------------
    return {
        "status": "success",
        "predicted_result": predicted_label,
        "probabilities": prob_dict,
        "team_a": team_a,
        "team_b": team_b,
        "top_factors": key_factors,
        "shap_details": shap_list
    }
