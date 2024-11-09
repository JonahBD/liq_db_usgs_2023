import random
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Step 1: Create a sample DataFrame

df = pd.read_excel(r"C:\Users\jdundas2\OneDrive - Brigham Young University\Liq\Italy Data\Attempt 05 - PGA, 10-100\10-100 subset\liq_methods_performance_10-100_without_clay_A05.xlsx")
h1_basic = 0.460780521
LPI =
Vs =
max_effective =

liq_df = df[(df['Liquefaction'] == 1) & (df["PGA"] > pga - 0.001)]
no_liq_df = df[(df['Liquefaction'] == 0) & (df["PGA"] > pga - 0.001)]
x = "h2_cumulative"
y = "LPI"

# a is the intercept at a given pga value
a = -8.92037390038764 + 11.7649657769085 * pga
# b * h2_cumulative
b = 0.34050373061748
# c * LPI
c = 0.0869353182127432

coefficients = [a, b, c]

def y_probabilities(coe, x_value, y_prob):
    return (-np.log(1 / y_prob - 1) - coe[0] - coe[1] * x_value) / coe[2]

x_values = np.linspace(0, 10, 100)
y_values_10prob = y_probabilities(coefficients, x_values, .076)
y_values_20prob = y_probabilities(coefficients, x_values, .15)
y_values_30prob = y_probabilities(coefficients, x_values, .50)
y_values_40prob = y_probabilities(coefficients, x_values, .85)


# Step 2: Create a plot
plt.figure(figsize=(10, 6))

# Step 3: Plot the DataFrames
plt.scatter(no_liq_df[x], no_liq_df[y], label='No Manifestation', color='black', marker='x')
plt.scatter(liq_df[x], liq_df[y], label='Manifestation', color='red', marker='o', alpha=0.5)

plt.plot(x_values, y_values_10prob, color='#598bd5', linestyle='-', linewidth=2, label="7.6% probability")
plt.plot(x_values, y_values_20prob, color='#008000', linestyle='-', linewidth=2, label="15% probability")
plt.plot(x_values, y_values_30prob, color='#ffc002', linestyle='-', linewidth=2, label="50% probability")
plt.plot(x_values, y_values_40prob, color='#b0001e', linestyle='-', linewidth=2, label="85% probability")

# Step 5: Customize the plot
plt.title('Model 1 when PGA = 0.46g')
plt.xlabel("H2c (m)")
plt.ylabel(y)
plt.axhline(0, color='black', lw=0.5, ls='None')  # Optional: x-axis
plt.axvline(0, color='black', lw=0.5, ls='None')  # Optional: y-axis
plt.ylim(0,40)
plt.xlim(0,8)
plt.legend(loc="lower right")
plt.grid()
plt.show()
