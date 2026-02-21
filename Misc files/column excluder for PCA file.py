import pandas as pd

import_file = r"C:\Users\jonah\OneDrive\Finalized Liq Data\log_reg_parameters_OG_A08.xlsx"
export_file_path = r"C:\Users\jonah\OneDrive\Finalized Liq Data\log_reg_parameters_OG_A08_post_column_excluder.xlsx"
df = pd.read_excel(import_file)

columns = list(df)
columns_to_exclude = ['std', 'mean']
for col in columns:
    for col_drop in columns_to_exclude:
        if col_drop in col:
            df.drop(columns=col, inplace=True)

new_name = import_file.rstrip(".xls")
# df.to_excel(f'{new_name}_some_col_excluded.xlsx', index=False)
df.to_excel(export_file_path, index=False)