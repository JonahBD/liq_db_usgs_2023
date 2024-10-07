import pandas as pd

liq_param_compiled_path = r"C:\Users\jdundas2\OneDrive - Brigham Young University\Liq\Italy Data\Attempt 06 - GWT, OG\OG Data\liq_param_compiled_OG_A06.xlsx"
log_reg_param_path = r"C:\Users\jdundas2\OneDrive - Brigham Young University\Liq\Italy Data\Attempt 06 - GWT, OG\OG Data\log_reg_parameters_OG_A06.xlsx"
output_folder_path = r"C:\Users\jdundas2\OneDrive - Brigham Young University\Liq\Italy Data\MAIN_output"
attempt = "A02"

liq_param_compiled_df = pd.read_excel(liq_param_compiled_path)
log_reg_param_df = pd.read_excel(log_reg_param_path)

duplicate_cols = [col for col in liq_param_compiled_df.columns if col in log_reg_param_df.columns and col != 'site']
log_reg_param_df.drop(columns=duplicate_cols, inplace=True)

merged_df = pd.merge(liq_param_compiled_df, log_reg_param_df, on="site", how="left")
merged_df.drop(columns=["h1_φ' U (degrees)_median"], inplace=True)

substrings_to_exclude = ['h2', 'std', 'mean', 'results']
columns_to_include = ['h2_basic', "h2_cumulative"]
cols_to_remove = [col for col in merged_df if (any(substring in col for substring in substrings_to_exclude) and col not in columns_to_include)]
# cols_to_remove.extend(['stratified', 'clay_profile', 'exclude', 'h1b_sand_percent', 'methods_perform',
#                        'towhata_cumulative', 'h1_thickness', 'sand_percent', 'LPIish_cumulative', 'EQ', 'EQ_mag', 'PGA',
#                        'Liquefaction', 'GWT [m]'])
merged_df.drop(columns=cols_to_remove, inplace=True)
# merged_df.rename(columns={'towhata_basic': "towhata", "LPIish_basic": "LPIish"}, inplace=True)

merged_df.to_excel(fr"{output_folder_path}\MAIN_output_{attempt}.xlsx", index=False)