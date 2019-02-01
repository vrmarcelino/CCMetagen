#!/bin/bash
#PBS -P FGEN
#PBS -l select=1:ncpus=12:mem=300GB
#PBS -l walltime=20:00:00

cd $PBS_O_WORKDIR


module load kraken2
module load jellyfish/1.1.10
module load blast
th=12


in_dir=03_Quality_Control_more_ds/
out_dir=06_TaxAssign/Kraken2_more_ds

mkdir -p $out_dir

# databases
nt=../large_databases/kraken/nt/



for f in $in_dir/*.fast*; do
	o_part1=$out_dir/${f/$in_dir\//''}
	o=${o_part1/.good.fast[a|q]/}
	echo $o
	time kraken2 --output $o.nt.tsv --report $o.nt_report.tsv --db $nt --threads $th $f
done





