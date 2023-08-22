import pandas as pd
import numpy as np
import warnings
import os, glob
import xlwt
pd.set_option('display.max_columns', None)

def soil_parameters(df):
    Pa = 101.325

    # Add new columns to homogenized excel files to calculate Ic values
    new_columns = ['qc calc', 'qt calc', 'Qt', "Rf (%)", "Gamma (kN/m^3)", "Total Stress (kPa)", "Effective Stress (kPa)",
                   "Fr (%)", 'n1', "Cn", "Qtn", "Ic", 'n2', 'error', 'OCR R', 'OCR K', "cu_bq","cu_14", "M", "k0_1", 'k0_2', "Vs R",
                   'Vs M', "k (m/s)", 'ψ', "φ' R", "φ' K", "φ' J", 'Qtn,cs', "φ' M", "φ' U", 'Dr B', 'Dr K', 'Dr J', 'Dr I',
                   'Cn2', "qc1", 'qc2', 'error2']
    df_new_columns = pd.DataFrame(columns=new_columns)
    df = pd.concat([df, df_new_columns], axis=1)
    df = df[['Depth (m)', 'qc (MPa)', 'fs (kPa)', 'u (kPa)', 'qt (MPa)', 'qc calc', 'qt calc', 'Qt', "Rf (%)", "Gamma (kN/m^3)",
         "Total Stress (kPa)", "Effective Stress (kPa)", "Fr (%)", 'n1', "Cn", "Qtn", "Ic", 'n2', 'error', 'OCR R', 'OCR K',
         'cu_bq','cu_14', "M", "k0_1", 'k0_2', "Vs R", 'Vs M', "k (m/s)", 'ψ', "φ' R", "φ' K", "φ' J", 'Qtn,cs', "φ' M", "φ' U",
         'Dr B', 'Dr K', 'Dr J', 'Dr I', 'Cn2', "qc1", 'qc2', 'error2', "Unnamed: 5", 'GWT [m]', 'Date of CPT [gg/mm/aa]',
         'u [si/no]', 'preforo [m]']]

    # "qc calc" and "qt calc" columns created to turn negative values into 0 and converting units for our calculations without editing the raw data
    df['qc calc'] = df['qc (MPa)'] * 1000
    df['qt calc'] = df['qt (MPa)'] * 1000
    for i in range(len(df.index)):
        row = df.loc[i].copy(deep=False)
        if row['qc calc'] <= 0:
            df.at[i,'qc calc'] = float('NaN')
        if row['qt calc'] <= 0:
            df.at[i,'qt calc'] = float('NaN')


    # Rf calc
    def calcRf(fs, qt_calc):
        if fs < 0.00001:
            return 0
        elif np.isnan(qt_calc) == True:
            return 0
        else:
            return np.divide(fs, qt_calc) * 100


    df['Rf (%)'] = [calcRf(x, y) for x, y in zip(df['fs (kPa)'], df['qt calc'])]


    # Gamma calc
    def calcGamma(Rf, qt_calc):
        if Rf <= 0:
            return 18.08  # default gamma value when there's a pre-hole
        else:
            return 9.81 * (0.27 * np.log10(Rf) + 0.36 * np.log10(qt_calc / Pa) + 1.236)


    df['Gamma (kN/m^3)'] = [calcGamma(x, y) for x, y in zip(df['Rf (%)'], df["qt calc"])]

    # Total Stress calculation
    df['Total Stress (kPa)'] = df['Gamma (kN/m^3)'] * df['Depth (m)']
    for i in range(1, len(df.index)):
        row = df.loc[i]
        previous = df.loc[i - 1]
        df.at[i, 'Total Stress (kPa)'] = (row['Depth (m)'] - previous['Depth (m)']) * row['Gamma (kN/m^3)'] + previous[
            'Total Stress (kPa)']

    # Effective Stress calculation
    if df.loc[0]['GWT [m]'] > 0:
        GWT = df.loc[0]['GWT [m]']
        df['Effective Stress (kPa)'] = df['Total Stress (kPa)']
        for i in range(len(df.index)):
            row = df.loc[i]
            if row['Depth (m)'] >= GWT:
                df.at[i, 'Effective Stress (kPa)'] = row['Total Stress (kPa)'] - ((row['Depth (m)'] - GWT) * 9.81)
    # Fr calcuation
            if row['fs (kPa)'] <= 0:
                df.at[i, 'Fr (%)'] = 0
            else:
                df.at[i, 'Fr (%)'] = (row["fs (kPa)"] / (row["qt calc"] - row['Total Stress (kPa)']) * 100).astype(
                    float)
    else:
        warnings.warn('GWT marked as 0 or not provided on ' + str(filename))



    # Qt calculation
    df['Qt'] = [(x - y) / z for x, y, z in zip(df["qt calc"], df["Total Stress (kPa)"], df['Effective Stress (kPa)'])]

    # Ic calculation Rollins
    df['n1'] = 1  # Use 1 as the first guess for n
    tolerance = 0.01  # Define the Ic iteration tolerance here
    counter = False

    while counter == False:
        # Calculate Cn
        df['Cn'] = (Pa / df['Effective Stress (kPa)']) ** df['n1']
        df['Cn'] = [1.7 if x >= 1.7 else x for x in df['Cn']]

        # Calculate Qtn
        df['Qtn'] = (((df["qt calc"] - df['Total Stress (kPa)']) / Pa) * df['Cn']).astype(float)

        # Calculate Ic
        for i in range(len(df.index)):
            row = df.loc[i]
            if row['Fr (%)'] <= 0 or row['Qtn'] <= 0:
                df.at[i, 'Ic'] = 0
            elif row['Fr (%)'] == float('NaN') or row['Qtn'] == float('NaN'):
                df.at[i, 'Ic'] = float('NaN')
            else:
                df.at[i, 'Ic'] = (((3.47 - np.log10(row['Qtn'])) ** 2) + (np.log10(row['Fr (%)']) + 1.22) ** 2) ** 0.5

        # Calculate n2
        for i in range(len(df.index)):
            row = df.loc[i]
            temp = 0.381 * (row['Ic']) + 0.05 * (row['Effective Stress (kPa)'] / Pa) - .15
            if temp > 1:
                df.at[i, 'n2'] = 1
            else:
                df.at[i, 'n2'] = temp
        # Calculate the error and set n2 as n1 for further iterations
        df['error'] = df['n1'] - df['n2']
        df['n1'] = df['n2']

        counter1 = True
        # Check to see if every row meets our error tolerance. If not, repeat the process
        for i in range(len(df.index)):
            row = df.loc[i]
            if row['Ic'] > 0 and row['error'] > tolerance:
                counter1 = False
                break

        counter = counter1

    # Dr calculation Idriss and Boulanger 2008
    df['qc1'] = df['qc calc']
    tolerance = 0.01  # Define the Dr iteration tolerance here

    counter = False
    it_counter = 0

    while counter == False:
        df['Cn2'] = (Pa / df['Effective Stress (kPa)']) ** (1.338 - .249 * df['qc1'] ** .264)
        df['qc2'] = df['Cn2'] * df['qc calc'] / Pa
        df['Dr I'] = .478 * df['qc1'] ** .264 - 1.063
        df['error2'] = np.abs(df['qc1'] - df['qc2'])

        df['qc1'] = df['qc2']

        it_counter += 1

        counter1 = True
        # Check to see if every row meets our error tolerance. If not, repeat the process
        for i in range(len(df.index)):
            row = df.loc[i]
            if it_counter == 100:
                if row['Dr I'] > 0 and row['error2'] > tolerance:
                    df.at[i, 'Dr I'] = 'No Solution'
            else:
                if row['Dr I'] > 0 and row['error2'] > tolerance:
                    counter1 = False
                    break

        counter = counter1

    # Cohesive Layer Properties
    # OCR calculations
    # Robertson 2009
    def calcOCR_R(Ic, Qt):
        if Ic >= 2.6:
            return .25 * Qt ** 1.25


    df['OCR R'] = [calcOCR_R(x, y) for x, y in zip(df['Ic'], df['Qt'])]


    # Kulkawy and Mayne 1990
    def calcOCR_K(Ic, Qt):
        k = 0.33  # An average value of k = 0.33 can be assumed, with an expected range of 0.2 to 0.5. Higher values of k are recommended in aged, heavily overconsolidated clays.
        if Ic >= 2.6 and Qt < 20:
            return k * Qt


    df['OCR K'] = [calcOCR_K(x, y) for x, y in zip(df['Ic'], df['Qt'])]

    for i in range(len(df.index)):
        row = df.loc[i]
        if row['Ic'] >= 2.6:
            df.at[i, 'Dr I'] = float('NaN')
        if row['Ic'] == 0:
            df.at[i, 'Dr I'] = float('NaN')

        if row["Ic"] >= 2.6:

        # cu calculations Lunne et al. 1997
            # Anagnostopoulos et al. 2003
            GWT = df.loc[0]['GWT [m]']
            if row['Depth (m)'] >= GWT:
                u0 = (row['Depth (m)'] - GWT) * 9.81
            else:
                u0 = 0
            Bq = (row['u (kPa)'] - u0) / (row['qt calc'] - row['Total Stress (kPa)'])
            if Bq <= -0.1:
                Bq = -0.009999999
            Nkt = 10.5 - 4.6 * np.log(Bq + 0.1)
            df.at[i, 'cu_bq'] = (row['qt calc'] - row['Total Stress (kPa)']) / Nkt
            df.at[i, 'cu_14'] = (row['qt calc'] - row['Total Stress (kPa)']) / 14  # Dr. Rollins wanted to use a set value of Nkt = 14 in addition to the bq calc since he is unfamiliar with bq

        # M calculations
            # Robertson 2009. From what I can tell from the paper, M is in MPa
            if row['Qt'] >= 14:
                df.at[i, 'M'] = (row['qt calc'] - row['Total Stress (kPa)']) * 14
            else:
                df.at[i, 'M'] = (row['qt calc'] - row['Total Stress (kPa)']) * row['Qt']

        # k0 calculations Kulhway and Mayne 1990
            df.at[i, 'k0_1'] = (row['qt calc'] - row['Total Stress (kPa)']) / row['Effective Stress (kPa)'] * .1
            df.at[i, 'k0_2'] = 0.5 * (row['OCR R']) ** 0.5

        # Vs calculation
            # Robertson 2009
            avs = 10 ** (0.55 * row['Ic'] + 1.68)
            if (avs * (row['qt calc'] - row['Total Stress (kPa)'])) > 0:
                df.at[i, 'Vs R'] = (avs * (row['qt calc'] - row['Total Stress (kPa)']) / Pa) ** .5

            # Mayne 2006
            if row['fs (kPa)'] > 0:
                df.at[i, 'Vs M'] = 51.6 * np.log(row['fs (kPa)']) + 18.5

        # k for permeability from Robertson 2015
            if row['Ic'] < 3.27:
                df.at[i, 'k (m/s)'] = 10 ** (.952 - 3.04 * row['Ic'])
            if row['Ic'] > 3.27 and row['Ic'] < 4:
                df.at[i, 'k (m/s)'] = 10 ** (-4.52 - 1.37 * row['Ic'])

        # ψ state parameter calculation from Robertson 2010
        #     df.at[i, 'ψ'] = (5.581 * row['Ic'] ** 3 - 0.403 * row['Ic'] ** 4 - 21.63 * row['Ic'] ** 2 + 33.75 * row['Ic'] - 17.88) * ((row['qt calc'] - row['Total Stress (kPa)']) / Pa) * (Pa / row['Effective Stress (kPa)']) ** (0.381 * row['Ic'] + 0.05 * (row['Effective Stress (kPa)'] / Pa) - 0.15)

            # φ' Mayne 2006
            GWT = df.loc[0]['GWT [m]']
            if row['Depth (m)'] >= GWT:
                u0 = (row['Depth (m)'] - GWT) * 9.81
            else:
                u0 = 0
            Bq = (row['u (kPa)'] - u0) / (row['qt calc'] - row['Total Stress (kPa)'])
            if Bq <= 0:
                Bq = 0.1
            elif Bq > 1:
                Bq = 1
            if row['Qt'] > 0:
                df.at[i, "φ' M"] = 29.5 * Bq ** 0.121 * (0.256 + 0.336 * Bq + np.log10(row['Qt']))
            # if row["φ' M"] > 40:
            #   df.at[i,"φ' M"] = 40
            # elif row["φ' M"] < 20:
            #   df.at[i,"φ' M"] = 20

    # Non-cohesive Layer Properties

    for i in range(len(df.index)):
        row = df.loc[i]
        if row['Ic'] < 2.6 and row['Ic'] > 0:
        # φ' calculation
            # Robertson and Campanella 1983
            if row['qc calc'] > 0:
                df.at[i, "φ' R"] = np.degrees(np.arctan(1 / 2.68 * (np.log10(row['qc calc'] / row['Effective Stress (kPa)']) + 0.29)))
            # Kulhawy and Mayne 1990
            df.at[i, "φ' K"] = 17.6 + 11 * np.log10(row['Qtn'])

            # Jefferies and Been 2006
            if row['Ic'] <= 1.64:
                Kc = 1.0
            elif row['Ic'] > 1.64 and row['Ic'] < 2.36 and row['Fr (%)'] < 0.5:
                Kc = 1.0
            elif row['Ic'] > 1.64 and row['Ic'] <= 2.5:
                Kc = 5.58 * (row["Ic"]) ** 3 - 0.403 * (row["Ic"]) ** 4 - 21.63 * (row["Ic"]) ** 2 + 33.75 * (
                row["Ic"]) - 17.88
            else:
                Kc = 6 * 10 ** -7 * row['Ic'] ** 16.76
            df.at[i, "φ' J"] = 33 + 15.84 * (
                np.log10(Kc * row['Qtn'])) - 26.88  # Used a φ'cv value of 33 degrees per Dr. Rollins' instructions

            df.at[i, 'Qtn,cs'] = Kc * row['Qtn']

            # Uzielli, Mayne, and Cassidy 2013
            df.at[i, "φ' U"] = 25 * (row['qt calc'] / (row['Effective Stress (kPa)']) ** 0.5) ** 0.1

        # DR calculation
            # Baldi et al. 1986      ******WEIRD NUMBERS**********
            C0, C2 = 15.7, 2.41  # For moderately compressible, normally consolidated, unaged and uncemented, predominantly quartz sands the constants are: C0 = 15.7 and C2 = 2.41
            Qcn = (row['qc calc'] / Pa) / (row['Effective Stress (kPa)'] / Pa) ** 0.5
            df.at[i, 'Dr B'] = (1 / C2) * np.log(Qcn / C0)

            # Kulhawy and Mayne 1990
            df.at[i, 'Dr K'] = (row[
                                    'Qtn'] / 350) ** 0.5  # Used the Qtn/350 simplification of this equation per Dr. Rollins' instructions since we don't have the needed information for the non-simplified version of the equation

            # Jamiolkowski et al. 2003
            c0 = 17.68
            c1 = 0.5
            c2 = 3.10
            df.at[i, 'Dr J'] = 1 / c2 * np.log((row['qt calc'] / Pa) / (c0 * (row['Effective Stress (kPa)'] / Pa) ** c1))

        # ψ state parameter calculation from Robertson 2010
            df.at[i, 'ψ'] = 0.56 - 0.33 * np.log10(Kc * row['Qtn'])

        # Vs calculation
            # Robertson 2009
            avs = 10 ** (0.55 * row['Ic'] + 1.68)
            df.at[i, 'Vs R'] = (avs * (row['qt calc'] - row['Total Stress (kPa)']) / Pa) ** 0.5

            # Mayne 2006
            if row['fs (kPa)'] > 0:
                df.at[i, 'Vs M'] = 51.6 * np.log(row['fs (kPa)']) + 18.5

        # k for permeability from Robertson 2010
            df.at[i, 'k (m/s)'] = 10 ** (0.952 - 3.04 * row['Ic'])

    df.drop(['qc calc','qt calc','Qt','n1','Cn','Qtn','n2','error','qc1','qc2','error2','Cn2','Qtn,cs'], axis=1,inplace=True)
    return df

folder_path = r"C:\Users\jdundas2\Documents\Step 5 downloads\5. CPTU standard excel (1685 items)"
for filename in glob.glob(os.path.join(folder_path, "*.xls*")):
    df = pd.read_excel(filename)
    df = soil_parameters(df)
    filename = filename.replace("5. CPTU standard excel (1685 items)","Calculated Soil Parameters (trial 1)")
    ending = filename[-1]
    if ending == 'x':
        df.to_excel(filename, index=False)
    else:
        filename = filename.replace('.xls','.xlsx')
        df.to_excel(filename, index=False)



# df = pd.read_excel(r"C:\Users\jdundas2\Documents\Code Checks\Mirabello Italy check sheet.xlsx")
# df = soil_parameters(df)
# df.to_excel(r"C:\Users\jdundas2\Documents\Code Checks\Mirabello final check with calcs.xlsx", index=False)
