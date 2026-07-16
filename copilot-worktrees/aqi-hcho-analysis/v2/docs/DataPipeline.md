\# Data Pipeline



\## Overview



The data pipeline handles acquisition, preprocessing, feature engineering, and dataset creation.



\## Pipeline Steps



\### 1. Data Acquisition



\#### Sentinel-5P (TROPOMI)

\- Products: NO₂, SO₂, CO, O₃, HCHO

\- Source: Google Earth Engine

\- Quality: QA value > 0.5



\#### ERA5

\- Variables: Temperature, wind, humidity, boundary layer height

\- Source: Copernicus CDS API



\#### FIRMS

\- Product: Active fires

\- Source: NASA FIRMS API



\#### CPCB

\- Parameter: PM2.5

\- Source: OpenAQ API



\### 2. Preprocessing



\#### Cleaning

\- Remove outliers using IQR method

\- Handle missing values



\#### Alignment

\- Align to 0.25° × 0.25° grid

\- Bilinear interpolation



\#### Gap-filling

\- Temporal: ±3 day window

\- Spatial: Gaussian filter



\#### Feature Engineering

\- Lag features: 1, 2, 3, 7 days

\- Rolling averages: 3, 7 days

\- Meteorological features



\### 3. Dataset Creation



\#### Sequences

\- For LSTM: sequences of length 7

\- For CNN-LSTM: spatiotemporal grids



\#### Splitting

\- Chronological split

\- 70% train, 15% validation, 15% test



\### 4. Outputs



\- `train.parquet`: Training dataset

\- `validation.parquet`: Validation dataset

\- `test.parquet`: Test dataset

\- `feature\_matrix.csv`: Full feature matrix

