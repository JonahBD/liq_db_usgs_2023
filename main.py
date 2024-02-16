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

################ USER INPUTS ############################
# american_date = True # True or False
input_folder_path = r"C:\Users\jdundas2\OneDrive - Brigham Young University\Liq\Gabrelle update\OG fiels no DMT - Copy"
export_folder_path = r"C:\Users\jdundas2\OneDrive - Brigham Young University\Liq\Gabrelle update\soil_parameters"
vals_pga_and_liq = r"C:\Users\jdundas2\Documents\PGA-liq values 02 13 23.xlsx"
date_column_name = 'Date of CPT [gg/mm/aa]'
depth_column_name = "Depth (m)"
date1 = "20may"
date2 = "29may"
#########################################################

FS1 = "FS_" + date1
FS2 = "FS_" + date2

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

    gwt = df.loc[0]['GWT [m]']
    if not isinstance(gwt, (int, float)):
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

    df = soil_parameters(df)

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

    df = FS_liq(df, 6.1, 5.9, date1, date2)

    df = h1_h2_basic(df, depth_column_name, FS1)
    df = h1_h2_basic(df, depth_column_name, FS2)
    df = h1_h2_cumulative(df, depth_column_name, FS1)
    df = h1_h2_cumulative(df, depth_column_name, FS2)

    df = LPI(df, depth_column_name, FS1, date1)
    df = LPI(df, depth_column_name, FS2, date2)

    df = Towhata_2016(df, "LPI_"+date1, "h1_basic_"+date1, date1)
    df = Towhata_2016(df, "LPI_" + date1, "h1_cumulative_" + date1, date1)
    df = Towhata_2016(df, "LPI_" + date2, "h1_basic_" + date2, date2)
    df = Towhata_2016(df, "LPI_" + date2, "h1_cumulative_" + date2, date2)

    df = LPIish(df, depth_column_name, FS1, date1, "h1_basic_"+date1)
    df = LPIish(df, depth_column_name, FS1, date1, "h1_cumulative_"+date1)
    df = LPIish(df, depth_column_name, FS2, date2, "h1_basic_"+date2)
    df = LPIish(df, depth_column_name, FS2, date2, "h1_cumulative_"+date2)

    df = LSN(df, depth_column_name, "qc1ncs", FS1, date1)
    df = LSN(df, depth_column_name, "qc1ncs", FS2, date2)

    # Reorder the columns
    df = df[[depth_column_name, 'qc (MPa)', 'fs (kPa)', 'u (kPa)', 'qt (MPa)', "Rf (%)",
             "Gamma (kN/m^3)", "Total Stress (kPa)", "Effective Stress (kPa)", "Fr (%)", "Ic",
             'OCR R', 'OCR K', 'cu_bq', 'cu_14', "M", "k0_1", 'k0_2', "Vs R", 'Vs M', "k (m/s)", 'ψ', "φ' R",
             "φ' K", "φ' J", "φ' M", "φ' U", 'Dr B', 'Dr K', 'Dr J', 'Dr I', 'qc1n',"u calc","qc1ncs", f'eps_{date1}', f'eps_{date2}', 'Kσ', 'rd_20may', 'rd_29may', "CSR_"+date1,
             "CRR_"+date1, 'CSR_'+date2, 'CRR_'+date2, "FS_"+date1, "FS_"+date2,'h1_basic_'+date1,'h2_basic_'+date1,'h1_basic_'+date2,'h2_basic_'+date2,
             'h1_cumulative_'+date1,'h2_cumulative_'+date1,'h1_cumulative_'+date2,'h2_cumulative_'+date2, "LPI_"+date1,"LPI_"+date2,
             f'towhata_basic_{date1}', f'towhata_cumulative_{date1}', f'towhata_basic_{date2}', f'towhata_cumulative_{date2}',
             "LPIish_basic_"+date1,"LPIish_basic_"+date2, "LPIish_cumulative_"+date1,"LPIish_cumulative_"+date2, 'LSN_'+date1, 'LSN_'+date2,
             "Unnamed: 5", 'GWT [m]', 'Date of CPT [gg/mm/aa]', 'u [si/no]', 'preforo [m]', 'PGA_'+date1, 'PGA_'+date2,'Liquefaction',
             f'towhata_basic_{date1}_results', f'towhata_basic_{date2}_results', f'towhata_cumulative_{date1}_results', f'towhata_cumulative_{date2}_results',
             f'LSN_{date1}_results', f'LSN_{date2}_results', f'LPIish_basic_{date1}_results', f'LPIish_basic_{date2}_results',
             f'LPIish_cumulative_{date1}_results', f'LPIish_cumulative_{date2}_results', f'LPI_{date1}_results', f'LPI_{date2}_results']]

    df.to_excel(export_folder_path_df, index=False)
    loop.update(1)
loop.close()
pga_df = pd.DataFrame({'Missing PGA sites':missing_pga})
preforo_df = pd.DataFrame({'Preforo is below GWT':preforo_below_GWT})
nan_preforo_df = pd.DataFrame({'nan preforo' : nan_preforo})
missing_date_df = pd.DataFrame({'Missing Date':missing_date})
weird_gwt_preforo_df = pd.DataFrame({'gwt or preforo wrong type':GWT_or_preforo_wrong_type})
GWT_zero_nan_df = pd.DataFrame({'GWT zero or missing':GWT_zero_nan})
sites_to_check = pd.concat([pga_df, preforo_df,nan_preforo_df, missing_date_df,weird_gwt_preforo_df], axis=1)
export_folder_path_check_df = os.path.join(export_folder_path,'sites_to_check.xlsx')
sites_to_check.to_excel(export_folder_path_check_df, index=False)