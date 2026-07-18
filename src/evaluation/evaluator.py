# ============================================================
# Evaluator
# ============================================================

"""Model evaluator class."""

import numpy as np
import pandas as pd
import json
from pathlib import Path
from loguru import logger
from typing import Dict, Any, Optional

from src.evaluation.metrics import calculate_all_metrics


class Evaluator:
    """
    Model evaluator.

    Handles model evaluation, metric calculation, and result storage.
    """

    def __init__(self, output_dir: str = "outputs/metrics/"):
        """
        Initialize the evaluator.

        Args:
            output_dir (str): Directory for metric outputs
        """
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)
        self.metrics = {}

    def evaluate(
        self,
        y_true: np.ndarray,
        y_pred: np.ndarray,
        model_name: str = "model",
        save_results: bool = True,
    ) -> Dict[str, float]:
        """
        Evaluate model predictions.

        Args:
            y_true (np.ndarray): True values
            y_pred (np.ndarray): Predicted values
            model_name (str): Name of the model
            save_results (bool): Whether to save results

        Returns:
            dict: Evaluation metrics
        """
        logger.info(f"📊 Evaluating {model_name}...")

        metrics = calculate_all_metrics(y_true, y_pred)

        # Add additional statistics
        metrics.update(
            {
                "n_samples": len(y_true),
                "mean_true": float(np.mean(y_true)),
                "mean_pred": float(np.mean(y_pred)),
                "std_true": float(np.std(y_true)),
                "std_pred": float(np.std(y_pred)),
            }
        )

        self.metrics[model_name] = metrics

        logger.info(f"  RMSE: {metrics['rmse']:.4f}")
        logger.info(f"  MAE: {metrics['mae']:.4f}")
        logger.info(f"  R²: {metrics['r2']:.4f}")
        logger.info(f"  MAPE: {metrics['mape']:.2f}%")

        if save_results:
            self.save_metrics(model_name, metrics)

        return metrics

    def evaluate_models(
        self,
        predictions: Dict[str, np.ndarray],
        y_true: np.ndarray,
        save_results: bool = True,
    ) -> Dict[str, Dict[str, float]]:
        """
        Evaluate multiple models.

        Args:
            predictions (dict): {model_name: predictions}
            y_true (np.ndarray): True values
            save_results (bool): Whether to save results

        Returns:
            dict: {model_name: metrics}
        """
        results = {}
        for model_name, y_pred in predictions.items():
            results[model_name] = self.evaluate(y_true, y_pred, model_name, save_results)

        return results

    def save_metrics(self, model_name: str, metrics: Dict[str, float]) -> None:
        """Save metrics to JSON file."""
        filepath = self.output_dir / f"{model_name}_metrics.json"
        # Convert numpy scalar types to native Python floats for JSON serialization
        serializable_metrics = {}
        for k, v in metrics.items():
            if isinstance(v, (np.float32, np.float64, np.int32, np.int64)):
                serializable_metrics[k] = float(v)
            else:
                serializable_metrics[k] = v
        with open(filepath, "w") as f:
            json.dump(serializable_metrics, f, indent=2)

        logger.info(f"💾 Metrics saved to {filepath}")

    def load_metrics(self, model_name: str) -> Dict[str, float]:
        """Load metrics from JSON file."""
        filepath = self.output_dir / f"{model_name}_metrics.json"
        if not filepath.exists():
            logger.warning(f"Metrics file not found: {filepath}")
            return {}

        with open(filepath, "r") as f:
            return json.load(f)

    def create_comparison_table(self, metrics: Dict[str, Dict[str, float]]) -> pd.DataFrame:
        """Create comparison table for multiple models."""
        df = pd.DataFrame(metrics).T
        # Select relevant columns
        columns = ["rmse", "mae", "r2", "mape", "n_samples"]
        available_cols = [c for c in columns if c in df.columns]
        return df[available_cols]
