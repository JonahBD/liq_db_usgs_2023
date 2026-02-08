from ML_functions import *
from functions import *
import pandas as pd
import glob, os
from tqdm import tqdm

missing_pga = []
preforo_below_GWT = []
nan_preforo = []

################ USER INPUTS ############################
american_date = True # True or False
input_folder_path = r"C:\Users\jdundas2\Documents\testing\og files"
export_folder_path = r"C:\Users\jdundas2\Documents\testing\soil parameters"
sites_to_check_folder_path = r"C:\Users\jdundas2\Documents\testing"
vals_pga_and_liq = r"C:\Users\jdundas2\Documents\all current sites.xlsx"
date_column_name = 'Date of CPT [gg/mm/aa]'
depth_column_name = "Depth (m)"
date1 = "20may"
date2 = "29may"
#########################################################

FS1 = "FS_" + date1
FS2 = "FS_" + date2

sites = []

for filename in glob.glob(os.path.join(input_folder_path, "*.xls*")):
    site = os.path.basename(filename).rstrip(".xls")
    sites.append(site)

loop = tqdm(total=(len(sites)))

for filename in glob.glob(os.path.join(input_folder_path, "*.xls*")):
    site = os.path.basename(filename).rstrip(".xls")
    # print(site)
    loop.set_description(f"soil parameters - {site} :")

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

    df.at[0, f'towhata_basic_{date1}'] = Towhata_2016(df, "LPI_"+date1, "h1_basic_"+date1)
    df.at[0, f'towhata_cumulative_{date1}'] = Towhata_2016(df, "LPI_" + date1, "h1_cumulative_" + date1)
    df.at[0, f'towhata_basic_{date2}'] = Towhata_2016(df, "LPI_" + date2, "h1_basic_" + date2)
    df.at[0, f'towhata_cumulative_{date2}'] = Towhata_2016(df, "LPI_" + date2, "h1_cumulative_" + date2)

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
             "φ' K", "φ' J", "φ' M", "φ' U", 'Dr B', 'Dr K', 'Dr J', 'Dr I', 'qc1n',"u calc","qc1ncs",'Kσ', 'rd_20may', 'rd_29may', "CSR_"+date1,
             "CRR_"+date1, 'CSR_'+date2, 'CRR_'+date2, "FS_"+date1, "FS_"+date2,'h1_basic_'+date1,'h2_basic_'+date1,'h1_basic_'+date2,'h2_basic_'+date2,
             'h1_cumulative_'+date1,'h2_cumulative_'+date1,'h1_cumulative_'+date2,'h2_cumulative_'+date2, "LPI_"+date1,"LPI_"+date2,
             f'towhata_basic_{date1}', f'towhata_cumulative_{date1}', f'towhata_basic_{date2}', f'towhata_cumulative_{date2}',
             "LPIish_"+date1,"LPIish_"+date2, 'LSN_'+date1, 'LSN_'+date2,
             "Unnamed: 5", 'GWT [m]', 'Date of CPT [gg/mm/aa]', 'u [si/no]', 'preforo [m]', 'PGA_'+date1, 'PGA_'+date2,'Liquefaction']] #TODO: should we move date to the end so that it's easy to take out for the ML model code?

    df.to_excel(export_folder_path_df, index=False)
    loop.update(1)
loop.close()

pga_df = pd.DataFrame({'Missing PGA sites':missing_pga})
preforo_df = pd.DataFrame({'Preforo is below GWT':preforo_below_GWT})
nan_preforo_df = pd.DataFrame({'nan preforo' : nan_preforo})
sites_to_check = pd.concat([pga_df, preforo_df,nan_preforo_df], axis=1)
export_folder_path_check_df = os.path.join(sites_to_check_folder_path,'sites_to_check.xlsx')
sites_to_check.to_excel(export_folder_path_check_df, index=False)


################ USER INPUTS ############################
input_folder_path = r"C:\Users\jdundas2\Documents\testing\soil parameters"
export_folder_path = r"C:\Users\jdundas2\Documents\testing"
depth_column_name = "Depth (m)"
depth_step = 0.01 # in meters
#########################################################

# acceptable_list_confirmation = False
# while acceptable_list_confirmation == False:
#     acceptable_list_confirmation, depth_step_selected_columns, one_row_selected_columns = user_input_columns(input_folder_path, depth_column_name, acceptable_list_confirmation)

# print(depth_step_selected_columns, one_col_selected_columns)

depth_step_selected_columns = ['qc (MPa)', 'fs (kPa)', 'u (kPa)', 'qt (MPa)', 'Rf (%)', 'Gamma (kN/m^3)', 'Total Stress (kPa)', 'Effective Stress (kPa)', 'Fr (%)', 'Ic', 'OCR R', 'OCR K', 'cu_bq', 'cu_14', 'M', 'k0_1', 'k0_2', 'Vs R', 'Vs M', 'k (m/s)', 'ψ', "φ' R", "φ' K", "φ' J", "φ' M", "φ' U", 'Dr B', 'Dr K', 'Dr J', 'Dr I', 'qc1n', 'u calc', 'qc1ncs', 'Kσ', 'rd_20may', 'rd_29may', 'CSR_20may', 'CRR_20may', 'CSR_29may', 'CRR_29may', 'FS_20may', 'FS_29may']
one_row_selected_columns = ['h1_basic_20may', 'h2_basic_20may', 'h1_basic_29may', 'h2_basic_29may', 'h1_cumulative_20may', 'h2_cumulative_20may', 'h1_cumulative_29may', 'h2_cumulative_29may', 'LPI_20may', 'LPI_29may', 'LPIish_20may', 'LPIish_29may', 'LSN_20may', 'LSN_29may', 'Liquefaction']
max_depth, max_depth_site = finding_max_depth(input_folder_path, depth_column_name)
# print(max_depth, max_depth_site)
# max_depth = 40


df, depth_step_columns, target_depths = create_monster_df(max_depth, depth_step, depth_step_selected_columns, one_row_selected_columns)
df = fill_monster_df(input_folder_path, df, depth_step_selected_columns, target_depths, depth_column_name, one_row_selected_columns)
df.to_csv(export_folder_path+"\monster.csv")


