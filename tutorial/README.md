# Tutorial

CCMetagen is a pipeline to classify organisms in metagenomes or metatranscriptomes accurately.
This tutorial provides a step-by-step guide to obtain a taxonomic profile for a set of samples.

We will use a set of metatranscriptomes from Australian birds.

The full dataset can be downloaded [here](http://www.ncbi.nlm.nih.gov/bioproject/PRJNA472212).
In this tutorial we will use a subset of it - 75000 PE reads from four libraries - that way you can test and run the pipeline faster. 
You can download the test dataset [here -- link]. This dataset is composed of 4 metatranscritptome libraries of Australian birds, including ducks, avocets and turnstones.

Make sure you have CCMetagen, KMA, and all its dependencies are installed and accessible from your $PATH. The installation is described [here](https://github.com/vrmarcelino/CCMetagen).

Download or build your own indexed database. Here we will use the the [ncbi_nt_no_env_11jun2019](https://cloudstor.aarnet.edu.au/plus/s/Mp8gLimDYoLfelH), which contains the ncbi nucleotide collection but excludes most artificial (e.g. cloning vectors) and environmental sequences without valid taxids. The database must be uncompressed before use: `unzip ncbi_nt_no_env_11jun2019.zip`. The uncompressed database occupies 196GB of disk space, and will require around 500GB of RAM to run. If that is an issue, smaller reference databases can be used (e.g. RefSeq and UNITE databases). [Insert links to download]. You can also use the [CCMetagen webserver](https://cge.cbs.dtu.dk/services/ccmetagen/).

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

KMA will produce three files. The one used in CCMetagen ends with .res, and it should look like [this](https://github.com/vrmarcelino/CCMetagen/blob/master/tutorial/figs_tutorial/Turnstone_Temperate_Flu_Ng.res).

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
	CCMetagen.py -i $f -o $out
done
```

This will generate another 3 files per sample.
Here are examples of the produced [.csv file](https://github.com/vrmarcelino/CCMetagen/blob/master/tutorial/figs_tutorial/Turnstone_Temperate_Flu_Ng.res.csv), the [.html file](https://htmlpreview.github.io/?https://github.com/vrmarcelino/CCMetagen/blob/master/tutorial/figs_tutorial/Turnstone_Temperate_Flu_Ng.res.html), and the [.tsv file](https://github.com/vrmarcelino/CCMetagen/blob/master/tutorial/figs_tutorial/Turnstone_Temperate_Flu_Ng.res.tsv), which is used to produce the krona graph.

If you use the entire nt database (ncbi_nt_kma), you might get raws without taxonomic information - these are entries in genbank without a valid taxid. To avoid those entries, use the updated and 'clean' nt database [ncbi_nt_no_env_11jun2019](https://cloudstor.aarnet.edu.au/plus/s/Mp8gLimDYoLfelH).


### Produce summary table
Finally, merge the results into a single table using the script CCMetagen_merge.py
By default, this script will merge taxa at the species level.
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

Let's produce a family-level table to process in PhyloSeq, filtering Metazoa and Viriplantae, for input in PhyloSeq:

```
CCMetagen_merge.py -i $output_dir -t Family -kr r -l Kingdom -tlist Metazoa,Viridiplantae -o Bird_family_table_filtered
```
This file should look like [this](https://github.com/vrmarcelino/CCMetagen/blob/master/tutorial/Bird_family_table_filtered.csv).

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
```
library(dplyr); packageVersion("dplyr")
```
[1] ‘0.7.8’

Set ggplot colour theme to white: 
```
theme_set(theme_bw())
```

##### Import data and convert to a phyloseq object

```
raw_CCMetagen_data <-read.csv("Bird_family_table_filtered.csv",check.names=FALSE)
```

PhyloSeq does not like rows with the same taxonomy, so our unclassififed taxa (unk_f) are a problem. 
We will therefore separate bacterial from eukaryotic unclassifified taxa. Note that you can skip these steps if you remove unclassififed taxa (unk_f) with CCMetagen_merge.

First, we will add a new column containing family names and superkingdom:

```
raw_CCMetagen_data$SuperKFamily <- paste(raw_CCMetagen_data$Superkingdom, raw_CCMetagen_data$Family, sep="_")

```

Let's also add an 'unclassififed' string at the end of these to avoid confusion:
```
raw_CCMetagen_data <- data.frame(lapply(raw_CCMetagen_data, function(x) {sub("Bacteria_$", "Bacteria_unclassififed", x)}))
raw_CCMetagen_data <- data.frame(lapply(raw_CCMetagen_data, function(x) {sub("Eukaryota_$", "Eukaryota_unclassififed", x)}))
```

Then we need to deete taxonomic ranks for which there are multiple taxa merged into 'Eukaryota_unclassififed' or 'Bacteria_unclassififed'. In our case , we will delete Phylum, Class, Order and the previous Family. We will also convert the abundances to numeric, aggregate the unclassififed taxa, and rename the new family column:

```
CCMetagen_data <-raw_CCMetagen_data[,-which(names(raw_CCMetagen_data) %in% c("Phylum","Class","Order","Family"))]
CCMetagen_data[,1:4] <-mutate_all(CCMetagen_data[,1:4], function(x) as.numeric(as.character(x)))
CCMetagen_data <- aggregate(. ~ Superkingdom+Kingdom+SuperKFamily,CCMetagen_data, sum)
colnames(CCMetagen_data)[3] <- "Family"
```

Now this data is ready to be converted to PhyloSeq.


Separate species' abundances and taxonomy columns
```
taxa_raw <- as.matrix(CCMetagen_data[,1:3])
rownames(taxa_raw) <- taxa_raw[,3]
abund_raw <- as.matrix(CCMetagen_data[,4:7])
rownames(abund_raw) <- CCMetagen_data[,3]
```
Convert to phyloseq object
```
tax = tax_table(taxa_raw)
taxa = otu_table(abund_raw, taxa_are_rows = TRUE)
taxa

CCMeta_physeq = phyloseq(taxa, tax)
CCMeta_physeq
```

##### Plot

Plot bar graphs
Note that this takes a while for large files
```
plot_bar(CCMeta_physeq, fill = "Superkingdom")

```
<img src=figs_tutorial/Superkingdom.png width="500" height="450">

You can also fill in teh graphs by Family, but the figure is unclear due to the large number of families.
Therefore let's keep only the 16 most abundant ones.

```
TopNOTUs <- names(sort(taxa_sums(CCMeta_physeq), TRUE)[1:16])
TopFamilies <- prune_taxa(TopNOTUs, CCMeta_physeq)
```
Plot bars, colouring by different taxonomic ranks
"NA" here represents taxa that were classified at family level but did not have a higher-rank tax classification.
```
plot_bar(TopFamilies, fill = "Family")

```
<img src=figs_tutorial/Most_abudnant_families.png width="500" height="550">


##### Organised plots
Organise samples and families, add custom colours.
Arrange the order of families, keeping Fungi and Bacteria Apart 
The idea is to get bacterial taxa in blue, fungal taxa in red and other eukaryotic taxa in pink.

```
p = plot_bar(TopFamilies, fill="Family")
p$data$Sample <- factor(p$data$Sample, levels = c("Shelduck_Healthy.res","Temperate_Duck_Flu_Ng.res",
                        "Avocet_Outback.res","Turnstone_Temperate_Flu_Ng.res"))	

families = levels(p$data$Family)
families
p$data$Family <- factor(p$data$Family, levels = c("Bacteria_Bacillaceae","Bacteria_Enterobacteriaceae",
"Bacteria_Fusobacteriaceae","Bacteria_Streptococcaceae","Bacteria_unk_f","Eukaryota_Apiosporaceae","Eukaryota_Cystofilobasidiaceae",
"Eukaryota_Debaryomycetaceae","Eukaryota_Dipodascaceae","Eukaryota_Dothioraceae","Eukaryota_Metschnikowiaceae","Eukaryota_Mucoraceae",
"Eukaryota_Nectriaceae","Eukaryota_Saccotheciaceae","Eukaryota_Tuberaceae","Eukaryota_Trichomonadidae","Eukaryota_unk_f"))
```

Set colors
We need 11 colors for fungi
```
getPalette = colorRampPalette(c("#ffffcc", "#800026"))( 11 )
getPalette
```
Then paste the color codes after the blues (5 bacterial families), and before the pink and grey (last 2 colours)
```
family_Palette <- c("#08519c","#2171b5","#4292c6","#6baed6","#c6dbef",
"#FFFFCC","#F2E5BB","#E5CCAA","#D8B29A","#CC9989","#BF7F79","#B26568",
"#A64C57","#993247","#8C1936","#800026")
```

Now plot it:
```                          
fig <- p + scale_fill_manual(values=family_Palette) +
  geom_bar(aes(fill=Family), stat="identity", position="stack") +
  guides(fill=guide_legend(ncol=2))

fig
```
<img src=figs_tutorial/Nicer_fam_figure.png width="500" height="550">

To reproduce the figure of the full dataset, see R script [here](https://github.com/vrmarcelino/CCMetagen/blob/master/tutorial/PhyloSeq_graphs_publication.R).





