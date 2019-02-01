#!/bin/bash
#PBS -P FGEN
#PBS -l select=1:ncpus=10:mem=250GB
#PBS -l walltime=72:00:00

cd $PBS_O_WORKDIR


module load kraken2
module load jellyfish/1.1.10
module load blast
th=10

out_fp=06_TaxAssign/Kraken2
mkdir -p $out_fp


##### Input files #####

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

# RefSeq_partial database
refseq_f_partial=../large_databases/kraken/RefSeq_f_part/
echo "RefSeq fungi partial"
echo "1 metatrans - in silico"
#time kraken2 --output $out_fp/1_mtt_refSeq_f_part.tsv --report $out_fp/1_mtt_refSeq_f_part_report.tsv --db $refseq_f_partial --threads $th --paired $mtt1_R1 $mtt1_R2
echo "2 metagenome - in silico"
#time kraken2 --output $out_fp/2_mtg_refSeq_f_part.tsv --report $out_fp/2_mtg_refSeq_f_part_report.tsv --db $refseq_f_partial --threads $th --paired $mtg2_R1 $mtg2_R2
echo "3 metatranscriptome - in vitro"
#time kraken2 --output $out_fp/3_mtt_refSeq_f_part.tsv --report $out_fp/3_mtt_refSeq_f_part_report.tsv --db $refseq_f_partial --threads $th --paired $mtt3_R1 $mtt3_R2
echo "4 nanopore - in vitro"
#time kraken2 --output $out_fp/4_nanop_refSeq_f_part.tsv --report $out_fp/4_nanop_refSeq_f_part_report.tsv --db $refseq_f_partial --threads $th $nanop4
echo "5 metatrans - in silico - contigs"
#time kraken2 --output $out_fp/5_mtt_ctg_refSeq_f_part.tsv --report $out_fp/5_mtt_ctg_refSeq_f_part_report.tsv --db $refseq_f_partial --threads $th $mtt5_ctg
echo "6 metagenome- in silico - contigs"
#time kraken2 --output $out_fp/6_mtg_ctg_refSeq_f_part.tsv --report $out_fp/6_mtg_ctg_refSeq_f_part_report.tsv --db $refseq_f_partial --threads $th $mtg6_ctg
echo "7 metatranscriptome - in vitro - contigs"
#time kraken2 --output $out_fp/7_mtt_ctg_refSeq_f_part.tsv --report $out_fp/7_mtt_ctg_refSeq_f_part_report.tsv --db $refseq_f_partial --threads $th $mtt7_ctg
echo "8 metatranscriptome - in vitro - original"
#time kraken2 --output $out_fp/8_mtt_refSeq_f_part.tsv --report $out_fp/8_mtt_refSeq_f_part_report.tsv --db $refseq_f_partial --threads $th --paired $mtt8_R1 $mtt8_R2
echo "9 metatranscriptome - in vitro - contigs - original"
#time kraken2 --output $out_fp/9_mtt_ctg_refSeq_f_part.tsv --report $out_fp/9_mtt_ctg_refSeq_f_part_report.tsv --db $refseq_f_partial --threads $th $mtt9_ctg
echo "Done!"


RefSeq_bf=../large_databases/kraken/RefSeq_bf/
echo "RefSeq bf"
echo "1 metatrans - in silico"
#time kraken2 --output $out_fp/1_mtt_refSeq_bf.tsv --report $out_fp/1_mtt_refSeq_bf_report.tsv --db $RefSeq_bf --threads $th --paired $mtt1_R1 $mtt1_R2
echo "2 metagenome - in silico"
#time kraken2 --output $out_fp/2_mtg_refSeq_bf.tsv --report $out_fp/2_mtg_refSeq_bf_report.tsv --db $RefSeq_bf --threads $th --paired $mtg2_R1 $mtg2_R2
echo "3 metatranscriptome - in vitro"
#time kraken2 --output $out_fp/3_mtt_refSeq_bf.tsv --report $out_fp/3_mtt_refSeq_bf_report.tsv --db $RefSeq_bf --threads $th --paired $mtt3_R1 $mtt3_R2
echo "4 nanopore - in vitro"
#time kraken2 --output $out_fp/4_nanop_refSeq_bf.tsv --report $out_fp/4_nanop_refSeq_bf_report.tsv --db $RefSeq_bf --threads $th $nanop4
echo "5 metatrans - in silico - contigs"
#time kraken2 --output $out_fp/5_mtt_ctg_refSeq_bf.tsv --report $out_fp/5_mtt_ctg_refSeq_bf_report.tsv --db $RefSeq_bf --threads $th $mtt5_ctg
echo "6 metagenome- in silico - contigs"
#time kraken2 --output $out_fp/6_mtg_ctg_refSeq_bf.tsv --report $out_fp/6_mtg_ctg_refSeq_bf_report.tsv --db $RefSeq_bf --threads $th $mtg6_ctg
echo "7 metatranscriptome - in vitro - contigs"
#time kraken2 --output $out_fp/7_mtt_ctg_refSeq_bf.tsv --report $out_fp/7_mtt_ctg_refSeq_bf_report.tsv --db $RefSeq_bf --threads $th $mtt7_ctg
echo "8 metatranscriptome - in vitro - original"
#time kraken2 --output $out_fp/8_mtt_refSeq_bf.tsv --report $out_fp/8_mtt_refSeq_bf_report.tsv --db $RefSeq_bf --threads $th --paired $mtt8_R1 $mtt8_R2
echo "9 metatranscriptome - in vitro - contigs - original"
#time kraken2 --output $out_fp/9_mtt_ctg_refSeq_bf.tsv --report $out_fp/9_mtt_ctg_refSeq_bf_report.tsv --db $RefSeq_bf --threads $th $mtt9_ctg
echo "Done!"



nt=../large_databases/kraken/nt/
echo "nt"
echo "1 metatrans - in silico"
time kraken2 --output $out_fp/1_mtt_nt.tsv --report $out_fp/1_mtt_nt_report.tsv --db $nt --threads $th --paired $mtt1_R1 $mtt1_R2
echo "2 metagenome - in silico"
time kraken2 --output $out_fp/2_mtg_nt.tsv --report $out_fp/2_mtg_nt_report.tsv --db $nt --threads $th --paired $mtg2_R1 $mtg2_R2
echo "3 metatranscriptome - in vitro"
time kraken2 --output $out_fp/3_mtt_nt.tsv --report $out_fp/3_mtt_nt_report.tsv --db $nt --threads $th --paired $mtt3_R1 $mtt3_R2
echo "4 nanopore - in vitro"
time kraken2 --output $out_fp/4_nanop_nt.tsv --report $out_fp/4_nanop_nt_report.tsv --db $nt --threads $th $nanop4
echo "5 metatrans - in silico - contigs"
time kraken2 --output $out_fp/5_mtt_ctg_nt.tsv --report $out_fp/5_mtt_ctg_nt_report.tsv --db $nt --threads $th $mtt5_ctg
echo "6 metagenome- in silico - contigs"
time kraken2 --output $out_fp/6_mtg_ctg_nt.tsv --report $out_fp/6_mtg_ctg_nt_report.tsv --db $nt --threads $th $mtg6_ctg
echo "7 metatranscriptome - in vitro - contigs"
time kraken2 --output $out_fp/7_mtt_ctg_nt.tsv --report $out_fp/7_mtt_ctg_nt_report.tsv --db $nt --threads $th $mtt7_ctg
echo "8 metatranscriptome - in vitro - original"
time kraken2 --output $out_fp/8_mtt_nt.tsv --report $out_fp/8_mtt_nt_report.tsv --db $nt --threads $th --paired $mtt8_R1 $mtt8_R2
echo "9 metatranscriptome - in vitro - contigs - original"
time kraken2 --output $out_fp/9_mtt_ctg_nt.tsv --report $out_fp/9_mtt_ctg_nt_report.tsv --db $nt --threads $th $mtt9_ctg
echo "Done!"







