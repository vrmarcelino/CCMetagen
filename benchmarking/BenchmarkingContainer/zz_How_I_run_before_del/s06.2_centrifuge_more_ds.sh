#!/bin/bash
#PBS -P FGEN
#PBS -l select=1:ncpus=12:mem=300GB
#PBS -l walltime=5:00:00

cd $PBS_O_WORKDIR

module load centrifuge blast blast+

th=12


##### Input files #####

in_dir=03_Quality_Control_more_ds/
out_dir=06_TaxAssign/centrifuge_more_ds

mkdir -p $out_dir

# database
db_nt=db/centrifuge/ncbi_nt_official_cent/nt


for f in $in_dir/*.fast*; do
	o_part1=$out_dir/${f/$in_dir\//''}
	o=${o_part1/.good.fast[a|q]/}
	echo $o
	time centrifuge -x $db_nt -f $f -S $o.nt --report-file $o.nt.tsv -p $th
done




