# ============================================================
# Custom Loss Functions
# ============================================================

"""Custom loss functions for model training."""

import tensorflow as tf
import numpy as np


def mse_loss(y_true: tf.Tensor, y_pred: tf.Tensor) -> tf.Tensor:
    """Mean Squared Error loss."""
    return tf.reduce_mean(tf.square(y_true - y_pred))


def mae_loss(y_true: tf.Tensor, y_pred: tf.Tensor) -> tf.Tensor:
    """Mean Absolute Error loss."""
    return tf.reduce_mean(tf.abs(y_true - y_pred))


def huber_loss(y_true: tf.Tensor, y_pred: tf.Tensor, delta: float = 1.0) -> tf.Tensor:
    """Huber loss (robust to outliers)."""
    error = y_true - y_pred
    abs_error = tf.abs(error)

    quadratic = tf.minimum(abs_error, delta)
    linear = abs_error - quadratic

    return tf.reduce_mean(0.5 * quadratic**2 + delta * linear)


def weighted_mse_loss(y_true: tf.Tensor, y_pred: tf.Tensor, weights: tf.Tensor) -> tf.Tensor:
    """Weighted Mean Squared Error loss."""
    return tf.reduce_mean(weights * tf.square(y_true - y_pred))


def masked_mse_loss(y_true: tf.Tensor, y_pred: tf.Tensor, mask: tf.Tensor) -> tf.Tensor:
    """Masked Mean Squared Error loss."""
    return tf.reduce_mean(tf.boolean_mask(tf.square(y_true - y_pred), mask))


def quantile_loss(y_true: tf.Tensor, y_pred: tf.Tensor, quantile: float = 0.5) -> tf.Tensor:
    """Quantile loss for probabilistic forecasting."""
    error = y_true - y_pred
    return tf.reduce_mean(tf.maximum(quantile * error, (quantile - 1) * error))


def get_loss_function(name: str, **kwargs):
    """Get loss function by name."""
    losses = {
        "mse": mse_loss,
        "mae": mae_loss,
        "huber": huber_loss,
        "weighted_mse": weighted_mse_loss,
        "masked_mse": masked_mse_loss,
        "quantile": quantile_loss,
    }

    if name not in losses:
        raise ValueError(f"Unknown loss function: {name}")

    return losses[name]


if __name__ == "__main__":
    # Test loss functions
    y_true = tf.constant([1.0, 2.0, 3.0, 4.0])
    y_pred = tf.constant([1.2, 2.1, 2.9, 3.8])

    print(f"MSE: {mse_loss(y_true, y_pred):.4f}")
    print(f"MAE: {mae_loss(y_true, y_pred):.4f}")
    print(f"Huber: {huber_loss(y_true, y_pred):.4f}")