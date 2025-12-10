from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import pandas as pd

# Routers
from backend.routers.performance import performance_router
from backend.routers.injury import injury_router
from backend.routers.match import match_router

# Config and model loader
import backend.config as config
from backend.utils.load_models import load_all_models


# -----------------------------------------------------------
# 1. INITIALIZE FASTAPI APP
# -----------------------------------------------------------
app = FastAPI(
    title="XAI-Powered Football Analytics Suite",
    description="API for Player Performance Prediction, Injury Risk Analysis, and Match Outcome Prediction",
    version="1.0.0"
)


# -----------------------------------------------------------
# 2. ENABLE CORS FOR FRONTEND (React / Streamlit)
# -----------------------------------------------------------
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],    # allow all for development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# -----------------------------------------------------------
# 3. APP STARTUP: LOAD MODELS + DATASET
# -----------------------------------------------------------
@app.on_event("startup")
def load_resources():
    print("🔄 Loading dataset and ML models...")

    # Load dataset
    app.state.dataset = pd.read_csv(config.DATASET_PATH)

    # Load all pre-trained ML models
    (
        app.state.performance_model,
        app.state.performance_explainer,
        app.state.injury_model,
        app.state.injury_explainer,
        app.state.injury_label_encoder,
        app.state.match_model,
        app.state.match_explainer,
        app.state.match_label_encoder
    ) = load_all_models()

    print("✅ Resources loaded successfully!")


# -----------------------------------------------------------
# 4. REGISTER ROUTERS
# -----------------------------------------------------------
app.include_router(performance_router, prefix="/api/performance", tags=["Player Performance"])
app.include_router(injury_router, prefix="/api/injury", tags=["Injury Risk"])
app.include_router(match_router, prefix="/api/match", tags=["Match Outcome"])


# -----------------------------------------------------------
# 5. ROOT ENDPOINT
# -----------------------------------------------------------
@app.get("/")
def home():
    return {
        "message": "Welcome to XAI Football Analytics API",
        "endpoints": {
            "performance": "/api/performance/predict",
            "injury_risk": "/api/injury/predict",
            "match_outcome": "/api/match/predict",
            "docs": "/docs"
        }
    }
