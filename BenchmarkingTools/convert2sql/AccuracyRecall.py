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
TaxRank="Species"


###### Open database:
connection = sqlite3.connect(sql_fp)
cursor = connection.cursor()

# Create new Results database
# Note that Order is written with two 'O's, as Order is a sql command
query = """CREATE TABLE IF NOT EXISTS Results{} (Approach text, Sample text,
RefDatabase text, TruePos integer, FalsePos integer, Recall float, Accuracy float);""".format(TaxRank)

cursor.execute(query)
connection.commit()

##########################

### Class to store info that goes in the Results tables # script
class results_info():
     def __init__(self, Approach=None,Sample=None,RefDatabase=None,
                  TruePos=None,FalsePos=None,Recall=None,Accuracy=None):
         
         self.Approach = Approach
         self.Sample = Sample
         self.RefDatabase = RefDatabase
         self.TruePos = TruePos
         self.FalsePos = FalsePos
         self.Recall = Recall
         self.Accuracy = Accuracy



#### Function to produce query that gets True Positives # script
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
    print("")
    return query


### Function to produce query that gets False Positives # script
# Ignore where Species_Taxid is null
def query4falses(approach,sample,taxLevel,query4trues):
        
    variables=(approach,taxLevel,approach,approach,taxLevel,query4trues,
               approach,sample,approach,taxLevel)
   
    query = """
    SELECT DISTINCT {}.{}_TaxID
    FROM {}
    WHERE {}.{}_TaxID NOT IN 
    ({})
    AND {}.Sample='{}'
    AND {}.{}_TaxID IS NOT NULL;""".format(*variables)
    
    print (query)
    print("")
    return query   

### Function that calculates the total number of matches for a given sample
# ad tax. level
def query4total(approach,sample,taxLevel):
    
    variables = (taxLevel,approach,sample,taxLevel)
    query = """SELECT count(DISTINCT {}_taxID) 
    FROM {} 
    WHERE Sample='{}'
    AND {}_taxID IS NOT NULL;""".format(*variables)
    print (query)
    print("")
    return query
    
### function that calculates the total number of <species> (or any tax level)
# in a given sample
def query4taxIn (sample,taxLevel):
    
    variables = (taxLevel,sample)
    query = """SELECT COUNT(DISTINCT {}_TAxID) 
    FROM FUNGI 
    WHERE SAMPLE='{}';""".format(*variables)
    print (query)
    print("")
    return query



##########################

# Get a list of all samples + RefDatabases available in benchm.db:

store_results = []

approaches = ['KMA', 'BLASTn']


for apr in approaches:
    query="""SELECT DISTINCT Sample, RefDatabase FROM {};""".format(apr)
    cursor.execute(query)
    samp_refdb = cursor.fetchall()
    
    for i in samp_refdb:
        row = results_info()
        row.Approach = apr
        row.Sample = i[0]
        row.RefDatabase = i[1]
        
        # Get true positives:
        queryT = query4trues(row.Approach,row.Sample,TaxRank)
        cursor.execute(queryT)
        row.TruePos = len(cursor.fetchall())
        
        # Get false positives:
        queryT = queryT.replace(";","")
        queryF = query4falses(row.Approach,row.Sample,TaxRank,queryT)
        cursor.execute(queryF)
        row.FalsePos = len(cursor.fetchall())
        
        # check if TruePos + FalsePos match the total:
        queryT = query4total(row.Approach,row.Sample,TaxRank)
        cursor.execute(queryT)
        total_matches = cursor.fetchall()[0][0]
        
        if row.TruePos + row.FalsePos != total_matches:
            print ("")
            print ("Warning, TruePos + FalsePos do not match the total")
            print ("something is missing!")
            print("")
        
        # Calc recall (% of the input that were recivered within true positives)
        queryR = query4taxIn(row.Sample,TaxRank)
        cursor.execute(queryR)
        total_input = cursor.fetchall()[0][0]
        row.Recall = row.TruePos * 100 / total_input

        # Calc accuracy (% from all matches that are true positives)
        row.Accuracy = row.TruePos * 100  / total_matches
      
        store_results.append(row)
    
    
for i in store_results:
    print (i.TruePos)
    print (i.Recall)
    print (i.Accuracy)










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
