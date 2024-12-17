import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from scipy.interpolate import make_interp_spline

# Sample DataFrame
df = pd.read_excel(r"C:\Users\hf233\OneDrive - Brigham Young University\Liq\Italy Data\Attempt 08 - OG\OG Data\liq_param_compiled_OG_A08.xlsx")
df = df[(df["PGA"] > .4)]
y_axis = 'h2_cumulative'

df_manifestation = df[df['Liquefaction'] == 1]
df_no_manifestation = df[df['Liquefaction'] == 0]
plt.scatter(df_no_manifestation['h1_basic'], df_no_manifestation[y_axis], color='black', marker='x', label='No Manifestation')
plt.scatter(df_manifestation['h1_basic'], df_manifestation[y_axis], color='red', marker='o', label='Manifestation', alpha=.55)

# Sample dictionaries with x and y keys
ishihara_curve = {'x': [1,2,3,5,6,6.5,7,7.5,8,8.55,9,9.25,9.5], 'y': [0.35,0.7,1.09,1.825,2.15,2.35,2.55,2.9,3.5,4.7,6,7,8]}

# Function to plot smooth lines for each dictionary
def plot_smooth_line(data_dict, label, color):
    # Retrieve x and y data
    x_data = data_dict['x']
    y_data = data_dict['y']

    # Plot the smooth line
    plt.plot(x_data, y_data, color=color, label=label)

# Plot lines for each dictionary
plot_smooth_line(ishihara_curve, 'Ishihara Curve 0.4g-0.5g', '#FFC000')

# Define the equation and add it to the plot
x_values = np.linspace(1, max(df['h1_basic']), 400)  # Assume H1 basic goes up to the max of current data or specify your range
y_values = 0.0217 * (0.45**-1.9481) * (x_values**1.5688)
plt.plot(x_values, y_values, 'green', label='Ishihara Power Law at 0.45g')  # Plotting the equation

# Adding labels and legend
plt.xlabel('H1b (m)')
plt.ylabel("H2c (m)")
plt.legend()
plt.xlim(left=0)
plt.ylim(bottom=0, top=8)
plt.title('Ishihara Curves for 0.4g-0.5g')

plt.text(6,7.5, 'Predicted\nManifestation', fontsize=7, ha='center', va='center',bbox=dict(facecolor='none', edgecolor='black', boxstyle='round,pad=0.1'))#
plt.text(25, 5, 'No Predicted\nManifestation', fontsize=7, ha='center', va='center', bbox=dict(facecolor='none', edgecolor='black', boxstyle='round,pad=0.1'))

plt.show()
