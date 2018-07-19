#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Parse the results of 1 KrakenHLL result and store it in the SQLite3 'bench.db'

USAGE ex: python KrakenHLL2SQL.py -i 1_mtt_refseq_f_partial.tsv -n 1_mtt -sql benchm.db -r RefSeq_f_partial

@ V.R.Marcelino
Created on Thu Jul 19 11:06:33 2018
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
parser.add_argument('-r', '--reference_database', help='Reference database used, options are RefSeq_f_partial and RefSeq_bf', required=True)
parser.add_argument('-sql', '--SQL_db', help='SQL database where it should store the data', required=True)

args = parser.parse_args()
in_res_file = args.input_centrifuge_report
ref_database = args.reference_database
sql_fp = args.SQL_db
sample_name = args.input_sample_name

# Tests and torubleshooting
#in_res_file = "1_mtt_refseq_f_partial.tsv"
#sql_fp="benchm.db"
#ref_database = "RefSeq_f_partial"
#sample_name="1_mtt"


############# 
connection = sqlite3.connect(sql_fp)
cursor = connection.cursor()

# Create a table if it does not exist:
# Note that Order is written with two 'O's, as Order is a sql command
query = """CREATE TABLE IF NOT EXISTS KrakenHLL (TaxID integer, Lineage text, 
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
        
        match_info.Lineage = line[8]

        match_info.Sample = sample_name
        match_info.RefDatabase = ref_database  
        
        # Relative abundance
        match_info.Abundance = float(line[0])
        
        # get Lineage info from NCBI
        match_info.TaxId = int(line[6])

        if match_info.TaxId != 0:
            match_info = fNCBItax.lineage_extractor(match_info.TaxId , match_info)

        else:
            print ("Note: %i percent of the reads were unclassified." %(match_info.Abundance))

        store_lineage_info.append(match_info)      


# output as a SQLite3:
query = "INSERT INTO KrakenHLL VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);"
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
print ("Table KrakenHLL Table saved in %s sqlite3 database" %(sql_fp))
print ("")





#for i in store_lineage_info:
#    print (i.Species)
#    print (i.Class)
#    print (i.Order)


