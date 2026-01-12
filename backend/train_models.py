import pandas as pd
import numpy as np
import joblib
from pathlib import Path
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.ensemble import RandomForestRegressor, RandomForestClassifier
from sklearn.model_selection import train_test_split
import shap
import lime
import lime.lime_tabular

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_PATH = BASE_DIR / "data" / "football_master_dataset.csv"
MODEL_DIR = BASE_DIR / "models"
MODEL_DIR.mkdir(exist_ok=True)

print("Loading dataset...")
df = pd.read_csv(DATA_PATH)

# Handle missing values
df = df.fillna(df.select_dtypes(include=[np.number]).mean())

print(f"Dataset loaded: {df.shape[0]} rows, {df.shape[1]} columns")

# ==================== PERFORMANCE MODEL ====================
print("\nTraining Performance Model...")
performance_features = [
    "minutes_played", "goals", "assists", "passes", "shots", "tackles",
    "matches_played", "age"
]

# Use available columns only
performance_features = [f for f in performance_features if f in df.columns]

X_perf = df[performance_features].fillna(0)
y_perf = df["performance_score"].fillna(df["performance_score"].mean())

perf_model = Pipeline([
    ("scaler", StandardScaler()),
    ("model", RandomForestRegressor(n_estimators=200, random_state=42, n_jobs=-1))
])

perf_model.fit(X_perf, y_perf)
joblib.dump(perf_model, MODEL_DIR / "performance_model.pkl")
print(f"Performance model saved. Features: {performance_features}")

# Create SHAP explainer for performance
print("Creating SHAP explainer for performance...")
X_perf_sample = X_perf.sample(min(100, len(X_perf)), random_state=42)
perf_explainer = shap.TreeExplainer(perf_model.named_steps['model'])
joblib.dump(perf_explainer, MODEL_DIR / "shap_explainer_performance.pkl")
print("Performance SHAP explainer saved")

# ==================== INJURY MODEL ====================
print("\nTraining Injury Risk Model...")
# Use available columns - map to closest available features
injury_features = [
    "age", "minutes_played", "matches_played", "injuries_last_season"
]

# Use available columns only
injury_features = [f for f in injury_features if f in df.columns]

X_injury = df[injury_features].fillna(0)
y_injury = df["injury_risk"].fillna(df["injury_risk"].mean())

# Ensure injury risk is between 0 and 1
y_injury = np.clip(y_injury, 0, 1)

inj_model = Pipeline([
    ("scaler", StandardScaler()),
    ("model", RandomForestRegressor(n_estimators=200, random_state=42, n_jobs=-1))
])

inj_model.fit(X_injury, y_injury)
joblib.dump(inj_model, MODEL_DIR / "injury_risk_model.pkl")
print(f"Injury model saved. Features: {injury_features}")

# Create SHAP explainer for injury
print("Creating SHAP explainer for injury...")
X_injury_sample = X_injury.sample(min(100, len(X_injury)), random_state=42)
inj_explainer = shap.TreeExplainer(inj_model.named_steps['model'])
joblib.dump(inj_explainer, MODEL_DIR / "shap_explainer_injury.pkl")
print("Injury SHAP explainer saved")

# ==================== MATCH MODEL ====================
print("\nTraining Match Outcome Model...")

# For match prediction, we'll aggregate team stats
# Create synthetic match data from player data
match_data = []

for team in df["team"].unique():
    team_df = df[df["team"] == team]
    
    # Aggregate team stats
    team_performance = team_df["performance_score"].mean()
    team_injury_risk = team_df["injury_risk"].mean()
    team_goals = team_df["goals"].sum()
    team_assists = team_df["assists"].sum()
    team_passes = team_df["passes"].sum()
    team_minutes = team_df["minutes_played"].sum()
    
    match_data.append({
        "team": team,
        "avg_performance": team_performance,
        "avg_injury_risk": team_injury_risk,
        "total_goals": team_goals,
        "total_assists": team_assists,
        "total_passes": team_passes,
        "total_minutes": team_minutes,
        "num_players": len(team_df)
    })

match_df = pd.DataFrame(match_data)

# Create synthetic match pairs
match_pairs = []
np.random.seed(42)

for _ in range(500):  # Generate 500 synthetic matches
    teams = np.random.choice(match_df["team"].values, size=2, replace=False)
    team_a, team_b = teams[0], teams[1]
    
    team_a_stats = match_df[match_df["team"] == team_a].iloc[0]
    team_b_stats = match_df[match_df["team"] == team_b].iloc[0]
    
    # Calculate team strength (weighted by performance and injury risk)
    team_a_strength = team_a_stats["avg_performance"] * (1 - team_a_stats["avg_injury_risk"])
    team_b_strength = team_b_stats["avg_performance"] * (1 - team_b_stats["avg_injury_risk"])
    
    # Determine winner probabilistically
    total_strength = team_a_strength + team_b_strength
    if total_strength > 0:
        team_a_win_prob = team_a_strength / total_strength
    else:
        team_a_win_prob = 0.5
    
    outcome = "Team A" if np.random.random() < team_a_win_prob else "Team B"
    
    match_pairs.append({
        "team_a_avg_performance": team_a_stats["avg_performance"],
        "team_a_avg_injury_risk": team_a_stats["avg_injury_risk"],
        "team_a_total_goals": team_a_stats["total_goals"],
        "team_a_total_assists": team_a_stats["total_assists"],
        "team_a_total_passes": team_a_stats["total_passes"],
        "team_b_avg_performance": team_b_stats["avg_performance"],
        "team_b_avg_injury_risk": team_b_stats["avg_injury_risk"],
        "team_b_total_goals": team_b_stats["total_goals"],
        "team_b_total_assists": team_b_stats["total_assists"],
        "team_b_total_passes": team_b_stats["total_passes"],
        "outcome": outcome
    })

match_train_df = pd.DataFrame(match_pairs)

match_features = [
    "team_a_avg_performance", "team_a_avg_injury_risk", "team_a_total_goals",
    "team_a_total_assists", "team_a_total_passes",
    "team_b_avg_performance", "team_b_avg_injury_risk", "team_b_total_goals",
    "team_b_total_assists", "team_b_total_passes"
]

X_match = match_train_df[match_features]
y_match = match_train_df["outcome"]

match_model = Pipeline([
    ("scaler", StandardScaler()),
    ("model", RandomForestClassifier(n_estimators=200, random_state=42, n_jobs=-1))
])

match_model.fit(X_match, y_match)
joblib.dump(match_model, MODEL_DIR / "match_outcome_model.pkl")
print(f"Match model saved. Features: {match_features}")

# Create SHAP explainer for match
print("Creating SHAP explainer for match...")
X_match_sample = X_match.sample(min(100, len(X_match)), random_state=42)
match_explainer = shap.TreeExplainer(match_model.named_steps['model'])
joblib.dump(match_explainer, MODEL_DIR / "shap_explainer_match.pkl")
print("Match SHAP explainer saved")

# Save feature names for each model
joblib.dump(performance_features, MODEL_DIR / "performance_features.pkl")
joblib.dump(injury_features, MODEL_DIR / "injury_features.pkl")
joblib.dump(match_features, MODEL_DIR / "match_features.pkl")

print("\nAll models trained successfully!")
print(f"Models saved to: {MODEL_DIR}")
