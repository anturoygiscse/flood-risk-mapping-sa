# 03_fill_sinks.py
from pysheds.grid import Grid
import os

print("Loading DEM...")
grid = Grid.from_raster('data/raw/dem_onkaparinga.tif')
dem  = grid.read_raster('data/raw/dem_onkaparinga.tif')
print(f"DEM loaded. Shape: {dem.shape}")

print("Step 1: Filling pits...")
pit_filled = grid.fill_pits(dem)

print("Step 2: Filling depressions...")
flooded = grid.fill_depressions(pit_filled)

print("Step 3: Resolving flat areas...")
inflated = grid.resolve_flats(flooded)

output = 'data/processed/dem_filled.tif'
grid.to_raster(inflated, output, nodata=-9999)

print(f"\nDone! Filled DEM saved: {output}")
print(f"File size: {os.path.getsize(output)/1e6:.1f} MB")
print("Ready for flow analysis!")