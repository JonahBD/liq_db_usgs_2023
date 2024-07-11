import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import roc_curve, auc
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LogisticRegression

#################################################################
# Inputs
df = pd.read_excel(r"C:\Users\jdundas2\OneDrive - Brigham Young University\Liq\Final Data\OG Data\liq_param_compiled_6-12.xlsx" )
columns_of_interest = ['LPI_results']
#################################################################
for method in columns_of_interest:
    # Split the data into features (X) and target variable (y)
    X = df[[method]].values  # Features
    y = df['Liquefaction'].values  # Target variable

    # Split data into training and testing sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.7, random_state=0) #ts = .7, rs=42

    # Fit a logistic regression model
    model = LogisticRegression()
    model.fit(X_train, y_train)

    # Predict probabilities for the test set
    probs = model.predict_proba(X_test)[:, 1]  # Probabilities for class 1 (liquefaction)

    # Compute ROC curve and ROC area
    fpr, tpr, thresholds = roc_curve(y_test, probs)  # Calculate false positive rate and true positive rate
    roc_auc = auc(fpr, tpr)  # Calculate area under the curve (AUC)

    # Plot ROC curve
    plt.figure()
    plt.plot(fpr, tpr, color='darkorange', lw=2, label='ROC curve (area = %0.2f)' % roc_auc)
    plt.plot([0, 1], [0, 1], color='navy', lw=2, linestyle='--')
    plt.xlim([0.0, 1.0])
    plt.ylim([0.0, 1.05])
    plt.xlabel('False Positive Rate')
    plt.ylabel('True Positive Rate')
    plt.title(f'Receiver Operating Characteristic (ROC) Analysis for {method}')
    plt.legend(loc="lower right")
    # plt.show()

    youden_j = tpr - fpr

    # Find the index of the maximum Youden's J
    optimal_threshold_index = np.argmax(youden_j)

    # Get the corresponding optimal threshold, sensitivity, and specificity
    optimal_threshold = thresholds[optimal_threshold_index]
    optimal_sensitivity = tpr[optimal_threshold_index]
    optimal_specificity = 1 - fpr[optimal_threshold_index]

    print("Optimal Threshold:", optimal_threshold)
    print("Optimal Sensitivity:", optimal_sensitivity)
    print("Optimal Specificity:", optimal_specificity)
    #--------------------------------------------------------------------------
    # Define a range of LPI threshold values to consider
    threshold_values = np.linspace(min(df[method]), max(df[method]), num=100)

    # Initialize variables to store performance metrics
    best_threshold = None
    best_youden_j = 0  # Initialize with 0
    best_predictions = None

    # Iterate over each threshold value
    for threshold in threshold_values:
        # Generate binary predictions based on the LPI threshold
        predictions = (df[method] >= threshold).astype(int)

        # Calculate true positive rate (sensitivity)
        tpr = (predictions[df['Liquefaction'] == 1] == 1).mean()

        # Calculate false positive rate
        fpr = (predictions[df['Liquefaction'] == 0] == 1).mean()

        # Calculate Youden's J statistic
        youden_j = tpr + (1 - fpr) - 1

        # Check if the current Youden's J statistic is better than the previous best
        if youden_j > best_youden_j:
            best_youden_j = youden_j
            best_threshold = threshold
            best_predictions = predictions

    print("Best Threshold (Youden's J):", best_threshold)
    print("Best Youden's J Statistic:", best_youden_j)

    #----------------------------------------------------------------------------
    import seaborn as sns
    import matplotlib.pyplot as plt

    # Filter the data based on the 'Liquefaction' column
    # Assuming that 'Liquefaction' contains binary indicators where one value indicates presence
    # and another value indicates absence of surficial liquefaction
    liquefaction_present = df[df['Liquefaction'] == 1]  # Assuming 1 indicates presence
    liquefaction_absent = df[df['Liquefaction'] == 0]  # Assuming 0 indicates absence

    # Plotting the KDE for both categories
    plt.figure(figsize=(10, 6))

    # KDE plot for cases where liquefaction is present
    sns.kdeplot(liquefaction_present[method], bw_adjust=0.5, label='Surficial Liquefaction Manifestation', color='black')

    # KDE plot for cases where liquefaction is absent
    sns.kdeplot(liquefaction_absent[method], bw_adjust=0.5, label='No Surficial Liquefaction Manifestation', color='blue')

    # Add labels and title
    plt.xlabel(f'{method}')
    plt.ylabel('Frequency')
    plt.title(f'Distribution of {method} with respect to Liquefaction Manifestation')

    # Add legend
    plt.legend()

    # Show the plot
    plt.show()