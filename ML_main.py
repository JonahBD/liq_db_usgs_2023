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

# max_depth, max_depth_site = finding_max_depth(input_folder_path)
# print(max_depth, max_depth_site)
max_depth = 'you mom'

df = pd.read_excel(glob.glob(os.path.join(input_folder_path, "*.xls*"))[0])
for column in df.columns:
    print(column, df.columns.get_loc(column))

columns = int(input('What columns do you want to include: '))
print(columns, type(columns))

df = create_monster_df(input_folder_path, depth_column_name, max_depth, depth_step)



