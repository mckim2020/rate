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


def read_fpt_data(filename):
    """
    Read first passage time data from a file.
    
    Parameters
    ----------
    filename: Path to the file containing FPT data.
    
    Returns
    -------
    Numpy array of first passage times.
    """
    try:
        data = np.loadtxt(filename)
        return data
    except Exception as e:
        print(f"Error reading file {filename}: {e}")
        return None