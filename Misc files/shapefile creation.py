"""
This code combines any file with a "site" column with the CPTE-CPTU-DMT shapefile from the GIS database. We made it
for liq_param_compiled files to look at adjusted PGA values geospatially in QGIS.
"""

import pandas as pd
import geopandas as gpd
from datetime import date

################ USER INPUTS ############################
adj_pga_file_path = r"C:\Users\jdundas2\OneDrive - Brigham Young University\Liq\Gabrelle update\liq_param_compiled\liq_param_compiled_adj_pga_1_stdev sporting goods 6-7.xlsx"
geopackage_file_path = r"C:\Users\jdundas2\OneDrive - Brigham Young University\Liq\master cpt attribute table.xlsx.gpkg"
export_file_path = r"C:\Users\jdundas2\OneDrive - Brigham Young University\Liq\results geopackages"
#########################################################
today_date = date.today()
date = f'{today_date.month}-{today_date.day}'

df = pd.read_excel(adj_pga_file_path)
df.rename(columns={'site':'id_indpu',}, inplace=True)
gdf = gpd.read_file(geopackage_file_path)
# gdf.set_index('id_indpu', inplace=True)
adj_pga_gdf = 0

for index, row in df.iterrows():
    site = df.loc[index, 'id_indpu']
    if type(adj_pga_gdf) != gpd.GeoDataFrame:
        adj_pga_gdf = gdf.loc[gdf['id_indpu'] == site]
        # adj_pga_gdf = adj_pga_gdf.merge(df, on='id_indpu', how='left')
    else:
        # adj_pga_gdf = adj_pga_gdf.merge(df, on='id_indpu', how='left')
        adj_pga_gdf = pd.concat([adj_pga_gdf, gdf.loc[gdf['id_indpu'] == site]])

adj_pga_gdf = adj_pga_gdf.merge(df, on='id_indpu', how='left')
adj_pga_gdf.to_file(fr'{export_file_path}\sporting goods adj pga {date}.gpkg')