from fastapi import APIRouter, Request

router = APIRouter()

@router.get("/players")
def get_players(request: Request):
    df = request.app.state.dataset
    return sorted(df["player_name"].dropna().unique().tolist())
