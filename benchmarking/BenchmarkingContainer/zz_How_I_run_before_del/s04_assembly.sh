#!/bin/bash
#PBS -P FGEN
#PBS -l select=1:ncpus=20:mem=100GB
#PBS -l walltime=30:00:00

cd $PBS_O_WORKDIR

module load python/3.6.5
module load trinity/2.5.1
module load bowtie2/2.3.3.1
module load java/jdk1.7.0_80
module unload perl
module load perl/5.24.0
module load samtools/1.8

PATH=$PATH:/home/vros8020/FGEN_project/programs/SPAdes-3.11.1/
PATH=$PATH:/home/vros8020/FGEN_project/programs/SPAdes-3.11.1/bin/


### computer simulated metatranscriptome - Trinity
#mtt_1=03_Quality_Control/sim_metatrans_good_R1.fasta
#mtt_2=03_Quality_Control/sim_metatrans_good_R2.fasta

#time Trinity --seqType fa --left $mtt_1 --right $mtt_2 --output 04_Assembly/sim_metatrans_2_trinity --full_cleanup --bypass_java_version_check --max_memory 100G --CPU 20

# there might be an error during cleanup:
# shell-init: error retrieving current directory: getcwd: cannot access parent directories: No such file or directory
# Don't you worry, the final contigs are saved.

### simulated metagenome - MetaSPADES
#mtg_1=03_Quality_Control/sim_metagen_good_R1.fastq
#mtg_2=03_Quality_Control/sim_metagen_good_R2.fastq

# -m is for max memory
#time spades.py --meta -1 $mtg_1 -2 $mtg_2 -o 04_Assembly/sim_metagen -t 20 -m 80


### in vitro simulated metatranscriptome - Trinty  -subsampled
mock_3_mtt_1=03_Quality_Control/3_mtt_good_1.fastq
mock_3_mtt_2=03_Quality_Control/3_mtt_good_2.fastq

time Trinity --seqType fq --left $mock_3_mtt_1 --right $mock_3_mtt_2 --output 04_Assembly/3_mtt_trinity --full_cleanup --bypass_java_version_check --max_memory 100G --CPU 20


### in vitro simulated metatranscriptome - complete dataset (not subsampled) -- note that I changed the names here, so the time will be the contrary (3_mtt was the original name)
mock_8_mtt_ss_1=03_Quality_Control/8_mtt_ss_good_1.fastq
mock_8_mtt_ss_2=03_Quality_Control/8_mtt_ss_good_2.fastq

time Trinity --seqType fq --left $mock_8_mtt_ss_1 --right $mock_8_mtt_ss_2 --output 04_Assembly/8_mtt_ss_trinity --full_cleanup --bypass_java_version_check --max_memory 100G --CPU 20



