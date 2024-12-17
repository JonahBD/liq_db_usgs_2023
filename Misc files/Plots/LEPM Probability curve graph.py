import random
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Step 1: Create a sample DataFrame

df = pd.read_excel(r"C:\Users\hf233\OneDrive - Brigham Young University\Liq\Italy Data\Model Building 02\All Sites\log_reg_parameters_model_all_MORE.xlsx")
h1_basic = 11
LPI = 5
Vs = 150
max_effective = 110

# col_names = ["LPI", "h1_basic","h1_Vs R (m/s)_mean", "Max effective stress" ]
holding_constant_1 = "h1_basic"
holding_constant_2 = "h1_Vs R (m/s)_mean"
limit_1 = h1_basic
limit_2 = Vs

liq_df = df[(df['Liquefaction'] == 1) & (df[holding_constant_1] > limit_1 * .90) & (df[holding_constant_1] < limit_1 * 1.1)& (df[holding_constant_2] > limit_2 * .90)& (df[holding_constant_2] < limit_2 * 1.1)]
no_liq_df = df[(df['Liquefaction'] == 0) & (df[holding_constant_1] > limit_1 * .90) & (df[holding_constant_1] < limit_1 * 1.1)& (df[holding_constant_2] > limit_2 * .90)& (df[holding_constant_2] < limit_2 * 1.1)]
x = "LPI"
y = "Max effective stress"

# a is the intercept at a given pga value
a = -0.389496479708949 * limit_1 + -0.0224933862867034 * limit_2
# b * x
b = 0.16380123229265
# c * y
c = 0.0416527762192667

coefficients = [a, b, c]

def y_probabilities(coe, x_value, y_prob):
    return (-np.log(1 / y_prob - 1) - coe[0] - coe[1] * x_value) / coe[2]

x_values = np.linspace(0, 5000, 500)
y_values_10prob = y_probabilities(coefficients, x_values, .067)
y_values_20prob = y_probabilities(coefficients, x_values, .15)
y_values_30prob = y_probabilities(coefficients, x_values, .50)
y_values_40prob = y_probabilities(coefficients, x_values, .85)


# Step 2: Create a plot
plt.figure(figsize=(5, 4.5))

# Step 3: Plot the DataFrames
plt.scatter(no_liq_df[x], no_liq_df[y], label='No Manifestation', color='black', marker='x')
plt.scatter(liq_df[x], liq_df[y], label='Manifestation', color='red', marker='o', alpha=0.5)

plt.plot(x_values, y_values_10prob, color='#598bd5', linestyle='-', linewidth=2, label="6.7% probability")
plt.plot(x_values, y_values_20prob, color='#008000', linestyle='-', linewidth=2, label="15% probability")
plt.plot(x_values, y_values_30prob, color='#ffc002', linestyle='-', linewidth=2, label="50% probability")
plt.plot(x_values, y_values_40prob, color='#b0001e', linestyle='-', linewidth=2, label="85% probability")

# Step 5: Customize the plot
plt.title(f'H1b (m) ={limit_1} and H1b Vs M mean (m/s)={limit_2}')
plt.xlabel('LPI')
plt.ylabel('Effective Stress at Bottom of H1b (kPa)')
plt.axhline(0, color='black', lw=0.5, ls='None')  # Optional: x-axis
plt.axvline(0, color='black', lw=0.5, ls='None')  # Optional: y-axis
plt.xlim(0,30)
plt.ylim(0,260)
plt.legend(loc="lower right")
plt.grid()
plt.legend('',frameon=False)
plt.show()
