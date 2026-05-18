# 04_flow_analysis.py
from pysheds.grid import Grid
import numpy as np
import rasterio
import matplotlib.pyplot as plt

print("Loading filled DEM...")
grid = Grid.from_raster('data/processed/dem_filled.tif')
dem  = grid.read_raster('data/processed/dem_filled.tif')

# Calculate slope
print("Calculating slope...")
def calc_slope(dem_arr, cell_size):
    dem_f = dem_arr.astype(float)
    dem_f[dem_f == -9999] = np.nan
    dy, dx = np.gradient(dem_f, cell_size)
    return np.degrees(np.arctan(np.sqrt(dx**2 + dy**2)))

with rasterio.open('data/processed/dem_filled.tif') as src:
    dem_arr   = src.read(1).astype(float)
    cell_size = src.res[0]
    profile   = src.profile.copy()

slope = calc_slope(dem_arr, cell_size)
profile.update(dtype='float32', nodata=-9999)
with rasterio.open('data/processed/slope.tif', 'w', **profile) as dst:
    out = slope.copy()
    out[np.isnan(slope)] = -9999
    dst.write(out.astype('float32'), 1)
print(f"  Slope range: {np.nanmin(slope):.1f} to {np.nanmax(slope):.1f} degrees")

# Calculate flow direction
print("Calculating flow direction...")
fdir = grid.flowdir(dem)
grid.to_raster(fdir, 'data/processed/flow_direction.tif')

# Calculate flow accumulation
print("Calculating flow accumulation...")
acc = grid.accumulation(fdir)
grid.to_raster(acc, 'data/processed/flow_accumulation.tif')
print(f"  Max accumulation: {float(acc.max()):,.0f} pixels")

# Plot flow accumulation
acc_arr = np.array(acc).astype(float)
acc_arr[acc_arr <= 0] = 0.1
plt.figure(figsize=(10, 8))
im = plt.imshow(np.log10(acc_arr), cmap='Blues', interpolation='bilinear')
plt.colorbar(im, label='Log10 Flow Accumulation')
plt.title('Flow Accumulation — Onkaparinga Catchment', fontsize=14)
plt.tight_layout()
plt.savefig('maps/02_flow_accumulation.png', dpi=150)
plt.show()

print("\nAll done! Files saved:")
print("  data/processed/slope.tif")
print("  data/processed/flow_direction.tif")
print("  data/processed/flow_accumulation.tif")
print("  maps/02_flow_accumulation.png")