#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Parse the results of 1 KMA res file and store them in the SQLite3 'bench.db'
Works for ITS, RefSeq and UniProt, get their taxids and lineages (as identified in the Ref Database)
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
parser.add_argument('-r', '--reference_database', help='Reference database used, options are ITS, RefSeq, UniProt and nt', required=True)
parser.add_argument('-sql', '--SQL_db', help='SQL database where it should store the data', required=True)

args = parser.parse_args()
in_res_file = args.input_kma_result
ref_database = args.reference_database
sql_fp = args.SQL_db
sample_name = args.input_sample_name


# Tests and torubleshooting
ref_database = "ITS" # options are ITS, RefSeq or UniProt
in_res_file = "2_mtg_ITS.res"
#in_res_file_RefSeq = "2_mtg_refSeq_bf.spa"
sql_fp="benchm.db"
sample_name="mtg"

############# 
connection = sqlite3.connect(sql_fp)
cursor = connection.cursor()

# Create a table if it does not exist:
query = "CREATE TABLE IF NOT EXISTS KMA (TaxID integer, Lineage text, Sample text, RefDatabase text, Abundance text);"
cursor.execute(query)
connection.commit()

#############



# Read and store taxids in list of classes
store_lineage_info = []

# function with the following inputs
# in_res_file, sample, database,

with open(in_res_file) as res:
    next (res) # skip first line
    for line in csv.reader(res, delimiter='\t'):      
        split_match = re.split (r'(\|| )', line[0])

        match_info = cTaxInfo.TaxInfo()
        
        if ref_database == "ITS":
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

        elif ref_database == "RefSeq":
            match_info.TaxId = split_match[4]
            species = split_match[6] + " " + split_match[8]
            match_info.Lineage = species
            # include info from NCBI:
            match_info = fNCBItax.lineage_extractor(match_info.TaxId, match_info)
        
        elif ref_database == "UniProt":
            print("write something to search after TaxID=")
            
        elif ref_database == "nt":
            print("write something to search for taxid based on species name")
            
        else:
            print ("ref_database must be ITS, RefSeq, UniProt or nt")

        
        Abund = line[-3].split(' ')[-1] # Raw 'Depth' value
        match_info.Abundance = Abund
        match_info.Sample = sample_name
        match_info.RefDatabase = ref_database
        store_lineage_info.append(match_info)


# output as a SQLite3:
query = "INSERT INTO KMA VALUES (?,?,?,?,?);"
for i in store_lineage_info:
    cursor.execute(query,(i.TaxId, i.Lineage, i.Sample, i.RefDatabase, i.Abundance))
    
# Save db    
connection.commit()
connection.close()

#################
#check it is all right
for i in store_lineage_info:
    print (i.TaxId)
    print (i.Lineage)
    print (i.Sample)
    print (i.RefDatabase)
    print (i.Abundance)
    print (i.Family)

for i in store_lineage_info:
    if i.TaxId == 'unk_taxid':
        print (i.TaxId)
        print (i.Lineage)
        
        

cursor.execute("SELECT * FROM KMA;")
cursor.fetchall()





