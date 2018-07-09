#!/bin/bash
#PBS -P FGEN
#PBS -l select=1:ncpus=2:mem=100GB
#PBS -l walltime=48:00:00

cd $PBS_O_WORKDIR

module load python/3.5.1

time python add_taxid_to_ITSdb.py 

