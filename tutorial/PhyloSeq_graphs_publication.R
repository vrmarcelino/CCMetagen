# Produce nice graphs using PhyloSeq
# VRMarcelino - 18-April-2019

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

raw_CCMetagen_data <-read.csv("Bird_family_table.csv",check.names=FALSE)

# separate species and taxonomy columns
taxa_raw <- as.matrix(raw_CCMetagen_data[,10:ncol(raw_CCMetagen_data)])
rownames(taxa_raw) <- raw_CCMetagen_data[,ncol(raw_CCMetagen_data)]
families_raw <- as.matrix(raw_CCMetagen_data[,1:9])
rownames(families_raw) <- raw_CCMetagen_data[,ncol(raw_CCMetagen_data)]

# convert to phyloseq object
tax = tax_table(taxa_raw)
families_depth = otu_table(families_raw, taxa_are_rows = TRUE)
families_depth

CCMeta_physeq = phyloseq(families_depth, tax)
CCMeta_physeq


#### Analyse and Plot ####

# plot bar graph
# takes a while if the file is large
#plot_bar(CCMeta_physeq, fill = "Kingdom")
#plot_bar(CCMeta_physeq, fill = "Family")

# There are too many taxa to represent, so let's keep the names of the 20 most abundant ones (+Unclassified and 'Others')
SortedOTUs <- names(sort(taxa_sums(CCMeta_physeq), TRUE))
Taxa2Merge <- SortedOTUs[22:length(SortedOTUs)] # 22th and beyond will be merged

Merged_taxa <- merge_taxa(CCMeta_physeq,Taxa2Merge) 
# by default, this will merge all to the taxa with highest abundance, but in the plots, this is called 'NA'

plot_bar(Merged_taxa, fill = "Family") + guides(fill=guide_legend(ncol=2))

# cross-checks:
# otus <- otu_table(Merged_taxa)
# write.csv(otus, file='otus-fam_check.csv') (note that NA is 'Orthomyxoviridae' in this table)


########################
# organise samples and families, add custom colours:
p = plot_bar(Merged_taxa, fill="Family")
p$data$Sample <- factor(p$data$Sample, levels = c("1_Shelduck_Disease","2_Shelduck_Healthy",
                        "3_Turnstone_Temperate_Flu_Negative","4_Turnsone_Temperate_Flu_Positive",
                        "5_Temperate_Duck_Flu_positive","6_Temperate_Duck_Flu_negative","7_Outback_Duck",
                        "8_Avocet_Tempereate","9_Avocet_Outback"))	

# organise order of Families, keeping Fungi and Bacteria Apart:
families = levels(p$data$Family)
families
p$data$Family <- factor(p$data$Family, levels = c("Bacillaceae","Bacteroidaceae",
"Campylobacteraceae","Enterobacteriaceae","Fusobacteriaceae","Pseudomonadaceae","Streptococcaceae",
"Apiosporaceae","Bulleribasidiaceae","Cladosporiaceae","Cystofilobasidiaceae",
"Debaryomycetaceae","Dipodascaceae","Metschnikowiaceae","Mucoraceae","Nectriaceae",
"Rhizopodaceae","Saccotheciaceae","Sporidiobolaceae","Trichomonadidae","Unclassified"))


# set colors

# need 12 colors for fungi
getPalette = colorRampPalette(c("#ffffcc", "#800026"))( 12 )
getPalette

# then paste after the blues, and before the pink and grey
# I got the blues from Color Brewer
family_Palette <- c("#084594","#2171b5","#4292c6","#6baed6","#9ecae1","#c6dbef","#eff3ff",
"#FFFFCC","#F3E7BC","#E7D0AD","#DCB99E","#D0A28F","#C58B80","#B97371","#AE5C62",
"#A24553","#972E44","#8B1735","#800026", "#7a0177","#bdbdbd")
                
publication_fig <- p + scale_fill_manual(values=family_Palette, na.value="black") +
  geom_bar(aes(fill=Family), stat="identity", position="stack") +
  guides(fill=guide_legend(ncol=2))

publication_fig

#########################
### Notes on families:

# Bacteria (7):
"Bacillaceae"
"Bacteroidaceae"
"Campylobacteraceae"
"Enterobacteriaceae"
"Fusobacteriaceae"
"Pseudomonadaceae"
"Streptococcaceae"  

#Fungi (12)
"Apiosporaceae"
"Bulleribasidiaceae"
"Cladosporiaceae" 
"Cystofilobasidiaceae"
"Debaryomycetaceae"
"Dipodascaceae"
"Metschnikowiaceae"
"Mucoraceae"
"Nectriaceae"
"Rhizopodaceae"
"Saccotheciaceae"
"Sporidiobolaceae"

# Other euks (protozoa) 
"Trichomonadidae"

# Taxa without a family-level classification:
"Unclassified"

# Taxa present at lower abundance were merged and are indicated as 'NA' (manually rename it to 'Others')
"NA"


