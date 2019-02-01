#!/bin/bash
#PBS -P FGEN
#PBS -l select=1:ncpus=4:mem=100GB
#PBS -l walltime=120:00:00
#PBS -M vanessa.marcelino@sydney.edu.au
#PBS -m ae

cd $PBS_O_WORKDIR

python rename_nt.py

