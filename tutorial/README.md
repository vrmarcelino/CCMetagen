# Tutorial

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
Here we will also remove everything that matches to Metazoa (bird sequences) and Viriplantae.
Note that the input file here is the output folder of CCMetagen.
```
CCMetagen_merge.py --input_fp $output_dir --keep_or_remove r --filtering_tax_level Kingdom --taxa_list Metazoa,Viridiplantae --output_fp Bird_species_table
```

This also works:
```
CCMetagen_merge.py -i $output_dir -kr r -l Kingdom -tlist Metazoa,Viridiplantae -o Bird_species_table
```

If you prefer to merge taxa at different taxonomic levels, use the flag -t' (or '--tax_level):
Options are case-sensitive: Species (Default), Genus, Family, Order, Class, Phylum, Kingdom and Superkingdom.

```
CCMetagen_merge.py --input_fp $output_dir -t Family -o Bird_family_table
```

It is also possible to summarize taxa at different taxonomic levels within PhyloSeq. However, we do not recommend to use the species table produced with CCMetagen_merge to produce a family-level figue/analyses in PhyloSeq because you will lose information. 
When results are merged at species level, all unclassified taxa will be clustered togetehr in one row, while merging at higher taxonomic levels will retain the information about the abudnances of the different taxa.


Therefore, we let's produce a family-level table, filtering Metazoa and Viriplantae, for input in PhyloSeq:

```
CCMetagen_merge.py -i $output_dir -t Family -kr r -l Kingdom -tlist Metazoa,Viridiplantae -o Bird_family_table_filtered
```

Switch to R to proceed with microbiome analyses using PhyloSeq.

### Microbiome analyses
In this tutorial we will use [PhyloSeq](https://www.bioconductor.org/packages/release/bioc/html/phyloseq.html), which is a user-friendly and well-documented R package to analyse microbiome data.

In R:

##### Install and load packages + settings:
Install phyloseq:
```
source('http://bioconductor.org/biocLite.R')
biocLite('phyloseq')
```
Load the necessary modules:
```
library("phyloseq"); packageVersion("phyloseq")
```
[1] ‘1.24.2’

```
library("ggplot2"); packageVersion("ggplot2")
```
[1] ‘3.1.0’

```
library (RColorBrewer); packageVersion("RColorBrewer")
```
[1] ‘1.1.2’

Set ggplot colour theme to white: 
```
theme_set(theme_bw())
```

##### Import data and convert to a phyloseq object

```
raw_CCMetagen_data <-read.csv("Bird_family_table_filtered.csv",check.names=FALSE)
```

Separate species and taxonomy columns - note that this will change according to how many samples you have
We have 4 samples here, therefore our taxa start at column, while the samples (microbial species data) are in columns 1 to 4.
```
taxa_raw <- as.matrix(raw_CCMetagen_data[,5:ncol(raw_CCMetagen_data)])
rownames(taxa_raw) <- raw_CCMetagen_data[,ncol(raw_CCMetagen_data)]
species_raw <- as.matrix(raw_CCMetagen_data[,1:4])
rownames(species_raw) <- raw_CCMetagen_data[,ncol(raw_CCMetagen_data)]
```
Convert to phyloseq object
```
tax = tax_table(taxa_raw)
taxa = otu_table(species_raw, taxa_are_rows = TRUE)
taxa

CCMeta_physeq = phyloseq(taxa, tax)
CCMeta_physeq
```

##### Plot

Plot bar graphs
Note that this takes a while for large files
```
plot_bar(CCMeta_physeq, fill = "Superkingdom")```

```
<img src=figs_tutorial/Superkingdom.png width="100" height="100">

```
plot_bar(CCMeta_physeq, fill = "Family")
```


<<Figure 1 here>>


This graph is ok, but the large number of taxa makes the figure unclear. Therefore let's keep only the 16 most abundant ones.

```
TopNOTUs <- names(sort(taxa_sums(CCMeta_physeq), TRUE)[1:16])
TopFamilies <- prune_taxa(TopNOTUs, CCMeta_physeq)
```
Plot bars, colouring by different taxonomic ranks
"NA" here represents taxa that were classified at family level but did not have a higher-rank tax classification.
```
plot_bar(TopFamilies, fill = "Superkingdom")
plot_bar(TopFamilies, fill = "Family")

```

##### Organised plots
Organise samples and families, add custom colours.
Arrange the order of families, keeping Fungi and Bacteria Apart 
The idea is to get bacterial taxa in blue, fungal taxa in red and other eukaryotic taxa in pink.

```
p = plot_bar(TopFamilies, fill="Family")
p$data$Sample <- factor(p$data$Sample, levels = c("Shelduck_Healthy","Temperate_Duck_Flu_Ng",
                        "Avocet_Outback","Turnstone_Temperate_Flu_Ng"))	


families = levels(p$data$Family)
families
p$data$Family <- factor(p$data$Family, levels = c("Bacillaceae","Enterobacteriaceae",
"Fusobacteriaceae","Streptococcaceae","Apiosporaceae","Cystofilobasidiaceae",
"Debaryomycetaceae","Dipodascaceae","Dothioraceae","Metschnikowiaceae","Mucoraceae","Nectriaceae",
"Saccotheciaceae","Tuberaceae","Trichomonadidae","Unclassified"))

```

Set colors
We need 10 colors for fungi
```
getPalette = colorRampPalette(c("#ffffcc", "#800026"))( 10 )
getPalette
```
Then paste the color codes after the blues (4 bacterial families), and before the pink and grey (last 2 colours)
```
family_Palette <- c("#08519c","#2171b5","#4292c6","#6baed6",
"#FFFFCC","#F0E2B9","#E2C6A7","#D4AA94","#C68D82","#B8716F","#AA555D","#9C384A",
"#8E1C38","#800026","#ae017e","#999999")
```

Now plot it:
```                          
fig <- p + scale_fill_manual(values=family_Palette) +
  geom_bar(aes(fill=Family), stat="identity", position="stack") +
  guides(fill=guide_legend(ncol=2))

fig
```

To reproduce the figure of the full dataset, see R script [here](https://github.com/vrmarcelino/CCMetagen/blob/master/tutorial/PhyloSeq_graphs_publication.R).



