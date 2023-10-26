import pandas as pd
import numpy as np
import glob, os

def finding_max_depth (input_folder_path_calculated_files):

    max_depth_list = []
    site_list = []

    for filename in glob.glob(os.path.join(input_folder_path_calculated_files, "*.xls*")):

        site = os.path.basename(filename).rstrip(".xls")
        df = pd.read_excel(filename)

        max_depth_list.append(df["Depth (m)"].max())

        site_list.append(site)


    max_depth = max(max_depth_list)
    max_depth_index = max_depth_list.index(max_depth)
    site_name_max_depth = site_list[max_depth_index]


    return max_depth, site_name_max_depth

def create_monster_df (input_folder_path_calculated_files, depth_column_name):

    counter = 0
    monster_df = pd.DataFrame()

    for filename in glob.glob(os.path.join(input_folder_path_calculated_files, "*.xls*")):
        site = os.path.basename(filename).rstrip(".xls")
        df = pd.read_excel(filename)
        print(site)

        temp_col_names = []
        temp_col_vals = []

        for index, row in df.iterrows():
            depth = row["Depth (m)"]
            for column in df.columns:
                if column ==  depth_column_name:
                    continue
                else:
                    var = row[column]
                    # monster_df.at[counter , column + "_d_" + str(depth)] = row[column]
                    temp_col_names.append(column + "_d_" + str(depth))
                    temp_col_vals.append(row[column])
        # df_col_names = pd.DataFrame(temp_col_names)
        # df_col_val = pd.DataFrame(temp_col_vals)
        monster_df = pd.DataFrame({"header": temp_col_names, "vals": temp_col_vals}).T
        # monster_df.loc[counter] = {temp_col_vals}
        counter += 1
    return monster_df