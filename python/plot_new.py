import numpy as np
import matplotlib.pyplot as plt



# Define constants
kB = 8.617333262e-5
factor = 0.9003163162
Eb = 1.0



# Calculate rates
# temps = np.array([100*i for i in range(15, 21)]) # OLD 1
# temps = np.array([100*i for i in range(10, 16)]) # OLD 2
temps = np.array([50*i for i in range(20, 25)]) # NEW
temps_inv = 1 / temps
# rate_brute = np.array([3.826167e-04, 6.315928e-04, 9.122555e-04, 1.384604e-03, 1.905692e-03, 2.610109e-03]) # OLD 1
# rate_brute = np.array([8.311737e-06, 2.144097e-05, 5.231211e-05, 1.270616e-04, 2.181624e-04, 3.803282e-04]) # OLD 2
# rate_brute = np.array([8.179092e-06, 1.440374e-05, 2.304549e-05, 3.694538e-05, 5.623861e-05]) # NEW
rate_brute = np.array([8.195662e-06, 1.403123e-05, 2.234387e-05, 3.703013e-05, 5.759542e-05]) # NEW
rate_theory = factor * np.exp(- Eb / kB / temps)

# Fit theory to line
fit_brute = np.polyfit(temps_inv, np.log(rate_brute), 1)
fit_theory = np.polyfit(temps_inv, np.log(rate_theory), 1)

# Plot Arrhenius plot
plt.scatter(temps_inv, rate_theory, s=20, color='black')
plt.plot(temps_inv, np.exp(temps_inv*fit_theory[0]+fit_theory[1]), 'k--', label=r'Theory ($\Delta H$ = %.2e eV)' %Eb)
plt.scatter(temps_inv, rate_brute, s=20, color='red', marker='o', label=r"Numerical Results ($\Delta H$ = %.2e eV)" %(-fit_brute[0]*kB))
plt.yscale('log')
# plt.ylim([9e-3, 1.5e-1])
plt.xlabel(r'1/T [$\rm{K}^{-1}$]')
plt.ylabel(r'Transition Rate [$s^{-1}$]')
plt.legend()
# plt.minorticks_on()
# plt.grid(which='both', linestyle='-', linewidth='0.5', color='gray')
plt.savefig('arrhenius.png', dpi=300)
plt.clf()



# # Plot potential energy
# x = np.linspace(-1.6, 1.6, 100)
# u = x**4-2*x**2
# plt.plot(x, u, c='black')
# plt.xlabel(r'$x$')
# plt.title(r'$U(x) = x^4 - 2x^2$')
# plt.savefig('pot.png')
# plt.clf()