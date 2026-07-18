# ============================================================
# Evaluation Visualizer
# ============================================================

"""Visualization tools for model evaluation."""

import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from pathlib import Path
from loguru import logger
from typing import Optional, Dict, List


def plot_predicted_vs_actual(
    y_true: np.ndarray,
    y_pred: np.ndarray,
    title: str = "Predicted vs Actual",
    save_path: Optional[str] = None,
) -> None:
    """
    Plot predicted vs actual values.

    Args:
        y_true (np.ndarray): True values
        y_pred (np.ndarray): Predicted values
        title (str): Plot title
        save_path (str): Path to save the plot
    """
    fig, ax = plt.subplots(figsize=(8, 8))

    # Scatter plot
    ax.scatter(y_true, y_pred, alpha=0.5, s=20, color="#1A73E8")

    # Perfect prediction line
    min_val = min(y_true.min(), y_pred.min())
    max_val = max(y_true.max(), y_pred.max())
    ax.plot([min_val, max_val], [min_val, max_val], "r--", linewidth=2, label="Perfect Prediction")

    ax.set_xlabel("Actual PM2.5 (µg/m³)", fontsize=12)
    ax.set_ylabel("Predicted PM2.5 (µg/m³)", fontsize=12)
    ax.set_title(title, fontsize=14)
    ax.legend()
    ax.grid(True, alpha=0.3)

    plt.tight_layout()

    if save_path:
        Path(save_path).parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(save_path, dpi=150)
        logger.info(f"📊 Plot saved to {save_path}")

    plt.close()


def plot_residuals(
    y_true: np.ndarray,
    y_pred: np.ndarray,
    title: str = "Residuals Analysis",
    save_path: Optional[str] = None,
) -> None:
    """
    Plot residuals analysis.

    Args:
        y_true (np.ndarray): True values
        y_pred (np.ndarray): Predicted values
        title (str): Plot title
        save_path (str): Path to save the plot
    """
    residuals = y_true - y_pred

    fig, axes = plt.subplots(2, 2, figsize=(12, 10))

    # Residuals vs Predicted
    axes[0, 0].scatter(y_pred, residuals, alpha=0.5, s=20, color="#1A73E8")
    axes[0, 0].axhline(y=0, color="r", linestyle="--")
    axes[0, 0].set_xlabel("Predicted PM2.5 (µg/m³)")
    axes[0, 0].set_ylabel("Residuals (µg/m³)")
    axes[0, 0].set_title("Residuals vs Predicted")
    axes[0, 0].grid(True, alpha=0.3)

    # Histogram of residuals
    axes[0, 1].hist(residuals, bins=30, edgecolor="black", color="#1A73E8", alpha=0.7)
    axes[0, 1].axvline(x=0, color="r", linestyle="--")
    axes[0, 1].set_xlabel("Residuals (µg/m³)")
    axes[0, 1].set_ylabel("Frequency")
    axes[0, 1].set_title("Distribution of Residuals")
    axes[0, 1].grid(True, alpha=0.3)

    # QQ Plot
    from scipy import stats

    stats.probplot(residuals, dist="norm", plot=axes[1, 0])
    axes[1, 0].set_title("QQ Plot of Residuals")

    # Error vs Time (assuming order matters)
    axes[1, 1].plot(residuals, color="#1A73E8", alpha=0.7)
    axes[1, 1].axhline(y=0, color="r", linestyle="--")
    axes[1, 1].set_xlabel("Sample Index")
    axes[1, 1].set_ylabel("Residuals (µg/m³)")
    axes[1, 1].set_title("Residuals by Sample")
    axes[1, 1].grid(True, alpha=0.3)

    plt.suptitle(title, fontsize=14)
    plt.tight_layout()

    if save_path:
        Path(save_path).parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(save_path, dpi=150)
        logger.info(f"📊 Residuals plot saved to {save_path}")

    plt.close()


def plot_metrics_comparison(
    metrics: Dict[str, Dict[str, float]],
    metrics_to_show: List[str] = ["rmse", "mae", "r2", "mape"],
    title: str = "Model Comparison",
    save_path: Optional[str] = None,
) -> None:
    """
    Plot comparison of model metrics.

    Args:
        metrics (dict): {model_name: {metric: value}}
        metrics_to_show (list): Metrics to display
        title (str): Plot title
        save_path (str): Path to save the plot
    """
    if not metrics:
        logger.warning("No metrics to compare")
        return

    fig, axes = plt.subplots(1, len(metrics_to_show), figsize=(5 * len(metrics_to_show), 5))

    if len(metrics_to_show) == 1:
        axes = [axes]

    model_names = list(metrics.keys())

    for idx, metric in enumerate(metrics_to_show):
        ax = axes[idx]

        values = [metrics[model].get(metric, 0) for model in model_names]

        colors = plt.cm.viridis(np.linspace(0.2, 0.8, len(model_names)))

        bars = ax.bar(model_names, values, color=colors)

        # Add value labels
        for bar, val in zip(bars, values):
            if metric in ["r2"]:
                label = f"{val:.3f}"
            else:
                label = f"{val:.2f}"
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                bar.get_height() + 0.05 * max(values),
                label,
                ha="center",
                va="bottom",
                fontsize=10,
            )

        ax.set_ylabel(metric.upper())
        ax.set_title(metric.upper())
        ax.grid(True, alpha=0.3, axis="y")

    plt.suptitle(title, fontsize=14)
    plt.tight_layout()

    if save_path:
        Path(save_path).parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(save_path, dpi=150)
        logger.info(f"📊 Metrics comparison saved to {save_path}")

    plt.close()


def plot_learning_curves(
    history: Dict[str, List[float]],
    save_path: Optional[str] = None,
) -> None:
    """
    Plot training and validation learning curves.

    Args:
        history (dict): Training history
        save_path (str): Path to save the plot
    """
    fig, axes = plt.subplots(1, 2, figsize=(12, 4))

    # Loss
    axes[0].plot(history.get("loss", []), label="Train Loss", color="#1A73E8")
    axes[0].plot(history.get("val_loss", []), label="Val Loss", color="#FF6B35")
    axes[0].set_xlabel("Epoch")
    axes[0].set_ylabel("Loss")
    axes[0].set_title("Loss")
    axes[0].legend()
    axes[0].grid(True, alpha=0.3)

    # MAE
    axes[1].plot(history.get("mae", []), label="Train MAE", color="#1A73E8")
    axes[1].plot(history.get("val_mae", []), label="Val MAE", color="#FF6B35")
    axes[1].set_xlabel("Epoch")
    axes[1].set_ylabel("MAE")
    axes[1].set_title("Mean Absolute Error")
    axes[1].legend()
    axes[1].grid(True, alpha=0.3)

    plt.tight_layout()

    if save_path:
        Path(save_path).parent.mkdir(parents=True, exist_ok=True)
        plt.savefig(save_path, dpi=150)
        logger.info(f"📊 Learning curves saved to {save_path}")

    plt.close()
