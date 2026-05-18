# Flood Risk Mapping — Onkaparinga Catchment, South Australia

![Flood Risk Map](maps/flood_risk_final.png)

## Overview
This project builds a **Flood Risk Index Map** for the Onkaparinga catchment 
in South Australia using terrain analysis, hydrology modelling, and spatial 
overlay in Python and QGIS.

The model identifies flood-prone areas by combining three key factors:
- **Land elevation** — low-lying areas are more flood-prone
- **Slope steepness** — flat areas accumulate water
- **Flow accumulation** — areas where water converges from upstream

## Study Area
Lower Onkaparinga River catchment, south of Adelaide, SA.
Covers Port Noarlunga, Seaford, Old Noarlunga, and Onkaparinga River National Park.

## Tools & Technologies
| Tool | Purpose |
|---|---|
| Python (rasterio, geopandas, pysheds) | DEM processing and analysis |
| Python (matplotlib, folium) | Visualisation and web mapping |
| QGIS 3.x | Professional cartographic output |
| ArcGIS Online | StoryMap (coming soon) |

## Data Sources
| Dataset | Source | Resolution |
|---|---|---|
| DEM (Onkaparinga 2019) | ELVIS — elevation.fsdf.org.au | 1 metre LiDAR |
| Watercourses | data.sa.gov.au | - |
| LGA Boundaries | data.sa.gov.au | - |
| Catchment boundaries | BOM Geofabric | - |

## Methodology
Raw DEM (9 tiles) → Merge → Fill sinks → Slope analysis
→ Flow direction → Flow accumulation → Weighted overlay
→ Flood Risk Index (0–1) → Classified map (5 classes)
## Results
| Risk Level | Pixels | Description |
|---|---|---|
| Very High | 3,007,381 | Flat coastal and low-lying urban areas |
| High | 3,134,628 | Near-river and low elevation zones |
| Medium | 21,678 | Transitional zones |
| Low | 3,114,957 | Moderate elevation areas |
| Very Low | 2,721,342 | Elevated hilly terrain |

## Scripts
| Script | Purpose |
|---|---|
| 01_merge_dem.py | Merge 9 DEM tiles into one file |
| 02_inspect_dem.py | Inspect and visualise DEM |
| 03_fill_sinks.py | Fill sinks and depressions |
| 04_flow_analysis.py | Calculate slope, flow direction, accumulation |
| 05_normalise.py | Normalise all layers to 0–1 scale |
| 06_risk_index.py | Calculate weighted flood risk index |
| 07_zonal_stats.py | Zonal statistics per council area |
| 08_interactive_map.py | Create interactive web map |

## Maps
- `maps/01_dem_overview.png` — Elevation map
- `maps/02_flow_accumulation.png` — Flow accumulation map
- `maps/03_flood_risk_map.png` — Flood risk map (Python)
- `maps/flood_risk_final.png` — Professional QGIS map
- `maps/flood_risk_interactive.html` — Interactive web map

## Author
**Antu Roy**
MSc Remote Sensing & GIS — Jahangirnagar University
Target: GIS Analyst roles — Adelaide, South Australia
LinkedIn: linkedin.com/in/antu-roy-gis

## License
Data sourced from Australian Government open data portals.
Licensed under Creative Commons Attribution 4.0 International.
