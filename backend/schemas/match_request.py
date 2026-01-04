from pydantic import BaseModel
from typing import List

class MatchRequest(BaseModel):
    team_a: List[str]
    team_b: List[str]
