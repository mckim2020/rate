import numpy as np
import matplotlib.pyplot as plt



# Define constants
kB = 8.617333262e-5
factor = 0.9003163162
Eb = 1.0



temp = 1200
mu = 0.05
num_itr = 100



timesteps = [2e-1, 8e-2, 4e-2, 2e-2, 8e-3, 4e-3, 2e-3, 1e-3, 5e-4]
rates = [2.937773e-06, 2.652021e-06, 2.388562e-06, 2.679862e-06, 2.181016e-06, 2.811027e-06, 2.563238e-06, 2.345299e-06, 4.712532e-06]



# Sort timesteps and corresponding rates in decreasing order
sorted_timesteps, sorted_rates = zip(*sorted(zip(timesteps, rates), reverse=True))

# Plotting
plt.figure(figsize=(8, 6))
plt.plot(sorted_timesteps, sorted_rates, marker='o', color='black', label='1200K')
plt.xscale('log')  # Using a logarithmic scale for timesteps
plt.xlabel('Time Step Size')
plt.ylabel('Transition Rates')
plt.grid(True)
plt.legend()
plt.show()