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


def render():
    """Render the Model Performance page."""
    st.header("📊 Model Performance Analysis")
    st.caption("Evaluate the accuracy and reliability of our predictions")
    
    # Load metrics
    metrics = {}
    try:
        with open('outputs/metrics/rf_metrics.json', 'r') as f:
            metrics['Random Forest'] = json.load(f)
    except:
        pass
    
    try:
        with open('outputs/metrics/lstm_metrics.json', 'r') as f:
            metrics['LSTM'] = json.load(f)
    except:
        pass
    
    try:
        with open('outputs/metrics/cnn_lstm_metrics.json', 'r') as f:
            metrics['CNN-LSTM'] = json.load(f)
    except:
        pass
    
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