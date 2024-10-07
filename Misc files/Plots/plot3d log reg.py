import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

# Load data (replace with your actual path)
df = pd.read_excel(
    r"C:\Users\hf233\OneDrive - Brigham Young University\Liq\Italy Data\Model Building\OG\log_reg_parameters_OG_A05.xlsx")
vars = ["h1_φ' R_median","h2_cumulative", 'LPI']  # Added another variable for 3D
linear_predictors = [-3.4012429703011+2.68658450501996,-0.0849101353467824, 0.230174481116412,0.153672176172119]  # Updated coefficients

# Function to calculate the z value for a given probability, x, and y
def calculate_z_for_probability(x_vals, y_vals, probability, coefs):
    # Rearrange the logistic regression equation and solve for z
    z = np.log((probability) / (1 - probability))  # inverse of the sigmoid np.log(probability / (1 - probability))
    z_vals = (z - coefs[0] - coefs[1] * x_vals - coefs[2] * y_vals) / coefs[3]  # Adjusted for 3rd variable (PGA)
    return z_vals

# Plot function in 3D
def plot_3d_with_lines(df, x_col, y_col, z_col, marker_col, variables, linear_predictors):
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(111, projection='3d')

    # Separate data points by marker_col and plot them once with labels
    df_marker_1 = df[df[marker_col] == 1]
    df_marker_0 = df[df[marker_col] == 0]

    # Plot manifestation markers (solid red circles)
    ax.scatter(df_marker_0[x_col], df_marker_0[y_col], df_marker_0[z_col], c='black', marker='+',
               label='No Manifestation')
    ax.scatter(df_marker_1[x_col], df_marker_1[y_col], df_marker_1[z_col], c='red', marker='o',
               label='Manifestation', edgecolors='black', alpha=0.55)

    # Generate grid for x and y values for plotting probability lines
    x_vals = np.linspace(df[x_col].min(), df[x_col].max(), 100)
    y_vals = np.linspace(df[y_col].min(), df[y_col].max(), 100)
    X, Y = np.meshgrid(x_vals, y_vals)

    # Calculate z values for different probabilities
    Z_50 = calculate_z_for_probability(X, Y, 0.5, linear_predictors)  # 50% probability
    Z_15 = calculate_z_for_probability(X, Y, 0.15, linear_predictors)  # 15% probability
    Z_85 = calculate_z_for_probability(X, Y, 0.85, linear_predictors)  # 85% probability
    Z_6 = calculate_z_for_probability(X, Y, 0.06, linear_predictors)  # 6% probability

    # Plot the probability surfaces
    ax.plot_surface(X, Y, Z_50, color='blue', alpha=0.3, label='50% Probability Surface')
    ax.plot_surface(X, Y, Z_15, color='orange', alpha=0.3, label='15% Probability Surface')
    ax.plot_surface(X, Y, Z_85, color='green', alpha=0.3, label='85% Probability Surface')
    ax.plot_surface(X, Y, Z_6, color='red', alpha=0.3, label='6% Probability Surface')

    # Set labels
    ax.set_xlabel(x_col)
    ax.set_ylabel(y_col)
    ax.set_zlabel(z_col)
    ax.set_title('3D Probability of Liquefaction')

    # Set axes limits to start from 0
    ax.set_xlim([0, df[x_col].max()])
    ax.set_ylim([0, df[y_col].max()])
    ax.set_zlim([1, df[z_col].max()])

    # Add legend with a white background
    ax.legend(loc='best', frameon=True, facecolor='white', edgecolor='black')
    plt.show()

# Example usage with columns 'h2_cumulative', 'LPI', 'PGA', and 'Liquefaction' marker
plot_3d_with_lines(df, vars[0], vars[1], vars[2], 'Liquefaction', vars, linear_predictors)
