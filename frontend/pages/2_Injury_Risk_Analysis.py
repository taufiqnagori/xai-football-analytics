import streamlit as st
from utils.api_client import get_players, predict_injury
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.title("🩺 Injury Risk Prediction")
st.markdown("Predict injury risk for players using ML models with XAI explanations")

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

player = st.selectbox("Select Player", players, key="injury_player_select")

if st.button("Predict Injury Risk", key="injury_predict_btn"):
    with st.spinner("Predicting injury risk..."):
        result = predict_injury(player)
    
    if "error" in result:
        st.error(f"❌ Error: {result['error']}")
    else:
        # Display prediction
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Player", result.get("player", "N/A"))
        
        with col2:
            risk_percentage = result.get("injury_risk_percentage", 0)
            st.metric("Injury Risk", f"{risk_percentage:.2f}%")
        
        with col3:
            # Risk level
            if risk_percentage >= 70:
                risk_level = "🔴 High Risk"
            elif risk_percentage >= 40:
                risk_level = "🟡 Medium Risk"
            else:
                risk_level = "🟢 Low Risk"
            st.metric("Risk Level", risk_level)
        
        # Visual gauge
        st.subheader("Risk Gauge")
        fig = go.Figure(go.Indicator(
            mode = "gauge+number+delta",
            value = risk_percentage,
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': "Injury Risk (%)"},
            delta = {'reference': 50},
            gauge = {
                'axis': {'range': [None, 100]},
                'bar': {'color': "darkblue"},
                'steps': [
                    {'range': [0, 40], 'color': "lightgreen"},
                    {'range': [40, 70], 'color': "yellow"},
                    {'range': [70, 100], 'color': "red"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': 70
                }
            }
        ))
        
        fig.update_layout(height=300)
        st.plotly_chart(fig, use_container_width=True)
        
        # SHAP Explanation
        explanation = result.get("explanation", {})
        
        if explanation:
            st.subheader("🔍 XAI Explanation (SHAP)")
            
            top_features = explanation.get("top_features", {})
            key_factors = explanation.get("key_factors", [])
            
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
                
                colors = ['#e74c3c' if x > 0 else '#2ecc71' for x in df_shap["SHAP Value"]]
                
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
                    xaxis_title="SHAP Value (Positive = Increases Risk)",
                    yaxis_title="Feature",
                    height=400,
                    showlegend=False
                )
                
                st.plotly_chart(fig, use_container_width=True)
            
            if key_factors:
                st.subheader("📊 Key Factors")
                for factor in key_factors:
                    st.write(f"• {factor}")
        else:
            st.info("ℹ️ No explanation data available")
