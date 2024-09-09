import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages
import glob, os
from tqdm import tqdm

# Problems: Not all variables have units in the name. We need to fix that. Also, some of the variables have very large
# values that make the scale of the graph go crazy. Maybe we should try and limit this on a variable by variable basis?
#

############### USER INPUTS ############################
soil_parameters_input_path = r"C:\Users\jdundas2\OneDrive - Brigham Young University\Liq\Italy Data\Attempt 06 - GWT, OG\OG Data\Soil Parameters"
PDF_folder_path = r"C:\Users\jdundas2\OneDrive - Brigham Young University\Liq\Italy Data\PDF Plots\Attempt 02"
depth_column_name = "Depth (m)"
columns_to_exclude = ['u calc (kPa)']
x_axis_limits = {
    'qt (MPa)': (0, 50),
    'Rf (%)': (0, 20),
    'Gamma (kN/m^3)': (0, 25),
    'Fr (%)': (0,30),
    'OCR R': (0, 20),
    'OCR K': (0, 20),
    'cu_bq (kPa)': (0, 500),
    'cu_14 (kPa)': (0, 500),
    'su_HB (kPa)': (0, 500),
    'M (kPa)': (0, 100000),
    'k0_1': (0, 10),
    'k0_2': (0, 10),
    'Vs R (m/s)': (0, 750),
    'Vs M (m/s)': (0, 750),
    'k (m/s)': (0, .2),
    # 'ψ': (0, 20), maybe change this later?
    "φ' R (degrees)": (0, 50),
    "φ' K (degrees)": (0, 50),
    "φ' J (degrees)": (0, 50),
    "φ' M (degrees)": (0, 50),
    "φ' U (degrees)": (0, 50),
    'Dr B': (0, 1),
    'Dr K': (0, 1),
    'Dr J': (0, 1),
    'Dr I': (0, 1),
    'qc1n': (0, 500),
    'qc1ncs': (0, 500),
    'Volumetric Strain (%)': (0, 10),
    'Kσ': (0, 1.1),
    'Fines Content (%)': (0, 100),
    'Shear Stress Reduction Coefficient': (0, 1),
    'CSR': (0, 1000000),
    'CRR': (0, 10),
    'Factor of Safety': (0, 5),
}
#########################################################

sites = []

for filename in glob.glob(os.path.join(soil_parameters_input_path, "*.xls*")):
    site = os.path.basename(filename).rstrip(".xls").lstrip("Copy of")
    sites.append(site)

loop = tqdm(total=(len(sites)))

for filename in glob.glob(os.path.join(soil_parameters_input_path, "*.xls*")):
    site = os.path.basename(filename).rstrip(".xls").lstrip("Copy of")
    if site == "sites_to_check":
        continue
    # print(site)
    loop.set_description(f"soil parameters - {site} :")

    df = pd.read_excel(filename)
    df = df.apply(pd.to_numeric, errors="coerce")

    pdf_pages = PdfPages(fr"{PDF_folder_path}\{site}.pdf")

    # Iterate through each column in the DataFrame except the reference column
    for column in df.columns[4:42]:
        if column in columns_to_exclude:
            continue

        plt.figure(figsize=(8, 12))  # Create a new figure
        if column in x_axis_limits:
            max = x_axis_limits[column][1]
            if df[column].max() > max:
                df[column] = [max if x > max else x for x in df[column]]

        plt.plot(df[column], df[depth_column_name], color='b', label=column)  # Plot against reference column
        plt.title(f'{column}')  # Set the title of the plot
        plt.xlabel(column)  # Set x-axis label
        plt.ylabel(depth_column_name)  # Set y-axis label
        plt.gca().invert_yaxis()


        # Set x-axis limits if specified
        if column in x_axis_limits:
            if df[column].max() > x_axis_limits[column][1]:
                plt.xlim(x_axis_limits[column])


        # plt.legend()  # Add legend - redundant since there is only one variable per graph
        plt.grid(True)  # Add grid
        pdf_pages.savefig()  # Save the current figure into the PDF
        plt.close()  # Close the figure to free up memory

    # Close the PdfPages object
    pdf_pages.close()

    loop.update(1)
loop.close()