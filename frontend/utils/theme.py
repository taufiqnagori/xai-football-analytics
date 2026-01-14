"""
Theme toggle utility for all pages
"""
import streamlit as st

def init_theme():
    """Initialize theme in session state"""
    if 'theme' not in st.session_state:
        st.session_state.theme = 'dark'

def render_theme_toggle():
    """Render theme toggle button fixed at top-right"""
    init_theme()
    
    # Create button with unique key per page
    theme_toggle = st.button(
        "🌙 Dark" if st.session_state.theme == 'dark' else "☀️ Light",
        key="theme_toggle",
        help="Toggle between Light and Dark theme"
    )
    
    if theme_toggle:
        st.session_state.theme = 'light' if st.session_state.theme == 'dark' else 'dark'
        st.rerun()

def get_theme_styles():
    """Get theme-specific styles"""
    theme = st.session_state.get('theme', 'dark')
    
    if theme == 'light':
        return """
        <style>
            /* Light Theme Styles - Global */
            .stApp {
                background: #f8f9fa !important;
            }
            .stApp[data-theme] {
                background: #f8f9fa !important;
            }
            
            /* Text colors */
            h1, h2, h3, h4, h5, h6 {
                color: #1a1a1a !important;
            }
            p, span, div, label, li {
                color: #1a1a1a !important;
            }
            .stMarkdown p, .stMarkdown span, .stMarkdown div {
                color: #1a1a1a !important;
            }
            
            /* Cards */
            .main-card {
                background: rgba(255, 255, 255, 0.95) !important;
                color: #1a1a1a !important;
                border: 1px solid rgba(0, 0, 0, 0.1) !important;
            }
            .main-card p, .main-card h3, .main-card h2, .main-card h1 {
                color: #1a1a1a !important;
            }
            
            .nav-card {
                background: rgba(255, 255, 255, 0.95) !important;
                color: #1a1a1a !important;
                border: 1px solid rgba(0, 0, 0, 0.1) !important;
            }
            .nav-card-title, .nav-card-desc {
                color: #1a1a1a !important;
            }
            
            .feature-card {
                background: rgba(255, 255, 255, 0.95) !important;
                color: #1a1a1a !important;
                border: 1px solid rgba(0, 0, 0, 0.1) !important;
            }
            .feature-card h3, .feature-card p {
                color: #1a1a1a !important;
            }
            
            .team-card {
                background: rgba(255, 255, 255, 0.95) !important;
                color: #1a1a1a !important;
                border: 1px solid rgba(0, 0, 0, 0.1) !important;
            }
            .team-card h3 {
                color: #1a1a1a !important;
            }
            
            .player-card {
                background: rgba(255, 255, 255, 0.8) !important;
                color: #1a1a1a !important;
                border-left: 4px solid #667eea !important;
            }
            .player-card p {
                color: #1a1a1a !important;
            }
            
            .metric-container {
                background: rgba(255, 255, 255, 0.95) !important;
                color: #1a1a1a !important;
                border: 1px solid rgba(0, 0, 0, 0.1) !important;
            }
            
            /* Info boxes */
            .info-box, .warning-box, .error-box, .success-box {
                color: #1a1a1a !important;
            }
            .info-box p, .warning-box p, .error-box p, .success-box p {
                color: #1a1a1a !important;
            }
            
            /* Buttons - keep gradient but ensure visibility */
            .stButton > button {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
                color: white !important;
            }
            
            /* Theme toggle button - light theme */
            button[key="theme_toggle"] {
                background: rgba(255, 255, 255, 0.9) !important;
                color: #1a1a1a !important;
                border: 1px solid rgba(0, 0, 0, 0.2) !important;
                box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1) !important;
            }
            
            button[key="theme_toggle"]:hover {
                background: rgba(255, 255, 255, 1) !important;
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15) !important;
            }
            
            /* Selectbox/Dropdown - Light theme */
            .stSelectbox > div > div,
            div[data-baseweb="select"] > div {
                background-color: rgba(255, 255, 255, 0.95) !important;
                border: 1px solid rgba(0, 0, 0, 0.15) !important;
                color: #1a1a1a !important;
            }
            
            .stSelectbox > div > div:hover,
            div[data-baseweb="select"] > div:hover {
                background-color: rgba(255, 255, 255, 1) !important;
                border-color: rgba(0, 0, 0, 0.25) !important;
            }
            
            .stSelectbox label,
            div[data-baseweb="select"] label {
                color: #1a1a1a !important;
            }
            
            /* Dropdown options */
            ul[role="listbox"],
            div[data-baseweb="popover"] {
                background-color: rgba(255, 255, 255, 0.98) !important;
                border: 1px solid rgba(0, 0, 0, 0.15) !important;
            }
            
            ul[role="listbox"] li,
            div[data-baseweb="popover"] li {
                color: #1a1a1a !important;
            }
            
            ul[role="listbox"] li:hover,
            div[data-baseweb="popover"] li:hover {
                background-color: rgba(102, 126, 234, 0.1) !important;
            }
            
            /* Selectbox text */
            .stSelectbox label {
                color: #1a1a1a !important;
            }
            
            /* Page subtitles and hero text */
            .hero-subtitle, .page-subtitle {
                color: rgba(26, 26, 26, 0.8) !important;
            }
            
            .footer-text {
                color: rgba(26, 26, 26, 0.6) !important;
            }
            
            /* Light theme sidebar */
            section[data-testid="stSidebar"] > div,
            section[data-testid="stSidebar"],
            .css-1d391kg {
                background: rgba(248, 249, 250, 0.98) !important;
                backdrop-filter: blur(10px) !important;
                border-right: 1px solid rgba(0, 0, 0, 0.1) !important;
            }
            
            section[data-testid="stSidebar"] *,
            .css-1d391kg * {
                color: rgba(26, 26, 26, 0.9) !important;
            }
        </style>
        """
    else:
        # Dark theme - ensure text is visible
        return """
        <style>
            .hero-subtitle, .page-subtitle {
                color: rgba(255, 255, 255, 0.8) !important;
            }
            .footer-text {
                color: rgba(255, 255, 255, 0.6) !important;
            }
            
            /* Theme toggle button - dark theme */
            button[key="theme_toggle"] {
                background: rgba(0, 0, 0, 0.4) !important;
                color: white !important;
                border: 1px solid rgba(255, 255, 255, 0.2) !important;
                backdrop-filter: blur(10px) !important;
            }
            
            button[key="theme_toggle"]:hover {
                background: rgba(0, 0, 0, 0.5) !important;
                border-color: rgba(255, 255, 255, 0.3) !important;
            }
            
            /* Selectbox/Dropdown - Dark theme */
            .stSelectbox > div > div,
            div[data-baseweb="select"] > div {
                background-color: rgba(255, 255, 255, 0.1) !important;
                border: 1px solid rgba(255, 255, 255, 0.2) !important;
                color: white !important;
            }
            
            .stSelectbox > div > div:hover,
            div[data-baseweb="select"] > div:hover {
                background-color: rgba(255, 255, 255, 0.15) !important;
                border-color: rgba(255, 255, 255, 0.3) !important;
            }
            
            .stSelectbox label,
            div[data-baseweb="select"] label {
                color: rgba(255, 255, 255, 0.9) !important;
            }
            
            /* Dropdown options - dark theme */
            ul[role="listbox"],
            div[data-baseweb="popover"] {
                background-color: rgba(20, 18, 45, 0.98) !important;
                border: 1px solid rgba(255, 255, 255, 0.1) !important;
            }
            
            ul[role="listbox"] li,
            div[data-baseweb="popover"] li {
                color: rgba(255, 255, 255, 0.9) !important;
            }
            
            ul[role="listbox"] li:hover,
            div[data-baseweb="popover"] li:hover {
                background-color: rgba(102, 126, 234, 0.2) !important;
            }
            
            /* Dark theme sidebar */
            section[data-testid="stSidebar"] > div,
            section[data-testid="stSidebar"],
            .css-1d391kg {
                background: rgba(20, 18, 45, 0.98) !important;
                backdrop-filter: blur(10px) !important;
                border-right: 1px solid rgba(255, 255, 255, 0.08) !important;
            }
            
            section[data-testid="stSidebar"] *,
            .css-1d391kg * {
                color: rgba(255, 255, 255, 0.9) !important;
            }
        </style>
        """
