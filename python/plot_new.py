import numpy as np
import matplotlib.pyplot as plt



# Define constants
kB = 8.617333262e-5
factor = 0.9003163162
Eb = 1.0



# Calculate rates
temps = np.array([1000*i for i in range(3, 8)])
temps_inv = 1 / temps
rate_brute = np.array([1.509312e-02, 4.250627e-02, 6.879322e-02, 1.029381e-01, 1.338356e-01]) # NEW
rate_theory = factor * np.exp(- Eb / kB / temps)

# Fit theory to line
fit_brute = np.polyfit(temps_inv, np.log(rate_brute), 1)
fit_theory = np.polyfit(temps_inv, np.log(rate_theory), 1)

# Plot Arrhenius plot
plt.scatter(temps_inv, rate_theory, s=20, color='black')
plt.plot(temps_inv, np.exp(temps_inv*fit_theory[0]+fit_theory[1]), 'k--', label=r'Theory ($\Delta H$ = %.2e eV)' %Eb)
plt.scatter(temps_inv, rate_brute, s=20, color='red', label=r"Numerical Results ($\Delta H$ = %.2e eV)" %(-fit_brute[0]*kB))
plt.yscale('log')
# plt.ylim([9e-3, 1.5e-1])
plt.xlabel(r'1/T [$\rm{K}^{-1}$]')
plt.ylabel(r'Transition Rate [$s^{-1}$]')
plt.legend()
# plt.minorticks_on()
# plt.grid(which='both', linestyle='-', linewidth='0.5', color='gray')
plt.savefig('arrhenius.png')
plt.clf()



# Plot potential energy
x = np.linspace(-1.6, 1.6, 100)
u = x**4-2*x**2
plt.plot(x, u, c='black')
plt.xlabel(r'$x$')
plt.title(r'$U(x) = x^4 - 2x^2$')
plt.savefig('pot.png')
plt.clf()