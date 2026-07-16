# 🌍 Swachh Agam Dashboard

**Streamlit-based Interactive Dashboard for Satellite-based AQI Prediction & HCHO Hotspot Analysis**

**Team**: Swachh Agam | ISRO Bharatiya Antariksh Hackathon 2026

---

## 📋 Overview

This dashboard provides real-time visualization and analysis of:
- 🌡️ **Air Quality Index (AQI)** predictions using satellite data
- 🧪 **HCHO Hotspot Detection** through formaldehyde concentration mapping
- 🔥 **Biomass Burning Analysis** with fire-HCHO correlation
- 📊 **ML Model Performance** metrics and explainability (SHAP)
- 📥 **Data Export & Sharing** in multiple formats
- 🔔 **Real-time Alerts** for critical events
- ⚙️ **Admin Panel** for system management

---

## 🚀 Quick Start

### 1. Setup Environment

```bash
# Install dependencies
pip install -r requirements.txt

# Or use conda
conda create -n swachh-agam python=3.9
conda activate swachh-agam
pip install -r requirements.txt
```

### 2. Run Dashboard

```bash
cd dashboard
streamlit run app.py
```

The app will open at `http://localhost:8501`

### 3. Explore Pages

Navigate using the left sidebar:
- 🏠 **Dashboard** - Overview with KPI cards
- 🗺️ **Map View** - Interactive geospatial analysis
- 📊 **Model Performance** - ML metrics and comparison
- 🔥 **Biomass Burning** - HCHO hotspot analysis
- 📥 **Export & Share** - Download data
- 🔔 **Alerts** - Notifications
- 📄 **Reports** - Generated reports
- 🗂️ **Data Sources** - Data management
- ⚙️ **Admin Panel** - System controls
- ❓ **Help & Support** - Documentation

---

## 📁 Project Structure

```
dashboard/
├── app.py                          # Main entry point
├── config.yaml                     # Dashboard configuration
├── requirements.txt                # Python dependencies
├── README.md                       # This file
│
├── pages/
│   ├── 01_🏠_Dashboard.py         # Overview page
│   ├── 02_🗺️_Map_View.py          # Geospatial analysis
│   ├── 03_📊_Model_Performance.py  # ML metrics
│   ├── 04_🔥_Biomass_Burning.py    # HCHO analysis
│   ├── 05_📥_Export_Share.py       # Data export
│   ├── 06_🔔_Alerts.py             # Notifications
│   ├── 07_📄_Reports.py            # Report generation
│   ├── 08_🗂️_Data_Sources.py       # Data management
│   ├── 09_⚙️_Admin_Panel.py        # Admin controls
│   └── 10_❓_Help_Support.py       # Help & documentation
│
├── components/
│   ├── __init__.py
│   ├── header.py                   # Header component
│   ├── metrics_cards.py            # KPI cards
│   ├── map_viewer.py               # Map wrapper
│   ├── charts.py                   # Chart utilities
│   └── alerts.py                   # Alert system (stub)
│
├── utils/
│   ├── __init__.py
│   ├── data_loader.py              # Data loading & caching
│   ├── map_utils.py                # Map helper functions
│   ├── chart_utils.py              # Chart formatting
│   ├── export.py                   # Export functionality
│   └── shap_explainer.py           # SHAP helper (stub)
│
└── assets/
    ├── logo.png                    # Swachh Agam logo
    ├── styles.css                  # Custom CSS
    └── icons/                      # Icon files
```

---

## 🛠️ Technology Stack

| Component | Technology | Version |
|-----------|-----------|---------|
| **Framework** | Streamlit | 1.35.0 |
| **Mapping** | Folium + Streamlit-Folium | 0.14.0 |
| **Charts** | Plotly | 5.17.0 |
| **Data** | Pandas, NumPy | 2.0.3, 1.24.3 |
| **Geospatial** | GeoPandas, Rasterio | 0.14.0, 1.3.9 |
| **ML** | Scikit-learn, XGBoost | 1.3.0, 2.0.3 |
| **Explainability** | SHAP | 0.42.1 |
| **Config** | PyYAML | 6.0 |

---

## 📊 Phase Implementation Status

### ✅ Phase 1: Core Structure (COMPLETE)
- [x] Folder structure
- [x] Main app.py entry point
- [x] Configuration system (config.yaml)
- [x] 10 page stubs
- [x] Component framework
- [x] Utility modules
- [x] Dependencies file

### ⏳ Phase 2: Dashboard Home (COMPLETE)
- [ ] Header with branding
- [ ] Sidebar navigation
- [ ] KPI cards (AQI, HCHO, Fires)
- [ ] Date selector
- [ ] Interactive map
- [ ] Layer controls
- [ ] Time slider

### 📅 Phase 3: Map View (Planned)
- [ ] Choropleth map (AQI)
- [ ] Fire markers layer
- [ ] HCHO hotspots layer
- [ ] Wind vectors layer
- [ ] Info panel
- [ ] Time series chart
- [ ] Correlation analysis

### 📅 Phase 4: Model Performance (Planned)
- [ ] Metric cards
- [ ] Model comparison table
- [ ] Scatter plot
- [ ] Feature importance
- [ ] SHAP explainability

### 📅 Phase 5: Biomass Burning (Planned)
- [ ] Cluster map
- [ ] Cluster statistics
- [ ] Fire-HCHO correlation
- [ ] Wind transport analysis
- [ ] Source contribution chart

### 📅 Phase 6: Supporting Pages (Planned)
- [ ] Export & Share
- [ ] Alerts
- [ ] Reports
- [ ] Data Sources
- [ ] Admin Panel
- [ ] Help & Support

---

## 🎨 Design Guidelines

### Color Palette

**AQI Categories:**
- 🟢 Good (0-50): `#2ECC71`
- 🟡 Satisfactory (51-100): `#F39C12`
- 🟠 Moderate (101-200): `#E67E22`
- 🔴 Poor (201-300): `#E74C3C`
- 🟣 Very Poor (301-400): `#8E44AD`
- 🔴 Hazardous (401+): `#C0392B`

**Brand Colors:**
- Primary: `#0066CC` (Blue)
- Secondary: `#FF6B6B` (Red)
- Accent: `#4ECDC4` (Teal)

---

## 📝 Configuration

Edit `config.yaml` to customize:
- Map center & zoom level
- Alert thresholds
- Data refresh intervals
- UI theme settings
- Performance parameters

Example:
```yaml
map:
  center_lat: 23.1815
  center_lon: 79.9864
  default_zoom: 5

alerts:
  aqi_poor_threshold: 200
  aqi_hazardous_threshold: 400
  hcho_high_threshold: 15.0
```

---

## 📡 Data Sources

The dashboard integrates data from:
- **Sentinel-5P (TROPOMI)** - NO₂, SO₂, CO, O₃, HCHO
- **MODIS** - Aerosol Optical Depth (AOD)
- **VIIRS/FIRMS** - Active fires
- **ERA5** - Meteorological data
- **CPCB** - Ground PM2.5 measurements
- **OpenAQ** - Air quality data

---

## 🔧 Development

### Adding New Pages

1. Create file in `pages/` with naming convention: `NN_emoji_Page_Name.py`
2. The page will auto-appear in sidebar navigation
3. Access via `st.session_state.page = 'page_key'`

Example:
```python
# pages/11_🎯_New_Page.py
import streamlit as st

st.title("🎯 New Page")
st.write("Your content here")
```

### Adding Components

1. Create function in `components/` module
2. Import and use in pages:

```python
from components.header import render_header

render_header()
```

### Adding Utilities

1. Create function in `utils/` module
2. Import and use in pages:

```python
from utils.data_loader import load_aqi_data

data = load_aqi_data()
```

---

## 🚀 Deployment

### Streamlit Cloud
```bash
# Push to GitHub
git push origin main

# Deploy at share.streamlit.io
# Select repository and deploy
```

### Docker
```bash
# Build
docker build -t swachh-agam-dashboard .

# Run
docker run -p 8501:8501 swachh-agam-dashboard
```

### Local Server
```bash
streamlit run app.py
```

---

## 📊 Performance Targets

- Page load time: < 3 seconds
- Map interaction: < 500ms response
- Data refresh: Every 6 hours
- Concurrent users: 100+
- Uptime: 99.5%

---

## 👥 Team

**Swachh Agam** - ISRO Hackathon 2026

| Role | Name | Responsibility |
|------|------|-----------------|
| Team Lead & Integration | Amarjit Verma | Overall integration & QA |
| Dashboard Lead | Ravi Kumar | UI/UX and frontend |
| Data & Preprocessing | Siddharth Yadav | Data pipeline |
| Analysis | Anurag Kumar | HCHO & fire analysis |

---

## 📞 Support

- **GitHub Issues**: [Report bugs](https://github.com/amarjitverma/aqi-hcho-analysis/issues)
- **Email**: amarjitengr@gmail.com
- **Documentation**: [GitHub Wiki](https://github.com/amarjitverma/aqi-hcho-analysis/wiki)

---

## 📄 License

MIT License - See LICENSE file in root directory

---

## 🎯 Next Steps

1. **Phase 2 Start**: Implement Dashboard Home with KPI cards and map
2. **Data Integration**: Connect real processed data to dashboard
3. **Testing**: Comprehensive testing on multiple browsers/devices
4. **Deployment**: Deploy to Streamlit Cloud or dedicated server
5. **User Feedback**: Iterate based on user feedback

---

**Last Updated**: July 16, 2026 | **Status**: Phase 1 Complete ✅

**Built with ❤️ for ISRO Bharatiya Antariksh Hackathon 2026**
