import numpy as np
import pandas as pd
from sklearn.model_selection import KFold
from sklearn.metrics import accuracy_score, balanced_accuracy_score

# Sample data
log_reg_file_path = r"C:\Users\jdundas2\OneDrive - Brigham Young University\Liq\Italy Data\Attempt 07 - OG\OG Data\log_reg_parameters_OG_A07.xlsx"

df = pd.read_excel(log_reg_file_path)
# df["h1_φ' R_median_withZeros"] = df["h1_φ' R_median"].fillna(0)
df["h1_φ' R_median_withZeros"] = df["h1_φ' R (degrees)_median"].fillna(0)
df['phi here?'] = [-3.24237250424891 if x == 0 else 3.24237250424891 for x in df["h1_φ' R_median_withZeros"]]


# Define the model's equation
def logistic_model(X, coeffs):
    linear_combination = coeffs[0] + coeffs[1] * X[:, 0] + coeffs[2] * X[:, 1] + coeffs[3] * X[:, 2] + coeffs[4] * X[:, 3]
    return np.exp(linear_combination) / (1 + np.exp(linear_combination))


# Coefficients from your model (intercept, coefficient for X1, coefficient for X2)
coefficients = [-1.97942967277575, -0.0804218995253738, 0.359579825073672, 0.193532837109407, 1]  # Example: y = 1 + 1*X1 + 1*X2

# Prepare features and target
X = df[["h1_φ' R_median_withZeros", "h2_cumulative", "LPI", "phi here?"]].values
y = df['Liquefaction'].values

# Cross-validation setup
kf = KFold(n_splits=10, shuffle=True)  # 5-fold cross-validation
accuracy_list = []

for train_index, test_index in kf.split(X):
    X_train, X_test = X[train_index], X[test_index]
    y_train, y_test = y[train_index], y[test_index]

    # Predict probabilities using the logistic model
    y_pred_prob = logistic_model(X_test, coefficients)

    # Convert probabilities to binary predictions (0 or 1) based on a threshold
    y_pred = (y_pred_prob >= 0.5).astype(int)

    # Calculate accuracy
    accuracy = accuracy_score(y_test, y_pred)
    print(accuracy)
    accuracy_list.append(accuracy)

# Average accuracy across folds
average_accuracy = np.mean(accuracy_list)
print(f'Average Accuracy: {average_accuracy:.2f}')