#!/bin/bash
#PBS -P FGEN
#PBS -l select=1:ncpus=5:mem=1000GB
#PBS -l walltime=6:00:00

cd $PBS_O_WORKDIR

PATH=$PATH:/home/vros8020/FGEN_project/programs/kma/

th=4

# out files
out_fp=06_TaxAssign/KMA
mkdir -p $out_fp


##### Input files #####

## Reads:

# metatranscriptome - in silico

mtt1_R1=03_Quality_Control/1_mtt_good_R1.fasta
mtt1_R2=03_Quality_Control/1_mtt_good_R2.fasta

# metagenome - in silico
mtg2_R1=03_Quality_Control/2_mtg_good_R1.fastq
mtg2_R2=03_Quality_Control/2_mtg_good_R2.fastq

# metatranscriptome - in vitro - subsampled
mtt3_R1=03_Quality_Control/3_mtt_good_R1.fastq
mtt3_R2=03_Quality_Control/3_mtt_good_R2.fastq

# metagenome in vitro
nanop4=03_Quality_Control/4_nanopore.fastq

## Contigs:
# metatranscriptome - in silico
mtt5_ctg=04_Assembly/5_mtt_contigs.fasta

# metagenome - in silico
mtg6_ctg=04_Assembly/6_mtg_contigs.fasta

# metatranscriptome in vitro:
mtt7_ctg=04_Assembly/7_mtt_contigs.fasta

## Original metatranscriptome:
mtt8_R1=03_Quality_Control/8_mtt_good_R1.fastq
mtt8_R2=03_Quality_Control/8_mtt_good_R2.fastq

mtt9_ctg=04_Assembly/9_mtt_contigs.fasta


##### Analyses sets #####

# Only use -1t1 for short reads! Not in nanop or contigs
# Except in UNITE datadase - where we are mapping agaist a single region.

# -and = Both mrs and p_value thresholds has to reached to in order to report a template hit.
# -apm f" forces paired end reads to stick together, this makes no difference if reads are single end.
# "-ca" allows for circular alignment, which gives better alignments for circular genomes (especially with nanopore reads). 
#     If the genomes are not circular, it will not make any difference in the alignment (makes no sense for fungi).
# use -mem_mode for all analyses (including UNITE - it is more accurate for some reason, but my sample size was 1)


# ITS:
db_its=../large_databases/KMA/Unite_ITS/ITS_unite
echo "ITS"
#echo "1 metatrans - in silico"
echo "2 metagenome - in silico"
#time kma -ipe $mtg2_R1 $mtg2_R2 -o $out_fp/2_mtg_ITS -t_db $db_its -t $th -1t1 -mem_mode -and -apm f
echo "3 metatranscriptome - in vitro"
#time kma -ipe $mtt3_R1 $mtt3_R2 -o $out_fp/3_mtt_ITS -t_db $db_its -t $th -1t1 -mem_mode -and -apm f
echo "4 nanopore - in vitro"
#time kma -i $nanop4 -o $out_fp/4_nanop_ITS -t_db $db_its -t $th -1t1 -mem_mode -and -apm f -mp 20 -bcNano
#echo "5 metatrans - in silico - contigs"
echo "6 metagenome- in silico - contigs"
#time kma -i $mtg6_ctg -o $out_fp/6_mtg_ctg_ITS -t_db $db_its -t $th -1t1 -mem_mode -and -apm f
echo "7 metatranscriptome - in vitro - contigs"
#time kma -i $mtt7_ctg -o $out_fp/7_mtt_ctg_ITS -t_db $db_its -t $th -1t1 -mem_mode -and -apm f
echo "8 metatranscriptome - in vitro - original"
#time kma -ipe $mtt8_R1 $mtt8_R2 -o $out_fp/8_mtt_ITS -t_db $db_its -t $th -1t1 -mem_mode -and -apm f
echo "9 metatranscriptome - in vitro - contigs - original"
#time kma -i $mtt9_ctg -o $out_fp/9_mtt_ctg_ITS -t_db $db_its -t $th -1t1 -mem_mode -and -apm f

echo "done!"



# RefSeq_partial
db_refSeq_f_part=../large_databases/KMA/RefSeq_fungi_partial/refseq_f_partial
echo "RefSeq fungi partial"
echo "1 metatrans - in silico"
#time kma -ipe $mtt1_R1 $mtt1_R2 -o $out_fp/1_mtt_refSeq_f_part -t_db $db_refSeq_f_part -t $th -1t1 -mem_mode -and -apm f
echo "2 metagenome - in silico"
#time kma -ipe $mtg2_R1 $mtg2_R2 -o $out_fp/2_mtg_refSeq_f_part -t_db $db_refSeq_f_part -t $th -1t1 -mem_mode -and -apm f
echo "3 metatranscriptome - in vitro"
#time kma -ipe $mtt3_R1 $mtt3_R2 -o $out_fp/3_mtt_refSeq_f_part -t_db $db_refSeq_f_part -t $th -1t1 -mem_mode -and -apm f
echo "4 nanopore - in vitro"
#time kma -i $nanop4 -o $out_fp/4_nanop_refSeq_f_part -t_db $db_refSeq_f_part -t $th -mem_mode -and -apm f -mp 20 -bcNano
echo "5 metatrans - in silico - contigs"
#time kma -i $mtt5_ctg -o $out_fp/5_mtt_ctg_refSeq_f_part -t_db $db_refSeq_f_part -t $th -mem_mode -and -apm f
echo "6 metagenome- in silico - contigs"
#time kma -i $mtg6_ctg -o $out_fp/6_mtg_ctg_refSeq_f_part -t_db $db_refSeq_f_part -t $th -mem_mode -and -apm f
echo "7 metatranscriptome - in vitro - contigs"
#time kma -i $mtt7_ctg -o $out_fp/7_mtt_ctg_refSeq_f_part -t_db $db_refSeq_f_part -t $th -mem_mode -and -apm f
echo "8 metatranscriptome - in vitro - original"
#time kma -ipe $mtt8_R1 $mtt8_R2 -o $out_fp/8_mtt_refSeq_f_part -t_db $db_refSeq_f_part -t $th -1t1 -mem_mode -and -apm f
echo "9 metatranscriptome - in vitro - contigs - original"
#time kma -i $mtt9_ctg -o $out_fp/9_mtt_ctg_refSeq_f_part -t_db $db_refSeq_f_part -t $th -mem_mode -and -apm f

echo "done!"



# RefSeq_bacFun
echo "RefSeq bacteria and fungi"
db_refSeq_bf=../large_databases/KMA/RefSeq_BacFun/refseq_bf
echo "RefSeq fungi partial"
echo "1 metatrans - in silico"
#time kma -ipe $mtt1_R1 $mtt1_R2 -o $out_fp/1_mtt_refSeq_bf -t_db $db_refSeq_bf -t $th -1t1 -mem_mode -and -apm f
echo "2 metagenome - in silico"
#time kma -ipe $mtg2_R1 $mtg2_R2 -o $out_fp/2_mtg_refSeq_bf -t_db $db_refSeq_bf -t $th -1t1 -mem_mode -and -apm f
echo "3 metatranscriptome - in vitro"
#time kma -ipe $mtt3_R1 $mtt3_R2 -o $out_fp/3_mtt_refSeq_bf -t_db $db_refSeq_bf -t $th -1t1 -mem_mode -and -apm f
echo "4 nanopore - in vitro"
#time kma -i $nanop4 -o $out_fp/4_nanop_refSeq_bf -t_db $db_refSeq_bf -t $th -mem_mode -and -apm f -mp 20 -bcNano
echo "5 metatrans - in silico - contigs"
#time kma -i $mtt5_ctg -o $out_fp/5_mtt_ctg_refSeq_bf -t_db $db_refSeq_bf -t $th -mem_mode -and -apm f
echo "6 metagenome- in silico - contigs"
#time kma -i $mtg6_ctg -o $out_fp/6_mtg_ctg_refSeq_bf -t_db $db_refSeq_bf -t $th -mem_mode -and -apm f
echo "7 metatranscriptome - in vitro - contigs"
#time kma -i $mtt7_ctg -o $out_fp/7_mtt_ctg_refSeq_bf -t_db $db_refSeq_bf -t $th -mem_mode -and -apm f
echo "8 metatranscriptome - in vitro - original"
#time kma -ipe $mtt8_R1 $mtt8_R2 -o $out_fp/8_mtt_refSeq_bf -t_db $db_refSeq_bf -t $th -1t1 -mem_mode -and -apm f
echo "9 metatranscriptome - in vitro - contigs - original"
#time kma -i $mtt9_ctg -o $out_fp/9_mtt_ctg_refSeq_bf -t_db $db_refSeq_bf -t $th -mem_mode -and -apm f

echo "done!"


# GenBank - full ncbi
#echo "nt"
nt_db=../large_databases/KMA/NCBI_nt/ncbi_nt
echo "1 metatrans - in silico"
time kma -ipe $mtt1_R1 $mtt1_R2 -o $out_fp/1_mtt_nt -t_db $nt_db -t $th -1t1 -mem_mode -and -apm f
echo "2 metagenome - in silico"
time kma -ipe $mtg2_R1 $mtg2_R2 -o $out_fp/2_mtg_nt -t_db $nt_db -t $th -1t1 -mem_mode -and -apm f
echo "3 metatranscriptome - in vitro"
time kma -ipe $mtt3_R1 $mtt3_R2 -o $out_fp/3_mtt_nt -t_db $nt_db -t $th -1t1 -mem_mode -and -apm f
echo "4 nanopore - in vitro"
time kma -i $nanop4 -o $out_fp/4_nanop_nt -t_db $nt_db -t $th -mem_mode -and -apm f -mp 20 -bcNano
echo "5 metatrans - in silico - contigs"
time kma -i $mtt5_ctg -o $out_fp/5_mtt_ctg_nt -t_db $nt_db -t $th -mem_mode -and -apm f
echo "6 metagenome- in silico - contigs"
time kma -i $mtg6_ctg -o $out_fp/6_mtg_ctg_nt -t_db $nt_db -t $th -mem_mode -and -apm f
echo "7 metatranscriptome - in vitro - contigs"
time kma -i $mtt7_ctg -o $out_fp/7_mtt_ctg_nt -t_db $nt_db -t $th -mem_mode -and -apm f
echo "8 metatranscriptome - in vitro - original"
time kma -ipe $mtt8_R1 $mtt8_R2 -o $out_fp/8_mtt_nt -t_db $nt_db -t $th -1t1 -mem_mode -and -apm f
echo "9 metatranscriptome - in vitro - contigs - original"
time kma -i $mtt9_ctg -o $out_fp/9_mtt_ctg_nt -t_db $nt_db -t $th -mem_mode -and -apm f

echo "DONE!!!"


