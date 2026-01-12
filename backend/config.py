from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

DATASET_PATH = BASE_DIR / "data" / "football_master_dataset.csv"
MODEL_DIR = BASE_DIR / "models"

MODEL_PATHS = {
    "performance_model": MODEL_DIR / "performance_model.pkl",
    "injury_model": MODEL_DIR / "injury_risk_model.pkl",
    "match_model": MODEL_DIR / "match_outcome_model.pkl",
}
