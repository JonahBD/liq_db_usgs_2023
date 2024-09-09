from modified_for_pga_adj_functions import *
import pandas as pd
import glob, os
from tqdm import tqdm

missing_pga = []
preforo_below_GWT = []
nan_preforo = []
missing_date = []
GWT_or_preforo_wrong_type = []
GWT_zero_nan = []
LD_not_working = []
pga_limited = []
pga_values_hit_lim = []

################ USER INPUTS ############################
input_folder_path = r"C:\Users\hf233\OneDrive - Brigham Young University\Liq\Gabrelle update\OG 2-14"
export_folder_path = r"C:\Users\hf233\OneDrive - Brigham Young University\Liq\Gabrelle update\adj pga one stdev cap HB"
vals_pga_and_liq = r"C:\Users\hf233\OneDrive - Brigham Young University\Liq\PGA-liq values 02 13 23.xlsx"
date_column_name = 'Date of CPT [gg/mm/aa]'
depth_column_name = "Depth (m)"
#########################################################

sites = []

for filename in glob.glob(os.path.join(input_folder_path, "*.xls*")):
    site = os.path.basename(filename).rstrip(".xls").lstrip("Copy of")
    sites.append(site)

loop = tqdm(total=(len(sites)))

for filename in glob.glob(os.path.join(input_folder_path, "*.xls*")):
    site = os.path.basename(filename).rstrip(".xls").lstrip("Copy of")
    # print(site)
    loop.set_description(f"soil parameters - {site} :")

    pga = 0
    eq = 0
    mag = 0
    counter = 0
    liq = 0
    og_pga = 0
    keep_going = True
    export_folder_path_df = os.path.join(export_folder_path, site + '.xlsx')
    while keep_going:
        # print(f'counter: {counter}\n pga: {pga}\n liq: {liq}')
        df = pd.read_excel(filename)

        if df.loc[0]['GWT [m]'] == 0 or df.loc[0]['GWT [m]'] == float('NaN'):
            GWT_zero_nan.append(site)

        date = df.loc[0][date_column_name]
        if date == "-" or date == float('NaN'):
            date = float("NaN")
            missing_date.append(site)

        GWT = df.loc[0]['GWT [m]']
        if not isinstance(GWT, (int, float)):
            GWT_or_preforo_wrong_type.append(site)
            keep_going = False
            continue
        preforo = df.loc[0]["preforo [m]"]
        if not isinstance(preforo, (int, float)):
            GWT_or_preforo_wrong_type.append(site)
            keep_going = False
            continue

        if isinstance(date,pd.Timestamp):
            df.at[0, date_column_name] = date
        else:
            df.at[0, date_column_name] = pd.to_datetime(date, dayfirst=True)


        df = soil_parameters(df, site)

        try:
            if counter == 0:
                df, eq, mag, liq = PGA_insertion(df,vals_pga_and_liq, site)
                og_pga = df.loc[0]['PGA']
            else:
                df.at[0, 'PGA'] = pga
                df.at[0, "EQ"] = eq
                df.at[1, "EQ"] = mag
                df.at[0, 'Liquefaction'] = liq
                df.at[1, "PGA"] = 'OG PGA below'
                df.at[2, 'PGA'] = og_pga
        except KeyError:
            # print("This site is missing its PGA: " + site)
            missing_pga.append(site)
            loop.update(1)
            keep_going = False
            continue

        preforo_checker = preforo_check(df, "GWT [m]", "preforo [m]")
        if preforo_checker == "GWT is above preforo":
            preforo_below_GWT.append(site)
        elif preforo_checker == "Nan preforo":
            nan_preforo.append(site)

        df = FS_liq(df)

        df = h1_h2_basic(df, depth_column_name, "Factor of Safety")
        df = h1_h2_cumulative(df, depth_column_name, "Factor of Safety")
        df = h1_basic_sand_percent(df, depth_column_name)

        df, lpi = LPI(df, depth_column_name, "Factor of Safety")

        df, tow_b = Towhata_2016(df, "LPI", "h1_basic")
        df, tow_c = Towhata_2016(df, "LPI", "h1_cumulative")

        df, lpiish_b = LPIish(df, depth_column_name, "Factor of Safety", "h1_basic")
        df, lpiish_c = LPIish(df, depth_column_name, "Factor of Safety", "h1_cumulative")

        df, lsn = LSN(df, depth_column_name, "qc1ncs", "Factor of Safety", GWT)

        df, ish_b = ishihara_curves(df, 'basic')
        df, ish_c = ishihara_curves(df, 'cumulative')

        df, ld_cr = LD_and_CR(df, "Ic", depth_column_name, "Factor of Safety","Effective Stress (kPa)", "Total Stress (kPa)",'GWT [m]', 'Qtn', 'Fr (%)', 'qt calc')

        df = methods_performance_variable(df)

        if (df.loc[0]['zb'] - df.loc[0]['za']) >= 0.75 * df.loc[0]['h2_cumulative']:
            df.at[0, 'stratified'] = 0
        else:
            df.at[0, 'stratified'] = 1

        if df.loc[0]['clay_profile'] == 1 and df.loc[0]['Liquefaction'] == 0:
            df.at[0, 'exclude'] = 1
        else:
            df.at[0, 'exclude'] = 0


        pga = df.loc[0]['PGA']
        pga_increase_incriment = .05
        # total = lpi + tow_c + tow_b + lpiish_c + lpiish_b + lsn + ish_c + ish_b + ld_cr
        # print(f'total: {total}')

        # print(abs(pga - og_pga))
        upper_bound = float(f"{(og_pga * 10 ** (0.24)):.3f}")
        lower_bound = float(f"{(og_pga * 10 ** (-0.24)):.3f}")
        if pga - og_pga > 0 and pga > upper_bound:
            pga = upper_bound
            continue
        elif pga - og_pga < 0 and pga < lower_bound:
            pga = lower_bound
            continue
        elif pga == upper_bound or pga == lower_bound:
            keep_going = False
            df = df[[depth_column_name, 'qc (MPa)', 'fs (kPa)', 'u (kPa)', 'qt (MPa)', "Rf (%)",
                     "Gamma (kN/m^3)", "Total Stress (kPa)", "Effective Stress (kPa)", "Fr (%)", "Ic",
                     'OCR R', 'OCR K', 'cu_bq (kPa)', 'cu_14 (kPa)', 'su_HB (kPa)', "M (kPa)", "k0_1", 'k0_2', "Vs R (m/s)", 'Vs M (m/s)', "k (m/s)", 'ψ',
                     "φ' R (degrees)",
                     "φ' K (degrees)", "φ' J (degrees)", "φ' M (degrees)", "φ' U (degrees)", 'Dr B', 'Dr K', 'Dr J', 'Dr I', 'qc1n', "u calc (kPa)", "qc1ncs", f'Volumetric Strain (%)',
                     'Kσ', 'Fines Content (%)', 'Shear Stress Reduction Coefficient', "CSR",
                     "CRR", "Factor of Safety", 'h1_basic', 'h2_basic', 'h1_cumulative', 'h2_cumulative', "LPI",
                     f'towhata_basic', f'towhata_cumulative', "LPIish_basic", "LPIish_cumulative", 'LSN', 'LD', 'CR',
                     'za', 'zb',
                     "Unnamed: 5", 'GWT [m]', 'Date of CPT [gg/mm/aa]', 'u [si/no]', 'preforo [m]', 'PGA', "EQ",
                     'Liquefaction', 'clay_profile','exclude', 'stratified', 'h1b_sand_percent',
                     'ishihara_curve_basic_results', 'ishihara_curve_cumulative_results', f'towhata_basic_results',
                     f'towhata_cumulative_results', f'LSN_results', f'LPIish_basic_results',
                     f'LPIish_cumulative_results',
                     'LD_and_CR_results', 'LD_and_CR_binary_results', f'LPI_results', 'methods_perform']]

            df.to_excel(export_folder_path_df, index=False)
            pga_limited.append(site)
            pga_values_hit_lim.append(pga)
            continue


        if df.loc[0]['Liquefaction'] == 1:
            if lpi == 1:
                keep_going = False
            else:
                pga = pga * (pga_increase_incriment + 1)
                counter += 1
        else:
            if lpi == 0:
                keep_going = False
            else:
                pga = pga * (1 - pga_increase_incriment)
                counter += 1
        if counter >= 50:
            keep_going = False
            print(f'Counter hit 50 so you have a problem on site {site}')

        # print(f'pga is {pga} counter is {counter}')




    # Reorder the columns
        df = df[[depth_column_name, 'qc (MPa)', 'fs (kPa)', 'u (kPa)', 'qt (MPa)', "Rf (%)",
                 "Gamma (kN/m^3)", "Total Stress (kPa)", "Effective Stress (kPa)", "Fr (%)", "Ic",
                 'OCR R', 'OCR K', 'cu_bq (kPa)', 'cu_14 (kPa)','su_HB (kPa)', "M (kPa)", "k0_1", 'k0_2', "Vs R (m/s)", 'Vs M (m/s)', "k (m/s)", 'ψ', "φ' R (degrees)",
                 "φ' K (degrees)", "φ' J (degrees)", "φ' M (degrees)", "φ' U (degrees)", 'Dr B', 'Dr K', 'Dr J', 'Dr I', 'qc1n',"u calc (kPa)","qc1ncs", f'Volumetric Strain (%)', 'Kσ', 'Fines Content (%)', 'Shear Stress Reduction Coefficient', "CSR",
                 "CRR", "Factor of Safety",'h1_basic','h2_basic','h1_cumulative','h2_cumulative', "LPI",
                 f'towhata_basic', f'towhata_cumulative',"LPIish_basic", "LPIish_cumulative", 'LSN', 'LD', 'CR', 'za', 'zb',
                 "Unnamed: 5", 'GWT [m]', 'Date of CPT [gg/mm/aa]', 'u [si/no]', 'preforo [m]', 'PGA',"EQ",'Liquefaction','clay_profile', 'stratified',
                 'h1b_sand_percent','ishihara_curve_basic_results','ishihara_curve_cumulative_results', f'towhata_basic_results',
                 f'towhata_cumulative_results',f'LSN_results', f'LPIish_basic_results', f'LPIish_cumulative_results',
                 'LD_and_CR_results', 'LD_and_CR_binary_results', f'LPI_results', 'methods_perform']]

        df.to_excel(export_folder_path_df, index=False)
    loop.update(1)
loop.close()
pga_df = pd.DataFrame({'Missing PGA sites':missing_pga})
preforo_df = pd.DataFrame({'Preforo is below GWT':preforo_below_GWT})
nan_preforo_df = pd.DataFrame({'nan preforo' : nan_preforo})
missing_date_df = pd.DataFrame({'Missing Date':missing_date})
weird_GWT_preforo_df = pd.DataFrame({'GWT or preforo wrong type':GWT_or_preforo_wrong_type})
GWT_zero_nan_df = pd.DataFrame({'GWT zero or missing':GWT_zero_nan})
wrong_LD_df = pd.DataFrame({'LD is wrong': LD_not_working})
high_c_df = pd.DataFrame({'Site with lim pga': pga_limited})
pga_values_c_50_df = pd.DataFrame({'Pga values': pga_values_hit_lim})
sites_to_check = pd.concat([pga_df, preforo_df,nan_preforo_df, missing_date_df,weird_GWT_preforo_df, wrong_LD_df, high_c_df, pga_values_c_50_df], axis=1)
export_folder_path_check_df = os.path.join(export_folder_path,'sites_to_check.xlsx')
sites_to_check.to_excel(export_folder_path_check_df, index=False)