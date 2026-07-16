# ============================================================
# Fire-HCHO Correlation Analysis
# ============================================================

"""Lagged correlation analysis between fire counts and HCHO levels."""

import numpy as np
import pandas as pd
from scipy.stats import pearsonr, spearmanr
from loguru import logger


def lagged_correlation(fire_counts, hcho_values, max_lag=3):
    """
    Calculate lagged correlation between fire counts and HCHO.

    Args:
        fire_counts (np.ndarray): Daily fire counts
        hcho_values (np.ndarray): Daily HCHO values
        max_lag (int): Maximum lag in days

    Returns:
        pd.DataFrame: Correlation results by lag
    """
    logger.info(f"📈 Calculating lagged correlation (max lag: {max_lag})")

    results = []
    for lag in range(max_lag + 1):
        if lag == 0:
            fire_lagged = fire_counts
            hcho_aligned = hcho_values
        else:
            fire_lagged = fire_counts[:-lag]
            hcho_aligned = hcho_values[lag:]

        min_len = min(len(fire_lagged), len(hcho_aligned))
        fire_lagged = fire_lagged[:min_len]
        hcho_aligned = hcho_aligned[:min_len]

        pearson_r, pearson_p = pearsonr(fire_lagged, hcho_aligned)
        spearman_r, spearman_p = spearmanr(fire_lagged, hcho_aligned)

        results.append({
            "lag_days": lag,
            "pearson_r": pearson_r,
            "pearson_p": pearson_p,
            "spearman_r": spearman_r,
            "spearman_p": spearman_p,
            "n_samples": min_len
        })

    df = pd.DataFrame(results)

    # Find optimal lag
    best_idx = df["pearson_r"].idxmax()
    optimal_lag = int(df.loc[best_idx, "lag_days"])

    logger.info(f"  Optimal lag: {optimal_lag} days (r = {df.loc[best_idx, 'pearson_r']:.3f})")

    return df


def calculate_source_contribution(clusters):
    """
    Calculate source region contribution percentages.

    Args:
        clusters (dict): Cluster data from hotspot detection

    Returns:
        pd.DataFrame: Source contributions
    """
    if not clusters:
        logger.warning("No clusters provided")
        return pd.DataFrame()

    total = sum(c["mean_hcho"] * c["num_cells"] for c in clusters.values())

    contributions = []
    for cluster in clusters.values():
        cluster_total = cluster["mean_hcho"] * cluster["num_cells"]
        contributions.append({
            "source_region": cluster["source_region"],
            "num_cells": cluster["num_cells"],
            "mean_hcho": cluster["mean_hcho"],
            "total_contribution": cluster_total,
            "percentage": (cluster_total / total) * 100 if total > 0 else 0
        })

    df = pd.DataFrame(contributions)
    df = df.sort_values("percentage", ascending=False)

    logger.info("  Source attribution:")
    for _, row in df.iterrows():
        logger.info(f"    {row['source_region']}: {row['percentage']:.1f}%")

    return df


if __name__ == "__main__":
    # Test with sample data
    np.random.seed(42)
    fire_counts = np.random.poisson(10, 100)
    hcho_values = fire_counts * 0.5 + np.random.randn(100) * 0.1

    results = lagged_correlation(fire_counts, hcho_values)
    print(results)