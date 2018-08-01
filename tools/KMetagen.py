#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
KMetagen main script

Version 0.1

@ V.R.Marcelino
Created on Wed Jul 25 17:13:10 2018

"""

# imports
import sys
import csv
import pandas as pd
from argparse import ArgumentParser
import os
from os import listdir
import re

# local imports
#import cTaxInfo
#import fNCBItax
import fParseKMA

# help
if len(sys.argv) == 1:
    print ("")
    print (" KMetagen - Metagenomic analyses")
    print ("")
    print ("Usage: KMetagen.py <options> ")
    print ("")
    print ("")
    sys.exit()


parser = ArgumentParser()

# change this to Requires = True!
parser.add_argument('-m', '--mode', help="""what do you want KMetagen to do? 
                    Valid options at the moment are: parse_kma""", required=False)

parser.add_argument('-i', '--res_fp', help='Path to the KMA result (.res file)', required=False)
parser.add_argument('-o', '--output_fp', default = 'KMetagen_out', 
                    help='Path to the output file. Default = KMetagen_out', required=False)
parser.add_argument('-r', '--reference_database', default = 'ITS', 
                    help='Which reference datbase was used. Default = ITS', required=False)


# what to do:
args = parser.parse_args()
#mode = args.mode


# debugging:
#out_fp = "06_TaxAssign/KMetagen"
#in_kma_folder_fp = "KMA_long_ctgs"
#ref_database = "ITS"

mode = 'parse_kma'

##### Take as input individual files and output a file with tax info
if mode == 'parse_kma':
    args = parser.parse_args()
    f = args.res_fp
    ref_database = args.reference_database
    
    df = pd.read_csv(f, sep='\t', index_col=0)

    # Rename headers:
    df.index.name = "Closest_match"
 
    # first quality filter:
    df = fParseKMA.res_filter(df, 20, 50, 0.2, 0.05)
    
    # add tax info
    df = fParseKMA.populate_w_tax(df, ref_database)
           
    # save to file
    out = args.output_fp + ".csv"
    pd.DataFrame.to_csv(df, out)
    


#### To do:
### Make output usable by KRONA!
    

















# check if flags are compatible, otherwise return a error?
# or does KMA will do that?



# funcions



    
    