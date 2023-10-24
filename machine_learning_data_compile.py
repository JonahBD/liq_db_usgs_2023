from ML_compile_functions import *
import pandas as pd
import numpy as np
import glob, os
from datetime import datetime

################ USER INPUTS ############################
american_date = True # True or False
input_folder_path = r"C:\Users\hf233\Documents\Italy\5. CPTU standard\Files from drive"
export_folder_path = r"C:\Users\hf233\Documents\Italy\5. CPTU standard\test files"
#########################################################

for files in glob.glob(os.path.join(input_folder_path, "*.xls*")):

    site = os.path.basename(filename).rstrip(".xls")
    print(site)
    df = pd.read_excel(filename)

    df = change_df(df)

print(df)
