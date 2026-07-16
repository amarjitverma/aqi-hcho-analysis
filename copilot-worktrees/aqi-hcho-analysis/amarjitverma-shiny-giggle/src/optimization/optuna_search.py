# ============================================================
# Optuna Hyperparameter Search
# ============================================================

"""Hyperparameter optimization using Optuna."""

import optuna
import numpy as np
import tensorflow as tf
from loguru import logger
from typing import Dict, Any, Optional

from src.models.lstm.lstm import LSTMModel
from src.models.cnn_lstm.cnn_lstm import CNNLSTMModel
from src.models.convlstm.convlstm import ConvLSTMModel
from src.models.transformer.transformer import TransformerModel
from src.training.trainer import Trainer
from src.evaluation.metrics import calculate_all_metrics


def run_optuna_search(
    model_name: str,
    X_train: np.ndarray,
    y_train: np.ndarray,
    X_val: np.ndarray,
    y_val: np.ndarray,
    n_trials: int = 50,
    study_name: str = "aqi_hcho_optimization",
    storage: Optional[str] = None,
) -> Dict[str, Any]:
    """
    Run Optuna hyperparameter search.

    Args:
        model_name (str): Name of the model
        X_train (np.ndarray): Training features
        y_train (np.ndarray): Training targets
        X_val (np.ndarray): Validation features
        y_val (np.ndarray): Validation targets
        n_trials (int): Number of trials
        study_name (str): Name of the study
        storage (str): Storage URL for study persistence

    Returns:
        dict: Best parameters and results
    """
    logger.info(f"🔍 Running Optuna search for {model_name} ({n_trials} trials)")

    # Create objective function
    def objective(trial: optuna.Trial) -> float:
        params = _get_hyperparameters(trial, model_name)

        # Build model
        model = _build_model(model_name, params)
        input_shape = (X_train.shape[1],)
        model.build(input_shape)
        model.compile()

        # Train
        trainer = Trainer(model=model.model, config={})
        trainer.train(
            X_train, y_train,
            X_val, y_val,
            epochs=30,
            batch_size=params.get("batch_size", 32),
            verbose=0,
        )

        # Evaluate
        y_pred = model.predict(X_val)
        metrics = calculate_all_metrics(y_val, y_pred)

        return metrics["rmse"]

    # Create study
    if storage:
        study = optuna.create_study(
            study_name=study_name,
            storage=storage,
            direction="minimize",
            load_if_exists=True,
        )
    else:
        study = optuna.create_study(direction="minimize")

    # Run optimization
    study.optimize(objective, n_trials=n_trials, show_progress_bar=True)

    # Log results
    logger.info(f"✅ Best RMSE: {study.best_value:.4f}")
    logger.info(f"✅ Best parameters: {study.best_params}")

    return {
        "best_params": study.best_params,
        "best_value": study.best_value,
        "study": study,
    }


def _get_hyperparameters(trial: optuna.Trial, model_name: str) -> Dict[str, Any]:
    """Get hyperparameters for a given model."""
    if model_name == "lstm":
        return {
            "lstm_units": trial.suggest_int("lstm_units", 32, 256, step=32),
            "dropout_rate": trial.suggest_float("dropout_rate", 0.1, 0.5, step=0.1),
            "learning_rate": trial.suggest_float("learning_rate", 1e-4, 1e-2, log=True),
            "batch_size": trial.suggest_categorical("batch_size", [16, 32, 64]),
        }
    elif model_name == "cnn_lstm":
        return {
            "conv_filters": trial.suggest_int("conv_filters", 32, 128, step=32),
            "lstm_units": trial.suggest_int("lstm_units", 32, 256, step=32),
            "learning_rate": trial.suggest_float("learning_rate", 1e-4, 1e-2, log=True),
            "batch_size": trial.suggest_categorical("batch_size", [8, 16, 32]),
        }
    elif model_name == "convlstm":
        return {
            "filters": trial.suggest_int("filters", 32, 128, step=32),
            "kernel_size": trial.suggest_int("kernel_size", 2, 5),
            "lstm_units": trial.suggest_int("lstm_units", 32, 256, step=32),
            "learning_rate": trial.suggest_float("learning_rate", 1e-4, 1e-2, log=True),
            "batch_size": trial.suggest_categorical("batch_size", [8, 16, 32]),
        }
    elif model_name == "transformer":
        return {
            "d_model": trial.suggest_int("d_model", 64, 256, step=32),
            "n_heads": trial.suggest_int("n_heads", 4, 16, step=2),
            "n_layers": trial.suggest_int("n_layers", 2, 8),
            "learning_rate": trial.suggest_float("learning_rate", 1e-4, 1e-2, log=True),
            "batch_size": trial.suggest_categorical("batch_size", [16, 32, 64]),
        }
    else:
        raise ValueError(f"Unknown model: {model_name}")


def _build_model(model_name: str, params: Dict[str, Any]):
    """Build model with given parameters."""
    if model_name == "lstm":
        return LSTMModel(
            lstm_units=params.get("lstm_units", 128),
            dropout_rate=params.get("dropout_rate", 0.3),
            learning_rate=params.get("learning_rate", 0.001),
        )
    elif model_name == "cnn_lstm":
        return CNNLSTMModel(
            conv_filters=params.get("conv_filters", 64),
            lstm_units=params.get("lstm_units", 128),
            learning_rate=params.get("learning_rate", 0.001),
        )
    elif model_name == "convlstm":
        return ConvLSTMModel(
            filters=params.get("filters", 64),
            kernel_size=params.get("kernel_size", 3),
            lstm_units=params.get("lstm_units", 128),
            learning_rate=params.get("learning_rate", 0.001),
        )
    elif model_name == "transformer":
        return TransformerModel(
            d_model=params.get("d_model", 128),
            n_heads=params.get("n_heads", 8),
            n_layers=params.get("n_layers", 4),
            learning_rate=params.get("learning_rate", 0.001),
        )
    else:
        raise ValueError(f"Unknown model: {model_name}")