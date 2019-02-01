#!/bin/bash
#PBS -P FGEN
#PBS -l select=1:ncpus=10:mem=60GB
#PBS -l walltime=10:00:00

# 27 - Jun - 2018

cd $PBS_O_WORKDIR

# QC of Illumina samples
module load prinseq

#### Computer Simulated metatranscriptome ####
mtt_R1=01_Simulated_metatranscriptome/sim_metatrans_R1.fas
mtt_R2=01_Simulated_metatranscriptome/sim_metatrans_R2.fas

# filter sequences with more than 5 Ns:
prinseq-lite -fasta $mtt_R1 -fasta2 $mtt_R2 -out_good 03_Quality_Control/sim_metatrans_good -out_bad 03_Quality_Control/sim_metatrans_bad -ns_max_n 5

#### Computer Simulated metagenome ####
mtg_R1=02_Simulated_metagenome/sim_metagen_R1.fastq
mtg_R2=02_Simulated_metagenome/sim_metagen_R2.fastq

# filter sequences with more than 5 Ns and average quality <= 25 (keep sequences unless >/= 27 wrong bases are inserted)
prinseq-lite -fastq $mtg_R1 -fastq2 $mtg_R2 -out_good 03_Quality_Control/sim_metagen_good -out_bad 03_Quality_Control/sim_metagen_bad -ns_max_n 5 -min_qual_mean 25 -out_format 3

#### In vitro simulated metatrasncriptomes (mock commm) ####
# filter sequences with more than 5 Ns and average quality <= 25 
mock_mtt_R1=00_Datasets_raw/03_InVitro_metatranscriptome/Fun_Com_01_R1.fastq
mock_mtt_R2=00_Datasets_raw/03_InVitro_metatranscriptome/Fun_Com_01_R2.fastq
prinseq-lite -fastq $mock_mtt_R1 -fastq2 $mock_mtt_R2 -out_good 03_Quality_Control/8_mtt_good -out_bad 03_Quality_Control/8_mtt_bad -ns_max_n 5 -min_qual_mean 25 -out_format 3



#### For other (bacetrial) datasets:
in_dir=00_Datasets_raw_more_ds
output_dir=03_Quality_Control_more_ds
mkdir -p $output_dir

for f in $in_dir/*.fasta; do
	o_part1=$output_dir/${f/$in_dir\//''}
	o=${o_part1/.fasta/}
	echo $o
	prinseq-lite -fasta $f -out_good $o.good -out_bad $o.bad -ns_max_n 5
done

