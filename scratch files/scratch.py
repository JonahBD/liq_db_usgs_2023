import pandas as pd

all = pd.read_excel(r"C:\Users\jdundas2\OneDrive - Brigham Young University\Liq\Final Data\OG Data\PCA_parameters_all_sites 7-5.xlsx")
subset = pd.read_excel(r"C:\Users\jdundas2\OneDrive - Brigham Young University\Liq\Final Data\OG Data\liq_param_compiled_10_150_7-3.xlsx")
subset.rename(columns={'id_indpu': 'site'}, inplace=True)
subset = subset['site']

df = all.merge(subset)
# df = all.loc[all['Liquefaction'] == 1]

df.to_excel(fr'C:\Users\jdundas2\OneDrive - Brigham Young University\Liq\Final Data\pca_parameters_lpi_labeled.xlsx', index=False)
