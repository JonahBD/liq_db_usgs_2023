import pandas as pd
import numpy as np

export_folder_path =r'C:\Users\hf233\OneDrive - Brigham Young University\Liq\Italy Data\Attempt 04\OG Data'
df = pd.read_excel(r"C:\Users\hf233\OneDrive - Brigham Young University\Liq\Italy Data\Attempt 04\OG Data\liq_methods_performance_OG_without_clay_A04.xlsx") #Run on liq methods performance to exclue or include clays
methods = [
    {
        'column': 'LPI_results',
        'label': 'LPI',
        "color": 'b'
    },{
        'column': 'LPIish_basic_results',
        'label': 'LPIISH',
        "color": 'g'
    },
    {
        'column': 'LSN_results',
        'label':'LSN',
        "color": 'r'
    },
    {
        'column': 'LD_and_CR_binary_results',
        'label': 'Hutabarat and Bray',
        "color": '#FFA500'
    },{
        'column': 'ishihara_curve_basic_results',
        'label': "Ishihara Basic",
        "color":'#800080'
    },{
        'column': 'ishihara_curve_cumulative_results',
        'label': "Ishihara Cumulative",
        "color":'#808080'
    },{
        'column': 'towhata_basic_results',
        'label': "Towhata",
        "color":'k'
    }

        ]
mosaic_df = pd.DataFrame()
liq_column_name = 'Observations'
mosaic_df[liq_column_name] = df['Liquefaction']

liq_array = mosaic_df[liq_column_name].to_numpy()
new_array = np.where(liq_array == 1, 'Manifestation', "No Manifestation")
mosaic_df[liq_column_name] = new_array
for m in methods:
    mosaic_df[m['label']] = df[m['column']]
    liq_array = df[m['column']].to_numpy()
    new_array = np.where(liq_array == 1, 'Manifestation', "No Manifestation")
    mosaic_df[m['label']] = new_array

mosaic_df.to_excel(f'{export_folder_path}\mosaic.xlsx', index=False)