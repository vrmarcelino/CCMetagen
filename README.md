# CCMetagen

CCMetagen processes sequence alignments produced with [KMA](https://bitbucket.org/genomicepidemiology/kma), which implements the ConClave sorting scheme to achieve highly accurate read mappings. The pipeline is fast enough to use the whole NCBI nt collection as reference, facilitating the inclusion of understudied organisms, such as microbial eukaryotes, in metagenome surveys. CCMetagen produces ranked taxonomic results in user-friendly formats that are ready for publication or downstream statistical analyses.

If you use CCMetagen, please cite: TBA

A quick-start guide is given below. For a more detailed manual - see: xxx.
We also provide a tutorial to reproduce our metagenome clasisfication of the bird microbiome here: xxx


## Requirements and Installation

Make sure you have the dependencies below installed and accessible in your $PATH.
The guidelines below are for Unix systems.

  * If you do not have it already, download and install [Python 3](https://www.python.org/downloads/)
CCMetagen requires Python modules [pandas](https://pandas.pydata.org/) and [ETE3](http://etetoolkit.org/). The easiest way to install these modules is via conda or pip:

`conda install pandas`

  * You need a C-compiler and zlib development files to install KMA:

`sudo apt-get install libz-dev`

  * Download and install [KMA](https://bitbucket.org/genomicepidemiology/kma):
```
git clone https://bitbucket.org/genomicepidemiology/kma.git
cd kma && make
```

  * [Krona](https://github.com/marbl/Krona) is required for graphs. To install Krona it in the local folder:
```
wget https://github.com/marbl/Krona/releases/download/v2.7/KronaTools-2.7.tar
tar xvf KronaTools-2.7.tar 
cd  KronaTools-2.7
./install.pl --prefix . 
```

  * Then download CCMetagen and add it to your path.
If you have git:
```
git clone https://github.com/vrmarcelino/CCMetagen
```
You can also download the python files from https://github.com/vrmarcelino/CCMetagen/tree/master/tools

Then add CCMetagen to the path, temporarily or permanently. For example:
`PATH=$PATH<your_folder>/CCMetagen/tools`

To update CCMetagen, go to the CCMetagen folder and type: `git pull`

## Databases

Donwload the indexed (redy-to-go) nt database [here - add link]().
This database contains everything in NCBI nucleotide collection, and therefore is suitable to include microbial eukaryotes in metagenome surveys.

To build your own reference database, please refer to the manual (insert link).


## Quick Start

First map reads to the database with KMA.
For paired-end files:
```
kma -ipe $SAMPLE_R1 $SAMPLE_R2 -o sample_out_kma -t_db $db -t $th -1t1 -mem_mode -and -apm f
```

For single-end files:
kma -i $SAMPLE -o sample_out_kma -t_db $db -t $th -1t1 -mem_mode -and


Where:

$db is the path to the reference database
$th is the number of threads
$SAMPLE_R1 is the path to the mate1 of a paired-end metagenome/metatranscriptome sample (fastq or fasta)
$SAMPLE_R2 is the path to the mate2 of a paired-end metagenome/metatranscriptome sample (fastq or fasta)
$SAMPLE is the path to a single-end metagenome/metatranscriptome file (reads or contigs)


Then run CCMetagen:
```
CCMetagen.py -i $sample_out_kma.res -o results
```
Where $sample_out_kma.res is alignment results produced by KMA.

Note that if you are running CCMetagen from the local folder (instead of adding it to your path), you may need to add 'python' before CCMetagen: `python CCMetagen.py -i $sample_out_kma.res -o results`

Done. This will make an additional quality filter and output a text file with ranked taxonomic classifications and a krona graph file for interactive visualization.


For options to customize your analyze, please refer to the [Manual - add link](), or type:
```
CCMetagen.py -h
```

To summarize multiple CCMetagen results and/or exclude taxa from the analyses, use CCMetagen_merge:
```
CCMetagen_merge.py -i $CCMetagen_out
```

The flags '-t' define the taxonomic level to merge the results. The default is species-level.

You can also filter taxa at different taxonomic levels using -l (--filtering_tax_level), '-tlist' (--taxa_list) and '-kr' (--keep_or_remove) flags.
For example, to merge various CCMetagen results (in a folder called 'CCMetagen_res') at family-level, and remove Metazoa, Viridiplantae and Unclassified (NA) taxa at Kingdom level:
```
CCMetagen_merge.py -i $CCMetagen_out -t Family -kr r -l Kingdom -tlist Metazoa,Viridiplantae,NA -o family_table
```

For options, type:
```
KMetagen_merge.py -h
```

You can also refer to our [tutorial - add link] for an applied example of the CCMetagen pipeline.


## FAQs

  * Error taxid not found.
You probably need to update your local ETE3 database, which contains the taxids and their lineages information:
```
python
from ete3 import NCBITaxa
ncbi = NCBITaxa()
ncbi.update_taxonomy_database()
quit()
```

  * TypeError: concat() got an unexpected keyword argument 'sort'
If you get this error, please update the python module pandas:
```
pip install pandas --upgrade --user
```




 



