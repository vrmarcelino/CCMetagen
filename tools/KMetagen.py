#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
KMetagen main script

Version 0.1

@ V.R.Marcelino
Created on Wed Jul 25 17:13:10 2018

"""

# imports
import sys
from argparse import ArgumentParser
import fRunKMA

# help
if len(sys.argv) == 1:
    print ("")
    print (" KMetagen - Metagenomic analyses")
    print ("")
    print ("Usage: KMetagen.py <options> ")
    print ("")
    print ("")
    sys.exit()


parser = ArgumentParser()


th = '3'
out_fp = "06_TaxAssign/KMetagen"
db_its="../large_databases/KMA/Unite_ITS/ITS_unite"

inR1="test_mtt_R1.fasta"
inR2="test_mtt_R2.fasta"




# check if flags are compatible, otherwise return a error?
# or does KMA will do that?



# funcions



    
    