from ML_functions import *
import pandas as pd
import numpy as np
import glob, os
from datetime import datetime

################ USER INPUTS ############################
input_folder_path = r"C:\Users\jdundas2\Documents\Fully ran code 11 06 23\soil parameters"
export_folder_path = r"C:\Users\jdundas2\Documents\Fully ran code 11 06 23"
depth_column_name = "Depth (m)"
depth_step = 0.01 # in meters
#########################################################

# acceptable_list_confirmation = False
# while acceptable_list_confirmation == False:
#     acceptable_list_confirmation, depth_step_selected_columns, one_row_selected_columns = user_input_columns(input_folder_path, depth_column_name, acceptable_list_confirmation)

# print(depth_step_selected_columns, one_col_selected_columns)

depth_step_selected_columns = ['qc (MPa)', 'fs (kPa)', 'u (kPa)', 'qt (MPa)', 'Rf (%)', 'Gamma (kN/m^3)', 'Total Stress (kPa)', 'Effective Stress (kPa)', 'Fr (%)', 'Ic', 'OCR R', 'OCR K', 'cu_bq', 'cu_14', 'M', 'k0_1', 'k0_2', 'Vs R', 'Vs M', 'k (m/s)', 'ψ', "φ' R", "φ' K", "φ' J", "φ' M", "φ' U", 'Dr B', 'Dr K', 'Dr J', 'Dr I', 'qc1n', 'u calc', 'qc1ncs', 'Kσ', 'rd_20may', 'rd_29may', 'CSR_20may', 'CRR_20may', 'CSR_29may', 'CRR_29may', 'FS_20may', 'FS_29may']
one_row_selected_columns = ['h1_basic_20may', 'h2_basic_20may', 'h1_basic_29may', 'h2_basic_29may', 'h1_cumulative_20may', 'h2_cumulative_20may', 'h1_cumulative_29may', 'h2_cumulative_29may', 'LPI_20may', 'LPI_29may', 'LPIish_20may', 'LPIish_29may', 'LSN_20may', 'LSN_29may', 'Liquefaction']
# max_depth, max_depth_site = finding_max_depth(input_folder_path, depth_column_name)
# print(max_depth, max_depth_site)
max_depth = 40


df, depth_step_columns, target_depths = create_monster_df(max_depth, depth_step, depth_step_selected_columns, one_row_selected_columns)
df = fill_monster_df(input_folder_path, df, depth_step_selected_columns, target_depths, depth_column_name, one_row_selected_columns)
df.to_csv(export_folder_path+"\monster.csv")


