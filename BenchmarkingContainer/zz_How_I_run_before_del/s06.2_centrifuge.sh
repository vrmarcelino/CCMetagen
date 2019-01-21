#!/bin/bash
#PBS -P FGEN
#PBS -l select=1:ncpus=12:mem=300GB
#PBS -l walltime=2:00:00

cd $PBS_O_WORKDIR

module load centrifuge blast blast+

th=12

# out files
out_fp=06_TaxAssign/centrifuge
mkdir $out_fp


##### Input files #####

## Reads:

# metatranscriptome - in silico
mtt1_R1=03_Quality_Control/1_mtt_good_R1.fasta
mtt1_R2=03_Quality_Control/1_mtt_good_R2.fasta

# metagenome - in silico
mtg2_R1=03_Quality_Control/2_mtg_good_R1.fastq
mtg2_R2=03_Quality_Control/2_mtg_good_R2.fastq

# metatranscriptome - in vitro - subsampled
mtt3_R1=03_Quality_Control/3_mtt_good_1.fastq
mtt3_R2=03_Quality_Control/3_mtt_good_2.fastq

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
mtt8_R1=03_Quality_Control/8_mtt_good_1.fastq
mtt8_R2=03_Quality_Control/8_mtt_good_2.fastq

mtt9_ctg=04_Assembly/9_mtt_contigs.fasta


##### Analyses sets #####


# GenBank - full ncbi
db_nt=db/centrifuge/ncbi_nt_official_cent/nt
echo "GenBank full"
echo "1 metatrans - in silico"
#time centrifuge -x $db_nt -f -1 $mtt1_R1 -2 $mtt1_R2 -S $out_fp/mtt_1_nt --report-file $out_fp/mtt_1_nt_report.tsv -p $th
echo "2 metagenome - in silico"
#time centrifuge -x $db_nt -1 $mtg2_R1 -2 $mtg2_R2 -S $out_fp/mtg_2_nt --report-file $out_fp/mtg_2_nt_report.tsv -p $th
echo "3 metatranscriptome - in vitro"
#time centrifuge -x $db_nt -1 $mtt3_R1 -2 $mtt3_R2 -S $out_fp/mtt_3_nt --report-file $out_fp/mtt_3_nt_report.tsv -p $th
echo "4 nanopore - in vitro"
#time centrifuge -x $db_nt -q $nanop4 -S $out_fp/nanop_4_nt --report-file $out_fp/nanop_4_nt_report.tsv -p $th
echo "5 metatrans - in silico - contigs"
#time centrifuge -x $db_nt -f $mtt5_ctg -S $out_fp/mtt_5_ctg_nt --report-file $out_fp/mtt_5_ctg_nt_report.tsv -p $th
echo "6 metagenome- in silico - contigs"
#time centrifuge -x $db_nt -f $mtg6_ctg -S $out_fp/mtg_6_ctg_nt --report-file $out_fp/mtg_6_ctg_nt_report.tsv -p $th
echo "7 metatranscriptome - in vitro - contigs"
time centrifuge -x $db_nt -f $mtt7_ctg -S $out_fp/mtt_7_ctg_nt --report-file $out_fp/mtt_7_ctg_nt_report.tsv -p $th
echo "8 metatranscriptome - in vitro - original"
#time centrifuge -x $db_nt -1 $mtt8_R1 -2 $mtt8_R2 -S $out_fp/mtt_8_nt --report-file $out_fp/mtt_8_nt_report.tsv -p $th
echo "9 metatranscriptome - in vitro - contigs - original"
#time centrifuge -x $db_nt -f $mtt9_ctg -S $out_fp/mtt_9_ctg_nt --report-file $out_fp/mtt_9_ctg_nt_report.tsv -p $th
echo ""


# RefSeq bacteria and fungi
db_refseq_bf=db/centrifuge/RefSeq/bacfun_refseq
echo "RefSeq bacteria and fungi"
echo "1 metatrans - in silico"
#time centrifuge -x $db_refseq_bf -f -1 $mtt1_R1 -2 $mtt1_R2 -S $out_fp/mtt_1_refseq_bf --report-file $out_fp/mtt_1_refseq_bf_report.tsv -p $th
echo "2 metagenome - in silico"
#time centrifuge -x $db_refseq_bf -1 $mtg2_R1 -2 $mtg2_R2 -S $out_fp/mtg_2_refseq_bf --report-file $out_fp/mtg_2_refseq_bf_report.tsv -p $th
echo "3 metatranscriptome - in vitro"
#time centrifuge -x $db_refseq_bf -1 $mtt3_R1 -2 $mtt3_R2 -S $out_fp/mtt_3_refseq_bf --report-file $out_fp/mtt_3_refseq_bf_report.tsv -p $th
echo "4 nanopore - in vitro"
#time centrifuge -x $db_refseq_bf -q $nanop4 -S $out_fp/nanop_4_refseq_bf --report-file $out_fp/nanop_4_refseq_bf_report.tsv -p $th
echo "5 metatrans - in silico - contigs"
#time centrifuge -x $db_refseq_bf -f $mtt5_ctg -S $out_fp/mtt_5_ctg_refseq_bf --report-file $out_fp/mtt_5_ctg_refseq_bf_report.tsv -p $th
echo "6 metagenome- in silico - contigs"
#time centrifuge -x $db_refseq_bf -f $mtg6_ctg -S $out_fp/mtg_6_ctg_refseq_bf --report-file $out_fp/mtg_6_ctg_refseq_bf_report.tsv -p $th
echo "7 metatranscriptome - in vitro - contigs"
time centrifuge -x $db_refseq_bf -f $mtt7_ctg -S $out_fp/mtt_7_ctg_refseq_bf --report-file $out_fp/mtt_7_ctg_refseq_bf_report.tsv -p $th
echo "8 metatranscriptome - in vitro - original"
#time centrifuge -x $db_refseq_bf -1 $mtt8_R1 -2 $mtt8_R2 -S $out_fp/mtt_8_refseq_bf --report-file $out_fp/mtt_8_refseq_bf_report.tsv -p $th
echo "9 metatranscriptome - in vitro - contigs - original"
#time centrifuge -x $db_refseq_bf -f $mtt9_ctg -S $out_fp/mtt_9_ctg_refseq_bf --report-file $out_fp/mtt_9_ctg_refseq_bf_report.tsv -p $th
echo ""



# RefSeq fungi - incomplete db (50%)
db_refseq_f_part=db/centrifuge/RefSeq/refseq_fun_partial_db
echo "RefSeq fungi - incomplete db"
echo "1 metatrans - in silico"
#time centrifuge -x $db_refseq_f_part -f -1 $mtt1_R1 -2 $mtt1_R2 -S $out_fp/mtt_1_refseq_f_part --report-file $out_fp/mtt_1_refseq_f_part_report.tsv -p $th
echo "2 metagenome - in silico"
#time centrifuge -x $db_refseq_f_part -1 $mtg2_R1 -2 $mtg2_R2 -S $out_fp/mtg_2_refseq_f_part --report-file $out_fp/mtg_2_refseq_f_part_report.tsv -p $th
echo "3 metatranscriptome - in vitro"
#time centrifuge -x $db_refseq_f_part -1 $mtt3_R1 -2 $mtt3_R2 -S $out_fp/mtt_3_refseq_f_part --report-file $out_fp/mtt_3_refseq_f_part_report.tsv -p $th
echo "4 nanopore - in vitro"
#time centrifuge -x $db_refseq_f_part -q $nanop4 -S $out_fp/nanop_4_refseq_f_part --report-file $out_fp/nanop_4_refseq_f_part_report.tsv -p $th
echo "5 metatrans - in silico - contigs"
#time centrifuge -x $db_refseq_f_part -f $mtt5_ctg -S $out_fp/mtt_5_ctg_refseq_f_part --report-file $out_fp/mtt_5_ctg_refseq_f_part_report.tsv -p $th
echo "6 metagenome- in silico - contigs"
#time centrifuge -x $db_refseq_f_part -f $mtg6_ctg -S $out_fp/mtg_6_ctg_refseq_f_part --report-file $out_fp/mtg_6_ctg_refseq_f_part_report.tsv -p $th
echo "7 metatranscriptome - in vitro - contigs"
time centrifuge -x $db_refseq_f_part -f $mtt7_ctg -S $out_fp/mtt_7_ctg_refseq_f_part --report-file $out_fp/mtt_7_ctg_refseq_f_part_report.tsv -p $th
echo "8 metatranscriptome - in vitro - original"
#time centrifuge -x $db_refseq_f_part -1 $mtt8_R1 -2 $mtt8_R2 -S $out_fp/mtt_8_refseq_f_part --report-file $out_fp/mtt_8_refseq_f_part_report.tsv -p $th
echo "9 metatranscriptome - in vitro - contigs - original"
#time centrifuge -x $db_refseq_f_part -f $mtt9_ctg -S $out_fp/mtt_9_ctg_refseq_f_part --report-file $out_fp/mtt_9_ctg_refseq_f_part_report.tsv -p $th
echo ""


