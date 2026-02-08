from functions import *
import pandas as pd
import glob, os

df_length = []
depth_step = []
site_list = []

folder_path = r"C:\Users\jdundas2\Documents\5. 10 20 23 CPTU standard excel (1685 items)"
for filename in glob.glob(os.path.join(folder_path, "*.xls*")):
    site = os.path.basename(filename).rstrip(".xls")
    site_list.append(site)
    df = pd.read_excel(filename)
    df_length.append(df.shape[0])
    middle = int(df.shape[0]/2)
    before_middle = int(middle - 1)
    depth_step.append(df.iloc[middle]["Depth (m)"]-df.iloc[before_middle]['Depth (m)'])
outputs = pd.DataFrame({'site':site_list,'df_length':df_length, 'depth_step':depth_step})
outputs.to_excel(r'C:\Users\jdundas2\Documents\ML_parameters.xlsx', index=False)
