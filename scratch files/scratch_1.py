import pandas as pd
import shutil

ten_meters = pd.read_excel(r"C:\Users\jdundas2\OneDrive - Brigham Young University\Liq\Final Data\10m liquefaction sites.xlsx")
one_fifty = pd.read_excel(r"C:\Users\jdundas2\OneDrive - Brigham Young University\Liq\Final Data\150m non liquefaction sites.xlsx")
source_folder_path = r"C:\Users\jdundas2\OneDrive - Brigham Young University\Liq\Final Data\OG Data\Soil Parameters"
destination_folder_path = r"C:\Users\jdundas2\OneDrive - Brigham Young University\Liq\Final Data\OG Data\Soil Parameters (10m 150m)"

df = pd.concat([ten_meters, one_fifty])

for site in df['id_indpu']:
    shutil.copyfile(f'{source_folder_path}\\{site}.xlsx', f'{destination_folder_path}\\{site}.xlsx')