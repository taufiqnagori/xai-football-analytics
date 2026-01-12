import streamlit as st
from utils.api_client import get_players, predict_performance
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.title("📈 Player Performance Prediction")
st.markdown("Predict player performance using ML models with XAI explanations")

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
    st.code("""
    # In a new terminal, run:
    venv\\Scripts\\activate
    uvicorn backend.main:app --reload
    """, language="bash")
    st.stop()

player = st.selectbox("Select Player", players, key="perf_player_select")

if st.button("Predict Performance", key="perf_predict_btn"):
    with st.spinner("Predicting performance..."):
        result = predict_performance(player)
    
    if "error" in result:
        st.error(f"❌ Error: {result['error']}")
    else:
        # Display prediction
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("Player", result.get("player", "N/A"))
        
        with col2:
            perf_score = result.get("predicted_performance", 0)
            st.metric("Predicted Performance Score", f"{perf_score:.2f}")
        
        with col3:
            # Performance rating
            if perf_score >= 90:
                rating = "⭐ Excellent"
            elif perf_score >= 80:
                rating = "⭐ Very Good"
            elif perf_score >= 70:
                rating = "⭐ Good"
            else:
                rating = "⭐ Average"
            st.metric("Rating", rating)
        
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
