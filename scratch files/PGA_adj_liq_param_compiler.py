import pandas as pd
import glob, os
from tqdm import tqdm
import time
from datetime import date

# time.sleep(60*60*43)

################ USER INPUTS ############################
input_folder_path = r"C:\Users\jdundas2\OneDrive - Brigham Young University\Liq\Final Data\PGA adj"
export_folder_path = r"C:\Users\jdundas2\OneDrive - Brigham Young University\Liq\Final Data"
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

    site_characteristics = ['PGA', 'Liquefaction', 'GWT [m]', 'stratified', 'clay_profile',
                            'h1_basic', 'h1_cumulative', 'h2_basic', 'h2_cumulative', 'za', 'zb','LD', 'CR']

    methods = ['LPI', 'towhata_basic', 'towhata_cumulative', 'LPIish_basic', 'LPIish_cumulative', 'LSN',
               'ishihara_curve_basic', 'ishihara_curve_cumulative']

    # Columns to add to liq sheet
    liq_df.at[indx_counter, "site"] = site

    liq_df.at[indx_counter, 'EQ'] = df.loc[0, 'EQ']
    liq_df.at[indx_counter, 'EQ_mag'] = df.loc[1, 'EQ']

    for site_characteristic in site_characteristics:
        if site_characteristic == "PGA":
            if df.loc[1, site_characteristic] == "OG PGA below":
                liq_df.at[indx_counter, "OG PGA"] = df.loc[2, site_characteristic]
                liq_df.at[indx_counter, "New PGA"] = df.loc[0, site_characteristic]
                liq_df.at[indx_counter, "Diff PGA"] = df.loc[0, site_characteristic] - df.loc[2, site_characteristic]
                continue
            else:
                liq_df.at[indx_counter, "OG PGA"] = df.loc[0, site_characteristic]
                liq_df.at[indx_counter, "New PGA"] = float('Nan')
                liq_df.at[indx_counter, "Diff PGA"] = 0
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
    if indx_counter == 30:
        liq_df.to_excel(f'{export_folder_path}\_30_liq_param_compiled_PGA_adj_{date}.xlsx', index=False)
loop.close()

liq_df.to_excel(f'{export_folder_path}\liq_param_compiled_PGA_adj_{date}.xlsx', index=False)
