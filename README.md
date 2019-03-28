# CCMetagen

CCMetagen processes sequence alignments produced with [KMA](https://bitbucket.org/genomicepidemiology/kma), which implements the ConClave sorting scheme to achieve highly accurate read mappings. The pipeline is fast enough to use the whole NCBI nt collection as reference, facilitating the inclusion of understudied organisms, such as microbial eukaryotes, in metagenome surveys. CCMetagen produces ranked taxonomic results in user-friendly formats that are ready for publication or downstream statistical analyses.

If you use CCMetagen, please cite: TBA

A quick-start guide is given below. For a more detailed manual - see: xxx.
We also provide a tutorial to reproduce our metagenome clasisfication of the bird microbiome here: xxx


## Requirements and Installation

Make sure you have the depencies below installed and accessible in your $PATH.
The guidelines below are for unix systems.

  * If you do not have it already, donwload and install [Python 3](https://www.python.org/downloads/)
CCMetgen requires Python modules [pandas](https://pandas.pydata.org/) and [ETE3](http://etetoolkit.org/). The easiest way to install these modules is via conda or pip:

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

Then add KMetagen to the path, temporally or permanently. For example:
`PATH=$PATH<your_folder>/CCMetagen/tools`




## Quick Start


`write one line code here`

```
write code here


```
##### Mapping

##### Taxonomic profiling

