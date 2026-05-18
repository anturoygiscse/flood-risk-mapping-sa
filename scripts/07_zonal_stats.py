# 07_zonal_stats.py
import geopandas as gpd
from rasterstats import zonal_stats
import rasterio
from shapely.geometry import box
import glob

print("Loading council boundaries...")
lga_files = glob.glob('data/raw/LGA_shp/*.shp')
councils = gpd.read_file(lga_files[0])
councils = councils.to_crs('EPSG:28354')

# Get raster extent and clip councils to it
print("Clipping councils to study area...")
with rasterio.open('data/processed/flood_risk_continuous.tif') as src:
    bounds = src.bounds
    raster_crs = src.crs

study_area = box(bounds.left, bounds.bottom, bounds.right, bounds.top)
study_gdf = gpd.GeoDataFrame({'geometry': [study_area]}, crs=raster_crs)
councils_clipped = gpd.clip(councils, study_gdf)
print(f"Councils in study area: {len(councils_clipped)}")

print("Calculating zonal statistics...")
stats = zonal_stats(
    councils_clipped,
    'data/processed/flood_risk_continuous.tif',
    stats=['mean', 'max', 'std'],
    nodata=-9999
)

councils_clipped['mean_risk'] = [s['mean'] for s in stats]
councils_clipped['max_risk']  = [s['max']  for s in stats]

councils_sorted = councils_clipped.dropna(subset=['mean_risk'])
councils_sorted = councils_sorted.sort_values('mean_risk', ascending=False)

print("\nFlood risk by council:")
print("-" * 50)
for i, row in councils_sorted.iterrows():
    print(f"{str(row.iloc[0]):<35} Mean: {row['mean_risk']:.3f}  Max: {row['max_risk']:.3f}")

councils_clipped.to_file('data/processed/councils_flood_risk.shp')
councils_sorted[['mean_risk','max_risk']].to_csv(
    'data/processed/flood_risk_by_council.csv')

print("\nSaved: councils_flood_risk.shp")
print("Saved: flood_risk_by_council.csv")