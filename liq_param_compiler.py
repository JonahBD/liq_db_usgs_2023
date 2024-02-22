import pandas as pd
import glob, os
from tqdm import tqdm

################ USER INPUTS ############################
input_folder_path = r"C:\Users\hf233\OneDrive - Brigham Young University\Liq\Gabrelle update\Only one eq soil parameters"
export_folder_path = r"C:\Users\hf233\OneDrive - Brigham Young University\Liq\Gabrelle update\Only one eq soil parameters\liq param sheet"
#########################################################

sites = []
liq_df = pd.DataFrame()
indx_counter = 0
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
    liq_df.at[indx_counter,"site"] = site

    liq_df.at[indx_counter,"LPI"] = df.loc[0]["LPI"]

    liq_df.at[indx_counter, f'towhata_basic'] = df.loc[0][f'towhata_basic']

    liq_df.at[indx_counter, f'towhata_basic'] = df.loc[0][f'towhata_basic']

    liq_df.at[indx_counter, f'towhata_cumulative'] = df.loc[0][f'towhata_cumulative']

    liq_df.at[indx_counter, "LPIish_basic"] = df.loc[0]["LPIish_basic"]

    liq_df.at[indx_counter, "LPIish_cumulative"] = df.loc[0]["LPIish_cumulative"]

    liq_df.at[indx_counter, 'LSN'] = df.loc[0]['LSN']

    #Results section
    liq_df.at[indx_counter, f'LPI_results'] = df.loc[0][f'LPI_results']

    liq_df.at[indx_counter, f'towhata_basic_results'] = df.loc[0][f'towhata_basic_results']

    liq_df.at[indx_counter, f'towhata_basic_results'] = df.loc[0][f'towhata_basic_results']

    liq_df.at[indx_counter, f'towhata_cumulative_results'] = df.loc[0][f'towhata_cumulative_results']

    liq_df.at[indx_counter, "LPIish_basic" + "_results"] = df.loc[0]["LPIish_basic" + "_results"]

    liq_df.at[indx_counter, "LPIish_cumulative" + "_results"] = df.loc[0]["LPIish_cumulative" + "_results"]

    liq_df.at[indx_counter, 'LSN' + "_results"] = df.loc[0]['LSN' + "_results"]

    liq_df.at[indx_counter, 'Liquefaction'] = df.loc[0]['Liquefaction']

    indx_counter += 1
    loop.update(1)
loop.close()

liq_df.to_excel(f'{export_folder_path}\liq_param_compiled.xlsx', index=False)