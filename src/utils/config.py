# ============================================================
# Configuration Loader
# ============================================================

"""Loads configuration from YAML files."""

import os
import yaml
from pathlib import Path
from loguru import logger


def load_config(config_path: str = "config/config.yaml") -> dict:
    """
    Load configuration from YAML file.

    Args:
        config_path (str): Path to config file

    Returns:
        dict: Configuration dictionary
    """
    config_file = Path(config_path)

    if not config_file.exists():
        logger.warning(f"Config file not found: {config_path}. Using defaults.")
        return get_default_config()

    with open(config_file, "r") as f:
        config = yaml.safe_load(f)

    logger.info(f"✅ Loaded configuration from {config_path}")
    return config


def get_default_config() -> dict:
    """Get default configuration."""
    return {
        "project": {
            "name": "aqi-hcho-analysis",
            "version": "1.0.0",
            "description": "Satellite-Based Surface AQI Prediction & HCHO Hotspot Analysis",
        },
        "data": {
            "grid_resolution": 0.25,
            "grid_size": 120,
            "india_bounds": {"lat_min": 8, "lat_max": 38, "lon_min": 68, "lon_max": 98},
        },
        "model": {
            "lstm": {
                "seq_length": 7,
                "lstm_units": 128,
                "dropout_rate": 0.3,
                "batch_size": 32,
                "epochs": 100,
            },
            "cnn_lstm": {
                "seq_length": 7,
                "conv_filters": 64,
                "lstm_units": 128,
                "batch_size": 16,
                "epochs": 100,
            },
            "convlstm": {
                "seq_length": 7,
                "filters": 64,
                "kernel_size": 3,
                "lstm_units": 128,
                "batch_size": 16,
                "epochs": 100,
            },
            "transformer": {
                "seq_length": 7,
                "d_model": 128,
                "n_heads": 8,
                "n_layers": 4,
                "batch_size": 32,
                "epochs": 100,
            },
        },
        "analysis": {
            "dbscan_eps": 0.5,
            "dbscan_min_samples": 4,
            "hcho_percentile": 90,
            "max_lag": 3,
            "decay_constant": 0.02,
        },
        "dashboard": {"port": 8501, "theme": "dark"},
    }


if __name__ == "__main__":
    config = load_config()
    print(f"Project: {config['project']['name']}")
