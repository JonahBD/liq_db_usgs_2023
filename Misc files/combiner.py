import pandas as pd

# All rows and columns from the smaller_df are preserved. All columns from the larger_df will be added to the smaller_df
# in the combined_df. Any rows in the larger_df that aren't in the smaller_df will not be included in the combined_df.

larger_df = pd.read_excel(r"C:\Users\jonah\OneDrive\Finalized Liq Data\Vs_h1.xlsx")

# Smaller DataFrame (only has a fraction of the keys)
smaller_df = pd.read_excel(
    r"C:\Users\jonah\OneDrive\Finalized Liq Data\log_reg_parameters_OG_A08_post_column_excluder.xlsx")

# Merge the DataFrames to keep all data from the smaller one
combined_df = pd.merge(smaller_df, larger_df, on='site', how='left')

# Display the combined DataFrame
combined_df.to_excel(
    r"C:\Users\jonah\OneDrive\Finalized Liq Data\log_reg_parameters_OG_A08_MORE.xlsx", index=False)