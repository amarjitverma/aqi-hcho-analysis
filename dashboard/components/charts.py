"""
Charts Component - Plotly chart utilities
"""

import plotly.graph_objects as go
import plotly.express as px
import streamlit as st

def create_time_series_chart(data, x_col, y_col, title="Time Series", y_label="Value"):
    """Create a time series line chart"""
    fig = px.line(
        data,
        x=x_col,
        y=y_col,
        title=title,
        labels={y_col: y_label},
        markers=True
    )
    fig.update_layout(
        hovermode='x unified',
        height=400
    )
    return fig

def create_scatter_plot(data, x_col, y_col, title="Scatter Plot", color_col=None):
    """Create a scatter plot"""
    fig = px.scatter(
        data,
        x=x_col,
        y=y_col,
        color=color_col,
        title=title,
        trendline="ols"
    )
    fig.update_layout(height=400)
    return fig

def create_bar_chart(data, x_col, y_col, title="Bar Chart", orientation="v"):
    """Create a bar chart"""
    fig = px.bar(
        data,
        x=x_col,
        y=y_col,
        title=title,
        orientation=orientation
    )
    fig.update_layout(height=400)
    return fig

def create_correlation_heatmap(data, title="Correlation"):
    """Create correlation heatmap"""
    corr_matrix = data.corr()
    fig = go.Figure(
        data=go.Heatmap(z=corr_matrix.values, x=corr_matrix.columns, y=corr_matrix.columns)
    )
    fig.update_layout(title=title, height=500)
    return fig
