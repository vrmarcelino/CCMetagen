#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
KMetagen main script

Version 0.1

@ V.R.Marcelino
Created on Wed Jul 25 17:13:10 2018
Updated: 17 Dec 2019
Version: 0.1

"""

# imports
import sys
import pandas as pd
from argparse import ArgumentParser
import subprocess

# local imports
import fParseKMA
import cTaxInfo # needed in fParseKMA
import fNCBItax # needed in fParseKMA
import fAcc2TaxId # needed in fParseKMA for nt database
import random # for random base name (important if running KMetagen on multiple files)

# help
if len(sys.argv) == 1:
    print ("")
    print ("KMetagen - Identify species in metagenome datasets")
    print ("version: 0.1")
    print ("To be used with KMA")
    print ("")
    print ("Usage: KMetagen.py <options> ")
    print ("Ex: KMetagen.py -m 1 -i KMA_out/2_mtg_ITS.res -r UNITE -o parse_result_2mtg")
    print ("")
    print ("")
    print ("""When running KMetagen for multiple files in a folder:
input_dir=KMA_out
output_dir=KMetagen_results
mkdir $output_dir
for f in $input_dir/*.res; do 
    out=$output_dir/${f/$input_dir\/}
    KMetagen.py -m visual -i $f -r UNITE -o $out
done""")
    print ("")
    print ("For help and options, type: KMetagen.py -h")
    print ("")
    print ("")
    sys.exit()


parser = ArgumentParser()

parser.add_argument('-m', '--mode', help="""what do you want KMetagen to do? 
                    Valid options at the moment are:
                        text: parses kma, filters based on quality and output a text file with taxonomic information and detailed mapping information
                        visual: parses kma, filters based on quality and output a simplified text file and a krona html file for visualisation""", required=True)

parser.add_argument('-i', '--res_fp', help='Path to the KMA result (.res file)', required=True)
parser.add_argument('-o', '--output_fp', default = 'KMetagen_out', 
                    help='Path to the output file. Default = KMetagen_out', required=False)
parser.add_argument('-r', '--reference_database', default = 'ITS', 
                    help='Which reference database was used. Options: UNITE, RefSeq or nt. Default = UNITE', required=False)

parser.add_argument('-c', '--coverage', default = 20, 
                    help='Minimum coverage. Default = 20',type=int, required=False)
parser.add_argument('-q', '--query_identity', default = 50, 
                    help='Minimum query identity (Phyllum level). Default = 50', type=int, required=False)
parser.add_argument('-d', '--depth', default = 0.2,
                    help='Minimum sequencing depth. Default = 0.2.',type=int, required=False)
parser.add_argument('-p', '--pvalue', default = 0.05, 
                    help='Minimum p-value. Default = 0.05.',type=int, required=False)

# nt specific arguments:
parser.add_argument('-t', '--threads', default = 1, 
                    help='Number of threads. Default = 1.',type=int, required=False)
parser.add_argument('-a', '--acc_taxid_map', default = None, 
                    help='Path to the accession_taxid_nucl.map file.',required=False)



# what to do:
args = parser.parse_args()
mode = args.mode
f = args.res_fp
ref_database = args.reference_database
c = args.coverage
q = args.query_identity
d = args.depth
p = args.pvalue
acc_taxid_map=args.acc_taxid_map
th = args.threads

# developing and debugging:
#out_fp = "KMetagen_nt_results"
#f = "2_mtg_ITS.res"
#f = "6_mtg_test.res" 
#ref_database = "nt"
#mode = '1'
#c = 20
#q = 50
#d = 0.2
#p = 0.05
#acc_taxid_map="accession_taxid_test.map" 
#th = 1 # number of threads/cores to run when using the whole nt database


### If the reference database is nt, check that accession_taxid_nucl.map is given 
# and then produce the filtered accession to taxid mao:
if ref_database == "nt":
    if acc_taxid_map == None:
        print ("Error: You must specify the path to the accession_taxid_nucl.map file" )
        sys.exit()
        
    else:
            
        # random base name
        rb = str(random.randint(1000000,9999999))
            
        # extract accession numbers in one text file
        command = "awk '{print $1}' " + f + " > " + rb + "_accessions.temp"
        subprocess.run(command, shell=True) 
        
        # get a filtered accession 2 taxid map file
        fAcc2TaxId.filter_acc2taxid_map(f, acc_taxid_map, th, rb)

        # load it to memory (test)
        filtered_acc2_taxid_map = rb + "_acc2taxid_map_filtered.temp"
        with open(filtered_acc2_taxid_map) as a:
            acc2tax_dic = dict(x.rstrip().split(None, 1) for x in a)
            
# otherwse init non used variables
else:
    rb = None
    acc2tax_dic = None

##### Take as input individual .res files and output a file with tax info

if mode == 'text':
    
    print ("")
    print ("Reading file %s" %(f))
    print ("")
    
    df = pd.read_csv(f, sep='\t', index_col=0)

    # Rename headers:
    df.index.name = "Closest_match"
 
    # first quality filter (coverage, query identity, Depth and p-value)
    df = fParseKMA.res_filter(df, ref_database, c, q, d, p)
    
    # add tax info
#    df = fParseKMA.populate_w_tax(df, ref_database, acc2tax_dic, th, f, rb)
    df = fParseKMA.populate_w_tax(df, ref_database, acc2tax_dic = acc2tax_dic, threads = th, in_res_file = f, rb = rb)
      
    # save to file
    out = args.output_fp + ".csv"
    pd.DataFrame.to_csv(df, out)
    
    print ("csv file saved as %s" %(out))
    print ("")

##### Take as input individual .res files and output a Krona file 
if mode == 'visual':

    print ("")
    print ("Reading file %s" %(f))
    print ("")
    
    df = pd.read_csv(f, sep='\t', index_col=0)

    # Rename headers:
    df.index.name = "Match"
 
    # first quality filter (coverage, query identity, Depth and p-value)
    df = fParseKMA.res_filter(df, ref_database, c, q, d, p)
    
    # add tax info
    df = fParseKMA.populate_w_tax(df, ref_database, acc2tax_dic = acc2tax_dic,threads = th, in_res_file = f, rb = rb)


    krona_info = df[['Depth','Kingdom','Phylum','Class','Order','Genus','Species']]

    # save dataframe to file
    out1 = args.output_fp + ".tsv"
    pd.DataFrame.to_csv(krona_info, out1, sep='\t', index=False)
    
    # save krona file
    out2 = args.output_fp + ".html" 
    
    shell_command = "ktImportText " + out1 + " -o " + out2
    subprocess.run(shell_command, shell=True)

    print ("krona file saved as %s" %(out2))
    print ("")


##### Clean up temporary files:
if ref_database == "nt":
    fAcc2TaxId.cleanup(rb)

# remove .pyc/.pyo ?
    
    

    
    
    