import pandas as pd
import numpy as np

compiled = pd.read_excel(r"C:\Users\jdundas2\OneDrive - Brigham Young University\Liq\Final Data\OG Data\liq_param_compiled_10_150_7-3.xlsx")
pca = pd.read_excel(r"C:\Users\jdundas2\OneDrive - Brigham Young University\Liq\Final Data\OG Data\PCA_parameters_all_sites 7-1.xlsx")

# linear_predictor = .87908464750829 + -0.0992873354236673 * pca["h1_φ' R_median"] + 0.3125294225309 * pca["LPI"] + 0.614696806583199 * pca["PGA"]
# linear_predictor = 1.93313846917024 + -0.0915855869567442 * pca["h1_φ' R_median"] + 0.298505612181314 * pca["LPI"]
# linear_predictor = 3.54417348207553 + -0.0795580764791788 * pca["h1_basic"] + -0.135462619271519 * pca["h1_φ' R_median"] + 0.339624888791761 * pca["LPI"]
# linear_predictor = 13.2015446951802 + -182767222.114379 * pca["h1_k (m/s)_equivalent"] + -0.261737488636114 * pca["h1_φ' R_median"] + -0.0271838689858064 * pca["h2_Vs M_median"] + 0.563415237518111 * pca["LPI"] + -0.0231261007197522 * pca["sand_percent"]
# linear_predictor = -0.455528762607509 + 0.126017766375067 * pca["LPI"]
# linear_predictor = 1.82448449517987 + -0.0435870427572786 * pca["h1_Dr B_mean"] + -0.181124870409241 * pca["h2_φ' J_mean"] + 0.222614713643377 * pca["LPI"] + 6.6859630462023 * pca["PGA"]
# linear_predictor = -1.46369592715239 + -2.29846962135262 * pca["h1_Dr B_mean"] + 0.367293376022061 * pca["LPI"]
linear_predictor = -2.49436325637352 + -0.0101857211558844 * pca["h1_Vs M_median"] + 0.204971498168668 * pca["LPI"]

pca["our_method"] = np.exp(linear_predictor) / (1 + np.exp(linear_predictor))
our_method_df = pca[['site','our_method']]

df = compiled.merge(our_method_df, on='site', how='left')
df['our_method_binary_results'] = [1 if x > 0.5 else 0 for x in df['our_method']]
# print(compiled['our_method'])
df.to_excel(r"C:\Users\jdundas2\OneDrive - Brigham Young University\Liq\Final Data\OG Data\liq_param_compiled_vs_method.xlsx", index=False)