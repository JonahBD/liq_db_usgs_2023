import pandas as pd
import numpy as np

compiled = pd.read_excel(r"C:\Users\jdundas2\OneDrive - Brigham Young University\Liq\Italy Data\Attempt 08 - OG\OG Data\liq_param_compiled_OG_A08.xlsx")
pca = pd.read_excel(r"C:\Users\jdundas2\OneDrive - Brigham Young University\Liq\Italy Data\Model Building 02\All Sites\log_reg_parameters_model_all_MORE.xlsx")
# pca["h1_φ' R_median_With_Zeros"] = pca["h1_φ' R (degrees)_median"].fillna(0)
# pca['phi here?'] = [-2.68658450501996 if x == 0 else 2.68658450501996 for x in pca["h1_φ' R_median_With_Zeros"]]
run_optimizer = True
run_target_TP_number = False
target_TP_number = 115
method_name = "LEPM"
iterations = 1000

liq_sites = 132
# non_liq_sites = 1609
non_liq_sites = 1983

best_threshold_value = 0
best_true_rate = 0

# linear_predictor = .87908464750829 + -0.0992873354236673 * pca["h1_φ' R (degrees)_median"] + 0.3125294225309 * pca["LPI"] + 0.614696806583199 * pca["PGA"]
# linear_predictor = 1.93313846917024 + -0.0915855869567442 * pca["h1_φ' R (degrees)_median"] + 0.298505612181314 * pca["LPI"]
# linear_predictor = 3.54417348207553 + -0.0795580764791788 * pca["h1_basic"] + -0.135462619271519 * pca["h1_φ' R (degrees)_median"] + 0.339624888791761 * pca["LPI"]
# linear_predictor = 13.2015446951802 + -182767222.114379 * pca["h1_k (m/s)_equivalent"] + -0.261737488636114 * pca["h1_φ' R (degrees)_median"] + -0.0271838689858064 * pca["h2_Vs M (m/s)_median"] + 0.563415237518111 * pca["LPI"] + -0.0231261007197522 * pca["sand_percent"]
# linear_predictor = -0.455528762607509 + 0.126017766375067 * pca["LPI"]
# linear_predictor = 1.82448449517987 + -0.0435870427572786 * pca["h1_Dr B_mean"] + -0.181124870409241 * pca["h2_φ' J (degrees)_mean"] + 0.222614713643377 * pca["LPI"] + 6.6859630462023 * pca["PGA"]
# linear_predictor = -1.46369592715239 + -2.29846962135262 * pca["h1_Dr B_mean"] + 0.367293376022061 * pca["LPI"]
# linear_predictor = -2.49436325637352 + -0.0101857211558844 * pca["h1_Vs M (m/s)_median"] + 0.204971498168668 * pca["LPI"]
# linear_predictor = -3.29627859662139 + -0.0176312292020156 * pca["h1_φ' R_median"] + 0.15680779457338 * pca["h2_cumulative"] + 0.181815722365216 * pca["LPI"]
# linear_predictor_02 = -3.96017469580081 + 0.109788766975956 * pca["h2_cumulative"] + 0.183865120025159 * pca["LPI"]
#
# linear_predictor -0.720479384425238 + -0.0840638498355794 * pca["h1_φ' R_median"] + 0.207988422546471 * pca["LPI"] #total data
# linear_predictor = 0.826993863130674 + -0.068082042953569 * pca["h1_φ' R_median"] + 0.264562821341293 * pca["LPI"] #balanced

# linear_predictor = -1.97942967277575 + -0.0804218995253738 * pca["h1_φ' R_median_withZeros"] + 0.359579825073672 * pca["h2_cumulative"] + 0.193532837109407 * pca["LPI"] + pca["phi here?"]
# linear_predictor = -3.4012429703011 + -0.0849101353467824 * pca["h1_φ' R_median_With_Zeros"] + 0.230174481116412 * pca["h2_cumulative"] + 0.153672176172119 * pca["LPI"] + pca["phi here?"]

pca['H2_cumulative^2'] = pca['h2_cumulative']**2
pca['PGA^2'] = pca['PGA']**2
pca['LPI^2'] = pca['LPI']**2

# method 1: optimal threshold = 0.076, LPI threshold = 0.051
# linear_predictor = -8.92037390038763 + 0.340503730617479 * pca["h2_cumulative"] + 0.0869353182127434 * pca["LPI"] + 11.7649657769085 * pca["PGA"]

# method 2: optimal threshold = 0.105
# linear_predictor = 10.8878413792518 + 1.17893307442733 * pca["h2_cumulative"] + -0.143842105352312 * pca["H2_cumulative^2"] + 0.153653090183619 * pca["LPI"] + -0.00271557922869899 * pca["LPI^2"] + -105.94413098433 * pca["PGA"] + 158.437015868848 * pca["PGA^2"]

#method 3: optimal threshold = 0.054
# linear_predictor = 5.09301725735299 + 3.3690414185889 * pca["h2_cumulative"] + -0.366702634445039 * pca["H2_cumulative^2"] + -1.14833459523902 * pca["LPI"] + -0.0216155931134554 * pca["LPI^2"] + -62.5212258748251 * pca["PGA"] + 89.6719563891621 * pca["PGA^2"] + 0.12789122664704 * pca["h2_cumulative"] * pca["LPI"] + -5.40049202824887 * pca["h2_cumulative"] * pca["PGA"] + 3.11453438343866 * pca["LPI"] * pca["PGA"]

#CHOSEN METHOD (method 2, LPI^2 removed): optimal threshold = 0.097, LPI threshold = 0.039
# linear_predictor = 10.6792558895584 + 1.40495611982079 * pca["h2_cumulative"] + -0.176140402756966 * pca["H2_cumulative^2"] + 0.0770038726102139 * pca["LPI"] + -105.035269005498 * pca["PGA"] + 158.093503861048 * pca["PGA^2"]

#LPI
# linear_predictor =  -4.14426634838716 + 0.198557354736245 * pca["LPI"]

#LEPM
linear_predictor = -0.389496479708949 * pca["h1_basic"] + -0.0224933862867034 * pca["h1_Vs M (m/s)_mean"] + 0.163801232292651 * pca["LPI"] + 0.0416527762192667 * pca["Max effective stress"]


pca[f"{method_name}"] = np.exp(linear_predictor) / (1 + np.exp(linear_predictor))

our_method_df = pca[['site',f'{method_name}']]

df = compiled.merge(our_method_df, on='site', how='left')
our_method = f'{method_name}'

while run_optimizer:
    for value in range(1,iterations+1):
        df['our_method_binary_results'] = [
            np.nan if np.isnan(x) else (1 if x > (value / iterations) else 0)
            for x in df[f'{method_name}']
        ]

        df[f'{our_method}_true_negative'] = 0
        df[f'{our_method}_false_negative'] = 0
        df[f'{our_method}_true_positive'] = 0
        df[f'{our_method}_false_positive'] = 0

        for index, row in df.iterrows():
            our_val = row['our_method_binary_results']
            liq_val = row["Liquefaction"]  # _italy

            if liq_val == 0 and our_val == 0:
                df.at[index, f'{our_method}_true_negative'] = 1
            elif liq_val == 1 and our_val == 0:
                df.at[index, f'{our_method}_false_negative'] = 1
            elif liq_val == 1 and our_val == 1:
                df.at[index, f'{our_method}_true_positive'] = 1
            elif liq_val == 0 and our_val == 1:
                df.at[index, f'{our_method}_false_positive'] = 1

        tp_rate = df[f"{our_method}_true_positive"].sum() / liq_sites
        tn_rate = df[f"{our_method}_true_negative"].sum()/non_liq_sites

        combined_true_rate = (tp_rate + tn_rate) / 2
        # print(combined_true_rate, best_true_rate)

        if combined_true_rate > best_true_rate:
            # print(combined_true_rate, value/iterations)
            best_true_rate = combined_true_rate
            best_threshold_value = value / iterations

    print(f"best true combined rate: {best_true_rate}\n"
          f"best threshold value: {best_threshold_value}\n")

    run_optimizer = False

while run_target_TP_number:
    for value in range(1,iterations+1):

        df[f'{method_name}_binary_results'] = [
            np.nan if np.isnan(x) else (1 if x > (value / iterations) else 0)
            for x in df[f'{method_name}']
        ]
        df[f'{our_method}_true_negative'] = 0
        df[f'{our_method}_false_negative'] = 0
        df[f'{our_method}_true_positive'] = 0
        df[f'{our_method}_false_positive'] = 0

        for index, row in df.iterrows():
            our_val = row[f'{method_name}_binary_results']
            liq_val = row["Liquefaction"]  # _italy

            if liq_val == 0 and our_val == 0:
                df.at[index, f'{our_method}_true_negative'] = 1
            elif liq_val == 1 and our_val == 0:
                df.at[index, f'{our_method}_false_negative'] = 1
            elif liq_val == 1 and our_val == 1:
                df.at[index, f'{our_method}_true_positive'] = 1
            elif liq_val == 0 and our_val == 1:
                df.at[index, f'{our_method}_false_positive'] = 1

        tp_num = df[f"{our_method}_true_positive"].sum()
        print(f"TP rate: {tp_num}, threshold value: {value/iterations}")
        if tp_num <= target_TP_number:
            run_target_TP_number = False
            break

user_input = float(input("Enter threshold value hoe: "))
print(f"You entered: {user_input}")

df[f'{method_name}_binary_results'] = [1 if x > user_input else 0 for x in df[f'{method_name}']]

# print(compiled['our_method'])
df.to_excel(r"C:\Users\jdundas2\OneDrive - Brigham Young University\Liq\Italy Data\Attempt 08 - OG\OG Data\liq_param_compiled_LEPM_optimal_threshold.xlsx", index=False)