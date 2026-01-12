# Football XAI Suite - Setup and Run Guide

## ✅ What Was Fixed

### Backend Fixes:
1. **train_models.py**: 
   - Added complete match model training
   - Added SHAP explainers for all three models
   - Fixed feature selection based on available dataset columns
   - Added proper error handling

2. **main.py**: 
   - Added CORS middleware for frontend communication
   - Added startup event to load models
   - Fixed router imports

3. **Routers** (performance, injury, match):
   - Fixed all imports and function signatures
   - Added proper SHAP explanation integration
   - Fixed data transformation for pipeline models
   - Added comprehensive error handling

4. **load_models.py**: 
   - Complete rewrite to load all models, explainers, and features
   - Added proper error handling for missing files

5. **data_access.py**: 
   - Fixed column name handling (uses 'team' not 'club_name')
   - Added helper functions for player/team queries

6. **shap_helpers.py**: 
   - Fixed SHAP value extraction for pipeline models
   - Added support for numpy arrays and DataFrames

### Frontend Fixes:
1. **API Client**: 
   - Fixed all endpoint URLs
   - Fixed request formats (JSON instead of params)
   - Added proper error handling

2. **Frontend Pages**: 
   - Complete rewrite with proper UI
   - Added SHAP visualizations using Plotly
   - Added proper error handling and user feedback
   - Match prediction page with 11-player selection

3. **Requirements**: 
   - Added plotly for visualizations

## 🚀 How to Run

### Step 1: Train Models
```bash
python backend/train_models.py
```

This will:
- Load the dataset from `data/football_master_dataset.csv`
- Train 3 models: performance, injury, match
- Create SHAP explainers for all models
- Save everything to `models/` directory

### Step 2: Start Backend API
```bash
uvicorn backend.main:app --reload
```

The API will be available at: `http://127.0.0.1:8000`

### Step 3: Start Frontend
```bash
streamlit run frontend/app.py
```

The frontend will be available at: `http://localhost:8501`

## 📋 API Endpoints

### Performance Prediction
- **GET** `/api/performance/players` - Get list of players
- **POST** `/api/performance/predict` - Predict performance
  ```json
  {
    "player_name": "Erling Haaland"
  }
  ```

### Injury Risk Prediction
- **GET** `/api/injury/players` - Get list of players
- **POST** `/api/injury/predict` - Predict injury risk
  ```json
  {
    "player_name": "Erling Haaland"
  }
  ```

### Match Outcome Prediction
- **GET** `/api/match/players` - Get list of players
- **POST** `/api/match/predict` - Predict match outcome
  ```json
  {
    "team_a": ["Player1", "Player2", ..., "Player11"],
    "team_b": ["Player1", "Player2", ..., "Player11"]
  }
  ```

## 🔍 XAI Features

All endpoints return SHAP explanations including:
- Top contributing features
- Feature importance values
- Key factors affecting prediction
- For match prediction: influential players

## ⚠️ Important Notes

1. **Dataset**: Uses `data/football_master_dataset.csv`
   - Column names: `team` (not `club_name`)
   - Available features may differ from ideal requirements
   - Models adapt to available columns

2. **Match Prediction**: 
   - Requires exactly 11 players per team
   - No duplicate players within teams
   - No players in both teams

3. **Model Training**: 
   - Run `train_models.py` before starting API
   - Models are saved to `models/` directory
   - SHAP explainers are created automatically

## 🐛 Troubleshooting

1. **Import Errors**: Make sure you're in the project root directory
2. **Model Not Found**: Run `train_models.py` first
3. **CORS Errors**: Backend CORS is configured for all origins
4. **SHAP Errors**: Models must be trained with SHAP explainers

## 📊 Dataset Requirements

The current dataset should have these columns:
- `player_name`
- `team`
- `performance_score`
- `injury_risk`
- `goals`, `assists`, `passes`, `shots`, `tackles`
- `minutes_played`, `matches_played`
- `age`, `injuries_last_season`

If your dataset has different columns, update `train_models.py` to use available columns.
