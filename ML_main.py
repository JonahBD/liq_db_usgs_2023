from ML_functions import *
import pandas as pd
import numpy as np
import glob, os
from datetime import datetime

################ USER INPUTS ############################
input_folder_path = r"C:\Users\hf233\Documents\Italy\5. CPTU standard\calculated files\testing files"
export_folder_path = r"C:\Users\hf233\Documents\Italy\5. CPTU standard\Files from drive\ran tests"
depth_column_name = "Depth (m)"
depth_step = 0.01 # in meters
#########################################################

# acceptable_list = False
# while acceptable_list == False:
#     acceptable_list, depth_step_selected_columns, one_col_selected_columns = user_input_columns(input_folder_path, depth_column_name, acceptable_list)

# print(depth_step_selected_columns, one_col_selected_columns)

depth_step_selected_columns = ['qc (MPa)', 'fs (kPa)', 'u (kPa)', 'qt (MPa)', 'Rf (%)', 'Gamma (kN/m^3)', 'Total Stress (kPa)', 'Effective Stress (kPa)', 'Fr (%)', 'Ic', 'OCR R', 'OCR K', 'cu_bq', 'cu_14', 'M', 'k0_1', 'k0_2', 'Vs R', 'Vs M', 'k (m/s)', 'ψ', "φ' R", "φ' K", "φ' J", "φ' M", "φ' U", 'Dr B', 'Dr K', 'Dr J', 'Dr I', 'qc1n', 'u calc', 'qc1ncs', 'Kσ', 'rd_20may', 'rd_29may', 'CSR_20may', 'CRR_20may', 'CSR_29may', 'CRR_29may', 'FS_20may', 'FS_29may']
one_col_selected_columns = ['h1_basic_20may', 'h2_basic_20may', 'h1_basic_29may', 'h2_basic_29may', 'h1_cumulative_20may', 'h2_cumulative_20may', 'h1_cumulative_29may', 'h2_cumulative_29may', 'LPI_20may', 'LPI_29may', 'LPIish_20may', 'LPIish_29may', 'LSN_20may', 'LSN_29may', 'Unnamed: 5', 'GWT [m]', 'Date of CPT [gg/mm/aa]', 'u [si/no]', 'preforo [m]', 'PGA_20may', 'PGA_29may', 'Liquefaction']
# max_depth, max_depth_site = finding_max_depth(input_folder_path)
# print(max_depth, max_depth_site)
max_depth = 50.01


df = create_monster_df(input_folder_path, depth_column_name, max_depth, depth_step, depth_step_selected_columns, one_col_selected_columns)



