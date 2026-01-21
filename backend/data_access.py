import pandas as pd
import numpy as np
from backend.config import DATASET_PATH

_df = None

def _load_df():
    global _df
    if _df is None:
        _df = pd.read_csv(DATASET_PATH)
    return _df

def engineer_features(df_row):
    """
    Apply feature engineering to a single player row (Series)
    Returns the enhanced row with engineered features
    """
    row = df_row.copy() if isinstance(df_row, pd.Series) else pd.Series(df_row)
    
    # Handle division by zero with safe division
    def safe_divide(numerator, denominator, default=0):
        if denominator == 0:
            return default
        return numerator / denominator
    
    # 1. FORM FEATURES (Goals/Assists per game)
    matches_played = row.get('matches_played', 1) or 1
    minutes_played = row.get('minutes_played', 1) or 1
    
    row['goals_per_match'] = safe_divide(row.get('goals', 0), matches_played)
    row['assists_per_match'] = safe_divide(row.get('assists', 0), matches_played)
    row['passes_per_match'] = safe_divide(row.get('passes', 0), matches_played)
    
    # 2. INVOLVEMENT FEATURES
    row['total_actions'] = row.get('goals', 0) + row.get('assists', 0) + row.get('tackles', 0)
    row['actions_per_90'] = safe_divide(row['total_actions'] * 90, minutes_played)
    
    # 3. EFFICIENCY FEATURES
    row['shot_accuracy'] = safe_divide(row.get('goals', 0), row.get('shots', 1))
    row['pass_success_rate'] = safe_divide(
        row.get('passes', 0),
        row.get('passes', 0) + row.get('shots', 0) + 1
    )
    
    # 4. INJURY RISK FEATURES
    row['injury_frequency'] = safe_divide(row.get('injuries_last_season', 0), matches_played)
    row['is_injury_prone'] = 1 if row.get('injuries_last_season', 0) > 1 else 0
    
    # 5. EXPERIENCE & POSITION FEATURES
    age = row.get('age', 0)
    row['is_young'] = 1 if age < 25 else 0
    row['is_veteran'] = 1 if age > 32 else 0
    
    # 6. WORKLOAD FEATURES
    # For single row, estimate based on the value itself
    row['high_workload'] = 1 if minutes_played > 2000 else 0  # Roughly top 25%
    row['full_season'] = 1 if matches_played > 30 else 0
    
    # 7. STARTING XI INDICATOR
    row['is_starter'] = int(row.get('is_starting_xi', 0)) if pd.notna(row.get('is_starting_xi')) else 0
    
    return row

def get_player_row(player_name: str):
    """
    Get a single player's data row
    """
    df = _load_df()
    row = df[df["player_name"] == player_name]
    return None if row.empty else row.iloc[0]

def get_players():
    """
    Get list of all unique player names
    """
    df = _load_df()
    return sorted(df["player_name"].dropna().unique().tolist())

def get_teams():
    """
    Get list of all unique team names
    Note: Dataset uses 'team' column, not 'club_name'
    """
    df = _load_df()
    return sorted(df["team"].dropna().unique().tolist())

def get_team_players(team_name: str):
    """
    Get all players for a given team
    """
    df = _load_df()
    return df[df["team"] == team_name]

def get_players_by_names(player_names: list):
    """
    Get multiple players' data by their names
    """
    df = _load_df()
    return df[df["player_name"].isin(player_names)]

def get_default_squad(team_name: str, squad_size: int = 11):
    """
    Get default Playing XI (11 players) for a team
    Strategy: Select best players by performance score, trying to balance positions
    Returns list of player names (no duplicates)
    """
    df = _load_df()
    team_df = df[df["team"] == team_name].copy()
    
    if team_df.empty:
        return []
    
    # Remove duplicates by player_name, keep first occurrence
    team_df = team_df.drop_duplicates(subset=["player_name"], keep="first")
    
    # Sort by performance score (descending)
    team_df = team_df.sort_values("performance_score", ascending=False)
    
    # Try to get a balanced squad (at least 1 GK, prefer 3-4 DF, 3-4 MF, 2-3 FW)
    # But if not enough players in certain positions, just take top performers
    squad = []
    position_counts = {"GK": 1, "DF": 4, "MF": 4, "FW": 2}
    
    # First pass: Get at least one of each position if available
    for pos, count in position_counts.items():
        pos_players = team_df[team_df["position"] == pos].head(count)
        for _, player in pos_players.iterrows():
            player_name = player["player_name"]
            if len(squad) < squad_size and player_name not in squad:
                squad.append(player_name)
    
    # Second pass: Fill remaining slots with top performers regardless of position
    remaining = squad_size - len(squad)
    if remaining > 0:
        for _, player in team_df.iterrows():
            if len(squad) >= squad_size:
                break
            player_name = player["player_name"]
            if player_name not in squad:
                squad.append(player_name)
    
    return squad[:squad_size]

def get_team_players_list(team_name: str):
    """
    Get all players for a team with their details
    Returns list of dicts with player info
    """
    df = _load_df()
    team_df = df[df["team"] == team_name].copy()
    
    if team_df.empty:
        return []
    
    players = []
    for _, row in team_df.iterrows():
        players.append({
            "name": row["player_name"],
            "position": row.get("position", "Unknown"),
            "performance_score": float(row.get("performance_score", 0)),
            "injury_risk": float(row.get("injury_risk", 0)),
            "goals": int(row.get("goals", 0)),
            "assists": int(row.get("assists", 0)),
            "age": int(row.get("age", 0))
        })
    
    return sorted(players, key=lambda x: x["performance_score"], reverse=True)
