from pydantic import BaseModel

class InjuryRequest(BaseModel):
    player_name: str
