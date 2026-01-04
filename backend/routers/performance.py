import pandas as pd
from fastapi import APIRouter, Request

from backend.schemas.performance_request import PerformanceRequest

# --------------------------------------------------
# Router
# --------------------------------------------------
performance_router = APIRouter()


@performance_router.get("/players")
def get_players(request: Request):
    df = request.app.state.dataset
    return sorted(df["player_name"].dropna().unique().tolist())


@performance_router.post("/predict")
def predict_performance(payload: PerformanceRequest, request: Request):
    df = request.app.state.dataset
    model = request.app.state.performance_model

    player_name = payload.player_name
    player = df[df["player_name"] == player_name]

    if player.empty:
        return {"error": "Player not found"}

    # --------------------------------------------------
    # IMPORTANT: Pipeline expects FULL RAW INPUT
    # --------------------------------------------------
    X = player.copy()

    # Remove target column if present
    if "performance_score" in X.columns:
        X = X.drop(columns=["performance_score"])

    # --------------------------------------------------
    # Prediction (PIPELINE SAFE)
    # --------------------------------------------------
    prediction = float(model.predict(X)[0])

    return {
        "player": player_name,
        "predicted_performance": prediction,
        "note": "Prediction generated using full pipeline input"
    }
