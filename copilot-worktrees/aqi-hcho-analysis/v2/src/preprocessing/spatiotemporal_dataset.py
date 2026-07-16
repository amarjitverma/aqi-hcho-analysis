# ============================================================
# Spatiotemporal Dataset Creator
# ============================================================

"""
Creates 4D spatiotemporal grids for CNN-LSTM/ConvLSTM models.
"""

import numpy as np
from loguru import logger


def create_spatiotemporal_grid(
    data: np.ndarray,
    seq_length: int = 7,
    grid_shape: tuple = (120, 120),
    stride: int = 1,
) -> np.ndarray:
    """
    Create spatiotemporal grid for CNN-LSTM/ConvLSTM.

    Args:
        data (np.ndarray): 4D array (time, lat, lon, channels)
        seq_length (int): Sequence length
        grid_shape (tuple): Grid dimensions (height, width)
        stride (int): Stride between sequences

    Returns:
        np.ndarray: Spatiotemporal grid (samples, time, height, width, channels)
    """
    logger.info(f"📊 Creating spatiotemporal grid with sequence length {seq_length}...")

    n_time, h, w, c = data.shape
    n_samples = (n_time - seq_length) // stride + 1

    grid = np.zeros((n_samples, seq_length, h, w, c))

    for i in range(n_samples):
        start_idx = i * stride
        grid[i] = data[start_idx : start_idx + seq_length]

    logger.info(f"  Created grid shape: {grid.shape}")
    return grid


if __name__ == "__main__":
    # Test with sample data
    test_data = np.random.randn(100, 120, 120, 6)
    grid = create_spatiotemporal_grid(test_data, seq_length=7)
    print(f"Grid shape: {grid.shape}")