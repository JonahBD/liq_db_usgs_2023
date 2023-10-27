from ML_functions import *
import pandas as pd
import numpy as np
import glob, os
from datetime import datetime

################ USER INPUTS ############################
input_folder_path = r"C:\Users\jdundas2\Documents\Step 5 downloads\testing_finished"
export_folder_path = r"C:\Users\hf233\Documents\Italy\5. CPTU standard\Files from drive\ran tests"
depth_column_name = "Depth (m)"
depth_step = 0.01 # in meters
#########################################################
acceptable_list = False
while acceptable_list == False:
    acceptable_list, depth_step_selected_columns, one_col_selected_columns = user_input_columns(input_folder_path, depth_column_name, acceptable_list)

print(depth_step_selected_columns, one_col_selected_columns)

# max_depth, max_depth_site = finding_max_depth(input_folder_path)
# print(max_depth, max_depth_site)
max_depth = 'you mom'


# df = create_monster_df(input_folder_path, depth_column_name, max_depth, depth_step)



