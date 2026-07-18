# ============================================================
# Inference Pipeline
# ============================================================

"""Inference pipeline for making predictions."""

import numpy as np
import pandas as pd
from pathlib import Path
from loguru import logger
from typing import Dict, Any, Optional

from src.models.lstm.lstm import LSTMModel
from src.models.cnn_lstm.cnn_lstm import CNNLSTMModel
from src.models.convlstm.convlstm import ConvLSTMModel
from src.models.transformer.transformer import TransformerModel
from src.models.ensemble.ensemble import EnsembleModel


class InferencePipeline:
    """
    Inference pipeline for making predictions on new data.
    """

    def __init__(self, model_dir: str = "outputs/models/"):
        """
        Initialize inference pipeline.

        Args:
            model_dir (str): Directory containing trained models
        """
        self.model_dir = Path(model_dir)
        self.model = None
        self.scaler = None

    def load_model(self, model_name: str, model_path: Optional[str] = None) -> None:
        """
        Load a trained model.

        Args:
            model_name (str): Name of the model
            model_path (str): Path to model weights
        """
        models = {
            "lstm": LSTMModel,
            "cnn_lstm": CNNLSTMModel,
            "convlstm": ConvLSTMModel,
            "transformer": TransformerModel,
        }

        if model_name not in models:
            raise ValueError(f"Unknown model: {model_name}")

        if model_path is None:
            model_path = self.model_dir / model_name / "best_model.h5"

        self.model = models[model_name]()
        self.model.load(str(model_path))
        logger.info(f"✅ Model loaded from {model_path}")

    def predict(self, X: np.ndarray) -> np.ndarray:
        """
        Make predictions.

        Args:
            X (np.ndarray): Features

        Returns:
            np.ndarray: Predictions
        """
        if self.model is None:
            raise ValueError("No model loaded. Call load_model() first.")

        return self.model.predict(X)

    def predict_from_df(
        self,
        df: pd.DataFrame,
        feature_cols: list,
        scaler=None,
    ) -> np.ndarray:
        """
        Make predictions from DataFrame.

        Args:
            df (pd.DataFrame): Input DataFrame
            feature_cols (list): Feature column names
            scaler: Scaler used during training

        Returns:
            np.ndarray: Predictions
        """
        X = df[feature_cols].values

        if scaler is not None:
            X = scaler.transform(X)

        return self.predict(X)
