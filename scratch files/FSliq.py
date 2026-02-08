from functions import *
import pandas as pd
import glob, os

pga_df = pd.read_excel(r"C:\Users\jdundas2\Downloads\ALL sites.xlsx")
pga_df.set_index('site', inplace=True)
# print(pga_df)
keyerrors = []

folder_path = r"C:\Users\jdundas2\Documents\Step 5 downloads\Calculated Soil Parameters (trial 1)"
for filename in glob.glob(os.path.join(folder_path, "*.xls*")):
    site = os.path.basename(filename).removesuffix('.xlsx')
    df = pd.read_excel(filename)
    try:
        df.at[0,'PGA_20may'] = pga_df.loc[site]['PGA_20may']
        df.at[0,'PGA_29may'] = pga_df.loc[site]['PGA_29may']
        df.at[0,'Liquefaction'] = pga_df.loc[site]["Liquefaction"]
    except KeyError:
        keyerrors.append(site)
        continue
    # print(pga_df.loc[site]['PGA_20may'])
    df = FSliq(df,6.1,5.9)
    filename = filename.replace('Calculated Soil Parameters (trial 1)', 'Calculated PGA')
    # filename = filename.replace('.xls', '.xlsx')
    df.to_excel(filename, index=False)

print(keyerrors)
