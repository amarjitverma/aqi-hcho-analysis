# ============================================================
# Transformer Model
# ============================================================

"""Transformer model for time-series PM2.5 prediction."""

import tensorflow as tf
from tensorflow.keras import layers, models
from src.models.base_model import BaseModel


class TransformerModel(BaseModel):
    """Transformer model for time-series PM2.5 prediction."""

    def __init__(self, d_model=128, n_heads=8, n_layers=4, learning_rate=0.001):
        self.d_model = d_model
        self.n_heads = n_heads
        self.n_layers = n_layers
        self.learning_rate = learning_rate
        self.model = None

    def build(self, input_shape):
        """Build Transformer model."""
        from tensorflow.keras import layers, models

        inputs = layers.Input(shape=input_shape)

        # Positional encoding (simplified)
        x = layers.Dense(self.d_model)(inputs)

        # Transformer blocks (simplified)
        for _ in range(self.n_layers):
            # Multi-head attention
            attn = layers.MultiHeadAttention(
                num_heads=self.n_heads, key_dim=self.d_model // self.n_heads
            )(x, x)
            x = layers.Add()([x, attn])
            x = layers.LayerNormalization()(x)

            # Feed forward
            ff = layers.Dense(self.d_model * 2, activation="relu")(x)
            ff = layers.Dense(self.d_model)(ff)
            x = layers.Add()([x, ff])
            x = layers.LayerNormalization()(x)

        # Global pooling and output
        x = layers.GlobalAveragePooling1D()(x)
        x = layers.Dense(64, activation="relu")(x)
        x = layers.Dropout(0.2)(x)
        outputs = layers.Dense(1)(x)

        self.model = models.Model(inputs, outputs)
        return self.model

    def compile(self, **kwargs):
        optimizer = tf.keras.optimizers.Adam(learning_rate=self.learning_rate)
        self.model.compile(optimizer=optimizer, loss="mse", metrics=["mae"])

    def train(self, X_train, y_train, X_val, y_val, epochs=100, batch_size=32, **kwargs):
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
