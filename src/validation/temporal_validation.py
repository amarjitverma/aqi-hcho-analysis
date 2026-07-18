# ============================================================
# Temporal Validation
# ============================================================

"""Temporal validation methods for time-series predictions."""

import numpy as np
from sklearn.model_selection import TimeSeriesSplit
from loguru import logger


def temporal_validation(
    model_fn: callable,
    X: np.ndarray,
    y: np.ndarray,
    n_splits: int = 5,
    test_size: int = None,
) -> dict:
    """
    Perform time-series cross-validation.

    Args:
        model_fn (callable): Function that builds and trains a model
        X (np.ndarray): Features
        y (np.ndarray): Targets
        n_splits (int): Number of splits
        test_size (int): Size of test set

    Returns:
        dict: Temporal validation results
    """
    logger.info(f"⏰ Performing temporal validation ({n_splits} splits)")

    tscv = TimeSeriesSplit(n_splits=n_splits, test_size=test_size)

    results = {"rmse": [], "mae": [], "r2": [], "mape": []}

    for fold, (train_idx, val_idx) in enumerate(tscv.split(X)):
        X_train, X_val = X[train_idx], X[val_idx]
        y_train, y_val = y[train_idx], y[val_idx]

        # Build and train model
        model = model_fn()
        model.fit(X_train, y_train)

        # Predict and evaluate
        y_pred = model.predict(X_val)
        from src.evaluation.metrics import calculate_all_metrics

        metrics = calculate_all_metrics(y_val, y_pred)

        for key in results.keys():
            results[key].append(metrics[key])

        logger.info(f"  Fold {fold+1}: RMSE = {metrics['rmse']:.4f}")

    summary = {}
    for key, values in results.items():
        summary[f"{key}_mean"] = np.mean(values)
        summary[f"{key}_std"] = np.std(values)

    logger.info(f"✅ Temporal validation complete")
    logger.info(f"  RMSE: {summary['rmse_mean']:.4f} (±{summary['rmse_std']:.4f})")

    return {"results": results, "summary": summary}
