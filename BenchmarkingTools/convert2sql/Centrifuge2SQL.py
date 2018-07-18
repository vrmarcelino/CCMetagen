#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script to convert Centrifuge report to SQL database

USAGE: Centrifuge2SQL.py -i mtt_refseq_bf_report.tsv -n 1_mtt -r RefSeq_bf -sql benchm.db

@ V.R.Marcelino
Created on Wed Jul 18 08:24:19 2018
"""

from argparse import ArgumentParser
import sqlite3
from ete3 import NCBITaxa
ncbi = NCBITaxa()
import cTaxInfo # script that define classes used here
import fNCBItax # script with function to get lineage from taxid
import csv

parser = ArgumentParser()
parser.add_argument('-i', '--input_centrifuge_report', help='The path to the centrifuge result', required=True)
parser.add_argument('-n', '--input_sample_name', help='Tthe name of the sample', required=True)
parser.add_argument('-r', '--reference_database', help='Reference database used, options are RefSeq_f_partial, RefSeq_bf and nt', required=True)
parser.add_argument('-sql', '--SQL_db', help='SQL database where it should store the data', required=True)

args = parser.parse_args()
in_res_file = args.input_centrifuge_report
ref_database = args.reference_database
sql_fp = args.SQL_db
sample_name = args.input_sample_name

# Tests and torubleshooting
#in_res_file = "mtg_nt_report.tsv"
#in_res_file = "2_mtg_ITS.txt"
#sql_fp="benchm.db"
#sample_name="2_mtg"
#ref_database = "RefSeq_bf"
#ref_database = "ITS"

############# 
connection = sqlite3.connect(sql_fp)
cursor = connection.cursor()

# Create a table if it does not exist:
# Note that Order is written with two 'O's, as Order is a sql command
query = """CREATE TABLE IF NOT EXISTS Centrifuge (TaxID integer, Lineage text, 
Sample text, RefDatabase text, Abundance real, Kingdom text,Kingdom_TaxId integer,
Phylum text, Phylum_TaxId integer, Class text, Class_TaxId integer, OOrder text,
Order_TaxId integer, Family text, Family_TaxId integer, Genus text, 
Genus_TaxId integer, Species text, Species_TaxId integer);"""

cursor.execute(query)
connection.commit()

#############

# Read and store taxids in list of classes
store_lineage_info = []

with open(in_res_file) as res:
    next (res) # skip first line
    for line in csv.reader(res, delimiter='\t'):

        match_info = cTaxInfo.TaxInfo()
        
        match_info.Lineage = line[0]

        match_info.TaxId = int(line[1])  
        match_info.Sample = sample_name
        match_info.RefDatabase = ref_database  
        
        # Abundance here is the number of unique reads, rather than 'abundance' form centrifuge
        # as there are usually not 30 species with abundance > 0.
        match_info.Abundance = int(line[5])
        
        # get Lineage info from NCBI
        match_info = fNCBItax.lineage_extractor(match_info.TaxId , match_info)

        store_lineage_info.append(match_info)      


# output as a SQLite3:
query = "INSERT INTO Centrifuge VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);"
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
print ("Table Centrifuge Table saved in %s sqlite3 database" %(sql_fp))
print ("")


