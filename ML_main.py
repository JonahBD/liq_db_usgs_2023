from ML_functions import *
import pandas as pd
import numpy as np
import glob, os
from datetime import datetime

################ USER INPUTS ############################
input_folder_path_calculated_files = r"C:\Users\hf233\Documents\Italy\5. CPTU standard\calculated files\testing files"
export_folder_path = r"C:\Users\hf233\Documents\Italy\5. CPTU standard\Files from drive\ran tests"
#########################################################

# max_depth, site_of_max_depth  = finding_max_depth(input_folder_path_calculated_files)
# print(max_depth, site_of_max_depth)

df = create_monster_df(input_folder_path_calculated_files, "Depth (m)")



