import pandas as pd

################ USER INPUTS ############################
input_file_path = r"C:\Users\jdundas2\OneDrive - Brigham Young University\Liq\Gabrelle update\liq_methods_performance 03 25.xlsx"
export_file_path = r"C:\Users\jdundas2\OneDrive - Brigham Young University\Liq\Gabrelle update"
#########################################################

df = pd.read_excel(input_file_path)

i = 0
for column in df.columns:
    if "results" in column and ("negative" in column or "positive" in column):
        stratified_value = 0
        non_stratified_value = 0
        for index, row in df.iterrows():
            if row['stratified'] == 1 and row[column] == 1:
                # df.at[i, "s_method"] = str(column)
                stratified_value += 1
            elif row['stratified'] == 0 and row[column] == 1:
                # df.at[i, "s_method"] = str(column)
                non_stratified_value += 1
        df.at[i, "stratified_value"] = stratified_value
        df.at[i, "non-stratified_value"] = non_stratified_value
        i += 1

df.to_excel(f'{export_file_path}\liq_methods_performance_stratified 03 26.xlsx', index=False)