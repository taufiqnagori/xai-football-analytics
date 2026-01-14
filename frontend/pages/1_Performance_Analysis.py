import streamlit as st
from utils.api_client import get_players, predict_performance
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Page config
st.set_page_config(
    page_title="Player Performance Analysis",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Load CSS
import os
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CSS_PATH = os.path.join(BASE_DIR, "style.css")
with open(CSS_PATH, encoding='utf-8') as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# Theme toggle
from utils.theme import init_theme, render_theme_toggle, get_theme_styles
init_theme()

# Theme toggle button - fixed position
col1, col2, col3 = st.columns([1, 1, 1])
with col3:
    render_theme_toggle()

st.markdown(get_theme_styles(), unsafe_allow_html=True)

# Header
st.markdown("""
    <div style="text-align: center; padding: 2rem 0;">
        <h1>📈 Player Performance Prediction</h1>
        <p class="page-subtitle" style="font-size: 1.2rem;">
            Predict player performance using ML models with XAI explanations
        </p>
    </div>
""", unsafe_allow_html=True)

st.markdown("---")

# Get players list
with st.spinner("Loading players..."):
    players = get_players()

if not players:
    st.markdown("""
        <div class="error-box">
            <h3>⚠️ Connection Error</h3>
            <p>Could not load players. Make sure the backend API is running.</p>
        </div>
    """, unsafe_allow_html=True)
    st.info("""
    **To start the backend:**
    1. Open a new terminal
    2. Activate virtual environment: `venv\\Scripts\\activate`
    3. Run: `uvicorn backend.main:app --reload`
    4. Backend should be available at: http://127.0.0.1:8000
    """)
    st.stop()

# Main Content
col1, col2 = st.columns([1, 2])

with col1:
    st.markdown("""
        <div class="main-card">
            <h3>🔍 Select Player</h3>
        </div>
    """, unsafe_allow_html=True)
    
    player = st.selectbox(
        "Choose a player",
        players,
        key="perf_player_select",
        help="Select a player to analyze their predicted performance"
    )
    
    predict_btn = st.button(
        "🚀 Predict Performance",
        key="perf_predict_btn",
        type="primary",
        use_container_width=True
    )

with col2:
    st.markdown("""
        <div class="info-box">
            <h4>ℹ️ How It Works</h4>
            <p>Select a player and click "Predict Performance" to get:</p>
            <ul>
                <li>Predicted performance score</li>
                <li>SHAP feature importance analysis</li>
                <li>Key factors affecting the prediction</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)

# Prediction Results
if predict_btn:
    with st.spinner("🔮 Analyzing player performance..."):
        result = predict_performance(player)
    
    if "error" in result:
        st.markdown(f"""
            <div class="error-box">
                <h3>❌ Error</h3>
                <p>{result['error']}</p>
            </div>
        """, unsafe_allow_html=True)
    else:
        # Display prediction
        st.markdown("---")
        st.markdown("""
            <div class="prediction-result slide-in">
                <h2>🎯 Prediction Results</h2>
            </div>
        """, unsafe_allow_html=True)
        
        perf_score = result.get("predicted_performance", 0)
        
        # Metrics Row
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown(f"""
                <div class="metric-container">
                    <div style="color: rgba(255, 255, 255, 0.7); font-size: 0.9rem; margin-bottom: 0.5rem;">Player</div>
                    <div style="font-size: 1.5rem; font-weight: 600; color: white;">{result.get('player', 'N/A')}</div>
                </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
                <div class="metric-container">
                    <div style="color: rgba(255, 255, 255, 0.7); font-size: 0.9rem; margin-bottom: 0.5rem;">Performance Score</div>
                    <div class="metric-value">{perf_score:.2f}</div>
                </div>
            """, unsafe_allow_html=True)
        
        with col3:
            if perf_score >= 90:
                rating = "⭐ Excellent"
                rating_color = "#22c55e"
            elif perf_score >= 80:
                rating = "⭐ Very Good"
                rating_color = "#3b82f6"
            elif perf_score >= 70:
                rating = "⭐ Good"
                rating_color = "#fbbf24"
            else:
                rating = "⭐ Average"
                rating_color = "#ef4444"
            
            st.markdown(f"""
                <div class="metric-container">
                    <div style="color: rgba(255, 255, 255, 0.7); font-size: 0.9rem; margin-bottom: 0.5rem;">Rating</div>
                    <div style="font-size: 1.5rem; font-weight: 600; color: {rating_color};">{rating}</div>
                </div>
            """, unsafe_allow_html=True)
        
        # SHAP Explanation
        explanation = result.get("explanation", {})
        
        if explanation:
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("""
                <div class="main-card">
                    <h3>🔍 XAI Explanation (SHAP)</h3>
                    <p style="color: rgba(255, 255, 255, 0.7);">
                        Understanding which features most influence the performance prediction
                    </p>
                </div>
            """, unsafe_allow_html=True)
            
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
                
                colors = ['#22c55e' if x > 0 else '#ef4444' for x in df_shap["SHAP Value"]]
                
                fig.add_trace(go.Bar(
                    y=df_shap["Feature"],
                    x=df_shap["SHAP Value"],
                    orientation='h',
                    marker_color=colors,
                    text=[f"{x:.3f}" for x in df_shap["SHAP Value"]],
                    textposition='outside',
                    textfont=dict(color='white', size=12)
                ))
                
                fig.update_layout(
                    title="Feature Importance (SHAP Values)",
                    xaxis_title="SHAP Value",
                    yaxis_title="Feature",
                    height=400,
                    showlegend=False,
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='white'),
                    xaxis=dict(gridcolor='rgba(255, 255, 255, 0.1)'),
                    yaxis=dict(gridcolor='rgba(255, 255, 255, 0.1)')
                )
                
                st.plotly_chart(fig, use_container_width=True)
            
            if key_factors:
                st.markdown("""
                    <div class="main-card">
                        <h3>📊 Key Factors</h3>
                    </div>
                """, unsafe_allow_html=True)
                
                for factor in key_factors:
                    st.markdown(f"""
                        <div class="player-card">
                            <p style="margin: 0; color: white;">• {factor}</p>
                        </div>
                    """, unsafe_allow_html=True)
        else:
            st.markdown("""
                <div class="info-box">
                    <p>ℹ️ No explanation data available</p>
                </div>
            """, unsafe_allow_html=True)

# Back to Home
st.markdown("<br>", unsafe_allow_html=True)
if st.button("🏠 Back to Home", use_container_width=True):
    st.switch_page("app.py")
