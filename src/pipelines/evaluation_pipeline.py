# ============================================================
# Evaluation Pipeline
# ============================================================

"""Evaluation pipeline for model assessment."""

import numpy as np
import pandas as pd
from pathlib import Path
from loguru import logger
from typing import Dict, Any, Optional

from src.evaluation.evaluator import Evaluator
from src.evaluation.visualizer import (
    plot_predicted_vs_actual,
    plot_residuals,
    plot_metrics_comparison,
)


class EvaluationPipeline:
    """
    Evaluation pipeline for model assessment.
    """

    def __init__(self, output_dir: str = "outputs/"):
        """
        Initialize evaluation pipeline.

        Args:
            output_dir (str): Output directory
        """
        self.output_dir = Path(output_dir)
        self.evaluator = Evaluator(str(output_dir / "metrics"))

        # Create output directories
        (output_dir / "figures").mkdir(parents=True, exist_ok=True)

    def evaluate_model(
        self,
        y_true: np.ndarray,
        y_pred: np.ndarray,
        model_name: str = "model",
        save_results: bool = True,
    ) -> Dict[str, float]:
        """
        Evaluate a single model.

        Args:
            y_true (np.ndarray): True values
            y_pred (np.ndarray): Predicted values
            model_name (str): Name of the model
            save_results (bool): Whether to save results

        Returns:
            dict: Evaluation metrics
        """
        logger.info(f"📊 Evaluating {model_name}...")

        metrics = self.evaluator.evaluate(y_true, y_pred, model_name, save_results)

        # Generate plots
        plot_predicted_vs_actual(
            y_true,
            y_pred,
            title=f"{model_name}: Predicted vs Actual",
            save_path=str(self.output_dir / "figures" / f"{model_name}_predicted_vs_actual.png"),
        )

        plot_residuals(
            y_true,
            y_pred,
            title=f"{model_name}: Residuals Analysis",
            save_path=str(self.output_dir / "figures" / f"{model_name}_residuals.png"),
        )

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
            results[model_name] = self.evaluate_model(y_true, y_pred, model_name, save_results)

        # Generate comparison plot
        plot_metrics_comparison(
            results,
            save_path=str(self.output_dir / "figures" / "model_comparison.png"),
        )

        return results
