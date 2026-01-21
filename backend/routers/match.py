from fastapi import APIRouter, Request, HTTPException
from backend.data_access import get_players_by_names, engineer_features
from backend.schemas.match_request import MatchRequest
import pandas as pd
import numpy as np

router = APIRouter(tags=["Match"])

def get_feature_importance_explanation(model, feature_names, features_dict):
    """
    Generate feature importance explanation for XGBoost match model
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
        }).sort_values("importance", ascending=False).head(10)
        
        # Create explanation
        top_features = {row['feature']: round(float(row['importance']), 4) 
                       for _, row in importance_df.iterrows()}
        
        key_factors = [f"{feat}: {imp:.1%} importance" 
                      for feat, imp in top_features.items()]
        
        return {
            "top_features": top_features,
            "key_factors": key_factors,
            "explanation": "Top factors influencing match prediction based on team statistics"
        }
    except Exception as e:
        return {
            "top_features": {},
            "key_factors": ["Feature importance calculation unavailable"],
            "explanation": f"Error: {str(e)}"
        }

@router.get("/teams")
def get_teams(request: Request):
    """
    Returns list of all available teams
    """
    from backend.data_access import get_teams
    return get_teams()

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

@router.get("/teams/{team_name}/players")
def get_team_players(team_name: str, request: Request):
    """
    Returns all players for a specific team
    """
    from backend.data_access import get_team_players
    players_df = get_team_players(team_name)
    if players_df.empty:
        raise HTTPException(status_code=404, detail=f"Team '{team_name}' not found")
    
    return [
        {
            "player_name": row["player_name"],
            "performance_score": round(float(row.get("performance_score", 0)), 2),
            "injury_risk": round(float(row.get("injury_risk", 0)), 2),
            "position": str(row.get("position", "Unknown"))
        }
        for _, row in players_df.iterrows()
    ]

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
    """
    try:
        model = request.app.state.match_model
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

        # Check for duplicate players
        if len(set(team_a_players)) != len(team_a_players):
            raise HTTPException(status_code=400, detail="Team A has duplicate players")
        
        if len(set(team_b_players)) != len(team_b_players):
            raise HTTPException(status_code=400, detail="Team B has duplicate players")

        # Check for players in both teams
        common_players = set(team_a_players) & set(team_b_players)
        if common_players:
            raise HTTPException(
                status_code=400,
                detail=f"Players cannot be in both teams: {', '.join(common_players)}"
            )

        # Get player data
        team_a_df = get_players_by_names(team_a_players)
        team_b_df = get_players_by_names(team_b_players)

        # Remove duplicates by player_name (keep first occurrence)
        team_a_df = team_a_df.drop_duplicates(subset=['player_name'], keep='first').reset_index(drop=True)
        team_b_df = team_b_df.drop_duplicates(subset=['player_name'], keep='first').reset_index(drop=True)

        # Check if all players exist
        missing_a = set(team_a_players) - set(team_a_df["player_name"].values)
        missing_b = set(team_b_players) - set(team_b_df["player_name"].values)
        
        if missing_a:
            raise HTTPException(status_code=404, detail=f"Team A players not found: {', '.join(missing_a)}")
        
        if missing_b:
            raise HTTPException(status_code=404, detail=f"Team B players not found: {', '.join(missing_b)}")

        # Apply feature engineering to each player
        team_a_engineered = team_a_df.copy()
        team_b_engineered = team_b_df.copy()
        
        team_a_engineered = team_a_engineered.apply(engineer_features, axis=1)
        team_b_engineered = team_b_engineered.apply(engineer_features, axis=1)

        # Calculate team statistics using engineered features
        team_a_performance = team_a_engineered["performance_score"].mean()
        team_a_injury_risk = team_a_engineered["injury_risk"].mean()
        team_a_goals = team_a_engineered["goals"].sum()
        team_a_starters = team_a_engineered["is_starter"].sum()
        team_a_goals_per_match = team_a_engineered["goals_per_match"].mean()

        team_b_performance = team_b_engineered["performance_score"].mean()
        team_b_injury_risk = team_b_engineered["injury_risk"].mean()
        team_b_goals = team_b_engineered["goals"].sum()
        team_b_starters = team_b_engineered["is_starter"].sum()
        team_b_goals_per_match = team_b_engineered["goals_per_match"].mean()

        # Prepare features for model - MUST match training feature names exactly
        match_features_dict = {
            "team_a_performance": team_a_performance,
            "team_a_injury_risk": team_a_injury_risk,
            "team_a_goals": team_a_goals,
            "team_a_starters": team_a_starters,
            "team_a_goals_per_match": team_a_goals_per_match,
            "team_b_performance": team_b_performance,
            "team_b_injury_risk": team_b_injury_risk,
            "team_b_goals": team_b_goals,
            "team_b_starters": team_b_starters,
            "team_b_goals_per_match": team_b_goals_per_match,
        }

        X = pd.DataFrame([match_features_dict])
        X = X.fillna(0)
        
        # Reorder columns to match model's expected feature order
        X = X[feature_names]

        # Prediction
        prediction = model.predict(X)[0]
        probabilities = model.predict_proba(X)[0]
        
        # Get class names - handle both pipeline and direct model
        if hasattr(model, 'named_steps'):
            class_names = model.named_steps['model'].classes_
        else:
            class_names = model.classes_
        
        # Map probabilities to team names
        team_a_win_prob = 0.0
        team_b_win_prob = 0.0
        
        for i, class_name in enumerate(class_names):
            if class_name == 1:  # Team A win
                team_a_win_prob = float(probabilities[i])
            elif class_name == 0:  # Team B win
                team_b_win_prob = float(probabilities[i])

        # Get explanation
        explanation = get_feature_importance_explanation(model, feature_names, match_features_dict)

        return {
            "team_a_win_probability": round(team_a_win_prob * 100, 2),
            "team_b_win_probability": round(team_b_win_prob * 100, 2),
            "predicted_winner": "Team A" if team_a_win_prob > team_b_win_prob else "Team B",
            "team_a_stats": {
                "avg_performance": round(float(team_a_performance), 2),
                "avg_injury_risk": round(float(team_a_injury_risk), 2),
                "total_goals": int(team_a_goals),
                "starters": int(team_a_starters),
                "goals_per_match": round(float(team_a_goals_per_match), 2)
            },
            "team_b_stats": {
                "avg_performance": round(float(team_b_performance), 2),
                "avg_injury_risk": round(float(team_b_injury_risk), 2),
                "total_goals": int(team_b_goals),
                "starters": int(team_b_starters),
                "goals_per_match": round(float(team_b_goals_per_match), 2)
            },
            "explanation": explanation
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Match prediction error: {str(e)}")
