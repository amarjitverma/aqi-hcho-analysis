# ============================================================
# Objective Function for Optuna
# ============================================================

"""Objective functions for hyperparameter optimization."""

import optuna
import numpy as np

from src.models.lstm.lstm import LSTMModel
from src.models.cnn_lstm.cnn_lstm import CNNLSTMModel
from src.models.convlstm.convlstm import ConvLSTMModel
from src.models.transformer.transformer import TransformerModel
from src.training.trainer import Trainer
from src.evaluation.metrics import calculate_all_metrics


def objective(trial: optuna.Trial) -> float:
    """
    Objective function for Optuna optimization.

    Args:
        trial (optuna.Trial): Optuna trial

    Returns:
        float: RMSE value to minimize
    """
    # This is a factory function that returns an objective for a specific model
    # The actual implementation is in optuna_search.py
    raise NotImplementedError("Use run_optuna_search() instead")


def create_objective(
    model_name: str,
    X_train: np.ndarray,
    y_train: np.ndarray,
    X_val: np.ndarray,
    y_val: np.ndarray,
    epochs: int = 30,
):
    """
    Create an objective function for a specific model.

    Args:
        model_name (str): Name of the model
        X_train (np.ndarray): Training features
        y_train (np.ndarray): Training targets
        X_val (np.ndarray): Validation features
        y_val (np.ndarray): Validation targets
        epochs (int): Number of epochs for each trial

    Returns:
        callable: Objective function
    """

    def objective(trial: optuna.Trial) -> float:
        # Get hyperparameters based on model
        if model_name == "lstm":
            params = {
                "lstm_units": trial.suggest_int("lstm_units", 32, 256, step=32),
                "dropout_rate": trial.suggest_float("dropout_rate", 0.1, 0.5, step=0.1),
                "learning_rate": trial.suggest_float("learning_rate", 1e-4, 1e-2, log=True),
                "batch_size": trial.suggest_categorical("batch_size", [16, 32, 64]),
            }
        elif model_name == "cnn_lstm":
            params = {
                "conv_filters": trial.suggest_int("conv_filters", 32, 128, step=32),
                "lstm_units": trial.suggest_int("lstm_units", 32, 256, step=32),
                "learning_rate": trial.suggest_float("learning_rate", 1e-4, 1e-2, log=True),
                "batch_size": trial.suggest_categorical("batch_size", [8, 16, 32]),
            }
        elif model_name == "convlstm":
            params = {
                "filters": trial.suggest_int("filters", 32, 128, step=32),
                "kernel_size": trial.suggest_int("kernel_size", 2, 5),
                "lstm_units": trial.suggest_int("lstm_units", 32, 256, step=32),
                "learning_rate": trial.suggest_float("learning_rate", 1e-4, 1e-2, log=True),
                "batch_size": trial.suggest_categorical("batch_size", [8, 16, 32]),
            }
        elif model_name == "transformer":
            params = {
                "d_model": trial.suggest_int("d_model", 64, 256, step=32),
                "n_heads": trial.suggest_int("n_heads", 4, 16, step=2),
                "n_layers": trial.suggest_int("n_layers", 2, 8),
                "learning_rate": trial.suggest_float("learning_rate", 1e-4, 1e-2, log=True),
                "batch_size": trial.suggest_categorical("batch_size", [16, 32, 64]),
            }
        else:
            raise ValueError(f"Unknown model: {model_name}")

        # Build model
        if model_name == "lstm":
            model = LSTMModel(**params)
        elif model_name == "cnn_lstm":
            model = CNNLSTMModel(**params)
        elif model_name == "convlstm":
            model = ConvLSTMModel(**params)
        elif model_name == "transformer":
            model = TransformerModel(**params)
        else:
            raise ValueError(f"Unknown model: {model_name}")

        input_shape = (X_train.shape[1],)
        model.build(input_shape)
        model.compile()

        # Train
        trainer = Trainer(model=model.model, config={})
        trainer.train(
            X_train,
            y_train,
            X_val,
            y_val,
            epochs=epochs,
            batch_size=params.get("batch_size", 32),
            verbose=0,
        )

        # Evaluate
        y_pred = model.predict(X_val)
        metrics = calculate_all_metrics(y_val, y_pred)

        return metrics["rmse"]

    return objective
