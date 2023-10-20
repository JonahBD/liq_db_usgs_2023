from functions import *
import pandas as pd
import numpy as np
import glob, os
from datetime import datetime

missing_pga = []
preforo_below_GWT = []
nan_preforo = []

################ USER INPUTS ############################
american_date = True # True or False
input_folder_path = r"C:\Users\hf233\Documents\Italy\5. CPTU standard\Files from drive"
export_folder_path = r"C:\Users\hf233\Documents\Italy\5. CPTU standard\test files"
vals_pga_and_liq = r"C:\Users\hf233\Documents\Italy\pga.xlsx"
date_column_name = 'Date of CPT [gg/mm/aa]'
#########################################################

for filename in glob.glob(os.path.join(input_folder_path, "*.xls*")):

    site = os.path.basename(filename).rstrip(".xls")
    print(site)

    df = pd.read_excel(filename)
    date = df.loc[0][date_column_name]
    if american_date:
        if isinstance(date,pd.Timestamp):
            date = date.strftime('%m') + '/' + date.strftime('%d') + '/' + date.strftime('%Y')
    df.at[0, date_column_name] = pd.to_datetime(date, dayfirst=True)

    export_folder_path_df = os.path.join(export_folder_path,site + '.xlsx')

    df = soil_parameters(df)

    try:
        df = PGA_insertion(df,vals_pga_and_liq, site)
    except KeyError:
        print("This site is missing its PGA: " + site)
        missing_pga.append(site)
        continue

    preforo_checker = preforo_check(df, "GWT [m]", "preforo [m]")
    if preforo_checker == "GWT is above preforo":
        preforo_below_GWT.append(site)
    elif preforo_checker == "Nan preforo":
        nan_preforo.append(site)


    df = FS_liq(df, 6.1, 5.9)

    df = h1_h2_basic(df, 'Depth (m)','FS_20may')
    df = h1_h2_basic(df, 'Depth (m)', 'FS_29may')
    df = h1_h2_cumulative(df, 'Depth (m)', 'FS_20may')
    df = h1_h2_cumulative(df, 'Depth (m)', 'FS_29may')

    # print(df)

    df = LPI(df,"Depth (m)","FS_20may","20may")
    df = LPI(df,"Depth (m)","FS_29may","29may")

    df = LPIish(df, "Depth (m)", "FS_20may","20may", "h1_basic_20may")
    df = LPIish(df, "Depth (m)", "FS_20may", "20may", "h1_cumulative_20may")
    df = LPIish(df, "Depth (m)", "FS_29may", "29may", "h1_basic_29may")
    df = LPIish(df, "Depth (m)", "FS_29may", "29may", "h1_cumulative_29may")


    df = LSN(df, "Depth (m)", "qc1ncs", "FS_20may", "20may")
    df = LSN(df, "Depth (m)", "qc1ncs", "FS_29may", "29may")

    # Reorder the columns
    df = df[['Depth (m)', 'qc (MPa)', 'fs (kPa)', 'u (kPa)', 'qt (MPa)', "Rf (%)",
             "Gamma (kN/m^3)", "Total Stress (kPa)", "Effective Stress (kPa)", "Fr (%)", "Ic",
             'OCR R', 'OCR K', 'cu_bq', 'cu_14', "M", "k0_1", 'k0_2', "Vs R", 'Vs M', "k (m/s)", 'ψ', "φ' R",
             "φ' K", "φ' J", "φ' M", "φ' U", 'Dr B', 'Dr K', 'Dr J', 'Dr I', 'qc1n',"u calc","qc1ncs",'Kσ', 'rd_20may', 'rd_29may', "CSR_20may",
             "CRR_20may", 'CSR_29may', 'CRR_29may', "FS_20may", "FS_29may",'h1_basic_20may','h2_basic_20may','h1_basic_29may','h2_basic_29may',
             'h1_cumulative_20may','h2_cumulative_20may','h1_cumulative_29may','h2_cumulative_29may', "LPI_20may","LPI_29may","LPIish_20may","LPIish_29may",
             'LSN_20may', 'LSN_29may',
             "Unnamed: 5", 'GWT [m]', 'Date of CPT [gg/mm/aa]', 'u [si/no]', 'preforo [m]', 'PGA_20may', 'PGA_29may','Liquefaction']]

    df.to_excel(export_folder_path_df, index=False)

pga_df = pd.DataFrame({'Missing PGA sites':missing_pga})
preforo_df = pd.DataFrame({'Preforo is below GWT':preforo_below_GWT})
nan_preforo_df = pd.DataFrame({'nan preforo' : nan_preforo})
sites_to_check = pd.concat([pga_df, preforo_df,nan_preforo_df], axis=1)
export_folder_path_check_df = os.path.join(export_folder_path,'sites_to_check.xlsx')
sites_to_check.to_excel(export_folder_path_check_df, index=False)