#!/bin/bash
#PBS -P FGEN
#PBS -l select=1:ncpus=10:mem=300GB
#PBS -l walltime=24:00:00

cd $PBS_O_WORKDIR

module load centrifuge
module load blast


# the last command (without -a) downloads only complete genomes
# -m for dust mask - mask low-complexity regions in the genome

# not working via PBS, doing it manually...
# centrifuge-download -o library -a "Contig" -m -d "fungi" refseq > seqid2taxid.map
# centrifuge-download -o library -a "Scaffold" -m -d "fungi" refseq >> seqid2taxid.map
# centrifuge-download -o library -a "Chromosome" -m -d "fungi" refseq >> seqid2taxid.map
# centrifuge-download -o library -m -d "fungi,bacteria" refseq >> seqid2taxid.map

# $ centrifuge-download -o taxonomy taxonomy
# cat library/*/*.fna > input-sequences.fna

centrifuge-build -p 10 --conversion-table seqid2taxid.map --taxonomy-tree taxonomy/nodes.dmp --name-table taxonomy/names.dmp input-sequences.fna bacfun_refseq

