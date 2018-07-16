#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script to assess the accuracy and recall of the different programs
@ V.R.Marcelino
Created on Mon Jul 16 11:29:09 2018
"""

import sqlite3
from argparse import ArgumentParser

parser = ArgumentParser()
parser.add_argument('-sql', '--SQL_db', help='SQL database to nake comparisons', required=True)

args = parser.parse_args()

#sql_fp = args.SQL_db
sql_fp="benchm.db"


###### Open database:
connection = sqlite3.connect(sql_fp)
cursor = connection.cursor()

# Create new Results database - Species
# Note that Order is written with two 'O's, as Order is a sql command
query = """CREATE TABLE IF NOT EXISTS ResultsSpecies (Approach text, Sample text,
RefDatabase text, TruePos integer, FalsePos integer, Recall float, Accuracy float);"""

cursor.execute(query)
connection.commit()

#############




# Each sample and program correspond to one row, then check accuracy and recall

# True Positives from KMA, ITS, 2_mtg
# Ignore where Species_Taxid is null
query = """
SELECT DISTINCT KMA.Species_TaxID
FROM KMA
INNER JOIN FUNGI ON KMA.Species_TaxID = Fungi.Species_TaxID
WHERE Fungi.SAMPLE='2_mtg' AND KMA.Sample='2_mtg'
AND KMA.Species_TaxID IS NOT NULL;
"""

cursor.execute(query)
results = cursor.fetchall()
n_tre_pos = len(results)
n_tre_pos
# 15

# False Positives from KMA, ITS, 2_mtg
# Ignore where Species_Taxid is null
query = """
SELECT DISTINCT KMA.Species_TaxID, KMA.Species
FROM KMA
LEFT JOIN FUNGI ON KMA.Species_TaxID = Fungi.Species_TaxID
WHERE Fungi.Species_TaxID IS NULL
AND KMA.Sample='2_mtg'
AND KMA.Species_TaxID IS NOT NULL;
"""
cursor.execute(query)
results = cursor.fetchall()
len(results)

n_false_pos = len(results) # 191

### Sum of matches
# Check if it correpsonds to the sum of the true positives and false positives
query = "SELECT count(DISTINCT Species_taxID) from KMA WHERE Sample='2_mtg';"
cursor.execute(query)
cursor.fetchall()



## test with variables
var_inputs=('KMA', 'KMA', 'KMA', 'KMA', '2_mtg', 'KMA')

query = """SELECT DISTINCT {}.Species_TaxID
FROM {}
LEFT JOIN FUNGI ON {}.Species_TaxID = Fungi.Species_TaxID
WHERE Fungi.Species_TaxID IS NULL
AND {}.Sample='{}'
AND {}.Species_TaxID IS NOT NULL;
""".format(*var_inputs)
cursor.execute(query)
len(cursor.fetchall())



##### Function to produce query that gets False Positives
# Ignore where Species_Taxid is null
def query4falses(approach,sample,taxLevel):
    
    variables=(approach,taxLevel,approach,approach,taxLevel,taxLevel,
               taxLevel,approach,sample,approach,taxLevel)
    
    query = """SELECT DISTINCT {}.{}_TaxID
    FROM {}
    LEFT JOIN FUNGI ON {}.{}_TaxID = Fungi.{}_TaxID
    WHERE Fungi.{}_TaxID IS NULL
    AND {}.Sample='{}'
    AND {}.{}_TaxID IS NOT NULL;""".format(*variables)
    
    print (query)
    
    return query


##### Function to produce query that gets True Positives
# Ignore where Species_Taxid is null
def query4trues(approach,sample,taxLevel):
        
    variables=(approach,taxLevel,approach,approach,taxLevel,taxLevel,
               sample,approach,sample,approach,taxLevel)
    
    query = """
    SELECT DISTINCT {}.{}_TaxID
    FROM {}
    INNER JOIN FUNGI ON {}.{}_TaxID = Fungi.{}_TaxID
    WHERE Fungi.SAMPLE='{}' AND {}.Sample='{}'
    AND {}.{}_TaxID IS NOT NULL;""".format(*variables)
    
    print (query)
    
    return query





query = query4falses('KMA','2_mtg','Species')
cursor.execute(query)
n_false_pos = len(cursor.fetchall())
n_false_pos

query = query4trues('KMA','2_mtg','Species')
cursor.execute(query)
n_true_pos = len(cursor.fetchall())
n_true_pos








### test with row factory

row_factory = sqlite3.Row
connection.row_factory = sqlite3.Row
cursor = connection.cursor()
#do something, then:
cursor.execute(query)
results = cursor.fetchall()
res=cursor.fetchone()
res['Species']
res['Species_TaxID']




cursor.execute(query)
len(cursor.fetchall())




header=['id', 'name', 'taxid']
stmt = """ SELECT {} FROM {} WHERE ...""".format(','.join([x for x in header]), 'tablename')


# """SELECT DISTINT  FROM {} ......""".format()
con.row_factory = sqlite3.Row

cursor.execute(query,(["KMA.Species_TaxID", "KMA"]))
#results = cursor.fetchall()
for row in cursor:
    print(row)
len(results)


tup=tuple(["KMA.Species_TaxID"])





#### Save db
connection.commit()
connection.close()
