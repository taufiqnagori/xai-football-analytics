from pydantic import BaseModel

class PlayerRequest(BaseModel):
    player_name: str


class MatchRequest(BaseModel):
    team_a: str
    team_b: str
