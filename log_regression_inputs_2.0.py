from ML_functions import *
import pandas as pd
import numpy as np
import glob, os
import scipy.stats
import time
from datetime import date
from tqdm import tqdm
import warnings

warnings.filterwarnings("ignore", category=RuntimeWarning)

################ USER INPUTS ############################
input_folder_path = r"C:\Users\jonah\OneDrive\BYU Onedrive\Liq\Italy Data\Attempt 08 - OG\OG Data\Soil Parameters"
export_folder_path = r"C:\Users\jonah\OneDrive\Finalized Liq Data"
depth_column_name = "Depth (m)"
name = "OG"
attempt_number = "A08"
#########################################################

today_date = date.today()
date_str = f'{today_date.month}-{today_date.day}'

pca_site_parameters_col = [
    'Liquefaction', 'LSN', 'LPIish_basic', 'LPIish_cumulative', 'LPI',
    'h2_basic', 'h2_cumulative', 'h1_basic', 'PGA', 'CR', 'LD',
    'za', 'zb', 'clay_profile', 'exclude'
]

# >>> CHANGED: removed Vs columns from this list; we'll compute Vs means separately <<<
pca_parameters_col = [
    'OCR R', 'OCR K', 'cu_bq (kPa)', 'cu_14 (kPa)', 'M (kPa)',
    'k (m/s)', 'cu_HB (kPa)', 'Fines Content (%)', 'qc1ncs',
    "φ' R (degrees)", "φ' K (degrees)", "φ' J (degrees)", "φ' M (degrees)", "φ' U (degrees)",
    'Dr B', 'Dr K', 'Dr J', 'Dr I', 'Ic', 'qc1n', 'Effective Stress (kPa)',
    'CSR', "CRR", "Volumetric Strain (%)", 'k0_1', 'k0_2', 'ψ', 'Factor of Safety'
]

# >>> ADDED: list of Vs columns to compute means using second script's approach <<<
vs_cols = ["Vs M (m/s)", "Vs R (m/s)"]

sites = []
for filename in glob.glob(os.path.join(input_folder_path, "*.xls*")):
    site = os.path.basename(filename).rstrip(".xls")
    sites.append(site)

loop = tqdm(total=len(sites), colour="#c6e2ff")

counter = 0
pca_parameters_df = pd.DataFrame()

for filename in glob.glob(os.path.join(input_folder_path, "*.xls*")):
    site = os.path.basename(filename).rstrip(".xls")
    loop.set_description(f"pca_parameters - {site} :")

    if site == "sites_to_check":
        continue

    df = pd.read_excel(filename)

    pca_parameters_df.at[counter, 'site'] = site

    # depths / layer boundaries
    h1_depth = df.loc[0, 'h1_basic']
    h2_depth = df.loc[0, 'h2_basic'] + h1_depth
    pca_parameters_df.at[counter, 'h1_thickness'] = h1_depth

    # >>> CHANGED (minor): coerce depths to numeric for consistency/robustness <<<
    depths = pd.to_numeric(df[depth_column_name], errors='coerce').to_numpy(dtype=float)

    # keep your original indexing behavior
    h1_index = int(np.where(depths == h1_depth)[0][0])
    h2_index = int(np.argmin(np.abs(depths - h2_depth)))

    pca_parameters_df.at[counter, 'stratified'] = df.loc[0, 'stratified']

    # sand percent
    Ic = pd.to_numeric(df['Ic'], errors='coerce').to_numpy(dtype=float)
    Ic = Ic[0:h1_index]
    sand = (Ic < 2.6).sum()
    clay = (Ic > 2.6).sum()
    sand_perc = sand / (sand + clay) * 100 if (sand + clay) > 0 else np.nan
    pca_parameters_df.at[counter, 'sand_percent'] = sand_perc

    # thickness arrays (unchanged)
    h1_depths_sliced = depths[0:h1_index]
    h1_first_depth_value = depths[0]
    h1_depth_offset = np.append(h1_first_depth_value, h1_depths_sliced)[:-1]
    h1_thickness = h1_depths_sliced - h1_depth_offset

    h2_depths_sliced = depths[h1_index:h2_index]
    h2_first_depth_value = depths[0]
    h2_depth_offset = np.append(h2_first_depth_value, h2_depths_sliced)[:-1]
    h2_thickness = h2_depths_sliced - h2_depth_offset

    index_dict = {
        'h1': h1_index,
        'h2': h2_index,
    }

    # ----------------------------------------------------
    # MAIN PARAMETER LOOP (MEDIANS) - same as before
    # ----------------------------------------------------
    for col in pca_parameters_col:
        for (key, value) in index_dict.items():
            values = pd.to_numeric(df[col], errors='coerce').to_numpy(dtype=float)

            if value == h1_index and key != 'h2':
                sliced_values = values[0:h1_index].copy()
                thickness = h1_thickness
            else:
                sliced_values = values[h1_index:h2_index].copy()
                thickness = h2_thickness

            # Hydraulic conductivity special case (unchanged)
            if col == "k (m/s)":
                H_over_k = thickness / sliced_values
                H_over_k = H_over_k[~np.isnan(H_over_k)]
                if len(H_over_k) > 0:
                    pca_parameters_df.at[counter, f"{key}_{col}_equivalent"] = h1_depth / np.sum(H_over_k)
                else:
                    pca_parameters_df.at[counter, f"{key}_{col}_equivalent"] = np.nan

            if h1_index == h2_index and key == 'h2':
                pca_parameters_df.at[counter, f"{key}_{col}_median"] = np.nan
            else:
                pca_parameters_df.at[counter, f"{key}_{col}_median"] = np.nanmedian(sliced_values)

    # ----------------------------------------------------
    # >>> ADDED: UPDATED Vs MEANS (NO EQUIVALENT Vs) <<<
    # Uses: pd.to_numeric + (<0 => NaN) + np.nanmean, like your second script
    # ----------------------------------------------------
    for col in vs_cols:
        values = pd.to_numeric(df[col], errors='coerce').to_numpy(dtype=float, copy=True)
        values[values < 0] = np.nan  # <<< ADDED: throw out bad Vs values exactly like code #2

        # h1 mean
        h1_vals = values[0:h1_index+1].copy()
        pca_parameters_df.at[counter, f"h1_{col}_mean"] = np.nanmean(h1_vals)

        # h2 mean (only if h2 exists)
        if h1_index == h2_index:
            pca_parameters_df.at[counter, f"h2_{col}_mean"] = np.nan
        else:
            h2_vals = values[h1_index+1:h2_index+1].copy()
            pca_parameters_df.at[counter, f"h2_{col}_mean"] = np.nanmean(h2_vals)

    # ----------------------------------------------------
    # >>> ADDED: EXTRA FROM SECOND CODE: Max effective stress at h1 depth <<<
    # ----------------------------------------------------
    eff = df.loc[df[depth_column_name] == h1_depth, 'Effective Stress (kPa)']
    pca_parameters_df.at[counter, 'Max effective stress'] = eff.iloc[0] if len(eff) else np.nan

    # site-level cols (unchanged)
    for col in pca_site_parameters_col:
        pca_parameters_df.at[counter, str(col)] = df.loc[0, str(col)]

    if counter == 30:
        pca_parameters_df.to_excel(
            fr'{export_folder_path}\log_reg_parameters_{name}_{attempt_number}_first30.xlsx',
            index=False
        )

    counter += 1
    loop.update(1)

loop.close()

pca_parameters_df.to_excel(
    fr'{export_folder_path}\log_reg_parameters_{name}_{attempt_number}.xlsx',
    index=False
)