from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, roc_auc_score
from sklearn.model_selection import cross_val_score
import pandas as pd

pca = pd.read_excel(r"C:\Users\jdundas2\OneDrive - Brigham Young University\Liq\Final Data\OG Data\PCA_parameters_randomized_balanced_no_nans 7-1.xlsx")

# Assuming 'pca' is your dataframe
X = pca[["h1_φ' R_median", 'LPI']]  # Predictor variables
y = pca['Liquefaction']  # Target variable

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=.2, random_state=42)

# Initialize logistic regression model
model = LogisticRegression()

# Fit the model on training data
model.fit(X_train, y_train)

# Coefficients (parameters) of the logistic regression model
coefficients = model.coef_

# Intercept of the logistic regression model
intercept = model.intercept_

print("Intercept:", intercept)
print("Coefficient for h1_Vs M_median:", coefficients[0][0])  # assuming the first column is for h1_Vs M_median
print("Coefficient for LPI:", coefficients[0][1])             # assuming the second column is for LPI

# Predict on the test set
y_pred = model.predict(X_test)

# Evaluate metrics
accuracy = accuracy_score(y_test, y_pred)
precision = precision_score(y_test, y_pred)
recall = recall_score(y_test, y_pred)
roc_auc = roc_auc_score(y_test, y_pred)

print(f"Accuracy: {accuracy}")
print(f"Precision: {precision}")
print(f"Recall: {recall}")
print(f"ROC-AUC: {roc_auc}")


# Perform cross-validation (e.g., 5-fold cross-validation)
cv_scores = cross_val_score(model, X, y, cv=5, scoring='accuracy')

print("Cross-validation scores:")
print(cv_scores)
print(f"Mean CV accuracy: {cv_scores.mean()}")
