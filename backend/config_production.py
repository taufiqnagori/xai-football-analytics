"""
Production Configuration - Model versioning and deployment settings
"""

MODEL_VERSION = "2.0"
USE_XGBOOST = True

# Model file mappings
MODEL_VERSIONS = {
    "v1": {
        "performance": "performance_model.pkl",
        "injury": "injury_risk_model.pkl",
        "match": "match_outcome_model.pkl",
    },
    "v2": {
        "performance": "performance_model_v2.pkl",
        "injury": "injury_risk_model_v2.pkl",
        "match": "match_outcome_model_v2.pkl",
    }
}

CURRENT_MODELS = MODEL_VERSIONS[f"v{MODEL_VERSION}"]

# Feature sets by version
FEATURES = {
    "v2": {
        "performance": [
            "minutes_played", "matches_played", "goals", "assists", "passes", "shots", "tackles",
            "goals_per_match", "assists_per_match", "actions_per_90", "shot_accuracy",
            "pass_success_rate", "age", "is_young", "is_veteran", "is_starter", "full_season"
        ],
        "injury": [
            "age", "minutes_played", "matches_played", "injuries_last_season",
            "injury_frequency", "is_injury_prone", "is_young", "is_veteran",
            "high_workload", "full_season"
        ],
        "match": [
            "team_a_performance", "team_a_injury_risk", "team_a_goals", "team_a_starters", "team_a_goals_per_match",
            "team_b_performance", "team_b_injury_risk", "team_b_goals", "team_b_starters", "team_b_goals_per_match"
        ]
    }
}

# Model performance thresholds
PERFORMANCE_THRESHOLDS = {
    "performance_r2": 0.95,
    "injury_r2": 0.90,
    "match_accuracy": 0.60
}

# Logging and monitoring
LOG_PREDICTIONS = True
MONITOR_ACCURACY = True
RETRAINING_INTERVAL_DAYS = 30

# Feature engineering pipeline
ENABLE_FEATURE_ENGINEERING = True

# Model interpretability
ENABLE_FEATURE_IMPORTANCE = True
TOP_FEATURES_COUNT = 5
