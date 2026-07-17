# ============================================================
# Dashboard Page: Model Performance
# ============================================================

"""Model performance page for the dashboard."""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import json
import numpy as np
from pathlib import Path
import logging

logger = logging.getLogger(__name__)


def render():
    """Render the Model Performance page."""
    import sys
    from pathlib import Path
    dashboard_path = Path(__file__).parent.parent
    if str(dashboard_path) not in sys.path:
        sys.path.insert(0, str(dashboard_path))

    from components.header import render_header
    from components.navigation import render_navigation
    render_header()
    render_navigation('model_performance')
    
    st.header("📊 Model Performance Analysis")
    st.caption("Evaluate the accuracy and reliability of our predictions")
    
    # Load metrics
    metrics = {}
    metrics_path = Path('outputs/metrics')
    try:
        with open(metrics_path / 'rf_metrics.json', 'r') as f:
            metrics['Random Forest'] = json.load(f)
    except Exception as e:
        logger.debug(f'RF metrics not found: {e}')
    try:
        with open(metrics_path / 'lstm_metrics.json', 'r') as f:
            metrics['LSTM'] = json.load(f)
    except Exception as e:
        logger.debug(f'LSTM metrics not found: {e}')
    try:
        with open(metrics_path / 'cnn_lstm_metrics.json', 'r') as f:
            metrics['CNN-LSTM'] = json.load(f)
    except Exception as e:
        logger.debug(f'CNN-LSTM metrics not found: {e}')
    
    if not metrics:
        st.warning("No model metrics found. Run the training pipeline first.")
        return
    
    # Display metrics
    st.subheader("Model Comparison")
    
    # Create comparison table
    df = pd.DataFrame(metrics).T
    df = df.round(3)
    
    st.dataframe(df.style.apply(lambda x: ['background-color: #1B5E20; color: white' if v == x.min() else '' for v in x]))
    
    # Performance gauges
    st.subheader("Performance Gauges")
    
    # Get best model
    if 'LSTM' in metrics:
        best_model = metrics['LSTM']
    elif 'CNN-LSTM' in metrics:
        best_model = metrics['CNN-LSTM']
    else:
        best_model = metrics['Random Forest']
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("RMSE", f"{best_model.get('rmse', 0):.2f} µg/m³")
    with col2:
        st.metric("MAE", f"{best_model.get('mae', 0):.2f} µg/m³")
    with col3:
        st.metric("R²", f"{best_model.get('r2', 0):.3f}")
    with col4:
        st.metric("MAPE", f"{best_model.get('mape', 0):.1f}%")


if __name__ == "__main__":
    render()
