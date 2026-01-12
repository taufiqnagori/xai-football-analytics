import requests
from typing import List, Dict, Any

BASE = "http://127.0.0.1:8000/api"

def get_players() -> List[str]:
    """Get list of all players"""
    try:
        r = requests.get(f"{BASE}/performance/players", timeout=5)
        r.raise_for_status()
        return r.json()
    except requests.exceptions.ConnectionError:
        print(f"Connection Error: Could not connect to backend at {BASE}")
        print("Make sure the backend is running: uvicorn backend.main:app --reload")
        return []
    except requests.exceptions.Timeout:
        print(f"Timeout: Backend at {BASE} did not respond in time")
        return []
    except Exception as e:
        print(f"Error fetching players: {e}")
        return []

def get_teams() -> List[str]:
    """Get list of all teams"""
    try:
        # Teams are derived from players, so we'll get unique teams from dataset
        # For now, return empty list - teams will be derived from player data
        return []
    except Exception as e:
        print(f"Error fetching teams: {e}")
        return []

def predict_performance(player_name: str) -> Dict[str, Any]:
    """Predict player performance"""
    try:
        r = requests.post(
            f"{BASE}/performance/predict",
            json={"player_name": player_name}
        )
        r.raise_for_status()
        return r.json()
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            return {"error": f"Player '{player_name}' not found"}
        return {"error": str(e)}
    except Exception as e:
        return {"error": str(e)}

def predict_injury(player_name: str) -> Dict[str, Any]:
    """Predict injury risk"""
    try:
        r = requests.post(
            f"{BASE}/injury/predict",
            json={"player_name": player_name}
        )
        r.raise_for_status()
        return r.json()
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 404:
            return {"error": f"Player '{player_name}' not found"}
        return {"error": str(e)}
    except Exception as e:
        return {"error": str(e)}

def predict_match(team_a: List[str], team_b: List[str]) -> Dict[str, Any]:
    """Predict match outcome between two teams of 11 players each"""
    try:
        r = requests.post(
            f"{BASE}/match/predict",
            json={
                "team_a": team_a,
                "team_b": team_b
            }
        )
        r.raise_for_status()
        return r.json()
    except requests.exceptions.HTTPError as e:
        if e.response.status_code == 400:
            error_detail = e.response.json().get("detail", str(e))
            return {"error": error_detail}
        if e.response.status_code == 404:
            error_detail = e.response.json().get("detail", str(e))
            return {"error": error_detail}
        return {"error": str(e)}
    except Exception as e:
        return {"error": str(e)}
