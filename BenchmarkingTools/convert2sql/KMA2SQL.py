#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Parse the results of 1 KMA res file and store them in the SQLite3 'bench.db'
Works for UNITE, RefSeq and UniProt, get their taxids and lineages (as identified in the Ref Databases)

USAGE ex: python KMA2SQL.py -i 2_mtg_ITS.res -n mtg -r ITS -sql benchm.db

### ONLY ITS and RefSeq Working at the moment!!!


@ V.R.Marcelino
Created on Tue Jul 10 17:12:08 2018
"""

import csv
import re
from argparse import ArgumentParser
import sqlite3
from ete3 import NCBITaxa
ncbi = NCBITaxa()
import cTaxInfo # script that define classes used here
import fNCBItax # script with function to get lineage from taxid

parser = ArgumentParser()
parser.add_argument('-i', '--input_kma_result', help='The path to the .res or .spa file', required=True)
parser.add_argument('-n', '--input_sample_name', help='Tthe name of the sample', required=True)
parser.add_argument('-r', '--reference_database', help='Reference database used, options are UNITE, RefSeq_f_partial, RefSeq_bf, UniProt and nt', required=True)
parser.add_argument('-sql', '--SQL_db', help='SQL database where it should store the data', required=True)

args = parser.parse_args()
in_res_file = args.input_kma_result
ref_database = args.reference_database
sql_fp = args.SQL_db
sample_name = args.input_sample_name


# Tests and torubleshooting
#ref_database = "UNITE" # options are UNITE, RefSeq or UniProt
#in_res_file = "2_mtg_ITS.res"
#in_res_file_RefSeq = "2_mtg_refSeq_bf.spa"
#sql_fp="benchm.db"
#sample_name="mtg"

############# 
connection = sqlite3.connect(sql_fp)
cursor = connection.cursor()

# Create a table if it does not exist:
# Note that Order is written with two 'O's, as Order is a sql command
query = """CREATE TABLE IF NOT EXISTS KMA (TaxID integer, Lineage text, 
Sample text, RefDatabase text, Abundance real, Kingdom text,Kingdom_TaxId integer,
Phylum text, Phylum_TaxId integer, Class text, Class_TaxId integer, OOrder text,
Order_TaxId integer, Family text, Family_TaxId integer, Genus text, 
Genus_TaxId integer, Species text, Species_TaxId integer);"""


cursor.execute(query)
connection.commit()

#############


# Read and store taxids in list of classes
store_lineage_info = []

# loop with the following inputs
# in_res_file, sample, database,

with open(in_res_file) as res:
    next (res) # skip first line
    for line in csv.reader(res, delimiter='\t'):      
        split_match = re.split (r'(\|| )', line[0])

        match_info = cTaxInfo.TaxInfo()
        
        if ref_database == "UNITE":
            match_info.Lineage = split_match[12]
            
            if split_match[4] != 'unk_taxid':
                
                match_info.TaxId = int(split_match[4])
                match_info = fNCBItax.lineage_extractor(match_info.TaxId , match_info)
                
            # Handle unknown taxids: 
            else:
                full_lin = split_match[12]
                species_full_name = full_lin.split('_')[-2:]
                species_name_part2 = species_full_name[1].replace('sp', 'sp.')
                species_name = species_full_name[0] + " " + species_name_part2
                
                # get taxid from species name
                retrieved_taxid = ncbi.get_name_translator([species_name])
                
                # if found, add to class object
                if len(retrieved_taxid) != 0:
                    match_info.TaxId = retrieved_taxid[species_name][0]
                    match_info = fNCBItax.lineage_extractor(match_info.TaxId, match_info)
        
                # if unkwnon, try with genus only:
                else:
                    retrieved_taxid = ncbi.get_name_translator([species_full_name[0]])
                    
                    # if found, add to class object
                    if len(retrieved_taxid) != 0:
                        match_info.TaxId = retrieved_taxid[species_full_name[0]][0]
                        match_info = fNCBItax.lineage_extractor(match_info.TaxId, match_info)
                
                    # if still not found, print warning
                    else:
                        print ("")
                        print ("WARNING: no taxid found for %s" %(full_lin))
                        print ("this match will not get the NCBItax lineage information")
                        print ("and will not be included in the analyses")
                        print ("")
                        match_info.TaxId = split_match[4] # 'unk_taxid'
                        match_info.Lineage = split_match[12] # lineage from ITS - Unite db only.

        elif ref_database == "RefSeq_f_partial" or ref_database == "RefSeq_bf":
            match_info.TaxId = split_match[4]
            species = split_match[6] + " " + split_match[8]
            match_info.Lineage = species
            # include info from NCBI:
            match_info = fNCBItax.lineage_extractor(match_info.TaxId, match_info)
                   
        elif ref_database == "nt":
            print("write something to search for taxid based on species name")
            
        else:
            print ("ref_database must be UNITE, RefSeq_f_partial, RefSeq_bf or nt")

        
        Abund = line[-3].split(' ')[-1] # Raw 'Depth' value
        match_info.Abundance = float(Abund)
        match_info.Sample = sample_name
        match_info.RefDatabase = ref_database
        store_lineage_info.append(match_info)


# output as a SQLite3:
query = "INSERT INTO KMA VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);"
for i in store_lineage_info:
    cursor.execute(query,(i.TaxId,i.Lineage,i.Sample,i.RefDatabase,i.Abundance,
                          i.Kingdom,i.Kingdom_TaxId,i.Phylum,i.Phylum_TaxId,
                          i.Class,i.Class_TaxId,i.Order,i.Order_TaxId,i.Family,
                          i.Family_TaxId,i.Genus,i.Genus_TaxId,i.Species,
                          i.Species_TaxId))
        

# Save db
connection.commit()
connection.close()

print ("")
print ("Done!")
print ("Table KMA saved in %s sqlite3 database" %(sql_fp))
print ("")

#################
#check it is all right
#for i in store_lineage_info:
#    print (i.TaxId)
#    print (i.Lineage)
#    print (i.Sample)
#    print (i.RefDatabase)
#    print (i.Abundance)
#    print (i.Family)

#for i in store_lineage_info:
#    if i.TaxId == 'unk_taxid':
#        print (i.TaxId)
#        print (i.Lineage)
        

