#!/bin/bash

#SBATCH --job-name="brute"            # Job name
#SBATCH -p cpu                        # GPU Parition requested
#SBATCH --output=brute.out            # GPU output file
#SBATCH --error=brute.err             # GPU error file



gcc ./c/parallel/bfc_1d_$1.c -o bfc_1d_$1 -lm
./bfc_1d_$1