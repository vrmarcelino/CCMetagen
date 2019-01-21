#!/bin/bash
#PBS -P FGEN
#PBS -l select=1:ncpus=4:mem=100GB
#PBS -l walltime=5:00:00

cd $PBS_O_WORKDIR

# when running locally:
#PATH=$PATH:/Users/vanessamarcelino/OneDrive\ -\ The\ University\ of\ Sydney\ \(Staff\)/OneDrive_VRM/KMetagen_project/KMetagen/tools

# when running on Artemis:
PATH=$PATH:/home/vros8020/FGEN_project/programs/KMetagen/tools
PATH=$PATH:/home/vros8020/FGEN_project/programs/KronaTools-2.7/bin

module load python/3.6.5

input_dir=06_TaxAssign/KMA
out_fp=06_TaxAssign/KMetagen
mkdir -p $out_fp



# Run KMetagen (with KMA 1.1.4 for ITS)
for f in $input_dir/*ITS.res; do 
	out=$out_fp/${f/$input_dir\/}
	time KMetagen.py -i $f -r UNITE -o $out
done


## RefSeq
for f in $input_dir/*refSeq_f_part.res; do 
	out=$out_fp/${f/$input_dir\/}
	time KMetagen.py -i $f -r RefSeq -o $out
done

for f in $input_dir/*refSeq_bf.res; do 
	out=$out_fp/${f/$input_dir\/}
	time KMetagen.py -i $f -r RefSeq -o $out
done


## nt
for f in $input_dir/*nt.res; do 
	out=$out_fp/${f/$input_dir\/}
	time KMetagen.py -i $f -r nt -o $out
done


echo "done!"



