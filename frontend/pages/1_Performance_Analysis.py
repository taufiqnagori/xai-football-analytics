import streamlit as st
from utils.api_client import (
    get_performance_players,
    predict_performance
)

st.title("⚽ Player Performance Analysis")

players = get_performance_players()

player = st.selectbox("Select Player", players)

if st.button("Predict Performance"):
    result = predict_performance(player)

    if "error" in result:
        st.error(result["error"])
    else:
        st.metric(
            "Predicted Performance Score",
            round(result["predicted_performance"], 2)
        )

        if "explanation" in result:
            st.subheader("Key Factors")
            for k in result["explanation"]["key_factors"]:
                st.write(f"• {k}")
