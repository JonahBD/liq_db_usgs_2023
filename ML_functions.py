import pandas as pd
import numpy as np
import glob, os
from tqdm import tqdm


def user_input_columns (input_folder_path_calculated_files, depth_column_name, acceptable_list_confirmation):

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
    acceptable_list_confirmation = input("Is this correct? (True or False) *this is case sensitive*: ")
    if acceptable_list_confirmation == "True":

        acceptable_list_confirmation = True
    else:
        acceptable_list_confirmation = False

    return acceptable_list_confirmation, depth_step_selected_columns, one_col_selected_columns


def finding_max_depth (input_folder_path_calculated_files, depth_col_name):

    max_depth_list = []
    site_list = []

    for filename in tqdm(glob.glob(os.path.join(input_folder_path_calculated_files, "*.xls*"))):

        site = os.path.basename(filename).rstrip(".xls")
        df = pd.read_excel(filename)

        max_depth_list.append(df[depth_col_name].max())

        site_list.append(site)

    max_depth = max(max_depth_list)
    max_depth_index = max_depth_list.index(max_depth)
    max_depth_site_name = site_list[max_depth_index]

    return max_depth, max_depth_site_name

def interpolator_ML (value_above, value_below, depth_below, depth_above, target_depth):

    if value_below == "No Solution" or value_above == "No Solution":
        interpolated_val = np.nan
    elif value_above == "" or value_below == "": # TODO: should we change empty strings to nans in the soil parameter functions
        interpolated_val = np.nan
    elif (np.isnan(float(value_above))) or (np.isnan(float(value_below))): # TODO: the last error thrown was OverflowError: cannot convert float infinity to integer 036010P218CPTU218
        interpolated_val = np.nan
    elif (abs((value_below)) == 9999) or (abs(int(value_above)) == 9999):
        interpolated_val = np.nan
    elif depth_below == depth_above:
        return value_above
    else:
        interpolated_val = value_below + (value_above-value_below)/(depth_above - depth_below) * (target_depth - depth_below)

    return interpolated_val

def closest(site_depth_column, target_depth):
    abs_diff = np.abs(site_depth_column - target_depth)
    index = np.argmin(abs_diff)
    nearest = site_depth_column[index]
    # nearest = site_depth_column[min(range(len(site_depth_column)), key=lambda i: abs(site_depth_column[i] - target_depth))]
    # index = site_depth_column[site_depth_column == nearest].index[0]
    if nearest == target_depth:
        return index, site_depth_column[index], index, site_depth_column[index]
    if nearest < target_depth:
        before_index = index
        after_index = index + 1
    elif nearest > target_depth:
        before_index = index - 1
        after_index = index
    before_depth = site_depth_column[before_index]
    after_depth = site_depth_column[after_index]
    return before_index, before_depth, after_index, after_depth


def create_monster_df (max_depth, depth_step, depth_step_selected_columns, one_col_selected_columns):

    depth_step_columns = [
        f"{column_name}:{round(step * depth_step, 2)}"
        for column_name in depth_step_selected_columns
        for step in range(1, int(max_depth / depth_step) + 1)
    ]

    one_col_columns = [
        f"{column_name}" for column_name in one_col_selected_columns
    ]

    target_depths = [
        round(step * depth_step, 2)
        for step in range(1, int(max_depth / depth_step) + 1)
    ]

    monster_df = pd.DataFrame(columns=(depth_step_columns + one_col_columns))

    return monster_df, depth_step_columns, target_depths

def fill_monster_df (input_folder_path, monster_df, depth_step_selected_columns, target_depths, depth_col_name, one_row_selected_col):

    sites = []

    for filename in glob.glob(os.path.join(input_folder_path, "*.xls*")):
        site = os.path.basename(filename).rstrip(".xls")
        sites.append(site)

    loop = tqdm(total=len(sites), colour="#c6e2ff")

    for filename in glob.glob(os.path.join(input_folder_path, "*.xls*")):
        monster_row = []
        #TODO: add loading bar
        site = os.path.basename(filename).rstrip(".xls")
        loop.set_description(f"{site} :")

        monster_df = pd.concat([monster_df, pd.DataFrame(index=pd.Index([site]))])
        df = pd.read_excel(filename)
        # print(site)

        for col in depth_step_selected_columns:
            values = df[col].to_numpy()
            depths = df[depth_col_name].to_numpy()

            for target_depth in target_depths:

                if target_depth > depths[-1]:
                    # Handle cases where target_depth is outside the DataFrame's depth range
                    monster_row.append(np.nan)
                elif target_depth < depths[0]: #this if for a preforo
                    monster_row.append(np.nan)
                else:
                    try:
                        idx_before, depth_before, idx_after, depth_after = closest(depths, target_depth)

                        value_before = values[idx_before]
                        value_after = values[idx_after]

                        monster_row.append(
                            interpolator_ML(value_after, value_before, depth_before, depth_after, target_depth))
                    except IndexError:
                        monster_row.append(value_after)

        for col in one_row_selected_col:
            vals = df.loc[0,col]
            monster_row.append(vals)

        monster_df.loc[site] = monster_row
        loop.update(1)

    return monster_df
