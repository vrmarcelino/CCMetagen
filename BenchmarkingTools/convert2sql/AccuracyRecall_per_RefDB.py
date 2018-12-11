#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script to get one file per Database with Accuracy at several taxon levels

Works wth sqlite3

@ V.R.Marcelino
Created on Fri Nov 30 12:56:01 2018

"""

import sqlite3
from argparse import ArgumentParser
import cResInfo # custom classes used here
import fQueries # custom functions used here
import csv

parser = ArgumentParser()
parser.add_argument('-sql', '--SQL_db', help='SQL database to make comparisons', required=True)
parser.add_argument('-r', '--ref_db', help='reference database: UNITE, RefSeq_f_partial, RefSeq_bf or nt', required=True)
parser.add_argument('-o', '--output_csv', help='output file path', required=False)


args = parser.parse_args()
sql_fp = args.SQL_db
ref_db = args.ref_db
out_file = args.output_csv

# editing and debugging
#sql_fp="benchm.db"
#ref_db="RefSeq_f_partial"

accuracy_results=['ResultsPhylum','ResultsClass','ResultsOrder','ResultsFamily','ResultsGenus','ResultsSpecies']



#### Open database:
connection = sqlite3.connect(sql_fp)
cursor = connection.cursor()

#### Loop through approaches and add all info to benchm.db:

store_results = []


# Loop trough taxon levels and get the wanted results for each level
for r in accuracy_results:
    query="SELECT Approach, Sample, Accuracy, Recall FROM {} WHERE RefDatabase = '{}';".format(r,ref_db)
    cursor.execute(query)
    info_from_results = cursor.fetchall()
    
    for i in info_from_results:
        
        row = cResInfo.results_info() # init class object
    
        row.Approach = i[0]
        row.Sample = i[1]
        row.Accuracy = i[2]
        row.Recall = i[3]
        
        
        # define taxon level:
        taxonlevel = r.replace('Results','')

        row.TaxLevel = taxonlevel
        
        store_results.append(row)
        
      
  
# Save 
with open(out_file, 'w') as csv_file:
    wr = csv.writer(csv_file, delimiter=',')
    wr.writerow(["Aproach","Sample","Accuracy","Recall","TaxLevel"])
    for i in store_results:
        wr.writerow(list(i))
        


print ("Done!")
        
