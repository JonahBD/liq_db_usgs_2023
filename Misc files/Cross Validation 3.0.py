import numpy as np
import pandas as pd
from sklearn.model_selection import KFold
from sklearn.metrics import accuracy_score

# Sample data
log_reg_file_path = r"C:\Users\hf233\OneDrive - Brigham Young University\Liq\Italy Data\Model Building 02\Clay Sites\log_reg_parameters_model_clay_MORE.xlsx"
df = pd.read_excel(log_reg_file_path)
threshold = 0.99999

# df["h1_φ' R_median_withZeros"] = df["h1_φ' R_median"].fillna(0)
# df["h1_φ' R_median_withZeros"] = df["h1_φ' R (degrees)_median"].fillna(0)
# df['phi here?'] = [-3.24237250424891 if x == 0 else 3.24237250424891 for x in df["h1_φ' R_median_withZeros"]]
# df["LPI^2"]=df['LPI']**2
# df["H2_cumulative^2"]=df['h2_cumulative']**2
# df['PGA^2']=df['PGA']**2
# df['LPIxH2']=df['LPI']*df['h2_cumulative']
# df['H2xPGA']=df['PGA']*df['h2_cumulative']
# df['LPIxPGA']=df['PGA']*df['LPI']

# Define the model's equation
def logistic_model(X, coeffs):
    linear_combination = coeffs[0] + np.dot(X, coeffs[1:])  #With intercept# Intercept + dot product of coefficients and features
    # linear_combination = np.dot(X, coeffs[0:]) #No intercept
    return np.exp(linear_combination) / (1 + np.exp(linear_combination))

# Coefficients from your model (intercept + coefficient for each X feature)
#model 1 [-8.92037390038764,0.34050373061748,0.0869353182127432, 11.7649657769085], ["h2_cumulative","LPI", "PGA"]
# model 2 [10.8878413792517,1.17893307442733, -0.143842105352312,0.153653090183619,-0.00271557922869898,-105.944130984329,158.437015868847 ], ["h2_cumulative", "H2_cumulative^2", "LPI","LPI^2", "PGA","PGA^2"]
#model 3 w/ interactive [5.09301725735328, 3.36904141858887,-0.366702634445042,-1.14833459523899, -0.0216155931134555,-62.5212258748271,89.6719563891651,0.127891226647041,-5.4004920282488, 3.11453438343859], ["h2_cumulative","H2_cumulative^2","LPI","LPI^2", "PGA","PGA^2",'LPIxH2', 'H2xPGA', 'LPIxPGA']
#Chosen method
coefficients = [-0.201372018212869 , -0.246477030598477 , -0.0201860652847881 , 0.162212187962329 , 0.0299100694258082]  # Example coefficients

# Prepare features and target
X = df[["h1_basic","h1_Vs M (m/s)_mean","LPI","Max effective stress"]].values
y = df['Liquefaction'].values

# Cross-validation setup
kf = KFold(n_splits=10, shuffle=True)  # 10-fold cross-validation
accuracy_list = []

for train_index, test_index in kf.split(X):
    X_train, X_test = X[train_index], X[test_index]
    y_train, y_test = y[train_index], y[test_index]

    # Predict probabilities using the logistic model
    y_pred_prob = logistic_model(X_test, coefficients)

    # Convert probabilities to binary predictions (0 or 1) based on a threshold
    y_pred = (y_pred_prob >= threshold).astype(int)

    # Calculate accuracy
    accuracy = accuracy_score(y_test, y_pred)
    print(accuracy)
    accuracy_list.append(accuracy)

# Average accuracy across folds
average_accuracy = np.mean(accuracy_list)
stdev = np.std(accuracy_list)
print(f'Average Accuracy: {average_accuracy:.2f}\n'
      f"stdev: {stdev}")
