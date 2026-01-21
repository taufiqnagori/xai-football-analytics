"""Utility functions to make explanations more user-friendly"""

# Feature description mappings
FEATURE_DESCRIPTIONS = {
    # Performance features
    "full_season": "Player participation in full season",
    "is_starter": "Player is a starting XI regular",
    "matches_played": "Number of matches played",
    "minutes_played": "Total minutes on the field",
    "shot_accuracy": "Shooting accuracy percentage",
    "goals_per_match": "Average goals per match",
    "assists_per_match": "Average assists per match",
    "passes_per_match": "Average passes per match",
    "actions_per_90": "Average actions per 90 minutes",
    "pass_success_rate": "Passing success percentage",
    "total_actions": "Total on-field actions",
    
    # Injury features
    "injury_frequency": "How often player gets injured",
    "is_injury_prone": "Player has injury susceptibility",
    "is_young": "Player is under 25 years old",
    "is_veteran": "Player is over 32 years old",
    "high_workload": "Player has high playing workload",
    "age": "Player's age",
    "injuries_last_season": "Injuries sustained last season",
    
    # Match features
    "team_a_performance": "Team A's average player performance",
    "team_a_injury_risk": "Team A's average injury risk",
    "team_a_goals": "Team A's total goals in dataset",
    "team_a_starters": "Team A's number of starting XI players",
    "team_a_goals_per_match": "Team A's goals per match average",
    "team_b_performance": "Team B's average player performance",
    "team_b_injury_risk": "Team B's average injury risk",
    "team_b_goals": "Team B's total goals in dataset",
    "team_b_starters": "Team B's number of starting XI players",
    "team_b_goals_per_match": "Team B's goals per match average",
}

def get_feature_description(feature_name: str) -> str:
    """Get a user-friendly description of a feature"""
    return FEATURE_DESCRIPTIONS.get(feature_name, feature_name.replace("_", " ").title())

def format_explanation_text(explanation_dict: dict, model_type: str = "general") -> str:
    """
    Format explanation dictionary into user-friendly narrative text
    
    Args:
        explanation_dict: Dictionary containing explanation data
        model_type: Type of model - 'performance', 'injury', or 'match'
    
    Returns:
        Formatted explanation text
    """
    top_features = explanation_dict.get("top_features", {})
    
    if not top_features:
        return "No explanation data available"
    
    # Get top 3 features
    sorted_features = sorted(top_features.items(), key=lambda x: abs(x[1]), reverse=True)[:3]
    
    if model_type == "performance":
        text = "This player's performance score is mainly driven by:\n\n"
        for i, (feature, importance) in enumerate(sorted_features, 1):
            description = get_feature_description(feature)
            percentage = importance * 100
            text += f"{i}. **{description}** ({percentage:.1f}% influence)\n"
        text += "\nThese factors together determine the player's overall performance rating."
        
    elif model_type == "injury":
        text = "This player's injury risk is influenced by:\n\n"
        for i, (feature, importance) in enumerate(sorted_features, 1):
            description = get_feature_description(feature)
            percentage = importance * 100
            text += f"{i}. **{description}** ({percentage:.1f}% influence)\n"
        text += "\nConsider these factors when assessing injury prevention strategies."
        
    elif model_type == "match":
        text = "The match prediction is mainly determined by:\n\n"
        for i, (feature, importance) in enumerate(sorted_features, 1):
            description = get_feature_description(feature)
            percentage = importance * 100
            # Add context about which team
            if "team_a" in feature:
                text += f"{i}. **{description} (Team A)** ({percentage:.1f}% influence)\n"
            elif "team_b" in feature:
                text += f"{i}. **{description} (Team B)** ({percentage:.1f}% influence)\n"
            else:
                text += f"{i}. **{description}** ({percentage:.1f}% influence)\n"
        text += "\nThese team-level statistics are the strongest predictors of match outcome."
        
    else:
        text = "Key influencing factors:\n\n"
        for i, (feature, importance) in enumerate(sorted_features, 1):
            description = get_feature_description(feature)
            percentage = importance * 100
            text += f"{i}. **{description}** ({percentage:.1f}%)\n"
    
    return text

def translate_feature_name(feature_name: str) -> str:
    """Translate technical feature name to readable label"""
    translations = {
        "team_a_performance": "Team A Performance",
        "team_b_performance": "Team B Performance",
        "team_a_injury_risk": "Team A Injury Risk",
        "team_b_injury_risk": "Team B Injury Risk",
        "team_a_goals": "Team A Goals",
        "team_b_goals": "Team B Goals",
        "team_a_starters": "Team A Starters",
        "team_b_starters": "Team B Starters",
        "team_a_goals_per_match": "Team A Goals/Match",
        "team_b_goals_per_match": "Team B Goals/Match",
        "full_season": "Full Season Player",
        "is_starter": "Starting XI Regular",
        "is_injury_prone": "Injury Prone",
        "injury_frequency": "Injury Frequency",
        "is_young": "Young Player",
        "is_veteran": "Veteran Player",
        "high_workload": "High Workload",
    }
    return translations.get(feature_name, feature_name.replace("_", " ").title())

def create_insight_text(result: dict, model_type: str = "general") -> str:
    """
    Create insight text based on prediction result
    
    Args:
        result: Prediction result dictionary
        model_type: 'performance', 'injury', or 'match'
    
    Returns:
        Insight text
    """
    if model_type == "performance":
        score = result.get("predicted_performance", 0)
        if score >= 85:
            return "🌟 **Excellent Performance**: This player is performing exceptionally well and is a key asset to the team."
        elif score >= 70:
            return "✅ **Good Performance**: This player is contributing well to the team with solid overall statistics."
        else:
            return "📈 **Moderate Performance**: This player shows room for improvement in key performance areas."
            
    elif model_type == "injury":
        risk = result.get("injury_risk_percentage", 0)
        if risk >= 70:
            return "⚠️ **High Risk**: This player has a high likelihood of injury. Consider careful monitoring and recovery protocols."
        elif risk >= 40:
            return "🟡 **Moderate Risk**: This player has some injury risk factors. Monitor closely and ensure proper training load management."
        else:
            return "✅ **Low Risk**: This player has a low injury likelihood. Continue with current training and recovery practices."
            
    elif model_type == "match":
        team_a_prob = result.get("team_a_win_probability", 50)
        if team_a_prob > 60:
            return "🟢 **Team A Favored**: Team A has a significant advantage and is more likely to win based on squad composition."
        elif team_a_prob > 40:
            return "🟡 **Competitive Match**: Both teams are evenly matched. The match could go either way."
        else:
            return "🔵 **Team B Favored**: Team B has a significant advantage and is more likely to win based on squad composition."
    
    return ""
