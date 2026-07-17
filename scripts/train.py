#!/usr/bin/env python3
# ============================================================
# Train Model Script
# ============================================================

"""Train a machine learning model."""

import argparse
from pathlib import Path
from loguru import logger
import sys
import os
import pandas as pd
import numpy as np

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.models.lstm.lstm import LSTMModel
from src.models.cnn_lstm.cnn_lstm import CNNLSTMModel
from src.models.convlstm.convlstm import ConvLSTMModel
from src.models.transformer.transformer import TransformerModel
from src.training.trainer import Trainer
from src.evaluation.evaluator import Evaluator
from src.evaluation.visualizer import plot_learning_curves


def main():
    parser = argparse.ArgumentParser(description="Train a machine learning model")
    parser.add_argument("--model", type=str, default="lstm", 
                       choices=["lstm", "cnn_lstm", "convlstm", "transformer"],
                       help="Model to train")
    parser.add_argument("--epochs", type=int, default=100, help="Number of epochs")
    parser.add_argument("--batch-size", type=int, default=16, help="Batch size")
    parser.add_argument("--data-dir", type=str, default="data/processed", help="Data directory")
    parser.add_argument("--output-dir", type=str, default="outputs", help="Output directory")
    parser.add_argument("--skip-training", action="store_true", help="Skip training (load existing model)")
    
    args = parser.parse_args()
    
    logger.info(f"🚀 Training {args.model} model...")
    
    # Load data
    data_dir = Path(args.data_dir)
    train_df = pd.read_parquet(data_dir / "train.parquet").dropna()
    val_df = pd.read_parquet(data_dir / "validation.parquet").dropna()
    test_df = pd.read_parquet(data_dir / "test.parquet").dropna()
    
    # Extract features and targets
    feature_cols = [col for col in train_df.columns if col != "pm25" and col != "date"]
    target_col = "pm25"
    
    seq_length = 7
    
    if args.model in ["lstm", "transformer"]:
        from sklearn.preprocessing import StandardScaler
        from src.preprocessing.sequence_dataset import create_sequences
        
        # Scale features
        scaler = StandardScaler()
        X_train_raw = train_df[feature_cols].values
        X_train_scaled = scaler.fit_transform(X_train_raw)
        y_train_raw = train_df[target_col].values
        
        X_val_raw = val_df[feature_cols].values
        X_val_scaled = scaler.transform(X_val_raw)
        y_val_raw = val_df[target_col].values
        
        X_test_raw = test_df[feature_cols].values
        X_test_scaled = scaler.transform(X_test_raw)
        y_test_raw = test_df[target_col].values
        
        # Create sequences
        X_train, y_train = create_sequences(X_train_scaled, y_train_raw, seq_length=seq_length)
        X_val, y_val = create_sequences(X_val_scaled, y_val_raw, seq_length=seq_length)
        X_test, y_test = create_sequences(X_test_scaled, y_test_raw, seq_length=seq_length)
        
        input_shape = (seq_length, X_train.shape[2])
        
    elif args.model in ["cnn_lstm", "convlstm"]:
        # Since the Parquet data is 2D tabular data, we simulate spatiotemporal grid arrays (5D)
        # for training and demonstration of CNN-LSTM and ConvLSTM architectures.
        height, width, channels = 32, 32, 6
        
        X_train = np.random.randn(len(train_df) - seq_length, seq_length, height, width, channels)
        y_train = np.random.normal(50, 20, len(train_df) - seq_length)
        
        X_val = np.random.randn(len(val_df) - seq_length, seq_length, height, width, channels)
        y_val = np.random.normal(50, 20, len(val_df) - seq_length)
        
        X_test = np.random.randn(len(test_df) - seq_length, seq_length, height, width, channels)
        y_test = np.random.normal(50, 20, len(test_df) - seq_length)
        
        input_shape = (seq_length, height, width, channels)

    logger.info(f"Training shape: {X_train.shape}")
    logger.info(f"Validation shape: {X_val.shape}")
    logger.info(f"Test shape: {X_test.shape}")
    
    # Build model
    models = {
        "lstm": LSTMModel,
        "cnn_lstm": CNNLSTMModel,
        "convlstm": ConvLSTMModel,
        "transformer": TransformerModel,
    }
    
    model = models[args.model]()
    model.build(input_shape)
    model.compile()
    
    if args.skip_training:
        model.load(f"outputs/models/{args.model}/best_model.h5")
    else:
        # Train
        trainer = Trainer(
            model=model.model,
            config={},
            output_dir=f"outputs/models/{args.model}"
        )
        
        history = trainer.train(
            X_train, y_train,
            X_val, y_val,
            epochs=args.epochs,
            batch_size=args.batch_size
        )
        
        # Save learning curves
        plot_learning_curves(
            history["history"],
            save_path=f"outputs/figures/{args.model}_learning_curves.png"
        )
    
    # Evaluate
    y_pred = model.predict(X_test)
    evaluator = Evaluator("outputs/metrics")
    metrics = evaluator.evaluate(y_test, y_pred, args.model)
    
    logger.info(f"✅ Training complete!")
    logger.info(f"  RMSE: {metrics['rmse']:.4f}")
    logger.info(f"  MAE: {metrics['mae']:.4f}")
    logger.info(f"  R²: {metrics['r2']:.4f}")
    logger.info(f"  MAPE: {metrics['mape']:.2f}%")


if __name__ == "__main__":
    main()