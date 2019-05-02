#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Classe that store results info 

Required to benchmark the results and store info in 'bench.db'

@ V.R.Marcelino
Created on 17 Jul 2018
Last update 30 Apr 2019

"""

### Class to store info that goes in the Results tables
class results_info():
     def __init__(self, Approach=None,Sample=None,RefDatabase=None,
                  TruePos=None,FalsePos=None,Recall=None,Precision=None,TaxLevel=None):
         
         self.Approach = Approach
         self.Sample = Sample
         self.RefDatabase = RefDatabase
         self.TruePos = TruePos
         self.FalsePos = FalsePos
         self.Recall = Recall
         self.Precision = Precision
         self.TaxLevel = TaxLevel

     def __iter__(self):
         return iter([self.Approach, self.Sample, self.Precision, self.Recall, self.TaxLevel])

