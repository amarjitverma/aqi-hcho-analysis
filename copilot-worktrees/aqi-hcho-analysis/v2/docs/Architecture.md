# System Architecture

## Overview

The AQI & HCHO Hotspot Analysis platform follows a modular architecture with clear separation of concerns. The system is designed to be scalable, maintainable, and reproducible.

## Architecture Diagram
┌─────────────────────────────────────────────────────────────────────────────┐
│ DATA ACQUISITION │
│ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ │
│ │ Sentinel-5P │ │ MODIS │ │ VIIRS │ │ ERA5 │ │
│ │ (NO₂, SO₂, │ │ (AOD) │ │ (Fires) │ │ (Weather) │ │
│ │ CO, O₃, │ │ │ │ │ │ │ │
│ │ HCHO) │ │ │ │ │ │ │ │
│ └─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘ │
│ CPCB / OpenAQ │
│ (Ground PM2.5 Data) │
└─────────────────────────────────────────────────────────────────────────────┘
│
▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ PREPROCESSING & GIS │
│ • Spatial Alignment (0.25° grid) • Gap-Filling (Cloud Cover) │
│ • Feature Engineering • Temporal/Sequential Data Prep │
│ • Chronological Data Split (Train/Val/Test) │
└─────────────────────────────────────────────────────────────────────────────┘
│
▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ MODEL TRAINING │
│ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ ┌─────────────┐ │
│ │ LSTM │ │ CNN-LSTM │ │ ConvLSTM │ │ Transformer │ │
│ │ (Baseline) │ │ (Hybrid) │ │ (Spatial) │ │ (Attention) │ │
│ └─────────────┘ └─────────────┘ └─────────────┘ └─────────────┘ │
│ Ensemble │
└─────────────────────────────────────────────────────────────────────────────┘
│
▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ SCIENTIFIC ANALYSIS │
│ • HCHO Hotspot Detection (DBSCAN) • Fire-HCHO Lagged Correlation │
│ • Wind Transport & Plume Decay • Source Region Attribution │
│ • Trend & Seasonal Analysis │
└─────────────────────────────────────────────────────────────────────────────┘
│
▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ VISUALIZATION │
│ • Interactive Maps (Folium) • Charts (Plotly) │
│ • Time-Series Animations • Dashboard Data Generation │
└─────────────────────────────────────────────────────────────────────────────┘
│
▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ STREAMLIT DASHBOARD │
│ ┌─────────────────┐ ┌─────────────────┐ ┌─────────────────┐ │
│ │ Map View │ │ Performance │ │ Biomass │ │
│ │ (AQI / HCHO / │ │ (Metrics / │ │ Burning │ │
│ │ Fire / Wind) │ │ Charts) │ │ (Hotspots) │ │
│ └─────────────────┘ └─────────────────┘ └─────────────────┘ │
└─────────────────────────────────────────────────────────────────────────────┘
│
▼
┌─────────────────────────────────────────────────────────────────────────────┐
│ OUTPUTS │
│ • AQI Maps • HCHO Hotspot Maps • Correlation Plots │
│ • Reports • Model Metrics • Predictions │
└─────────────────────────────────────────────────────────────────────────────┘

## Module Descriptions

### Data Acquisition
Handles downloading data from satellite, meteorological, and ground sources.

### Preprocessing & GIS
Cleans, aligns, and prepares data for modeling. Includes gap-filling and feature engineering.

### Model Training
Trains multiple deep learning architectures (LSTM, CNN-LSTM, ConvLSTM, Transformer).

### Scientific Analysis
Performs HCHO hotspot detection, fire-HCHO correlation, and wind transport analysis.

### Visualization
Generates maps, charts, and dashboard data.

### Dashboard
Interactive Streamlit application for exploring results.

## Data Flow

1. Raw data is downloaded from sources
2. Data is preprocessed and aligned to 0.25° grid
3. Features are engineered
4. Models are trained and evaluated
5. Scientific analysis is performed
6. Results are visualized in the dashboard