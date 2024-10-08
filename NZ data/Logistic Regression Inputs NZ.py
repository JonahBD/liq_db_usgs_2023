from ML_functions import *
import pandas as pd
import numpy as np
import glob, os
import scipy.stats
import time
from datetime import date
import warnings

warnings.filterwarnings("ignore", category=RuntimeWarning)

time.sleep(60*60*3)

################ USER INPUTS ############################
input_folder_path = r"C:\Users\jdundas2\OneDrive - Brigham Young University\Liq\NZ data\Attempt 04"
export_folder_path = input_folder_path
depth_column_name = "Depth (m)"
name_of_export_file = 'log_reg_parameters'
attempt_number = "A06"
folder_list = [f'soil_parameters_2010_{attempt_number}', f'soil_parameters_2011_{attempt_number}', f'soil_parameters_2016_{attempt_number}']
#########################################################
today_date = date.today()
date = f'{today_date.month}-{today_date.day}'

log_reg_site_parameters_col = ['Liquefaction', 'LSN', 'LPIish_basic',
                          'LPIish_cumulative', 'LPI', 'h2_basic',
                          'h2_cumulative', 'h1_basic', 'PGA', 'CR', 'LD', 'za', 'zb'] #'Liquefaction_italy',
log_reg_parameters_col = ['OCR R', 'OCR K', 'cu_bq (kPa)', 'cu_14 (kPa)', 'M (kPa)', 'Vs R (m/s)', 'Vs M (m/s)', 'k (m/s)', 'cu_HB (kPa)', 'Fines Content (%)', 'qc1ncs',
                     "φ' R (degrees)",
                     "φ' K (degrees)", "φ' J (degrees)", "φ' M (degrees)", "φ' U (degrees)", 'Dr B', 'Dr K', 'Dr J', 'Dr I', 'Ic', 'qc1n', 'Effective Stress (kPa)']


for folder in folder_list:
    sites = []
    
    for filename in glob.glob(os.path.join(f'{input_folder_path}\{folder}', "*.xls*")):
        site = os.path.basename(filename).rstrip(".xls")
        sites.append(site)
    
    loop = tqdm(total=len(sites), colour="#c6e2ff")
    
    counter = 0
    log_reg_parameters_df = pd.DataFrame()
    
    for filename in glob.glob(os.path.join(f'{input_folder_path}\{folder}', "*.xls*")):
        site = os.path.basename(filename).rstrip(".xls")
        loop.set_description(f"log_reg_parameters {folder} - {site} :")
    
        if site == "sites_to_check":
            continue
    
        df = pd.read_excel(filename)
        # if df.loc[0, 'clay_profile'] == 1:
        #     loop.update(1)
        #     continue
    
        log_reg_parameters_df.at[counter, 'site'] = site
        h1_depth = df.loc[0, 'h1_basic']
        h2_depth = df.loc[0, 'h2_basic'] + h1_depth
        log_reg_parameters_df.at[counter, 'h1_thickness'] = h1_depth
        depths = df[depth_column_name].to_numpy()
        h1_index = int(np.where(depths == h1_depth)[0][0])
        h2_index = int(np.argmin(np.abs(depths - h2_depth)))
        # print(h1_index, h2_index)
    
        log_reg_parameters_df.at[counter, 'stratified'] = df.loc[0, 'stratified']
        # print(type(index))
    
        Ic = df['Ic'].to_numpy()
        Ic = Ic[0:h1_index]
        sand = (Ic < 2.6).sum()
        clay = (Ic > 2.6).sum()
        sand_perc = sand / (sand + clay) * 100
        log_reg_parameters_df.at[counter, 'sand_percent'] = sand_perc
    
        h1_depths_sliced = depths[0:h1_index]
        h1_first_depth_value = depths[0]
        h1_depth_offset = np.append(h1_first_depth_value, h1_depths_sliced)[:-1]
        h1_thickness = h1_depths_sliced - h1_depth_offset
    
        h2_depths_sliced = depths[h1_index:h2_index]
        h2_first_depth_value = depths[0]
        h2_depth_offset = np.append(h2_first_depth_value, h2_depths_sliced)[:-1]
        h2_thickness = h2_depths_sliced - h2_depth_offset
    
        index_dict ={
            'h1': h1_index,
            'h2': h2_index,
        }
    
        for col in log_reg_parameters_col:
            for (key, value) in index_dict.items():
                # print(col)
                values = df[col].to_numpy()
                if value == h1_index:
                    sliced_values = values[0:h1_index]
                    thickness = h1_thickness
                else:
                    sliced_values = values[h1_index:h2_index]
                    thickness = h2_thickness
                # print(col)
                if str(col) == "k (m/s)":
                    H_over_k = np.divide(thickness, sliced_values)
                    H_over_k = H_over_k[np.logical_not(np.isnan(H_over_k))]
                    log_reg_parameters_df.at[counter, str(key) + '_' + str(col) + "_equivalent"] = h1_depth / (np.sum(H_over_k))
                log_reg_parameters_df.at[counter, str(key) + '_' + str(col) + "_mean"] = np.nanmean(sliced_values)
                log_reg_parameters_df.at[counter, str(key) + '_' + str(col) + "_median"] = np.nanmedian(sliced_values)
                log_reg_parameters_df.at[counter, str(key) + '_' + str(col) + "_std"] = np.nanstd(sliced_values)
                # log_reg_parameters_df.at[counter, str(key) + '_' + str(col) + "_skew"] = scipy.stats.skew(sliced_values, nan_policy='omit')
    
        for col in log_reg_site_parameters_col:
            log_reg_parameters_df.at[counter, str(col)] = df.loc[0, str(col)]
    
        if counter == 30:
            log_reg_parameters_df.to_excel(f'{export_folder_path}\{name_of_export_file}_{folder}.xlsx', index=False)
    
        counter += 1
        loop.update(1)
    loop.close()
    
    log_reg_parameters_df.to_excel(f'{export_folder_path}\{name_of_export_file}_{folder}.xlsx', index=False)
