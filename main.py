from functions import *
import pandas as pd
import glob, os


folder_path = r"C:\Users\jdundas2\Documents\Step 5 downloads\5. CPTU standard excel (1685 items)"
for filename in glob.glob(os.path.join(folder_path, "*.xls*")):
    df.name = os.path.basename(filename).rstrip(".xls")
    df = pd.read_excel(filename)

    df = soil_parameters(df)
    df = FSliq(df, 6.1, 5.9)

    basic_20may = h1_h2_basic(df, 'Depth (m)', 'FS_20may')
    basic_29may = h1_h2_basic(df, 'Depth (m)', 'FS_29may')

    cumulative_20may = h1_h2_cumulative(df, 'Depth (m)', 'FS_20may')
    cumulative_29may = h1_h2_cumulative(df, 'Depth (m)', 'FS_29may')

    df.at[0,'h1_basic_20may'] = basic_20may[0]
    df.at[0, 'h2_basic_20may'] = basic_20may[1]
    df.at[0,'h1_cumulative_20may'] = cumulative_20may[0]
    df.at[0,'h2_cumulative_20may'] = cumulative_20may[1]

    df.at[0, 'h1_basic_29may'] = basic_29may[0]
    df.at[0, 'h2_basic_29may'] = basic_29may[1]
    df.at[0, 'h1_cumulative_29may'] = cumulative_29may[0]
    df.at[0, 'h2_cumulative_29may'] = cumulative_29may[1]

    filename = filename.replace('Calculated PGA', 'h1 h2 calcs')

    df.to_excel(filename, index=False)
