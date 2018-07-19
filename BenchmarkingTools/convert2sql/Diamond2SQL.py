#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Parse the results of Diamond blast and store it in the SQLite3 'bench.db'

USAGE ex: python Diamond2SQL.py -i nanop_uniref90.txt -n 4_nanop -sql benchm.db -r UniProt

@ V.R.Marcelino
Created on Thu Jul 19 11:37:32 2018
"""

import re
from argparse import ArgumentParser
import sqlite3
from ete3 import NCBITaxa
ncbi = NCBITaxa()
import cTaxInfo # script that define classes used here
import fNCBItax # script with function to get lineage from taxid

parser = ArgumentParser()
parser.add_argument('-i', '--input_blastn_result', help='The path to the .txt file in tabular format', required=True)
parser.add_argument('-n', '--input_sample_name', help='Tthe name of the sample', required=True)
parser.add_argument('-r', '--reference_database', help='Reference database used, only option so far is UniProt', required=True)
parser.add_argument('-sql', '--SQL_db', help='SQL database where it should store the data', required=True)

args = parser.parse_args()
in_res_file = args.input_blastn_result
ref_database = args.reference_database
sql_fp = args.SQL_db
sample_name = args.input_sample_name


# Tests and torubleshooting
#in_res_file = "test_diamond.txt"
#sql_fp="benchm.db"
#sample_name="4_nanopg"
#ref_database = "UniProt"


############# 
connection = sqlite3.connect(sql_fp)
cursor = connection.cursor()

# Create a table if it does not exist:
# Note that Order is written with two 'O's, as Order is a sql command
query = """CREATE TABLE IF NOT EXISTS Diamond (TaxID integer, Lineage text, 
Sample text, RefDatabase text, Abundance real, Kingdom text,Kingdom_TaxId integer,
Phylum text, Phylum_TaxId integer, Class text, Class_TaxId integer, OOrder text,
Order_TaxId integer, Family text, Family_TaxId integer, Genus text, 
Genus_TaxId integer, Species text, Species_TaxId integer);"""

cursor.execute(query)
connection.commit()

#############
# Since Blast and Diamond output one line per read, we need to calculate the
# abundance of each hit. Skiping lineage (from match)

print ("calculating matches... takes a while for large files")

taxid_finder = re.compile(r'(?<=TaxID\=)(.*)(?= )')
taxids_dict = {}

with open(in_res_file) as res:
    for line in res:
        taxid = int(taxid_finder.findall(line)[0])
        
        # if taxid alreday there, add one to abundance
        if taxid in taxids_dict.keys():
            taxids_dict[taxid] = taxids_dict[taxid] + 1
            
        # iif not, add new item:
        else:
            taxids_dict[taxid] = 1
        


#############
# Read dict and store taxids in list of classes
print ("getting taxonomic information")
store_lineage_info = []

for key, value in taxids_dict.items():
    
    match_info = cTaxInfo.TaxInfo()

    match_info.TaxId = key
    
    try:
        match_info = fNCBItax.lineage_extractor(match_info.TaxId , match_info)
    
    except ValueError:
        print("Ooops! %i is not a valid taxid and will not be considered in the analysis" %(match_info.TaxId))
        
    match_info.Abundance = value
    match_info.Sample = sample_name
    match_info.RefDatabase = ref_database
    store_lineage_info.append(match_info)


#############

#### output as a SQLite3:
query = "INSERT INTO Diamond VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);"
for i in store_lineage_info:
    cursor.execute(query,(i.TaxId,i.Lineage,i.Sample,i.RefDatabase,i.Abundance,
                          i.Kingdom,i.Kingdom_TaxId,i.Phylum,i.Phylum_TaxId,
                          i.Class,i.Class_TaxId,i.Order,i.Order_TaxId,i.Family,
                          i.Family_TaxId,i.Genus,i.Genus_TaxId,i.Species,
                          i.Species_TaxId))
        
#### Save db
connection.commit()
connection.close()

print ("")
print ("Done!")
print ("Table Diamond saved in %s sqlite3 database" %(sql_fp))
print ("")





