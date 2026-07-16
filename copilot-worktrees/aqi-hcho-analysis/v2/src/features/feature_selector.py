# ============================================================
# Feature Selector
# ============================================================

"""Feature selection methods."""

import pandas as pd
import numpy as np
from sklearn.feature_selection import SelectKBest, f_regression, mutual_info_regression
from sklearn.ensemble import RandomForestRegressor
from loguru import logger


def select_features(
    X: pd.DataFrame,
    y: pd.Series,
    method: str = "mutual_info",
    k: int = 20,
) -> tuple:
    """
    Select top k features using specified method.

    Args:
        X (pd.DataFrame): Feature matrix
        y (pd.Series): Target
        method (str): 'mutual_info', 'f_regression', or 'rf'
        k (int): Number of features to select

    Returns:
        tuple: (selected_X, selected_features)
    """
    logger.info(f"🔍 Selecting top {k} features using {method}...")

    if method == "mutual_info":
        selector = SelectKBest(mutual_info_regression, k=k)
    elif method == "f_regression":
        selector = SelectKBest(f_regression, k=k)
    elif method == "rf":
        selector = RandomForestFeatureSelector(k=k)
    else:
        raise ValueError(f"Unknown method: {method}")

    selected_X = selector.fit_transform(X, y)
    selected_features = X.columns[selector.get_support()].tolist()

    logger.info(f"  Selected features: {selected_features}")
    return selected_X, selected_features


class RandomForestFeatureSelector:
    """Feature selector using Random Forest importance."""

    def __init__(self, k: int = 20, random_state: int = 42):
        self.k = k
        self.random_state = random_state
        self.support_ = None

    def fit_transform(self, X, y):
        rf = RandomForestRegressor(n_estimators=100, random_state=self.random_state)
        rf.fit(X, y)

        # Get feature importances
        importances = rf.feature_importances_
        indices = np.argsort(importances)[::-1][:self.k]

        self.support_ = np.zeros(len(X.columns), dtype=bool)
        self.support_[indices] = True

        return X.iloc[:, indices]


def correlation_selection(X: pd.DataFrame, y: pd.Series, threshold: float = 0.3) -> list:
    """
    Select features based on correlation with target.

    Args:
        X (pd.DataFrame): Feature matrix
        y (pd.Series): Target
        threshold (float): Minimum absolute correlation

    Returns:
        list: Selected feature names
    """
    correlations = X.corrwith(y).abs()
    selected = correlations[correlations > threshold].index.tolist()

    logger.info(f"  Selected {len(selected)} features with correlation > {threshold}")
    return selected


if __name__ == "__main__":
    # Test with sample data
    X = pd.DataFrame(
        {
            "feature1": np.random.randn(100),
            "feature2": np.random.randn(100),
            "feature3": np.random.randn(100) + 2 * np.random.randn(100),
        }
    )
    y = pd.Series(np.random.randn(100))
    selected_X, selected_features = select_features(X, y, k=2)
    print(f"Selected features: {selected_features}")