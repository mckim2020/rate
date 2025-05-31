import numpy as np
import matplotlib.pyplot as plt
from matplotlib.ticker import LogLocator, FormatStrFormatter



# Define constants
kB = 8.617333262e-5
factor = 1.5005271936
Eb = 2.08333333333

# Calculate rates
temps = np.array([1000*i for i in range(5, 11)])
temps_inv = 1 / temps
rate_brute = np.array([1.487890e-2, 2.836256e-2, 5.702567e-2, 7.979205e-2, 1.154460e-1, 1.341438e-1]) # OLD
rate_theory = factor * np.exp(- Eb / kB / temps)

# Fit theory to line
fit_brute = np.polyfit(temps_inv, np.log(rate_brute), 1)
fit_theory = np.polyfit(temps_inv, np.log(rate_theory), 1)

# Plot Arrhenius plot
plt.scatter(temps_inv, rate_theory, s=20, color='black')
plt.plot(temps_inv, np.exp(temps_inv*fit_theory[0]+fit_theory[1]), 'k--', label=r'Theory ($\Delta H$ = %.2e eV)' %Eb)
plt.scatter(temps_inv, rate_brute, s=20, color='red', label=r"Numerical Results ($\Delta H$ = %.2e eV)" %(-fit_brute[0]*kB))
plt.yscale('log')
plt.ylim([9e-3, 1.5e-1])
plt.xlabel(r'1/T [$\rm{K}^{-1}$]')
plt.ylabel(r'Transition Rate [$s^{-1}$]')
plt.legend()
# plt.minorticks_on()
# plt.grid(which='both', linestyle='-', linewidth='0.5', color='gray')
plt.savefig('arrhenius.png')
plt.clf()



# Plot potential energy
x = np.linspace(-1.6, 1.6, 100)
u = 4/3*x**4 - 10/3*x**2 + 2
plt.plot(x, u, c='black')
plt.xlabel(r'$x$')
plt.ylabel(r'$U(x)$')
plt.savefig('pot.png')
plt.clf()