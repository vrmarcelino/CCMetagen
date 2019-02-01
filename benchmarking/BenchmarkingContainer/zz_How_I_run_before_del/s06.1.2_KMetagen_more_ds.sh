#!/bin/bash
#PBS -P FGEN
#PBS -l select=1:ncpus=2:mem=100GB
#PBS -l walltime=5:00:00

cd $PBS_O_WORKDIR

# when running locally:
#PATH=$PATH:/Users/vanessamarcelino/OneDrive\ -\ The\ University\ of\ Sydney\ \(Staff\)/OneDrive_VRM/KMetagen_project/KMetagen/tools

# when running on Artemis:
PATH=$PATH:/home/vros8020/FGEN_project/programs/KMetagen/tools
PATH=$PATH:/home/vros8020/FGEN_project/programs/KronaTools-2.7/bin

module load python/3.6.5

input_dir=06_TaxAssign/KMA_more_ds
out_fp=06_TaxAssign/KMetagen_more_ds
mkdir -p $out_fp



## nt
for f in $input_dir/*nt.res; do 
	out=$out_fp/${f/$input_dir\/}
	time KMetagen.py -i $f -r nt -o $out
done


echo "done!"



