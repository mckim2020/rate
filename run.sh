#!/bin/sh

for i in 1000 1100 1200 1300 1400 1500;
do
	sbatch run_cpu.sbatch $i;
done