from functions import *
import pandas as pd
import numpy as np
import glob, os
from datetime import datetime
from tqdm import tqdm

missing_pga = []
preforo_below_GWT = []
nan_preforo = []
missing_date = []
GWT_or_preforo_wrong_type = []
GWT_zero_nan = []
LD_not_working = []

################ USER INPUTS ############################
input_folder_path = r"C:\Users\jdundas2\OneDrive - Brigham Young University\Liq\Cliq settings changed\Step 5 our files"
export_folder_path = r"C:\Users\jdundas2\OneDrive - Brigham Young University\Liq\Cliq settings changed\soil parameters"
vals_pga_and_liq = r"C:\Users\jdundas2\Documents\PGA-liq values 02 13 23.xlsx"
date_column_name = 'Date of CPT [gg/mm/aa]'
depth_column_name = "Depth (m)"
#########################################################

sites = []

for filename in glob.glob(os.path.join(input_folder_path, "*.xls*")):
    site = os.path.basename(filename).rstrip(".xls").lstrip("Copy of")
    sites.append(site)

loop = tqdm(total=(len(sites)))

for filename in glob.glob(os.path.join(input_folder_path, "*.xls*")):
    site = os.path.basename(filename).rstrip(".xls").lstrip("Copy of")
    # print(site)
    loop.set_description(f"soil parameters - {site} :")

    df = pd.read_excel(filename)

    if df.loc[0]['GWT [m]'] == 0 or df.loc[0]['GWT [m]'] == float('NaN'):
        GWT_zero_nan.append(site)

    date = df.loc[0][date_column_name]
    if date == "-" or date == float('NaN'):
        date = float("NaN")
        missing_date.append(site)

    GWT = df.loc[0]['GWT [m]']
    if not isinstance(GWT, (int, float)):
        GWT_or_preforo_wrong_type.append(site)
        continue
    preforo = df.loc[0]["preforo [m]"]
    if not isinstance(preforo, (int, float)):
        GWT_or_preforo_wrong_type.append(site)
        continue

    if isinstance(date,pd.Timestamp):
        df.at[0, date_column_name] = date
    else:
        df.at[0, date_column_name] = pd.to_datetime(date, dayfirst=True)

    export_folder_path_df = os.path.join(export_folder_path,site + '.xlsx')

    df = soil_parameters(df, site)

    try:
        df = PGA_insertion(df,vals_pga_and_liq, site)
    except KeyError:
        # print("This site is missing its PGA: " + site)
        missing_pga.append(site)
        loop.update(1)
        continue

    preforo_checker = preforo_check(df, "GWT [m]", "preforo [m]")
    if preforo_checker == "GWT is above preforo":
        preforo_below_GWT.append(site)
    elif preforo_checker == "Nan preforo":
        nan_preforo.append(site)

    df = FS_liq(df)

    df = h1_h2_basic(df, depth_column_name, "FS")
    df = h1_h2_cumulative(df, depth_column_name, "FS")

    df = LPI(df, depth_column_name, "FS")
    df = LPI(df, depth_column_name, "FS")

    df = Towhata_2016(df, "LPI", "h1_basic")
    df = Towhata_2016(df, "LPI", "h1_cumulative")

    df = LPIish(df, depth_column_name, "FS", "h1_basic")
    df = LPIish(df, depth_column_name, "FS", "h1_cumulative")

    df = LSN(df, depth_column_name, "qc1ncs", "FS", GWT)

    df = ishihara_curves(df, 'basic')
    df = ishihara_curves(df, 'cumulative')

    df = LD_and_CR(df, "Ic", depth_column_name, "FS","Effective Stress (kPa)", "Total Stress (kPa)",'GWT [m]', 'Qtn', 'Fr (%)', 'qt calc')
    if df.loc[0]['LD_and_CR_result'] == 'Something went wrong':
        LD_not_working.append(site)
    # Reorder the columns
    df = df[[depth_column_name, 'qc (MPa)', 'fs (kPa)', 'u (kPa)', 'qt (MPa)', "Rf (%)",
             "Gamma (kN/m^3)", "Total Stress (kPa)", "Effective Stress (kPa)", "Fr (%)", "Ic",
             'OCR R', 'OCR K', 'cu_bq', 'cu_14', "M", "k0_1", 'k0_2', "Vs R", 'Vs M', "k (m/s)", 'ψ', "φ' R",
             "φ' K", "φ' J", "φ' M", "φ' U", 'Dr B', 'Dr K', 'Dr J', 'Dr I', 'qc1n',"u calc","qc1ncs", f'eps', 'Kσ', 'rd', "CSR",
             "CRR", "FS",'h1_basic','h2_basic','h1_cumulative','h2_cumulative', "LPI",
             f'towhata_basic', f'towhata_cumulative',"LPIish_basic", "LPIish_cumulative", 'LSN', 'LD', 'CR', 'za', 'zb',
             "Unnamed: 5", 'GWT [m]', 'Date of CPT [gg/mm/aa]', 'u [si/no]', 'preforo [m]', 'PGA',"EQ",'Liquefaction',
             'ishihara_curve_basic_result','ishihara_curve_cumulative_result', f'towhata_basic_results',
             f'towhata_cumulative_results',f'LSN_results', f'LPIish_basic_results', f'LPIish_cumulative_results',
             'LD_and_CR_result', 'LD_and_CR_binary_result', f'LPI_results']]

    df.to_excel(export_folder_path_df, index=False)
    loop.update(1)
loop.close()
pga_df = pd.DataFrame({'Missing PGA sites':missing_pga})
preforo_df = pd.DataFrame({'Preforo is below GWT':preforo_below_GWT})
nan_preforo_df = pd.DataFrame({'nan preforo' : nan_preforo})
missing_date_df = pd.DataFrame({'Missing Date':missing_date})
weird_GWT_preforo_df = pd.DataFrame({'GWT or preforo wrong type':GWT_or_preforo_wrong_type})
GWT_zero_nan_df = pd.DataFrame({'GWT zero or missing':GWT_zero_nan})
wrong_LD_df = pd.DataFrame({'LD is wrong': LD_not_working})
sites_to_check = pd.concat([pga_df, preforo_df,nan_preforo_df, missing_date_df,weird_GWT_preforo_df, wrong_LD_df], axis=1)
export_folder_path_check_df = os.path.join(export_folder_path,'sites_to_check.xlsx')
sites_to_check.to_excel(export_folder_path_check_df, index=False)