from functions import *
import pandas as pd
import numpy as np
import glob, os
from datetime import datetime
from tqdm import tqdm

input_folder_path = r"C:\Users\jdundas2\OneDrive - Brigham Young University\Liq\Gabrelle update\Soil parameters ITALY 4-29\to run"
export_folder_path = r"C:\Users\jdundas2\OneDrive - Brigham Young University\Liq\Gabrelle update\Soil parameters ITALY 4-29\to run"
vals_pga_and_liq = r"C:\Users\jdundas2\OneDrive - Brigham Young University\Liq\PGA-liq ITALY values 05 03 24.xlsx"

for filename in glob.glob(os.path.join(input_folder_path, "*.xls*")):
    df = pd.read_excel(filename)
    site = os.path.basename(filename).rstrip(".xls").lstrip("Copy of")
    if site == "sites_to_check":
        continue
    pga_df = pd.read_excel(vals_pga_and_liq)
    pga_df.set_index('site', inplace=True)
    # if pga_df.loc[site]['PGA_20may'] > pga_df.loc[site]['PGA_29may']:
    #     df.at[0, 'PGA'] = pga_df.loc[site]['PGA_20may']
    #     df.at[0,"EQ"] = "20_may"
    #     df.at[1,"EQ"] = 6.1
    # else:
    #     df.at[0, 'PGA'] = pga_df.loc[site]['PGA_29may'] # NOTE: change this back to 29may when not comparing with cliq files
    #     df.at[0, "EQ"] = "29_may"
    #     df.at[1, "EQ"] = 5.9
    # df.at[0, 'PGA_20may'] = pga_df.loc[site]['PGA_20may']
    # df.at[0, 'PGA_29may'] = pga_df.loc[site]['PGA_29may']
    df.at[0, 'Liquefaction_italy'] = pga_df.loc[site]['Liquefaction']
    export_folder_path_df = os.path.join(export_folder_path, site + '.xlsx')
    df.to_excel(export_folder_path_df, index=False)