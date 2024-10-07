import pandas as pd
import matplotlib.pyplot as plt

def scatterplot_2x2_matrix(df, columns, marker_column, plot_size=0.35):
    """
    Creates a 2x2 scatterplot matrix for the selected columns with customized markers for
    'No Manifestation' and 'Manifestation', and ensures equal width and height for all plots.

    :param df: The DataFrame containing the data.
    :param columns: List of 3 column names to include in the scatterplot matrix.
    :param marker_column: The column used to change the marker style (expects values 0 and 1).
    :param plot_size: Float representing the width and height of each plot. Default is 0.35.
    """
    # Ensure exactly 3 columns are selected
    if len(columns) != 3:
        raise ValueError("Exactly 3 columns must be provided for plotting.")

    # Define custom markers, labels, and colors
    marker_map = {0: 'x', 1: 'o'}
    label_map = {0: 'No Manifestation', 1: 'Manifestation'}
    color_map = {0: 'black', 1: 'red'}
    alpha_map = {0: 1, 1: 0.5}  # Full transparency for 'No Manifestation', 50% transparency for 'Manifestation'
    marker_size = 25

    # Create a 2x2 grid of scatter plots
    fig, axes = plt.subplots(2, 2, figsize=(10, 10))

    # Scatter plot for h2_cumulative (Y) vs LPI (X) (top-left, aligned with bottom-left x-axis)
    ax = axes[0, 0]
    for marker_val in [0, 1]:
        df_filtered = df[df[marker_column] == marker_val]
        ax.scatter(df_filtered[columns[1]], df_filtered[columns[0]],
                   marker=marker_map[marker_val],
                   label=label_map[marker_val],
                   color=color_map[marker_val],
                   alpha=alpha_map[marker_val], s=marker_size)
    ax.set_ylabel('H2c (m)')  # h2_cumulative on Y-axis
    ax.set_xticks([])  # Remove x-ticks from the top-left plot
    ax.set_xlabel('')  # Remove x-axis label

    # Scatter plot for PGA (Y) vs LPI (X) (bottom-left)
    ax_bottom_left = axes[1, 0]
    for marker_val in [0, 1]:
        df_filtered = df[df[marker_column] == marker_val]
        ax_bottom_left.scatter(df_filtered[columns[1]], df_filtered[columns[2]],
                               marker=marker_map[marker_val],
                               label=label_map[marker_val],
                               color=color_map[marker_val],
                               alpha=alpha_map[marker_val], s=marker_size)
    ax_bottom_left.set_xlabel(columns[1])  # LPI on X-axis
    ax_bottom_left.set_ylabel('PGA (g)')  # PGA on Y-axis

    # Align top-left plot with the bottom-left plot's x-axis, use the same plot size for both
    ax.set_position([0.1, 0.55, plot_size, plot_size])  # Adjust top-left plot position and size
    ax_bottom_left.set_position([0.1, 0.15, plot_size, plot_size])  # Adjust bottom-left plot position and size

    # Scatter plot for PGA (Y) vs h2_cumulative (X) (bottom-right, y-axis aligned with the right edge)
    ax_bottom_right = axes[1, 1]
    for marker_val in [0, 1]:
        df_filtered = df[df[marker_column] == marker_val]
        ax_bottom_right.scatter(df_filtered[columns[0]], df_filtered[columns[2]],
                                marker=marker_map[marker_val],
                                label=label_map[marker_val],
                                color=color_map[marker_val],
                                alpha=alpha_map[marker_val], s=marker_size)
    ax_bottom_right.set_xlabel('H2c (m)')  # h2_cumulative on X-axis
    ax_bottom_right.set_yticks([])  # Remove y-ticks

    ax_right_pos = ax_bottom_left.get_position()  # Get the position of the bottom-right plot
    ax_bottom_right.set_position([ax_right_pos.x0 +plot_size , ax_right_pos.y0, plot_size, plot_size])  # Adjust bottom-right plot position and size

    # Add legend to the empty top-right plot, also using the same plot size
    axes[0, 1].axis('off')  # Remove axis from top-right plot (properly)
    handles, labels = ax.get_legend_handles_labels()
    axes[0, 1].legend(handles, labels, loc='center', fontsize=12, markerscale=1.5, frameon=False)
    axes[0, 1].set_position([plot_size,plot_size, plot_size, plot_size])  # Adjust legend area to match plot size

    # Adjust layout to remove extra white space
    # plt.subplots_adjust(left=0.1, right=0.95, top=0.95, bottom=0.1, wspace=0.3, hspace=0.3)

    plt.show()

# Example usage:

# Load your data
df = pd.read_excel(r"C:\Users\hf233\OneDrive - Brigham Young University\Liq\Italy Data\Attempt 08 - OG\OG Data\log_reg_parameters_OG_A08.xlsx")  # Replace with your file path

# Call the function to plot with dynamically selected columns
# You can modify plot_size to adjust the width and height of each plot
scatterplot_2x2_matrix(df, columns=['h2_cumulative', 'LPI', 'PGA'], marker_column='Liquefaction', plot_size=0.4)

# 'H2c'
