import pandas as pd
import numpy as np
import glob, os


def user_input_columns (input_folder_path_calculated_files, depth_column_name, acceptable_list):

    df = pd.read_excel(glob.glob(os.path.join(input_folder_path_calculated_files, "*.xls*"))[0])
    for column in df.columns:
        print(df.columns.get_loc(column), column)

    columns = input("\nWhat columns do you want to include? Don't include the depth column. (example: 2-45,51,54): ")

    selections = columns.split(',')

    all_selected_columns = []

    for selection in selections:
        if '-' in selection:
            start, end = map(int, selection.split('-'))
            all_selected_columns.extend(df.columns[start:end + 1])
        else:
            all_selected_columns.append(df.columns[int(selection)])

    # column_df = df[selected_columns]
    if depth_column_name in all_selected_columns:
        all_selected_columns.remove(depth_column_name)
    all_selected_columns_df = pd.DataFrame(columns=all_selected_columns)

    print('-------------------------------------------------------------------\n')
    for column in all_selected_columns_df.columns:
        print(all_selected_columns_df.columns.get_loc(column),column)
    one_row_inputs = input("\nWhat columns have only one row? (example: 2-45,51,54): ")

    selections = one_row_inputs.split(',')

    one_col_selected_columns = []

    for selection in selections:
        if '-' in selection:
            start, end = map(int, selection.split('-'))
            one_col_selected_columns.extend(all_selected_columns_df.columns[start:end + 1])
        else:
            one_col_selected_columns.append(all_selected_columns_df.columns[int(selection)])

    depth_step_selected_columns = all_selected_columns
    for i in depth_step_selected_columns[:]:
        if i in one_col_selected_columns:
            depth_step_selected_columns.remove(i)

    print('-------------------------------------------------------------------\n')
    print("Here is the list of columns that will have values for each depth step interval:\n\t"+str(depth_step_selected_columns)+"\n")
    print("Here is the list of columns that will only have one column (i.e. not a value for each depth step interval):\n\t"+str(one_col_selected_columns)+"\n")
    acceptable_list = input("Is this correct? (True or False) *this is case sensitive*: ")
    if acceptable_list == "True":
        acceptable_list = True
    else:
        acceptable_list = False

    return acceptable_list, depth_step_selected_columns, one_col_selected_columns


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

def create_monster_df (input_folder_path, depth_column_name, max_depth, depth_step, depth_step_selected_columns, one_col_selected_columns):

    monster_df = pd.DataFrame



    return monster_df
#------------------------------------------------------------------------------------------------------------
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
