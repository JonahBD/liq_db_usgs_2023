import pandas as pd

# Sample DataFrames
# Larger DataFrame
larger_df = pd.read_excel(r"C:\Users\jdundas2\OneDrive - Brigham Young University\Liq\Italy Data\Attempt 08 - OG\OG Data\Vs_h1.xlsx")

# Smaller DataFrame (only has a fraction of the keys)
smaller_df = pd.read_excel(r"C:\Users\jdundas2\OneDrive - Brigham Young University\Liq\Italy Data\Model Building\Soil Type models\log_reg_parameters_model_mixed.xlsx")

# Merge the DataFrames to keep all data from the smaller one
combined_df = pd.merge(smaller_df, larger_df, on='site', how='left')

# Display the combined DataFrame
combined_df.to_excel(r"C:\Users\jdundas2\OneDrive - Brigham Young University\Liq\Italy Data\Model Building\Soil Type models\log_reg_parameters_model_mixed_MORE.xlsx", index=False)