# FloodMapAI
FloodMapAI is an interactive flood-risk prediction tool that uses machine learning and environmental data to estimate flood probability. It features an intuitive heatmap, on-click location details, smart markers, and FEMA comparison to help users explore and understand local flood vulnerability.

An interactive, map-based flood-risk visualization tool that uses machine learning, environmental data, and geospatial mapping to estimate and explore predicted flood risk for any location in the dataset.
The dashboard includes a heatmap, detailed clickable markers, and dynamic filtering controls, making it suitable for research, emergency planning, and community awareness.

🚀 Features
🔥 Machine Learning Flood Prediction

Uses a Random Forest Regressor to model flood risk.

Trained on elevation, rainfall patterns, storm events, and precipitation metrics.

Predicts a continuous predicted_risk score for each location.

🗺️ Interactive Map

Built using Folium + Leaflet.js:

Always-on heatmap showing flood intensity.

Clickable markers revealing detailed environmental metrics.

Dynamic layer control for toggling heatmap and point layers.

Color-coded risk legend with continuous gradient.

🎚️ Real-Time Marker Filtering

Interactive sliders allow filtering by:

Risk level

Elevation

Yearly rainfall

Markers update live based on slider values.

📂 Input Data Requirements

The application reads a CSV named:

elev_flood_rain_merged.csv


It must contain the following columns:

Geographic data:
latitude_x, longitude_x

Elevation:
altitude (ft)

Rainfall & storm metrics:
total_rainfall_year, average_daily_rain, max_daily_rain,
rainy_days_count, heavy_rain_events,
very_heavy_events, mean_precip_probability,
mean_precip_cover

Target variable:
WNTW_RISKV (historical or externally defined flood-risk score)

📦 Installation
pip install pandas scikit-learn folium branca

▶️ Run the Dashboard

Place the dataset in the same folder as the script, then run:

python flood_risk_dashboard_clickable.py


This will generate:

flood_risk_dashboard_clickable.html


Open it in any browser.

🧠 Model Overview

The Random Forest model uses 9 environmental predictors:

Elevation

Annual rainfall

Average & max daily rainfall

Number of rainy days

Heavy / very heavy rain events

Mean precipitation probability & coverage

After training, risk predictions are normalized and visualized as:

A heatmap, showing high-risk zones in red.

Colored markers, where clicking reveals detailed metrics.

🎛️ Interactive Controls
Filter Markers Panel

Adjust sliders to dynamically hide or show points:

Risk ≥ slider value

Elevation ≥ slider value

Rainfall ≥ slider value

Layer Toggle

Turn on/off:

Flood Risk Heatmap

Detailed Points Layer

💾 Output

The final product is a fully interactive HTML dashboard generating:

flood_risk_dashboard_clickable.html


This file is self-contained and can be shared or deployed on any static web server.
