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
    parser.add_argument("--batch-size", type=int, default=32, help="Batch size")
    parser.add_argument("--data-dir", type=str, default="data/processed", help="Data directory")
    parser.add_argument("--output-dir", type=str, default="outputs", help="Output directory")
    parser.add_argument("--skip-training", action="store_true", help="Skip training (load existing model)")
    
    args = parser.parse_args()
    
    logger.info(f"🚀 Training {args.model} model...")
    
    # Load data
    data_dir = Path(args.data_dir)
    train_df = pd.read_parquet(data_dir / "train.parquet")
    val_df = pd.read_parquet(data_dir / "validation.parquet")
    test_df = pd.read_parquet(data_dir / "test.parquet")
    
    # Extract features and targets
    feature_cols = [col for col in train_df.columns if col != "pm25" and col != "date"]
    target_col = "pm25"
    
    X_train = train_df[feature_cols].values
    y_train = train_df[target_col].values
    X_val = val_df[feature_cols].values
    y_val = val_df[target_col].values
    X_test = test_df[feature_cols].values
    y_test = test_df[target_col].values
    
    logger.info(f"Training: {len(X_train)} samples")
    logger.info(f"Validation: {len(X_val)} samples")
    logger.info(f"Test: {len(X_test)} samples")
    logger.info(f"Features: {len(feature_cols)}")
    
    # Build model
    models = {
        "lstm": LSTMModel,
        "cnn_lstm": CNNLSTMModel,
        "convlstm": ConvLSTMModel,
        "transformer": TransformerModel,
    }
    
    model = models[args.model]()
    input_shape = (X_train.shape[1],)
    model.build(input_shape)
    model.compile()
    
    if args.skip_training:
        model.load(f"outputs/models/{args.model}/best_model.keras")
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