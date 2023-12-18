# CCMetagen

CCMetagen processes sequence alignments produced with [KMA](https://bitbucket.org/genomicepidemiology/kma), which implements the ConClave sorting scheme to achieve highly accurate read mappings. The pipeline is fast enough to use the whole NCBI nt collection as reference, facilitating the inclusion of understudied organisms, such as microbial eukaryotes, in metagenome surveys. CCMetagen produces ranked taxonomic results in user-friendly formats that are ready for publication or downstream statistical analyses.

If you this tool, please cite CCMetagen and KMA:

  * [Marcelino VR, Clausen PT, Buchman J, Wille M, Iredell JR, Meyer W, Lund O, Sorrell T, Holmes EC. 2019. CCMetagen: comprehensive and accurate identification of eukaryotes and prokaryotes in metagenomic data. Genome Biology. 2020 Dec;21(1):1-5.](https://genomebiology.biomedcentral.com/articles/10.1186/s13059-020-02014-2)

  * [Clausen PT, Aarestrup FM, Lund O. 2018. Rapid and precise alignment of raw reads against redundant databases with KMA. BMC bioinformatics. 2018 Dec;19(1):307.](https://bmcbioinformatics.biomedcentral.com/articles/10.1186/s12859-018-2336-6)

Besides the guidelines below, we also provide a tutorial to reproduce our metagenome clasisfication analyses of the microbiome of wild birds [here](https://github.com/vrmarcelino/CCMetagen/tree/master/docs/tutorial).

The guidelines below will guide you in using the command-line version of the CCMetagen pipeline.

CCMetagen is also available as a web service at https://cge.food.dtu.dk/services/CCMetagen/.
Note that we recommend using this command-line version to analyze data exceeding 1.5Gb.


## Installation

We recommend installing CCMetagen through [conda](https://docs.conda.io/en/latest/). This will install CCMetagen along with all of its required dependencies.

After installing conda, you can create a new environment with CCMetagen through the following command:

```
conda create -n ccmetagen ccmetagen -c bioconda -c conda-forge
```

You can then activate your environment with:

```
conda activate ccmetagen
```

The `-n ccmetagen` flag will name the environment as `ccmetagen`, but you can choose any different name that you'd like. The `ccmetagen` after that specifies that you'd like the CCMetagen package installed into that environment.
Finally, the `-c bioconda -c conda-forge` specifies that you'd like to use the Bioconda and Conda-Forge channels, which host CCMetagen and its dependencies.

You can also install CCMetagen from source, or using pip, the Python package manager. For that, follow the installation instructions in the deprecated README file in the [docs](https://github.com/vrmarcelino/CCMetagen/tree/master/docs/old_repository_README.md).

Check your CCMetagen installation by running `CCMetagen.py --version` on your command-line.


## Databases

After installing CCMetagen, you will need a reference database to perform taxonomic classification. There are two ways to obtain this:

**Option 1** Download the indexed (ready-to-go) nt from [here](FIXME).
Download the ncbi_nt_Dec_2023.zip file (XXGB zipped file, XXXGB uncompressed) or the RefSeq_bf_2024.zip (90GB zipped file)
Unzip the database, e.g.: `unzip ncbi_nt_kma`.
The nt database contains the whole in NCBI nucleotide collection (as of Aug 2023), and therefore is suitable to identify a range of microorganisms, including prokaryotes and eukaryotes.

There are two versions of the nt database, the one previously mentioned, and another one that does not contain environemntal or artificial sequences. The file ncbi_nt_no_env_Dec2023.zip contains all ncbi nt entries excluding the descendants of environmental eukaryotes (taxid 61964), environmental prokaryotes (48479), unclassified sequences (12908) and artificial sequences (28384).

**Option 2:** Build your own reference database (recommended!)
Follow the instructions in the [KMA website](https://bitbucket.org/genomicepidemiology/kma) to index the database.
It is important that taxids are incorporated in sequence headers for processing with CCMetagen. Sequence headers should look like 
`>1234|sequence_description`, where 1234 is the taxid. 
We provide scripts to rename sequences in the nt database [here](https://github.com/vrmarcelino/CCMetagen/tree/master/docs/benchmarking/rename_nt).

If you want to use the RefSeq database, the format is similar to the one required for Kraken. The [Opiniomics blog](http://www.opiniomics.org/building-a-kraken-database-with-new-ftp-structure-and-no-gi-numbers/) describes how to download sequences in an adequate format. Note that you still need to build the index with KMA: `kma_index -i refseq.fna -o refseq_indexed -NI -Sparse -` or `kma_index -i refseq.fna -o refseq_indexed -NI -Sparse TG` for faster analysis.


## Quick Start

  * First map sequence reads (or contigs) to the database with **KMA**.

For paired-end files:

```
kma -ipe $SAMPLE_R1 $SAMPLE_R2 -o sample_out_kma -t_db $db -t $th -1t1 -mem_mode -and -apm f
```

For single-end files:
```
kma -i $SAMPLE -o sample_out_kma -t_db $db -t $th -1t1 -mem_mode -and
```

If you want to calculate abundance in reads per million (RPM) or in number of reads (fragments), or if you want to calculate the proportion of mapped reads, add the flag -ef (extended features):
```
kma -ipe $SAMPLE_R1 $SAMPLE_R2 -o sample_out_kma -t_db $db -t $th -1t1 -mem_mode -and -apm f -ef
```

Where:

- `$db` is the path to the reference database
- `$th` is the number of threads
- `$SAMPLE_R1` is the path to the mate1 of a paired-end metagenome/metatranscriptome sample (fastq or fasta)
- `$SAMPLE_R2` is the path to the mate2 of a paired-end metagenome/metatranscriptome sample (fastq or fasta)
- `$SAMPLE` is the path to a single-end metagenome/metatranscriptome file (reads or contigs)

Then run `CCMetagen.py`:

```
CCMetagen.py -i $sample_out_kma.res -o results
```

Where $sample_out_kma.res is alignment results produced by KMA.

Note that if you are running CCMetagen from the local folder (instead of adding it to your path), you may need to add 'python' before CCMetagen: `python CCMetagen.py -i $sample_out_kma.res -o results`

Done! This will make an additional quality filter and output a text file with ranked taxonomic classifications and a krona graph file for interactive visualization.

An example of the CCMetagen output can be found [here (.csv file)](https://github.com/vrmarcelino/CCMetagen/blob/master/docs/tutorial/figs_tutorial/Turnstone_Temperate_Flu_Ng.res.csv) and [here (.html file)](https://htmlpreview.github.io/?https://github.com/vrmarcelino/CCMetagen/blob/master/docs/tutorial/figs_tutorial/Turnstone_Temperate_Flu_Ng.res.html).

<img src=docs/tutorial/figs_tutorial/krona_photo.png width="500" height="419.64">

In the .csv file, you will find the depth (abundance) of each match.

## Abundance units

**Depth can be estimated in four ways:** 

1. By applying an additional correction for template length (default in KMA and CCMetagen);
2. By counting the number of nucleotides matching the reference sequence (use flag --depth_unit nc);
3. By calculating depth in Reads Per Million (RPM, use flag --depth_unit rpm); or
4. By counting the number of fragments (i.e. number of PE reads matching to teh reference sequence, use flag --depth_unit fr). If you want RPM or fragment units, you will need to suply the .mapstats file generated with KMA (which you get when running kma with the flag '-ef').


## Balancing sensitivity and specificity

You can **adjust the stringency of the taxonomic assignments** by adjusting the minimum coverage (--coverage), the minimum abundance (--depth), and the minimum level of sequence similarity (--query_identity). Coverage is the percentage of bases in the reference sequence that is covered by the consensus sequence (your query), it can be over 100% when the consensus sequence is larger than the reference (due to insertions for example). You can also adjust the KMA settings to facilitate the identification of more distant-related taxa (see below)

If you change the default depth unit, we recommend adjusting the minimum abundance (--depth) to remove taxa found in low abundance accordingly. For example, you can use -d 200 (200 nucleotides) when using --depth_unit nc, which is similar to -d 0.2 when using the default '--depth_unit kma' option. If you choose to calculate abundances in RPM, you may want to adjust the minimum abundance according to your sequence depth.
For example, to calculate abundances in RPM, and filter out all matches with less than one read per million:

```
CCMetagen.py -i $sample_out_kma.res -o results -map $sample_out_kma.mapstat --depth_unit rpm --depth 1
```

If you would like to know the **proportion of reads mapped** to each template, run kma with the '-ef' flag. This will generate a file with the '.mapstat' extension. Then provide this file to CCMetagen (-map $sample_out_kma.mapstat) and add the flag '-ef y':

```
CCMetagen.py -i $sample_out_kma.res -o results -map $sample_out_kma.mapstat -ef y
```
This will filter the .mapstat file, removing the templates that did not pass CCMetagen's quality control, will add the percentage of mapped reads for each template and will output a file with extension 'stats_csv'. It will also output the overall proportion of reads mapped to these templates in the terminal. For more details about the additional columns of this file, please check [KMA's manual](https://bitbucket.org/genomicepidemiology/kma/src/master/KMAspecification.pdf).

When working with highly complex environemnts for which reference databases are scarce (e.g. many soil and marine metagenomes), it is common to obtain a low proportion of classified reads, especially if the sequencing depth is low. For a more sensitive analysis, besides relaxing the CCMetatgen settings, you can adjust the KMA aligner settings, by for example: removing the `-and` and the `-apm f` flags, so that you can get a match even when the reference sequences are not significantly overrepresented or when only one of the PE reads maps to the template. Check the [KMA manual](https://bitbucket.org/genomicepidemiology/kma/src/master/KMAspecification.pdf) for more details. It can also be useful to build a customized reference database with additional genomes of organisms that are closely related to what you expect to find in your samples.

## Understanding the ranked taxonomic output of CCMetagen:
The taxonomic classifications reflect the sequence similarity between query and reference sequences, according to default or user-defined similarity thresholds. For example, if a match is 97% similar to the reference sequence, the match will not get a species-level classification. If the match is 85% similar to the reference sequence, then the species, genus and family-level classifications will be 'none'.
Note that this is different from identifications tagged as unk_x (unknown taxa). These unknowns indicate taxa where higher-rank classifications have not been defined (according to the NCBI taxonomy database), and it is unrelated to sequence similarity.


For a list of options to customize your analyze, type:
```
CCMetagen.py -h
```

  * **To get the abundance of each taxon, and/or summarize results for multiple samples, use CCMetagen_merge**:
```
CCMetagen_merge.py -i $CCMetagen_out
```

Where `$CCMetagen_out` is the folder containing the CCMetagen taxonomic classifications.
The results must be in .csv format (default or '--mode text' output of CCMetagen), and these files **must end in ".ccm.csv"**.

The flag '-t' define the taxonomic level to merge the results. The default is species-level.

You can also filter out specific taxa, at any taxonomic level:

Use flag -kr to keep (k) or remove (r) taxa.
Use flag -l to set the taxonomic level for the filtering.
Use flag -tlist to list the taxa to keep or remove (separated by comma).

EX1: Filter out bacteria: `CCMetagen_merge.py -i $CCMetagen_out -kr r -l Kingdom -tlist Bacteria`

EX2: Filter out bacteria and Metazoa: `CCMetagen_merge.py -i $CCMetagen_out -kr r -l Kingdom -tlist Bacteria, Metazoa`

EX3: Merge results at family-level, and remove Metazoa and Viridiplantae taxa at Kingdom level:
```
CCMetagen_merge.py -i $CCMetagen_out -t Family -kr r -l Kingdom -tlist Metazoa,Viridiplantae -o family_table
```

For species-level filtering (where there is a space in taxa names), use quotation marks.
Ex 4: Keep only _Escherichia coli_ and _Candida albicans_:
```
CCMetagen_merge.py -i 05_KMetagen/ -kr k -l Species -tlist "Escherichia coli,Candida albicans"
```

If you only have one sample, you can also use CMetagen_merge to get one line per taxa.

To see all options, type:
```
CCMetagen_merge.py -h
```
This file should look like [this](https://github.com/vrmarcelino/CCMetagen/blob/master/tutorial/figs_tutorial/Bird_family_table_filtered.csv).


* **To extract sequences of a given taxon, use CCMetagen_extract_seqs**:

This script will produce a fasta file containing all reads assigned to a taxon of interest. 
Ex: Generate a fasta file containing all sequences that mapped to the genus Eschericha:
```
CCMetagen_extract_seqs.py -iccm $CCMetagen_out -ifrag $sample_out_kma.frag -l Genus -t Eschericha
```

Where `$CCMetagen_out` is the .csv file generated with CCMetagen and `$sample_out_kma.frag` is the .frag file generated with KMA. The frag file needs to be decompressed: `gunzip *.frag.gz`

For species-level filtering (where there is a space in taxon names), use quotation marks.
Ex: Generate a fasta file containing all sequences that mapped to _E. coli_:
```
CCMetagen_extract_seqs.py -iccm $CCMetagen_out -ifrag $sample_out_kma.frag -l Species -t "Escherichia coli"
```


**Check out our [tutorial](https://github.com/vrmarcelino/CCMetagen/tree/master/docs/tutorial) for an applied example of the CCMetagen pipeline.**



## FAQs

* Error taxid not found.
  You probably need to update your local ETE3 database, which contains the taxids and lineage information:
```
python
from ete3 import NCBITaxa
ncbi = NCBITaxa()
ncbi.update_taxonomy_database()
quit()
```

* TypeError: concat() got an unexpected keyword argument 'sort'.
  If you get this error, please update the python module pandas:
```
pip install pandas --upgrade --user
```

* WARNING: no NCBI's taxid found for accession [something], this match will not get taxonomic ranks

  This is not an error, this is just a warning indicating that one of your query sequences matchs to a genbank record for which the NCBI taxonomic identifier (taxid) is not known. CCMetagen therefore will not be able to assign taxonomic ranks to this match, but you will still be able to see it in the output file.

* KeyError: "['Superkingdom' 'Kingdom' 'Phylum' 'Class' 'Order' 'Family' .... ] not in index"
  Make sure that the output of CCMetagen ends in '.csv'.

* The results of the CCMetagen_merge.py at different taxonomic levels do not sum up.
  As explained above, this script merges all unclassified taxa at a given taxonomic level. For example, if you have 20 matches to the genus _Candida_, but only 2 matches were classified at the species level, the output of CCMetagen_merge.py -t Species (default) will only have the abundances of two classified _Candida_ species, while the others will be merged with the "Unclassified" taxa. The output of CCMetagen_merge.py -t Genus however will contain all 20 matches. 
  If this behaviour is undesirable, one option is to disable the similarity thresholds (use flag -off) - so that all taxonomic levels are reported regardless of their similarity to the reference sequence. Alternatively, you can cluster species at the 'Closest_match' (using the flag --tax_level Closest_match).


## Complete option list

CCMetagen:
```
usage: CCMetagen.py [-h] [-m MODE] -i RES_FP [-o OUTPUT_FP]
                    [-r REFERENCE_DATABASE] [-ef EXTENDED_OUTPUT_FILE]
                    [-du DEPTH_UNIT] [-map MAPSTAT] [-d DEPTH] [-c COVERAGE]
                    [-q QUERY_IDENTITY] [-p PVALUE] [-st SPECIES_THRESHOLD]
                    [-gt GENUS_THRESHOLD] [-ft FAMILY_THRESHOLD]
                    [-ot ORDER_THRESHOLD] [-ct CLASS_THRESHOLD]
                    [-pt PHYLUM_THRESHOLD] [-off TURN_OFF_SIM_THRESHOLDS]
                    [--version]

optional arguments:
  -h, --help            show this help message and exit
  -m MODE, --mode MODE  what do you want CCMetagen to do? Valid options are
                        'visual', 'text' or 'both': text: parses kma, filters
                        based on quality and output a text file with taxonomic
                        information and detailed mapping information visual:
                        parses kma, filters based on quality and output a
                        simplified text file and a krona html file for
                        visualization both: outputs both text and visual file
                        formats. Default = both
  -i RES_FP, --res_fp RES_FP
                        Path to the KMA result (.res file)
  -o OUTPUT_FP, --output_fp OUTPUT_FP
                        Path to the output file. Default = CCMetagen_out
  -r REFERENCE_DATABASE, --reference_database REFERENCE_DATABASE
                        Which reference database was used. Options: UNITE,
                        RefSeq or nt. Default = nt
  -ef EXTENDED_OUTPUT_FILE, --extended_output_file EXTENDED_OUTPUT_FILE
                        Produce an extended output file that includes the
                        percentage of classified reads. Options: y or n. To
                        use this featire, you need to generate the mapstat
                        file when required unning KMA (use flag -ef), and use
                        it as input in CCMetagen (flag --mapstat). Default = n
  -du DEPTH_UNIT, --depth_unit DEPTH_UNIT
                        Desired unit for Depth(abundance) measurements.
                        Default = kma (KMA default depth, which is the number
                        of nucleotides overlapping each template, divided by
                        the lengh of the template). Alternatively, you can
                        have abundance calculated in Reads Per Million (RPM,
                        option 'rpm'), in number of nucleotides overlaping the
                        template (option 'nc') or in number of fragments (i.e.
                        PE reads, option 'fr'). If you use the 'nc', 'rpm' or
                        'fr' options, remember to change the default --depth
                        parameter accordingly. Valid options are nc, rpm, fr
                        and kma
  -map MAPSTAT, --mapstat MAPSTAT
                        Path to the mapstat file produced with KMA when using
                        the -ef flag (.mapstat). Required when calculating
                        abundances in RPM or in number of fragments, or when
                        producing the extended_output_file
  -d DEPTH, --depth DEPTH
                        minimum sequencing depth. Default = 0.2. The unit
                        corresponds to the one used with --depth_unit If you
                        use --depth_unit different from the default, change
                        this accordingly.
  -c COVERAGE, --coverage COVERAGE
                        Minimum coverage. Default = 20 (i.e. 20% of the
                        reference sequence)
  -q QUERY_IDENTITY, --query_identity QUERY_IDENTITY
                        Minimum query identity (Phylum level). Default = 50
  -p PVALUE, --pvalue PVALUE
                        Minimum p-value. Default = 0.05.
  -st SPECIES_THRESHOLD, --species_threshold SPECIES_THRESHOLD
                        Species-level similarity threshold. Default = 98.41
  -gt GENUS_THRESHOLD, --genus_threshold GENUS_THRESHOLD
                        Genus-level similarity threshold. Default = 96.31
  -ft FAMILY_THRESHOLD, --family_threshold FAMILY_THRESHOLD
                        Family-level similarity threshold. Default = 88.51
  -ot ORDER_THRESHOLD, --order_threshold ORDER_THRESHOLD
                        Order-level similarity threshold. Default = 81.21
  -ct CLASS_THRESHOLD, --class_threshold CLASS_THRESHOLD
                        Class-level similarity threshold. Default = 80.91
  -pt PHYLUM_THRESHOLD, --phylum_threshold PHYLUM_THRESHOLD
                        Phylum-level similarity threshold. Default = 0 - not
                        applied
  -off TURN_OFF_SIM_THRESHOLDS, --turn_off_sim_thresholds TURN_OFF_SIM_THRESHOLDS
                        Turns simularity-based filtering off. Options = y or
                        n. Default = n
  --version             show program's version number and exit
 ```

