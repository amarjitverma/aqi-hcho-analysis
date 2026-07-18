# ============================================================
# Postprocessing
# ============================================================

"""Post-processing of model predictions."""

import numpy as np
import pandas as pd
from loguru import logger
from typing import Optional, Dict, Any, Union


def postprocess_predictions(
    predictions: np.ndarray,
    original_shape: Optional[tuple] = None,
    clip_min: float = 0.0,
    clip_max: float = None,
    convert_to_aqi: bool = False,
) -> Union[np.ndarray, pd.DataFrame]:
    """
    Post-process model predictions.

    Args:
        predictions (np.ndarray): Raw predictions
        original_shape (tuple): Shape to reshape to
        clip_min (float): Minimum value for clipping
        clip_max (float): Maximum value for clipping
        convert_to_aqi (bool): Whether to convert PM2.5 to AQI

    Returns:
        np.ndarray or pd.DataFrame: Post-processed predictions
    """
    logger.info("🔧 Post-processing predictions...")

    result = predictions.copy()

    # Clip values
    if clip_min is not None or clip_max is not None:
        result = np.clip(result, clip_min, clip_max if clip_max is not None else np.inf)
        logger.info(f"  Clipped values to [{clip_min}, {clip_max}]")

    # Reshape
    if original_shape is not None:
        result = result.reshape(original_shape)
        logger.info(f"  Reshaped to {original_shape}")

    # Convert to AQI
    if convert_to_aqi:
        from src.data.preprocessor import calculate_aqi

        aqi_values = []
        for val in result.flatten():
            aqi_info = calculate_aqi(val)
            aqi_values.append(aqi_info["aqi"])

        result = np.array(aqi_values).reshape(result.shape)
        logger.info("  Converted to AQI values")

    return result


def create_prediction_report(
    y_true: Optional[np.ndarray],
    y_pred: np.ndarray,
    dates: Optional[np.ndarray] = None,
    locations: Optional[np.ndarray] = None,
) -> pd.DataFrame:
    """
    Create a prediction report.

    Args:
        y_true (np.ndarray): True values (optional)
        y_pred (np.ndarray): Predicted values
        dates (np.ndarray): Dates
        locations (np.ndarray): Locations

    Returns:
        pd.DataFrame: Prediction report
    """
    report = {"predicted": y_pred}

    if y_true is not None:
        report["actual"] = y_true
        report["error"] = y_true - y_pred
        report["abs_error"] = np.abs(report["error"])

    if dates is not None:
        report["date"] = dates

    if locations is not None:
        report["latitude"] = locations[:, 0]
        report["longitude"] = locations[:, 1]

    df = pd.DataFrame(report)
    logger.info(f"📊 Created prediction report with {len(df)} rows")

    return df
