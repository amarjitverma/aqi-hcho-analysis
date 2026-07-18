# ============================================================
# LSTM Model
# ============================================================

"""LSTM model for time-series PM2.5 prediction."""

import tensorflow as tf
from tensorflow.keras import layers, models
from src.models.base_model import BaseModel


class LSTMModel(BaseModel):
    """LSTM model for time-series PM2.5 prediction."""

    def __init__(
        self,
        lstm_units: int = 128,
        dropout_rate: float = 0.3,
        learning_rate: float = 0.001,
    ):
        self.lstm_units = lstm_units
        self.dropout_rate = dropout_rate
        self.learning_rate = learning_rate
        self.model = None

    def build(self, input_shape: tuple) -> tf.keras.Model:
        """Build LSTM model."""
        model = models.Sequential(
            [
                layers.LSTM(self.lstm_units, return_sequences=True, input_shape=input_shape),
                layers.Dropout(self.dropout_rate),
                layers.LSTM(self.lstm_units // 2),
                layers.Dropout(self.dropout_rate),
                layers.Dense(64, activation="relu"),
                layers.Dropout(0.2),
                layers.Dense(1, name="pm25_output"),
            ]
        )

        self.model = model
        return model

    def compile(self, **kwargs):
        """Compile the model."""
        optimizer = tf.keras.optimizers.Adam(learning_rate=self.learning_rate)
        self.model.compile(
            optimizer=optimizer,
            loss="mse",
            metrics=["mae"],
        )

    def train(self, X_train, y_train, X_val, y_val, epochs=100, batch_size=32, **kwargs):
        """Train the model."""
        callbacks = [
            tf.keras.callbacks.EarlyStopping(
                monitor="val_loss", patience=10, restore_best_weights=True
            ),
            tf.keras.callbacks.ReduceLROnPlateau(
                monitor="val_loss", factor=0.5, patience=5, min_lr=1e-6
            ),
        ]

        history = self.model.fit(
            X_train,
            y_train,
            validation_data=(X_val, y_val),
            epochs=epochs,
            batch_size=batch_size,
            callbacks=callbacks,
            verbose=1,
        )

        return history

    def predict(self, X):
        """Make predictions."""
        return self.model.predict(X).flatten()

    def evaluate(self, X, y):
        """Evaluate the model."""
        loss, mae = self.model.evaluate(X, y, verbose=0)
        return {"loss": loss, "mae": mae}
