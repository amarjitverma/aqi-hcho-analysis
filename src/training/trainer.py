# ============================================================
# Base Trainer
# ============================================================

"""Base trainer class for deep learning models."""

import os
import time
import numpy as np
import tensorflow as tf
from loguru import logger
from typing import Dict, Any, Optional, List, Callable
from pathlib import Path


class Trainer:
    """
    Base trainer class for deep learning models.

    Handles training loop, validation, checkpointing, and logging.
    """

    def __init__(
        self,
        model: tf.keras.Model,
        config: Dict[str, Any],
        output_dir: str = "models/checkpoints/",
        callbacks: List[tf.keras.callbacks.Callback] = None,
    ):
        """
        Initialize the trainer.

        Args:
            model (tf.keras.Model): Model to train
            config (dict): Training configuration
            output_dir (str): Directory for checkpoints
            callbacks (list): List of callbacks
        """
        self.model = model
        self.config = config
        self.output_dir = Path(output_dir)
        self.callbacks = callbacks or []
        self.history = None
        self.best_epoch = 0
        self.best_metrics = {}

        # Create output directory
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def train(
        self,
        X_train: np.ndarray,
        y_train: np.ndarray,
        X_val: np.ndarray,
        y_val: np.ndarray,
        epochs: int = 100,
        batch_size: int = 32,
        validation_freq: int = 1,
        verbose: int = 1,
    ) -> Dict[str, Any]:
        """
        Train the model.

        Args:
            X_train (np.ndarray): Training features
            y_train (np.ndarray): Training targets
            X_val (np.ndarray): Validation features
            y_val (np.ndarray): Validation targets
            epochs (int): Number of epochs
            batch_size (int): Batch size
            validation_freq (int): Validation frequency
            verbose (int): Verbosity level

        Returns:
            dict: Training history
        """
        logger.info(f"🚀 Starting training for {epochs} epochs")
        logger.info(f"  Training samples: {len(X_train)}")
        logger.info(f"  Validation samples: {len(X_val)}")
        logger.info(f"  Batch size: {batch_size}")
        logger.info(f"  Output directory: {self.output_dir}")

        # Prepare callbacks
        callbacks = self._get_callbacks()

        # Train
        start_time = time.time()

        history = self.model.fit(
            X_train,
            y_train,
            validation_data=(X_val, y_val),
            epochs=epochs,
            batch_size=batch_size,
            callbacks=callbacks,
            verbose=verbose,
            validation_freq=validation_freq,
        )

        self.history = history
        elapsed_time = time.time() - start_time
        logger.info(f"✅ Training completed in {elapsed_time:.2f} seconds")

        # Get best metrics
        self._extract_best_metrics(history)

        return {"history": history.history, "best_metrics": self.best_metrics}

    def _get_callbacks(self) -> List[tf.keras.callbacks.Callback]:
        """Get callbacks with default values if not provided."""
        callbacks = []

        # Checkpoint callback
        checkpoint_path = self.output_dir / "best_model.h5"
        callbacks.append(
            tf.keras.callbacks.ModelCheckpoint(
                filepath=str(checkpoint_path),
                monitor="val_loss",
                save_best_only=True,
                verbose=1,
            )
        )

        # Early stopping
        callbacks.append(
            tf.keras.callbacks.EarlyStopping(
                monitor="val_loss", patience=10, restore_best_weights=True, verbose=1
            )
        )

        # Reduce LR on plateau
        callbacks.append(
            tf.keras.callbacks.ReduceLROnPlateau(
                monitor="val_loss",
                factor=0.5,
                patience=5,
                min_lr=1e-7,
                verbose=1,
            )
        )

        # Add user-provided callbacks
        if self.callbacks:
            callbacks.extend(self.callbacks)

        return callbacks

    def _extract_best_metrics(self, history) -> None:
        """Extract best metrics from training history."""
        best_val_loss = min(history.history.get("val_loss", [float("inf")]))
        best_epoch = history.history.get("val_loss", []).index(best_val_loss) + 1

        self.best_epoch = best_epoch
        self.best_metrics = {
            "best_epoch": best_epoch,
            "best_val_loss": best_val_loss,
            "best_val_mae": min(history.history.get("val_mae", [0])),
            "best_train_loss": min(history.history.get("loss", [0])),
        }

        logger.info(f"  Best epoch: {best_epoch}")
        logger.info(f"  Best val loss: {best_val_loss:.4f}")

    def save_checkpoint(self, name: str = "latest") -> None:
        """Save model checkpoint."""
        path = self.output_dir / f"{name}.h5"
        self.model.save(path)
        logger.info(f"💾 Checkpoint saved to {path}")

    def load_checkpoint(self, name: str = "best_model") -> None:
        """Load model checkpoint."""
        path = self.output_dir / f"{name}.h5"
        if path.exists():
            self.model = tf.keras.models.load_model(path)
            logger.info(f"📥 Checkpoint loaded from {path}")
        else:
            logger.warning(f"Checkpoint not found: {path}")

    def plot_training_history(self, save_path: Optional[str] = None) -> None:
        """Plot training history."""
        import matplotlib.pyplot as plt

        if self.history is None:
            logger.warning("No training history available")
            return

        fig, axes = plt.subplots(1, 2, figsize=(12, 4))

        # Loss
        axes[0].plot(self.history.history.get("loss", []), label="Train Loss")
        axes[0].plot(self.history.history.get("val_loss", []), label="Val Loss")
        axes[0].set_xlabel("Epoch")
        axes[0].set_ylabel("Loss")
        axes[0].set_title("Loss")
        axes[0].legend()
        axes[0].grid(True, alpha=0.3)

        # MAE
        axes[1].plot(self.history.history.get("mae", []), label="Train MAE")
        axes[1].plot(self.history.history.get("val_mae", []), label="Val MAE")
        axes[1].set_xlabel("Epoch")
        axes[1].set_ylabel("MAE")
        axes[1].set_title("Mean Absolute Error")
        axes[1].legend()
        axes[1].grid(True, alpha=0.3)

        plt.tight_layout()

        if save_path:
            plt.savefig(save_path, dpi=150)
            logger.info(f"📊 Training plot saved to {save_path}")

        plt.close()