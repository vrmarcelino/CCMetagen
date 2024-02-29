#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Script to extract sequence reads (or contigs) assigned to a given taxon.

Created on Wed Jun 10 19:37:36 2020.

@author: V.R.Marcelino
"""


# imports

import sys
import pandas as pd
import csv
from argparse import ArgumentParser


# help
if len(sys.argv) == 1:
    print("")
    print(
        """Produces a fasta file containing the sequences assigned to a given taxon"""
    )
    print("For help and options, type: CCMetagen_extract_seqs.py -h")
    print("")


parser = ArgumentParser()
parser.add_argument(
    "-ifrag",
    "--input_frags",
    help="The path to the file containing frags (decompressed)",
    required=True,
)
parser.add_argument(
    "-iccm",
    "--input_ccmetagen",
    help="The path to the ccmetagen result csv file",
    required=True,
)
parser.add_argument(
    "-l",
    "--taxonomic_level",
    help="""Taxonomic level to merge the results. Options:
                    Species, Genus, Family, Order, Class, Phylum, Kingdom and Superkingdom""",
    required=True,
)
parser.add_argument(
    "-t",
    "--taxon",
    help="""Taxon for which you want to extract sequences. 
                    Use quotation marks to specify species (e.g. -t 'Escherichia coli')""",
    required=True,
)
parser.add_argument(
    "-o",
    "--output_fp",
    default="wanted_taxon_seqs",
    help="Path to the output file. Default = wanted_taxon_seqs",
    required=False,
)


args = parser.parse_args()
frags_fp = args.input_frags
iccm = args.input_ccmetagen
tax_level = args.taxonomic_level
tax_name = args.taxon
o_file = args.output_fp + ".fas"


# developing and debugging:
# frags_fp = "test2.frag"
# iccm = "/test2_CCMetagen_nt_results.csv"
# tax_name = "Aspergillaceae"
# tax_level = "Family"
# o_file = "wanted_seq.fas"

## Get a list for all Closest_match where <tax_rank> == <tax_name>:
df = pd.read_csv(iccm, sep=",", index_col=0)

wanted_df = df[df[tax_level].str.match(tax_name).fillna(False)]


# Then extract sequences for that taxon.
ofile_good = open(o_file, "w")

cg = 0  # count good reads
with open(frags_fp) as frags:
    for line in csv.reader(frags, delimiter="\t"):
        match = line[5]
        seq_id = line[6]
        seq_read = line[0]

        if match in wanted_df.index.values:
            ofile_good.write(">" + seq_id + "\n" + seq_read + "\n")
            cg += 1

ofile_good.close()

print("")
print("Done.")
print(
    "%i sequences classified as %s were saved in the %s file." % (cg, tax_name, o_file)
)
print("Forward and reverse reads were saved to the same file")
print("")
