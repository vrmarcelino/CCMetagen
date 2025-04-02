#!/usr/bin/bash

## ================================================================================================ ##   handibles.mar.25
##   A less modular script than rename_nt.py (which operates on individual fasta files), this will  ##
##   download all the NCBI `"reference genome"` level accessions (currently 20,858 fna, 31GB), and  ##
##   add the `taxid` to the header ( i.e. `>accession_abc` to `>1234|accession_abc`)                ##
##                                                                                                  ##
##   > rename_refseq.sh  $destination_folder  $nthreads                                             ##
## ------------------------------------------------------------------------------------------------ ##

workdir=$1
threeds=$2
if [ -z $workdir ] ; then echo " < ! >   need to provide a destination folder!" ; stop 1 ; fi
if [ -z $threeds ] ; then threeds=20 ; fi
# the dir wherin the RefSeq is stowed
mkdir -p $workdir

echo " + 1 +   recommended to dl some NCBI RefSeq genomes - 30m  ---------------"
wget https://ftp.ncbi.nlm.nih.gov/genomes/refseq/bacteria/assembly_summary.txt -O $workdir/assembly_summary.txt   > $workdir/wgetlog1.temp 2>&1  
grep "reference genome" $workdir/assembly_summary.txt >> $workdir/assembly_summary_ref.txt                                # 20,858 references
cut -f20 $workdir/assembly_summary_ref.txt | parallel -j $threeds "wget -r -np -nH --cut-dirs=5 {}/{/}_genomic.fna.gz -O $workdir/{/}_genomic.fna.gz" >> $workdir/wgetlog1.temp 2>&1  
# 26GB, 29min, Mar.2025 - 20,860 fna.gz


echo " + 2 +   get RefSeq ("_") accession-taxid listings - 10m?  ---------------"
wget http://ftp.ncbi.nih.gov/pub/taxonomy/accession2taxid/nucl_gb.accession2taxid.gz -O $workdir/nucl_gb.accession2taxid.gz >> $workdir/wgetlog2.temp 2>&1           # 2.3/13GB - non TranscrShotAss / WGS
wget https://ftp.ncbi.nlm.nih.gov/pub/taxonomy/accession2taxid/nucl_wgs.accession2taxid.gz -O $workdir/nucl_wgs.accession2taxid.gz >> $workdir/wgetlog3.temp 2>&1   # 5.0/33GB - TranscrShotAss / WGS
zgrep "_" $workdir/nucl_*.accession2taxid.gz | cut -f 2-3 > $workdir/accession_taxid_nucl-rs.map                          # 124,253,447 entries ; says 3m but thats not true


echo " + 3 +   function to list accession-fasta pairs - 3m  --------------------"
accession_filename () {
  zcat $1 | awk -v filen=$1 '/^>/ {print substr($1, 2), "\t", filen}'
}
export -f accession_filename
parallel --keep-order -j $threeds accession_filename {} ::: ${workdir}/*genomic.fna.gz > $workdir/accession_fqpath-rs.map  # 3m, 1,074,620 entries, 20857 fna.gz 


echo " + 4 +   sort & join two lists by accession - 3m  ----(ignore 9606 error!)"
time join -j 1 -e XXXcatastrophotronXXXX -o 1.2,2.2 <( sort $workdir/accession_taxid_nucl-rs.map ) <( sort $workdir/accession_fqpath-rs.map ) | tr " " "\t" | sort -u > $workdir/taxid_fqpath.map
## 
# join: /dev/fd/63:307894: is not sorted: NM_001000.4     9606
# join: input is not in sorted order


echo " + 5 +   re-stamp headers - 30m  -----------------------------------------"
cat $workdir/taxid_fqpath.map | \
  parallel --colsep "\t" -j $threeds "gzip -dc {2} | sed -E \"s/>/>{1}\|/g\" > {=2 s/(.*).fna.gz/\${1}_taxID2.fna/=} "  >> $workdir/stamplog.temp 2>&1

parallel -j $threeds gzip {} ::: $workdir/*genomic_taxID2.fna && rm $workdir/*genomic.fna.gz  # 20min
