# ============================================================
# Spatial Interpolation
# ============================================================

"""Spatial interpolation methods."""

import numpy as np
from scipy.interpolate import griddata, RBFInterpolator
from scipy.spatial import cKDTree
from loguru import logger


def interpolate_spatial(
    points: np.ndarray,
    values: np.ndarray,
    grid_points: np.ndarray,
    method: str = "linear",
) -> np.ndarray:
    """
    Interpolate values to grid points.

    Args:
        points (np.ndarray): Known points (n, 2) [lon, lat]
        values (np.ndarray): Known values (n,)
        grid_points (np.ndarray): Target grid points (m, 2)
        method (str): 'linear', 'nearest', 'cubic', 'rbf'

    Returns:
        np.ndarray: Interpolated values
    """
    logger.info(f"📐 Interpolating with method: {method}")

    if method == "rbf":
        # Radial Basis Function interpolation
        rbf = RBFInterpolator(points, values, kernel="gaussian", epsilon=1.0)
        return rbf(grid_points).flatten()

    elif method in ["linear", "nearest", "cubic"]:
        return griddata(points, values, grid_points, method=method)

    else:
        raise ValueError(f"Unknown method: {method}")


def idw_interpolation(
    points: np.ndarray,
    values: np.ndarray,
    grid_points: np.ndarray,
    power: float = 2.0,
    radius: float = None,
) -> np.ndarray:
    """
    Inverse Distance Weighting interpolation.

    Args:
        points (np.ndarray): Known points (n, 2)
        values (np.ndarray): Known values (n,)
        grid_points (np.ndarray): Target grid points (m, 2)
        power (float): Power parameter
        radius (float): Search radius

    Returns:
        np.ndarray: Interpolated values
    """
    logger.info(f"📐 IDW interpolation (power={power})")

    tree = cKDTree(points)
    m = len(grid_points)
    result = np.zeros(m)

    for i, gp in enumerate(grid_points):
        # Find nearest neighbors
        if radius:
            idx = tree.query_ball_point(gp, radius)
        else:
            # Query all points
            idx = list(range(len(points)))

        if not idx:
            # No points in radius, use nearest
            idx = tree.query(gp)[1]
            idx = [idx] if isinstance(idx, (int, np.integer)) else idx[:1]

        # Compute weights
        dist = np.linalg.norm(points[idx] - gp, axis=1)
        dist = np.maximum(dist, 1e-10)  # Avoid division by zero
        weights = 1 / (dist ** power)
        weights /= weights.sum()

        result[i] = np.sum(values[idx] * weights)

    return result


def nearest_neighbor_interpolation(
    points: np.ndarray,
    values: np.ndarray,
    grid_points: np.ndarray,
) -> np.ndarray:
    """
    Nearest neighbor interpolation.

    Args:
        points (np.ndarray): Known points (n, 2)
        values (np.ndarray): Known values (n,)
        grid_points (np.ndarray): Target grid points (m, 2)

    Returns:
        np.ndarray: Interpolated values
    """
    tree = cKDTree(points)
    _, idx = tree.query(grid_points)
    return values[idx]


if __name__ == "__main__":
    # Test with sample data
    points = np.random.randn(100, 2)
    values = np.random.randn(100)
    grid = np.random.randn(1000, 2)

    result = interpolate_spatial(points, values, grid)
    print(f"Interpolated {len(result)} points")