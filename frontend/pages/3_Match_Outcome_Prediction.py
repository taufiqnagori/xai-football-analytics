import streamlit as st
from utils.api_client import (
    get_match_players,
    predict_match
)

st.title("🏆 Match Outcome Prediction")

players = get_match_players()
player = st.selectbox("Select Player", players)

if st.button("Predict Match Outcome"):
    result = predict_match(player)

    if "error" in result:
        st.error(result["error"])
    else:
        st.success("Prediction Successful")
        st.write(result["predicted_match_outcome"])
