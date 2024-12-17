import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import matplotlib.patches as patches
from scipy.interpolate import make_interp_spline
import matplotlib.lines as mlines

x_axis = 'h1_basic'
y_axis = 'LPI'

# Sample DataFrame
df = pd.read_excel(r"C:\Users\hf233\OneDrive - Brigham Young University\Liq\Italy Data\Attempt 08 - OG\OG Data\liq_param_compiled_OG_A08.xlsx")
# df = df[(df["PGA"] > .4)]
# max_y = max(df[y_axis]+3)
max_y = 35


# Add custom patches
highlight_areas = [
    (5, 0, 45, max_y, 'A', 'orange'),
    (3, 0, 2, 5, 'B1', 'green'),
    (3, 5, 2, max_y, 'B2', 'blue'),
    (0, 0, 3, 5, 'B3', 'y'),  # x, y, width, height, label
    (0, 5, 3, max_y, 'C','red'), # x, y, width, height, label
]
patch_handles = []
for x, y, width, height, label, color in highlight_areas:
    rect = patches.Rectangle((x, y), width, height, color=color, alpha=0.3)
    plt.gca().add_patch(rect)
    # Create a legend patch handle
    patch_handles.append(patches.Patch(color=color, alpha=0.3, label=label))



df_manifestation = df[df['Liquefaction'] == 1]
df_no_manifestation = df[df['Liquefaction'] == 0]
plt.scatter(df_no_manifestation[x_axis], df_no_manifestation[y_axis], color='black', marker='x', label='No Manifestation')
plt.scatter(df_manifestation[x_axis], df_manifestation[y_axis], color='red', marker='o', label='Manifestation', alpha=.5)

# Sample dictionaries with x and y keys
line_1 = {'x': [0,5], 'y': [5,5]}
line_2 = {'x': [3,3], 'y': [0,max_y]}
line_3 = {'x': [5,5], 'y': [0,max_y]}

# Function to plot smooth lines for each dictionary
def plot_smooth_line(data_dict, label, color):
    # Retrieve x and y data
    x_data = data_dict['x']
    y_data = data_dict['y']
    # Plot the line
    plt.plot(x_data, y_data, color=color, label=label)

# Plot lines for each dictionary
plot_smooth_line(line_1, label="", color='blue')
plot_smooth_line(line_2, label="", color='blue')
plot_smooth_line(line_3, label="", color='blue')

# Add text annotations
# text_annotations = [
#     (1.5, 30, 'C'), (1.5, 2.5, 'B3'), (4, 1, 'B1'), (4, 30, 'B2'), (15, 15, 'A')
# ]
# for x, y, text in text_annotations:
#     plt.text(x, y, text, fontsize=12, ha='center', va='center', bbox=dict(facecolor='grey', edgecolor='none', boxstyle='round,pad=0.15', alpha=.75))



# Setting the axes and legend
plt.xlabel('H1b')
plt.ylabel(y_axis)
plt.legend()
plt.xlim(left=0,right=42)
plt.ylim(bottom=0, top=max_y)
plt.legend(handles=plt.gca().get_legend_handles_labels()[0] + patch_handles)
plt.title('Towhata (2016) Chart')
plt.show()
