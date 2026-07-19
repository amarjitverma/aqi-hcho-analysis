# ============================================================
# Spatial Validation
# ============================================================

"""Spatial validation methods for geospatial predictions."""

import numpy as np
from loguru import logger


def spatial_validation(
    model_fn: callable,
    X: np.ndarray,
    y: np.ndarray,
    coords: np.ndarray,
    n_folds: int = 5,
    distance_threshold: float = 1.0,
) -> dict:
    """
    Perform spatial block cross-validation.

    Args:
        model_fn (callable): Function that builds and trains a model
        X (np.ndarray): Features
        y (np.ndarray): Targets
        coords (np.ndarray): Spatial coordinates (lat, lon)
        n_folds (int): Number of folds
        distance_threshold (float): Distance threshold for spatial blocks

    Returns:
        dict: Spatial validation results
    """
    logger.info(f"🌍 Performing spatial validation ({n_folds} folds)")

    # Cluster points spatially
    from sklearn.cluster import KMeans

    kmeans = KMeans(n_clusters=n_folds, random_state=42)
    cluster_labels = kmeans.fit_predict(coords)

    results = {"rmse": [], "mae": [], "r2": [], "mape": []}

    for fold in range(n_folds):
        val_idx = cluster_labels == fold
        train_idx = cluster_labels != fold

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

    logger.info("✅ Spatial validation complete")
    logger.info(f"  RMSE: {summary['rmse_mean']:.4f} (±{summary['rmse_std']:.4f})")

    return {"results": results, "summary": summary}
