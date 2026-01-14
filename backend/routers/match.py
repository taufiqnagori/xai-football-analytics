from fastapi import APIRouter, Request, HTTPException
from backend.data_access import get_players_by_names
from backend.schemas.match_request import MatchRequest
from backend.utils.shap_helpers import (
    get_shap_top_features,
    format_key_factors,
    extract_feature_importance
)
import pandas as pd
import numpy as np

router = APIRouter(tags=["Match"])

@router.get("/teams")
def get_teams(request: Request):
    """
    Returns list of all available teams
    """
    from backend.data_access import get_teams
    return get_teams()

@router.get("/teams/{team_name}/players")
def get_team_players(team_name: str, request: Request):
    """
    Returns all players for a specific team with their details
    """
    from backend.data_access import get_team_players_list
    players = get_team_players_list(team_name)
    if not players:
        raise HTTPException(status_code=404, detail=f"Team '{team_name}' not found")
    return players

@router.get("/teams/{team_name}/squad")
def get_default_squad(team_name: str, request: Request):
    """
    Returns default Playing XI (11 players) for a team
    """
    from backend.data_access import get_default_squad
    squad = get_default_squad(team_name)
    if not squad:
        raise HTTPException(status_code=404, detail=f"Team '{team_name}' not found or has no players")
    return {
        "team": team_name,
        "squad": squad,
        "squad_size": len(squad)
    }

@router.get("/players")
def get_players(request: Request):
    """
    Returns unique player names for dropdown
    """
    df = request.app.state.dataset
    return sorted(df["player_name"].dropna().unique().tolist())

@router.post("/predict")
def predict_match(payload: MatchRequest, request: Request):
    """
    Predicts match outcome between two teams of 11 players each
    
    Input: List of 11 player names for Team A and Team B
    Output: Win probabilities and SHAP explanation
    """
    df = request.app.state.dataset
    model = request.app.state.match_model
    explainer = request.app.state.match_explainer
    feature_names = request.app.state.match_features

    team_a_players = payload.team_a
    team_b_players = payload.team_b

    # Validate inputs
    if len(team_a_players) != 11:
        raise HTTPException(
            status_code=400,
            detail=f"Team A must have exactly 11 players. Got {len(team_a_players)}"
        )
    
    if len(team_b_players) != 11:
        raise HTTPException(
            status_code=400,
            detail=f"Team B must have exactly 11 players. Got {len(team_b_players)}"
        )

    # Check for duplicate players within teams
    if len(set(team_a_players)) != len(team_a_players):
        raise HTTPException(
            status_code=400,
            detail="Team A has duplicate players"
        )
    
    if len(set(team_b_players)) != len(team_b_players):
        raise HTTPException(
            status_code=400,
            detail="Team B has duplicate players"
        )

    # Check for players playing in both teams
    common_players = set(team_a_players) & set(team_b_players)
    if common_players:
        raise HTTPException(
            status_code=400,
            detail=f"Players cannot be in both teams: {', '.join(common_players)}"
        )

    # Get player data
    team_a_df = get_players_by_names(team_a_players)
    team_b_df = get_players_by_names(team_b_players)

    # Check if all players exist
    missing_a = set(team_a_players) - set(team_a_df["player_name"].values)
    missing_b = set(team_b_players) - set(team_b_df["player_name"].values)
    
    if missing_a:
        raise HTTPException(
            status_code=404,
            detail=f"Team A players not found: {', '.join(missing_a)}"
        )
    
    if missing_b:
        raise HTTPException(
            status_code=404,
            detail=f"Team B players not found: {', '.join(missing_b)}"
        )

    # Calculate team statistics
    team_a_performance = team_a_df["performance_score"].mean()
    team_a_injury_risk = team_a_df["injury_risk"].mean()
    team_a_goals = team_a_df["goals"].sum()
    team_a_assists = team_a_df["assists"].sum()
    team_a_passes = team_a_df["passes"].sum()

    team_b_performance = team_b_df["performance_score"].mean()
    team_b_injury_risk = team_b_df["injury_risk"].mean()
    team_b_goals = team_b_df["goals"].sum()
    team_b_assists = team_b_df["assists"].sum()
    team_b_passes = team_b_df["passes"].sum()

    # Prepare features for model
    match_features = {
        "team_a_avg_performance": team_a_performance,
        "team_a_avg_injury_risk": team_a_injury_risk,
        "team_a_total_goals": team_a_goals,
        "team_a_total_assists": team_a_assists,
        "team_a_total_passes": team_a_passes,
        "team_b_avg_performance": team_b_performance,
        "team_b_avg_injury_risk": team_b_injury_risk,
        "team_b_total_goals": team_b_goals,
        "team_b_total_assists": team_b_assists,
        "team_b_total_passes": team_b_passes,
    }

    X = pd.DataFrame([match_features])
    X = X.fillna(0)

    # Prediction
    prediction = model.predict(X)[0]
    probabilities = model.predict_proba(X)[0]
    
    # Get class names
    class_names = model.named_steps['model'].classes_
    
    # Map probabilities to team names
    team_a_win_prob = 0.0
    team_b_win_prob = 0.0
    
    for i, class_name in enumerate(class_names):
        if class_name == "Team A":
            team_a_win_prob = probabilities[i]
        elif class_name == "Team B":
            team_b_win_prob = probabilities[i]

    # If model doesn't have Team A/B classes, use probabilities directly
    if team_a_win_prob == 0.0 and team_b_win_prob == 0.0:
        if len(probabilities) == 2:
            team_a_win_prob = probabilities[0]
            team_b_win_prob = probabilities[1]
        else:
            # Fallback: use performance comparison
            total_strength = team_a_performance * (1 - team_a_injury_risk) + team_b_performance * (1 - team_b_injury_risk)
            if total_strength > 0:
                team_a_win_prob = (team_a_performance * (1 - team_a_injury_risk)) / total_strength
                team_b_win_prob = 1 - team_a_win_prob
            else:
                team_a_win_prob = 0.5
                team_b_win_prob = 0.5

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
                top_k=10
            )
            
            explanation = {
                "top_features": extract_feature_importance(shap_list),
                "key_factors": format_key_factors(shap_list),
                "shap_values": shap_list,
                "influential_players": _get_influential_players(
                    shap_list, team_a_df, team_b_df
                )
            }
        except Exception as e:
            print(f"⚠️ SHAP explanation error: {e}")
            explanation = {
                "top_features": {},
                "key_factors": ["SHAP explanation unavailable"],
                "shap_values": [],
                "influential_players": []
            }
    else:
        explanation = {
            "top_features": {},
            "key_factors": ["SHAP explainer not loaded"],
            "shap_values": [],
            "influential_players": []
        }

    return {
        "team_a_win_probability": round(team_a_win_prob * 100, 2),
        "team_b_win_probability": round(team_b_win_prob * 100, 2),
        "predicted_winner": "Team A" if team_a_win_prob > team_b_win_prob else "Team B",
        "team_a_stats": {
            "avg_performance": round(team_a_performance, 2),
            "avg_injury_risk": round(team_a_injury_risk, 2),
            "total_goals": int(team_a_goals),
            "total_assists": int(team_a_assists)
        },
        "team_b_stats": {
            "avg_performance": round(team_b_performance, 2),
            "avg_injury_risk": round(team_b_injury_risk, 2),
            "total_goals": int(team_b_goals),
            "total_assists": int(team_b_assists)
        },
        "explanation": explanation
    }

def _get_influential_players(shap_list, team_a_df, team_b_df):
    """
    Identify which players influenced the prediction most
    """
    influential = []
    
    # Check team A performance features
    team_a_perf_shap = next((item for item in shap_list if "team_a_avg_performance" in item.get("feature", "")), None)
    if team_a_perf_shap and team_a_perf_shap.get("shap_value", 0) > 0:
        top_player_a = team_a_df.nlargest(1, "performance_score")
        if not top_player_a.empty:
            influential.append({
                "player": top_player_a.iloc[0]["player_name"],
                "team": "Team A",
                "reason": "Highest performance score"
            })
    
    # Check team B performance features
    team_b_perf_shap = next((item for item in shap_list if "team_b_avg_performance" in item.get("feature", "")), None)
    if team_b_perf_shap and team_b_perf_shap.get("shap_value", 0) > 0:
        top_player_b = team_b_df.nlargest(1, "performance_score")
        if not top_player_b.empty:
            influential.append({
                "player": top_player_b.iloc[0]["player_name"],
                "team": "Team B",
                "reason": "Highest performance score"
            })
    
    return influential
