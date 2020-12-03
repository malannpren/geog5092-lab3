import geopandas as gpd
import pandas as pd
import rasterio as raster
import random
from shapely.geometry import Point
import fiona
def printfunc(final_join):
    # This function creates a print statement of mean, aws0150, for a table that describes the watersheds, HUC8 and HUC12.
    for row in final_join.iterrows():
        print('The mean value for', row[0][0], 'and HUC8 watershed', row[0][1], 'is', row[1][1])
#part 1
data = r"C:\Users\catan\Desktop\lab3.gpkg"
listlayers = fiona.listlayers(data)
ssurgo = []
wdbhuc = []
random.seed(0)
for item in listlayers:
    if 'ssurgo' in item:
        ssurgo.append(item)
    if 'huc' in item:
        wdbhuc.append(item)
sample_points = {'point_id': [], 'geometry': [], 'HUC':[]}
for layer in wdbhuc:
    watershed_output = gpd.read_file('.\lab3.gpkg', layer = layer)
    listname = [f for f in watershed_output.columns if 'HUC' in f][0]
    for idx, row in watershed_output.iterrows():
        extent = row['geometry'].bounds
        areakm = row['Shape_Area'] / 1000000
        point_count = int(round(areakm * 0.05))
        i = int(0)
        while i < point_count:
            x = random.uniform(extent[0], extent[2])
            y = random.uniform(extent[1], extent[3])
            p = (Point(x,y))
            if row['geometry'].contains(p):
                sample_points['geometry'].append(p)
                sample_points['point_id'].append(row[listname][0:8])
                sample_points['HUC'].append(listname)
                i = i + 1
df = gpd.GeoDataFrame(sample_points)
df.groupby(by='point_id').count()
# part 2
ssurgo_output = gpd.read_file('.\lab3.gpkg', layer = 'ssurgo_mapunits_lab3')
join = gpd.sjoin(df, ssurgo_output, how="left", op="within")
final_join = join.groupby(['HUC', 'point_id']).mean()
printfunc(final_join)
