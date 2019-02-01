#!/bin/bash
#PBS -P FGEN
#PBS -l select=1:ncpus=20:mem=100GB
#PBS -l walltime=48:00:00

cd $PBS_O_WORKDIR

module load diamond

th=20

out_fp=06_TaxAssign/Diamond
mkdir $out_fp


##### Input files #####

## Reads:
# metatranscriptome - in silico
mtt1_R12=03_Quality_Control/1_mtt_good_R12int.fasta

# metagenome - in silico
mtg2_R12=03_Quality_Control/2_mtg_good_R12int.fastq

# metatranscriptome - in vitro - subsampled
mtt3_R12=03_Quality_Control/3_mtt_good_R12int.fastq

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
mtt8_R12=03_Quality_Control/8_mtt_good_R12int.fastq

mtt9_ctg=04_Assembly/9_mtt_contigs.fasta




##### Analyses sets #####

taxmap=../large_databases/Diamond/prot.accession2taxid.gz

nr=../large_databases/Diamond/nr.dmnd

diamond blastx -d $nr -q $mtt9_ctg -o $out_fp/mtt_9_ctg_nr.txt -e 1E-5 -k 3 -p $th -f 6 qseqid qlen sseqid stitle pident length evalue staxids --taxonmap $taxmap --more-sensitive


#
# UniProt/ UniRef90
#db_uniref90=../large_databases/Diamond/uniref90_db.dmnd
echo "UniRef90 database"

echo "1 metatrans - in silico"
#time diamond blastx -d $db_uniref90 -q $mtt1_R12 -o $out_fp/mtt_1_uniref90.txt -e 1E-5 -p $th -f 6 qseqid sseqid stitle staxids pident length evalue --taxonmap $taxmap

echo "2 metagenome - in silico"
#time diamond blastx -d $db_uniref90 -q $mtg2_R12 -o $out_fp/mtg_2_uniref90.txt -e 1E-5 -p $th -f 6 qseqid sseqid stitle staxids pident length evalue --taxonmap $taxmap

echo "3 metatranscriptome - in vitro"
#time diamond blastx -d $db_uniref90 -q $mtt3_R12 -o $out_fp/mtt_3_uniref90.txt -e 1E-5 -p $th -f 6 qseqid sseqid stitle staxids pident length evalue --taxonmap $taxmap

echo "nanopore - in vitro"
#time diamond blastx -d $db_uniref90 -q $nanop4 -o $out_fp/nanop_4_uniref90.txt -e 1E-5 -p $th -f 6 qseqid sseqid stitle staxids pident length evalue --taxonmap $taxmap --more-sensitive

echo "5 metatrans - in silico - contigs"
#time diamond blastx -d $db_uniref90 -q $mtt5_ctg -o $out_fp/mtt_5_ctg_uniref90.txt -e 1E-5 -p $th -f 6 qseqid sseqid stitle staxids pident length evalue --taxonmap $taxmap --more-sensitive

echo "6 metagenome- in silico - contigs"
#time diamond blastx -d $db_uniref90 -q $mtg6_ctg -o $out_fp/mtg_6_ctg_uniref90.txt -e 1E-5 -p $th -f 6 qseqid sseqid stitle staxids pident length evalue --taxonmap $taxmap --more-sensitive

echo "7 metatranscriptome - in vitro - contigs"
#time diamond blastx -d $db_uniref90 -q $mtt7_ctg -o $out_fp/mtt_7_ctg_uniref90.txt -e 1E-5 -p $th -f 6 qseqid sseqid stitle staxids pident length evalue --taxonmap $taxmap --more-sensitive

echo "8 metatranscriptome - in vitro - original"
#time diamond blastx -d $db_uniref90 -q $mtt8_R12 -o $out_fp/mtt_8_uniref90.txt -e 1E-5 -p $th -f 6 qseqid sseqid stitle staxids pident length evalue --taxonmap $taxmap --more-sensitive

echo "9 metatranscriptome - in vitro - contigs - original"
#time diamond blastx -d $db_uniref90 -q $mtt9_ctg -o $out_fp/mtt_9_ctg_uniref90.txt -e 1E-5 -p $th -f 6 qseqid sseqid stitle staxids pident length evalue --taxonmap $taxmap --more-sensitive

echo ""



