import numpy as np
import pandas as pd
from sklearn.metrics import roc_curve, auc
import matplotlib.pyplot as plt

df = pd.read_excel(r"C:\Users\jdundas2\OneDrive - Brigham Young University\Liq\Italy Data\Attempt 07 - OG\OG Data\liq_param_compiled_vs_method.xlsx"
                   ) #Takes in liq_param_compiled file
methods = [
    {
        'column': 'LPI',
        'label': 'LPI',
        "color": 'b'
    },{
        'column': 'LPIish_basic',
        'label': 'LPIish',
        "color": 'g'
    },
    {
        'column': 'LSN',
        'label':'LSN',
        "color": 'r'
    },
    {
        'column': 'LD_and_CR_binary_results',
        'label': 'Hutabarat and Bray',
        "color": '#20b2aa'
    },{
        'column': 'ishihara_curve_basic_results',
        'label': "Ishihara Basic",
        "color":'#ff55fc'
    },{
        'column': 'ishihara_curve_cumulative_results',
        'label': "Ishihara Cumulative",
        "color":'#808080'
    },{
        'column': 'towhata_basic_results',
        'label': "Towhata",
        "color":'k'
    }
    ,{
        'column': 'our_method',
        'label': "LϕI",
        "color":'#ffaa00'
    }
        ]
         # 'LPIish_basic', 'LSN', 'LD_and_CR_binary_results', 'ishihara_curve_basic_results', 'ishihara_curve_cumulative_results', 'towhata_basic_results']
# method_results = f'{method}_results'

y_true = df["Liquefaction"].to_numpy()
for m in methods:
    y_scores = df[m['column']].to_numpy()

    fpr, tpr, thresholds = roc_curve(y_true, y_scores)

    roc_auc = auc(fpr, tpr)

    # plt.figure()
    plt.plot(fpr, tpr, lw=2,color= m["color"], label=f'{m["label"]} AUC = %0.2f' % roc_auc) #, color='darkorange'
plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--', label= "Random Guess AUC = 0.5")
plt.xlim([0.0, 1.0])
plt.ylim([0.0, 1.05])
plt.xlabel('False Positive Rate')
plt.ylabel('True Positive Rate')
plt.title('Receiver Operating Characteristic')
plt.legend(loc="lower right")
plt.show()