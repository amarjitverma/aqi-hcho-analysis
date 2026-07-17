#!/usr/bin/env python3
# ============================================================
# Predict Script
# ============================================================

"""Make predictions using a trained model."""

import argparse
from pathlib import Path
from loguru import logger
import sys
import os
import pandas as pd
import numpy as np

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.inference.predictor import Predictor
from src.inference.postprocessing import postprocess_predictions


def main():
    parser = argparse.ArgumentParser(description="Make predictions using a trained model")
    parser.add_argument("--model", type=str, default="lstm", help="Model to use")
    parser.add_argument("--input", type=str, default="data/processed/test.parquet", help="Input data")
    parser.add_argument("--output", type=str, default="outputs/predictions/predictions.csv", help="Output file")
    parser.add_argument("--convert-to-aqi", action="store_true", help="Convert PM2.5 to AQI")
    
    args = parser.parse_args()
    
    logger.info(f"🔮 Making predictions using {args.model}...")
    
    # Load data
    df = pd.read_parquet(args.input).dropna()
    
    # Define feature columns
    feature_cols = [col for col in df.columns if col != "pm25" and col != "date"]
    
    # Load model
    predictor = Predictor(model_dir="outputs/models/")
    predictor.load_model(
        model_name=args.model,
        feature_cols=feature_cols
    )
    
    seq_length = 7
    df_seq = df.iloc[seq_length:]
    
    if args.model in ["lstm", "transformer"]:
        from sklearn.preprocessing import StandardScaler
        from src.preprocessing.sequence_dataset import create_sequences
        
        # Scale features
        scaler = StandardScaler()
        X_raw = df[feature_cols].values
        X_scaled = scaler.fit_transform(X_raw)
        y_raw = df["pm25"].values if "pm25" in df.columns else np.zeros(len(df))
        
        X_seq, _ = create_sequences(X_scaled, y_raw, seq_length=seq_length)
        predictions = predictor.predict(X_seq)
        
    elif args.model in ["cnn_lstm", "convlstm"]:
        # Simulate 5D grid for prediction demonstration
        height, width, channels = 32, 32, 6
        X_seq = np.random.randn(len(df) - seq_length, seq_length, height, width, channels)
        predictions = predictor.predict(X_seq)
        
    else:
        # Standard 2D model (e.g. ensemble fallback if any)
        X = df[feature_cols].values
        predictions = predictor.predict(X)
        df_seq = df
        
    # Post-process
    predictions = postprocess_predictions(
        predictions,
        clip_min=0,
        convert_to_aqi=args.convert_to_aqi
    )
    
    # Save results
    df_results = pd.DataFrame({
        "predicted": predictions,
        "actual": df_seq["pm25"].values if "pm25" in df_seq.columns else np.nan,
    })
    if "date" in df_seq.columns:
        df_results["date"] = df_seq["date"].values
    
    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    df_results.to_csv(args.output, index=False)
    
    logger.info(f"✅ Predictions saved to {args.output}")
    logger.info(f"  Mean prediction: {predictions.mean():.2f}")
    logger.info(f"  Std prediction: {predictions.std():.2f}")


if __name__ == "__main__":
    main()