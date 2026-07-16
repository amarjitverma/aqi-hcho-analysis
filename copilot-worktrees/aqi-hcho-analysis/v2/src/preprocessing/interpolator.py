# ============================================================
# Gap-Filling Interpolator
# ============================================================

"""
Fills gaps in satellite data using temporal and spatial interpolation.
"""

import numpy as np
from scipy.ndimage import gaussian_filter
from scipy.interpolate import griddata
from loguru import logger


def fill_gaps(
    data: np.ndarray,
    temporal_window: int = 3,
    spatial_window: int = 3,
    sigma: float = 1.0,
    method: str = "gaussian",
) -> np.ndarray:
    """
    Fill gaps in data using temporal and spatial interpolation.

    Args:
        data (np.ndarray): 2D or 3D array (time, lat, lon) or (lat, lon)
        temporal_window (int): Temporal window size
        spatial_window (int): Spatial window size
        sigma (float): Gaussian filter sigma
        method (str): 'gaussian' or 'nearest'

    Returns:
        np.ndarray: Gap-filled data
    """
    logger.info("🔧 Filling gaps in data...")

    # Handle 2D data
    if data.ndim == 2:
        return _fill_gaps_2d(data, spatial_window, sigma, method)

    # Handle 3D data (time, lat, lon)
    filled = data.copy()
    n_time = data.shape[0]

    # Temporal gap-filling
    for t in range(n_time):
        if np.isnan(data[t]).all():
            # Find nearest valid time step
            for dt in range(1, temporal_window + 1):
                if t - dt >= 0 and not np.isnan(data[t - dt]).all():
                    filled[t] = data[t - dt]
                    break
                elif t + dt < n_time and not np.isnan(data[t + dt]).all():
                    filled[t] = data[t + dt]
                    break

    # Spatial gap-filling
    for t in range(n_time):
        if np.isnan(filled[t]).any():
            filled[t] = _fill_gaps_2d(filled[t], spatial_window, sigma, method)

    logger.info(f"  Filled gaps for {n_time} time steps")
    return filled


def _fill_gaps_2d(data: np.ndarray, window: int = 3, sigma: float = 1.0, method: str = "gaussian") -> np.ndarray:
    """Fill gaps in 2D data."""
    if method == "gaussian":
        # Create masked array
        masked = np.ma.masked_where(np.isnan(data), data)
        filled = gaussian_filter(masked.filled(0), sigma=sigma)
        # Restore original values where present
        filled[~np.isnan(data)] = data[~np.isnan(data)]
        return filled

    elif method == "nearest":
        # Use nearest neighbor interpolation
        x = np.arange(data.shape[1])
        y = np.arange(data.shape[0])
        x_grid, y_grid = np.meshgrid(x, y)

        # Get valid points
        valid = ~np.isnan(data)
        points = np.column_stack([y_grid[valid], x_grid[valid]])
        values = data[valid]

        if len(points) == 0:
            return np.zeros_like(data)

        # Interpolate
        filled = griddata(points, values, (y_grid, x_grid), method="nearest")
        return filled

    else:
        raise ValueError(f"Unknown method: {method}")


def interpolate_missing_by_time(
    data: np.ndarray,
    time_axis: int = 0,
    method: str = "linear",
) -> np.ndarray:
    """
    Interpolate missing values along time axis.

    Args:
        data (np.ndarray): Input data
        time_axis (int): Axis for time
        method (str): Interpolation method ('linear', 'nearest')

    Returns:
        np.ndarray: Interpolated data
    """
    from scipy.interpolate import interp1d

    filled = data.copy()
    n_time = data.shape[time_axis]

    # Transpose so time is first axis
    if time_axis != 0:
        data = np.moveaxis(data, time_axis, 0)

    for i in range(data.shape[1]):
        for j in range(data.shape[2]):
            values = data[:, i, j]
            if np.isnan(values).all():
                continue

            # Get valid indices
            valid_idx = ~np.isnan(values)
            if valid_idx.sum() < 2:
                continue

            # Interpolate
            x = np.arange(n_time)
            interp = interp1d(
                x[valid_idx],
                values[valid_idx],
                kind=method,
                fill_value="extrapolate",
                bounds_error=False,
            )
            data[:, i, j] = interp(x)

    # Move back to original axis order
    if time_axis != 0:
        data = np.moveaxis(data, 0, time_axis)

    return data


if __name__ == "__main__":
    # Test with sample data
    test_data = np.random.randn(10, 120, 120)
    test_data[0, 30:40, 40:50] = np.nan  # Add some gaps
    filled = fill_gaps(test_data)
    print(f"Gaps remaining: {np.isnan(filled).sum()}")