# ============================================================
# Training Callbacks
# ============================================================

"""Custom training callbacks."""

import os
import json
import numpy as np
import tensorflow as tf
from loguru import logger
from pathlib import Path
from typing import Dict, Any, Optional


class EarlyStopping(tf.keras.callbacks.Callback):
    """
    Custom early stopping callback.

    Stops training when a monitored metric has stopped improving.
    """

    def __init__(
        self,
        monitor: str = "val_loss",
        min_delta: float = 1e-4,
        patience: int = 10,
        mode: str = "min",
        restore_best_weights: bool = True,
        verbose: int = 1,
    ):
        super().__init__()
        self.monitor = monitor
        self.min_delta = min_delta
        self.patience = patience
        self.mode = mode
        self.restore_best_weights = restore_best_weights
        self.verbose = verbose
        self.best_weights = None
        self.best_epoch = 0
        self.best_value = None
        self.wait = 0
        self.stopped_epoch = 0

    def on_train_begin(self, logs=None):
        self.best_value = np.inf if self.mode == "min" else -np.inf
        self.wait = 0

    def on_epoch_end(self, epoch, logs=None):
        current = logs.get(self.monitor)
        if current is None:
            return

        if self._is_improvement(current):
            self.best_value = current
            self.best_epoch = epoch
            self.best_weights = self.model.get_weights()
            self.wait = 0
        else:
            self.wait += 1
            if self.wait >= self.patience:
                self.stopped_epoch = epoch
                self.model.stop_training = True
                if self.restore_best_weights and self.best_weights is not None:
                    self.model.set_weights(self.best_weights)
                    if self.verbose:
                        logger.info(
                            f"⏹️ Early stopping at epoch {epoch+1}, "
                            f"best {self.monitor}: {self.best_value:.4f}"
                        )

    def _is_improvement(self, current: float) -> bool:
        if self.mode == "min":
            return current < self.best_value - self.min_delta
        else:
            return current > self.best_value + self.min_delta


class ModelCheckpoint(tf.keras.callbacks.Callback):
    """
    Custom model checkpoint callback.
    """

    def __init__(
        self,
        filepath: str,
        monitor: str = "val_loss",
        mode: str = "min",
        save_best_only: bool = True,
        verbose: int = 1,
    ):
        super().__init__()
        self.filepath = Path(filepath)
        self.monitor = monitor
        self.mode = mode
        self.save_best_only = save_best_only
        self.verbose = verbose
        self.best_value = None

        # Create directory
        self.filepath.parent.mkdir(parents=True, exist_ok=True)

    def on_train_begin(self, logs=None):
        self.best_value = np.inf if self.mode == "min" else -np.inf

    def on_epoch_end(self, epoch, logs=None):
        current = logs.get(self.monitor)
        if current is None:
            return

        if self.save_best_only:
            if self._is_improvement(current):
                self.best_value = current
                self.model.save(self.filepath)
                if self.verbose:
                    logger.info(
                        f"💾 Checkpoint saved at epoch {epoch+1}: " f"{self.monitor} = {current:.4f}"
                    )
        else:
            # Save every epoch
            epoch_path = self.filepath.parent / f"epoch_{epoch+1:04d}.keras"
            self.model.save(epoch_path)

    def _is_improvement(self, current: float) -> bool:
        if self.mode == "min":
            return current < self.best_value
        else:
            return current > self.best_value


class ReduceLROnPlateau(tf.keras.callbacks.Callback):
    """
    Reduce learning rate when a metric has stopped improving.
    """

    def __init__(
        self,
        monitor: str = "val_loss",
        factor: float = 0.5,
        patience: int = 5,
        min_lr: float = 1e-7,
        verbose: int = 1,
    ):
        super().__init__()
        self.monitor = monitor
        self.factor = factor
        self.patience = patience
        self.min_lr = min_lr
        self.verbose = verbose
        self.wait = 0
        self.best_value = None

    def on_train_begin(self, logs=None):
        self.best_value = np.inf
        self.wait = 0

    def on_epoch_end(self, epoch, logs=None):
        current = logs.get(self.monitor)
        if current is None:
            return

        if current < self.best_value:
            self.best_value = current
            self.wait = 0
        else:
            self.wait += 1
            if self.wait >= self.patience:
                current_lr = float(tf.keras.backend.get_value(self.model.optimizer.learning_rate))
                new_lr = max(current_lr * self.factor, self.min_lr)

                if new_lr < current_lr:
                    tf.keras.backend.set_value(self.model.optimizer.learning_rate, new_lr)
                    if self.verbose:
                        logger.info(
                            f"📉 Reducing learning rate from {current_lr:.2e} to {new_lr:.2e}"
                        )
                    self.wait = 0


class TensorBoardCallback(tf.keras.callbacks.Callback):
    """TensorBoard logging callback."""

    def __init__(self, log_dir: str = "logs/tensorboard"):
        super().__init__()
        self.log_dir = Path(log_dir)
        self.writer = None

    def on_train_begin(self, logs=None):
        import datetime

        log_path = self.log_dir / datetime.datetime.now().strftime("%Y%m%d-%H%M%S")
        self.writer = tf.summary.create_file_writer(str(log_path))
        logger.info(f"📊 TensorBoard logs: {log_path}")

    def on_epoch_end(self, epoch, logs=None):
        if self.writer is None:
            return

        with self.writer.as_default():
            for key, value in logs.items():
                tf.summary.scalar(key, value, step=epoch)
            self.writer.flush()
