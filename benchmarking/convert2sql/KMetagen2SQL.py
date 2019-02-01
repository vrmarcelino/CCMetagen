#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Parse the results of 1 KMetagen csv file and store them in the SQLite3 'bench.db'

USAGE ex: python KMetagen2SQL.py -i 2_mtg_ITS.res -n mtg -r UNITE -sql benchm.db


@ V.R.Marcelino
Created on 29 Dec 2018
"""

import csv
import re
from argparse import ArgumentParser
import sqlite3
import pandas as pd
from ete3 import NCBITaxa
import numpy # check for NaN

ncbi = NCBITaxa()
import cTaxInfo # script that define classes used here
import fNCBItax # script with function to get lineage from taxid

parser = ArgumentParser()
parser.add_argument('-i', '--input_KMetagen_result', help='The path to the .res or .spa file', required=True)
parser.add_argument('-n', '--input_sample_name', help='Tthe name of the sample', required=True)
parser.add_argument('-r', '--reference_database', help='Reference database used, options are UNITE, RefSeq_f_partial and RefSeq_bf', required=True)
parser.add_argument('-sql', '--SQL_db', help='SQL database where it should store the data', required=True)

args = parser.parse_args()
in_res_file = args.input_KMetagen_result
ref_database = args.reference_database
sql_fp = args.SQL_db
sample_name = args.input_sample_name


# Tests and torubleshooting
#ref_database = "RefSeq"
#in_res_file = "output_2mtg_RefSeq.csv"
#in_res_file = "KMetagen_result_2mtg_sparse.csv"
#sql_fp="benchm.db"
#sample_name="2_mtg"

############# 
connection = sqlite3.connect(sql_fp)
cursor = connection.cursor()

# Create a table if it does not exist:
# Note that Order is written with two 'O's, as Order is a sql command
query = """CREATE TABLE IF NOT EXISTS KMetagen (TaxID integer, Lineage text, 
Sample text, RefDatabase text, Abundance real, Kingdom text,Kingdom_TaxId integer,
Phylum text, Phylum_TaxId integer, Class text, Class_TaxId integer, OOrder text,
Order_TaxId integer, Family text, Family_TaxId integer, Genus text, 
Genus_TaxId integer, Species text, Species_TaxId integer);"""


cursor.execute(query)
connection.commit()

#############


# Read and store taxids in list of classes
store_lineage_info = []


# read Kmetagen as a pandas dataframe:
df = pd.read_csv(in_res_file, sep=',', index_col=0)

# loop through db and store relevant info
for index, row in df.iterrows():
    
    #start class tax info
    match_info = cTaxInfo.TaxInfo()
    
    match_info.Lineage = index
    match_info.Abundance = row['Depth']
    
    match_info.Sample = sample_name
    match_info.RefDatabase = ref_database
    
    if numpy.isnan(row['LCA_TaxId']) == False:
        match_info.TaxId = int(row['LCA_TaxId'])
        match_info = fNCBItax.lineage_extractor(match_info.TaxId , match_info)
    
    else:
        print ("")
        print ("WARNING: no taxid found for %s" %(match_info.Lineage))
        print ("This match will not get the NCBItax lineage information")
        print ("and will not be included in the analyses.")
        print ("")
        match_info.TaxId = 'unk_taxid'

    store_lineage_info.append(match_info)

        

# output as a SQLite3:
query = "INSERT INTO KMetagen VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);"
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
print ("Table KMetagen saved in %s sqlite3 database" %(sql_fp))
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
