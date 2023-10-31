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
        all_selected_columns.remove(depth_column_name) #TODO what do we want to do about the date column? Remove it, or save it somewhere else
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

def interpolator_ML (value_above, value_below, depth_below, depth_above, target_depth):

    if (value_above == np.isnan(value_above)) or (value_below == np.isnan(value_above)):
        interpolated_val = np.nan
    elif depth_below == depth_above:
        return value_above
    else:
        interpolated_val = value_below + (value_above-value_below)/(depth_above - depth_below) * (target_depth - depth_below)

    return interpolated_val

def closest(site_depth_column, target_depth):
    nearest = site_depth_column[min(range(len(site_depth_column)), key=lambda i: abs(site_depth_column[i] - target_depth))]
    index = site_depth_column[site_depth_column == nearest].index[0]
    if nearest == target_depth:
        return index, index
    if nearest < target_depth:
        before_index = index
        after_index = index + 1
    elif nearest > target_depth:
        before_index = index - 1
        after_index = index
    before_value = site_depth_column[before_index]
    after_value = site_depth_column[after_index]
    if before_index == -1:
        return "this is in a preforo" # TODO: how do we want to handle preforos
    return before_index, after_index


def create_monster_df (max_depth, depth_step, depth_step_selected_columns):

    depth_step_columns = [
        f"{column_name}:{round(step * depth_step, 2)}"
        for column_name in depth_step_selected_columns
        for step in range(1, int(max_depth / depth_step) + 1)
    ]

    target_depths = [
        round(step * depth_step, 2)
        for step in range(1, int(max_depth / depth_step) + 1)
    ]

    monster_df = pd.DataFrame(columns=depth_step_columns)

    return monster_df, depth_step_columns, target_depths

def fill_monster_df (input_folder_path, monster_df, depth_step_selected_columns, target_depths, depth_col_name):

    for filename in glob.glob(os.path.join(input_folder_path, "*.xls*")):
        monster_row = []
        site = os.path.basename(filename).rstrip(".xls")
        monster_df = pd.concat([monster_df, pd.DataFrame(index=pd.Index([site]))])
        df = pd.read_excel(filename)
        # print(site)
        for col in depth_step_selected_columns:
            for target_depth in target_depths:
                index_before, index_after = closest(df[depth_col_name], target_depth) # TODO: add nans before min depth of df and after max depth of df
                value_before = df.loc[index_before][col]
                value_after = df.loc[index_after][col]
                monster_row.append(interpolator_ML(value_after, value_before, df.loc[index_before][depth_col_name], df.loc[index_after][depth_col_name], target_depth))

        monster_df.loc[site] = monster_row

    return monster_df
























    site_counter = 0
    site_names = []
    for filename in glob.glob(os.path.join(input_folder_path, "*.xls*")):
        site = os.path.basename(filename).rstrip(".xls")
        df = pd.read_excel(filename)
        print(site)
        site_names.append(site)
        df.set_index(depth_column_name)

        for col_monster_df in list_of_depth_step_columns:

            for col_soil_parameters in df.columns:
                column_name = col_monster_df.split(":")[0]
                depth_val = col_monster_df.split(":")[1]
                if col_soil_parameters == column_name:
                    for depth, row in df.iterrows():
                        soil_paramterer_depth_val = (depth * depth_step) + depth_step
                        if soil_paramterer_depth_val == depth_val:
                            monster_df.at[site_counter, col_monster_df] = df.at[depth, column_name]
        site_counter += 1
    monster_df.set_index(site_names)


    return monster_df
#------------------------------------------------------------------------------------------------------------
    counter = 0
    monster_df = pd.DataFrame()
    monster_depth = depth_step

    #df = pd.read_excel(glob.glob(os.path.join(input_folder_path, "*.xls*"))[0])
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
