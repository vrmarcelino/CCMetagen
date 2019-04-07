# Produce nice graphs using PhyloSeq
# VRMarcelino - 08-April-2019

rm(list=ls(all=TRUE))

#### Instal and load packages + settings ####
# to install phyloseq:
#source('http://bioconductor.org/biocLite.R')
#biocLite('phyloseq')

library("phyloseq"); packageVersion("phyloseq")
#[1] ‘1.24.2’

library("ggplot2"); packageVersion("ggplot2")
#[1] ‘3.1.0’

library (RColorBrewer); packageVersion("RColorBrewer")
# [1] ‘1.1.2’

# set ggplot colour theme to white
theme_set(theme_bw())



#### Import data and convert to a phyloseq object ####

raw_CCMetagen_data <-read.csv("Bird_species_table.csv",check.names=FALSE)

# separate species and taxonomy columns
taxa_raw <- as.matrix(raw_CCMetagen_data[,10:ncol(raw_CCMetagen_data)])
rownames(taxa_raw) <- raw_CCMetagen_data[,ncol(raw_CCMetagen_data)]
species_raw <- as.matrix(raw_CCMetagen_data[,1:9])
rownames(species_raw) <- raw_CCMetagen_data[,ncol(raw_CCMetagen_data)]

# convert to phyloseq object
tax = tax_table(taxa_raw)
species = otu_table(species_raw, taxa_are_rows = TRUE)
species

CCMeta_physeq = phyloseq(species, tax)
CCMeta_physeq


#### Analyse and Plot ####

# plot bar graph
# takes a while if the file is large
# plot_bar(CCMeta_physeq, fill = "Kingdom")

# Keep only the 50 most abundant Species (excluding taxa that were unclassified at species level)
TopNOTUs <- names(sort(taxa_sums(CCMeta_physeq), TRUE)[1:51])
TopNOTUs <- TopNOTUs[-1] #removes the unclassified species
TopSpecies <- prune_taxa(TopNOTUs, CCMeta_physeq)

# Plot bars, colouring by different taxonomic ranks
# "NA" here represents taxa that were classified at species level but did not have a higher-rank tax classification.
plot_bar(TopSpecies, fill = "Superkingdom")
plot_bar(TopSpecies, fill = "Genus")
plot_bar(TopSpecies, fill = "Family")


# organise samples and families, add custom colours:
p = plot_bar(TopSpecies, fill="Family")
p$data$Sample <- factor(p$data$Sample, levels = c("1_Shelduck_Disease","2_Shelduck_Healthy",
                        "3_Turnstone_Temperate_Flu_Negative","4_Turnsone_Temperate_Flu_Positive",
                        "5_Temperate_Duck_Flu_positive","6_Temperate_Duck_Flu_negative","7_Outback_Duck",
                        "8_Avocet_Tempereate","9_Avocet_Outback"))	

# organise order of Families, Keeping Fungi and Bacteria Apart:
families = levels(p$data$Family)
families
p$data$Family <- factor(p$data$Family, levels = c("Bacillaceae","Clostridiaceae","Enterobacteriaceae",
"Fusobacteriaceae","Pseudomonadaceae","Streptococcaceae","Apiosporaceae",
"Bulleribasidiaceae","Cladosporiaceae","Cryptococcaceae","Cystofilobasidiaceae",
"Debaryomycetaceae","Dipodascaceae","Metschnikowiaceae","Mucoraceae","Nectriaceae",
"Saccotheciaceae","Sporidiobolaceae","Bromoviridae"))

# set colors

# need 12 colors for fungi
getPalette = colorRampPalette(c("#ffffcc", "#800026"))( 12 )
getPalette

# then paste after the blues, and before the pink and grey
family_Palette <- c("#08519c","#2171b5","#4292c6","#6baed6","#9ecae1","#c6dbef",
"#FFFFCC","#F3E7BC","#E7D0AD","#DCB99E","#D0A28F","#C58B80","#B97371","#AE5C62",
"#A24553","#972E44","#8B1735","#800026", "#ae017e","#999999")
                
publication_fig <- p + scale_fill_manual(values=family_Palette, na.value="grey") +
  geom_bar(aes(fill=Family), stat="identity", position="stack") +
  guides(fill=guide_legend(ncol=2))

publication_fig

#########################
### Notes on families:

# Bacteria:
"Bacillaceae" 
"Clostridiaceae"
"Enterobacteriaceae"
"Fusobacteriaceae"
"Pseudomonadaceae"
"Streptococcaceae"  

#Fungi:
"Apiosporaceae"
"Bulleribasidiaceae"
"Cladosporiaceae" 
"Cryptococcaceae"
"Cystofilobasidiaceae"
"Debaryomycetaceae"
"Dipodascaceae"
"Metschnikowiaceae"
"Mucoraceae"
"Nectriaceae"
"Saccotheciaceae"
"Sporidiobolaceae"

# Virus:
"Bromoviridae"

# Taxa without a family-level classification:
"NA"
