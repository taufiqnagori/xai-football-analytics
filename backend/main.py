from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.routers import performance, injury, match
from backend.utils.load_models import load_all_models

app = FastAPI(
    title="Football XAI API",
    description="XAI Powered Sports Analytics Suite API",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify exact origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(performance.router, prefix="/api/performance", tags=["Performance"])
app.include_router(injury.router, prefix="/api/injury", tags=["Injury"])
app.include_router(match.router, prefix="/api/match", tags=["Match"])

# Load models on startup
@app.on_event("startup")
async def startup_event():
    load_all_models(app)

@app.get("/")
def root():
    return {
        "message": "Football XAI API",
        "endpoints": {
            "performance": "/api/performance/predict",
            "injury": "/api/injury/predict",
            "match": "/api/match/predict"
        }
    }

@app.get("/health")
def health():
    return {"status": "healthy"}
