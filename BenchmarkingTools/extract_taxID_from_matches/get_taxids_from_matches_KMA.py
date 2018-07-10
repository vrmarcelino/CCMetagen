#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Parse the results of KMA res files 
works for ITS, RefSeq and UniProt, get their taxids and species
@ V.R.Marcelino
Created on Tue Jul 10 17:12:08 2018
"""

import csv
import re
from argparse import ArgumentParser


parser = ArgumentParser()
parser.add_argument('-i', '--input_kma_result', help='The path to the .res or .spa file', required=True)
parser.add_argument('-r', '--reference_database', help='Reference database used, options are ITS, RefSeq or UniProt', required=True)
parser.add_argument('-o', '--output', help='output file path', required=True)

args = parser.parse_args()
in_res_file = args.input_kma_result
ref_database = args.reference_database
output_fp = args.output



#ref_database = "ITS" # options are ITS, RefSeq or UniProt
#in_res_file_ITS = "2_mtg_ITS.res"
#in_res_file_RefSeq = "2_mtg_refSeq_bf.spa"

# class that stores taxid and other info
class tax_info_storage(): 
    def __init__(self, taxid=None, lineage=None):
        self.taxid = taxid
        self.lineage = lineage

# Read and store taxids in list of classes
store_lineage_info = []
with open(in_res_file) as res:
    next (res) # skip first line
    for line in csv.reader(res):
        split_match = re.split (r'(\|| )', line[0])
        
        match_info = tax_info_storage()
        if ref_database == "ITS":
            match_info.taxid = split_match[4]
            match_info.lineage = split_match[12]
        
        elif ref_database == "RefSeq":
            match_info.taxid = split_match[4]
            species = split_match[6] + " " + split_match[8]
            match_info.lineage = species
        
        elif ref_database == "UniProt":
            print("write something to search after TaxID=")
            
        else:
            print ("ref_database must be ITS, RefSeq or UniProt")

        store_lineage_info.append(match_info)


#check it is all right
for i in store_lineage_info:
    print (i.taxid)
    print (i.lineage)

# output as a SQLite3 or .csv?


    







