import pandas as pd
import time
from datetime import date

# time.sleep(60*20)

################ USER INPUTS ############################
input_file_path = r"C:\Users\jdundas2\OneDrive - Brigham Young University\Liq\Gabrelle update\liq_param_compiled 03 19.xlsx"
export_file_path = r"C:\Users\jdundas2\OneDrive - Brigham Young University\Liq\Gabrelle update"
#########################################################
today_date = date.today()
date = f'{today_date.month}-{today_date.day}'

df = pd.read_excel(input_file_path)
scrap = pd.DataFrame()
#
for column in df.columns[1:]:
    if "results" in column:
        for index, row in df.iterrows():
            our_val = row[column]
            liq_val = row["Liquefaction"]#_italy
            if liq_val == 0 and our_val == 0:
                df.at[index, f'{column}_true_negative'] = 1
            elif liq_val == 1 and our_val == 0:
                df.at[index,f'{column}_false_negative'] = 1
            elif liq_val == 1 and our_val == 1:
                df.at[index, f'{column}_true_positive'] = 1
            elif liq_val == 0 and our_val == 1:
                df.at[index, f'{column}_false_positive'] = 1

i = 0
for column in df.columns:
    if "results" in column and ("negative" in column or "positive" in column):
        df.at[i, "method"] = str(column)
        df.at[i, "value"] = df[str(column)].sum()
        i += 1

df.to_excel(f'{export_file_path}\liq_methods_performance {date}.xlsx', index=False)
