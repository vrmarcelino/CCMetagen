#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Get a csv table with the mock communities info and convert it to a SQLite database
@ V.R.Marcelino
Created on Mon Jul 16 09:57:06 2018
"""
#import csv
import pandas as pd
import cTaxInfo # script that define classes used here
import fNCBItax # script with function to get lineage from taxid
import sqlite3



in_csv_fp="samples_info.csv"
fungi_csv = pd.read_csv(in_csv_fp)

sql_fp="benchm.db"


# store info in a list of objects
store_fungi_info = []

###### convert existing to cTaxInfo class abd include NCBI lineage info
for key, row in fungi_csv.iterrows():
    
    fungus = cTaxInfo.TaxInfo()
    
    fungus.Sample = row['Sample']
    fungus.Lineage = row['Lineage']
    fungus.TaxId = row['taxid']
    fungus.Covergae = row['Coverage']
    
    # include tax info from NCBI:
    fungus = fNCBItax.lineage_extractor(fungus.TaxId, fungus)
    
    store_fungi_info.append(fungus)
    

###### Add to SQL
connection = sqlite3.connect(sql_fp)
cursor = connection.cursor()

# Create a table if it does not exist:
# Note that Order is written with two 'O's, as Order is a sql command
query = """CREATE TABLE IF NOT EXISTS Fungi (Sample text, Lineage text,
Coverage float, TaxID integer, Superkingdom text, Superkingdom_TaxId integer,
Kingdom text, Kingdom_TaxId integer, Phylum text, Phylum_TaxId integer, 
Class text, Class_TaxId integer, OOrder text, Order_TaxId integer, Family text,
Family_TaxId integer, Genus text, Genus_TaxId integer, Species text, Species_TaxId integer);"""

cursor.execute(query)
connection.commit()

# output as a SQLite3:
query = "INSERT INTO Fungi VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);"
for i in store_fungi_info:
    cursor.execute(query,(i.Sample,i.Lineage,i.Coverage,i.TaxId,
                          i.Superkingdom, i.Superkingdom_TaxId,i.Kingdom,
                          i.Kingdom_TaxId,i.Phylum,i.Phylum_TaxId,i.Class,
                          i.Class_TaxId,i.Order,i.Order_TaxId,i.Family,
                          i.Family_TaxId,i.Genus,i.Genus_TaxId,i.Species,
                          i.Species_TaxId))


# Save db
connection.commit()
connection.close()
