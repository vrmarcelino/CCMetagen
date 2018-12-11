#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script to assess the accuracy and recall of the different programs

USAGE: python AccuracyRecall.py -tr Species -sql benchm.db -o Res_species.csv
    
@ V.R.Marcelino
Created on Mon Jul 16 11:29:09 2018
Modified - 30 Nov 2018
"""

import sqlite3
from argparse import ArgumentParser
import cResInfo # custom classes used here
import fQueries # custom functions used here
import csv

parser = ArgumentParser()
parser.add_argument('-sql', '--SQL_db', help='SQL database to make comparisons', required=True)
parser.add_argument('-tr', '--TaxRank', help='TaxRank to perform the analyses', required=True)
parser.add_argument('-o', '--output_csv', help='output file path', required=False)


args = parser.parse_args()
sql_fp = args.SQL_db
TaxRank = args.TaxRank
sql2csv = args.output_csv

# editing and debugging
#sql_fp="benchm.db"
#TaxRank="Species"
#sql2csv="Res_species.csv"

approaches = ['KMetagen', 'KMA', 'Centrifuge', 'KrakenHLL','Kraken2'] # approaches ot be analysed


print ("")
print ("running ... ")
print ("")



#### Open database:
connection = sqlite3.connect(sql_fp)
cursor = connection.cursor()

#### Loop through approaches and add all info to benchm.db:

store_results = []

for apr in approaches:
    query="""SELECT DISTINCT Sample, RefDatabase FROM {};""".format(apr)
    cursor.execute(query)
    samp_refdb = cursor.fetchall()
    
    for i in samp_refdb:
        
        row = cResInfo.results_info() # init class object
        
        row.Approach = apr
        row.Sample = i[0]
        row.RefDatabase = i[1]
        
        # Get true positives:
        queryT = fQueries.query4trues(row.Approach,row.Sample,TaxRank,row.RefDatabase)
        cursor.execute(queryT)
        row.TruePos = len(cursor.fetchall())
        
        # Get false positives:
        queryT = queryT.replace(";","")
        queryF = fQueries.query4falses(row.Approach,row.Sample,TaxRank,queryT,row.RefDatabase)
        cursor.execute(queryF)
        row.FalsePos = len(cursor.fetchall())
        
        # check if TruePos + FalsePos match the total:
        queryT = fQueries.query4total(row.Approach,row.Sample,TaxRank,row.RefDatabase)
        cursor.execute(queryT)
        total_matches = cursor.fetchall()[0][0]
        
        if row.TruePos + row.FalsePos != total_matches:
            print ("")
            print ("Warning, TruePos + FalsePos do not match the total")
            print ("something is missing!")
            print("")
        
        # Calc recall (% of the input that were recivered within true positives)
        queryR = fQueries.query4taxIn(row.Sample,TaxRank)
        cursor.execute(queryR)
        total_input = cursor.fetchall()[0][0]
        row.Recall = round((row.TruePos * 100 / total_input), 4)

        # Calc accuracy (% from all matches that are true positives)
        row.Accuracy = round((row.TruePos * 100  / total_matches), 4)
      
        store_results.append(row)
    
    
    
### Create new Results database
query = """CREATE TABLE IF NOT EXISTS Results{} (Approach text, 
Sample text, RefDatabase text, TruePos integer, FalsePos integer, 
Recall float, Accuracy float);""".format(TaxRank)

cursor.execute(query)
connection.commit()

    
### output as a SQLite3:
query = "INSERT INTO Results{} VALUES (?,?,?,?,?,?,?);".format(TaxRank)
for i in store_results:
    cursor.execute(query,(i.Approach, i.Sample, i.RefDatabase, i.TruePos,
                          i.FalsePos, i.Recall, i.Accuracy))
    
    
### Save to csv file?
if sql2csv != None:
  
    header=('Approach', 'Sample', 'RefDatabase', 'TruePos', 'FalsePos',
        'Recall', 'Accuracy')
    
    csvWriter = csv.writer(open(sql2csv, "w"))    
    csvWriter.writerow(header)

    query = "SELECT * from Results{};".format(TaxRank)
    cursor.execute(query)
    rows = cursor.fetchall()
    
    print ("saving to csv")
    for row in rows:
        csvWriter.writerow(row)



### Save db
connection.commit()
connection.close()


print ("")
print ("Done!")
print ("")
