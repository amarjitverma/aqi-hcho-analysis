# ============================================================
# Predictor
# ============================================================

"""Model prediction and inference."""

import numpy as np
import pandas as pd
from pathlib import Path
from loguru import logger
from typing import Optional, Dict, Any, Union

from src.models.lstm.lstm import LSTMModel
from src.models.cnn_lstm.cnn_lstm import CNNLSTMModel
from src.models.convlstm.convlstm import ConvLSTMModel
from src.models.transformer.transformer import TransformerModel
from src.models.ensemble.ensemble import EnsembleModel


class Predictor:
    """
    Predictor class for model inference.

    Handles loading models and making predictions on new data.
    """

    def __init__(self, model_dir: str = "models/checkpoints/"):
        """
        Initialize predictor.

        Args:
            model_dir (str): Directory containing model checkpoints
        """
        self.model_dir = Path(model_dir)
        self.model = None
        self.model_name = None
        self.scaler = None
        self.feature_cols = None

    def load_model(
        self,
        model_name: str,
        model_path: Optional[str] = None,
        scaler=None,
        feature_cols: Optional[list] = None,
    ) -> None:
        """
        Load a trained model.

        Args:
            model_name (str): Name of the model ('lstm', 'cnn_lstm', 'convlstm', 'transformer', 'ensemble')
            model_path (str): Path to model weights
            scaler: Scaler used during training
            feature_cols (list): Feature column names
        """
        models = {
            "lstm": LSTMModel,
            "cnn_lstm": CNNLSTMModel,
            "convlstm": ConvLSTMModel,
            "transformer": TransformerModel,
            "ensemble": EnsembleModel,
        }

        if model_name not in models:
            raise ValueError(f"Unknown model: {model_name}. Available: {list(models.keys())}")

        self.model_name = model_name
        self.scaler = scaler
        self.feature_cols = feature_cols

        if model_name == "ensemble":
            # Load all models for ensemble
            self.model = self._load_ensemble()
        else:
            # Load single model
            if model_path is None:
                model_path = self.model_dir / model_name / "best_model.h5"

            self.model = models[model_name]()
            self.model.load(str(model_path))
            logger.info(f"✅ Model loaded from {model_path}")

    def _load_ensemble(self) -> EnsembleModel:
        """Load all models for ensemble."""
        models = []
        for name in ["lstm", "cnn_lstm", "convlstm", "transformer"]:
            model_path = self.model_dir / name / "best_model.h5"
            if model_path.exists():
                model_class = {
                    "lstm": LSTMModel,
                    "cnn_lstm": CNNLSTMModel,
                    "convlstm": ConvLSTMModel,
                    "transformer": TransformerModel,
                }[name]
                model = model_class()
                model.load(str(model_path))
                models.append(model)
                logger.info(f"✅ Loaded {name} for ensemble")

        return EnsembleModel(models)

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

        # Scale if scaler is available
        if self.scaler is not None:
            X = self.scaler.transform(X)

        return self.model.predict(X)

    def predict_from_df(
        self,
        df: pd.DataFrame,
        feature_cols: Optional[list] = None,
    ) -> np.ndarray:
        """
        Make predictions from DataFrame.

        Args:
            df (pd.DataFrame): Input DataFrame
            feature_cols (list): Feature column names (overrides stored)

        Returns:
            np.ndarray: Predictions
        """
        cols = feature_cols or self.feature_cols
        if cols is None:
            raise ValueError("Feature columns not specified. Provide feature_cols.")

        X = df[cols].values
        return self.predict(X)

    def predict_with_uncertainty(
        self,
        X: np.ndarray,
        n_samples: int = 10,
    ) -> Dict[str, np.ndarray]:
        """
        Make predictions with uncertainty estimates.

        Args:
            X (np.ndarray): Features
            n_samples (int): Number of samples for uncertainty

        Returns:
            dict: Predictions with uncertainty
        """
        predictions = []
        for _ in range(n_samples):
            pred = self.predict(X)
            predictions.append(pred)

        predictions = np.array(predictions)

        return {
            "mean": np.mean(predictions, axis=0),
            "std": np.std(predictions, axis=0),
            "lower": np.percentile(predictions, 2.5, axis=0),
            "upper": np.percentile(predictions, 97.5, axis=0),
        }