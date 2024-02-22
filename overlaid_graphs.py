import matplotlib.pyplot
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import math
import os, glob

our_data_folder = r"C:\Users\jdundas2\OneDrive - Brigham Young University\Liq\Cliq settings changed\soil parameters"
cliq_data_folder = r"C:\Users\jdundas2\OneDrive - Brigham Young University\Liq\Cliq settings changed"
export_folder_path = r"C:\Users\jdundas2\OneDrive - Brigham Young University\Liq\Cliq settings changed\graphs"

for file in glob.glob(os.path.join(our_data_folder, "*.xls*")):
    our_data = pd.read_excel(file)
    filename = os.path.basename(file).rstrip('.xls')
    try:
        cliq_data = pd.read_excel(f'{cliq_data_folder}\{filename}.xls')
    except OSError:
        cliq_data = pd.read_excel(f'{cliq_data_folder}\{filename}.xlsx')
    file_folder_path = f"{export_folder_path}\{filename}"
    os.mkdir(file_folder_path)

    X = np.array(our_data[our_data.columns[0]])

    c_qc = np.array(cliq_data[cliq_data.columns[1]])
    c_fs = np.array(cliq_data[cliq_data.columns[2]])
    c_total_stress = np.array(cliq_data[cliq_data.columns[5]])
    c_effective_stress = np.array(cliq_data[cliq_data.columns[6]])
    c_CSR = np.array(cliq_data[cliq_data.columns[12]])
    c_k_sigma = np.array(cliq_data[cliq_data.columns[11]])
    c_Ic = np.array(cliq_data[cliq_data.columns[18]])
    c_m = np.array(cliq_data[cliq_data.columns[19]])
    c_qc1N = np.array(cliq_data[cliq_data.columns[21]])
    c_qc1Ncs = np.array(cliq_data[cliq_data.columns[23]])
    c_CRR = np.array(cliq_data[cliq_data.columns[26]])
    c_FS = np.array(cliq_data[cliq_data.columns[27]])
    c_LPI = np.array(cliq_data[cliq_data.columns[29]])
    c_rd = np.array(cliq_data[cliq_data.columns[7]])
    c_strain = np.array(cliq_data[cliq_data.columns[31]])

    # c_qc = np.array(cliq_data[cliq_data.columns[1]])
    # c_fs = np.array(cliq_data[cliq_data.columns[2]])
    # c_total_stress = np.array(cliq_data[cliq_data.columns[5]])
    # c_effective_stress = np.array(cliq_data[cliq_data.columns[6]])
    # c_CSR = np.array(cliq_data[cliq_data.columns[12]])
    # c_k_sigma = np.array(cliq_data[cliq_data.columns[11]])
    # c_Ic = np.array(cliq_data[cliq_data.columns[18]])
    # c_m = np.array(cliq_data[cliq_data.columns[19]])
    # c_qc1N = np.array(cliq_data[cliq_data.columns[20]])
    # c_qc1Ncs = np.array(cliq_data[cliq_data.columns[22]])
    # c_CRR = np.array(cliq_data[cliq_data.columns[25]])
    # c_FS = np.array(cliq_data[cliq_data.columns[26]])
    # c_LPI = np.array(cliq_data[cliq_data.columns[28]])
    # c_rd = np.array(cliq_data[cliq_data.columns[7]])

    qc = np.array(our_data[our_data.columns[1]])
    fs = np.array(our_data[our_data.columns[2]])
    total_stress = np.array(our_data[our_data.columns[7]])
    effective_stress = np.array(our_data[our_data.columns[8]])
    CSR = np.array(our_data[our_data.columns[39]])
    CSR[CSR > 2] = 2
    k_sigma = np.array(our_data[our_data.columns[36]])
    Ic = np.array(our_data[our_data.columns[10]])
    m = np.array(our_data[our_data.columns[15]])
    qc1N = np.array(our_data[our_data.columns[31]])
    qc1Ncs = np.array(our_data[our_data.columns[33]]) # Note: 3
    CRR = np.array(our_data[our_data.columns[40]])
    CRR[CRR > 4] = 4
    FS = np.array(our_data[our_data.columns[43]])
    FS[FS > 2] = 2
    LPI = np.array(our_data[our_data.columns[53]])
    rd = np.array(our_data[our_data.columns[37]])
    strain = np.array(our_data[our_data.columns[34]])

    our_columns = [qc, fs, total_stress, effective_stress, CSR, k_sigma, Ic, m, qc1N, qc1Ncs, CRR, FS, LPI, rd, strain]
    column_names = ['qc', 'fs', 'total_stress', 'effective_stress', 'CSR', 'k_sigma', 'Ic', 'm', 'qc1N', 'qc1Ncs', 'CRR', 'FS', 'LPI', 'rd_20may', 'eps_20may']
    cliq_columns = [c_qc, c_fs, c_total_stress, c_effective_stress, c_CSR, c_k_sigma, c_Ic, c_m, c_qc1N, c_qc1Ncs, c_CRR, c_FS, c_LPI, c_rd, c_strain]
    counter = 0

    for our_column, cliq_column in zip(our_columns, cliq_columns):
        plt.plot(X, cliq_column, color="green", label="cliq_data")
        plt.plot(X, our_column, color="blue", label="our_data")
        plt.xlabel("Depth")
        plt.ylabel(column_names[counter])
        plt.legend()
        plt.savefig(f"{file_folder_path}\{column_names[counter]}_{filename}", dpi=400)
        plt.close()
        counter += 1