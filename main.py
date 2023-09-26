from functions import *
import pandas as pd
import glob, os

counter = 0
df_name = []
error = False

folder_path = r"C:\Users\jdundas2\Documents\Step 5 downloads\5. CPTU standard excel (1685 items)"
for filename in glob.glob(os.path.join(folder_path, "*.xls*")):
    df = pd.read_excel(filename)
    site = os.path.basename(filename).rstrip(".xls")

    df = soil_parameters(df)
    try:
        df = PGA_insertion(df,r"C:\Users\jdundas2\Documents\all current sites.xlsx", site)
    except KeyError:
        print("The PGA doesn't exists for this site: " + site)
        continue
    df = FS_liq(df, 6.1, 5.9)

    df = h1_h2_basic(df, 'Depth (m)','FS_20may')
    df = h1_h2_basic(df, 'Depth (m)', 'FS_29may')
    df = h1_h2_cumulative(df, 'Depth (m)', 'FS_20may')
    df = h1_h2_cumulative(df, 'Depth (m)', 'FS_29may')

    filename = filename.replace('5. CPTU standard excel (1685 items)', 'polished')
    if filename[-1] == 's':
        filename = filename.replace('xls', 'xlsx')

    df.to_excel(filename, index=False)
