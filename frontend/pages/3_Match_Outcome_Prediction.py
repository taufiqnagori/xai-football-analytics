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
st.markdown("""
    <div style="text-align: center; padding: 2rem 0;">
        <h1>🏆 Match Outcome Prediction</h1>
        <p class="page-subtitle" style="font-size: 1.2rem;">
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
    **To start the backend:**
    1. Open a new terminal
    2. Activate virtual environment: `venv\\Scripts\\activate`
    3. Run: `uvicorn backend.main:app --reload`
    4. Backend should be available at: http://127.0.0.1:8000
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
            
            # Get available players for Team A (team players + all players)
            team_a_available = [p["player_name"] for p in st.session_state.team_a_players_list] if st.session_state.team_a_players_list else []
            available_for_a = sorted(list(set(team_a_available + all_players)))
            
            new_squad_a = []
            for i in range(11):
                current_player = st.session_state.team_a_squad[i] if i < len(st.session_state.team_a_squad) else None
                
                # Get player info if exists
                player_info = None
                if current_player and st.session_state.team_a_players_list:
                    player_info = next((p for p in st.session_state.team_a_players_list if p["player_name"] == current_player), None)
                
                # Player selection dropdown
                def format_player_name(x):
                    if not x:
                        return "Select Player"
                    player_info = next((p for p in st.session_state.team_a_players_list if p['player_name'] == x), None)
                    if player_info:
                        return f"{x} ({player_info['position']}) - {player_info['performance_score']:.1f}"
                    return x
                
                selected = st.selectbox(
                    f"Player {i+1}",
                    [None] + available_for_a,
                    key=f"team_a_player_{i}",
                    index=0 if not current_player else available_for_a.index(current_player) + 1 if current_player in available_for_a else 0,
                    format_func=format_player_name
                )
                
                if selected:
                    new_squad_a.append(selected)
                    # Display player info
                    if player_info:
                        st.caption(f"⚽ {player_info['position']} | 📊 {player_info['performance_score']:.1f} | ⚠️ Risk: {player_info['injury_risk']*100:.1f}%")
            
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
            
            # Get available players for Team B
            team_b_available = [p["player_name"] for p in st.session_state.team_b_players_list] if st.session_state.team_b_players_list else []
            available_for_b = sorted(list(set(team_b_available + all_players)))
            
            new_squad_b = []
            for i in range(11):
                current_player = st.session_state.team_b_squad[i] if i < len(st.session_state.team_b_squad) else None
                
                # Get player info if exists
                player_info = None
                if current_player and st.session_state.team_b_players_list:
                    player_info = next((p for p in st.session_state.team_b_players_list if p["player_name"] == current_player), None)
                
                # Player selection dropdown
                def format_player_name_b(x):
                    if not x:
                        return "Select Player"
                    player_info = next((p for p in st.session_state.team_b_players_list if p['player_name'] == x), None)
                    if player_info:
                        return f"{x} ({player_info['position']}) - {player_info['performance_score']:.1f}"
                    return x
                
                selected = st.selectbox(
                    f"Player {i+1}",
                    [None] + available_for_b,
                    key=f"team_b_player_{i}",
                    index=0 if not current_player else available_for_b.index(current_player) + 1 if current_player in available_for_b else 0,
                    format_func=format_player_name_b
                )
                
                if selected:
                    new_squad_b.append(selected)
                    # Display player info
                    if player_info:
                        st.caption(f"⚽ {player_info['position']} | 📊 {player_info['performance_score']:.1f} | ⚠️ Risk: {player_info['injury_risk']*100:.1f}%")
            
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
    
    # Check if result is valid
    if not result:
        st.markdown("""
            <div class="error-box">
                <h3>❌ Error</h3>
                <p>No result returned from prediction</p>
            </div>
        """, unsafe_allow_html=True)
    elif "error" in result:
        st.markdown(f"""
            <div class="error-box">
                <h3>❌ Error</h3>
                <p>{result['error']}</p>
            </div>
        """, unsafe_allow_html=True)
    else:
        # Prediction Results Section
        st.markdown("---")
        st.header("🎯 Prediction Results")
        
        team_a_prob = result.get("team_a_win_probability", 0)
        team_b_prob = result.get("team_b_win_probability", 0)
        predicted_winner = result.get("predicted_winner", "Unknown")
        
        # Winner announcement
        winner_team = st.session_state.team_a if predicted_winner == "Team A" else st.session_state.team_b
        st.markdown(f"""
        <div class="prediction-result">
            <h2>🏆 Predicted Winner: {winner_team}</h2>
            <p style="font-size: 1.2em; margin-top: 1rem;">
                {st.session_state.team_a}: <strong>{team_a_prob}%</strong> | 
                {st.session_state.team_b}: <strong>{team_b_prob}%</strong>
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        # Win Probability Visualization
        st.subheader("📊 Win Probability Comparison")
        
        fig = go.Figure()
        
        # Team A bar
        fig.add_trace(go.Bar(
            x=[st.session_state.team_a],
            y=[team_a_prob],
            name=st.session_state.team_a,
            marker_color='#3498db',
            text=[f"{team_a_prob}%"],
            textposition='outside',
            textfont=dict(size=16, color='white', family='Arial Black')
        ))
        
        # Team B bar
        fig.add_trace(go.Bar(
            x=[st.session_state.team_b],
            y=[team_b_prob],
            name=st.session_state.team_b,
            marker_color='#e74c3c',
            text=[f"{team_b_prob}%"],
            textposition='outside',
            textfont=dict(size=16, color='white', family='Arial Black')
        ))
        
        fig.update_layout(
            title=f"{st.session_state.team_a} vs {st.session_state.team_b} - Win Probability",
            yaxis_title="Win Probability (%)",
            yaxis_range=[0, 100],
            height=400,
            showlegend=False,
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)'
        )
        
        st.plotly_chart(fig, use_container_width=True)
        
        # Team Statistics
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("""
            <div class="main-card">
                <h2>📈 Team Statistics Comparison</h2>
            </div>
        """, unsafe_allow_html=True)
        
        team_a_stats = result.get("team_a_stats", {})
        team_b_stats = result.get("team_b_stats", {})
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown(f"""
                <div class="team-card">
                    <h3>🟦 {st.session_state.team_a}</h3>
                </div>
            """, unsafe_allow_html=True)
            col1a, col1b = st.columns(2)
            with col1a:
                st.metric("Avg Performance", f"{team_a_stats.get('avg_performance', 0):.2f}", delta=None)
                st.metric("Total Goals", team_a_stats.get('total_goals', 0), delta=None)
            with col1b:
                st.metric("Avg Injury Risk", f"{team_a_stats.get('avg_injury_risk', 0):.2f}", delta=None)
                st.metric("Total Assists", team_a_stats.get('total_assists', 0), delta=None)
        
        with col2:
            st.markdown(f"""
                <div class="team-card">
                    <h3>🟥 {st.session_state.team_b}</h3>
                </div>
            """, unsafe_allow_html=True)
            col2a, col2b = st.columns(2)
            with col2a:
                st.metric("Avg Performance", f"{team_b_stats.get('avg_performance', 0):.2f}", delta=None)
                st.metric("Total Goals", team_b_stats.get('total_goals', 0), delta=None)
            with col2b:
                st.metric("Avg Injury Risk", f"{team_b_stats.get('avg_injury_risk', 0):.2f}", delta=None)
                st.metric("Total Assists", team_b_stats.get('total_assists', 0), delta=None)
        
        # XAI Explanation
        explanation = result.get("explanation", {})
        
        if explanation:
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("""
                <div class="main-card">
                    <h2>🔍 What Determines This Prediction?</h2>
                    <p style="color: rgba(255, 255, 255, 0.7);">
                        Understanding which team strengths influence the match outcome
                    </p>
                </div>
            """, unsafe_allow_html=True)
            
            # Add insight box
            insight = create_insight_text(result, "match")
            st.markdown(f"""
                <div class="info-box">
                    <h4>💡 Summary</h4>
                    <p>{insight}</p>
                </div>
            """, unsafe_allow_html=True)
            
            top_features = explanation.get("top_features", {})
            key_factors = explanation.get("key_factors", [])
            influential_players = explanation.get("influential_players", [])
            
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
                
                colors = ['#2ecc71' if x > 0 else '#e74c3c' for x in df_shap["Importance"]]
                
                fig.add_trace(go.Bar(
                    y=df_shap["Feature"],
                    x=df_shap["Importance"],
                    orientation='h',
                    marker_color=colors,
                    text=[f"{x:.1%}" for x in df_shap["Importance"]],
                    textposition='outside'
                ))
                
                fig.update_layout(
                    title="Team Factors Most Important to Match Outcome",
                    xaxis_title="Importance (%)",
                    yaxis_title="",
                    height=500,
                    showlegend=False,
                    plot_bgcolor='rgba(0,0,0,0)',
                    paper_bgcolor='rgba(0,0,0,0)',
                    font=dict(color='white'),
                    xaxis=dict(gridcolor='rgba(255, 255, 255, 0.1)'),
                    yaxis=dict(gridcolor='rgba(255, 255, 255, 0.1)')
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
                # Add detailed explanation
                explanation_text = format_explanation_text(explanation, "match")
                st.markdown(f"""
                    <div class="main-card">
                        <h3>📖 Detailed Analysis</h3>
                        <p>{explanation_text}</p>
                    </div>
                """, unsafe_allow_html=True)
            
            if key_factors:
                st.markdown("""
                    <div class="main-card">
                        <h3>✨ Key Statistics Influencing Prediction</h3>
                    </div>
                """, unsafe_allow_html=True)
                for factor in key_factors:
                    # Parse and improve readability of factor text
                    st.markdown(f"""
                        <div class="player-card">
                            <p style="margin: 0; color: white;">• {factor}</p>
                        </div>
                    """, unsafe_allow_html=True)
            
            if influential_players:
                st.markdown("""
                    <div class="main-card">
                        <h3>⭐ Most Influential Players</h3>
                    </div>
                """, unsafe_allow_html=True)
                for player_info in influential_players:
                    team_name = st.session_state.team_a if player_info.get('team') == 'Team A' else st.session_state.team_b
                    st.markdown(f"""
                        <div class="player-card">
                            <p style="margin: 0; color: white;">
                                • <strong>{player_info.get('player', 'Unknown')}</strong> ({team_name}): {player_info.get('reason', 'N/A')}
                            </p>
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
