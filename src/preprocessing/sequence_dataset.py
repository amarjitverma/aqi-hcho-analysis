# ============================================================
# Sequence Dataset Creator
# ============================================================

"""
Creates time sequences for LSTM models.
"""

import numpy as np
import pandas as pd
from loguru import logger


def create_sequences(
    data: np.ndarray,
    target: np.ndarray,
    seq_length: int = 7,
    stride: int = 1,
) -> tuple:
    """
    Create sequences for LSTM training.

    Args:
        data (np.ndarray): Feature array (n_samples, n_features)
        target (np.ndarray): Target array (n_samples,)
        seq_length (int): Sequence length
        stride (int): Stride between sequences

    Returns:
        tuple: (X, y) sequences and targets
    """
    logger.info(f"📊 Creating sequences of length {seq_length}...")

    X, y = [], []
    for i in range(0, len(data) - seq_length, stride):
        X.append(data[i : i + seq_length])
        y.append(target[i + seq_length])

    X = np.array(X, dtype=np.float32)
    y = np.array(y, dtype=np.float32)

    logger.info(f"  Created {len(X)} sequences")
    logger.info(f"  X shape: {X.shape}, y shape: {y.shape}")
    return X, y


def create_sequences_from_df(
    df: pd.DataFrame,
    feature_cols: list,
    target_col: str,
    seq_length: int = 7,
) -> tuple:
    """
    Create sequences from DataFrame.

    Args:
        df (pd.DataFrame): Input DataFrame
        feature_cols (list): Feature column names
        target_col (str): Target column name
        seq_length (int): Sequence length

    Returns:
        tuple: (X, y, scaler)
    """
    from sklearn.preprocessing import StandardScaler

    # Extract features and target
    X_raw = df[feature_cols].values
    y_raw = df[target_col].values

    # Scale features
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X_raw)

    # Create sequences
    X_seq, y_seq = create_sequences(X_scaled, y_raw, seq_length)

    return X_seq, y_seq, scaler


if __name__ == "__main__":
    import pandas as pd

    # Test with sample data
    test_df = pd.DataFrame(
        {
            "feature1": np.random.randn(1000),
            "feature2": np.random.randn(1000),
            "target": np.random.randn(1000),
        }
    )
    X, y, scaler = create_sequences_from_df(
        test_df, ["feature1", "feature2"], "target", seq_length=7
    )
    print(f"X shape: {X.shape}, y shape: {y.shape}")