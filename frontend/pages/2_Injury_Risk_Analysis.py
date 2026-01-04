import streamlit as st
from utils.api_client import (
    get_injury_players,
    predict_injury
)

st.title("🩺 Injury Risk Analysis")

players = get_injury_players()
player = st.selectbox("Select Player", players)

if st.button("Predict Injury Risk"):
    result = predict_injury(player)

    if "error" in result:
        st.error(result["error"])
    else:
        st.metric(
            "Injury Risk Score",
            round(result["injury_risk_score"], 2)
        )
