import pandas as pd
import glob, os
from tqdm import tqdm
import time
from datetime import date

# time.sleep(60*60*9)

################ USER INPUTS ############################
input_folder_path = r"C:\Users\jonah\OneDrive\BYU Onedrive\Liq\Italy Data\Attempt 08 - OG\OG Data\Soil Parameters"
export_folder_path = r"C:\Users\jonah\OneDrive\Finalized Liq Data"
name = "OG"
attempt_number = "A08"
adj_PGA = False
adj_GWT = False
#########################################################
today_date = date.today()
date = f'{today_date.month}-{today_date.day}'

sites = []
liq_df = pd.DataFrame()
indx_counter = 0
for filename in glob.glob(os.path.join(input_folder_path, "*.xls*")):
    site = os.path.basename(filename).rstrip(".xls")
    sites.append(site)

loop = tqdm(total=(len(sites)))

for filename in glob.glob(os.path.join(input_folder_path, "*.xls*")):
    site = os.path.basename(filename).rstrip(".xls")
    loop.set_description(f"Loading - {site} :")

    if site == "sites_to_check":
        continue

    df = pd.read_excel(filename)

    # if df.loc[0]['clay_profile'] == 1 and df.loc[0]['Liquefaction'] == 0:
    #     df.at[0, 'exclude'] = 1
    # else:
    #     df.at[0, 'exclude'] = 0 # TODO: delete this chunk later. The files i'm currently running don't have an exclude column, but the main.py files have been updated to calculate this there

    site_characteristics = ['PGA', 'Liquefaction', 'GWT [m]', 'lat_wgs84', 'lon_wgs84', 'stratified', 'clay_profile','exclude', 'h1b_sand_percent',
                            'h1_basic', 'h1_cumulative', 'h2_basic', 'h2_cumulative', 'methods_perform', 'za', 'zb','LD', 'CR']

    methods = ['LPI', 'towhata_basic', 'towhata_cumulative', 'LPIish_basic', 'LPIish_cumulative', 'LSN',
               'ishihara_curve_basic', 'ishihara_curve_cumulative']

    if adj_PGA:
        site_characteristics.insert(1, 'OG_PGA')
    if adj_GWT:
        site_characteristics.insert(3, "OG_GWT")

    # Columns to add to liq sheet
    liq_df.at[indx_counter, "site"] = site

    liq_df.at[indx_counter, 'EQ'] = df.loc[0, 'EQ']
    liq_df.at[indx_counter, 'EQ_mag'] = df.loc[1, 'EQ']

    for site_characteristic in site_characteristics:
        if site_characteristic == "OG_PGA":
            liq_df.at[indx_counter, site_characteristic] = df.loc[2, "PGA"]
            continue
        elif site_characteristic == "OG_GWT":
            liq_df.at[indx_counter, site_characteristic] = df.loc[2, "GWT [m]"]
            continue
        liq_df.at[indx_counter, site_characteristic] = df.loc[0, site_characteristic]

    liq_df.at[indx_counter, 'LD_and_CR_results'] = df.loc[0, 'LD_and_CR_results']

    for method in methods:
        if method == "ishihara_curve_basic" or method == 'ishihara_curve_cumulative':
            continue
        liq_df.at[indx_counter, method] = df.loc[0][method]

    liq_df.at[indx_counter, 'LD_and_CR_binary_results'] = df.loc[0, 'LD_and_CR_binary_results']

    for method_results in methods:
        liq_df.at[indx_counter, f'{method_results}_results'] = df.loc[0,f'{method_results}_results']

    indx_counter += 1
    loop.update(1)
    if indx_counter == 10:
        liq_df.to_excel(fr'{export_folder_path}\liq_param_compiled_{name}_{attempt_number}_first10.xlsx', index=False)
loop.close()

liq_df.to_excel(fr'{export_folder_path}\liq_param_compiled_{name}_{attempt_number}.xlsx', index=False)
