#!/bin/bash
#PBS -P FGEN
#PBS -l select=1:ncpus=14:mem=400GB
#PBS -l walltime=100:00:00

cd $PBS_O_WORKDIR

module load blast

th=14

out_fp=06_TaxAssign/BLAST
mkdir $out_fp

##### Input files #####


## Reads:
# metatranscriptome - in silico
mtt1_R12=03_Quality_Control/1_mtt_good_R12int.fasta

# metagenome - in silico
mtg2_R12=03_Quality_Control/2_mtg_good_R12int.fasta

# metatranscriptome - in vitro - subsampled
mtt3_R12=03_Quality_Control/3_mtt_good_R12int.fasta

# metagenome in vitro
nanop4=03_Quality_Control/4_nanopore.fasta

## Contigs:
# metatranscriptome - in silico
mtt5_ctg=04_Assembly/5_mtt_contigs.fasta

# metagenome - in silico
mtg6_ctg=04_Assembly/6_mtg_contigs.fasta

# metatranscriptome in vitro:
mtt7_ctg=04_Assembly/7_mtt_contigs.fasta

## Original metatranscriptome:
mtt8_R12=03_Quality_Control/8_mtt_good_R12int.fasta

mtt9_ctg=04_Assembly/9_mtt_contigs.fasta



##### Analyses sets #####

# ITS 
db_ITS=../large_databases/BLAST/ITS_db
echo "ITS database"

echo "2 metagenome - in silico"
time blastn -query $mtg2_R12 -out $out_fp/2_mtg_ITS.txt -db $db_ITS -num_threads $th -outfmt 6 -evalue 1e-5

echo "3 metatranscriptome - in vitro"
time blastn -query $mtt3_R12 -out $out_fp/3_mtt_ITS.txt -db $db_ITS -num_threads $th -outfmt 6 -evalue 1e-5

echo "4 nanopore - in vitro"
time blastn -query $nanop4 -out $out_fp/4_nanop_ITS.txt -db $db_ITS -num_threads $th -outfmt 6 -evalue 1e-5

echo "6 metagenome- in silico - contigs"
time blastn -query $mtg6_ctg -out $out_fp/6_mtg_ctg_ITS.txt -db $db_ITS -num_threads $th -outfmt 6 -evalue 1e-5

echo "7 metatranscriptome - in vitro - contigs"
time blastn -query $mtt7_ctg -out $out_fp/7_mtt_ctg_ITS.txt -db $db_ITS -num_threads $th -outfmt 6 -evalue 1e-5

echo "8 metatranscriptome - in vitro - original"
time blastn -query $mtt8_R12 -out $out_fp/8_mtt_ITS.txt -db $db_ITS -num_threads $th -outfmt 6 -evalue 1e-5

echo "9 metatranscriptome - in vitro - contigs - original"
time blastn -query $mtt9_ctg -out $out_fp/9_mtt_ctg_ITS.txt -db $db_ITS -num_threads $th -outfmt 6 -evalue 1e-5

echo ""





# RefSeq fungi partial
refseq_f_partial_db=../large_databases/BLAST/refseq_f_partial_db
echo "RefSeq Fungi Partial"

echo "1 metatrans - in silico"
time blastn -query $mtt1_R12 -out $out_fp/1_mtt_refseq_f_partial.txt -db $refseq_f_partial_db -num_threads $th -outfmt 6 -evalue 1e-5

echo "2 metagenome - in silico"
time blastn -query $mtg2_R12 -out $out_fp/2_mtg_refseq_f_partial.txt -db $refseq_f_partial_db -num_threads $th -outfmt 6 -evalue 1e-5

echo "3 metatranscriptome - in vitro"
time blastn -query $mtt3_R12 -out $out_fp/3_mtt_refseq_f_partial.txt -db $refseq_f_partial_db -num_threads $th -outfmt 6 -evalue 1e-5

echo "4 nanopore - in vitro"
time blastn -query $nanop4 -out $out_fp/4_nanop_refseq_f_partial.txt -db $refseq_f_partial_db -num_threads $th -outfmt 6 -evalue 1e-5

echo "5 metatrans - in silico - contigs"
time blastn -query $mtt5_ctg -out $out_fp/5_mtt_ctg_refseq_f_partial.txt -db $refseq_f_partial_db -num_threads $th -outfmt 6 -evalue 1e-5

echo "6 metagenome- in silico - contigs"
time blastn -query $mtg6_ctg -out $out_fp/6_mtg_ctg_refseq_f_partial.txt -db $refseq_f_partial_db -num_threads $th -outfmt 6 -evalue 1e-5

echo "7 metatranscriptome - in vitro - contigs"
time blastn -query $mtt7_ctg -out $out_fp/7_mtt_ctg_refseq_f_partial.txt -db $refseq_f_partial_db -num_threads $th -outfmt 6 -evalue 1e-5

echo "8 metatranscriptome - in vitro - original"
time blastn -query $mtt8_R12 -out $out_fp/8_mtt_refseq_f_partial.txt -db $refseq_f_partial_db -num_threads $th -outfmt 6 -evalue 1e-5

echo "9 metatranscriptome - in vitro - contigs - original"
time blastn -query $mtt9_ctg -out $out_fp/9_mtt_ctg_refseq_f_partial.txt -db $refseq_f_partial_db -num_threads $th -outfmt 6 -evalue 1e-5

echo ""



# UniRef fungi and bacteria
refseq_bf_db=../large_databases/BLAST/refseq_bf_db
echo "UniRef Fungi and Bacteria"

echo "1 metatrans - in silico"
time blastn -query $mtt1_R12 -out $out_fp/1_mtt_refseq_bf.txt -db $refseq_bf_db -num_threads $th -outfmt 6 -evalue 1e-5

echo "2 metagenome - in silico"
time blastn -query $mtg2_R12 -out $out_fp/2_mtg_refseq_bf.txt -db $refseq_bf_db -num_threads $th -outfmt 6 -evalue 1e-5

echo "3 metatranscriptome - in vitro"
time blastn -query $mtt3_R12 -out $out_fp/3_mtt_refseq_bf.txt -db $refseq_bf_db -num_threads $th -outfmt 6 -evalue 1e-5

echo "4 nanopore - in vitro"
time blastn -query $nanop4 -out $out_fp/4_nanop_refseq_bf.txt -db $refseq_bf_db -num_threads $th -outfmt 6 -evalue 1e-5

echo "5 metatrans - in silico - contigs"
time blastn -query $mtt5_ctg -out $out_fp/5_mtt_ctg_refseq_bf.txt -db $refseq_bf_db -num_threads $th -outfmt 6 -evalue 1e-5

echo "6 metagenome- in silico - contigs"
time blastn -query $mtg6_ctg -out $out_fp/6_mtg_ctg_refseq_bf.txt -db $refseq_bf_db -num_threads $th -outfmt 6 -evalue 1e-5

echo "7 metatranscriptome - in vitro - contigs"
time blastn -query $mtt7_ctg -out $out_fp/7_mtt_ctg_refseq_bf.txt -db $refseq_bf_db -num_threads $th -outfmt 6 -evalue 1e-5

echo "8 metatranscriptome - in vitro - original"
time blastn -query $mtt8_R12 -out $out_fp/8_mtt_refseq_bf.txt -db $refseq_bf_db -num_threads $th -outfmt 6 -evalue 1e-5

echo "9 metatranscriptome - in vitro - contigs - original"
time blastn -query $mtt9_ctg -out $out_fp/9_mtt_ctg_refseq_bf.txt -db $refseq_bf_db -num_threads $th -outfmt 6 -evalue 1e-5

echo ""





# NCBI nt
nt_db=../large_databases/BLAST/nt_db
echo "nt"

echo "1 metatrans - in silico"
time blastn -query $mtt1_R12 -out $out_fp/1_mtt_nt.txt -db $nt_db -num_threads $th -outfmt 6 -evalue 1e-5

echo "2 metagenome - in silico"
time blastn -query $mtg2_R12 -out $out_fp/2_mtg_nt.txt -db $nt_db -num_threads $th -outfmt 6 -evalue 1e-5

echo "3 metatranscriptome - in vitro"
time blastn -query $mtt3_R12 -out $out_fp/3_mtt_nt.txt -db $nt_db -num_threads $th -outfmt 6 -evalue 1e-5

echo "4 nanopore - in vitro"
time blastn -query $nanop4 -out $out_fp/4_nanop_nt.txt -db $nt_db -num_threads $th -outfmt 6 -evalue 1e-5

echo "5 metatrans - in silico - contigs"
time blastn -query $mtt5_ctg -out $out_fp/5_mtt_ctg_nt.txt -db $nt_db -num_threads $th -outfmt 6 -evalue 1e-5

echo "6 metagenome- in silico - contigs"
time blastn -query $mtg6_ctg -out $out_fp/6_mtg_ctg_nt.txt -db $nt_db -num_threads $th -outfmt 6 -evalue 1e-5

echo "7 metatranscriptome - in vitro - contigs"
time blastn -query $mtt7_ctg -out $out_fp/7_mtt_ctg_nt.txt -db $nt_db -num_threads $th -outfmt 6 -evalue 1e-5

echo "8 metatranscriptome - in vitro - original"
time blastn -query $mtt8_R12 -out $out_fp/8_mtt_nt.txt -db $nt_db -num_threads $th -outfmt 6 -evalue 1e-5

echo "9 metatranscriptome - in vitro - contigs - original"
time blastn -query $mtt9_ctg -out $out_fp/9_mtt_ctg_nt.txt -db $nt_db -num_threads $th -outfmt 6 -evalue 1e-5

echo ""



