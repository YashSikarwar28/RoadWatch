#For testing the roads

import geopandas as gpd

gpkg_path = "data/osm/planet_80.11,12.783_80.612,13.099.gpkg"

gdf = gpd.read_file(gpkg_path, layer="lines")

roads = gdf["name"].dropna().unique()

print("\nFirst 100 roads in dataset:\n")

for road in roads[:100]:
    print(road)
