# ============================================================
# Dashboard Utilities
# ============================================================

"""Utilities for generating dashboard data files."""

import json
import numpy as np
from pathlib import Path
from loguru import logger


def generate_aqi_grid(
    pm25_predictions, lat_grid, lon_grid, output_path="dashboard/cache/aqi_grid.json"
):
    """
    Generate AQI grid data from PM2.5 predictions.

    Args:
        pm25_predictions (np.ndarray): 2D PM2.5 predictions
        lat_grid (np.ndarray): 2D latitude grid
        lon_grid (np.ndarray): 2D longitude grid
        output_path (str): Output file path
    """
    from src.data.preprocessor import calculate_aqi

    # Convert PM2.5 to AQI
    aqi_grid = np.zeros_like(pm25_predictions)
    for i in range(pm25_predictions.shape[0]):
        for j in range(pm25_predictions.shape[1]):
            if not np.isnan(pm25_predictions[i, j]):
                result = calculate_aqi(pm25_predictions[i, j])
                aqi_grid[i, j] = result["aqi"]
            else:
                aqi_grid[i, j] = np.nan

    # Create GeoJSON
    features = []
    for i in range(aqi_grid.shape[0]):
        for j in range(aqi_grid.shape[1]):
            if not np.isnan(aqi_grid[i, j]) and aqi_grid[i, j] > 0:
                features.append(
                    {
                        "type": "Feature",
                        "geometry": {
                            "type": "Point",
                            "coordinates": [float(lon_grid[i, j]), float(lat_grid[i, j])],
                        },
                        "properties": {
                            "aqi": int(aqi_grid[i, j]),
                            "pm25": float(pm25_predictions[i, j]),
                        },
                    }
                )

    geojson = {"type": "FeatureCollection", "features": features}

    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w") as f:
        json.dump(geojson, f, indent=2)

    logger.info(f"💾 AQI grid exported to {output_path} ({len(features)} points)")


def generate_model_metrics(metrics, output_path="dashboard/cache/model_metrics.json"):
    """
    Generate model metrics JSON for dashboard.

    Args:
        metrics (dict): Model metrics
        output_path (str): Output file path
    """
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w") as f:
        json.dump(metrics, f, indent=2)

    logger.info(f"💾 Model metrics exported to {output_path}")


def generate_dashboard_data():
    """
    Generate all dashboard data files.

    This function should be called after model training and analysis.
    """
    logger.info("📊 Generating dashboard data...")

    # Placeholder: In real implementation, load from outputs/
    # 1. Load PM2.5 predictions and grids
    # 2. Generate AQI grid
    # 3. Load HCHO hotspots from analysis
    # 4. Load fire data
    # 5. Load wind data
    # 6. Load model metrics

    # Example: Generate dummy metrics
    dummy_metrics = {"rmse": 12.4, "mae": 8.7, "r2": 0.87, "mape": 14.2}
    generate_model_metrics(dummy_metrics)

    logger.info("✅ Dashboard data generation complete")


if __name__ == "__main__":
    generate_dashboard_data()
