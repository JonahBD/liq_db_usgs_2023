import numpy as np
# --- Pickle
# File - --
import pandas as pd

# export_file_path_df = r"C:\Users\hf233\Downloads\maurer.csv"
pd.read_pickle(r"C:\Users\hf233\Downloads\CANTERBURYDATASET.pkl")

# --- H5
# File - --
import pandas as pd

pd.read_hdf(r"C:\Users\hf233\Downloads\CANTERBURYDATASET.h5", "CANTERBURYDATASET")

# --- CSV
# File - --
import pandas as pd
#TAkes about 1 hour 5 minutes to run
full_df = pd.read_csv(r"C:\Users\hf233\Downloads\CANTERBURYDATASET (1).csv", index_col=0)

# Disclaimer: When loading as a CSV the columns with multiple values (e.g. magnitude) will need additional processing to be accessed as an array.
# ---


def makeArray(text):
    return np.fromstring(text.strip("[]"), sep=', ')


full_df['Magnitude'] = full_df['Magnitude'].apply(makeArray)
full_df['PGA'] = full_df['PGA'].apply(makeArray)
full_df['PGAsigma'] = full_df['PGAsigma'].apply(makeArray)
full_df['GWT'] = full_df['GWT'].apply(makeArray)
full_df['Manifestation'] = full_df['Manifestation'].apply(makeArray)
full_df['depth'] = full_df['depth'].apply(makeArray)
full_df['qc'] = full_df['qc'].apply(makeArray)
full_df['qc_inv'] = full_df['qc_inv'].apply(makeArray)
full_df['fs'] = full_df['fs'].apply(makeArray)
full_df['fs_inv'] = full_df['fs_inv'].apply(makeArray)
full_df['u2'] = full_df['u2'].apply(makeArray)

# print(len(full_df.loc[5]['qc']))
# print(full_df['PGA'][1][0])
# full_df.to_excel(r"C:\Users\hf233\Downloads\maurer.xlsx", index=False)
# print(full_df)


from functions import *
import pandas as pd
import numpy as np
import glob, os
from datetime import datetime
from tqdm import tqdm

missing_pga = []
preforo_below_GWT = []
nan_preforo = []
missing_date = []
GWT_or_preforo_wrong_type = []
GWT_zero_nan = []
LD_not_working = []

################ USER INPUTS ############################
export_folder_path = r"C:\Users\hf233\OneDrive - Brigham Young University\Liq\NZ data"
depth_column_name = "Depth (m)"
#########################################################

sites = []

for site in full_df['CPTname']:
    sites.append(site)

loop = tqdm(total=(len(sites)))


for index, row in full_df.iterrows():
    # print(site)
    site = row['CPTname']
    loop.set_description(f"Homogenizing - {site} :")

    # print(type(row['Date']))
    df = pd.DataFrame({'Depth (m)': row['depth'], 'qc (MPa)': row['qc']/1000, 'fs (kPa)': row['fs'], 'u (kPa)': row['u2'], 'GWT [m]': '', 'Date of CPT [gg/mm/aa]': '', 'preforo [m]': '', "Unnamed: 5": ''})
    df = df.drop(df.index[0])

    # Reset the index
    df = df.reset_index(drop=True)
    def qt(df):
        for index, row in df.iterrows():
            df.at[index,'qt (MPa)'] = row['qc (MPa)'] + row['u (kPa)']/1000 * (1 - .8)#cliq uses .8, found in Gregg drilling guide 7
        return df
    df = qt(df)

    df = df[[depth_column_name, 'qc (MPa)', 'fs (kPa)', 'u (kPa)', 'qt (MPa)',
             "Unnamed: 5", 'GWT [m]', 'Date of CPT [gg/mm/aa]', 'preforo [m]']]
    eq_dates = ['2010', '2011', '2016']
    for n in range(3):
        df.at[0,'EQ'] = eq_dates[n]
        df.at[1, 'EQ'] = row['Magnitude'][n]
        df.at[0,'GWT [m]'] = row['GWT'][n]
        df.at[0, 'PGA'] = row['PGA'][n]
        if df[depth_column_name].iloc[-1] < 20: #NOTE: This limits any files to a depth of greater than 20 m
            continue
        if row['Manifestation'][n] == 10 or row['Manifestation'][n] == 4 or row['Manifestation'][n] == 5: #NOTE: this will change how many sites get used for each EQ
            continue
            #https://www.designsafe-ci.org/data/browser/public/designsafe.storage.published/PRJ-2937%2FData%20Paper%20Manuscript.pdf
        elif row['Manifestation'][n] > 0:
            df.at[0, "Liquefaction"] = 1
        else:
            df.at[0, "Liquefaction"] = 0
        df.to_excel(f'{export_folder_path}/eq_{eq_dates[n]}_final/{site}.xlsx', index=False)

    loop.update(1)
loop.close()



