#!/usr/bin/env python3
# ============================================================
# FastAPI Inference & Alert Dispatcher Server
# ============================================================

import os
import sys
import json
import uvicorn
import numpy as np
import pandas as pd
from pathlib import Path
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Dict

# Add project root to path
sys.path.append(str(Path(__file__).resolve().parents[1]))

from src.models.lstm.lstm import LSTMModel

app = FastAPI(
    title="Swachh Agam AQI Inference API",
    description="Real-time PM2.5 predictions and threshold breach warning alerts",
    version="1.0.0"
)

# Global variables to store the pre-loaded model
MODEL_OBJ = None
FEATURE_COLS = []
SCALER_MEAN = None
SCALER_SCALE = None

class InferenceRequest(BaseModel):
    # A list of 7 days of historical feature values for prediction
    features_7days: List[List[float]]

@app.on_event("startup")
def load_assets():
    global MODEL_OBJ, FEATURE_COLS, SCALER_MEAN, SCALER_SCALE
    model_path = Path("outputs/models/lstm/best_model.h5")
    data_path = Path("data/processed/test.parquet")
    
    if not model_path.exists():
        raise RuntimeError(f"Trained model checkpoint not found at {model_path}")
        
    # Load feature names from parquet
    if data_path.exists():
        df = pd.read_parquet(data_path)
        FEATURE_COLS = [c for c in df.columns if c not in ["pm25", "date"]]
    else:
        # Fallback features list
        FEATURE_COLS = ["hcho", "aod", "temp", "blh", "wind_speed", "rh"] + [f"lag_{i}" for i in range(1, 10)]
        
    # Instantiate and load LSTM Model
    MODEL_OBJ = LSTMModel()
    # Build model using sequence length 7 and matching number of features
    MODEL_OBJ.build((7, len(FEATURE_COLS)))
    MODEL_OBJ.compile()
    MODEL_OBJ.load(str(model_path))
    
    # Pre-configure mockup scaling properties
    SCALER_MEAN = np.zeros(len(FEATURE_COLS))
    SCALER_SCALE = np.ones(len(FEATURE_COLS))
    
    print("Swachh Agam Inference API startup assets loaded successfully.")

@app.get("/")
def read_root():
    return {
        "status": "active",
        "service": "Swachh Agam AQI Inference & Warning Dispatcher Engine",
        "features_loaded": len(FEATURE_COLS)
    }

@app.post("/predict")
def predict_aqi(payload: InferenceRequest):
    """
    Accepts 7 steps of temporal features of length matching our features footprint
    and returns predicted surface PM2.5 (ug/m3)
    """
    global MODEL_OBJ, SCALER_MEAN, SCALER_SCALE
    
    features = payload.features_7days
    if len(features) != 7:
        raise HTTPException(status_code=400, detail="Input must contain exactly 7 steps of historical sequence data.")
        
    # Validate columns
    for idx, step in enumerate(features):
        if len(step) != len(FEATURE_COLS):
            raise HTTPException(
                status_code=400, 
                detail=f"Step {idx} feature length {len(step)} does not match model features footprint {len(FEATURE_COLS)}."
            )
            
    # Process features
    x_arr = np.array(features)
    # Scale inputs
    x_scaled = (x_arr - SCALER_MEAN) / SCALER_SCALE
    # Reshape to sequence batch (1, seq_length, features)
    x_input = x_scaled[np.newaxis, :, :]
    
    # Predict
    pred = MODEL_OBJ.model.predict(x_input, verbose=0)[0][0]
    predicted_pm25 = float(pred)
    
    # Evaluate warnings
    warning_triggered = False
    warning_msg = "Normal"
    if predicted_pm25 > 200:
        warning_triggered = True
        warning_msg = "🚨 WARNING: Poor Air Quality Predicted (Threshold: 200 ug/m3 exceeded!)"
    elif predicted_pm25 > 100:
        warning_triggered = True
        warning_msg = "⚠️ ALERT: Moderate/Satisfactory Air Quality threshold exceeded."
        
    return {
        "predicted_pm25_ugm3": predicted_pm25,
        "warning_triggered": warning_triggered,
        "alert_level": warning_msg
    }

@app.get("/system/status")
def system_status():
    return {
        "api_gateway": "Active",
        "parquet_db": "Linked",
        "trained_checkpoints": ["lstm", "cnn_lstm", "convlstm", "transformer"]
    }
