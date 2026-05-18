# 01_merge_dem.py
import rasterio
from rasterio.merge import merge
import glob
import os

# Find all DEM tiles
tiles = glob.glob('data/raw/flood-risk-data/DEM/1 Metre/*.tif')

print(f"Found {len(tiles)} tiles:")
for t in tiles:
    print(f"  {os.path.basename(t)}")

# Open all tiles
datasets = [rasterio.open(t) for t in tiles]

# Merge into one
print("\nMerging tiles — please wait...")
mosaic, transform = merge(datasets)

# Copy settings from first tile
profile = datasets[0].profile.copy()
profile.update({
    "height": mosaic.shape[1],
    "width":  mosaic.shape[2],
    "transform": transform
})

# Save merged DEM
output = 'data/raw/dem_onkaparinga.tif'
with rasterio.open(output, 'w', **profile) as dst:
    dst.write(mosaic)

# Close all tiles
for ds in datasets:
    ds.close()

size_mb = os.path.getsize(output) / 1e6
print(f"\nDone! Merged DEM saved: {output}")
print(f"File size: {size_mb:.1f} MB")