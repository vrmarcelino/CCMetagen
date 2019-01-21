#!/bin/bash
#PBS -P FGEN
#PBS -l select=1:ncpus=5:mem=2000GB
#PBS -l walltime=4:00:00

cd $PBS_O_WORKDIR

PATH=$PATH:/home/vros8020/FGEN_project/programs/kma/

th=4


in_dir=03_Quality_Control_more_ds/
out_dir=06_TaxAssign/KMA_more_ds

mkdir -p $out_dir

# databases
db_its=../large_databases/KMA/Unite_ITS/ITS_unite
db_refSeq_f_part=../large_databases/KMA/RefSeq_fungi_partial/refseq_f_partial
db_refSeq_bf=../large_databases/KMA/RefSeq_BacFun/refseq_bf
nt_db=../large_databases/KMA/NCBI_nt/ncbi_nt


#for f in $in_dir/*.fast*; do
#	o_part1=$out_dir/${f/$in_dir\//''}
#	o=${o_part1/.good.fast[a|q]/}
#	echo $o
#	time kma -i $f -o $o.UNITE -t_db $db_its -t $th -1t1 -mem_mode -and
#	time kma -i $f -o $o.refSeq_f_part -t_db $db_refSeq_f_part -t $th -1t1 -mem_mode -and -ca
#	time kma -i $f -o $o.refSeq_bf -t_db $db_refSeq_bf -t $th -1t1 -mem_mode -and -ca
#	time kma -i $f -o $o.nt -t_db $nt_db -t $th -1t1 -mem_mode -and -ca
#done

# repeat the one that didn't work
# use 2TB instead of #1 like last time.

time kma -i 03_Quality_Control_more_ds/BMI_bmi_reads.good.fasta -o 06_TaxAssign/KMA_more_ds/BMI_bmi_reads.good.nt -t_db $nt_db -t $th -1t1 -mem_mode -and



