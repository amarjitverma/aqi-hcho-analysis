# ============================================================
# Ensemble Model
# ============================================================

"""Ensemble of multiple models."""

import numpy as np
from loguru import logger


class EnsembleModel:
    """Simple ensemble of models."""

    def __init__(self, models, weights=None):
        self.models = models
        self.weights = weights or [1.0 / len(models)] * len(models)

    def predict(self, X):
        """Make predictions using weighted average."""
        predictions = []
        for model, weight in zip(self.models, self.weights):
            pred = model.predict(X)
            predictions.append(pred * weight)
        return np.sum(predictions, axis=0)

    def evaluate(self, X, y):
        """Evaluate ensemble."""
        from sklearn.metrics import mean_squared_error, mean_absolute_error, r2_score

        y_pred = self.predict(X)
        return {
            "rmse": np.sqrt(mean_squared_error(y, y_pred)),
            "mae": mean_absolute_error(y, y_pred),
            "r2": r2_score(y, y_pred),
        }


def create_ensemble(models):
    """Create an ensemble of models."""
    logger.info(f"Creating ensemble of {len(models)} models")
    return EnsembleModel(models)
