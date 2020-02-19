#!/usr/bin/env python3
"""
CCMetagen_merge.py

Merge the abundance results of CCMetagen for several samples into a single table.
The results must be in .csv format (default CCMetagen or ---mode text)
And no other csv file should be present in the folder

USAGE example 1: Merge table at family level:
CCMetagen_merge.py -i CCMetagen_folder -t Family

USAGE example 2: Merge table by species (default) and keep only Cryptococcus and Candida:
CCMetagen_merge.py -i CCMetagen_folder -kr k -l Genus -tlist Candida,Cryptococcus

@ V.R.Marcelino
Created on Tue Dec 18 10:00:48 2018
"""

import sys
import pandas as pd
from argparse import ArgumentParser
import os


parser = ArgumentParser()
parser.add_argument('-i', '--input_fp', help="""Path to the folder containing CCMetagen text results.
                    Note that files must end with ".csv"
                    and the folder should not contain other .csv files""", required=True)
parser.add_argument('-t', '--tax_level', default = 'Species',
                    help="""Taxonomic level to merge the results. Options:
                    Closest_match (includes different genes for the same species),
                    Species (Default), Genus, Family, Order, Class, Phylum, Kingdom and Superkingdom
                    """, required=False)
parser.add_argument('-o', '--output_fp', default = 'merged_samples',
                    help='Path to the output file. Default = merged_samples', required=False)

# arguments to filter by taxonomy:
parser.add_argument('-kr', '--keep_or_remove', default = 'n',
                    help='keep or remove taxa. Options = k (keep), r (remove) and n (none, default)', required=False)

parser.add_argument('-l', '--filtering_tax_level', default = 'none',
                    help='level to perform taxonomic filtering, default = none', required=False)

parser.add_argument('-tlist', '--taxa_list', default = [], type=str,
                    help='list taxon names (comma-separated) that you want to keep or exclude', required=False)

args = parser.parse_args()
in_folder = args.input_fp
tax_level = args.tax_level
output = args.output_fp
kr = args.keep_or_remove


# debugging:
#in_folder = "CCMetagen_new"
#tax_level = "Species"
#output = "merged_samples_depth"
#kr = "n" # k for keep, r for remove, and n for none
#level = "Species"
#taxa = ["Escherichia coli"]


# Set the taxonomic levels to retain info:
l = ['Superkingdom','Kingdom','Phylum','Class','Order','Family','Genus','Species','Closest_match']

f4agg = {}

f4agg['Depth']= 'sum'
for i in l:
    if i == tax_level:
        f4agg[i] = 'first'
        break
    else:
        f4agg[i] = 'first'

# list of wanted taxa (no depth):
wanted_taxa = list(f4agg.keys())
wanted_taxa.remove('Depth')

# create new dataframe:
all_samples = pd.DataFrame()


# read input files and merge results
for file in os.listdir(in_folder):
    if file.endswith(".csv"):

        sample_name = file.split(".csv")[0]
        result_fp = os.path.join(in_folder, file)

        df = pd.read_csv(result_fp, sep=',', index_col=0)

        # this is needed because groupby excludes rows with NAs
        df = df.fillna("NA")

        # keep or remove taxa:
        if kr == "k":
            level = args.filtering_tax_level
            taxa = args.taxa_list.split(",")
            filt_df_str = "df[df['{}'].isin({})]".format(level,taxa)
            df = eval(filt_df_str)

        elif kr == "r":
            level = args.filtering_tax_level
            taxa = args.taxa_list.split(",")
            filt_df_str = "df[~df['{}'].isin({})]".format(level,taxa)
            df = eval(filt_df_str)
        elif kr == "n":
            pass
        else:
            print ("kr must be k (keep), r (remove) or n (none).")
            sys.exit("Try again.")

        # if tax_level = closest_match, we need an extra column:
        # Note that this will raise an ambiguity error in a future version of Pandas.
        if tax_level == 'Closest_match':
            df['Closest_match'] = df.index

        depth_by_tax = df.groupby(by=wanted_taxa).agg(f4agg)
        depth_by_tax.rename(columns={'Depth':sample_name}, inplace=True)

        all_samples = pd.concat([all_samples, depth_by_tax], sort=True, axis=1)


# Group taxon ranks
all_samples = all_samples.groupby(by=all_samples.columns, axis = 1).first()

# add taxon info at the end of the table:
tax_cols_l = list(f4agg.keys())
tax_cols_l.remove('Depth')

tax_cols = all_samples[tax_cols_l]
sample_cols = all_samples.drop(columns=tax_cols_l)

all_samples = pd.merge(sample_cols,tax_cols,left_index=True,right_index=True)

# Fill NaN with zeros:
all_samples = all_samples.fillna(0)

# Remove the artificially added NAs:
all_samples = all_samples.replace(["NA"], value = "")


### Save
out = output + ".csv"
pd.DataFrame.to_csv(all_samples, out, index=False)

print ("Done. Abundance estimates for all samples saved as %s" %(out))


