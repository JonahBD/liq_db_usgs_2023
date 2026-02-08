from functions import *
import pandas as pd
import glob, os
from tqdm import tqdm

input_folder_path = r"C:\Users\jdundas2\OneDrive - Brigham Young University\Liq\Gabrelle update\OG 2-14"
export_folder_path = r"C:\Users\jdundas2\OneDrive - Brigham Young University\Liq\Gabrelle update"
under_preforo = []
preforo_difference = []
first_value = []

sites = []

for filename in glob.glob(os.path.join(input_folder_path, "*.xls*")):
    site = os.path.basename(filename).rstrip(".xls").lstrip("Copy of")
    sites.append(site)

loop = tqdm(total=(len(sites)))

for filename in glob.glob(os.path.join(input_folder_path, "*.xls*")):
    site = os.path.basename(filename).rstrip(".xls").lstrip("Copy of")
    # print(site)
    loop.set_description(f"soil parameters - {site} :")

    df = pd.read_excel(filename)
    if df.loc[0]['Depth (m)'] < df.loc[0]["preforo [m]"]:
        under_preforo.append(site)
        preforo_difference.append(df.loc[0]["preforo [m]"] - df.loc[0]['Depth (m)'])
        first_value.append(df.loc[0]['qc (MPa)'])

    loop.update(1)
loop.close()

up = pd.DataFrame(list(zip(under_preforo,preforo_difference, first_value)),columns=['site','preforo difference','first qc value'])

up.to_excel(f"{export_folder_path}\\under_preforo.xlsx", index=False)