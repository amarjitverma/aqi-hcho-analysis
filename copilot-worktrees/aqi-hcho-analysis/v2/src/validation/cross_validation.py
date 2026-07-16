# ============================================================
# Cross Validation
# ============================================================

"""Cross-validation methods for model evaluation."""

import numpy as np
from sklearn.model_selection import TimeSeriesSplit, KFold
from loguru import logger
from typing import Any, Callable, Dict, List, Tuple


def cross_validate(
    model_fn: Callable,
    X: np.ndarray,
    y: np.ndarray,
    cv: int = 5,
    method: str = "kfold",
    **kwargs,
) -> Dict[str, List[float]]:
    """
    Perform cross-validation on the model.

    Args:
        model_fn (callable): Function that builds and trains a model
        X (np.ndarray): Features
        y (np.ndarray): Targets
        cv (int): Number of folds
        method (str): 'kfold' or 'timeseries'
        **kwargs: Additional arguments for model_fn

    Returns:
        dict: Cross-validation results
    """
    logger.info(f"🔄 Performing {method} cross-validation ({cv} folds)")

    if method == "timeseries":
        splitter = TimeSeriesSplit(n_splits=cv)
    else:
        splitter = KFold(n_splits=cv, shuffle=True, random_state=42)

    results = {"rmse": [], "mae": [], "r2": [], "mape": []}

    for fold, (train_idx, val_idx) in enumerate(splitter.split(X)):
        X_train, X_val = X[train_idx], X[val_idx]
        y_train, y_val = y[train_idx], y[val_idx]

        # Build and train model
        model = model_fn(**kwargs)
        model.fit(X_train, y_train)

        # Predict and evaluate
        y_pred = model.predict(X_val)
        from src.evaluation.metrics import calculate_all_metrics

        metrics = calculate_all_metrics(y_val, y_pred)

        for key in results.keys():
            results[key].append(metrics[key])

        logger.info(f"  Fold {fold+1}: RMSE = {metrics['rmse']:.4f}")

    # Compute mean and std
    summary = {}
    for key, values in results.items():
        summary[f"{key}_mean"] = np.mean(values)
        summary[f"{key}_std"] = np.std(values)

    logger.info(f"✅ Cross-validation complete")
    logger.info(f"  RMSE: {summary['rmse_mean']:.4f} (±{summary['rmse_std']:.4f})")
    logger.info(f"  R²: {summary['r2_mean']:.4f} (±{summary['r2_std']:.4f})")

    return {"results": results, "summary": summary}