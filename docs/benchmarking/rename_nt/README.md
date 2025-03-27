## Steps to rename the nt database to index with KMA

This script takes as input a sequential fasta file and a .tsv file with 2 headers: accession number and taxid.

You can download the accession2taxid map from NCBI with:
`wget ftp://ftp.ncbi.nih.gov/pub/taxonomy/accession2taxid/nucl_gb.accession2taxid.gz`


To extract the accession and the taxid info:
```
gunzip nucl_gb.accession2taxid.gz

cut -f 2-3 nucl_gb.accession2taxid > accession_taxid_nucl.map
```

Convert the genbank fasta file to sequencial fasta:
```awk '/^>/ {printf("\n%s\n",$0);next; } { printf("%s",$0);} END {printf("\n");}' < nt.fa > nt_sequential.fa```

Then use the rename_nt.py to add the taxids in sequence headers. You might need to change the name of the input files in the rename_nt.py script.

Sequence headers should look like `>1234|sequence_description`, where 1234 is the taxid.


## Steps to rename the RefSeq database

A less modular script than `rename_nt.py` (which operates on individual fasta files), this will download all the NCBI `"reference genome"` level accessions (currently 20,858 fna, 31GB), and add the `taxid` to the header ( i.e. `>accession_abc` to `>1234|accession_abc`).

Given a `$destination_folder` for the downloads (recommend you choose a new, empty folder!) and a number of `$nthreads`, should be able to call:
```
rename_refseq.sh  $destination_folder  $nthreads
```
The script took about 4 hours with an institutional connection and 20 cores.  
