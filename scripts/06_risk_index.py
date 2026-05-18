# 06_risk_index.py
import numpy as np
import rasterio
import matplotlib.pyplot as plt
import matplotlib.colors as mcolors

print("Loading normalised layers...")
elev_norm  = np.load('data/processed/elev_norm.npy')
slope_norm = np.load('data/processed/slope_norm.npy')
acc_norm   = np.load('data/processed/acc_norm.npy')

# Weighted overlay
w_elevation = 0.50
w_slope     = 0.20
w_flowaccum = 0.30

print("Calculating flood risk index...")
flood_risk = (w_elevation * elev_norm +
              w_slope     * slope_norm +
              w_flowaccum * acc_norm)

# Classify into 5 risk levels
risk_class = np.zeros_like(flood_risk)
risk_class[flood_risk >= 0.8] = 5
risk_class[(flood_risk >= 0.6) & (flood_risk < 0.8)] = 4
risk_class[(flood_risk >= 0.4) & (flood_risk < 0.6)] = 3
risk_class[(flood_risk >= 0.2) & (flood_risk < 0.4)] = 2
risk_class[flood_risk < 0.2]  = 1

# Save both rasters
with rasterio.open('data/processed/dem_filled.tif') as src:
    profile = src.profile.copy()

profile.update(dtype='float32', nodata=-9999)
with rasterio.open('data/processed/flood_risk_continuous.tif', 'w', **profile) as dst:
    dst.write(flood_risk.astype('float32'), 1)

profile.update(dtype='int16', nodata=0)
with rasterio.open('data/processed/flood_risk_classified.tif', 'w', **profile) as dst:
    dst.write(risk_class.astype('int16'), 1)

# Plot
colors_list = ['#1a9641', '#a6d96a', '#ffffbf', '#fdae61', '#d7191c']
cmap = mcolors.ListedColormap(colors_list)
plt.figure(figsize=(10, 8))
plt.imshow(risk_class, cmap=cmap, vmin=1, vmax=5, interpolation='nearest')
cbar = plt.colorbar(ticks=[1,2,3,4,5])
cbar.set_ticklabels(['Very Low','Low','Medium','High','Very High'])
plt.title('Flood Risk Map — Onkaparinga Catchment, SA', fontsize=14)
plt.tight_layout()
plt.savefig('maps/03_flood_risk_map.png', dpi=150)
plt.show()

print("\nDone!")
print(f"Very High risk: {(risk_class==5).sum():,} pixels")
print(f"High risk:      {(risk_class==4).sum():,} pixels")
print(f"Medium risk:    {(risk_class==3).sum():,} pixels")
print(f"Low risk:       {(risk_class==2).sum():,} pixels")
print(f"Very Low risk:  {(risk_class==1).sum():,} pixels")
print("Saved: maps/03_flood_risk_map.png")