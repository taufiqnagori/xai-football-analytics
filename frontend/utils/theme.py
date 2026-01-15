"""
Theme toggle utility for all pages
"""
import streamlit as st

def init_theme():
    """Initialize theme in session state"""
    if 'theme' not in st.session_state:
        st.session_state.theme = 'dark'

def render_theme_toggle():
    """Render theme toggle button - now in sidebar by default"""
    init_theme()
    
    # This is the old function for backward compatibility
    # The actual toggle is now in the sidebar (see sidebar setup in main pages)
    pass

def render_sidebar_theme_toggle():
    """Render theme toggle in the sidebar"""
    init_theme()
    
    # Create button with unique key per page
    # Note: This function is called within a st.sidebar context, so use st.button() not st.sidebar.button()
    theme_toggle = st.button(
        "🌙 Dark" if st.session_state.theme == 'dark' else "☀️ Light",
        key="theme_toggle_sidebar",
        use_container_width=True
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
            /* Light Theme Styles - Global Override */
            * {
                color: #1a1a1a !important;
            }
            
            .stApp {
                background: white !important;
                color: #1a1a1a !important;
            }
            
            /* All text elements - force black */
            body, body * {
                color: #1a1a1a !important;
            }
            
            /* Headings */
            h1 {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                -webkit-background-clip: text;
                -webkit-text-fill-color: transparent;
                background-clip: text;
            }
            
            h2, h3, h4, h5, h6 {
                color: #1a1a1a !important;
            }
            
            /* Paragraphs and text */
            p, span, div, label, li, a {
                color: #1a1a1a !important;
            }
            
            /* Cards */
            .main-card, .nav-card, .feature-card, .team-card, .player-card, .metric-container {
                background: rgba(255, 255, 255, 0.95) !important;
                color: #1a1a1a !important;
                border: 1px solid rgba(0, 0, 0, 0.1) !important;
            }
            
            .main-card *, .nav-card *, .feature-card *, .team-card *, .player-card *, .metric-container * {
                color: #1a1a1a !important;
            }
            
            /* Selectbox/Dropdown - Light theme */
            .stSelectbox > div > div,
            .stSelectbox > div > div > button,
            div[data-baseweb="select"] > div,
            div[data-baseweb="select"] button {
                background-color: white !important;
                border: 1px solid rgba(0, 0, 0, 0.15) !important;
                color: #1a1a1a !important;
            }
            
            .stSelectbox > div > div:hover,
            .stSelectbox > div > div > button:hover,
            div[data-baseweb="select"] > div:hover,
            div[data-baseweb="select"] button:hover {
                background-color: #f5f5f5 !important;
                border-color: rgba(0, 0, 0, 0.25) !important;
            }
            
            .stSelectbox label, div[data-baseweb="select"] label {
                color: #1a1a1a !important;
            }
            
            /* Dropdown options popup - Light theme */
            ul[role="listbox"],
            div[role="listbox"],
            div[data-baseweb="popover"],
            div[data-baseweb="listbox"],
            div[data-baseweb="menu"] {
                background-color: white !important;
                border: 1px solid rgba(0, 0, 0, 0.15) !important;
            }
            
            ul[role="listbox"] li,
            ul[role="listbox"] > li,
            div[role="listbox"] li,
            div[role="listbox"] span,
            div[data-baseweb="popover"] li,
            div[data-baseweb="popover"] > div,
            div[data-baseweb="listbox"] li,
            div[data-baseweb="listbox"] > div,
            div[data-baseweb="option"],
            div[data-baseweb="option"] span,
            div[data-baseweb="menuListItem"] {
                background-color: white !important;
                color: #1a1a1a !important;
            }
            
            ul[role="listbox"] li:hover,
            ul[role="listbox"] > li:hover,
            div[role="listbox"] li:hover,
            div[role="listbox"] > div:hover,
            div[data-baseweb="popover"] li:hover,
            div[data-baseweb="popover"] > div:hover,
            div[data-baseweb="listbox"] li:hover,
            div[data-baseweb="listbox"] > div:hover,
            div[data-baseweb="option"]:hover,
            div[data-baseweb="menuListItem"]:hover {
                background-color: rgba(102, 126, 234, 0.1) !important;
                color: #1a1a1a !important;
            }
            
            /* Ensure dropdown text stays black - all child elements */
            ul[role="listbox"] li *,
            div[role="listbox"] li *,
            div[role="listbox"] *,
            div[data-baseweb="popover"] *,
            div[data-baseweb="listbox"] *,
            div[data-baseweb="option"] *,
            div[data-baseweb="menuListItem"] * {
                color: #1a1a1a !important;
                background: transparent !important;
            }
            
            /* Buttons */
            .stButton > button {
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%) !important;
                color: white !important;
                border: none !important;
            }
            
            .stButton > button:hover {
                box-shadow: 0 4px 12px rgba(102, 126, 234, 0.35) !important;
            }
            
            /* Info boxes */
            .info-box, .warning-box, .error-box, .success-box {
                color: #1a1a1a !important;
            }
            
            .info-box *, .warning-box *, .error-box *, .success-box * {
                color: #1a1a1a !important;
            }
            
            /* Page subtitles and hero text */
            .hero-subtitle, .page-subtitle {
                color: rgba(26, 26, 26, 0.8) !important;
            }
            
            .footer-text {
                color: rgba(26, 26, 26, 0.6) !important;
            }
            
            /* Sidebar */
            section[data-testid="stSidebar"] > div,
            section[data-testid="stSidebar"],
            .css-1d391kg {
                background: rgba(248, 249, 250, 0.98) !important;
                border-right: 1px solid rgba(0, 0, 0, 0.1) !important;
            }
            
            section[data-testid="stSidebar"] *,
            .css-1d391kg * {
                color: rgba(26, 26, 26, 0.9) !important;
            }
            
            /* Theme toggle button - light theme - SIMPLE & DIRECT */
            button[key="theme_toggle_sidebar"] {
                background-color: white !important;
                background: white !important;
                color: #1a1a1a !important;
                border: 1px solid rgba(0, 0, 0, 0.2) !important;
                box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1) !important;
            }
            
            button[key="theme_toggle_sidebar"]:hover {
                background-color: #f5f5f5 !important;
                background: #f5f5f5 !important;
                color: #1a1a1a !important;
                box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15) !important;
            }
            
            button[key="theme_toggle_sidebar"] * {
                color: #1a1a1a !important;
            }
            
            /* Streamlit tooltip/popover styling */
            div[role="tooltip"] {
                background: white !important;
            }
            
            div[role="tooltip"] p,
            div[role="tooltip"] span,
            div[role="tooltip"] div {
                color: #1a1a1a !important;
                background: transparent !important;
            }
            
            /* Plotly charts - comprehensive text color override for light theme */
            svg text, svg tspan {
                fill: #1a1a1a !important;
                color: #1a1a1a !important;
            }
            
            .plotly-graph-div text,
            .plotly-graph-div tspan {
                fill: #1a1a1a !important;
                color: #1a1a1a !important;
            }
            
            .plotly-graph-div .xaxislayer-above text,
            .plotly-graph-div .yaxislayer-above text,
            .plotly-graph-div .zaxislayer text,
            .plotly-graph-div .xtick text,
            .plotly-graph-div .ytick text,
            .plotly-graph-div .ztick text,
            .plotly-graph-div .gtitle,
            .plotly-graph-div .g-xtitle,
            .plotly-graph-div .g-ytitle,
            .plotly-graph-div .legendtext,
            .plotly-graph-div .hovertext {
                fill: #1a1a1a !important;
                color: #1a1a1a !important;
            }
            
            /* Input fields */
            input, textarea, select {
                background: white !important;
                color: #1a1a1a !important;
                border: 1px solid rgba(0, 0, 0, 0.15) !important;
            }
            
            input:focus, textarea:focus, select:focus {
                background: #f5f5f5 !important;
                color: #1a1a1a !important;
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
