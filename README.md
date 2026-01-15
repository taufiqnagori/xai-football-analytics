# ⚽ XAI Football Analytics Suite

XAI Powered Sports Analytics suite for Player performance, Injury Risk and Match outcome.

## 🎯 Overview

The **XAI Football Analytics Suite** is a comprehensive machine learning platform designed to analyze football player data and make intelligent predictions using advanced ML models with transparent, explainable AI explanations via SHAP and LIME.

## ✨ Key Features

### 🤖 Machine Learning Models
- Advanced Random Forest models trained on comprehensive football datasets
- High-accuracy predictions based on historical player data

### 📊 SHAP Explanations
- Understand model predictions with SHAP (SHapley Additive exPlanations) values
- Visual feature importance plots showing which factors influence predictions

### 🎯 Accurate Predictions
- Get reliable performance scores, injury risks, and match outcome probabilities
- Data-driven insights for informed decision-making

### 💡 Transparent AI
- Every prediction comes with detailed explanations of contributing factors
- Interactive visualizations for easy interpretation

---

## 🚀 Features & Outputs

### 1. **Player Performance Analysis**
**Predict player performance scores using advanced ML models with XAI explanations**

#### Inputs:
- Player selection from available dataset
- Model parameters configuration

#### Outputs:
- **Performance Score**: Predicted player performance rating (0-100)
- **SHAP Explanation Plots**:
  - Feature importance bar chart
  - SHAP force plot showing contributing factors
  - Decision plot visualization
- **Top Contributing Factors**: List of key features affecting the prediction
- **Model Confidence**: Reliability metric for the prediction

---

### 2. **Injury Risk Analysis**
**Assess injury risk probability for players with detailed risk factors analysis**

#### Inputs:
- Player selection
- Historical health data
- Performance metrics

#### Outputs:
- **Injury Risk Probability**: Risk percentage (0-100%)
- **Risk Category**: Low / Medium / High
- **SHAP Explanation Plots**:
  - Top risk factors visualization
  - Feature contribution summary
  - Comparative risk analysis
- **Key Risk Factors**: Detailed breakdown of injury risk contributors
- **Recommendations**: Preventive measures based on analysis

---

### 3. **Match Outcome Prediction**
**Predict match outcomes between teams with AI-powered analytics and explanations**

#### Inputs:
- Team A selection and squad management
- Team B selection and squad management
- Match context (home/away, recent form, etc.)

#### Outputs:
- **Win Probabilities**:
  - Team A win probability
  - Team B win probability
  - Draw probability
- **Prediction Confidence**: Model certainty metric
- **SHAP Analysis**:
  - Team-level feature importance
  - Player contribution to match outcome
  - Key performance factors
- **Statistical Insights**:
  - Historical head-to-head records
  - Current form analysis
  - Squad strength comparison

---

## 📦 Tech Stack

- **Frontend**: Streamlit (Interactive UI)
- **Backend**: FastAPI (REST API)
- **ML Framework**: Python with scikit-learn
- **Data Processing**: Pandas, NumPy
- **Visualization**: Plotly, Matplotlib
- **XAI**: SHAP, LIME
- **Database**: CSV-based datasets

---

## 🏗️ Project Structure

```
Football-XAI-suite/
├── frontend/                    # Streamlit frontend application
│   ├── app.py                  # Home page
│   ├── style.css               # Global styling
│   ├── pages/
│   │   ├── 1_Performance_Analysis.py
│   │   ├── 2_Injury_Risk_Analysis.py
│   │   └── 3_Match_Outcome_Prediction.py
│   └── utils/
│       ├── api_client.py       # API communication
│       ├── theme.py            # Theme management
│       └── __init__.py
├── backend/                     # FastAPI backend
│   ├── main.py                 # API endpoints
│   ├── train_models.py         # Model training
│   ├── data_access.py          # Data handling
│   ├── config.py               # Configuration
│   ├── routers/                # API route handlers
│   ├── schemas/                # Data validation schemas
│   ├── utils/                  # Utility functions
│   └── data/                   # Datasets
├── models/                      # Trained ML models
├── notebooks/                   # Jupyter notebooks for analysis
└── requirements.txt            # Python dependencies
```

---

## 🛠️ Installation & Setup

### Prerequisites
- Python 3.8+
- pip package manager
- Virtual environment (recommended)

### Step 1: Clone Repository
```bash
git clone https://github.com/taufiqnagori/xai-football-analytics.git
cd Football-XAI-suite
```

### Step 2: Create Virtual Environment
```bash
python -m venv venv
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Start Backend Server
```bash
cd backend
uvicorn main:app --reload --port 8000
```

### Step 5: Start Frontend Application
```bash
cd frontend
streamlit run app.py
```

The application will open in your default browser at `http://localhost:8501`

---

## 📊 Sample Outputs

### Player Performance Analysis Output
```
Performance Score: 78.5/100
Top Contributing Factors:
  1. Recent Form (SHAP value: 0.15)
  2. Age (SHAP value: 0.12)
  3. Goals Scored (SHAP value: 0.10)
  4. Match Appearances (SHAP value: 0.09)
  5. Assists (SHAP value: 0.08)
```

### Injury Risk Analysis Output
```
Injury Risk: 28%
Risk Category: MEDIUM
Top Risk Factors:
  1. Injury History (SHAP value: 0.18)
  2. Match Frequency (SHAP value: 0.14)
  3. Age (SHAP value: 0.11)
  4. Previous Injuries (SHAP value: 0.09)
```

### Match Outcome Prediction Output
```
Team A Win Probability: 62%
Team B Win Probability: 28%
Draw Probability: 10%

Key Factors for Team A:
  - Strong Recent Form
  - Higher Average Player Rating
  - Home Advantage
```

---

## 🎨 UI Features

- **Dark/Light Theme Toggle**: Switch between dark and light modes
- **Responsive Sidebar Navigation**: Easy access to all prediction models
- **Interactive Visualizations**: Plotly-based interactive charts
- **Real-time Updates**: Instant predictions and explanations
- **Professional Design**: Clean, modern interface

---

## 📈 Performance Metrics

- **Model Accuracy**: 85%+ on test dataset
- **Prediction Speed**: <2 seconds per prediction
- **Data Coverage**: 500+ players, 1000+ historical matches
- **Feature Importance**: 15+ key features per model

---

## 📝 License

This project is licensed under the **MIT License** - see [LICENSE](LICENSE) file for details

### Full License Text:
```
MIT License

Copyright (c) 2026 Taufiq Nagori

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software...
```

For complete license text, see the [LICENSE](LICENSE) file in the repository.

---

## 👨‍💻 Author

**Taufiq Nagori**
- GitHub: [@taufiqnagori](https://github.com/taufiqnagori)
- Email: taufiqnagori99@gmail.com

---

## 🙏 Acknowledgments

- Built with Streamlit & FastAPI
- Machine Learning powered by scikit-learn
- XAI explanations using SHAP and LIME
- Football data from comprehensive datasets

---

## 📞 Support

For issues, questions, or suggestions, please:
- Open an issue on GitHub
- Contact the development team
- Check existing documentation

---

## 📚 Resources

- [SHAP Documentation](https://shap.readthedocs.io/)
- [LIME Documentation](https://lime-ml.readthedocs.io/)
- [Streamlit Docs](https://docs.streamlit.io/)
- [FastAPI Docs](https://fastapi.tiangolo.com/)

---

## Version History

### v1.0.0 (Current)
- ✅ Player Performance Analysis
- ✅ Injury Risk Assessment
- ✅ Match Outcome Prediction
- ✅ SHAP/LIME Explanations
- ✅ Dark/Light Theme
- ✅ Sidebar Navigation
- ✅ Responsive UI Design
