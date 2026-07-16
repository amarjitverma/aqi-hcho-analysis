# ============================================================
# Learning Rate Schedulers
# ============================================================

"""Learning rate schedulers for model training."""

import math
import tensorflow as tf


class CosineAnnealingScheduler(tf.keras.optimizers.schedules.LearningRateSchedule):
    """
    Cosine annealing learning rate scheduler.

    Decays learning rate following a cosine curve.
    """

    def __init__(
        self,
        initial_lr: float = 0.001,
        final_lr: float = 1e-7,
        epochs: int = 100,
        warmup_epochs: int = 5,
        warmup_lr: float = 1e-5,
    ):
        super().__init__()
        self.initial_lr = initial_lr
        self.final_lr = final_lr
        self.epochs = epochs
        self.warmup_epochs = warmup_epochs
        self.warmup_lr = warmup_lr

    def __call__(self, step):
        # Convert step to epoch (assuming 1 epoch = 1 step for simplicity)
        epoch = tf.cast(step, tf.float32)

        if epoch < self.warmup_epochs:
            # Linear warmup
            progress = epoch / self.warmup_epochs
            return self.warmup_lr + (self.initial_lr - self.warmup_lr) * progress

        # Cosine decay
        progress = (epoch - self.warmup_epochs) / (self.epochs - self.warmup_epochs)
        progress = tf.minimum(progress, 1.0)
        cosine_decay = 0.5 * (1 + tf.cos(math.pi * progress))

        return self.final_lr + (self.initial_lr - self.final_lr) * cosine_decay


class StepLR(tf.keras.optimizers.schedules.LearningRateSchedule):
    """
    Step learning rate scheduler.

    Decays learning rate by factor at specified step boundaries.
    """

    def __init__(
        self,
        initial_lr: float = 0.001,
        step_size: int = 30,
        gamma: float = 0.1,
    ):
        super().__init__()
        self.initial_lr = initial_lr
        self.step_size = step_size
        self.gamma = gamma

    def __call__(self, step):
        return self.initial_lr * (self.gamma ** (step // self.step_size))


class ReduceLROnPlateauScheduler:
    """
    Reduce learning rate when a metric has stopped improving.

    Wrapper for tf.keras.callbacks.ReduceLROnPlateau.
    """

    def __init__(
        self,
        monitor: str = "val_loss",
        factor: float = 0.5,
        patience: int = 5,
        min_lr: float = 1e-7,
    ):
        self.callback = tf.keras.callbacks.ReduceLROnPlateau(
            monitor=monitor,
            factor=factor,
            patience=patience,
            min_lr=min_lr,
            verbose=1,
        )

    def get_callback(self):
        """Get the callback instance."""
        return self.callback


def get_scheduler(name: str, **kwargs):
    """Get learning rate scheduler by name."""
    schedulers = {
        "cosine": CosineAnnealingScheduler,
        "step": StepLR,
        "plateau": ReduceLROnPlateauScheduler,
    }

    if name not in schedulers:
        raise ValueError(f"Unknown scheduler: {name}")

    return schedulers[name](**kwargs)


if __name__ == "__main__":
    # Test CosineAnnealingScheduler
    scheduler = CosineAnnealingScheduler(initial_lr=0.001, epochs=100)
    for step in range(0, 101, 10):
        lr = scheduler(step)
        print(f"Step {step}: LR = {lr:.6f}")