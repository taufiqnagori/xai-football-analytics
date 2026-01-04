import numpy as np
import pandas as pd

# -----------------------------------------------------------
# 1. CONVERT SHAP VALUES TO READABLE FORMAT
# -----------------------------------------------------------
def shap_to_json(shap_values, feature_names, top_k=5):
    """
    Converts SHAP values into a JSON-friendly list of:
    [
        {"feature": "goals", "value": 0.23},
        {"feature": "pass_accuracy", "value": -0.12},
        ...
    ]

    Sorted by absolute contribution.
    """
    shap_values = shap_values[0]  # first sample shap row

    df = pd.DataFrame({
        "feature": feature_names,
        "shap_value": shap_values,
        "abs_value": np.abs(shap_values)
    })

    df = df.sort_values("abs_value", ascending=False).head(top_k)

    return df[["feature", "shap_value"]].to_dict(orient="records")


# -----------------------------------------------------------
# 2. GET SHAP SUMMARY (TOP FEATURES ONLY)
# -----------------------------------------------------------
def get_shap_top_features(explainer, model_input, feature_names, top_k=5):
    """
    Generates SHAP values and returns the top contributing features.
    """

    # Compute SHAP values
    shap_values = explainer(model_input)

    # Convert SHAP object → numpy array
    if hasattr(shap_values, "values"):
        shap_values = shap_values.values

    # Convert to JSON-friendly format
    return shap_to_json(shap_values, feature_names, top_k=top_k)


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
      "goals increased the prediction",
      "dribble_success_rate decreased the prediction"
    ]
    """

    explanations = []

    for item in shap_list:
        feature = item["feature"]
        value = item["shap_value"]

        if value > 0:
            explanations.append(f"{feature} increased the prediction")
        else:
            explanations.append(f"{feature} decreased the prediction")

    return explanations


# -----------------------------------------------------------
# 4. GET TOP-N FEATURE NAMES ONLY (for charts)
# -----------------------------------------------------------
def extract_feature_importance(shap_list):
    """
    Extracts clean dict:
    {
        "goals": 0.44,
        "minutes_played": -0.12,
        ...
    }
    """
    return {item["feature"]: item["shap_value"] for item in shap_list}
