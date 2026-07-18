# ============================================================
# Trend Analysis
# ============================================================

"""Long-term trend analysis for HCHO and AQI."""

import numpy as np
import pandas as pd
from scipy import stats
from loguru import logger


class TrendAnalyzer:
    """Analyze long-term trends in air quality data."""

    def __init__(self):
        self.trend_results = None

    def compute_trend(self, data, time_steps):
        """
        Compute linear trend using Theil-Sen or OLS regression.

        Args:
            data (np.ndarray): Time series data
            time_steps (np.ndarray): Time indices

        Returns:
            dict: Trend statistics
        """
        logger.info("📈 Computing trend...")

        # Linear regression (OLS)
        slope, intercept, r_value, p_value, std_err = stats.linregress(time_steps, data)

        # Theil-Sen robust regression
        from scipy.stats import theilslopes

        theil_slope, theil_intercept, _, _ = theilslopes(data, time_steps)

        # Mann-Kendall test for monotonic trend
        from scipy.stats import kendalltau

        tau, mk_p_value = kendalltau(time_steps, data)

        results = {
            "slope_ols": slope,
            "intercept_ols": intercept,
            "r2": r_value**2,
            "p_value_ols": p_value,
            "slope_theil": theil_slope,
            "intercept_theil": theil_intercept,
            "mann_kendall_tau": tau,
            "mann_kendall_p": mk_p_value,
            "significant": p_value < 0.05,
        }

        self.trend_results = results

        logger.info(f"  Slope (OLS): {slope:.4f} per time step")
        logger.info(f"  R²: {r_value**2:.4f}")
        logger.info(f"  Significant: {p_value < 0.05}")

        return results

    def decompose_seasonality(self, data, period=12):
        """
        Decompose time series into trend, seasonal, and residual components.

        Args:
            data (np.ndarray): Time series data
            period (int): Seasonal period

        Returns:
            dict: Decomposition components
        """
        from statsmodels.tsa.seasonal import seasonal_decompose

        logger.info(f"📊 Decomposing seasonality (period={period})")

        # Create time series
        ts = pd.Series(data)

        try:
            result = seasonal_decompose(ts, model="additive", period=period)

            decomposition = {
                "trend": result.trend.values,
                "seasonal": result.seasonal.values,
                "residual": result.resid.values,
                "observed": result.observed.values,
            }

            self.trend_results = {"decomposition": decomposition}

            return decomposition

        except Exception as e:
            logger.error(f"Decomposition failed: {e}")
            return None

    def detect_change_points(self, data, method="pelt"):
        """
        Detect change points in time series.

        Args:
            data (np.ndarray): Time series data
            method (str): Detection method ('pelt', 'binary_segmentation')

        Returns:
            list: Change point indices
        """
        logger.info("🔍 Detecting change points...")

        try:
            import ruptures as rpt

            # Convert to 2D array
            data_2d = data.reshape(-1, 1)

            if method == "pelt":
                algo = rpt.Pelt(model="rbf").fit(data_2d)
                change_points = algo.predict(pen=10)
            elif method == "binary_segmentation":
                algo = rpt.BinarySegmentation(model="l2").fit(data_2d)
                change_points = algo.predict(n_bkps=3)
            else:
                raise ValueError(f"Unknown method: {method}")

            logger.info(f"  Found {len(change_points)} change points")
            return change_points

        except ImportError:
            logger.warning("ruptures not installed, skipping change point detection")
            return []


if __name__ == "__main__":
    # Test with sample data
    time_steps = np.arange(100)
    data = 10 + 0.5 * time_steps + np.random.randn(100) * 2

    analyzer = TrendAnalyzer()
    results = analyzer.compute_trend(data, time_steps)
    print(f"Slope: {results['slope_ols']:.3f}")
    print(f"Significant: {results['significant']}")
