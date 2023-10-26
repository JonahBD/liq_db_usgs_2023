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
    max_depth_site_name = site_list[max_depth_index]

    return max_depth, max_depth_site_name

def create_monster_df (input_folder_path, depth_column_name, max_depth, depth_step):

    counter = 0
    monster_df = pd.DataFrame()
    monster_depth = depth_step

    df = pd.read_excel(glob.glob(os.path.join(input_folder_path, "*.xls*"))[0])
    # for column in df.columns:
        # print(column, df.columns.get_loc(column))

    # for filename in glob.glob(os.path.join(input_folder_path, "*.xls*")):
    #     site = os.path.basename(filename).rstrip(".xls")
    #     df = pd.read_excel(filename)
    #     print(site)
    #
    #     temp_col_names = []
    #     temp_col_vals = []
    #
    #     for index, row in df.iterrows():
    #         depth = row[depth_column_name]
    #         for column in df.columns:
    #             if column ==  depth_column_name:
    #                 continue
    #             else:
    #                 # monster_df.at[counter , column + "_d_" + str(depth)] = row[column]
    #                 temp_col_names.append(column + "_d_" + str(monster_depth))
    #                 temp_col_vals.append(row[column])
    #     # df_col_names = pd.DataFrame(temp_col_names)
    #     # df_col_val = pd.DataFrame(temp_col_vals)
    #     monster_df = pd.DataFrame({"header": temp_col_names, "vals": temp_col_vals}).T
    #     # monster_df.loc[counter] = {temp_col_vals}
    #     counter += 1
    #     monster_depth += depth_step
    # return monster_df