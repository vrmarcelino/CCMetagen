#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
KMetagen_merge.py

Merge the abundance results of KMEtagen for several samples into a single table.
The results must be in .csv format (default KMEtagen or ---mode 1)
And no other csv file should be present in the folder

@ V.R.Marcelino
Created on Tue Dec 18 10:00:48 2018
"""

import sys
import csv
import pandas as pd 
from argparse import ArgumentParser
import os


parser = ArgumentParser()
parser.add_argument('-i', '--input_fp', help="""Path to the folder containing KMetagen text (.csv) results.
                    Note that the folder should not contain other .csv files""", required=True)
parser.add_argument('-t', '--tax_level', default = 'Species',
                    help="""Taxonomic level to merge the results. Options:
                    Closest_match (includes different genes for the same species),
                    Species (Default), Genus, Order, Class, Phylum and Kingdom
                    """, required=False)
parser.add_argument('-o', '--output_fp', default = 'merged_samples_abund.csv', 
                    help='Path to the output file. Default = merged_samples_abund.csv', required=False)


args = parser.parse_args()
in_folder = args.input_fp
tax_level = args.tax_level
output = args.output_fp

#in_folder = "KMetagen6"
#tax_level = "Genus"
#output = "merged_samples_depth.csv"


# create new dataframe:
all_samples = pd.DataFrame()


# read input files and merge results
for file in os.listdir(in_folder):
    if file.endswith("res.csv"):
        
        sample_name = file.split(".res.csv")[0]
        result_fp = os.path.join(in_folder, file)

        df = pd.read_csv(result_fp, sep=',', index_col=0)
        
        df = df.fillna("Unclassified")
        
        depth_by_tax = df.groupby(by=tax_level)["Depth"].sum()
        

        all_samples = pd.concat([all_samples, depth_by_tax.rename(sample_name)], sort=True, axis=1)
    

# name first row
all_samples.index.name = tax_level

# sort columns alphabetically
all_samples = all_samples.reindex(sorted(all_samples.columns), axis=1)

# Fill NaN with zeros:
all_samples = all_samples.fillna(0)

### Save
out = output + ".csv"
pd.DataFrame.to_csv(all_samples, out)

print ("Done. Abundance estimates for all samples saved as %s" %(out))


