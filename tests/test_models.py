# ============================================================
# Model Tests
# ============================================================

"""Tests for model architectures."""

import pytest
import numpy as np
import tensorflow as tf
import sys
import os

# Add project root to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.models.lstm.lstm import LSTMModel
from src.models.cnn_lstm.cnn_lstm import CNNLSTMModel
from src.models.convlstm.convlstm import ConvLSTMModel
from src.models.transformer.transformer import TransformerModel


class TestLSTMModel:
    """Tests for LSTM model."""
    
    def test_build(self):
        """Test model building."""
        model = LSTMModel()
        input_shape = (7, 10)  # sequence_length, n_features
        model.build(input_shape)
        assert model.model is not None
        assert len(model.model.layers) > 0
    
    def test_compile(self):
        """Test model compilation."""
        model = LSTMModel()
        input_shape = (7, 10)
        model.build(input_shape)
        model.compile()
        assert model.model.optimizer is not None
    
    def test_predict_shape(self):
        """Test prediction shape."""
        model = LSTMModel()
        input_shape = (7, 10)
        model.build(input_shape)
        model.compile()
        
        X_test = np.random.randn(10, 7, 10)
        pred = model.predict(X_test)
        assert pred.shape == (10,)


class TestCNNLSTMModel:
    """Tests for CNN-LSTM model."""
    
    def test_build(self):
        """Test model building."""
        model = CNNLSTMModel()
        input_shape = (7, 32, 32, 6)  # seq_length, height, width, channels
        model.build(input_shape)
        assert model.model is not None
    
    def test_predict_shape(self):
        """Test prediction shape."""
        model = CNNLSTMModel()
        input_shape = (7, 32, 32, 6)
        model.build(input_shape)
        model.compile()
        
        X_test = np.random.randn(10, 7, 32, 32, 6)
        pred = model.predict(X_test)
        assert pred.shape == (10,)


class TestConvLSTMModel:
    """Tests for ConvLSTM model."""
    
    def test_build(self):
        """Test model building."""
        model = ConvLSTMModel()
        input_shape = (7, 32, 32, 6)
        model.build(input_shape)
        assert model.model is not None
    
    def test_predict_shape(self):
        """Test prediction shape."""
        model = ConvLSTMModel()
        input_shape = (7, 32, 32, 6)
        model.build(input_shape)
        model.compile()
        
        X_test = np.random.randn(10, 7, 32, 32, 6)
        pred = model.predict(X_test)
        assert pred.shape == (10,)


class TestTransformerModel:
    """Tests for Transformer model."""
    
    def test_build(self):
        """Test model building."""
        model = TransformerModel()
        input_shape = (7, 10)
        model.build(input_shape)
        assert model.model is not None
    
    def test_predict_shape(self):
        """Test prediction shape."""
        model = TransformerModel()
        input_shape = (7, 10)
        model.build(input_shape)
        model.compile()
        
        X_test = np.random.randn(10, 7, 10)
        pred = model.predict(X_test)
        assert pred.shape == (10,)


class TestModelBase:
    """Tests for model base class."""
    
    def test_save_load(self, tmp_path):
        """Test model save and load."""
        model = LSTMModel()
        input_shape = (7, 10)
        model.build(input_shape)
        model.compile()
        
        # Save
        save_path = str(tmp_path / "test_model.h5")
        model.save(save_path)
        
        # Load
        new_model = LSTMModel()
        new_model.load(save_path)
        assert new_model.model is not None