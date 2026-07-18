# ============================================================
# Pipelines Module
# ============================================================

"""End-to-end pipelines for training, inference, and evaluation."""

from src.pipelines.train_pipeline import TrainPipeline
from src.pipelines.inference_pipeline import InferencePipeline
from src.pipelines.evaluation_pipeline import EvaluationPipeline

__all__ = [
    "TrainPipeline",
    "InferencePipeline",
    "EvaluationPipeline",
]
