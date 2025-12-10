import pandas as pd
import numpy as np

# -----------------------------------------------------------
# 1. FETCH PLAYER DATA FROM DATASET
# -----------------------------------------------------------
def get_player_row(player_name: str, dataset: pd.DataFrame):
    """
    Return the row of the dataset that matches the player's name.
    """
    player_row = dataset[dataset["player_name"].str.lower() == player_name.lower()]

    if player_row.empty:
        return None  # player not found

    return player_row.iloc[0]  # return as series


# -----------------------------------------------------------
# 2. PREPARE INPUT FOR PERFORMANCE MODEL
# -----------------------------------------------------------
def prepare_performance_input(player_row: pd.Series):
    """
    Extract only the columns needed for the performance model
    and convert into a single-row DataFrame for prediction.
    """

    performance_features = [
        "age", "height_cm", "weight_kg", "position",
        "matches_played", "minutes_played", "goals", "assists",
        "shots_on_target", "pass_accuracy", "dribbles_completed",
        "dribble_success_rate", "tackles", "interceptions",
        "sprint_speed", "stamina_score"
    ]

    df = pd.DataFrame([player_row[performance_features].to_dict()])
    return df


# -----------------------------------------------------------
# 3. PREPARE INPUT FOR INJURY RISK MODEL
# -----------------------------------------------------------
def prepare_injury_input(player_row: pd.Series):
    """
    Extract and format the feature set required for injury risk prediction.
    """

    injury_features = [
        "age", "position", "nationality", "club_name",
        "past_injury_count", "training_load_score",
        "average_distance_covered_km", "recovery_time_hours",
        "muscle_strength_score", "stamina_score",
        "minutes_played", "matches_played"
    ]

    df = pd.DataFrame([player_row[injury_features].to_dict()])
    return df


# -----------------------------------------------------------
# 4. PREPARE INPUT FOR MATCH OUTCOME MODEL (TEAM FEATURES)
# -----------------------------------------------------------
def prepare_match_team_features(team_player_names: list, dataset: pd.DataFrame):
    """
    Given a list of player names, this function:
    - fetches their rows
    - averages team-relevant stats
    - returns a team feature dictionary
    """

    rows = []
    missing_players = []

    for name in team_player_names:
        row = get_player_row(name, dataset)
        if row is None:
            missing_players.append(name)
        else:
            rows.append(row)

    # If no valid players found → return None
    if len(rows) == 0:
        return None, missing_players

    team_df = pd.DataFrame(rows)

    # Average for match model
    team_features = {
        "team_strength_rating": team_df["team_strength_rating"].mean(),
        "possession_pct": team_df["possession_pct"].mean(),
        "goals_scored_team": team_df["goals_scored_team"].mean(),
        "goals_conceded_team": team_df["goals_conceded_team"].mean(),
    }

    # Return team features + missing players
    return team_features, missing_players


# -----------------------------------------------------------
# 5. PREPARE FINAL MATCH MODEL INPUT
# -----------------------------------------------------------
def prepare_match_input(team_a_names, team_b_names, dataset):
    """
    Combines both teams' stats into a final ML-ready DataFrame
    for predicting match outcome.
    """

    team_a, missing_a = prepare_match_team_features(team_a_names, dataset)
    team_b, missing_b = prepare_match_team_features(team_b_names, dataset)

    # Return missing player errors
    missing_players = missing_a + missing_b

    if team_a is None or team_b is None:
        return None, missing_players

    match_input = pd.DataFrame([{
        "team_strength_rating": team_a["team_strength_rating"],
        "opponent_strength_rating": team_b["team_strength_rating"],
        "possession_pct": team_a["possession_pct"],
        "goals_scored_team": team_a["goals_scored_team"],
        "goals_conceded_team": team_a["goals_conceded_team"]
    }])

    return match_input, missing_players
