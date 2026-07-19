# ============================================================
# Chart Visualization
# ============================================================

"""Chart generation using Plotly."""

import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import pandas as pd


def create_scatter_plot(actual, predicted, title="Predicted vs Actual"):
    """
    Create a scatter plot of predicted vs actual values.

    Args:
        actual (np.ndarray): Actual values
        predicted (np.ndarray): Predicted values
        title (str): Plot title

    Returns:
        plotly.graph_objects.Figure: Scatter plot
    """
    df = pd.DataFrame({"Actual": actual, "Predicted": predicted})

    fig = px.scatter(
        df,
        x="Actual",
        y="Predicted",
        title=title,
        labels={"Actual": "Actual PM2.5 (µg/m³)", "Predicted": "Predicted PM2.5 (µg/m³)"},
        trendline="ols",
        color_discrete_sequence=["#1A73E8"],
    )

    # Add diagonal line
    min_val = min(actual.min(), predicted.min())
    max_val = max(actual.max(), predicted.max())
    fig.add_trace(
        go.Scatter(
            x=[min_val, max_val],
            y=[min_val, max_val],
            mode="lines",
            name="Perfect Prediction",
            line=dict(color="red", dash="dash"),
        )
    )

    fig.update_layout(template="plotly_dark", hovermode="closest", height=400)

    return fig


def create_feature_importance(features, importance, title="Feature Importance"):
    """
    Create a feature importance bar chart.

    Args:
        features (list): Feature names
        importance (list): Importance scores
        title (str): Plot title

    Returns:
        plotly.graph_objects.Figure: Bar chart
    """
    df = pd.DataFrame({"Feature": features, "Importance": importance}).sort_values(
        "Importance", ascending=True
    )

    fig = px.bar(
        df,
        x="Importance",
        y="Feature",
        orientation="h",
        title=title,
        labels={"Importance": "Importance (%)", "Feature": ""},
        color="Importance",
        color_continuous_scale="Viridis",
    )

    fig.update_layout(template="plotly_dark", height=400, showlegend=False)

    return fig


def create_correlation_chart(
    lags, correlations, p_values, optimal_lag=None, title="Fire-HCHO Lagged Correlation"
):
    """
    Create a lagged correlation chart.

    Args:
        lags (list): Lag days
        correlations (list): Correlation values
        p_values (list): P-values
        optimal_lag (int): Optimal lag
        title (str): Plot title

    Returns:
        plotly.graph_objects.Figure: Correlation chart
    """
    colors = ["#888" if lag_val != optimal_lag else "#2ECC71" for lag_val in lags]

    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x=lags,
            y=correlations,
            marker_color=colors,
            text=[f"p={p:.3f}" for p in p_values],
            textposition="outside",
        )
    )

    fig.add_hline(y=0, line_dash="dash", line_color="gray")

    if optimal_lag is not None:
        best_idx = lags.index(optimal_lag)
        fig.add_annotation(
            x=optimal_lag,
            y=correlations[best_idx] + 0.1,
            text=f"Optimal: {optimal_lag} days",
            showarrow=True,
            arrowhead=2,
            arrowsize=1,
            arrowcolor="#2ECC71",
        )

    fig.update_layout(
        template="plotly_dark",
        title=title,
        xaxis_title="Lag (Days)",
        yaxis_title="Pearson Correlation (r)",
        height=400,
    )

    return fig


def create_pie_chart(labels, values, title="Source Region Contribution"):
    """
    Create a pie chart.

    Args:
        labels (list): Labels
        values (list): Values
        title (str): Plot title

    Returns:
        plotly.graph_objects.Figure: Pie chart
    """
    fig = px.pie(
        names=labels, values=values, title=title, color_discrete_sequence=px.colors.qualitative.Set3
    )

    fig.update_layout(template="plotly_dark", height=400)

    return fig


def create_metrics_dashboard(metrics):
    """
    Create a metrics dashboard with gauges.

    Args:
        metrics (dict): Model metrics

    Returns:
        plotly.graph_objects.Figure: Metrics dashboard
    """
    fig = make_subplots(
        rows=2,
        cols=2,
        subplot_titles=("RMSE", "R²", "MAE", "MAPE"),
        specs=[
            [{"type": "indicator"}, {"type": "indicator"}],
            [{"type": "indicator"}, {"type": "indicator"}],
        ],
    )

    # RMSE
    fig.add_trace(
        go.Indicator(
            mode="number+gauge",
            value=metrics.get("rmse", 0),
            title={"text": "RMSE"},
            domain={"row": 0, "column": 0},
            gauge={
                "axis": {"range": [0, 30]},
                "bar": {"color": "#2ECC71" if metrics.get("rmse", 0) < 15 else "#FF9800"},
                "steps": [
                    {"range": [0, 15], "color": "#1B5E20"},
                    {"range": [15, 30], "color": "#4E342E"},
                ],
            },
        ),
        row=1,
        col=1,
    )

    # R²
    fig.add_trace(
        go.Indicator(
            mode="number+gauge",
            value=metrics.get("r2", 0),
            title={"text": "R²"},
            domain={"row": 0, "column": 1},
            gauge={
                "axis": {"range": [0, 1]},
                "bar": {"color": "#2ECC71" if metrics.get("r2", 0) > 0.8 else "#FF9800"},
                "steps": [
                    {"range": [0.8, 1], "color": "#1B5E20"},
                    {"range": [0.6, 0.8], "color": "#4E342E"},
                ],
            },
        ),
        row=1,
        col=2,
    )

    # MAE
    fig.add_trace(
        go.Indicator(
            mode="number+gauge",
            value=metrics.get("mae", 0),
            title={"text": "MAE"},
            domain={"row": 1, "column": 0},
            gauge={
                "axis": {"range": [0, 20]},
                "bar": {"color": "#2ECC71" if metrics.get("mae", 0) < 10 else "#FF9800"},
                "steps": [
                    {"range": [0, 10], "color": "#1B5E20"},
                    {"range": [10, 20], "color": "#4E342E"},
                ],
            },
        ),
        row=2,
        col=1,
    )

    # MAPE
    fig.add_trace(
        go.Indicator(
            mode="number+gauge",
            value=metrics.get("mape", 0),
            title={"text": "MAPE %"},
            domain={"row": 1, "column": 1},
            gauge={
                "axis": {"range": [0, 30]},
                "bar": {"color": "#2ECC71" if metrics.get("mape", 0) < 20 else "#FF9800"},
                "steps": [
                    {"range": [0, 20], "color": "#1B5E20"},
                    {"range": [20, 30], "color": "#4E342E"},
                ],
            },
        ),
        row=2,
        col=2,
    )

    fig.update_layout(template="plotly_dark", height=500, width=700)

    return fig
