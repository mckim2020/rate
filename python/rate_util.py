import numpy as np



def compute_reference_rate(temp, mu=0.02, kB=8.617333262e-5, factor=0.9003163162):
    """
    Compute the reference rate based on temperature and other parameters.
    
    Parameters
    ----------
    temp: Temperature in Kelvin.
    mu: Mobility constant (default is 0.02).
    kB: Boltzmann constant (default is 8.617333262e-5).
    factor: Pre-exponential factor (default is 0.9003163162).
    
    Returns
    -------
    Reference rate in s^-1.
    """
    return mu * factor * np.exp(-1.0 / (kB * temp))


def read_fpt_data(filename, dtype='int', dt=1e-2):
    """
    Read first passage time data from a file.
    
    Parameters
    ----------
    filename: Path to the file containing FPT data.
    dtype: Data type of the FPT values ('int' or 'long_int').
    dt: Time step in seconds (default is 0.01) 
        - only used if dtype is 'int' 
        - when overflow.
    
    Returns
    -------
    Numpy array of first passage times.
    """
    data = np.loadtxt(filename)
    fpt_values = []

    if dtype == 'int':
        max_int32 = 2**31 - 1

        for x in data:
            if x < 0: x = (2 * (max_int32 + 1) + x / dt) * dt
            fpt_values.append(x)

    else:
        fpt_values = data
    
    return np.array(fpt_values)


def plot_fpt_histogram(fpt_data, temp, bins=1000):
    import matplotlib.pyplot as plt

    plt.figure(figsize=(8, 8))
    plt.tick_params(axis='both', direction='in')
    plt.hist(fpt_data, bins=bins, edgecolor='black', alpha=0.7)
    plt.xticks(fontsize=18)
    plt.yticks(fontsize=18)
    # plt.title('Histogram of Data')
    plt.xlabel('First Passage Times (s)', fontsize=18)
    plt.ylabel('Frequency', fontsize=18)
    plt.grid(alpha=0.3)
    plt.axvline(np.mean(fpt_data), color='red', linestyle='dashed', linewidth=5, label=f'MFPT: {np.mean(fpt_data):.2e}')
    # plt.axvline(np.median(data), color='green', linestyle='dashed', linewidth=1, label=f'Median: {np.median(data):.2e}')
    plt.legend(fontsize=18)
    plt.yscale('log')
    plt.tight_layout()
    plt.savefig(f"fpt_histogram_{temp}.png", dpi=300)
    plt.clf()


def plot_arrhenius():
    import matplotlib.pyplot as plt

    temps = np.array([1000, 1100, 1200, 1300, 1400, 1500])
    brute_rates = np.array([1.68e-07, 4.68e-07, 1.13e-06, 2.36e-06, 4.44e-06, 7.66e-06])
    exact_rates = np.array([1.64e-07, 4.72e-07, 1.14e-06, 2.39e-06, 4.52e-06, 7.86e-06])

    plt.figure(figsize=(8, 8))
    plt.tick_params(axis='both', direction='in')
    plt.plot(1 / temps, exact_rates, 'k--', label='Kramers', linewidth=2.5)
    plt.scatter(1 / temps, brute_rates, 
                facecolors='none',
                edgecolors='blue',
                linewidths=1.5,
                s=100,
                label='Brute-force')
    plt.xlabel(r'$T^{-1}$ (1/K)', fontsize=20)
    plt.ylabel(r'Transition Rate (s$^{-1}$)', fontsize=20)
    plt.grid(True, linestyle='--', alpha=0.7)
    plt.yscale('log')
    plt.legend(fontsize=20)
    plt.tight_layout()
    plt.savefig('./arrhenius.png', dpi=300)
    plt.clf()