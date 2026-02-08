import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns

input_file_path = r"C:\Users\jdundas2\OneDrive - Brigham Young University\Liq\Final Data\OG Data\liq_methods_performance_without_clay 6-14.xlsx"
export_file_path = r"C:\Users\jdundas2\OneDrive - Brigham Young University\Liq\Final Data\Plots"
df = pd.read_excel(input_file_path)

df_liq = df[df['Liquefaction'] == 1]
df_no_liq = df[df['Liquefaction'] == 0]

histograms = ['LPI', 'LSN', 'LPIish_basic', 'h1_basic','h2_cumulative','CR','LD']

for histogram in histograms:
    fig, ax = plt.subplots()

    sns.kdeplot(df_no_liq[histogram], ax=ax, color='green', fill=True, label='No Manifestation')

    # ax2 = ax.twinx()
    sns.kdeplot(df_liq[histogram], ax=ax, color='red', fill=True, label='Manifestation')

    ax.legend(loc='upper right')
    # ax2.legend(loc='upper right')
    plt.tight_layout()
    # plt.show()
    fig.savefig(export_file_path + "\\" + histogram, bbox_inches='tight', dpi=300)
    plt.close(fig)


