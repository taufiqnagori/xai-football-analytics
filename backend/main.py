from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from backend.utils.load_models import load_all_models
from backend.routers.performance import performance_router
from backend.routers.injury import injury_router
from backend.routers.match import match_router

app = FastAPI(title="XAI Football Analytics API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def startup_event():
    load_all_models(app)

app.include_router(performance_router, prefix="/api/performance")
app.include_router(injury_router, prefix="/api/injury")
app.include_router(match_router, prefix="/api/match")
