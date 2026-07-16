# ============================================================
# Training Pipeline
# ============================================================

"""End-to-end training pipeline."""

import pandas as pd
import numpy as np
from pathlib import Path
from loguru import logger
from typing import Dict, Any, Optional

from src.models.lstm.lstm import LSTMModel
from src.models.cnn_lstm.cnn_lstm import CNNLSTMModel
from src.models.convlstm.convlstm import ConvLSTMModel
from src.models.transformer.transformer import TransformerModel
from src.models.ensemble.ensemble import EnsembleModel
from src.training.trainer import Trainer
from src.evaluation.evaluator import Evaluator
from src.evaluation.visualizer import plot_learning_curves


class TrainPipeline:
    """
    Training pipeline orchestrator.

    Handles loading data, training models, and saving results.
    """

    def __init__(
        self,
        config: Dict[str, Any],
        data_dir: str = "data/processed/",
        output_dir: str = "outputs/",
    ):
        """
        Initialize training pipeline.

        Args:
            config (dict): Configuration dictionary
            data_dir (str): Data directory
            output_dir (str): Output directory
        """
        self.config = config
        self.data_dir = Path(data_dir)
        self.output_dir = Path(output_dir)
        self.evaluator = Evaluator(str(output_dir / "metrics"))

        # Create output directories
        (output_dir / "models").mkdir(parents=True, exist_ok=True)
        (output_dir / "figures").mkdir(parents=True, exist_ok=True)

    def load_data(self) -> Dict[str, np.ndarray]:
        """
        Load training data.

        Returns:
            dict: Dictionary with train/val/test data
        """
        logger.info("📂 Loading data...")

        train_df = pd.read_parquet(self.data_dir / "train.parquet")
        val_df = pd.read_parquet(self.data_dir / "validation.parquet")
        test_df = pd.read_parquet(self.data_dir / "test.parquet")

        # This is a placeholder - actual feature extraction depends on data format
        # In practice, you would extract features and targets here

        return {
            "X_train": train_df.drop("pm25", axis=1).values,
            "y_train": train_df["pm25"].values,
            "X_val": val_df.drop("pm25", axis=1).values,
            "y_val": val_df["pm25"].values,
            "X_test": test_df.drop("pm25", axis=1).values,
            "y_test": test_df["pm25"].values,
        }

    def build_model(self, model_name: str, **kwargs) -> Any:
        """
        Build model by name.

        Args:
            model_name (str): Name of the model
            **kwargs: Model parameters

        Returns:
            Any: Model instance
        """
        logger.info(f"🏗️ Building {model_name} model...")

        models = {
            "lstm": LSTMModel,
            "cnn_lstm": CNNLSTMModel,
            "convlstm": ConvLSTMModel,
            "transformer": TransformerModel,
        }

        if model_name not in models:
            raise ValueError(f"Unknown model: {model_name}")

        model_class = models[model_name]

        # Get model parameters from config
        model_config = self.config.get("model", {}).get(model_name, {})

        # Merge with kwargs
        params = {**model_config, **kwargs}

        return model_class(**params)

    def run(
        self,
        model_name: str = "lstm",
        epochs: int = 100,
        batch_size: int = 32,
        **kwargs,
    ) -> Dict[str, Any]:
        """
        Run training pipeline.

        Args:
            model_name (str): Name of the model to train
            epochs (int): Number of epochs
            batch_size (int): Batch size
            **kwargs: Additional model parameters

        Returns:
            dict: Training results
        """
        logger.info("🚀 Starting training pipeline...")

        # Load data
        data = self.load_data()

        # Build model
        model = self.build_model(model_name, **kwargs)

        # Get input shape
        input_shape = (data["X_train"].shape[1],)
        model.build(input_shape)
        model.compile()

        # Train
        trainer = Trainer(
            model=model.model,
            config=self.config,
            output_dir=str(self.output_dir / "models" / model_name),
        )

        history = trainer.train(
            data["X_train"],
            data["y_train"],
            data["X_val"],
            data["y_val"],
            epochs=epochs,
            batch_size=batch_size,
        )

        # Evaluate
        y_pred = model.predict(data["X_test"])
        metrics = self.evaluator.evaluate(data["y_test"], y_pred, model_name)

        # Save learning curves
        plot_learning_curves(
            history["history"],
            save_path=str(self.output_dir / "figures" / f"{model_name}_learning_curves.png"),
        )

        results = {
            "model_name": model_name,
            "metrics": metrics,
            "history": history,
            "predictions": y_pred,
        }

        logger.info("✅ Training pipeline complete!")
        return results