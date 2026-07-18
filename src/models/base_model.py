# ============================================================
# Base Model
# ============================================================

"""Abstract base model class."""

from abc import ABC, abstractmethod
import tensorflow as tf


class BaseModel(ABC):
    """Base class for all models."""

    @abstractmethod
    def build(self, input_shape: tuple) -> tf.keras.Model:
        """Build and return the model architecture."""
        pass

    @abstractmethod
    def compile(self, **kwargs):
        """Compile the model."""
        pass

    @abstractmethod
    def train(self, X_train, y_train, X_val, y_val, **kwargs):
        """Train the model."""
        pass

    @abstractmethod
    def predict(self, X):
        """Make predictions."""
        pass

    @abstractmethod
    def evaluate(self, X, y):
        """Evaluate the model."""
        pass

    def save(self, filepath: str):
        """Save the model."""
        if self.model:
            self.model.save(filepath)

    def load(self, filepath: str):
        """Load the model."""
        self.model = tf.keras.models.load_model(filepath)
