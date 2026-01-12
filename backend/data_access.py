import pandas as pd
from backend.config import DATASET_PATH

_df = None

def _load_df():
    global _df
    if _df is None:
        _df = pd.read_csv(DATASET_PATH)
    return _df

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
