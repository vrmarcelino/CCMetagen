# CCMetagen Tutorial

CCMetagen is a pipeline to classify organisms in metagenomes or metatranscriptomes accurately.
This tutorial provides a step-by-step guide to obtain a taxonomic profile for a set of samples.

We will use a set of metatranscriptomes from Australian birds.

The full dataset can be downloaded [here](http://www.ncbi.nlm.nih.gov/bioproject/PRJNA472212).
In this tutorial we will use a subset of it - 75000 PE reads from four libraries - that way you can test and run the pipeline faster. 
You can download the test dataset [here -- link]. This dataset is composed of 4 metatranscritptome libraries of Australian birds, including ducks, avocets and turnstones.

Make sure you have CCMetagen, KMA, and all its dependencies are installed and accessible from your $PATH. The installation is described [here](https://github.com/vrmarcelino/CCMetagen).

Download or build your own indexed database. The indexed NCBI nt database can be downloaded [here -- link].
This database occupies 171GB of disk space, and will require around 500GB of RAM to run. If that is an issue, smaller reference databases can be used (e.g. RefSeq and UNITE databases). [Insert links to download].

This tutorial will not cover quality control, but we highly recommend QC to remove low-quality reads and adapters from your data.
If you are working with host-associated microbiomes, it is desirable to remove host reads as well. I personally like [KneadData](http://huttenhower.sph.harvard.edu/kneaddata) because it allows performing quality filtering, adapter removal and host filtering in one go.


### Mapping reads to a reference database with KMA

To map PE reads to a database, run: `kma -ipe <read1> <read2> -o <output> -t_db <ref_database> -1t1 -mem_mode -and -apm f`

We often work with multiple samples. 
Follow the steps below to run KMA and teh CCMetagen in batch.

Set file paths (note that you need to replace the file paths according to the locations of your folders):
```
input_dir=00_raw_reads
output_dir=01_KMA_res
mkdir $output_dir
nt_db=../../large_databases/KMA/NCBI_nt/ncbi_nt
```

Then run KMA for all files:
```
for r1 in $input_dir/*R1.fastq; do
	r2=${r1/R1.fastq/R2.fastq}
	o_part1=$output_dir/${r1/$input_dir\//''}
	o=${o_part1/.R*/}
	echo $o
	kma -ipe $r1 $r2 -o $o -t_db $nt_db -t 4 -1t1 -mem_mode -and -apm f
done
```
### Process the results with CCMetagen
First reset the variables:

```
input_dir=01_KMA_res
output_dir=02_CCMetagen
mkdir -p $output_dir
```
Then run CCMetagen:
```
for f in $input_dir/*.res; do 
	echo $f
	out=$output_dir/${f/$input_dir\/}
	CCMetagen.py -i $f -r nt -o $out
done
```

### Produce summary table
Finally, merge the results into a single table using the script CCMetagen_merge.py
By default, this script will merge taxa at species level.
Here we will also remove everything that matches to Metazoa (bird sequences), Viriplantae and everything that was Unclassified at the species level.
Note that the input file here is the output folder of CCMetagen.
```
CCMetagen_merge.py --input_fp $output_dir --keep_or_remove r --filtering_tax_level Kingdom --taxa_list Metazoa,Viridiplantae,Unclassified --output_fp Bird_species_table
```

This also works:
```
CCMetagen_merge.py -i $output_dir -kr r -l Kingdom -tlist Metazoa,Viridiplantae,Unclassified -o Bird_species_table
```

If you prefer to merge taxa at different taxonomic levels, use the flag -t' (or '--tax_level):
Options are case-sensitive: Species (Default), Genus, Family, Order, Class, Phylum, Kingdom and Superkingdom.

```
CCMetagen_merge.py --input_fp $output_dir -t Family -o Bird_family_table
```

It is also possible to summarize taxa at different taxonomic levels within PhyloSeq. Therefore, we will use the species-level table (Bird_species_table.csv) as input in PhyloSeq.

Switch to R to proceed with microbiome analyses using PhyloSeq.

### Microbiome analyses
In this tutorial we will use [PhyloSeq](https://www.bioconductor.org/packages/release/bioc/html/phyloseq.html), which is a user-friendly and well-documented R package to analyse microbiome data.


....

