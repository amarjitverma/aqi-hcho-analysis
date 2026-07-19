# ============================================================
# ConvLSTM Model
# ============================================================

"""ConvLSTM model for spatiotemporal PM2.5 prediction."""

import tensorflow as tf
from src.models.base_model import BaseModel


class ConvLSTMModel(BaseModel):
    """ConvLSTM model for spatiotemporal PM2.5 prediction."""

    def __init__(self, filters=64, lstm_units=128, kernel_size=3, learning_rate=0.001):
        self.filters = filters
        self.lstm_units = lstm_units
        self.kernel_size = kernel_size
        self.learning_rate = learning_rate
        self.model = None

    def build(self, input_shape):
        """Build ConvLSTM model."""
        from tensorflow.keras import layers, models

        model = models.Sequential(
            [
                layers.ConvLSTM2D(
                    self.filters,
                    kernel_size=self.kernel_size,
                    padding="same",
                    return_sequences=True,
                    input_shape=input_shape,
                ),
                layers.BatchNormalization(),
                layers.ConvLSTM2D(
                    self.filters // 2,
                    kernel_size=self.kernel_size,
                    padding="same",
                    return_sequences=True,
                ),
                layers.BatchNormalization(),
                layers.ConvLSTM2D(
                    self.filters // 4,
                    kernel_size=self.kernel_size,
                    padding="same",
                    return_sequences=False,
                ),
                layers.BatchNormalization(),
                layers.Flatten(),
                layers.Dense(64, activation="relu"),
                layers.Dropout(0.2),
                layers.Dense(1),
            ]
        )

        self.model = model
        return model

    def compile(self, **kwargs):
        optimizer = tf.keras.optimizers.Adam(learning_rate=self.learning_rate)
        self.model.compile(optimizer=optimizer, loss="mse", metrics=["mae"])

    def train(self, X_train, y_train, X_val, y_val, epochs=100, batch_size=16, **kwargs):
        callbacks = [
            tf.keras.callbacks.EarlyStopping(
                monitor="val_loss", patience=10, restore_best_weights=True
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
        return self.model.predict(X).flatten()

    def evaluate(self, X, y):
        loss, mae = self.model.evaluate(X, y, verbose=0)
        return {"loss": loss, "mae": mae}
