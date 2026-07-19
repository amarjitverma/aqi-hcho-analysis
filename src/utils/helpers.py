# ============================================================
# Helper Functions
# ============================================================

"""Common helper functions."""

import os
import json
import yaml
import numpy as np
import pandas as pd
from functools import wraps
import time
from loguru import logger


def ensure_dir(path: str):
    """Create directory if it doesn't exist."""
    os.makedirs(path, exist_ok=True)
    return path


def timer(func):
    """Decorator to time function execution."""

    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()
        logger.info(f"⏱️ {func.__name__} took {end - start:.2f} seconds")
        return result

    return wrapper


def get_date_range(start_date: str, end_date: str):
    """Get list of dates between start and end."""
    start = pd.to_datetime(start_date)
    end = pd.to_datetime(end_date)
    return pd.date_range(start, end).tolist()


def flatten_2d_array(arr: np.ndarray) -> np.ndarray:
    """Flatten 2D array to 1D."""
    return arr.flatten()


def save_json(data: dict, filepath: str):
    """Save data as JSON file."""
    ensure_dir(os.path.dirname(filepath))
    with open(filepath, "w") as f:
        json.dump(data, f, indent=2)


def load_json(filepath: str) -> dict:
    """Load JSON file."""
    with open(filepath, "r") as f:
        return json.load(f)


def save_yaml(data: dict, filepath: str):
    """Save data as YAML file."""
    ensure_dir(os.path.dirname(filepath))
    with open(filepath, "w") as f:
        yaml.dump(data, f, default_flow_style=False)


def load_yaml(filepath: str) -> dict:
    """Load YAML file."""
    with open(filepath, "r") as f:
        return yaml.safe_load(f)


def get_season(month: int) -> str:
    """Get season name from month."""
    if month in [12, 1, 2]:
        return "winter"
    elif month in [3, 4, 5]:
        return "summer"
    elif month in [6, 7, 8]:
        return "monsoon"
    elif month in [9, 10, 11]:
        return "post_monsoon"
    return "unknown"


def print_progress(current: int, total: int, prefix: str = "", suffix: str = ""):
    """Print progress bar."""
    bar_length = 50
    progress = current / total
    filled = int(bar_length * progress)
    bar = "█" * filled + "░" * (bar_length - filled)
    print(f"\r{prefix} |{bar}| {progress * 100:.1f}% {suffix}", end="")


if __name__ == "__main__":
    # Test timer decorator
    @timer
    def test_func():
        time.sleep(1)

    test_func()
