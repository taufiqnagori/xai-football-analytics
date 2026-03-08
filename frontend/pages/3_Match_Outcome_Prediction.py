import streamlit as st
from utils.api_client import get_teams, get_default_squad, get_team_players, get_players, predict_match
from utils.explanation_helper import translate_feature_name, create_insight_text, format_explanation_text
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import time

# Page config
st.set_page_config(
    page_title="Match Prediction",
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
theme = st.session_state.get('theme', 'dark')
text_color = '#1a1a1a' if theme == 'light' else 'white'
subtitle_color = '#1a1a1a' if theme == 'light' else 'rgba(255, 255, 255, 0.8)'

st.markdown(f"""
    <div style="text-align: center; padding: 2rem 0;">
        <h1 style="background: none; -webkit-text-fill-color: {text_color}; color: {text_color}; display: inline-block; white-space: normal; word-wrap: break-word; font-size: 2.5rem; margin: 0; font-weight: 700;">🏆 Match Outcome Prediction</h1>
        <p class="page-subtitle" style="font-size: 1.2rem; color: {subtitle_color};">
            Predict match results with AI-powered analytics and XAI explanations
        </p>
    </div>
""", unsafe_allow_html=True)

st.markdown("---")

# Initialize session state
if 'team_a' not in st.session_state:
    st.session_state.team_a = None
if 'team_b' not in st.session_state:
    st.session_state.team_b = None
if 'team_a_squad' not in st.session_state:
    st.session_state.team_a_squad = []
if 'team_b_squad' not in st.session_state:
    st.session_state.team_b_squad = []
if 'team_a_players_list' not in st.session_state:
    st.session_state.team_a_players_list = []
if 'team_b_players_list' not in st.session_state:
    st.session_state.team_b_players_list = []
if 'match_prediction_result' not in st.session_state:
    st.session_state.match_prediction_result = None

# Get teams
teams = get_teams()
if not teams:
    st.markdown("""
        <div class="error-box">
            <h3>⚠️ Connection Error</h3>
            <p>Could not load teams. Make sure the backend API is running.</p>
        </div>
    """, unsafe_allow_html=True)
    st.info("""
    **The backend API is waking up.** On free hosting, the first request can take up to 30 seconds.
    Please refresh the page in a moment.
    """)
    st.stop()

# Get all players for dropdown
all_players = get_players()

# Team Selection Section
st.markdown("""
    <div class="main-card">
        <h2>🏆 Select Teams</h2>
        <p style="color: rgba(255, 255, 255, 0.7);">
            Choose two teams and their squads. Default Playing XI will be auto-filled, but you can customize any player.
        </p>
    </div>
""", unsafe_allow_html=True)

col1, col2 = st.columns(2)

with col1:
    st.markdown("""
        <div class="team-card">
            <h3>🟦 Team A</h3>
        </div>
    """, unsafe_allow_html=True)
    team_a_selected = st.selectbox(
        "Choose Team A",
        [None] + teams,
        key="team_a_select",
        index=0 if st.session_state.team_a is None else teams.index(st.session_state.team_a) + 1 if st.session_state.team_a in teams else 0
    )
    
    if team_a_selected and team_a_selected != st.session_state.team_a:
        st.session_state.team_a = team_a_selected
        st.session_state.match_prediction_result = None  # Clear old prediction
        # Load default squad
        squad_data = get_default_squad(team_a_selected)
        st.session_state.team_a_squad = squad_data.get("squad", [])
        # Load all team players for dropdown
        st.session_state.team_a_players_list = get_team_players(team_a_selected)

with col2:
    st.markdown("""
        <div class="team-card">
            <h3>🟥 Team B</h3>
        </div>
    """, unsafe_allow_html=True)
    team_b_selected = st.selectbox(
        "Choose Team B",
        [None] + teams,
        key="team_b_select",
        index=0 if st.session_state.team_b is None else teams.index(st.session_state.team_b) + 1 if st.session_state.team_b in teams else 0
    )
    
    if team_b_selected and team_b_selected != st.session_state.team_b:
        st.session_state.team_b = team_b_selected
        st.session_state.match_prediction_result = None  # Clear old prediction
        # Load default squad
        squad_data = get_default_squad(team_b_selected)
        st.session_state.team_b_squad = squad_data.get("squad", [])
        # Load all team players for dropdown
        st.session_state.team_b_players_list = get_team_players(team_b_selected)

# Validation: Same team selected
if st.session_state.team_a and st.session_state.team_b:
    if st.session_state.team_a == st.session_state.team_b:
        st.markdown("""
            <div class="error-box">
                <h3>❌ Error</h3>
                <p>Both teams cannot be the same! Please select different teams.</p>
            </div>
        """, unsafe_allow_html=True)
        st.stop()

# Squad Management Section
if st.session_state.team_a or st.session_state.team_b:
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
        <div class="main-card">
            <h2>👥 Manage Squads</h2>
            <p style="color: rgba(255, 255, 255, 0.7);">
                Default Playing XI is auto-filled. You can change any player using the dropdowns below.
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    # Team A Squad
    with col1:
        if st.session_state.team_a:
            st.markdown(f"""
                <div class="team-card">
                    <h3>🟦 {st.session_state.team_a} Squad</h3>
                </div>
            """, unsafe_allow_html=True)
            
            # Ensure squad has 11 players
            while len(st.session_state.team_a_squad) < 11:
                st.session_state.team_a_squad.append(None)
            st.session_state.team_a_squad = st.session_state.team_a_squad[:11]
            
            # Get available players for Team A (ONLY team-specific players)
            team_a_available = st.session_state.team_a_players_list if isinstance(st.session_state.team_a_players_list, list) and (not st.session_state.team_a_players_list or isinstance(st.session_state.team_a_players_list[0], str)) else []
            available_for_a = sorted(team_a_available)  # Only team A players
            
            if not available_for_a:
                st.warning(f"⚠️ No players found for {st.session_state.team_a}")
            else:
                new_squad_a = []
                for i in range(11):
                    current_player = st.session_state.team_a_squad[i] if i < len(st.session_state.team_a_squad) else None
                    
                    # Format player name for display
                    def format_player_name(x):
                        if not x:
                            return "Select Player"
                        return x
                    
                    # Get current index safely
                    try:
                        current_index = available_for_a.index(current_player) + 1 if current_player and current_player in available_for_a else 0
                    except (ValueError, IndexError):
                        current_index = 0
                    
                    selected = st.selectbox(
                        f"Player {i+1}",
                        [None] + available_for_a,
                        key=f"team_a_player_{i}",
                        index=current_index,
                        format_func=format_player_name
                    )
                    
                    if selected:
                        new_squad_a.append(selected)
                
                st.session_state.team_a_squad = new_squad_a
                
                # Squad summary
                if len(st.session_state.team_a_squad) == 11:
                    st.markdown(f"""
                        <div class="success-box">
                            <p>✅ {st.session_state.team_a}: 11 players selected</p>
                        </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                        <div class="warning-box">
                            <p>⚠️ {st.session_state.team_a}: {len(st.session_state.team_a_squad)}/11 players</p>
                        </div>
                    """, unsafe_allow_html=True)
    
    # Team B Squad
    with col2:
        if st.session_state.team_b:
            st.markdown(f"""
                <div class="team-card">
                    <h3>🟥 {st.session_state.team_b} Squad</h3>
                </div>
            """, unsafe_allow_html=True)
            
            # Ensure squad has 11 players
            while len(st.session_state.team_b_squad) < 11:
                st.session_state.team_b_squad.append(None)
            st.session_state.team_b_squad = st.session_state.team_b_squad[:11]
            
            # Get available players for Team B (ONLY team-specific players)
            team_b_available = st.session_state.team_b_players_list if isinstance(st.session_state.team_b_players_list, list) and (not st.session_state.team_b_players_list or isinstance(st.session_state.team_b_players_list[0], str)) else []
            available_for_b = sorted(team_b_available)  # Only team B players
            
            if not available_for_b:
                st.warning(f"⚠️ No players found for {st.session_state.team_b}")
            else:
                new_squad_b = []
                for i in range(11):
                    current_player = st.session_state.team_b_squad[i] if i < len(st.session_state.team_b_squad) else None
                    
                    # Format player name for display
                    def format_player_name_b(x):
                        if not x:
                            return "Select Player"
                        return x
                    
                    # Get current index safely
                    try:
                        current_index = available_for_b.index(current_player) + 1 if current_player and current_player in available_for_b else 0
                    except (ValueError, IndexError):
                        current_index = 0
                    
                    selected = st.selectbox(
                        f"Player {i+1}",
                        [None] + available_for_b,
                        key=f"team_b_player_{i}",
                        index=current_index,
                        format_func=format_player_name_b
                    )
                    
                    if selected:
                        new_squad_b.append(selected)
                
                st.session_state.team_b_squad = new_squad_b
                
                # Squad summary
                if len(st.session_state.team_b_squad) == 11:
                    st.markdown(f"""
                        <div class="success-box">
                            <p>✅ {st.session_state.team_b}: 11 players selected</p>
                        </div>
                    """, unsafe_allow_html=True)
                else:
                    st.markdown(f"""
                        <div class="warning-box">
                            <p>⚠️ {st.session_state.team_b}: {len(st.session_state.team_b_squad)}/11 players</p>
                        </div>
                    """, unsafe_allow_html=True)

# Validation checks
validation_errors = []
if st.session_state.team_a and st.session_state.team_b:
    if len(st.session_state.team_a_squad) != 11:
        validation_errors.append(f"{st.session_state.team_a} must have exactly 11 players (currently {len(st.session_state.team_a_squad)})")
    if len(st.session_state.team_b_squad) != 11:
        validation_errors.append(f"{st.session_state.team_b} must have exactly 11 players (currently {len(st.session_state.team_b_squad)})")
    
    # Check for duplicate players
    common_players = set(st.session_state.team_a_squad) & set(st.session_state.team_b_squad)
    if common_players:
        validation_errors.append(f"Players cannot be in both teams: {', '.join(common_players)}")
    
    # Check for None values
    if None in st.session_state.team_a_squad:
        validation_errors.append(f"{st.session_state.team_a} has empty player slots")
    if None in st.session_state.team_b_squad:
        validation_errors.append(f"{st.session_state.team_b} has empty player slots")

# Prediction Button
st.markdown("---")
col1, col2, col3 = st.columns([1, 2, 1])

with col2:
    predict_button = st.button(
        "🚀 Predict Match Outcome",
        key="predict_btn",
        type="primary",
        use_container_width=True
    )

if predict_button:
    # Show validation errors
    if validation_errors:
        for error in validation_errors:
            st.markdown(f"""
                <div class="error-box">
                    <p>❌ {error}</p>
                </div>
            """, unsafe_allow_html=True)
        st.stop()
    
    # Show loading animation
    with st.spinner("🔮 Analyzing teams and predicting match outcome..."):
        time.sleep(0.5)  # Small delay for UX
        result = predict_match(st.session_state.team_a_squad, st.session_state.team_b_squad)
    
    # Save result to session state for persistence across reruns
    if result and "error" not in result:
        st.session_state.match_prediction_result = result
        st.success("✓ Prediction complete!")
    else:
        # Check if result is valid
        if not result:
            st.error("❌ No result returned from prediction")
        elif "error" in result:
            st.error(f"❌ Error: {result['error']}")

# Display results from session state if prediction was made previously  
if st.session_state.match_prediction_result is not None:
    result = st.session_state.match_prediction_result
    
    team_a_prob = float(result.get("team_a_win_probability", 0))
    team_b_prob = float(result.get("team_b_win_probability", 0))
    predicted_winner = str(result.get("predicted_winner", "Unknown"))
    winner_team_name = st.session_state.team_a if predicted_winner == "Team A" else st.session_state.team_b
    team_a_stats = result.get("team_a_stats", {})
    team_b_stats = result.get("team_b_stats", {})
    
    # ============================================================================
    # RESULTS SECTION - CONSISTENT WITH OTHER DASHBOARDS
    # ============================================================================
    st.markdown("---")
    st.markdown("""
        <div class="prediction-result slide-in">
            <h2>🎯 Prediction Results</h2>
        </div>
    """, unsafe_allow_html=True)
    
    # VS Banner - Visual head-to-head display
    team_a_color = "#3498db"
    team_b_color = "#ef4444"
    st.markdown(f"""
        <div style="display: flex; align-items: center; justify-content: center; gap: 1.5rem; padding: 1.5rem 2rem; margin: 0.5rem 0 1.5rem 0;
                    background: linear-gradient(135deg, rgba(52,152,219,0.12) 0%, rgba(0,0,0,0) 40%, rgba(0,0,0,0) 60%, rgba(239,68,68,0.12) 100%);
                    border-radius: 20px; border: 1px solid rgba(255,255,255,0.06);">
            <div style="text-align: center; flex: 1;">
                <div style="font-size: 2.4rem; font-weight: 800; color: {team_a_color}; letter-spacing: -0.5px; line-height: 1.2;">{st.session_state.team_a}</div>
                <div style="font-size: 1.6rem; font-weight: 700; color: rgba(52,152,219,0.8); margin-top: 0.2rem;">{team_a_prob:.1f}%</div>
            </div>
            <div style="text-align: center; flex-shrink: 0;">
                <div style="width: 72px; height: 72px; border-radius: 50%; border: 2px solid rgba(255,255,255,0.15);
                            display: flex; align-items: center; justify-content: center;
                            background: rgba(255,255,255,0.04);">
                    <span style="font-size: 1.4rem; font-weight: 900; color: rgba(255,255,255,0.25); letter-spacing: 3px;">VS</span>
                </div>
            </div>
            <div style="text-align: center; flex: 1;">
                <div style="font-size: 2.4rem; font-weight: 800; color: {team_b_color}; letter-spacing: -0.5px; line-height: 1.2;">{st.session_state.team_b}</div>
                <div style="font-size: 1.6rem; font-weight: 700; color: rgba(239,68,68,0.8); margin-top: 0.2rem;">{team_b_prob:.1f}%</div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    # Metrics Row - Match Prediction Results
    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(f"""
            <div class="metric-container">
                <div style="color: rgba(255, 255, 255, 0.7); font-size: 0.9rem; margin-bottom: 0.5rem;">Match Up</div>
                <div style="font-size: 1.3rem; font-weight: 600; color: white;">{st.session_state.team_a} vs {st.session_state.team_b}</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
            <div class="metric-container">
                <div style="color: rgba(255, 255, 255, 0.7); font-size: 0.9rem; margin-bottom: 0.5rem;">Predicted Winner</div>
                <div class="metric-value">{winner_team_name}</div>
            </div>
        """, unsafe_allow_html=True)
    
    with col3:
        winner_prob = team_a_prob if predicted_winner == "Team A" else team_b_prob
        st.markdown(f"""
            <div class="metric-container">
                <div style="color: rgba(255, 255, 255, 0.7); font-size: 0.9rem; margin-bottom: 0.5rem;">Win Probability</div>
                <div class="metric-value">{winner_prob:.1f}%</div>
            </div>
        """, unsafe_allow_html=True)
    
    # Win Probability Chart
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
        <div class="main-card">
            <h3>📊 Win Probability Comparison</h3>
        </div>
    """, unsafe_allow_html=True)
    
    # Create win probability bar chart
    fig_prob = go.Figure()
    
    fig_prob.add_trace(go.Bar(
        x=[st.session_state.team_a],
        y=[team_a_prob],
        marker_color='#3498db',
        text=[f"{team_a_prob:.1f}%"],
        textposition='outside',
        textfont=dict(size=14, color='white'),
        hovertemplate=f"<b>{st.session_state.team_a}</b><br>Win Probability: %{{y:.1f}}%<extra></extra>"
    ))
    
    fig_prob.add_trace(go.Bar(
        x=[st.session_state.team_b],
        y=[team_b_prob],
        marker_color='#ef4444',
        text=[f"{team_b_prob:.1f}%"],
        textposition='outside',
        textfont=dict(size=14, color='white'),
        hovertemplate=f"<b>{st.session_state.team_b}</b><br>Win Probability: %{{y:.1f}}%<extra></extra>"
    ))
    
    fig_prob.update_layout(
        xaxis_title="",
        yaxis_title="Win Probability (%)",
        yaxis_range=[0, 105],
        height=280,
        showlegend=False,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white', size=11),
        margin=dict(t=20, b=40, l=60, r=40),
        xaxis=dict(showgrid=False, zeroline=False, showline=False),
        yaxis=dict(showgrid=True, gridwidth=1, gridcolor='rgba(255,255,255,0.08)', zeroline=False, showline=False)
    )
    
    st.plotly_chart(fig_prob, use_container_width=True, key='session_win_prob')

    # Win Probability Donut Chart
    donut_col1, donut_col2 = st.columns([1, 1])

    with donut_col1:
        fig_donut = go.Figure(data=[go.Pie(
            labels=[st.session_state.team_a, st.session_state.team_b],
            values=[team_a_prob, team_b_prob],
            hole=0.6,
            marker=dict(colors=['#3498db', '#ef4444'], line=dict(color='rgba(0,0,0,0.3)', width=2)),
            textinfo='label+percent',
            textfont=dict(size=13, color='white'),
            hovertemplate="<b>%{label}</b><br>Win Probability: %{value:.1f}%<extra></extra>"
        )])
        fig_donut.update_layout(
            height=320,
            showlegend=False,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white'),
            margin=dict(t=30, b=30, l=30, r=30),
            annotations=[dict(
                text=f"<b>{winner_team_name}</b><br>Wins",
                x=0.5, y=0.5, font_size=16, font_color='white',
                showarrow=False
            )]
        )
        st.plotly_chart(fig_donut, use_container_width=True, key='win_donut')

    with donut_col2:
        # Probability breakdown with visual bars
        st.markdown(f"""
            <div style="padding: 1.5rem 1rem;">
                <h4 style="color: white !important; margin-bottom: 1.5rem; font-size: 1.1rem;">Win Probability Breakdown</h4>
                <div style="margin-bottom: 1.2rem;">
                    <div style="display: flex; justify-content: space-between; margin-bottom: 0.4rem;">
                        <span style="color: #3498db; font-weight: 600;">{st.session_state.team_a}</span>
                        <span style="color: #3498db; font-weight: 700;">{team_a_prob:.1f}%</span>
                    </div>
                    <div style="background: rgba(255,255,255,0.08); border-radius: 8px; height: 14px; overflow: hidden;">
                        <div style="background: linear-gradient(90deg, #3498db, #2980b9); width: {team_a_prob}%; height: 100%; border-radius: 8px; transition: width 0.5s;"></div>
                    </div>
                </div>
                <div style="margin-bottom: 1.2rem;">
                    <div style="display: flex; justify-content: space-between; margin-bottom: 0.4rem;">
                        <span style="color: #ef4444; font-weight: 600;">{st.session_state.team_b}</span>
                        <span style="color: #ef4444; font-weight: 700;">{team_b_prob:.1f}%</span>
                    </div>
                    <div style="background: rgba(255,255,255,0.08); border-radius: 8px; height: 14px; overflow: hidden;">
                        <div style="background: linear-gradient(90deg, #ef4444, #dc2626); width: {team_b_prob}%; height: 100%; border-radius: 8px; transition: width 0.5s;"></div>
                    </div>
                </div>
                <div style="margin-top: 1.5rem; padding: 1rem; background: rgba(255,255,255,0.04); border-radius: 12px; border: 1px solid rgba(255,255,255,0.08);">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <span style="color: rgba(255,255,255,0.6); font-size: 0.85rem;">Probability Margin</span>
                        <span style="color: white; font-weight: 700; font-size: 1.3rem;">{abs(team_a_prob - team_b_prob):.1f}%</span>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)

    # Team Statistics Comparison
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
        <div class="main-card">
            <h3>📊 Team Statistics Comparison</h3>
        </div>
    """, unsafe_allow_html=True)
    
    col1, col2 = st.columns(2, gap="medium")
    
    with col1:
        st.markdown(f"""
            <div class="main-card">
                <h4 style="color: #3498db; margin: 0 0 1.5rem 0;">■ {st.session_state.team_a}</h4>
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1.5rem;">
                    <div>
                        <p style="margin: 0 0 0.5rem 0; font-size: 0.75rem; color: rgba(255, 255, 255, 0.55); font-weight: 600;">Avg Performance</p>
                        <p style="margin: 0; font-size: 1.6rem; font-weight: 700; color: #3498db;">{team_a_stats.get('avg_performance', 0):.2f}</p>
                    </div>
                    <div>
                        <p style="margin: 0 0 0.5rem 0; font-size: 0.75rem; color: rgba(255, 255, 255, 0.55); font-weight: 600;">Avg Injury Risk</p>
                        <p style="margin: 0; font-size: 1.6rem; font-weight: 700; color: #3498db;">{team_a_stats.get('avg_injury_risk', 0):.2f}</p>
                    </div>
                    <div>
                        <p style="margin: 0 0 0.5rem 0; font-size: 0.75rem; color: rgba(255, 255, 255, 0.55); font-weight: 600;">Total Goals</p>
                        <p style="margin: 0; font-size: 1.6rem; font-weight: 700; color: #3498db;">{int(team_a_stats.get('total_goals', 0))}</p>
                    </div>
                    <div>
                        <p style="margin: 0 0 0.5rem 0; font-size: 0.75rem; color: rgba(255, 255, 255, 0.55); font-weight: 600;">Total Assists</p>
                        <p style="margin: 0; font-size: 1.6rem; font-weight: 700; color: #3498db;">{int(team_a_stats.get('total_assists', 0))}</p>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown(f"""
            <div class="main-card">
                <h4 style="color: #ef4444; margin: 0 0 1.5rem 0;">■ {st.session_state.team_b}</h4>
                <div style="display: grid; grid-template-columns: 1fr 1fr; gap: 1.5rem;">
                    <div>
                        <p style="margin: 0 0 0.5rem 0; font-size: 0.75rem; color: rgba(255, 255, 255, 0.55); font-weight: 600;">Avg Performance</p>
                        <p style="margin: 0; font-size: 1.6rem; font-weight: 700; color: #ef4444;">{team_b_stats.get('avg_performance', 0):.2f}</p>
                    </div>
                    <div>
                        <p style="margin: 0 0 0.5rem 0; font-size: 0.75rem; color: rgba(255, 255, 255, 0.55); font-weight: 600;">Avg Injury Risk</p>
                        <p style="margin: 0; font-size: 1.6rem; font-weight: 700; color: #ef4444;">{team_b_stats.get('avg_injury_risk', 0):.2f}</p>
                    </div>
                    <div>
                        <p style="margin: 0 0 0.5rem 0; font-size: 0.75rem; color: rgba(255, 255, 255, 0.55); font-weight: 600;">Total Goals</p>
                        <p style="margin: 0; font-size: 1.6rem; font-weight: 700; color: #ef4444;">{int(team_b_stats.get('total_goals', 0))}</p>
                    </div>
                    <div>
                        <p style="margin: 0 0 0.5rem 0; font-size: 0.75rem; color: rgba(255, 255, 255, 0.55); font-weight: 600;">Total Assists</p>
                        <p style="margin: 0; font-size: 1.6rem; font-weight: 700; color: #ef4444;">{int(team_b_stats.get('total_assists', 0))}</p>
                    </div>
                </div>
            </div>
        """, unsafe_allow_html=True)
    
    # Radar Chart - Visual Team Comparison
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
        <div class="main-card">
            <h3>🕸️ Team Comparison Radar</h3>
            <p style="color: rgba(255, 255, 255, 0.7);">Visual comparison of key team metrics</p>
        </div>
    """, unsafe_allow_html=True)

    # Normalize stats for radar chart (0-100 scale)
    perf_a = team_a_stats.get('avg_performance', 0)
    perf_b = team_b_stats.get('avg_performance', 0)
    injury_a = team_a_stats.get('avg_injury_risk', 0)
    injury_b = team_b_stats.get('avg_injury_risk', 0)
    goals_a = team_a_stats.get('total_goals', 0)
    goals_b = team_b_stats.get('total_goals', 0)
    assists_a = team_a_stats.get('total_assists', 0)
    assists_b = team_b_stats.get('total_assists', 0)

    # Scale values to comparable range for radar
    max_goals = max(goals_a, goals_b, 1)
    max_assists = max(assists_a, assists_b, 1)

    radar_categories = ['Performance', 'Fitness', 'Goals', 'Assists', 'Win Chance']

    radar_a = [
        perf_a,
        max(0, (1 - injury_a) * 100),
        (goals_a / max_goals) * 100,
        (assists_a / max_assists) * 100,
        team_a_prob
    ]
    radar_b = [
        perf_b,
        max(0, (1 - injury_b) * 100),
        (goals_b / max_goals) * 100,
        (assists_b / max_assists) * 100,
        team_b_prob
    ]

    fig_radar = go.Figure()
    fig_radar.add_trace(go.Scatterpolar(
        r=radar_a + [radar_a[0]],
        theta=radar_categories + [radar_categories[0]],
        fill='toself',
        fillcolor='rgba(52, 152, 219, 0.15)',
        line=dict(color='#3498db', width=2),
        name=st.session_state.team_a,
        hovertemplate="%{theta}: %{r:.1f}<extra>" + st.session_state.team_a + "</extra>"
    ))
    fig_radar.add_trace(go.Scatterpolar(
        r=radar_b + [radar_b[0]],
        theta=radar_categories + [radar_categories[0]],
        fill='toself',
        fillcolor='rgba(239, 68, 68, 0.15)',
        line=dict(color='#ef4444', width=2),
        name=st.session_state.team_b,
        hovertemplate="%{theta}: %{r:.1f}<extra>" + st.session_state.team_b + "</extra>"
    ))
    fig_radar.update_layout(
        polar=dict(
            bgcolor='rgba(0,0,0,0)',
            radialaxis=dict(visible=True, range=[0, 100], showticklabels=False, gridcolor='rgba(255,255,255,0.08)'),
            angularaxis=dict(gridcolor='rgba(255,255,255,0.08)', color='rgba(255,255,255,0.7)')
        ),
        showlegend=True,
        legend=dict(
            orientation="h", yanchor="bottom", y=-0.15, xanchor="center", x=0.5,
            font=dict(color='white', size=12)
        ),
        height=420,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        margin=dict(t=40, b=60, l=80, r=80)
    )
    st.plotly_chart(fig_radar, use_container_width=True, key='team_radar')

    # Head-to-Head Stat Bars
    st.markdown("""
        <div class="main-card">
            <h3>📏 Head-to-Head Comparison</h3>
        </div>
    """, unsafe_allow_html=True)

    h2h_stats = [
        ("Performance", perf_a, perf_b, f"{perf_a:.1f}", f"{perf_b:.1f}"),
        ("Fitness (1 - Injury Risk)", max(0, (1 - injury_a) * 100), max(0, (1 - injury_b) * 100), f"{max(0, (1 - injury_a) * 100):.0f}%", f"{max(0, (1 - injury_b) * 100):.0f}%"),
        ("Total Goals", goals_a, goals_b, str(int(goals_a)), str(int(goals_b))),
        ("Total Assists", assists_a, assists_b, str(int(assists_a)), str(int(assists_b))),
    ]

    for stat_name, val_a, val_b, disp_a, disp_b in h2h_stats:
        total = val_a + val_b if (val_a + val_b) > 0 else 1
        pct_a = (val_a / total) * 100
        pct_b = (val_b / total) * 100
        winner_a = "font-weight: 700;" if val_a > val_b else ""
        winner_b = "font-weight: 700;" if val_b > val_a else ""
        st.markdown(f"""
            <div style="margin-bottom: 1rem; padding: 0.8rem 1rem; background: rgba(255,255,255,0.02); border-radius: 10px;">
                <div style="display: flex; justify-content: space-between; align-items: center; margin-bottom: 0.4rem;">
                    <span style="color: #3498db; font-size: 0.95rem; {winner_a}">{disp_a}</span>
                    <span style="color: rgba(255,255,255,0.5); font-size: 0.8rem; font-weight: 600;">{stat_name}</span>
                    <span style="color: #ef4444; font-size: 0.95rem; {winner_b}">{disp_b}</span>
                </div>
                <div style="display: flex; height: 8px; border-radius: 4px; overflow: hidden; gap: 3px;">
                    <div style="background: #3498db; width: {pct_a}%; border-radius: 4px;"></div>
                    <div style="background: #ef4444; width: {pct_b}%; border-radius: 4px;"></div>
                </div>
            </div>
        """, unsafe_allow_html=True)

    # ============================================================================
    # DETAILED MATCH ANALYSIS - SIMPLE & EASY TO UNDERSTAND
    # ============================================================================
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Generate detailed analysis based on team stats
    def generate_match_analysis(team_a_name, team_b_name, team_a_stats, team_b_stats, team_a_prob, team_b_prob):
        """Generate human-readable match analysis based on team statistics"""
        
        perf_a = team_a_stats.get('avg_performance', 0)
        perf_b = team_b_stats.get('avg_performance', 0)
        injury_a = team_a_stats.get('avg_injury_risk', 0)
        injury_b = team_b_stats.get('avg_injury_risk', 0)
        goals_a = team_a_stats.get('total_goals', 0)
        goals_b = team_b_stats.get('total_goals', 0)
        assists_a = team_a_stats.get('total_assists', 0)
        assists_b = team_b_stats.get('total_assists', 0)
        
        analysis = []
        
        # Performance analysis
        if perf_a > perf_b:
            perf_diff = ((perf_a - perf_b) / perf_b * 100) if perf_b > 0 else 0
            analysis.append(f"✓ {team_a_name} has **stronger player performance** - players are in better form with {perf_diff:.0f}% higher average performance rating")
        else:
            perf_diff = ((perf_b - perf_a) / perf_a * 100) if perf_a > 0 else 0
            analysis.append(f"✓ {team_b_name} has **stronger player performance** - players are in better form with {perf_diff:.0f}% higher average performance rating")
        
        # Injury analysis
        if injury_a < injury_b:
            analysis.append(f"✓ {team_a_name} has **fewer injury concerns** - lower injury risk ({injury_a:.1f}%) means more players available and in better condition")
        else:
            analysis.append(f"✓ {team_b_name} has **fewer injury concerns** - lower injury risk ({injury_b:.1f}%) means more players available and in better condition")
        
        # Attacking power
        if goals_a > goals_b:
            analysis.append(f"✓ {team_a_name} has **stronger attacking power** - team has scored more goals ({int(goals_a)} vs {int(goals_b)}) showing better offensive capability")
        else:
            analysis.append(f"✓ {team_b_name} has **stronger attacking power** - team has scored more goals ({int(goals_b)} vs {int(goals_a)}) showing better offensive capability")
        
        # Team creativity
        if assists_a > assists_b:
            analysis.append(f"✓ {team_a_name} has **better team play** - more assists ({int(assists_a)} vs {int(assists_b)}) indicates good coordination and creativity")
        else:
            analysis.append(f"✓ {team_b_name} has **better team play** - more assists ({int(assists_b)} vs {int(assists_a)}) indicates good coordination and creativity")
        
        # Winner prediction explanation
        if team_a_prob > team_b_prob:
            prob_margin = team_a_prob - team_b_prob
            analysis.append(f"\n🏆 **Why {team_a_name} is favored:** Based on the statistics above, our AI model predicts {team_a_name} has a {prob_margin:.0f}% higher chance of winning this match. The combination of better player form, fewer injuries, and stronger attacking metrics gives {team_a_name} the advantage.")
        else:
            prob_margin = team_b_prob - team_a_prob
            analysis.append(f"\n🏆 **Why {team_b_name} is favored:** Based on the statistics above, our AI model predicts {team_b_name} has a {prob_margin:.0f}% higher chance of winning this match. The combination of better player form, fewer injuries, and stronger attacking metrics gives {team_b_name} the advantage.")
        
        return analysis
    
    analysis_points = generate_match_analysis(
        st.session_state.team_a, st.session_state.team_b,
        team_a_stats, team_b_stats,
        team_a_prob, team_b_prob
    )
    
    st.markdown("""
        <div class="main-card">
            <h3>📋 Detailed Match Analysis</h3>
            <p style="color: rgba(255, 255, 255, 0.7); margin-bottom: 1.5rem;">
                Here's what our AI model found when analyzing these two teams:
            </p>
        </div>
    """, unsafe_allow_html=True)
    
    for point in analysis_points:
        if point.startswith("\n🏆"):
            # Winner explanation
            st.markdown(f"""
                <div class="info-box" style="margin-top: 1.5rem;">
                    <p>{point}</p>
                </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown(f"""
                <div style="background: rgba(52, 152, 219, 0.08); border-left: 4px solid #3498db; padding: 1rem; margin-bottom: 0.8rem; border-radius: 4px;">
                    <p style="color: rgba(255, 255, 255, 0.9); margin: 0; font-size: 0.95rem;">{point}</p>
                </div>
            """, unsafe_allow_html=True)
    
    # SHAP XAI Explanation Chart
    explanation = result.get("explanation", {})
    shap_top_features = explanation.get("top_features", {})

    if shap_top_features:
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("""
            <div class="main-card">
                <h3>🔍 XAI Explanation (SHAP)</h3>
                <p style="color: rgba(255, 255, 255, 0.7);">
                    Which factors most influenced the AI's prediction
                </p>
            </div>
        """, unsafe_allow_html=True)

        shap_col1, shap_col2 = st.columns([3, 2])

        with shap_col1:
            # Create SHAP bar chart with team-aware labels
            df_shap = pd.DataFrame([
                {
                    "Feature": translate_feature_name(k).replace("Team A", st.session_state.team_a).replace("Team B", st.session_state.team_b),
                    "Importance": v
                }
                for k, v in shap_top_features.items()
            ])
            df_shap["Abs Value"] = df_shap["Importance"].abs()
            df_shap = df_shap.sort_values("Abs Value", ascending=True)

            fig_shap = go.Figure()
            colors_shap = ['#22c55e' if x > 0 else '#ef4444' for x in df_shap["Importance"]]

            fig_shap.add_trace(go.Bar(
                y=df_shap["Feature"],
                x=df_shap["Importance"],
                orientation='h',
                marker_color=colors_shap,
                text=[f"{x:.1%}" for x in df_shap["Importance"]],
                textposition='outside',
                textfont=dict(color='white', size=12)
            ))
            fig_shap.update_layout(
                title="Feature Influence on Prediction",
                xaxis_title="Importance (%)",
                yaxis_title="",
                height=max(250, len(df_shap) * 55),
                showlegend=False,
                plot_bgcolor='rgba(0,0,0,0)',
                paper_bgcolor='rgba(0,0,0,0)',
                font=dict(color='white'),
                margin=dict(t=40, b=40, l=10, r=40),
                xaxis=dict(gridcolor='rgba(255, 255, 255, 0.08)', zeroline=True, zerolinecolor='rgba(255,255,255,0.15)'),
                yaxis=dict(gridcolor='rgba(255, 255, 255, 0.05)')
            )
            st.plotly_chart(fig_shap, use_container_width=True, key='match_shap')

        with shap_col2:
            # Explanation narrative
            explanation_text = format_explanation_text(explanation, "match")
            st.markdown(f"""
                <div style="padding: 1rem 0.5rem;">
                    <h4 style="color: white !important; margin-bottom: 1rem; font-size: 1rem;">📖 What This Means</h4>
                    <p style="color: rgba(255,255,255,0.8); line-height: 1.7; font-size: 0.92rem;">{explanation_text}</p>
                </div>
            """, unsafe_allow_html=True)

            st.markdown(f"""
                <div style="margin-top: 1rem; padding: 1rem; background: rgba(34,197,94,0.08); border-left: 4px solid #22c55e; border-radius: 4px;">
                    <p style="color: rgba(255,255,255,0.7); margin: 0; font-size: 0.85rem;">
                        <span style="color: #22c55e;">Green bars</span> = pushes prediction toward {st.session_state.team_a}<br>
                        <span style="color: #ef4444;">Red bars</span> = pushes prediction toward {st.session_state.team_b}
                    </p>
                </div>
            """, unsafe_allow_html=True)

    # Key Match Insights
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
        <div class="main-card">
            <h3>💡 Key Insights</h3>
        </div>
    """, unsafe_allow_html=True)
    
    insights = []
    
    # Generate dynamic insights based on stats
    perf_diff = abs(team_a_stats.get('avg_performance', 0) - team_b_stats.get('avg_performance', 0))
    if perf_diff > 0.3:
        stronger_team = st.session_state.team_a if team_a_stats.get('avg_performance', 0) > team_b_stats.get('avg_performance', 0) else st.session_state.team_b
        insights.append(f"**Big Performance Gap** - {stronger_team} has significantly better player form")
    
    injury_diff = abs(team_a_stats.get('avg_injury_risk', 0) - team_b_stats.get('avg_injury_risk', 0))
    if injury_diff > 10:
        safer_team = st.session_state.team_a if team_a_stats.get('avg_injury_risk', 0) < team_b_stats.get('avg_injury_risk', 0) else st.session_state.team_b
        insights.append(f"**Health Advantage** - {safer_team} has significantly lower injury risk")
    
    goals_diff = abs(team_a_stats.get('total_goals', 0) - team_b_stats.get('total_goals', 0))
    if goals_diff > 5:
        attacking_team = st.session_state.team_a if team_a_stats.get('total_goals', 0) > team_b_stats.get('total_goals', 0) else st.session_state.team_b
        insights.append(f"**Attacking Edge** - {attacking_team} has scored significantly more goals")
    
    assists_diff = abs(team_a_stats.get('total_assists', 0) - team_b_stats.get('total_assists', 0))
    if assists_diff > 5:
        teamplay_team = st.session_state.team_a if team_a_stats.get('total_assists', 0) > team_b_stats.get('total_assists', 0) else st.session_state.team_b
        insights.append(f"**Team Play Quality** - {teamplay_team} has more assists showing better coordination")
    
    if team_a_prob > 55 or team_b_prob > 55:
        favorite = st.session_state.team_a if team_a_prob > team_b_prob else st.session_state.team_b
        confidence = max(team_a_prob, team_b_prob)
        insights.append(f"**Clear Favorite** - Our model is {confidence:.0f}% confident in {favorite}'s victory")
    else:
        insights.append(f"**Competitive Match** - Both teams are evenly matched with winning chances close")
    
    col1, col2 = st.columns(2, gap="medium")
    
    for idx, insight in enumerate(insights):
        if idx < 2:
            with col1:
                st.markdown(f"""
                    <div class="info-box">
                        <p>{insight}</p>
                    </div>
                """, unsafe_allow_html=True)
        else:
            with col2:
                st.markdown(f"""
                    <div class="info-box">
                        <p>{insight}</p>
                    </div>
                """, unsafe_allow_html=True)
    
    # Back to Home
    st.markdown("<br>", unsafe_allow_html=True)
    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        if st.button("🏠 Back to Home", use_container_width=True, key="back_to_home_btn", type="primary"):
            st.switch_page("app.py")
