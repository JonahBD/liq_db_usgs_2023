import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Load data (replace with your actual path)
df = pd.read_excel(
    r"C:\Users\hf233\OneDrive - Brigham Young University\Liq\Italy Data\Attempt 08 - OG\OG Data\log_reg_parameters_OG_A08_first30.xlsx")
vars = ["h2_cumulative", "LPI"]
linear_predictors = [-3.4012429703011, 0.230174481116412, 0.153672176172119]  # Logistic regression coefficients

# Function to calculate the y value for a given probability and x
def calculate_y_for_probability(x_vals, probability, coefs):
    # Rearrange the logistic regression equation and solve for y
    z = np.log((probability) / (1-probability))  # inverse of the sigmoid np.log(probability / (1 - probability))
    y_vals = (z - coefs[0] - coefs[1] * x_vals) / coefs[2]
    return y_vals


# Plot function
def plot_data_with_lines(df, x_col, y_col, marker_col, variables, linear_predictors):
    plt.figure(figsize=(6, 5))

    # Separate data points by marker_col and plot them once with labels
    df_marker_1 = df[df[marker_col] == 1]
    df_marker_0 = df[df[marker_col] == 0]

    # Plot manifestation markers (solid red circles)
    plt.scatter(df_marker_0[x_col], df_marker_0[y_col], facecolors='black', edgecolors='black', marker='+',
                label='No Manifestation')
    # plt.scatter(df_marker_1[x_col], df_marker_1[y_col], color='#FFF3F3', marker='o', label='Manifestation', edgecolors='#EA0000')
    plt.scatter(df_marker_1[x_col], df_marker_1[y_col], color='red', marker='o', label='Manifestation',edgecolors='black', alpha=.55)

    # Plot no manifestation markers (open circles with black border and white fill)


    # Generate x values for plotting
    x_vals = np.linspace(df[x_col].min(), df[x_col].max(), 100)

    # Calculate the y values for different probabilities
    y_vals_50 = calculate_y_for_probability(x_vals, 0.5, linear_predictors)  # 50% probability
    y_vals_15 = calculate_y_for_probability(x_vals, 0.15, linear_predictors)  # 15% probability
    y_vals_85 = calculate_y_for_probability(x_vals, 0.85, linear_predictors)  # 85% probability
    y_vals_6 = calculate_y_for_probability(x_vals, 0.06, linear_predictors)

    # Plot the probability lines
    plt.plot(x_vals, y_vals_50, c='blue', label='50% Probability Line')
    plt.plot(x_vals, y_vals_15, c='orange', label='15% Probability Line')
    plt.plot(x_vals, y_vals_85, c='green', label='85% Probability Line')
    plt.plot(x_vals, y_vals_6, c='red', label='6% Probability Line')

    # Add labels, title, and legend with white background
    plt.xlabel(x_col)
    plt.ylabel(y_col)
    plt.title('Probability of Liquefaction')

    # Customize the legend to have a white background
    plt.legend(loc='best', frameon=True, facecolor='white', edgecolor='black',framealpha=1)
    plt.grid(True)
    plt.ylim(bottom=0)
    plt.xlim(0)
    plt.xlabel(vars[0])

    # Show the plot
    plt.show()


# Example usage with columns 'h1_φ\' R_median', 'LPI', and 'Liquefaction' marker
plot_data_with_lines(df, vars[0], vars[1], 'Liquefaction', vars, linear_predictors)
