# ============================================================
# CNN-LSTM Model
# ============================================================

"""Hybrid CNN-LSTM model for spatiotemporal PM2.5 prediction."""

import tensorflow as tf
from src.models.base_model import BaseModel


class CNNLSTMModel(BaseModel):
    """CNN-LSTM model for spatiotemporal PM2.5 prediction."""

    def __init__(self, conv_filters=64, lstm_units=128, learning_rate=0.001):
        self.conv_filters = conv_filters
        self.lstm_units = lstm_units
        self.learning_rate = learning_rate
        self.model = None

    def build(self, input_shape):
        """Build CNN-LSTM model."""
        from tensorflow.keras import layers, models

        model = models.Sequential()

        # CNN Part
        model.add(
            layers.TimeDistributed(
                layers.Conv2D(self.conv_filters, (3, 3), activation="relu", padding="same"),
                input_shape=input_shape,
            )
        )
        model.add(layers.TimeDistributed(layers.MaxPooling2D((2, 2))))
        model.add(
            layers.TimeDistributed(
                layers.Conv2D(self.conv_filters * 2, (3, 3), activation="relu", padding="same")
            )
        )
        model.add(layers.TimeDistributed(layers.MaxPooling2D((2, 2))))
        model.add(layers.TimeDistributed(layers.Flatten()))

        # LSTM Part
        model.add(layers.LSTM(self.lstm_units, return_sequences=True))
        model.add(layers.Dropout(0.3))
        model.add(layers.LSTM(self.lstm_units // 2))
        model.add(layers.Dropout(0.3))

        # Output
        model.add(layers.Dense(64, activation="relu"))
        model.add(layers.Dropout(0.2))
        model.add(layers.Dense(1))

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
