import pandas as pd
import glob, os
from tqdm import tqdm

################ USER INPUTS ############################
input_folder_path = r"E:\Italy CPT stuff\testing"
export_folder_path = r"E:\Italy CPT stuff"
date1 = "20may"
date2 = "29may"
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
    # print(site)
    loop.set_description(f"soil parameters - {site} :")

    df = pd.read_excel(filename)


    #Columns to add to liq sheet
    liq_df.at[indx_counter,"site"] = site

    liq_df.at[indx_counter,"LPI_"+date1] = df.loc[0]["LPI_"+date1]
    liq_df.at[indx_counter, "LPI_" + date2] = df.loc[0]["LPI_" + date2]

    liq_df.at[indx_counter, f'towhata_basic_{date1}'] = df.loc[0][f'towhata_basic_{date1}']
    liq_df.at[indx_counter, f'towhata_basic_{date2}'] = df.loc[0][f'towhata_basic_{date2}']

    liq_df.at[indx_counter, f'towhata_basic_{date2}'] = df.loc[0][f'towhata_basic_{date2}']
    liq_df.at[indx_counter, f'towhata_basic_{date1}'] = df.loc[0][f'towhata_basic_{date1}']

    liq_df.at[indx_counter, f'towhata_cumulative_{date1}'] = df.loc[0][f'towhata_cumulative_{date1}']
    liq_df.at[indx_counter, f'towhata_cumulative_{date2}'] = df.loc[0][f'towhata_cumulative_{date2}']

    liq_df.at[indx_counter, "LPIish_basic_"+date1] = df.loc[0]["LPIish_basic_"+date1]
    liq_df.at[indx_counter, "LPIish_basic_" + date2] = df.loc[0]["LPIish_basic_" + date2]

    liq_df.at[indx_counter, "LPIish_cumulative_"+date1] = df.loc[0]["LPIish_cumulative_"+date1]
    liq_df.at[indx_counter, "LPIish_cumulative_" + date2] = df.loc[0]["LPIish_cumulative_" + date2]

    liq_df.at[indx_counter, 'LSN_'+date1] = df.loc[0]['LSN_'+date1]
    liq_df.at[indx_counter, 'LSN_' + date2] = df.loc[0]['LSN_' + date2]

    #Results section
    liq_df.at[indx_counter, f'LPI_{date1}_results'] = df.loc[0][f'LPI_{date1}_results']
    liq_df.at[indx_counter, f'LPI_{date2}_results'] = df.loc[0][f'LPI_{date2}_results']

    liq_df.at[indx_counter, f'towhata_basic_{date1}_results'] = df.loc[0][f'towhata_basic_{date1}_results']
    liq_df.at[indx_counter, f'towhata_basic_{date2}_results'] = df.loc[0][f'towhata_basic_{date2}_results']

    liq_df.at[indx_counter, f'towhata_basic_{date2}_results'] = df.loc[0][f'towhata_basic_{date2}_results']
    liq_df.at[indx_counter, f'towhata_basic_{date1}_results'] = df.loc[0][f'towhata_basic_{date1}_results']

    liq_df.at[indx_counter, f'towhata_cumulative_{date1}_results'] = df.loc[0][f'towhata_cumulative_{date1}_results']
    liq_df.at[indx_counter, f'towhata_cumulative_{date2}_results'] = df.loc[0][f'towhata_cumulative_{date2}_results']

    liq_df.at[indx_counter, "LPIish_basic_" + date1 + "_results"] = df.loc[0]["LPIish_basic_" + date1 + "_results"]
    liq_df.at[indx_counter, "LPIish_basic_" + date2 + "_results"] = df.loc[0]["LPIish_basic_" + date2 + "_results"]

    liq_df.at[indx_counter, "LPIish_cumulative_" + date1 + "_results"] = df.loc[0]["LPIish_cumulative_" + date1 + "_results"]
    liq_df.at[indx_counter, "LPIish_cumulative_" + date2 + "_results"] = df.loc[0]["LPIish_cumulative_" + date2 + "_results"]

    liq_df.at[indx_counter, 'LSN_' + date1 + "_results"] = df.loc[0]['LSN_' + date1 + "_results"]
    liq_df.at[indx_counter, 'LSN_' + date2 + "_results"] = df.loc[0]['LSN_' + date2 + "_results"]

    liq_df.at[indx_counter, 'Liquefaction'] = df.loc[0]['Liquefaction']

    indx_counter += 1
    loop.update(1)
loop.close()
export_folder_liq_df = os.path.join(export_folder_path,'liq_results_all_tests')
liq_df.to_excel(f'{export_folder_liq_df}.xlsx', index=False)