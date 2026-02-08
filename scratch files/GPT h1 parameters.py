from ML_functions import *
import pandas as pd
import numpy as np
import glob, os
import scipy.stats
import time
from tqdm import tqdm
from joblib import Parallel, delayed

# time.sleep(60*60*3.5)

################ USER INPUTS ############################
input_folder_path = r"C:\Users\jdundas2\OneDrive - Brigham Young University\Liq\Gabrelle update\Soil parameters 4 5"
export_folder_path = r'C:\Users\jdundas2\OneDrive - Brigham Young University\Liq\Gabrelle update'
depth_column_name = "Depth (m)"
date_of_creation = '04 05'
#########################################################

h1_site_parameters_col = ['Liquefaction', 'ishihara_curve_basic_results',
                          'ishihara_curve_cumulative_results', 'towhata_basic_results',
                          'towhata_cumulative_results', 'LSN_results', 'LPIish_basic_results',
                          'LPIish_cumulative_results', 'LD_and_CR_binary_results', 'LPI_results']
h1_parameters_col = ['OCR R', 'OCR K', 'cu_bq', 'cu_14', 'M', 'Vs R', 'Vs M', 'k (m/s)', 'su_HB', 'FC', 'qc1ncs',
                     "φ' R",
                     "φ' K", "φ' J", "φ' M", "φ' U", 'Dr B', 'Dr K', 'Dr J', 'Dr I']


def process_site(filename):
    site = os.path.basename(filename).rstrip(".xls")
    if site == "sites_to_check":
        return None

    df = pd.read_excel(filename)
    if df.loc[0, 'clay_profile'] == 1:
        return None

    h1_parameters = {}
    h1_parameters['site'] = site
    h1_depth = df.loc[0, 'h1_basic']
    h1_parameters['h1_thickness'] = h1_depth
    depths = df[depth_column_name].to_numpy()
    index = int(np.where(depths == h1_depth)[0][0])
    h1_parameters['stratified'] = df.loc[0, 'stratified']

    Ic = df['Ic'].to_numpy()
    Ic = Ic[0:index]
    sand = (Ic < 2.6).sum()
    clay = (Ic > 2.6).sum()
    sand_perc = sand / (sand + clay) * 100
    h1_parameters['sand_percent'] = sand_perc

    for col in h1_parameters_col:
        values = df[col].to_numpy()
        sliced_values = values[0:index]
        h1_parameters[str(col) + "_mean"] = np.nanmean(sliced_values)
        h1_parameters[str(col) + "_median"] = np.nanmedian(sliced_values)
        h1_parameters[str(col) + "_std"] = np.nanstd(sliced_values)
        h1_parameters[str(col) + "_skew"] = scipy.stats.skew(sliced_values, nan_policy='omit')

    for col in h1_site_parameters_col:
        h1_parameters[str(col)] = df.loc[0, str(col)]

    return h1_parameters


sites_filenames = glob.glob(os.path.join(input_folder_path, "*.xls*"))

# Process sites in parallel
processed_sites = Parallel(n_jobs=-1)(
    delayed(process_site)(filename) for filename in tqdm(sites_filenames, desc="Processing Sites"))

# Filter out None values and create DataFrame
h1_parameters_df = pd.DataFrame([site for site in processed_sites if site is not None])

# Export DataFrame to Excel
h1_parameters_df.to_excel(f'{export_folder_path}\h1_parameters {date_of_creation}.xlsx', index=False)