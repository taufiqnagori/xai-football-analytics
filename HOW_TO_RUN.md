# 🚀 How to Run Football XAI Suite

## Quick Start (Windows)

### Option 1: Using Batch Scripts (Easiest)

1. **Train Models First** (Required - Do this once or when you update data):
   ```
   Double-click: train_models.bat
   ```
   OR run in terminal:
   ```bash
   train_models.bat
   ```

2. **Start Backend API** (Terminal 1):
   ```
   Double-click: run_backend.bat
   ```
   OR run in terminal:
   ```bash
   run_backend.bat
   ```
   Backend will be available at: **http://127.0.0.1:8000**

3. **Start Frontend** (Terminal 2 - New Terminal):
   ```
   Double-click: run_frontend.bat
   ```
   OR run in terminal:
   ```bash
   run_frontend.bat
   ```
   Frontend will open automatically at: **http://localhost:8501**

---

### Option 2: Manual Commands

#### Step 1: Activate Virtual Environment
```bash
venv\Scripts\activate
```

#### Step 2: Train Models (First Time Only)
```bash
python backend/train_models.py
```

#### Step 3: Start Backend (Terminal 1)
```bash
uvicorn backend.main:app --reload
```
Backend runs on: **http://127.0.0.1:8000**

#### Step 4: Start Frontend (Terminal 2 - New Terminal)
```bash
streamlit run frontend/app.py
```
Frontend opens at: **http://localhost:8501**

---

## 📋 Step-by-Step Instructions

### Prerequisites Check
- ✅ Python 3.8+ installed
- ✅ Virtual environment exists (`venv` folder)
- ✅ Dataset file exists: `data/football_master_dataset.csv`

### First Time Setup

1. **Install Dependencies** (if not already installed):
   ```bash
   venv\Scripts\activate
   pip install -r requirements.txt
   ```

2. **Train Models**:
   ```bash
   python backend/train_models.py
   ```
   This creates:
   - `models/performance_model.pkl`
   - `models/injury_risk_model.pkl`
   - `models/match_outcome_model.pkl`
   - `models/shap_explainer_*.pkl` files

### Running the Application

**IMPORTANT**: You need **TWO terminals** running simultaneously:

#### Terminal 1 - Backend API:
```bash
# Activate venv
venv\Scripts\activate

# Start backend
uvicorn backend.main:app --reload
```

You should see:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete.
🔄 Loading dataset and models...
✅ Dataset loaded: 1259 rows
✅ Performance model loaded
...
```

#### Terminal 2 - Frontend (New Terminal):
```bash
# Activate venv
venv\Scripts\activate

# Start frontend
streamlit run frontend/app.py
```

You should see:
```
You can now view your Streamlit app in your browser.
Local URL: http://localhost:8501
```

---

## 🧪 Testing the API

### Test Backend Health:
Open browser: **http://127.0.0.1:8000/health**

### Test API Endpoints:
- **Performance**: http://127.0.0.1:8000/api/performance/players
- **Injury**: http://127.0.0.1:8000/api/injury/players
- **Match**: http://127.0.0.1:8000/api/match/players

### API Documentation:
- **Swagger UI**: http://127.0.0.1:8000/docs
- **ReDoc**: http://127.0.0.1:8000/redoc

---

## 🎯 Using the Frontend

1. **Performance Analysis**:
   - Select a player from dropdown
   - Click "Predict Performance"
   - View prediction + SHAP explanation

2. **Injury Risk Analysis**:
   - Select a player from dropdown
   - Click "Predict Injury Risk"
   - View risk percentage + SHAP explanation

3. **Match Outcome Prediction**:
   - Select 11 players for Team A
   - Select 11 players for Team B
   - Click "Predict Match Outcome"
   - View win probabilities + SHAP explanation

---

## ⚠️ Troubleshooting

### Error: "Model not found"
**Solution**: Run `python backend/train_models.py` first

### Error: "Module not found"
**Solution**: 
```bash
venv\Scripts\activate
pip install -r requirements.txt
```

### Error: "Port already in use"
**Solution**: 
- Backend: Change port: `uvicorn backend.main:app --reload --port 8001`
- Frontend: Streamlit will auto-use next available port

### Error: "CORS error" in frontend
**Solution**: Make sure backend is running on port 8000

### Frontend can't connect to backend
**Solution**: 
1. Check backend is running: http://127.0.0.1:8000/health
2. Check `frontend/utils/api_client.py` has correct BASE URL

---

## 📝 Quick Reference

| Component | Command | URL |
|-----------|---------|-----|
| Train Models | `python backend/train_models.py` | - |
| Backend API | `uvicorn backend.main:app --reload` | http://127.0.0.1:8000 |
| Frontend | `streamlit run frontend/app.py` | http://localhost:8501 |
| API Docs | - | http://127.0.0.1:8000/docs |

---

## 🔄 Typical Workflow

1. **First Time**:
   ```bash
   train_models.bat          # Train models
   run_backend.bat           # Start backend (Terminal 1)
   run_frontend.bat          # Start frontend (Terminal 2)
   ```

2. **Subsequent Runs**:
   ```bash
   run_backend.bat           # Start backend (Terminal 1)
   run_frontend.bat          # Start frontend (Terminal 2)
   ```

3. **After Dataset Changes**:
   ```bash
   train_models.bat          # Retrain models
   # Restart backend to load new models
   ```

---

## ✅ Success Indicators

**Backend Running Successfully**:
- ✅ Terminal shows "Application startup complete"
- ✅ http://127.0.0.1:8000/health returns `{"status": "healthy"}`
- ✅ Models loaded messages appear

**Frontend Running Successfully**:
- ✅ Browser opens automatically
- ✅ No connection errors in browser console
- ✅ Player dropdown populates with names

**Everything Working**:
- ✅ Can select players in frontend
- ✅ Predictions return results
- ✅ SHAP visualizations appear
- ✅ No errors in browser console

---

Need help? Check the logs in the terminal windows for detailed error messages!
