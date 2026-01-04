from pydantic import BaseModel

class PerformanceRequest(BaseModel):
    player_name: str
