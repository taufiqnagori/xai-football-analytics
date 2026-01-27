import numpy as np
import pandas as pd

# -----------------------------------------------------------
# 1. CONVERT SHAP VALUES TO READABLE FORMAT
# -----------------------------------------------------------
def shap_to_json(shap_values, feature_names, top_k=5):
    """
    Converts SHAP values into a JSON-friendly list of:
    [
        {"feature": "goals", "shap_value": 0.23},
        {"feature": "pass_accuracy", "shap_value": -0.12},
        ...
    ]

    Sorted by absolute contribution.
    """
    # Handle different SHAP output formats
    if hasattr(shap_values, 'values'):
        shap_values = shap_values.values
    
    shap_array = np.array(shap_values, dtype=np.float64)
    
    # Handle multi-output models
    if len(shap_array.shape) > 2:
        shap_array = shap_array[0]  # Take first output
    
    # Get first sample
    if len(shap_array.shape) > 1:
        shap_array = shap_array[0]
    
    df = pd.DataFrame({
        "feature": feature_names[:len(shap_array)],
        "shap_value": shap_array,
        "abs_value": np.abs(shap_array)
    })

    df = df.sort_values("abs_value", ascending=False).head(top_k)

    # Convert to JSON-friendly format (convert numpy types to Python types)
    result = []
    for _, row in df.iterrows():
        result.append({
            "feature": str(row["feature"]),
            "shap_value": float(row["shap_value"])
        })
    
    return result


# -----------------------------------------------------------
# 2. GET SHAP SUMMARY (TOP FEATURES ONLY)
# -----------------------------------------------------------
def get_shap_top_features(explainer, model_input, feature_names, top_k=5):
    """
    Generates SHAP values and returns the top contributing features.
    model_input can be a numpy array (transformed) or pandas DataFrame
    """
    try:
        # Convert to numpy if needed
        if hasattr(model_input, 'values'):
            model_input = model_input.values
        model_input = np.array(model_input)
        
        # Ensure 2D array
        if len(model_input.shape) == 1:
            model_input = model_input.reshape(1, -1)
        
        # Compute SHAP values
        shap_values = explainer.shap_values(model_input)
        
        # Convert SHAP object → numpy array
        if hasattr(shap_values, "values"):
            shap_values = shap_values.values
        
        # Handle list of arrays (multi-class)
        if isinstance(shap_values, list):
            # For classification, use the first class or average
            if len(shap_values) > 0:
                shap_values = shap_values[0]
            else:
                shap_values = np.array(shap_values)
        
        # Convert to JSON-friendly format
        return shap_to_json(shap_values, feature_names, top_k=top_k)
    except Exception as e:
        print(f"Error computing SHAP values: {e}")
        import traceback
        traceback.print_exc()
        # Return empty list on error
        return []


# -----------------------------------------------------------
# 3. FORMAT KEY FACTORS (POSITIVE / NEGATIVE)
# -----------------------------------------------------------
def format_key_factors(shap_list):
    """
    Converts SHAP output into easy English explanations.
    
    Example:
    Input:
    [
      {"feature": "goals", "shap_value": 0.45},
      {"feature": "dribble_success_rate", "shap_value": -0.20}
    ]

    Output:
    [
      "goals increased the prediction by 0.45",
      "dribble_success_rate decreased the prediction by 0.20"
    ]
    """

    explanations = []

    for item in shap_list:
        feature = item.get("feature", "unknown")
        value = item.get("shap_value", 0)
        
        # Clean feature name for display
        feature_display = feature.replace("_", " ").title()

        if value > 0:
            explanations.append(f"{feature_display} increased the prediction by {value:.3f}")
        else:
            explanations.append(f"{feature_display} decreased the prediction by {value:.3f}")

    return explanations


# -----------------------------------------------------------
# 4. GET TOP-N FEATURE NAMES ONLY (for charts)
# -----------------------------------------------------------
def extract_feature_importance(shap_list):
    """
    Extracts clean dict with normalized importance percentages that sum to 100%:
    {
        "goals": 0.44,
        "minutes_played": -0.12,
        ...
    }
    
    Note: Values are absolute contributions normalized to sum to 1.0
    (when displayed as percentages they'll sum to 100%)
    """
    if not shap_list:
        return {}
    
    # Get absolute values (convert to float to ensure JSON serializable)
    importance_dict = {}
    for item in shap_list:
        feature = item.get("feature", "unknown")
        value = float(item.get("shap_value", 0))
        importance_dict[feature] = value
    
    # If all values are zero or negative, return as-is
    if not importance_dict:
        return {}
    
    # Calculate total absolute contribution
    total_abs = sum(abs(v) for v in importance_dict.values())
    
    # Normalize to sum to 1.0 (will be 100% when formatted as percentage)
    if total_abs > 0:
        normalized = {k: float(v / total_abs) for k, v in importance_dict.items()}
    else:
        normalized = {k: float(v) for k, v in importance_dict.items()}
    
    return normalized
