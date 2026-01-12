import streamlit as st
from utils.api_client import get_players, predict_match
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.title("🏆 Match Outcome Prediction")
st.markdown("Predict match outcome between two teams of 11 players each with XAI explanations")

# Get players list
players = get_players()

if not players:
    st.error("⚠️ Could not load players. Make sure the backend API is running.")
    st.info("""
    **To start the backend:**
    1. Open a new terminal
    2. Activate virtual environment: `venv\\Scripts\\activate`
    3. Run: `uvicorn backend.main:app --reload`
    4. Backend should be available at: http://127.0.0.1:8000
    """)
    st.stop()

st.subheader("Select Teams")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### Team A")
    team_a_players = st.multiselect(
        "Select 11 players for Team A",
        players,
        key="team_a_select",
        help="Select exactly 11 players"
    )
    
    if len(team_a_players) > 11:
        st.warning(f"⚠️ You selected {len(team_a_players)} players. Please select exactly 11.")
    elif len(team_a_players) < 11:
        st.info(f"ℹ️ Select {11 - len(team_a_players)} more player(s) for Team A")
    else:
        st.success(f"✅ Team A: {len(team_a_players)} players selected")
    
    if team_a_players:
        st.write("**Team A Players:**")
        for i, player in enumerate(team_a_players, 1):
            st.write(f"{i}. {player}")

with col2:
    st.markdown("### Team B")
    team_b_players = st.multiselect(
        "Select 11 players for Team B",
        players,
        key="team_b_select",
        help="Select exactly 11 players"
    )
    
    if len(team_b_players) > 11:
        st.warning(f"⚠️ You selected {len(team_b_players)} players. Please select exactly 11.")
    elif len(team_b_players) < 11:
        st.info(f"ℹ️ Select {11 - len(team_b_players)} more player(s) for Team B")
    else:
        st.success(f"✅ Team B: {len(team_b_players)} players selected")
    
    if team_b_players:
        st.write("**Team B Players:**")
        for i, player in enumerate(team_b_players, 1):
            st.write(f"{i}. {player}")

# Check for duplicate players
if team_a_players and team_b_players:
    common = set(team_a_players) & set(team_b_players)
    if common:
        st.error(f"❌ Error: Players cannot be in both teams: {', '.join(common)}")

# Predict button
if st.button("Predict Match Outcome", key="match_predict_btn", type="primary"):
    # Validation
    if len(team_a_players) != 11:
        st.error(f"❌ Team A must have exactly 11 players. Currently has {len(team_a_players)}")
        st.stop()
    
    if len(team_b_players) != 11:
        st.error(f"❌ Team B must have exactly 11 players. Currently has {len(team_b_players)}")
        st.stop()
    
    common = set(team_a_players) & set(team_b_players)
    if common:
        st.error(f"❌ Players cannot be in both teams: {', '.join(common)}")
        st.stop()
    
    with st.spinner("Predicting match outcome..."):
        result = predict_match(team_a_players, team_b_players)
    
    if "error" in result:
        st.error(f"❌ Error: {result['error']}")
    else:
        # Display results
        st.subheader("🎯 Prediction Results")
        
        team_a_prob = result.get("team_a_win_probability", 0)
        team_b_prob = result.get("team_b_win_probability", 0)
        predicted_winner = result.get("predicted_winner", "Unknown")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Team A Win Probability", f"{team_a_prob}%")
        
        with col2:
            st.metric("Team B Win Probability", f"{team_b_prob}%")
        
        with col3:
            winner_emoji = "🏆" if predicted_winner == "Team A" else "🏆"
            st.metric("Predicted Winner", f"{winner_emoji} {predicted_winner}")
        
        # Visual comparison
        st.subheader("📊 Win Probability Comparison")
        
        fig = go.Figure(data=[
            go.Bar(
                x=['Team A', 'Team B'],
                y=[team_a_prob, team_b_prob],
                marker_color=['#3498db', '#e74c3c'],
                text=[f"{team_a_prob}%", f"{team_b_prob}%"],
                textposition='outside'
            )
        ])
        
        fig.update_layout(
            title="Win Probability Comparison",
            yaxis_title="Win Probability (%)",
            yaxis_range=[0, 100],
            height=400
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Team statistics
        st.subheader("📈 Team Statistics")
        
        team_a_stats = result.get("team_a_stats", {})
        team_b_stats = result.get("team_b_stats", {})
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### Team A Stats")
            st.metric("Avg Performance", f"{team_a_stats.get('avg_performance', 0):.2f}")
            st.metric("Avg Injury Risk", f"{team_a_stats.get('avg_injury_risk', 0):.2f}")
            st.metric("Total Goals", team_a_stats.get('total_goals', 0))
            st.metric("Total Assists", team_a_stats.get('total_assists', 0))
        
        with col2:
            st.markdown("### Team B Stats")
            st.metric("Avg Performance", f"{team_b_stats.get('avg_performance', 0):.2f}")
            st.metric("Avg Injury Risk", f"{team_b_stats.get('avg_injury_risk', 0):.2f}")
            st.metric("Total Goals", team_b_stats.get('total_goals', 0))
            st.metric("Total Assists", team_b_stats.get('total_assists', 0))
        
        # XAI Explanation
        explanation = result.get("explanation", {})
        
        if explanation:
            st.subheader("🔍 XAI Explanation (SHAP)")
            
            top_features = explanation.get("top_features", {})
            key_factors = explanation.get("key_factors", [])
            influential_players = explanation.get("influential_players", [])
            
            if top_features:
                # Create visualization
                df_shap = pd.DataFrame([
                    {"Feature": k.replace("_", " ").title(), "SHAP Value": v}
                    for k, v in top_features.items()
                ])
                
                # Sort by absolute value
                df_shap["Abs Value"] = df_shap["SHAP Value"].abs()
                df_shap = df_shap.sort_values("Abs Value", ascending=True)
                
                # Create horizontal bar chart
                fig = go.Figure()
                
                colors = ['#2ecc71' if x > 0 else '#e74c3c' for x in df_shap["SHAP Value"]]
                
                fig.add_trace(go.Bar(
                    y=df_shap["Feature"],
                    x=df_shap["SHAP Value"],
                    orientation='h',
                    marker_color=colors,
                    text=[f"{x:.3f}" for x in df_shap["SHAP Value"]],
                    textposition='outside'
                ))
                
                fig.update_layout(
                    title="Feature Importance (SHAP Values)",
                    xaxis_title="SHAP Value",
                    yaxis_title="Feature",
                    height=500,
                    showlegend=False
                )
                
                st.plotly_chart(fig, use_container_width=True)
            
            if key_factors:
                st.subheader("📊 Key Factors Influencing Prediction")
                for factor in key_factors:
                    st.write(f"• {factor}")
            
            if influential_players:
                st.subheader("⭐ Most Influential Players")
                for player_info in influential_players:
                    st.write(f"• **{player_info.get('player', 'Unknown')}** ({player_info.get('team', 'Unknown')}): {player_info.get('reason', 'N/A')}")
        else:
            st.info("ℹ️ No explanation data available")
