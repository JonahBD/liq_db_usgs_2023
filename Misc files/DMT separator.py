import pandas as pd
import glob, os
from tqdm import tqdm

missing_pga = []
preforo_below_GWT = []
nan_preforo = []

################ USER INPUTS ############################
american_date = True # True or False
input_folder_path = r"C:\Users\hf233\OneDrive - Brigham Young University\Liq\Gabrelle update\OG files from 2-14-24 - Copy"
dmt_folder_path = r"C:\Users\hf233\OneDrive - Brigham Young University\Liq\Gabrelle update\dmt test"
date_column_name = 'Date of CPT [gg/mm/aa]'
depth_column_name = "Depth (m)"
date1 = "20may"
date2 = "29may"
#########################################################

FS1 = "FS_" + date1
FS2 = "FS_" + date2

sites = []

for filename in glob.glob(os.path.join(input_folder_path, "*.xls*")):
    site = os.path.basename(filename).rstrip(".xls").lstrip("Copy of ")#Can take out this lstrip
    dmt = site.__contains__("DMT")
    if dmt == True:
        dmt_df = pd.read_excel(filename)
        final_dmt_path = os.path.join(dmt_folder_path,site + ".xlsx")
        dmt_df.to_excel(final_dmt_path, index=False)
        os.remove(filename)
    else:
        sites.append(site)