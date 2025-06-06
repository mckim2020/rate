import os, sys, argparse, numpy as np
from python.rate_util import compute_reference_rate, read_fpt_data, plot_fpt_histogram, plot_arrhenius



parser = argparse.ArgumentParser("Compute rate from FPT data")
parser.add_argument('--temp', type=int, default=1500, help="temperature in Kelvin")
parser.add_argument('--mu', type=float, default=0.02, help="mobility constant (default is 0.02)")
parser.add_argument('--kB', type=float, default=8.617333262e-5, help="Boltzmann constant (default is 8.617333262e-5)")
parser.add_argument('--factor', type=float, default=0.9003163162, help="pre-exponential factor (default is 0.9003163162)")
parser.add_argument('--fpt_dir', type=str, default="./data", help="directory containing first passage time data")
parser.add_argument('--bins', type=int, default=1000, help="number of bins for histogram (default is 1000)")
parser.add_argument('--verbose', action='store_true', help="print verbose output")
args = parser.parse_args()



# Reference data
rate_ref = compute_reference_rate(args.temp, args.mu, args.kB, args.factor)
if args.verbose: print(f"Reference rate at {args.temp} K: {rate_ref:.2e} s^-1")

# Read data from file
fpt_data = read_fpt_data(os.path.join(args.fpt_dir, 
                        f"fpt_values_{args.temp}_final.txt"),
                        dtype='int', dt=1e-2)
rate_fpt = 1.0 / np.mean(fpt_data)
if args.verbose: print(f"Brute-force rate from FPT data at {args.temp} K: {rate_fpt:.2e} s^-1")

# Create histogram
plot_fpt_histogram(fpt_data, args.temp, args.bins)
if args.verbose: print(f"Histogram saved as fpt_histogram_{args.temp}.png")

# Arrhenius plot
plot_arrhenius()
if args.verbose: print("Arrhenius plot saved as arrhenius.png")