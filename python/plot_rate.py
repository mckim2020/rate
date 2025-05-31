# Read FPT values from txt file
import numpy as np
import matplotlib.pyplot as plt



# Define lists to record data
temp_list = [1000, 1100, 1200, 1300, 1400, 1500]
rate_list_num = []
rate_list_theory = []

# Read and compute rates
for temp in temp_list:
    # Numerical rate
    file_name = '../data/fpt_values_' + str(temp) + '.txt'
    fpt_values = []

    with open(file_name, 'r') as file:
        for line in file:
            fpt_values.append(float(line.strip()))

            if float(line.strip()) < 0:
                print("HELLO!")

    fpt_values = np.array(fpt_values)
    rate_num = 1 / np.mean(fpt_values)
    rate_list_num.append(rate_num)

    # Theoretical rate
    mu = 0.02
    factor = 0.9003163162
    kB = 8.617333262e-5

    rate_theory = mu * factor * np.exp(-1.0 / kB / temp)
    rate_list_theory.append(rate_theory)

# Convert to numpy arrays
temp_array = np.array(temp_list)
rate_array_num = np.array(rate_list_num)
rate_array_theory = np.array(rate_list_theory)

plt.scatter(1/temp_array, rate_array_num, c='red', label='Numerical Rate')
plt.plot(1/temp_array, rate_array_theory, 'k:', label='Theoretical Rate')
plt.xticks(1/temp_array, labels=[f'{temp:d}' for temp in temp_array])
plt.yscale('log')
plt.xlabel('Temperature [K]')
plt.ylabel(r'Transition Rate [$s^{-1}$]')
plt.legend()
plt.savefig('./rate.png', dpi=300)
# plt.show()
plt.clf()