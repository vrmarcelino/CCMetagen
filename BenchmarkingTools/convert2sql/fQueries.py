#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Functions that produce SQLIte3 queries

Required to benchmark the results and store info in 'bench.db'

@ V.R.Marcelino
Created on 17 Jul 2018
Last update ---

"""

### Class to store info that goes in the Results tables
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


def query4trues(approach,sample,taxLevel,RefDb):
        
    variables=(approach,taxLevel,approach,approach,taxLevel,taxLevel,
               sample,approach,sample,approach,RefDb,approach,taxLevel)
    
    query = """
    SELECT DISTINCT {}.{}_TaxID
    FROM {}
    INNER JOIN FUNGI ON {}.{}_TaxID = Fungi.{}_TaxID
    WHERE Fungi.SAMPLE='{}' AND {}.Sample='{}'
    AND {}.RefDatabase='{}'
    AND {}.{}_TaxID IS NOT NULL;""".format(*variables)
    
    print (query)
    print("")
    return query


### Function to produce query that gets False Positives # script
# Ignore where Species_Taxid is null
def query4falses(approach,sample,taxLevel,query4trues,RefDb):
        
    variables=(approach,taxLevel,approach,approach,taxLevel,query4trues,
               approach,sample,approach,RefDb,approach,taxLevel)
   
    query = """
    SELECT DISTINCT {}.{}_TaxID
    FROM {}
    WHERE {}.{}_TaxID NOT IN 
    ({})
    AND {}.Sample='{}'
    AND {}.RefDatabase='{}'
    AND {}.{}_TaxID IS NOT NULL;""".format(*variables)
    
    print (query)
    print("")
    return query   


### Function that calculates the total number of matches for a given sample
# ad tax. level
def query4total(approach,sample,taxLevel):
    
    variables = (taxLevel,approach,sample,approach,RefDb,taxLevel)
    query = """SELECT count(DISTINCT {}_taxID) 
    FROM {} 
    WHERE Sample='{}'
    AND {}.RefDatabase='{}'
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


