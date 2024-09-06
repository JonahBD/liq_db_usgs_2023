import pandas as pd
import time
from datetime import date
from sklearn.metrics import cohen_kappa_score

# time.sleep(60*20)

################ USER INPUTS ############################
input_file_path = r"C:\Users\jdundas2\OneDrive - Brigham Young University\Liq\NZ data\Attempt 02\LSN 10 stuff\liq_param_compiled_2011_soil_parameter_7-29.xlsx"
export_file_path = r"C:\Users\jdundas2\OneDrive - Brigham Young University\Liq\NZ data\Attempt 02\LSN 10 stuff"
exclude_clay_sites = True
name = "10-100"
attempt_number = "A05"
#########################################################
today_date = date.today()
date = f'{today_date.month}-{today_date.day}'

df = pd.read_excel(input_file_path)
results = pd.DataFrame()

# for index, row in df.iterrows():
#     if row['clay_profile'] == 1 and row['Liquefaction'] == 0:
#         df.at[index, 'exclude'] = 1
#     else:
#         df.at[index, 'exclude'] = 0

if exclude_clay_sites:
    df = df[df['exclude'] == 0]

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
n = 0
for column in df.columns:
    if "results" in column and ("negative" in column or "positive" in column):
        results.at[i, "classification_method"] = str(column+":")
        results.at[i, "value"] = df[str(column)].sum()
        df.drop(columns=[column], inplace=True)
        df.reset_index(drop=True, inplace=True)
        i += 1
for column in df.columns:
    if "results" in column:
        if column == "LD_and_CR_results":
            continue
        results.at[n, "kappa_method"] = str(column[:-8]+":")
        results.at[n, "kappa"] = cohen_kappa_score(df['Liquefaction'], df[column])
        n += 4
#
df = pd.concat([df, results], axis=1)

if exclude_clay_sites:
    df.to_excel(fr'{export_file_path}\liq_methods_performance_{name}_without_clay_{attempt_number}.xlsx', index=False)
else:
    df.to_excel(fr'{export_file_path}\liq_methods_performance_{name}_with_clay_{attempt_number}.xlsx', index=False)