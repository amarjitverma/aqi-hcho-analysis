# ============================================================
# Uncertainty Quantification
# ============================================================

"""Uncertainty quantification methods for model predictions."""

import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.gaussian_process import GaussianProcessRegressor
from loguru import logger


def uncertainty_quantification(
    model,
    X: np.ndarray,
    method: str = "ensemble",
    n_estimators: int = 100,
    alpha: float = 0.95,
) -> dict:
    """
    Quantify uncertainty in model predictions.

    Args:
        model: Trained model
        X (np.ndarray): Features
        method (str): 'ensemble' or 'gaussian_process'
        n_estimators (int): Number of estimators for ensemble
        alpha (float): Confidence level

    Returns:
        dict: Predictions with uncertainty intervals
    """
    logger.info(f"📊 Quantifying uncertainty using {method}")

    if method == "ensemble":
        return _ensemble_uncertainty(X, model, n_estimators, alpha)
    elif method == "gaussian_process":
        return _gaussian_process_uncertainty(X, model, alpha)
    else:
        raise ValueError(f"Unknown method: {method}")


def _ensemble_uncertainty(X, model, n_estimators, alpha):
    """Ensemble-based uncertainty."""
    from sklearn.ensemble import BaggingRegressor

    # Create ensemble
    ensemble = BaggingRegressor(
        estimator=model,
        n_estimators=n_estimators,
        random_state=42,
        n_jobs=-1,
    )

    # Fit on full data
    ensemble.fit(X, model._y_train if hasattr(model, "_y_train") else X)

    # Predict
    predictions = []
    for estimator in ensemble.estimators_:
        predictions.append(estimator.predict(X))
    predictions = np.array(predictions)

    # Compute statistics
    mean = np.mean(predictions, axis=0)
    std = np.std(predictions, axis=0)

    # Confidence intervals
    z_score = 1.96  # For 95% confidence
    lower = mean - z_score * std
    upper = mean + z_score * std

    return {
        "mean": mean,
        "std": std,
        "lower": lower,
        "upper": upper,
        "alpha": alpha,
    }


def _gaussian_process_uncertainty(X, model, alpha):
    """Gaussian Process-based uncertainty."""
    # This requires the model to be a GaussianProcessRegressor
    if not isinstance(model, GaussianProcessRegressor):
        logger.warning("Model is not GaussianProcessRegressor. Using ensemble instead.")
        return _ensemble_uncertainty(X, model, 100, alpha)

    y_mean, y_std = model.predict(X, return_std=True)

    # Confidence intervals
    from scipy.stats import norm

    z_score = norm.ppf((1 + alpha) / 2)
    lower = y_mean - z_score * y_std
    upper = y_mean + z_score * y_std

    return {
        "mean": y_mean,
        "std": y_std,
        "lower": lower,
        "upper": upper,
        "alpha": alpha,
    }
