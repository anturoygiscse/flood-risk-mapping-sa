# 02_inspect_dem.py
import rasterio
import numpy as np
import matplotlib.pyplot as plt

# Load merged DEM
with rasterio.open('data/raw/dem_onkaparinga.tif') as src:
    dem = src.read(1).astype(float)
    nodata = src.nodata
    crs = src.crs
    res = src.res

# Replace nodata with NaN
if nodata is not None:
    dem[dem == nodata] = np.nan

# Print info
print("=== DEM Information ===")
print(f"CRS:        {crs}")
print(f"Resolution: {res[0]}m x {res[1]}m")
print(f"Shape:      {dem.shape[0]} rows x {dem.shape[1]} cols")
print(f"Min elev:   {np.nanmin(dem):.1f} m")
print(f"Max elev:   {np.nanmax(dem):.1f} m")
print(f"Mean elev:  {np.nanmean(dem):.1f} m")

# Plot
plt.figure(figsize=(10, 8))
plt.imshow(dem, cmap='terrain', interpolation='bilinear')
plt.colorbar(label='Elevation (metres)')
plt.title('Onkaparinga DEM: Elevation Map', fontsize=14)
plt.tight_layout()
plt.savefig('maps/01_dem_overview.png', dpi=150)
plt.show()
print("Map saved: maps/01_dem_overview.png")