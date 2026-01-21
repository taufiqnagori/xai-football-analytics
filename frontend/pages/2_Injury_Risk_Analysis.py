import streamlit as st
from utils.api_client import get_players, predict_injury
from utils.explanation_helper import translate_feature_name, create_insight_text, format_explanation_text
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Page config
st.set_page_config(
    page_title="Injury Risk Analysis",
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
from utils.theme import init_theme, render_sidebar_theme_toggle, get_theme_styles
init_theme()

# Sidebar theme toggle
with st.sidebar:
    # Navigation heading
    st.markdown("<div style='text-align: center; margin: 1rem 0;'><b>Navigation</b></div>", unsafe_allow_html=True)
    st.markdown("---")
    
    # Buttons in exact order with updated labels
    if st.button("🏠 Home", use_container_width=True, key="nav_home_sidebar"):
        st.switch_page("app.py")
    
    if st.button("📈 Player Performance", use_container_width=True, key="nav_perf_sidebar"):
        st.switch_page("pages/1_Performance_Analysis.py")
    
    if st.button("🩺 Injury Risk", use_container_width=True, key="nav_injury_sidebar"):
        st.switch_page("pages/2_Injury_Risk_Analysis.py")
    
    if st.button("🏆 Match Prediction", use_container_width=True, key="nav_match_sidebar"):
        st.switch_page("pages/3_Match_Outcome_Prediction.py")
    
    # Add spacing to push theme button to bottom
    st.markdown("<div style='margin-top: 2rem;'></div>", unsafe_allow_html=True)
    st.markdown("---")
    
    # Theme toggle at bottom
    render_sidebar_theme_toggle()

st.markdown(get_theme_styles(), unsafe_allow_html=True)

# Header
st.markdown("""
    <div style="text-align: center; padding: 2rem 0;">
        <h1>🩺 Injury Risk Prediction</h1>
        <p class="page-subtitle" style="font-size: 1.2rem;">
            Assess injury risk for players using ML models with XAI explanations
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
        key="injury_player_select",
        help="Select a player to assess their injury risk"
    )
    
    predict_btn = st.button(
        "🚀 Predict Injury Risk",
        key="injury_predict_btn",
        type="primary",
        use_container_width=True
    )

with col2:
    st.markdown("""
        <div class="info-box">
            <h4>ℹ️ How It Works</h4>
            <p>Select a player and click "Predict Injury Risk" to get:</p>
            <ul>
                <li>Injury risk percentage (0-100%)</li>
                <li>Risk level classification</li>
                <li>SHAP feature importance analysis</li>
                <li>Key risk factors</li>
            </ul>
        </div>
    """, unsafe_allow_html=True)

# Prediction Results
if predict_btn:
    with st.spinner("🔮 Analyzing injury risk..."):
        result = predict_injury(player)
    
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
        
        risk_percentage = result.get("injury_risk_percentage", 0)
        
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
                    <div style="color: rgba(255, 255, 255, 0.7); font-size: 0.9rem; margin-bottom: 0.5rem;">Injury Risk</div>
                    <div class="metric-value">{risk_percentage:.2f}%</div>
                </div>
            """, unsafe_allow_html=True)
        
        with col3:
            if risk_percentage >= 70:
                risk_level = "🔴 High Risk"
                risk_color = "#ef4444"
            elif risk_percentage >= 40:
                risk_level = "🟡 Medium Risk"
                risk_color = "#fbbf24"
            else:
                risk_level = "🟢 Low Risk"
                risk_color = "#22c55e"
            
            st.markdown(f"""
                <div class="metric-container">
                    <div style="color: rgba(255, 255, 255, 0.7); font-size: 0.9rem; margin-bottom: 0.5rem;">Risk Level</div>
                    <div style="font-size: 1.5rem; font-weight: 600; color: {risk_color};">{risk_level}</div>
                </div>
            """, unsafe_allow_html=True)
        
        # Visual gauge - Simple and Professional
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("""
            <div class="main-card">
                <h3>📊 Risk Gauge</h3>
            </div>
        """, unsafe_allow_html=True)
        
        # Determine risk color based on percentage
        if risk_percentage >= 70:
            gauge_color = "#dc2626"  # Soft red
            bg_color = "rgba(220, 38, 38, 0.1)"
        elif risk_percentage >= 40:
            gauge_color = "#ea580c"  # Soft orange
            bg_color = "rgba(234, 88, 12, 0.1)"
        else:
            gauge_color = "#16a34a"  # Soft green
            bg_color = "rgba(22, 163, 74, 0.1)"
        
        # Simple progress bar style gauge
        fig = go.Figure(go.Indicator(
            mode = "gauge+number",
            value = risk_percentage,
            domain = {'x': [0, 1], 'y': [0, 1]},
            title = {'text': "Injury Risk (%)", 'font': {'color': 'rgba(255, 255, 255, 0.9)', 'size': 18}},
            gauge = {
                'axis': {'range': [None, 100], 'tickcolor': 'rgba(255, 255, 255, 0.5)', 'tickwidth': 1},
                'bar': {'color': gauge_color, 'line': {'width': 0}},
                'steps': [
                    {'range': [0, 40], 'color': 'rgba(22, 163, 74, 0.2)'},
                    {'range': [40, 70], 'color': 'rgba(234, 88, 12, 0.2)'},
                    {'range': [70, 100], 'color': 'rgba(220, 38, 38, 0.2)'}
                ],
                'threshold': {
                    'line': {'color': gauge_color, 'width': 2},
                    'thickness': 0.6,
                    'value': risk_percentage
                },
                'bgcolor': 'rgba(0, 0, 0, 0)',
                'borderwidth': 1,
                'bordercolor': 'rgba(255, 255, 255, 0.1)'
            },
            number = {'font': {'color': 'rgba(255, 255, 255, 0.9)', 'size': 32}}
        ))
        
        fig.update_layout(
            height=280,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='rgba(255, 255, 255, 0.9)'),
            margin=dict(l=20, r=20, t=40, b=20)
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # SHAP Explanation
        explanation = result.get("explanation", {})
        
        if explanation:
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Add insight box
            insight = create_insight_text(result, "injury")
            st.markdown(f"""
                <div class="info-box">
                    <h4>⚠️ Summary</h4>
                    <p>{insight}</p>
                </div>
            """, unsafe_allow_html=True)
            
            st.markdown("""
                <div class="main-card">
                    <h3>🔍 What Causes This Injury Risk?</h3>
                    <p style="color: rgba(255, 255, 255, 0.7);">
                        Below are the factors influencing this player's injury likelihood
                    </p>
                </div>
            """, unsafe_allow_html=True)
            
            top_features = explanation.get("top_features", {})
            key_factors = explanation.get("key_factors", [])
            
            if top_features:
                # Create visualization with user-friendly labels
                df_shap = pd.DataFrame([
                    {"Feature": translate_feature_name(k), "Importance": v}
                    for k, v in top_features.items()
                ])
                
                # Sort by absolute value
                df_shap["Abs Value"] = df_shap["Importance"].abs()
                df_shap = df_shap.sort_values("Abs Value", ascending=True)
                
                # Create horizontal bar chart
                fig = go.Figure()
                
                colors = ['#ef4444' if x > 0 else '#22c55e' for x in df_shap["Importance"]]
                
                fig.add_trace(go.Bar(
                    y=df_shap["Feature"],
                    x=df_shap["Importance"],
                    orientation='h',
                    marker_color=colors,
                    text=[f"{x:.1%}" for x in df_shap["Importance"]],
                    textposition='outside',
                    textfont=dict(color='white', size=12)
                ))
                
                fig.update_layout(
                    title="Factors Contributing to Injury Risk",
                    xaxis_title="Importance (%)",
                    yaxis_title="",
                    height=400,
                    showlegend=False,
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='white'),
                    xaxis=dict(gridcolor='rgba(255, 255, 255, 0.1)'),
                    yaxis=dict(gridcolor='rgba(255, 255, 255, 0.1)')
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
                st.markdown("""
                    <div class="info-box">
                        <p style="margin: 0; font-size: 0.9rem;">
                            <strong>📊 Chart Guide:</strong> Red bars increase injury risk | Green bars decrease injury risk
                        </p>
                    </div>
                """, unsafe_allow_html=True)
                
                # Add detailed explanation
                explanation_text = format_explanation_text(explanation, "injury")
                st.markdown(f"""
                    <div class="main-card">
                        <h3>📖 Detailed Analysis</h3>
                        <p>{explanation_text}</p>
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

# JavaScript to manage sidebar visibility
st.markdown("""
<script>
    // Keep sidebar collapsed by default
    const observer = new MutationObserver(() => {
        const sidebar = document.querySelector('section[data-testid="stSidebar"]');
        const button = document.querySelector('button[aria-label="Close sidebar"]');
        
        if (sidebar && sidebar.style.display !== 'none') {
            // Sidebar is open, this is fine - Streamlit's hamburger menu controls it
        }
    });
    
    observer.observe(document.body, { subtree: true, attributes: true });
</script>
""", unsafe_allow_html=True)
