from fastapi import APIRouter, Request
from backend.schemas.injury_request import InjuryRequest

# --------------------------------------------------
# Router
# --------------------------------------------------
injury_router = APIRouter()


@injury_router.get("/players")
def get_players(request: Request):
    df = request.app.state.dataset
    return sorted(df["player_name"].dropna().unique().tolist())


@injury_router.post("/predict")
def predict_injury(payload: InjuryRequest, request: Request):
    """
    Predicts injury risk using FULL pipeline input
    """
    df = request.app.state.dataset
    model = request.app.state.injury_model

    player_name = payload.player_name
    player = df[df["player_name"] == player_name]

    if player.empty:
        return {"error": "Player not found"}

    # --------------------------------------------------
    # IMPORTANT: Pipeline expects FULL RAW INPUT
    # --------------------------------------------------
    X = player.copy()

    # Drop target column if present
    if "injury_risk" in X.columns:
        X = X.drop(columns=["injury_risk"])

    # --------------------------------------------------
    # Prediction
    # --------------------------------------------------
    prediction = model.predict(X)[0]

    try:
        prediction = float(prediction)
    except Exception:
        prediction = str(prediction)

    return {
        "player": player_name,
        "injury_risk_prediction": prediction
    }
