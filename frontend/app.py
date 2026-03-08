import streamlit as st
import os

# Page configuration
st.set_page_config(
    page_title="XAI Football Analytics Suite",
    page_icon="⚽",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Load CSS
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
CSS_PATH = os.path.join(BASE_DIR, "style.css")

# Google Search Console verification
st.markdown('<meta name="google-site-verification" content="-6CECMNOpUVkGgAZHeI2h-UNyzCjU40HCvkQVCui_Yo" />', unsafe_allow_html=True)
st.markdown('<meta name="viewport" content="width=device-width, initial-scale=1.0">', unsafe_allow_html=True)

# Load CSS
with open(CSS_PATH, encoding='utf-8') as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# ================================
# THEME TOGGLE
# ================================
from utils.theme import init_theme, render_sidebar_theme_toggle, get_theme_styles

init_theme()

# Sidebar navigation and theme toggle
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

# ================================
# HOME PAGE
# ================================

# Hero Section
theme = st.session_state.get('theme', 'dark')
text_color = '#1a1a1a' if theme == 'light' else 'white'
subtitle_color = '#1a1a1a' if theme == 'light' else 'rgba(255, 255, 255, 0.8)'

st.markdown(f"""
    <div style="text-align: center; padding: 0.2rem 0 0.3rem 0;">
        <h1 style="font-size: 3.5rem; margin-bottom: 0.3rem; display: inline-block; white-space: normal; word-wrap: break-word; background: none; -webkit-text-fill-color: {text_color}; color: {text_color};">⚽ XAI Football Analytics Suite</h1>
        <p class="hero-subtitle" style="font-size: 1.3rem; margin-bottom: 0.5rem; color: {subtitle_color};">
            AI-Powered Player Performance, Injury Risk & Match Outcome Prediction<br>
            <span style="color: #667eea;">Powered by SHAP & LIME Explanations</span>
        </p>
    </div>
""", unsafe_allow_html=True)

# Main Feature Cards
st.markdown("<br>", unsafe_allow_html=True)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("""
        <div class="nav-card slide-in">
            <div class="nav-card-icon">📈</div>
            <div class="nav-card-title">Player Performance</div>
            <div class="nav-card-desc">
                Predict player performance scores using advanced ML models with XAI explanations
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    if st.button("🚀 Analyze Performance", key="nav_perf", use_container_width=True):
        st.switch_page("pages/1_Performance_Analysis.py")

with col2:
    st.markdown("""
        <div class="nav-card slide-in">
            <div class="nav-card-icon">🩺</div>
            <div class="nav-card-title">Injury Risk</div>
            <div class="nav-card-desc">
                Assess injury risk probability for players with detailed risk factors analysis
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    if st.button("🚀 Assess Injury Risk", key="nav_injury", use_container_width=True):
        st.switch_page("pages/2_Injury_Risk_Analysis.py")

with col3:
    st.markdown("""
        <div class="nav-card slide-in">
            <div class="nav-card-icon">🏆</div>
            <div class="nav-card-title">Match Prediction</div>
            <div class="nav-card-desc">
                Predict match outcomes between teams with AI-powered analytics and explanations
            </div>
        </div>
    """, unsafe_allow_html=True)
    
    if st.button("🚀 Predict Match", key="nav_match", use_container_width=True):
        st.switch_page("pages/3_Match_Outcome_Prediction.py")

# Features Section
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("---")
st.markdown("""
    <div style="padding: 2rem 0;">
        <h2 style="text-align: center; margin-bottom: 2rem;">✨ Key Features</h2>
    </div>
""", unsafe_allow_html=True)

feature_col1, feature_col2 = st.columns(2)

with feature_col1:
    st.markdown("""
        <div class="feature-card">
            <h3>🤖 Machine Learning Models</h3>
            <p>Advanced Random Forest models trained on comprehensive football datasets</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
        <div class="feature-card">
            <h3>📊 SHAP Explanations</h3>
            <p>Understand model predictions with SHAP (SHapley Additive exPlanations) values</p>
        </div>
    """, unsafe_allow_html=True)

with feature_col2:
    st.markdown("""
        <div class="feature-card">
            <h3>🎯 Accurate Predictions</h3>
            <p>Get reliable performance scores, injury risks, and match outcome probabilities</p>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
        <div class="feature-card">
            <h3>💡 Transparent AI</h3>
            <p>Every prediction comes with detailed explanations of contributing factors</p>
        </div>
    """, unsafe_allow_html=True)

# Footer
st.markdown("<br><br>", unsafe_allow_html=True)
st.markdown("---")
st.markdown("""
    <div style="text-align: center; padding: 2rem 0; color: rgba(255, 255, 255, 0.6);">
        <p class="footer-text">Built with ❤️ using Streamlit, FastAPI, and XAI Technologies</p>
        <p class="footer-text" style="font-size: 0.9rem;">© 2026 XAI Football Analytics Suite</p>
    </div>
""", unsafe_allow_html=True)

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
