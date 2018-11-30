#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Classe that store results info 

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

