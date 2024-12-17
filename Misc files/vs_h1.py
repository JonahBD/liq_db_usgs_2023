import pandas as pd
from functions import *
import numpy as np
import glob, os
from datetime import datetime
from tqdm import tqdm
import time
import warnings
warnings.filterwarnings("ignore", category=FutureWarning)

pd.set_option('future.no_silent_downcasting', True)

################ USER INPUTS ############################
input_folder_path = r"C:\Users\hf233\OneDrive - Brigham Young University\Liq\Italy Data\Attempt 08 - OG\OG Data\Soil Parameters"
export_folder_path = r"C:\Users\hf233\OneDrive - Brigham Young University\Liq\Italy Data\Attempt 08 - OG\OG Data"
depth_column_name = "Depth (m)"
#########################################################

# Sample DataFrame
sites = []
counter = 0
Vs_h1_df = pd.DataFrame()

for filename in glob.glob(os.path.join(input_folder_path, "*.xls*")):
    site = os.path.basename(filename).rstrip(".xls").lstrip("Copy of")
    sites.append(site)

loop = tqdm(total=(len(sites)))

for filename in glob.glob(os.path.join(input_folder_path, "*.xls*")):
    site = os.path.basename(filename).rstrip(".xls").lstrip("Copy of")
    # print(site)
    if site == "sites_to_check":
        continue
    loop.set_description(f"soil parameters - {site} :")

    df = pd.read_excel(filename)

    Vs_h1_df.at[counter, 'site'] = site
    h1_depth = df.loc[0, 'h1_basic']
    Vs_h1_df.at[counter, 'h1_thickness'] = h1_depth
    depths = df[depth_column_name].to_numpy()
    h1_index = int(np.where(depths == h1_depth)[0][0]) + 1
    # print(h1_index, h2_index)

    h1_depths_sliced = depths[0:h1_index]
    h1_first_depth_value = depths[0]
    h1_depth_offset = np.append(h1_first_depth_value, h1_depths_sliced)[:-1]
    h1_thickness = h1_depths_sliced - h1_depth_offset

    index_dict = {
        'h1': h1_index,
    }

    for col in ["Vs M (m/s)", "Vs R (m/s)"]:
        for (key, value) in index_dict.items():
            # print(col)
            values = df[col].to_numpy()
            sliced_values = values[0:h1_index]
            sliced_values[sliced_values < 0] = np.nan
            thickness = h1_thickness

            H_over_vs = np.divide(thickness, sliced_values)
            H_over_vs = H_over_vs[np.logical_not(np.isnan(H_over_vs))]
            Vs_h1_df.at[counter, str(key) + '_' + str(col)] = np.nanmedian(thickness) * len(H_over_vs) / (np.sum(H_over_vs))
            # print(np.nanmedian(thickness),len(H_over_vs), (np.sum(H_over_vs)))

            # sliced_values[sliced_values == ''] = np.nan
            Vs_h1_df.at[counter, str(key) + '_' + str(col) + "_mean"] = np.nanmean(sliced_values)
            # Vs_h1_df.at[counter, str(key) + '_' + str(col) + "_median"] = np.nanmedian(sliced_values)
            # Vs_h1_df.at[counter, str(key) + '_' + str(col) + "_std"] = np.nanstd(sliced_values)

    h1 = df.loc[0]['h1_basic']
    Vs_h1_df.at[counter, 'Max effective stress'] = df.loc[df[depth_column_name] == h1, 'Effective Stress (kPa)'].iloc[0]

    if counter == 30:
        Vs_h1_df.to_excel(fr"{export_folder_path}\Vs_h1_FIRST30.xlsx", index=False)
    counter += 1
    loop.update(1)
loop.close()

Vs_h1_df.to_excel(fr"{export_folder_path}\Vs_h1.xlsx", index=False)