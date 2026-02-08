import pandas as pd
import numpy as np

all_sites = pd.read_excel(r"C:\Users\jdundas2\OneDrive - Brigham Young University\Liq\Final Data\PGA Adj\attribute table all.xlsx")

errors = pd.DataFrame()



counter = 0

for i, row in all_sites.iterrows():
    liq = all_sites['Liquefaction'][i]
    lpi = all_sites["LPI_results"][i]

    if (liq == 1 and lpi == 0) or (liq == 0 and lpi == 1):
        errors.at[counter, 'site'] = all_sites.loc[i]['id_indpu']
        errors.at[counter, 'LPI'] = all_sites.loc[i]['LPI']
        errors.at[counter, 'LPI_results'] = all_sites.loc[i]['LPI_results']
        errors.at[counter, 'Liquefaction'] = all_sites.loc[i]['Liquefaction']
        errors.at[counter, 'New PGA'] = all_sites.loc[i]['New PGA']
        errors.at[counter, 'Diff PGA'] = all_sites.loc[i]['Diff PGA']
        errors.at[counter, 'GWT'] = all_sites.loc[i]['GWT [m]']
        counter += 1

errors.to_excel(r"C:\Users\jdundas2\OneDrive - Brigham Young University\Liq\Final Data\PGA Adj\lpi_errors.xlsx", index=False)