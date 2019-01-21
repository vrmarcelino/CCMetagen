#!/bin/bash
#PBS -P FGEN
#PBS -l select=1:ncpus=16:mem=1000GB
#PBS -l walltime=30:00:00

cd $PBS_O_WORKDIR

PATH=$PATH:/home/vros8020/FGEN_project/programs/krakenuniq/
module load perl 
module load blast

th=16

out_fp=06_TaxAssign/KrakenUniq
mkdir -p $out_fp


##### Input files #####

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

# RefSeq_partial database
refseq_f_partial=../large_databases/krakenHLL/Refseq_f_partial/

echo "1 metatrans - in silico"
#time krakenuniq --report-file $out_fp/1_mtt_refseq_f_partial_preload.tsv --db $refseq_f_partial --threads $th --paired $mtt1_R1 $mtt1_R2
echo "2 metagenome - in silico"
#time krakenuniq --report-file $out_fp/2_mtg_refseq_f_partial.tsv --db $refseq_f_partial --threads $th --paired $mtg2_R1 $mtg2_R2
echo "3 metatranscriptome - in vitro"
#time krakenuniq --report-file $out_fp/3_mtt_refseq_f_partial.tsv --db $refseq_f_partial --threads $th --paired $mtt3_R1 $mtt3_R2
echo "4 nanopore - in vitro"
#time krakenuniq --report-file $out_fp/4_nanop_refseq_f_partial.tsv --db $refseq_f_partial --threads $th $nanop4
echo "5 metatrans - in silico - contigs"
#time krakenuniq --report-file $out_fp/5_mtt_ctg_refseq_f_partial.tsv --db $refseq_f_partial --threads $th $mtt5_ctg
echo "6 metagenome- in silico - contigs"
#time krakenuniq --report-file $out_fp/6_mtg_ctg_refseq_f_partial.tsv --db $refseq_f_partial --threads $th $mtg6_ctg
echo "7 metatranscriptome - in vitro - contigs"
#time krakenuniq --report-file $out_fp/7_mtt_ctg_refseq_f_partial.tsv --db $refseq_f_partial --threads $th $mtt7_ctg
echo "8 metatranscriptome - in vitro - original"
#time krakenuniq --report-file $out_fp/8_mtt_refseq_f_partial.tsv --db $refseq_f_partial --threads $th --paired $mtt8_R1 $mtt8_R2
echo "9 metatranscriptome - in vitro - contigs - original"
#time krakenuniq --report-file $out_fp/9_mtt_ctg_refseq_f_partial.tsv --db $refseq_f_partial --threads $th $mtt9_ctg




# ResSeq Bacteria and Fungi
refseq_bf=../large_databases/krakenHLL/refseq_bf/
echo "1 metatrans - in silico"
#time krakenuniq --report-file $out_fp/1_mtt_refseq_bf.tsv --db $refseq_bf --threads $th --paired $mtt1_R1 $mtt1_R2
echo "2 metagenome - in silico"
#time krakenuniq --report-file $out_fp/2_mtg_refseq_bf.tsv --db $refseq_bf --threads $th --paired $mtg2_R1 $mtg2_R2
echo "3 metatranscriptome - in vitro"
#time krakenuniq --report-file $out_fp/3_mtt_refseq_bf.tsv --db $refseq_bf --threads $th --paired $mtt3_R1 $mtt3_R2
echo "4 nanopore - in vitro"
#time krakenuniq --report-file $out_fp/4_nanop_refseq_bf.tsv --db $refseq_bf --threads $th $nanop4
echo "5 metatrans - in silico - contigs"
#time krakenuniq --report-file $out_fp/5_mtt_ctg_refseq_bf.tsv --db $refseq_bf --threads $th $mtt5_ctg
echo "6 metagenome- in silico - contigs"
#time krakenuniq --report-file $out_fp/6_mtg_ctg_refseq_bf.tsv --db $refseq_bf --threads $th $mtg6_ctg
echo "7 metatranscriptome - in vitro - contigs"
#time krakenuniq --report-file $out_fp/7_mtt_ctg_refseq_bf.tsv --db $refseq_bf --threads $th $mtt7_ctg
echo "8 metatranscriptome - in vitro - original"
#time krakenuniq --report-file $out_fp/8_mtt_refseq_bf.tsv --db $refseq_bf --threads $th --paired $mtt8_R1 $mtt8_R2
echo "9 metatranscriptome - in vitro - contigs - original"
time krakenuniq --report-file $out_fp/9_mtt_ctg_refseq_bf.tsv --db $refseq_bf --threads $th $mtt9_ctg

echo "Done!"



# nt
nt=../large_databases/KrakenUniq/microbial_nt/
echo "1 metatrans - in silico"
#time krakenuniq --report-file $out_fp/1_mtt_nt.tsv --db $nt --threads $th --paired $mtt1_R1 $mtt1_R2
echo "2 metagenome - in silico"
#time krakenuniq --report-file $out_fp/2_mtg_nt.tsv --db $nt --threads $th --paired $mtg2_R1 $mtg2_R2
echo "3 metatranscriptome - in vitro"
#time krakenuniq --report-file $out_fp/3_mtt_nt.tsv --db $nt --threads $th --paired $mtt3_R1 $mtt3_R2
echo "4 nanopore - in vitro"
#time krakenuniq --report-file $out_fp/4_nanop_nt.tsv --db $nt --threads $th $nanop4
echo "5 metatrans - in silico - contigs"
#time krakenuniq --report-file $out_fp/5_mtt_ctg_nt.tsv --db $nt --threads $th $mtt5_ctg
echo "6 metagenome- in silico - contigs"
#time krakenuniq --report-file $out_fp/6_mtg_ctg_nt.tsv --db $nt --threads $th $mtg6_ctg
echo "7 metatranscriptome - in vitro - contigs"
#time krakenuniq --report-file $out_fp/7_mtt_ctg_nt.tsv --db $nt --threads $th $mtt7_ctg
echo "8 metatranscriptome - in vitro - original"
#time krakenuniq --report-file $out_fp/8_mtt_nt.tsv --db $nt --threads $th --paired $mtt8_R1 $mtt8_R2
echo "9 metatranscriptome - in vitro - contigs - original"
time krakenuniq --report-file $out_fp/9_mtt_ctg_nt.tsv --db $nt --threads $th $mtt9_ctg

echo "Done!"



