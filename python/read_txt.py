# Read FPT values from txt file
import numpy as np
import matplotlib.pyplot as plt



file_name = '../data/fpt_values.txt'
fpt_values = []

with open(file_name, 'r') as file:
    for line in file:
        fpt_values.append(float(line.strip()))

fpt_values = np.array(fpt_values)

# Plot histogram
plt.hist(fpt_values, range=(0, 1e6), bins=100, color='blue', alpha=0.3)
plt.xlabel('First Passage Time')
plt.ylabel('Frequency')
plt.savefig('hist_fpt.png')
plt.clf()

# Obtain CDF
bins = np.linspace(fpt_values.min(), fpt_values.max(), 1000)
dx = bins[1] - bins[0]
count_dens, bin_edges = np.histogram(fpt_values, bins, density=True)
one_min_cdf = 1 - np.cumsum(count_dens * dx)
log_one_min_cdf = np.log(one_min_cdf)
bin_centers = (bin_edges[1:] + bin_edges[:-1]) / 2

# Plot CDF
plt.plot(bin_centers, one_min_cdf)
plt.savefig('cdf_fpt.png')
plt.clf()

# Plot log of CDF
plt.plot(bin_centers, log_one_min_cdf)
plt.savefig('log_cdf_fpt.png')
plt.clf()

# Fit 