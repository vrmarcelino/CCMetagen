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

## Original metatranscriptome:
mtt8_R1=03_Quality_Control/8_mtt_good_1.fastq
mtt8_R2=03_Quality_Control/8_mtt_good_2.fastq


##### Analyses sets #####

# GenBank - full ncbi
db_nt=db/centrifuge/ncbi_nt_official_cent/nt
echo "GenBank full"
echo "1 metatrans - in silico"
time centrifuge -x $db_nt -f -1 $mtt1_R1 -2 $mtt1_R2 -S $out_fp/mtt_1_nt --report-file $out_fp/mtt_1_nt_report.tsv -p $th
echo "2 metagenome - in silico"
time centrifuge -x $db_nt -1 $mtg2_R1 -2 $mtg2_R2 -S $out_fp/mtg_2_nt --report-file $out_fp/mtg_2_nt_report.tsv -p $th
echo "8 metatranscriptome - in vitro - original"
time centrifuge -x $db_nt -1 $mtt8_R1 -2 $mtt8_R2 -S $out_fp/mtt_8_nt --report-file $out_fp/mtt_8_nt_report.tsv -p $th
echo ""


# RefSeq bacteria and fungi
db_refseq_bf=db/centrifuge/RefSeq/bacfun_refseq
echo "RefSeq bacteria and fungi"
echo "1 metatrans - in silico"
time centrifuge -x $db_refseq_bf -f -1 $mtt1_R1 -2 $mtt1_R2 -S $out_fp/mtt_1_refseq_bf --report-file $out_fp/mtt_1_refseq_bf_report.tsv -p $th
echo "2 metagenome - in silico"
time centrifuge -x $db_refseq_bf -1 $mtg2_R1 -2 $mtg2_R2 -S $out_fp/mtg_2_refseq_bf --report-file $out_fp/mtg_2_refseq_bf_report.tsv -p $th
echo "8 metatranscriptome - in vitro - original"
time centrifuge -x $db_refseq_bf -1 $mtt8_R1 -2 $mtt8_R2 -S $out_fp/mtt_8_refseq_bf --report-file $out_fp/mtt_8_refseq_bf_report.tsv -p $th
echo ""


# RefSeq fungi - incomplete db (50%)
db_refseq_f_part=db/centrifuge/RefSeq/refseq_fun_partial_db
echo "RefSeq fungi - incomplete db"
echo "1 metatrans - in silico"
time centrifuge -x $db_refseq_f_part -f -1 $mtt1_R1 -2 $mtt1_R2 -S $out_fp/mtt_1_refseq_f_part --report-file $out_fp/mtt_1_refseq_f_part_report.tsv -p $th
echo "2 metagenome - in silico"
time centrifuge -x $db_refseq_f_part -1 $mtg2_R1 -2 $mtg2_R2 -S $out_fp/mtg_2_refseq_f_part --report-file $out_fp/mtg_2_refseq_f_part_report.tsv -p $th
echo "8 metatranscriptome - in vitro - original"
time centrifuge -x $db_refseq_f_part -1 $mtt8_R1 -2 $mtt8_R2 -S $out_fp/mtt_8_refseq_f_part --report-file $out_fp/mtt_8_refseq_f_part_report.tsv -p $th
echo ""


### Now run the bacterial datasets:
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



