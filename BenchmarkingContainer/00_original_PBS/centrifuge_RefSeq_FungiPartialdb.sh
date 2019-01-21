#!/bin/bash
#PBS -P FGEN
#PBS -l select=1:ncpus=10:mem=80GB
#PBS -l walltime=20:00:00

cd $PBS_O_WORKDIR

module load centrifuge
module load blast


centrifuge-build -p 10 --conversion-table seqid2taxid.map --taxonomy-tree taxonomy/nodes.dmp --name-table taxonomy/names.dmp RefSeq_fungi_partial_db/RefSeq_fung_partial.fna refseq_fun_partial_db


