# 🌍 AQI & HCHO Hotspot Analysis

**Satellite-based Surface AQI Prediction & HCHO Hotspot Analysis over India**

---

## 📋 Project Overview

This project addresses two critical air quality challenges in India:

1. **Surface AQI Prediction**: Predict PM2.5 concentrations using satellite data and deep learning (LSTM, CNN-LSTM, ConvLSTM, Transformer).
2. **HCHO Hotspot Detection**: Identify formaldehyde hotspots from biomass burning using DBSCAN clustering and analyze fire-HCHO correlation.

Built for **ISRO Bharatiya Antariksh Hackathon 2026**.

---

## 🎯 Objectives

| Objective | Description |
|-----------|-------------|
| **Objective 1** | Surface AQI Prediction using Sentinel-5P, ERA5, and CPCB data |
| **Objective 2** | HCHO Hotspot Identification using DBSCAN and wind transport analysis |

---

## 📁 Project Structure

```
aqi-hcho-analysis/
├── data/               # All datasets
│   ├── raw/            # Original immutable datasets
│   ├── interim/        # Temporarily processed datasets
│   ├── processed/      # Final ML-ready datasets
│   ├── features/       # Cached engineered features
│   ├── metadata/       # Variable documentation
│   └── external/       # Static reference datasets
│
├── src/                # Source code
│   ├── acquisition/    # Data download modules
│   ├── preprocessing/  # Data cleaning & alignment
│   ├── features/       # Feature engineering
│   ├── gis/            # GIS and geospatial utilities
│   ├── models/         # LSTM, CNN-LSTM, ConvLSTM, Transformer
│   ├── training/       # Training framework
│   ├── evaluation/     # Model evaluation
│   ├── analysis/       # HCHO hotspot, correlation, transport
│   └── utils/          # Utilities
│
├── dashboard/          # Streamlit application
├── models/             # Trained model weights
├── outputs/            # Generated outputs
├── config/             # Configuration files
├── docs/               # Documentation
├── tests/              # Unit and integration tests
└── scripts/            # Executable automation scripts
```

---

## 🚀 Quick Start

```bash
# Clone repository
git clone https://github.com/amarjitverma/aqi-hcho-analysis.git
cd aqi-hcho-analysis

# Create virtual environment
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure API keys
cp .env.example .env
# Edit .env with your API keys

# Download data
python scripts/download_data.py

# Preprocess data
python scripts/preprocess.py

# Train model
python scripts/train.py --model lstm

# Launch dashboard
streamlit run dashboard/app.py
```

---

## 📊 Expected Results

| Metric | Target |
|--------|--------|
| LSTM RMSE | < 15 µg/m³ |
| CNN-LSTM RMSE | < 12 µg/m³ |
| ConvLSTM RMSE | < 11 µg/m³ |
| Transformer RMSE | < 11 µg/m³ |
| R² | > 0.80 |
| Optimal Lag | 2 days |
| IGP Contribution | ~72% |

---

## 📡 Data Sources

- **Sentinel-5P (TROPOMI)** — NO₂, SO₂, CO, O₃, HCHO
- **MODIS** — Aerosol Optical Depth (AOD)
- **VIIRS** — Active fires
- **ERA5** — Meteorology (temperature, wind, humidity)
- **CPCB** — Ground PM2.5 data

---

## 🛠️ Technologies

- **Programming**: Python
- **Deep Learning**: TensorFlow, Keras
- **Geospatial**: Google Earth Engine, GeoPandas, Folium
- **Dashboard**: Streamlit, Plotly
- **Version Control**: Git, GitHub

---

## 👥 Team

**Team Swachh Agam**

The Team comprises four students pursuing their BS in Data Science and Applications from IIT Madras, working together to build a comprehensive air quality monitoring and analysis platform for the ISRO Hackathon.

- **Amarjit Verma** — Team Lead, Integration & QA
- **Siddharth Yadav** — Satellite Data & Preprocessing
- **Anurag Kumar** — HCHO & Fire Analysis
- **Ravi Kumar** — Dashboard & Visualization

---

## 📄 License

MIT License

---

**Built with ❤️ for ISRO Bharatiya Antariksh Hackathon 2026**
