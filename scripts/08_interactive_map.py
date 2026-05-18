# 08_interactive_map.py - FIXED VERSION
import folium
import numpy as np
import rasterio
from rasterio.warp import transform_bounds
from rasterio.crs import CRS
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors
import io, base64, glob
from PIL import Image
import geopandas as gpd

print("Creating interactive web map...")

with rasterio.open('data/processed/flood_risk_classified.tif') as src:
    data = src.read(1).astype(float)
    bounds = src.bounds
    crs = src.crs

wgs84 = CRS.from_epsg(4326)
left, bottom, right, top = transform_bounds(crs, wgs84,
    bounds.left, bounds.bottom, bounds.right, bounds.top)

centre_lat = (top + bottom) / 2
centre_lon = (left + right) / 2

# Create map with OpenStreetMap tiles
m = folium.Map(
    location=[centre_lat, centre_lon],
    zoom_start=13,
    tiles='OpenStreetMap'
)

# Add satellite view option
folium.TileLayer(
    tiles='https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
    attr='Esri',
    name='Satellite'
).add_to(m)

# Colour the risk map
data[data == 0] = np.nan
colors_list = ['#1a9641','#a6d96a','#ffffbf','#fdae61','#d7191c']
cmap = mcolors.ListedColormap(colors_list)
norm = mcolors.Normalize(vmin=1, vmax=5)

rgba = plt.cm.ScalarMappable(cmap=cmap, norm=norm).to_rgba(data, alpha=0.7)
rgba[np.isnan(data)] = [0,0,0,0]
img = Image.fromarray((rgba * 255).astype(np.uint8))

buf = io.BytesIO()
img.save(buf, format='PNG')
img_str = base64.b64encode(buf.getvalue()).decode()

folium.raster_layers.ImageOverlay(
    image=f"data:image/png;base64,{img_str}",
    bounds=[[bottom, left],[top, right]],
    opacity=0.75,
    name='Flood Risk Layer'
).add_to(m)

# Legend
legend_html = """
<div style="position:fixed;bottom:30px;left:30px;z-index:1000;
background:white;padding:12px;border-radius:8px;
border:2px solid #1F5C3E;font-size:13px;font-family:Arial;">
<b style="color:#1F5C3E">Flood Risk — Onkaparinga SA</b><br><br>
<i style="background:#d7191c;width:14px;height:14px;display:inline-block;margin-right:6px"></i>Very High<br>
<i style="background:#fdae61;width:14px;height:14px;display:inline-block;margin-right:6px"></i>High<br>
<i style="background:#ffffbf;width:14px;height:14px;display:inline-block;margin-right:6px"></i>Medium<br>
<i style="background:#a6d96a;width:14px;height:14px;display:inline-block;margin-right:6px"></i>Low<br>
<i style="background:#1a9641;width:14px;height:14px;display:inline-block;margin-right:6px"></i>Very Low
</div>
"""
m.get_root().html.add_child(folium.Element(legend_html))
folium.LayerControl().add_to(m)

m.save('maps/flood_risk_interactive.html')
print(f"Done! Centre: {centre_lat:.4f}, {centre_lon:.4f}")
print("Saved: maps/flood_risk_interactive.html")
print("Open in browser — requires internet connection for map tiles!")