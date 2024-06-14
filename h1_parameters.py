from ML_functions import *
import pandas as pd
import numpy as np
import glob, os
import scipy.stats
import time
from datetime import date
import warnings

warnings.filterwarnings("ignore", category=RuntimeWarning)

# time.sleep(60*60*3.5)

################ USER INPUTS ############################
input_folder_path = r"C:\Users\jdundas2\OneDrive - Brigham Young University\Liq\Gabrelle update\Soil parameters 4-29"
export_folder_path = r'C:\Users\jdundas2\OneDrive - Brigham Young University\Liq\Gabrelle update'
depth_column_name = "Depth (m)"
number_of_methods = 9
name_of_export_file = 'h1_parameters_all_sites'
#########################################################
today_date = date.today()
date = f'{today_date.month}-{today_date.day}'
print(date)

h1_site_parameters_col = ['Liquefaction', 'ishihara_curve_basic_results',
                          'ishihara_curve_cumulative_results', 'towhata_basic_results',
                          'towhata_cumulative_results', 'LSN_results', 'LPIish_basic_results',
                          'LPIish_cumulative_results', 'LD_and_CR_binary_results', 'LPI_results', 'h2_basic',
                          'h2_cumulative'] #'Liquefaction_italy',
h1_parameters_col = ['OCR R', 'OCR K', 'cu_bq', 'cu_14', 'M', 'Vs R', 'Vs M', 'k (m/s)', 'su_HB', 'FC', 'qc1ncs',
                     "φ' R",
                     "φ' K", "φ' J", "φ' M", "φ' U", 'Dr B', 'Dr K', 'Dr J', 'Dr I', 'Ic']

sites = []

for filename in glob.glob(os.path.join(input_folder_path, "*.xls*")):
    site = os.path.basename(filename).rstrip(".xls")
    sites.append(site)

loop = tqdm(total=len(sites), colour="#c6e2ff")

counter = 0
h1_parameters_df = pd.DataFrame()

for filename in glob.glob(os.path.join(input_folder_path, "*.xls*")):
    site = os.path.basename(filename).rstrip(".xls")
    loop.set_description(f"h1_parameters - {site} :")

    if site == "sites_to_check":
        continue

    df = pd.read_excel(filename)
    # if df.loc[0, 'clay_profile'] == 1:
    #     loop.update(1)
    #     continue

    h1_parameters_df.at[counter, 'site'] = site
    h1_depth = df.loc[0, 'h1_basic']
    h1_parameters_df.at[counter, 'h1_thickness'] = h1_depth
    depths = df[depth_column_name].to_numpy()
    index = int(np.where(depths == h1_depth)[0][0])
    h1_parameters_df.at[counter, 'stratified'] = df.loc[0, 'stratified']
    # print(type(index))

    Ic = df['Ic'].to_numpy()
    Ic = Ic[0:index]
    sand = (Ic < 2.6).sum()
    clay = (Ic > 2.6).sum()
    sand_perc = sand / (sand + clay) * 100
    h1_parameters_df.at[counter, 'sand_percent'] = sand_perc

    depths_sliced = depths[0:index]
    first_depth_value = depths[0]
    depth_offset = np.append(first_depth_value, depths_sliced)[:-1]
    thickness = depths_sliced - depth_offset

    for col in h1_parameters_col:
        # print(col)
        values = df[col].to_numpy()
        sliced_values = values[0:index]
        # print(col)
        if str(col) == "k (m/s)":
            H_over_k = np.divide(thickness, sliced_values)
            H_over_k = H_over_k[np.logical_not(np.isnan(H_over_k))]
            h1_parameters_df.at[counter, str(col) + "_equivalent"] = h1_depth / (np.sum(H_over_k))
        h1_parameters_df.at[counter, str(col) + "_mean"] = np.nanmean(sliced_values)
        h1_parameters_df.at[counter, str(col) + "_median"] = np.nanmedian(sliced_values)
        h1_parameters_df.at[counter, str(col) + "_std"] = np.nanstd(sliced_values)
        h1_parameters_df.at[counter, str(col) + "_skew"] = scipy.stats.skew(sliced_values, nan_policy='omit')

    for col in h1_site_parameters_col:
        h1_parameters_df.at[counter, str(col)] = df.loc[0, str(col)]

    sum_performance = 0
    for method in h1_site_parameters_col:
        if method in ['Liquefaction', 'h2_basic', 'h2_cumulative']:
            continue
        if h1_parameters_df.loc[counter, 'Liquefaction'] == 1: #liq sites
            sum_performance += h1_parameters_df.loc[counter, method]
            methods_performance = sum_performance / number_of_methods
            h1_parameters_df.at[counter, 'methods_perform'] = methods_performance

            if methods_performance == 0:
                h1_parameters_df.at[counter, 'methods_perform'] = 2

        else: #Non liq sites
            sum_performance += h1_parameters_df.loc[counter, method]
            methods_performance = (number_of_methods - sum_performance) / number_of_methods * -1
            h1_parameters_df.at[counter, 'methods_perform'] = methods_performance

            if methods_performance == 0:
                h1_parameters_df.at[counter, 'methods_perform'] = -2


    if counter == 30:
        h1_parameters_df.to_excel(f'{export_folder_path}\{name_of_export_file} {date}.xlsx', index=False)

    counter += 1
    loop.update(1)
loop.close()

h1_parameters_df.to_excel(f'{export_folder_path}\{name_of_export_file} {date}.xlsx', index=False)
