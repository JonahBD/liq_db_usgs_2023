import pandas as pd
import glob, os
from tqdm import tqdm
import time
from datetime import date

# time.sleep(60*60*4)

################ USER INPUTS ############################
input_folder_path = r"C:\Users\jdundas2\OneDrive - Brigham Young University\Liq\Gabrelle update\adj pga 5 31 (pga limit 1 stdev diff)"
export_folder_path = r'C:\Users\jdundas2\OneDrive - Brigham Young University\Liq\Gabrelle update'
#########################################################
today_date = date.today()
date = f'{today_date.month}-{today_date.day}'

sites = []
adj_pga_df = pd.DataFrame()
indx_counter = 0
changed_pga_counter = 0
for filename in glob.glob(os.path.join(input_folder_path, "*.xls*")):
    site = os.path.basename(filename).rstrip(".xls")
    sites.append(site)

loop = tqdm(total=(len(sites)))

for filename in glob.glob(os.path.join(input_folder_path, "*.xls*")):
    site = os.path.basename(filename).rstrip(".xls")
    loop.set_description(f"Loading - {site} :")

    if site == "sites_to_check":
        continue

    df = pd.read_excel(filename)

    #Columns to add to liq sheet
    adj_pga_df.at[indx_counter,"site"] = site
    
    if df.loc[1]["PGA"] == "OG PGA below":
        adj_pga_df.at[indx_counter, "OG PGA"] = df.loc[2]["PGA"]
        adj_pga_df.at[indx_counter, "New PGA"] = df.loc[0]["PGA"]
        changed_pga_counter += 1
    else:
        adj_pga_df.at[indx_counter, "OG PGA"] = df.loc[0]["PGA"]
        adj_pga_df.at[indx_counter, "New PGA"] = df.loc[0]["PGA"]
    adj_pga_df.at[indx_counter, "PGA Diff"] = adj_pga_df.loc[indx_counter]['New PGA'] - adj_pga_df.loc[indx_counter]["OG PGA"]
    if indx_counter == 30:
        adj_pga_df.to_excel(f'{export_folder_path}\ adj_pga {date}.xlsx', index=False)
    indx_counter += 1

    loop.update(1)
loop.close()

adj_pga_df.to_excel(f'{export_folder_path}\half stdv lowered pga {date}.xlsx', index=False)