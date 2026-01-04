import requests

BASE_URL = "http://127.0.0.1:8000/api"


# --------------------------------------------------
# PERFORMANCE
# --------------------------------------------------
def get_performance_players():
    res = requests.get(f"{BASE_URL}/performance/players")
    return res.json()

def predict_performance(player_name):
    payload = {"player_name": player_name}
    res = requests.post(
        f"{BASE_URL}/performance/predict",
        json=payload
    )
    return res.json()


# --------------------------------------------------
# INJURY
# --------------------------------------------------
def get_injury_players():
    res = requests.get(f"{BASE_URL}/injury/players")
    return res.json()

def predict_injury(player_name):
    payload = {"player_name": player_name}
    res = requests.post(
        f"{BASE_URL}/injury/predict",
        json=payload
    )
    return res.json()


# --------------------------------------------------
# MATCH
# --------------------------------------------------
def get_match_players():
    res = requests.get(f"{BASE_URL}/match/players")
    return res.json()

def predict_match(player_name):
    payload = {"player_name": player_name}
    res = requests.post(
        f"{BASE_URL}/match/predict",
        json=payload
    )
    return res.json()
