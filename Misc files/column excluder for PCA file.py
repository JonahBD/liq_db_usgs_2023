import pandas as pd

import_file = r"C:\Users\jdundas2\OneDrive - Brigham Young University\Liq\Italy Data\Attempt 08 - OG\OG Data\log_reg_parameters_OG_A08.xlsx"
export_file_path = r"C:\Users\jdundas2\OneDrive - Brigham Young University\Liq\Italy Data\Model Building\OG\log_reg_parameters\log_reg_parameters_OG_A08.xlsx"
df = pd.read_excel(import_file)

columns = list(df)
columns_to_exclude = ['std', 'mean']
for col in columns:
    for col_drop in columns_to_exclude:
        if col_drop in col:
            df.drop(columns=col, axis=1, inplace=True)

new_name = import_file.rstrip(".xls")
# df.to_excel(f'{new_name}_some_col_excluded.xlsx', index=False)
df.to_excel(export_file_path, index=False)