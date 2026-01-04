from fastapi import APIRouter, Request
from backend.schemas.match_request import MatchRequest

# --------------------------------------------------
# Router
# --------------------------------------------------
match_router = APIRouter()


@match_router.get("/players")
def get_players(request: Request):
    """
    Returns unique player names for dropdown
    """
    df = request.app.state.dataset
    return sorted(df["player_name"].dropna().unique().tolist())


@match_router.post("/predict")
def predict_match(payload: MatchRequest, request: Request):
    """
    Predicts match outcome using FULL pipeline input
    """
    df = request.app.state.dataset
    model = request.app.state.match_model

    player_name = payload.player_name
    player = df[df["player_name"] == player_name]

    if player.empty:
        return {"error": "Player not found"}

    # --------------------------------------------------
    # IMPORTANT: Pipeline expects FULL RAW INPUT
    # --------------------------------------------------
    X = player.copy()

    # Drop target column if present
    if "match_outcome" in X.columns:
        X = X.drop(columns=["match_outcome"])

    # --------------------------------------------------
    # Prediction
    # --------------------------------------------------
    prediction = model.predict(X)[0]

    try:
        prediction = str(prediction)
    except Exception:
        prediction = prediction

    return {
        "player": player_name,
        "match_outcome_prediction": prediction
    }
