import pandas as pd
import geopandas as gpd

# time.sleep(6*3600)

list_of_methods = ['LPI', 'towhata_basic', 'towhata_cumulative', 'LPIish_basic', 'LPIish_cumulative', 'LSN', 'LD_and_CR', 'ishihara_curve_basic', 'ishihara_curve_cumulative']

################ USER INPUTS ############################
parameter_file_path = r"C:\Users\jdundas2\OneDrive - Brigham Young University\Liq\Gabrelle update\liq_param_compiled 03 25.xlsx"
geopackage_file_path = r"C:\Users\jdundas2\OneDrive - Brigham Young University\Liq\master cpt attribute table.xlsx.gpkg"
export_file_path = r"C:\Users\jdundas2\OneDrive - Brigham Young University\Liq\results geopackages"
#########################################################

df = pd.read_excel(parameter_file_path)
gdf = gpd.read_file(geopackage_file_path)
# gdf.set_index('id_indpu', inplace=True)

for method in list_of_methods:
    true_negative = 0
    false_negative = 0
    true_positive = 0
    false_positive = 0
    for column in df.columns[1:]:
        if str(method)+"_results" in column:
            print(str(method)+"_results", column)
            for index, row in df.iterrows():
                our_val = row[column]
                liq_val = row["Liquefaction"]
                if liq_val == 0 and our_val == 0: # true_negative
                    if type(true_negative) != gpd.GeoDataFrame:
                        true_negative = gdf.loc[gdf['id_indpu'] == df.loc[index, 'site']]
                    else:
                        true_negative = pd.concat([true_negative, gdf.loc[gdf['id_indpu'] == df.loc[index, 'site']]])
                elif liq_val == 1 and our_val == 0: # false negative
                    if type(false_negative) != gpd.GeoDataFrame:
                        false_negative = gdf.loc[gdf['id_indpu'] == df.loc[index, 'site']]
                    else:
                        false_negative = pd.concat([false_negative, gdf.loc[gdf['id_indpu'] == df.loc[index, 'site']]])
                elif liq_val == 1 and our_val == 1: # true positive
                    if type(true_positive) != gpd.GeoDataFrame:
                        true_positive = gdf.loc[gdf['id_indpu'] == df.loc[index, 'site']]
                    else:
                        true_positive = pd.concat([true_positive, gdf.loc[gdf['id_indpu'] == df.loc[index, 'site']]])
                elif liq_val == 0 and our_val == 1: # false positive
                    if type(false_positive) != gpd.GeoDataFrame:
                        false_positive = gdf.loc[gdf['id_indpu'] == df.loc[index, 'site']]
                    else:
                        false_positive = pd.concat([false_positive, gdf.loc[gdf['id_indpu'] == df.loc[index, 'site']]])

    true_negative.to_file(fr'{export_file_path}\{method}_true_negative.gpkg')
    false_negative.to_file(fr'{export_file_path}\{method}_false_negative.gpkg')
    true_positive.to_file(fr'{export_file_path}\{method}_true_positive.gpkg')
    false_positive.to_file(fr'{export_file_path}\{method}_false_positive.gpkg')
