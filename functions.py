import pandas as pd
import numpy as np
import warnings
import scipy.integrate as integrate


def soil_parameters(df, site):
    Pa = 101.325  # Atmospheric pressure in kPa

    # /////////////////////////////////////////////// COLUMNS \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
    # Add new columns for each of the soil parameters
    new_columns = ['u calc', 'qc calc', 'qt calc', 'Qt', "Rf (%)", "Gamma (kN/m^3)", "Total Stress (kPa)",
                   "Effective Stress (kPa)",
                   "Fr (%)", 'n1', "Cn", "Qtn", "Ic", 'n2', 'error', 'OCR R', 'OCR K', "cu_bq", "cu_14", "M", "k0_1",
                   'k0_2', "Vs R",
                   'Vs M', "k (m/s)", 'ψ', "φ' R", "φ' K", "φ' J", 'Qtn,cs', "φ' M", "φ' U", 'Dr B', 'Dr K', 'Dr J',
                   'Dr I',
                   'Cn2', "qc1", 'qc2', 'error2']
    df_new_columns = pd.DataFrame(columns=new_columns)
    df = pd.concat([df, df_new_columns], axis=1)

    # /////////////////////////////////////////////// end COLUMNS \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

    # ///////////////////////////////////////////// GENERAL CALCULATIONS \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
    # "qc calc" and "qt calc" columns created to change bad data into numbers our equations can handle. Units are also converted

    qc_og = df['qc (MPa)']
    fs_og = df['fs (kPa)']
    qt_og = df['qt (MPa)']

    if df.loc[0]['Depth (m)'] < df.loc[0]['preforo [m]']:
        df['qc (MPa)'] = [float('Nan') if x < df.loc[0]['preforo [m]'] else y for x, y in zip(df['Depth (m)'], df['qc (MPa)'])]
        df['fs (kPa)'] = [float('Nan') if x < df.loc[0]['preforo [m]'] else y for x, y in zip(df['Depth (m)'], df['fs (kPa)'])]
        df['qt (MPa)'] = [float('Nan') if x < df.loc[0]['preforo [m]'] else y for x, y in zip(df['Depth (m)'], df['qt (MPa)'])]
    df['qc calc'] = df['qc (MPa)'] * 1000
    df['qt calc'] = df['qt (MPa)'] * 1000
    for i in range(len(df.index)):
        row = df.loc[i].copy(deep=False)
        if row['qc calc'] <= 0:
            df.at[i, 'qc calc'] = float('NaN')
        if row['qt calc'] <= 0:
            df.at[i, 'qt calc'] = float('NaN')

    # Rf calc
    def calcRf(fs, qt_calc):
        if fs < 0.00001:
            return 0
        elif np.isnan(qt_calc):
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

        df['u calc'] = 0

        for i in range(len(df.index)):
            row = df.loc[i]
            if row['Depth (m)'] >= GWT:
                df.at[i, 'Effective Stress (kPa)'] = row['Total Stress (kPa)'] - ((row['Depth (m)'] - GWT) * 9.81)
                df.at[i, 'u calc'] = ((row['Depth (m)'] - GWT) * 9.81).astype(np.int64)
                # print(type(row["u (kPa)"]), type(row["u (kPa)"]))
            # Fr calcuation
            if row['fs (kPa)'] <= 0:
                df.at[i, 'Fr (%)'] = 0
            else:
                df.at[i, 'Fr (%)'] = (row["fs (kPa)"] / (row["qt calc"] - row['Total Stress (kPa)']) * 100).astype(
                    float)
    else:
        GWT = df.loc[0]['GWT [m]']
        df['Effective Stress (kPa)'] = df['Total Stress (kPa)']

        df['u calc'] = 0

        for i in range(len(df.index)):
            row = df.loc[i]
            if row['Depth (m)'] >= GWT:
                df.at[i, 'Effective Stress (kPa)'] = row['Total Stress (kPa)'] - ((row['Depth (m)'] - GWT) * 9.81)
                df.at[i, 'u calc'] = ((row['Depth (m)'] - GWT) * 9.81).astype(np.int64)
                # print(type(row["u (kPa)"]), type(row["u (kPa)"]))
            # Fr calcuation
            if row['fs (kPa)'] <= 0:
                df.at[i, 'Fr (%)'] = 0
            else:
                df.at[i, 'Fr (%)'] = (row["fs (kPa)"] / (row["qt calc"] - row['Total Stress (kPa)']) * 100).astype(
                    float)
        GWT_zero_confirmed = ["038022P239CPTU245", '038016P302CPTU302', '038003P980CPTU1080', '036010P13CPTU13']
        if site not in GWT_zero_confirmed:
            warnings.warn(f'{site} GWT marked as 0 or not provided')

    # Qt calculation
    df['Qt'] = [(x - y) / z for x, y, z in zip(df["qt calc"], df["Total Stress (kPa)"], df['Effective Stress (kPa)'])]
    df["Qt"] = [0 if x < 0 else x for x in df["Qt"]]
    # ///////////////////////////////////////////// end GENERAL CALCULATIONS \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

    # ////////////////////////////////////////////// Ic CALCULATION \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
    df['n1'] = 1  # Use 1 as the first guess for n
    tolerance = 0.01  # Define the Ic iteration tolerance here
    counter = False

    while not counter:
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

        # Check to see if every row meets our error tolerance. If not, repeat the process
        counter1 = True
        for i in range(len(df.index)):
            row = df.loc[i]
            if row['Ic'] > 0 and row['error'] > tolerance:
                counter1 = False
                break
        counter = counter1
    # /////////////////////////////////////////// end Ic CALCULATION \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

    # df['Cn'] = (Pa / df['Effective Stress (kPa)'])**0.5 # NOTE: this is the simpler form of finding qc1n found on page 89 of the Idriss and Boulanger book
    # df['Cn'] = [1.7 if x >= 1.7 else x for x in df['Cn']]
    # df['qc1n'] = df['Cn'] * df['qc calc'] / Pa
    # df['Dr I'] = 0.478 * df['qc1n']**0.264 - 1.063

    # df['FC'] = 2 * 2.8 * df["Ic"] ** 2.6  # Taken from Emilia Romagna paper
    # Ic = df['Ic']
    # df['Kc'] = 5.581 * Ic**3 - 0.403 * Ic**4 - 21.63 * Ic**2 + 33.75 * Ic - 17.88
    # df['Kc'] = [1 if x <= 1.64 else y for x, y in zip(df['Ic'], df['Kc'])]
    # df["Kc"] = [1 if ((1.64 < x < 2.36) and z < 0.5) else y for x, y, z in zip(df['Ic'],df['Kc'], df['Fr (%)'])]
    # df["Kc"] = [float('nan') if x > 2.6 else y for x, y in zip(df['Ic'], df['Kc'])]
    # df['qc1ncs_cameron'] = df['Kc'] * df['Qtn']

    # //////////////////////////////// Dr CALCULATION Idriss and Boulanger 2008 \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

    df['qc1'] = df['qc calc']  # Set recorded qc values as initial qc1n guess
    tolerance = 0.01  # Define the Dr iteration tolerance here

    counter = False
    it_counter = 0  # Create variable to count the number of iterations

    while not counter:
        # Cn calculation
        df['m'] = (1.338 - 0.249 * (df['qc1'] / Pa) ** 0.264)
        # df['m'] = [0.264 if x < 0.264 else x for x in df['m']] # NOTE: the cap on "m" is based on I&B 2014 method
        # df['m'] = [0.782 if x > 0.782 else x for x in df['m']]
        df['Cn2'] = (Pa / df['Effective Stress (kPa)']) ** df['m']
        df['Cn2'] = [1.7 if x >= 1.7 else x for x in df['Cn2']]

        # New qc1 calculation
        df['qc2'] = df['Cn2'] * df['qc calc']

        # Dr calculation
        df['Dr I'] = .478 * ((df['qc1'] / Pa) ** .264) - 1.063

        # Find error between guess and new qcn1 calculation
        df['error2'] = np.abs(df['qc1'] - df['qc2'])

        # Set new qc1n calculation as new guess for next iteration
        df['qc1'] = df['qc2']

        # Count the number of iterations
        it_counter += 1

        # Check to see if every row meets our error tolerance. If not, repeat the process.
        # If there have been more than 100 iterations, set the value to Nan
        counter1 = True
        for i in range(len(df.index)):
            row = df.loc[i]
            if it_counter == 100:
                if row['Dr I'] > 0 and row['error2'] > tolerance:
                    df.at[i, 'Dr I'] = float('Nan')
            else:
                if row['Dr I'] > 0 and row['error2'] > tolerance:
                    counter1 = False
                    break

        counter = counter1

    # //////////////////////////////////// end Dr CALCULATION Idriss and Boulanger 2008 \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

    # //////////////////////////////////////////// COHESIVE LAYER PROPERTIES \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

    # ---------------------------------------- OCR calculations --------------------------------------------------------
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
    # -----------------------------------end OCR calculations ----------------------------------------------------------

    # Begin for loop to perform cell based calculations
    for i in range(len(df.index)):
        row = df.loc[i]
        if row['Ic'] >= 2.6:
            df.at[i, 'Dr I'] = float('NaN')
        if row['Ic'] == 0:
            df.at[i, 'Dr I'] = float('NaN')

        if row["Ic"] >= 2.6:  # Check the soil type

            # --------------------------- cu calculations --------------------------------------------------------------
            # Mayne & Peuchen 2018
            GWT = df.loc[0]['GWT [m]']
            if row['Depth (m)'] >= GWT:
                u0 = (row['Depth (m)'] - GWT) * 9.81
            else:
                u0 = 0
            Bq = (row['u calc'] - u0) / (row['qt calc'] - row['Total Stress (kPa)'])
            if Bq <= -0.1:
                Bq = -0.009999999
            Nkt = 10.5 - 4.6 * np.log(Bq + 0.1)
            df.at[i, 'cu_bq'] = (row['qt calc'] - row['Total Stress (kPa)']) / Nkt
            df.at[i, 'cu_14'] = (row['qt calc'] - row[
                'Total Stress (kPa)']) / 14  # Dr. Rollins wanted to use a set value of Nkt = 14 in addition to the bq calc since he is unfamiliar with bq

            #from Hutabarat and Bray 2022 method to calculate CR and LD
            IB = 100 * (row['Qtn'] + 10) / (row['Qtn'] * row['Fr (%)'] + 70)

            Nkt = 15
            K0 = 0.5
            phi_cs = 33
            if IB <= 22:
                df.at[i, 'su_HB'] = (row['qt calc'] - row['Total Stress (kPa)']) / Nkt
            else:
                df.at[i, 'su_HB'] = K0 * row['Effective Stress (kPa)'] * np.tan(phi_cs * np.pi / 180)
            # -------------------------- end cu calculations -----------------------------------------------------------

            # ----------------------------- M calculations -------------------------------------------------------------
            # Robertson 2009. From what I can tell from the paper, M is in MPa
            if row['Qt'] >= 14:
                df.at[i, 'M'] = (row['qt calc'] - row['Total Stress (kPa)']) * 14
            else:
                df.at[i, 'M'] = (row['qt calc'] - row['Total Stress (kPa)']) * row['Qt']
            # ------------------------------- end M calculations -------------------------------------------------------

            # -------------------------------k0 calculations -----------------------------------------------------------
            # Kulhway and Mayne 1990
            df.at[i, 'k0_1'] = (row['qt calc'] - row['Total Stress (kPa)']) / row['Effective Stress (kPa)'] * .1
            df.at[i, 'k0_2'] = 0.5 * (row['OCR R']) ** 0.5
            # -------------------------------end k0 calculations -------------------------------------------------------

            # ------------------------------- Vs calculation -----------------------------------------------------------
            # Robertson 2009
            avs = 10 ** (0.55 * row['Ic'] + 1.68)
            if (avs * (row['qt calc'] - row['Total Stress (kPa)'])) > 0:
                df.at[i, 'Vs R'] = (avs * (row['qt calc'] - row['Total Stress (kPa)']) / Pa) ** .5

            # Mayne 2006
            if row['fs (kPa)'] > 0:
                df.at[i, 'Vs M'] = 51.6 * np.log(row['fs (kPa)']) + 18.5
            # ---------------------------------end Vs calculation ------------------------------------------------------

            # --------------------------------k for permeability -------------------------------------------------------
            # Robertson 2015
            if row['Ic'] < 3.27:
                df.at[i, 'k (m/s)'] = 10 ** (.952 - 3.04 * row['Ic'])
            if 3.27 < row['Ic'] < 4:
                df.at[i, 'k (m/s)'] = 10 ** (-4.52 - 1.37 * row['Ic'])
            # --------------------------------end k for permeability ---------------------------------------------------

            # ------------------------------- φ' calculation -----------------------------------------------------------
            # Mayne 2006
            GWT = df.loc[0]['GWT [m]']
            if row['Depth (m)'] >= GWT:
                u0 = (row['Depth (m)'] - GWT) * 9.81
            else:
                u0 = 0
            Bq = (row['u calc'] - u0) / (row['qt calc'] - row['Total Stress (kPa)'])
            if Bq <= 0:
                Bq = 0.1
            elif Bq > 1:
                Bq = 1
            if row['Qt'] > 0:
                df.at[i, "φ' M"] = 29.5 * Bq ** 0.121 * (0.256 + 0.336 * Bq + np.log10(row['Qt']))
            # ----------------------------- end φ' calculation ---------------------------------------------------------
    # /////////////////////////////////////// end COHESIVE LAYER PROPERTIES \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

    # /////////////////////////////////////// NON-COHESIVE LAYER PROPERTIES \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\
    # Begin for loop to perform cell based calculations
    for i in range(len(df.index)):
        row = df.loc[i]
        if 2.6 > row['Ic'] > 0:  # Check the soil type. Ic == 0 means there's not data.

            # ---------------------------------------- φ' calculation --------------------------------------------------
            # Robertson and Campanella 1983
            if row['qc calc'] > 0:
                df.at[i, "φ' R"] = np.degrees(
                    np.arctan(1 / 2.68 * (np.log10(row['qc calc'] / row['Effective Stress (kPa)']) + 0.29)))

            # Kulhawy and Mayne 1990
            df.at[i, "φ' K"] = 17.6 + 11 * np.log10(row['Qtn'])

            # Jefferies and Been 2006
            if row['Ic'] <= 1.64:
                Kc = 1.0
            elif 1.64 < row['Ic'] < 2.36 and row['Fr (%)'] < 0.5:
                Kc = 1.0
            elif 1.64 < row['Ic'] <= 2.5:
                Kc = 5.58 * (row["Ic"]) ** 3 - 0.403 * (row["Ic"]) ** 4 - 21.63 * (row["Ic"]) ** 2 + 33.75 * (
                    row["Ic"]) - 17.88
            else:
                Kc = 6 * 10 ** -7 * row['Ic'] ** 16.76
            df.at[i, "φ' J"] = 33 + 15.84 * (
                np.log10(Kc * row['Qtn'])) - 26.88  # Used a φ'cv value of 33 degrees per Dr. Rollins' instructions

            # df.at[i, 'Qtn,cs'] = Kc * row['Qtn'] -------- if we want to check Qtn,cs values for checking here you go

            # Uzielli, Mayne, and Cassidy 2013
            df.at[i, "φ' U"] = 25 * (row['qt calc'] / (row['Effective Stress (kPa)']) ** 0.5) ** 0.1
            # ------------------------------------- end φ' calculation -------------------------------------------------

            # ------------------------------------------- DR calculation -----------------------------------------------
            # Baldi et al. 1986      ******WEIRD NUMBERS**********
            C0, C2 = 15.7, 2.41  # For moderately compressible, normally consolidated, unaged and uncemented, predominantly quartz sands the constants are: C0 = 15.7 and C2 = 2.41
            Qcn = (row['qc calc'] / Pa) / (row['Effective Stress (kPa)'] / Pa) ** 0.5
            df.at[i, 'Dr B'] = (1 / C2) * np.log(Qcn / C0)

            # Kulhawy and Mayne 1990
            df.at[i, 'Dr K'] = (row['Qtn'] / 350) ** 0.5  # Used the Qtn/350 simplification of this equation per
            # Dr. Rollins' instructions since we don't have the needed
            # information for the non-simplified version of the equation

            # Jamiolkowski et al. 2003
            c0 = 17.68
            c1 = 0.5
            c2 = 3.10
            df.at[i, 'Dr J'] = 1 / c2 * np.log(
                (row['qt calc'] / Pa) / (c0 * (row['Effective Stress (kPa)'] / Pa) ** c1))
            # -------------------------------------- end DR calculation ------------------------------------------------

            # ---------------------------------- ψ state parameter calculation -----------------------------------------
            # Robertson 2010
            df.at[i, 'ψ'] = 0.56 - 0.33 * np.log10(Kc * row['Qtn'])
            # ---------------------------------- end  ψ state parameter calculation ------------------------------------

            # ------------------------------------- Vs calculation -----------------------------------------------------
            # Robertson 2009
            avs = 10 ** (0.55 * row['Ic'] + 1.68)
            df.at[i, 'Vs R'] = (avs * (row['qt calc'] - row['Total Stress (kPa)']) / Pa) ** 0.5

            # Mayne 2006
            if row['fs (kPa)'] > 0:
                df.at[i, 'Vs M'] = 51.6 * np.log(row['fs (kPa)']) + 18.5
            # ------------------------------------- end Vs calculation -------------------------------------------------

            # --------------------------------- k for permeability -----------------------------------------------------
            # Robertson 2010
            df.at[i, 'k (m/s)'] = 10 ** (0.952 - 3.04 * row['Ic'])
            # --------------------------------- end k for permeability -------------------------------------------------

            # ----------------------------------------- M --------------------------------------------------------------
            # Robertson 2009. From what I can tell from the paper, M is in MPa
            if row['Ic'] > 2.2:
                if row['Qt'] >= 14:
                    df.at[i, 'M'] = (row['qt calc'] - row['Total Stress (kPa)']) * 14
                else:
                    df.at[i, 'M'] = (row['qt calc'] - row['Total Stress (kPa)']) * row['Qt']
            else:
                am = 0.0188 * (10 ** (0.55 * row['Ic'] + 1.68))
                df.at[i, 'M'] = am * (row['qt calc'] - row['Total Stress (kPa)'])
            # ------------------------------------- end M --------------------------------------------------------------

            # ------------------------------------- su -----------------------------------------------------------------
            # from Hutabarat and Bray 2022 method to calculate CR and LD
            IB = 100 * (row['Qtn'] + 10) / (row['Qtn'] * row['Fr (%)'] + 70)
            Nkt = 15
            K0 = 0.5
            phi_cs = 33
            if IB <= 22:
                df.at[i, 'su_HB'] = (row['qt calc'] - row['Total Stress (kPa)']) / Nkt
            else:
                df.at[i, 'su_HB'] = K0 * row['Effective Stress (kPa)'] * np.tan(phi_cs * np.pi / 180)
            # ------------------------------------- end su -------------------------------------------------------------
        elif row['Ic'] == 0:
            df.at[i, 'Ic'] = float('NaN')

    # //////////////////////////////////////// end NON-COHESIVE LAYER PROPERTIES \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\

    # Delete columns that stored variables for calculations but that we don't want in the final spreadsheet
    df.drop(['qc calc', 'Qt', 'n1', 'Cn', 'n2', 'error', 'qc1', 'qc2', 'error2', 'Cn2', 'Qtn,cs'],
            axis=1, inplace=True) #, 'Qtn' #NOTE: Took QTN out for Cr function to use
    df['qc (MPa)'] = qc_og
    df['fs (kPa)'] = fs_og
    df['qt (MPa)'] = qt_og
    return df


def PGA_insertion(df, PGA_filepath, site):
    pga_df = pd.read_excel(PGA_filepath)
    pga_df.set_index('site', inplace=True)
    if pga_df.loc[site]['PGA_20may'] > pga_df.loc[site]['PGA_29may']:
        df.at[0, 'PGA'] = pga_df.loc[site]['PGA_20may']
        df.at[0,"EQ"] = "20_may"
        df.at[1,"EQ"] = 6.1
    else:
        df.at[0, 'PGA'] = pga_df.loc[site]['PGA_29may'] # NOTE: change this back to 29may when not comparing with cliq files
        df.at[0, "EQ"] = "29_may"
        df.at[1, "EQ"] = 5.9
    # df.at[0, 'PGA_20may'] = pga_df.loc[site]['PGA_20may']
    # df.at[0, 'PGA_29may'] = pga_df.loc[site]['PGA_29may']
    df.at[0, 'Liquefaction'] = pga_df.loc[site]['Liquefaction']
    return df


# input df must have PGA and Liquefaction values already defined
def FS_liq(df):  # FS equation from Idriss and Boulanger 2008
    Pa = 101.325
    magnitude = df.loc[1,"EQ"]
    new_columns = ['qc1n', 'qc1ncs', 'Kσ', 'rd', "CRR", "CSR", "FS"]
    df_new_columns = pd.DataFrame(columns=new_columns)
    df = pd.concat([df, df_new_columns], axis=1)

    if df.loc[0]["GWT [m]"] < df.loc[0]['preforo [m]']:
        df.at[1, 'preforo [m]'] = 'preforo is below GWT'

    # FSliq part
    MSF = 6.9 * np.exp(-magnitude / 4) - .058
    if MSF > 1.8:
        MSF = 1.8

    # Calculating K sigma
    for i in range(len(df.index)):
        row = df.loc[i]  # this takes a screenshot
        if np.isnan(row['Dr I']) is True:
            df.at[i, 'qc1n'] = float('NaN')
        else:
            df.at[i, 'qc1n'] = ((row['Dr I'] + 1.063) / .478) ** (
                        1 / .264)  # from Dr I iterative calc (we backcalculate here)
        row = df.loc[i]

        FC = 2 * 2.8 * row["Ic"] ** 2.6  # Taken from Emilia Romagna paper
        if FC > 100:
            FC = 100
        elif FC < 0:
            FC = 0
        df.at[i, 'FC'] = FC

        qc1ncs = row["qc1n"] + (5.4 + row['qc1n'] / 16) * np.exp(
            1.63 + 9.7 / (FC + 0.01) - (15.7 / (FC + 0.01)) ** 2)
        df.at[i, "qc1ncs"] = qc1ncs

        row = df.loc[i]

        if 2.6 > row["Ic"] > 0:
            c_sigma = 1 / (37.3 - 8.27 * row['qc1n'] ** .264)# NOTE: Idriss and Boulganger 2008 uses qc1n while I&B 2014 uses qc1ncs
            if c_sigma > .3:
                c_sigma = .3

            Kσ = 1 - c_sigma * np.log(row["Effective Stress (kPa)"] / Pa)
            if Kσ > 1.1:
                Kσ = 1.1
            df.at[i, 'Kσ'] = Kσ

            # Calculating rd
            alpha = -1.012 - 1.126 * np.sin(
                row['Depth (m)'] / 11.73 + 5.133)  # rd is only good for depths less than 20 meters (pg 68)
            beta = .106 + .118 * np.sin(row['Depth (m)'] / 11.28 + 5.142)
            if row['Depth (m)'] <= 34: # NOTE: I&B 2008 caps this at 20, Cliq caps at 34
                rd = np.exp(alpha + beta * magnitude)
            else:
                rd = 0.12 * np.exp(0.22 * magnitude)
            if rd > 1:
                rd = 1
            df.at[i, 'rd'] = rd

            row = df.loc[i]

            # Calcuating CSR
            g = 1
            df.at[i, "CSR"] = .65 * df.loc[0, "PGA"] / g * row["Total Stress (kPa)"] / row[
                "Effective Stress (kPa)"] * row["rd"] / MSF / row['Kσ']

            row = df.loc[i]

            # Calcuatig CRR # NOTE: When qc1ncs is greater than about 250 it will throw an overflow error and generates inf values (ex. 036010P218CPTU218)
            with warnings.catch_warnings():
                warnings.filterwarnings("ignore", message="overflow encountered in exp")
                df.at[i, "CRR"] = np.exp(qc1ncs / 540 + (qc1ncs / 67) ** 2 - (qc1ncs / 80) ** 3 + (qc1ncs / 114) ** 4 - 3) #/ MSF1 / row["Kσ"]

            row = df.loc[i]

            # FS liq
            if row["Depth (m)"] <= df.loc[0]['GWT [m]']:
                df.at[i, "FS"] = 9999
            else:
                df.at[i, "FS"] = row['CRR'] / row['CSR']

    return df


# calculates h2 as the thickness of the shallowest liquefiable layer greater than 0.3 meters
# **h2 includes any non-liquefiable soil with thickness less than 0.3 meters**
def h1_h2_basic(df, depth_column_name, FS_column_name):
    # Initialize variables
    last_liq_depth = None
    start_liq_depth = None
    thick_liq = 0
    h2_thickness = 0
    h1_thickness = df.iloc[-1][depth_column_name]

    # Iterate through the DataFrame
    for index, row in df.iterrows():
        depth = row[depth_column_name]
        FS = row[FS_column_name]
        if FS == '':
            FS = float('NaN')

        if FS < 1 and start_liq_depth is not None:
            if thick_liq == 0:
                if 0 <= index < 2:
                    thick_liq += df.loc[index + 2][depth_column_name] - depth
                else:
                    thick_liq += depth - df.loc[index - 2][depth_column_name]
            else:
                thick_liq += depth - df.loc[index - 1][depth_column_name]

        if FS < 1 and (last_liq_depth is None or depth - last_liq_depth <= 0.3):
            last_liq_depth = depth
            if start_liq_depth is None:
                if index == 0:
                    start_liq_depth = depth
                    h1_index = 0
                else:
                    h1_index = index - 1
                    start_liq_depth = df.loc[index - 1][depth_column_name]
        else:
            if last_liq_depth is not None and thick_liq < 0.3 and depth - last_liq_depth < 0.15:
                last_liq_depth = None
                start_liq_depth = None
                thick_liq = 0
            elif last_liq_depth is not None and thick_liq > 0.3:
                h2_thickness = last_liq_depth - start_liq_depth
                h1_thickness = df.loc[h1_index][depth_column_name]
                break

    h1_column_name = "h1_basic"
    h2_columnn_name = "h2_basic"
    df.at[0, h1_column_name] = h1_thickness
    df.at[0, h2_columnn_name] = h2_thickness

    if h2_thickness >= .3:
        df.at[0, 'clay_profile'] = 0
    else:
        df.at[0, 'clay_profile'] = 1

    # This commented code will apply a cap of 10m to h1 and h2
    # if h1_thickness > 10:
    #     h1_thickness = 10
    # df.at[0, h1_column_name] = h1_thickness
    # if h1_thickness + h2_thickness >= 10:
    #     h2_thickness = 10 - h1_thickness
    # df.at[0, h2_columnn_name] = h2_thickness

    return df


# calculates h2 as the summation of all liquefiable layers for depths less than 10 meters
def h1_h2_cumulative(df, depth_column_name, FS_column_name):
    # Initialize variables
    last_liq_depth = None
    start_liq_depth = None
    h2_thickness = 0
    h1_thickness = 10

    # Iterate through the DataFrame
    for index, row in df.iterrows():
        depth = row[depth_column_name]
        FS = row[FS_column_name]
        if FS == '':
            FS = float('NaN')

        if FS < 1 and (last_liq_depth is None or depth - last_liq_depth <= 0.3):
            last_liq_depth = depth
            if start_liq_depth is None:
                if index == 0:
                    h1_index = 0
                    start_liq_depth = depth
                else:
                    h1_index = index - 1
                    start_liq_depth = df.loc[index - 1][depth_column_name]
        else:
            if last_liq_depth is not None and last_liq_depth - start_liq_depth < 0.3 and depth - last_liq_depth < 0.15:
                last_liq_depth = None
                start_liq_depth = None
            elif last_liq_depth is not None and depth - last_liq_depth > 0.3:
                h1_thickness = df.loc[h1_index][depth_column_name]
                if h1_thickness > 10:
                    h1_thickness = 10
                break

    for index, row in df.iterrows():
        depth = row[depth_column_name]
        FS = row[FS_column_name]
        if FS == '':
            FS = float('NaN')
        if 0 < FS < 1 and depth <= 10:
            if index == 0 and depth > 0.05:
                h2_thickness += df.loc[index + 1][depth_column_name] - depth
            elif index == 0 and depth <= 0.05:
                h2_thickness += depth
            else:
                h2_thickness += depth - df.loc[index - 1][depth_column_name]
        if depth > 10:
            break

    h1_column_name = "h1_cumulative" + FS_column_name.lstrip("FS")
    h2_columnn_name = "h2_cumulative" + FS_column_name.lstrip("FS")
    df.at[0, h1_column_name] = h1_thickness
    df.at[0, h2_columnn_name] = h2_thickness

    return df


def LPI(df, depth_column_name, FS_column_name):
    def Integrate_LPI(z):
        return (1 - row[FS_column_name]) * (10 - 0.5 * z)

    LPI = 0
    for i, row in df.iterrows():
        depth = row[depth_column_name]
        FS = row[FS_column_name]
        if depth <= 20 and FS <= 1:
            if i == 0:
                thick = df.loc[i + 1][depth_column_name] - depth
                start_depth = depth - thick
                LPI += integrate.quad(Integrate_LPI, start_depth, depth)[0]
            else:
                depth_before = df.loc[i - 1][depth_column_name]
                LPI += integrate.quad(Integrate_LPI, depth_before, depth)[0]

    #LPI evaluation from iwasaki 1984 pg 52
    if LPI == 0:
        result = "Liquefaction risk is very low"
        binary = 0
    elif LPI <= 5:
        result = "Liquefaction risk is low"
        binary = 0
    elif LPI <= 15:
        result = "Liquefaction risk is high"
        binary = 1
    elif LPI > 15 :
        result = "Liquefaction risk is very high"
        binary = 1

    df.at[0, "LPI"] = LPI
    df.at[0, f'LPI_results'] = binary

    return df


def LPIish(df, depth_column_name, FS_column_name, h1_column_name):
    """This is LPIISH as discussed in Maurer 2015, 'Moving towards an improved index for assessing liquefaction
    hazard: Lessons from historical data.' The inputs are your df, and column names, and it outputs the lpiish value
    into your df as well as a binary result for liquefaction, or the descriptive results found in the paper. You will have to
    change manually what results you want by altering the code from 'binary' to 'result.'"""
    def Integrate_LPIish(z):
        with warnings.catch_warnings():
            warnings.filterwarnings("ignore", message="overflow encountered in exp")
            c = 0
            # print(row[depth_column_name], 5/(25.56*(1-row[FS_column_name])))
            mFS = np.exp(5 / (25.56 * (1 - row[FS_column_name]))) - 1
            if row[FS_column_name] <= 1 and (h1 * mFS) <= 3:
                c = (1 - row[FS_column_name])
            return (25.56 / z) * c

    LPIish = 0
    for i, row in df.iterrows():
        h1 = df.loc[0][h1_column_name]
        depth = row[depth_column_name]
        if h1 < depth <= 20:
            if depth < 0.4:
                continue
            LPIish += integrate.quad(Integrate_LPIish, df.loc[i - 1][depth_column_name], depth)[0]

    #LPIish found on page 782 of maurer 2015 paper
    if LPIish >= 5:
        result = "Liquefaction manifestation is expected"
        binary = 1
    elif LPIish < 5:
        result = "Liquefaction manifestation is not expected"
        binary = 0

    if h1_column_name[:8] == "h1_basic":
        df.at[0, "LPIish_basic"] = LPIish
        df.at[0, f'LPIish_basic_results'] = binary
    else:
        df.at[0, "LPIish_" + 'cumulative'] = LPIish
        df.at[0, f'LPIish_cumulative_results'] = binary
    return df


def LSN(df, depth_column_name, qc1ncs_column_name, FS_column_name, GWT):
    def A1(qc1ncs):
        return 102 * qc1ncs ** -.82

    def A3(qc1ncs):
        return 2411 * qc1ncs ** -1.45

    def A5(qc1ncs):
        return 1701 * qc1ncs ** -1.42

    def A7(qc1ncs):
        return 1690 * qc1ncs ** -1.46

    def A9(qc1ncs):
        return 1430 * qc1ncs ** -1.48

    def A10(qc1ncs):
        return 64 * qc1ncs ** -.93

    def A11(qc1ncs):
        return 11 * qc1ncs ** -.65

    def A12(qc1ncs):
        return 9.7 * qc1ncs ** -.69

    def A13(qc1ncs):
        return 7.6 * qc1ncs ** -.71

    def A14(qc1ncs):
        return 0

    def interpolator(lower_limit_FS_ev, lower_limit_FS, upper_limit_FS_ev, upper_limit_FS, FS):

        range = lower_limit_FS_ev - upper_limit_FS_ev

        return (upper_limit_FS - FS) * 10 * range + upper_limit_FS_ev

    def Integrate_LSN(z):
        return eps * 10 / z

    below_range_counter = 0
    LSN = 0
    # total_rows_qc1ncs_qualifies = 0

    for i, row in df.iterrows():
        qc1ncs = row[qc1ncs_column_name]
        eps = np.nan
        FS = row[FS_column_name]
        depth = row[depth_column_name]
        if row[depth_column_name] <= 20 and not np.isnan(qc1ncs) and depth >= GWT:
            # total_rows_qc1ncs_qualifies += 1

            eps = A1(qc1ncs)

            if .5 <= FS <= .6 and 147 <= qc1ncs <= 200:
                eps = interpolator(A1(qc1ncs), .5, A3(qc1ncs), .6, FS)

            elif .6 <= FS <= .7 and 110 <= qc1ncs <= 200:
                if qc1ncs < 147:
                    eps = interpolator(eps, .6, A5(qc1ncs), .7, FS)
                else:
                    eps = interpolator(A3(qc1ncs), .6, A5(qc1ncs), .7, FS)

            elif .7 <= FS <= .8 and 80 <= qc1ncs <= 200:
                if qc1ncs < 110:
                    eps = interpolator(eps, .7, A7(qc1ncs), .8, FS)
                else:
                    eps = interpolator(A5(qc1ncs), .7, A7(qc1ncs), .8, FS)

            elif .8 <= FS <= .9 and 60 <= qc1ncs <= 200:
                if qc1ncs < 80:
                    eps = interpolator(eps, .8, A9(qc1ncs), .9, FS)
                else:
                    eps = interpolator(A7(qc1ncs), .8, A9(qc1ncs), .9, FS)

            elif .9 <= FS <= 1 and 0 <= qc1ncs <= 200:  # check out these bounds and the ones below
                if qc1ncs < 60:
                    eps = interpolator(eps, .9, A10(qc1ncs), 1, FS)
                else:
                    eps = interpolator(A9(qc1ncs), .9, A10(qc1ncs), 1, FS)

            elif 1 <= FS <= 1.1 and 0 <= qc1ncs <= 200:
                eps = interpolator(A10(qc1ncs), 1, A11(qc1ncs), 1.1, FS)

            elif 1.1 <= FS <= 1.2 and 0 <= qc1ncs <= 200:
                eps = interpolator(A11(qc1ncs), 1.1, A12(qc1ncs), 1.2, FS)

            elif 1.2 <= FS <= 1.3 and 0 <= qc1ncs <= 200:
                eps = interpolator(A12(qc1ncs), 1.2, A13(qc1ncs), 1.3, FS)

            elif FS >= 1.3 and 0 <= qc1ncs <= 200:
                if FS > 2:
                    FS = 2
                eps = interpolator(A13(qc1ncs), 1.3, A14(qc1ncs), 2, FS)

            if eps > 10: # NOTE: This capped value of 10 and extrapolating values when qc1ncs < 33 is Rollin's idea
                eps = 10

        if i == 0:
            LSN = 0
        elif not np.isnan(eps):
            LSN += integrate.quad(Integrate_LSN, df.loc[i - 1][depth_column_name], depth)[0]

        df.at[i,'eps'] = eps

    # LSN found in Maurer 2015 calibrating LSN paper
    if LSN < 20:
        result = "Little to no manifestation of liquefaction expected"
        binary = 0
    elif LSN < 40:
        result = "Moderate to severe manifestation of liquefaction is expected"
        binary = 1
    elif LSN >= 40:
        result = "Major manifestation of liquefaction expected"
        binary = 1

    df.at[0, "LSN"] = LSN
    df.at[0, f'LSN_results'] = binary

    # print("Number of qc1ncs values below range:" ,below_range_counter,"/",total_rows_qc1ncs_qualifies)

    return df


def Towhata_2016(df, LPI_column_name, h1_column_name):
    lpi_val = df.iloc[0][LPI_column_name]
    h1_val = df.iloc[0][h1_column_name]

    if h1_val > 5:
        qualification = "A"
    elif 3 < h1_val <= 5:
        if lpi_val < 5:
            qualification = "B1"
        else:
            qualification = "B2"
    elif h1_val <= 3:
        if lpi_val < 5:
            qualification = "B3"
        else:
            qualification = "C"

    #Towhata paper page 12 on pdf
    if qualification == "A":
        result = "Unlikely to liquefy"
        binary = 0
    elif qualification == "B1" or qualification == "B2" or qualification == "B3":
        result = "Low probability"
        binary = 1
    elif qualification == "C":
        result = "High probability"
        binary = 1

    if h1_column_name[:8] == "h1_basic":
        df.at[0, f'towhata_basic'] = qualification
        df.at[0, f'towhata_basic_results'] = binary
    else:
        df.at[0, f'towhata_cumulative'] = qualification
        df.at[0, f'towhata_cumulative_results'] = binary

    return df

def LD_and_CR (df, Ic_column_name, depth_column_name, FS_column_name, vert_effective_stress_column_name,total_stress_column_name, GWT_column_name, Qtn_column_name, Fr_column_name, qt_column_name):
    """This function computes the 'CPT-based liquefaction ejecta evaluation procedure' outlined by Bray and Hutabarat
    in their 2022 paper titled as such. The input is your df with specific column names, and it then adds LD,CR,za,zb,and su
    to your df"""
    LD = 0
    CR = 0
    # Initialize variables
    za_check = None
    za_temp = None
    za = None
    zb_check = None
    zb_temp = None
    zb = None
    counter = 0
    GWT = df.loc[0, GWT_column_name]

    for i, row in df.iterrows():
        Ic = row[Ic_column_name]
        depth = row[depth_column_name]

        if za is None:
            if Ic < 2.6 and depth >= GWT and za_check is None:
                za_check = depth
                if za_temp is None:
                    if i == 0:
                        za_temp = depth
                        za_index = 0
                    else:
                        za_index = i - 1
                        za_temp = df.loc[i-1][depth_column_name]
            else:
                if za_check is not None and Ic < 2.6:
                    za_check = depth
                elif za_check is not None and Ic >= 2.6 and za_check - za_temp < 0.25:
                    za_check = None
                    za_temp = None
                elif za_check is not None and za_check - za_temp >= 0.25:
                    za = df.loc[za_index][depth_column_name]

        if za is not None:
            if counter == 0:
                zb_temp = df.loc[i-1][depth_column_name]
                zb_check = df.loc[i-1][depth_column_name]
                counter += 1

            if Ic >= 2.6 and zb_temp is not None:
                zb_check = depth
            elif Ic >= 2.6 and zb_temp is None:
                zb_check = depth
                zb_temp = depth
            elif Ic < 2.6 and zb_check is not None:
                if zb_check - zb_temp < 0.25:
                    zb_check = None
                    zb_temp = None
                elif zb_check - zb_temp >= 0.25:
                    zb = zb_temp
                    break

    if za_temp is not None and counter == 0:
        za = za_temp
        zb = 15
    elif za is None or za > 15:
        za = 15
        zb = 15
    elif zb_temp is not None:
        zb = zb_temp
    elif zb is None or zb > 15:
        zb = 15

    kcs = 10 ** (.952 - 3.04 * 1.8)
    gamma_water = 9.81 # kN/m^3
    for i, row in df.iterrows():
        depth = row[depth_column_name]
        Ic = row[Ic_column_name]
        FS = row[FS_column_name]
        # Cr parameter
        if depth <= za:
            Qtn = row[Qtn_column_name]
            Fr = row[Fr_column_name]
            Nkt = 15
            qt = row[qt_column_name]
            eff_stress = row[vert_effective_stress_column_name]
            total_stress = row[total_stress_column_name]
            K0 = 0.5
            phi_cs = 33

            IB = 100 * (Qtn + 10) / (Qtn * Fr + 70)

            if IB <= 22:
                su = (qt - total_stress) / Nkt
            else:
                su = K0 * eff_stress * np.tan(phi_cs * np.pi / 180)

            if i == 0:
                CR += su * (df.loc[i + 1, depth_column_name] - depth)
            else:
                depth_before = df.loc[i - 1, depth_column_name]
                CR += su * (depth - depth_before)

        # Ld parameter
        if za < depth <= zb:
            ru = 1
            depth_before = df.loc[i-1, depth_column_name]
            h_A = depth

            if Ic < 1:
                # kv = 0.0081658
                print("this site has an Ic value less than 1 at " + str(depth)) # NOTE: Ignored these low and high Ic values that caused large jumps in LD value
                continue
            elif Ic > 4:
                # kv = 1*10**-10
                print("this site has an Ic value greater than 4 at " + str(depth))
                continue

            if 1 < Ic <= 3.27:
                kv = 10 ** (0.952 - 3.04 * Ic)
            elif 3.27 < Ic < 4:  # From Robertson and Cabal 2015 (Gregg CPT guide 6th edition pg 52)
                kv = 10 ** (-4.52 - 1.37 * Ic)

            if FS > 3 or FS == float('NaN') or FS == '' or FS == 9999:
                ru = 0
            elif 1 <= FS < 3:
                ru = 0.5 + np.arcsin(2 * FS ** -5 - 1) / np.pi
            h_exc = ru * row[vert_effective_stress_column_name] / gamma_water

            if h_exc >= h_A:
                LD += (kv / kcs * (h_exc - h_A) * gamma_water) * (depth - depth_before)
        elif depth > zb:
            break

    df.at[0,'LD'] = LD
    df.at[0, 'CR'] = CR
    df.at[0, 'za'] = za
    df.at[0, 'zb'] = zb

    #LD and CR results
    result = 'Something went wrong'
    if CR < 100 and LD < 2.5 or (100 < CR and LD < 0.15 * (CR-100) + 2.5) or LD == 0:
        result = 'No Liquefaction'
    elif CR < 90 and LD < 6 or (90 < CR and LD < 2/5 * (CR - 90) + 6):
        result = 'Minor'
    elif CR < 85 and LD < 15 or (85 < CR and LD < 9/11 * (CR - 85) + 15):
        result = 'Moderate'
    elif CR < 75 and LD < 85 or (75 < CR and LD < 33/25 * (CR - 75) + 85):
        result = 'Severe'
    elif CR < 75 and LD > 85 or (75 < CR and LD > 33/25 * (CR - 75) + 85):
        result = 'Extreme'
    df.at[0, 'LD_and_CR_results'] = result

    if result == 'No Liquefaction':
        df.at[0, 'LD_and_CR_binary_results'] = 0
    else:
        df.at[0,'LD_and_CR_binary_results'] = 1

    return df

def ishihara_curves(df, method):
    """While these are not the original ishihara curves, they come from the updated Maurer's power law equations from
    his 2022 paper titled 'Evaluation and updating of Ishihara’s (1985) model for liquefaction surface expression, with insights from
    machine and deep learning.' The method you input is either basic or cumulative as outlined in his paper. This will just label your
    output in the df as such method."""
    PGA = df.loc[0]['PGA']
    h1 = df.loc[0][f"h1_{method}"]
    h2 = df.loc[0][f"h2_{method}"]

    h2_ish = 0.0217 * PGA**-1.9481 * h1**1.5688

    if h2 >= h2_ish:
        df.at[0,f'ishihara_curve_{method}_results'] = 1
    else:
        df.at[0, f'ishihara_curve_{method}_results'] = 0

    return df


def preforo_check(df, GWT_column_name, preforo_column_name):
    GWT_val = df.loc[0][GWT_column_name]
    preforo_val = df.loc[0][preforo_column_name]
    if GWT_val >= preforo_val:
        preforo_check = "GWT is deeper than preforo"
    elif pd.isna(preforo_val):
        preforo_check = "Nan preforo"
    else:
        preforo_check = "GWT is above preforo"
    return preforo_check