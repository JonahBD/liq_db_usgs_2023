from ML_functions import *
import pandas as pd
import numpy as np
import glob, os
import scipy.stats
import time

# time.sleep(60*60*3.5)

################ USER INPUTS ############################
input_folder_path = r"C:\Users\jdundas2\OneDrive - Brigham Young University\Liq\Gabrelle update\Soil parameters 4-29"
export_folder_path = r'C:\Users\jdundas2\OneDrive - Brigham Young University\Liq\Gabrelle update'
depth_column_name = "Depth (m)"
date_of_creation = '04 05'
number_of_methods = 9
#########################################################

h1_parameters_col = ['k (m/s)']

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
    if df.loc[0, 'clay_profile'] == 1:
        loop.update(1)
        continue

    h1_parameters_df.at[counter, 'site'] = site
    h1_depth = df.loc[0, 'h1_basic']
    h1_parameters_df.at[counter, 'h1_thickness'] = h1_depth
    depths = df[depth_column_name].to_numpy()
    index = int(np.where(depths == h1_depth)[0][0])

    Ic = df['Ic'].to_numpy()
    # Ic = Ic[0:index]

    depths_sliced = depths[0:index]
    first_depth_value = depths[0]
    depth_offset = np.append(first_depth_value, depths_sliced)[:-1]
    thickness = depths_sliced - depth_offset

    for col in h1_parameters_col:
        # print(col)
        values = df[col].to_numpy()
        sliced_values = values[0:index]
        # print(col)
        H_over_k = np.divide(thickness, sliced_values)
        H_over_k = H_over_k[np.logical_not(np.isnan(H_over_k))]
        h1_parameters_df.at[counter, str(col) + "_equivalent"] = h1_depth / (np.sum(H_over_k))

    if counter == 30:
        h1_parameters_df.to_excel(f'{export_folder_path}\h1_k_parameter {date_of_creation}.xlsx', index=False)

    counter += 1
    loop.update(1)
loop.close()

h1_parameters_df.to_excel(f'{export_folder_path}\h1_k_parameters {date_of_creation}.xlsx', index=False)
