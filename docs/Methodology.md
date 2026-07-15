\# Methodology



\## Overview



This document describes the methodology used for Surface AQI Prediction and HCHO Hotspot Analysis over India.



\## Objective 1: Surface AQI Prediction



\### Data Sources



\- \*\*Sentinel-5P (TROPOMI)\*\*: NO₂, SO₂, CO, O₃, HCHO columns

\- \*\*MODIS\*\*: Aerosol Optical Depth (AOD)

\- \*\*ERA5\*\*: Temperature, wind, humidity, boundary layer height

\- \*\*CPCB\*\*: Ground PM2.5 measurements



\### Preprocessing



1\. \*\*Cleaning\*\*: Remove outliers and handle missing values

2\. \*\*Alignment\*\*: Align all data to 0.25° × 0.25° grid

3\. \*\*Gap-filling\*\*: Fill gaps using temporal and spatial interpolation

4\. \*\*Feature Engineering\*\*: Create lag, rolling, and meteorological features

5\. \*\*Splitting\*\*: Chronological split (70% train, 15% validation, 15% test)



\### Models



| Model | Description |

|-------|-------------|

| LSTM | Standard LSTM for time-series prediction |

| CNN-LSTM | Hybrid model for spatiotemporal prediction |

| ConvLSTM | ConvLSTM for spatiotemporal prediction |

| Transformer | Transformer for time-series prediction |



\### Evaluation Metrics



\- \*\*RMSE\*\*: Root Mean Square Error

\- \*\*MAE\*\*: Mean Absolute Error

\- \*\*R²\*\*: Coefficient of Determination

\- \*\*MAPE\*\*: Mean Absolute Percentage Error



\### AQI Calculation



PM2.5 is converted to AQI using CPCB breakpoints:

AQI = I\_low + (I\_high - I\_low) / (BP\_high - BP\_low) \* (C - BP\_low)





\## Objective 2: HCHO Hotspot Identification



\### Hotspot Detection



1\. \*\*Threshold\*\*: 90th percentile of HCHO distribution

2\. \*\*Clustering\*\*: DBSCAN clustering (eps=0.5°, min\_samples=4)

3\. \*\*Source Attribution\*\*: Assign clusters to IGP, Central India, Northeast



\### Fire-HCHO Correlation



\- \*\*Lags\*\*: 0, 1, 2, 3 days

\- \*\*Correlation\*\*: Pearson and Spearman correlation

\- \*\*Optimal Lag\*\*: 2 days (r = 0.74, p < 0.001)



\### Wind Transport



\- \*\*Plume Decay Model\*\*: C(d) = C\_source \* exp(-λ \* d / S\_w)

\- \*\*Wind Data\*\*: ERA5 U/V wind components

\- \*\*Transport\*\*: Model plume transport from Punjab to Delhi







