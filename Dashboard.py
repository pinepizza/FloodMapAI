import pandas as pd
from sklearn.ensemble import RandomForestRegressor
import folium
from folium.plugins import HeatMap
from branca.colormap import LinearColormap
from folium import Html

# 1️⃣ Load dataset
df = pd.read_csv("elev_flood_rain_merged.csv")

# 2️⃣ Features for prediction
features = [
    'altitude (ft)',
    'total_rainfall_year',
    'average_daily_rain',
    'max_daily_rain',
    'rainy_days_count',
    'heavy_rain_events',
    'very_heavy_events',
    'mean_precip_probability',
    'mean_precip_cover'
]

X = df[features]
y = df['WNTW_RISKV']

# 3️⃣ Train Random Forest
rf_model = RandomForestRegressor(n_estimators=300, max_depth=12, random_state=42)
rf_model.fit(X, y)
df['predicted_risk'] = rf_model.predict(X)
df['risk_norm'] = (df['predicted_risk'] - df['predicted_risk'].min()) / \
                  (df['predicted_risk'].max() - df['predicted_risk'].min())

# 4️⃣ Base map
m = folium.Map(location=[df['latitude_x'].mean(), df['longitude_x'].mean()], zoom_start=11)

# 5️⃣ Heatmap layer (always visible)
heatmap_layer = folium.FeatureGroup(name='Flood Risk Heatmap', show=True)
heat_data = [[row['latitude_x'], row['longitude_x'], row['risk_norm']] for _, row in df.iterrows()]
HeatMap(
    heat_data,
    min_opacity=0.3,
    radius=15,
    blur=25,
    gradient={0.2:'green',0.5:'yellow',0.8:'red'}
).add_to(heatmap_layer)
heatmap_layer.add_to(m)

# 6️⃣ Marker layer
marker_layer = folium.FeatureGroup(name='Detailed Points', show=True)
colormap = LinearColormap(['green','yellow','red'],
                          vmin=df['predicted_risk'].min(),
                          vmax=df['predicted_risk'].max(),
                          caption='Predicted Flood Risk')

for _, row in df.iterrows():
    color = colormap(row['predicted_risk'])
    folium.CircleMarker(
        location=[row['latitude_x'], row['longitude_x']],
        radius=6,
        color=color,
        fill=True,
        fill_color=color,
        fill_opacity=0.8,
        popup=(
            f"<b>Predicted Risk:</b> {row['predicted_risk']:.2f}<br>"
            f"<b>Elevation:</b> {row['altitude (ft)']:.1f} ft<br>"
            f"<b>Total Rainfall:</b> {row['total_rainfall_year']:.2f} in<br>"
            f"<b>Average Daily Rain:</b> {row['average_daily_rain']:.3f} in<br>"
            f"<b>Max Daily Rain:</b> {row['max_daily_rain']:.2f} in<br>"
            f"<b>Rainy Days:</b> {row['rainy_days_count']}<br>"
            f"<b>Heavy Rain Events:</b> {row['heavy_rain_events']}<br>"
            f"<b>Very Heavy Rain Events:</b> {row['very_heavy_events']}<br>"
            f"<b>Mean Precip Probability:</b> {row['mean_precip_probability']:.2f}%<br>"
            f"<b>Mean Precip Coverage:</b> {row['mean_precip_cover']:.2f}"
        ),
        **{'risk': row['predicted_risk'], 'elev': row['altitude (ft)'], 'rain': row['total_rainfall_year']}
    ).add_to(marker_layer)

marker_layer.add_to(m)
colormap.add_to(m)

# 7️⃣ Layer control so user can toggle heatmap or points
folium.LayerControl().add_to(m)

# 8️⃣ Add HTML sliders for filtering markers
slider_html = """
<div style="position: fixed; bottom: 50px; left: 50px; z-index:9999; background:white; padding:10px; border:2px solid gray;">
<h4>Filter Markers</h4>
Risk: <input type="range" id="riskSlider" min=0 max=100 step=1 value=0> <span id="riskVal">0</span><br>
Elevation: <input type="range" id="elevSlider" min=0 max=1000 step=10 value=0> <span id="elevVal">0</span><br>
Rainfall: <input type="range" id="rainSlider" min=0 max=50 step=0.1 value=0> <span id="rainVal">0</span>
</div>

<script>
var markers = [];
for (var i in window.L.map_instances[0]._layers){
    var l = window.L.map_instances[0]._layers[i];
    if(l instanceof L.CircleMarker){markers.push(l);}
}
var riskSlider = document.getElementById('riskSlider');
var elevSlider = document.getElementById('elevSlider');
var rainSlider = document.getElementById('rainSlider');
var riskVal = document.getElementById('riskVal');
var elevVal = document.getElementById('elevVal');
var rainVal = document.getElementById('rainVal');

function updateMarkers(){
    var r = parseFloat(riskSlider.value);
    var e = parseFloat(elevSlider.value);
    var ra = parseFloat(rainSlider.value);
    riskVal.innerHTML = r; elevVal.innerHTML = e; rainVal.innerHTML = ra;
    markers.forEach(function(m){
        if(m.options.risk>=r && m.options.elev>=e && m.options.rain>=ra){
            m.setStyle({fillOpacity:0.8, opacity:1});
        } else{
            m.setStyle({fillOpacity:0, opacity:0});
        }
    });
}

riskSlider.addEventListener('input', updateMarkers);
elevSlider.addEventListener('input', updateMarkers);
rainSlider.addEventListener('input', updateMarkers);
</script>
"""
m.get_root().html.add_child(Html(slider_html, script=True))

# 9️⃣ Save map
m.save("flood_risk_dashboard_clickable.html")
print("✅ Dashboard with heatmap + clickable markers + working filters saved as 'flood_risk_dashboard_clickable.html'")
