from functions import *
import pandas as pd
import glob, os

counter = 0
df_name = []
error = False

folder_path = r"C:\Users\hf233\Documents\Italy\5. CPTU standard"
for filename in glob.glob(os.path.join(folder_path, "*.xls*")):
    df = pd.read_excel(filename)
    site = os.path.basename(filename).rstrip(".xls")
    missing_pga = []
    only_clay_profile_list = []
    preforo_below_GWT = []
    print(site)

    df = soil_parameters(df)


    try:
        df = PGA_insertion(df,r"C:\Users\hf233\Documents\Italy\5. CPTU standard\GWT from CLIQ input\pga.xlsx", site)
    except KeyError:
        print("This site is missing its PGA: " + site)
        missing_pga.append(site)
        continue

    preforo_checker = preforo_check(df, "GWT [m]", "preforo [m]")
    if preforo_checker == "GWT is above preforo":
        preforo_below_GWT.append(site)


    df = FS_liq(df, 6.1, 5.9)

    df = h1_h2_basic(df, 'Depth (m)','FS_20may')
    df = h1_h2_basic(df, 'Depth (m)', 'FS_29may')
    df = h1_h2_cumulative(df, 'Depth (m)', 'FS_20may')
    df = h1_h2_cumulative(df, 'Depth (m)', 'FS_29may')

    # print(df)

    df = LPI(df,"Depth (m)","FS_20may","20may")
    df = LPI(df,"Depth (m)","FS_29may","29may")

    df = LPIish(df, "Depth (m)", "FS_20may","20may", "h1_basic_20may")
    df = LPIish(df, "Depth (m)", "FS_20may", "20may", "h1_cumulative_20may")
    df = LPIish(df, "Depth (m)", "FS_29may", "29may", "h1_basic_29may")
    df = LPIish(df, "Depth (m)", "FS_29may", "29may", "h1_cumulative_29may")


    df = LSN(df, "Depth (m)", "qc1ncs", "FS_20may", "20may")


    # df = df.drop()
    # Reorder the columns
    # df = df[['Depth (m)', 'qc (MPa)', 'fs (kPa)', 'u (kPa)', 'qt (MPa)', "Rf (%)",
    #          "Gamma (kN/m^3)", "Total Stress (kPa)", "Effective Stress (kPa)", "Fr (%)", "Ic",
    #          'OCR R', 'OCR K', 'cu_bq', 'cu_14', "M", "k0_1", 'k0_2', "Vs R", 'Vs M', "k (m/s)", 'ψ', "φ' R",
    #          "φ' K", "φ' J", "φ' M", "φ' U", 'Dr B', 'Dr K', 'Dr J', 'Dr I', 'qc1n','Kσ', 'rd_20may', 'rd_29may', "CSR_20may",
    #          "CRR_20may", 'CSR_29may', 'CRR_29may', "FS_20may", "FS_29may", "LPI_20may","LPI_29may","LPIish_20may","LPIish_29may",
    #          "Unnamed: 5", 'GWT [m]', 'Date of CPT [gg/mm/aa]', 'u [si/no]', 'preforo [m]', 'PGA_20may', 'PGA_29may','Liquefaction']]

    filename = filename.replace('5. CPTU standard', 'test files') #TODO why does this not make a new folder like I want. I need to put the folder in, then it can work
    if filename[-1] == 's':
        filename = filename.replace('xls', 'xlsx')

    df.to_excel(filename, index=False)
