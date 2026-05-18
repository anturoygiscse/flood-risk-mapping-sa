# 05_normalise.py
import numpy as np
import rasterio

def normalise(array, inverse=False):
    valid = array[~np.isnan(array)]
    mn, mx = valid.min(), valid.max()
    norm = (array - mn) / (mx - mn)
    if inverse:
        norm = 1 - norm
    return np.clip(norm, 0, 1)

def load_raster(path):
    with rasterio.open(path) as src:
        arr = src.read(1).astype(float)
        arr[arr == src.nodata] = np.nan
        return arr, src.profile

print("Loading rasters...")
dem_arr, profile = load_raster('data/processed/dem_filled.tif')
slope_arr, _     = load_raster('data/processed/slope.tif')
acc_arr, _       = load_raster('data/processed/flow_accumulation.tif')

print("Normalising...")
elev_norm  = normalise(dem_arr, inverse=True)
slope_norm = normalise(slope_arr, inverse=True)
acc_norm   = normalise(np.log10(acc_arr + 1))

np.save('data/processed/elev_norm.npy', elev_norm)
np.save('data/processed/slope_norm.npy', slope_norm)
np.save('data/processed/acc_norm.npy', acc_norm)

print("Done! All 3 layers normalised and saved.")