#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script to run KMA 

Requires KMA to be installed and accessible in your $PATH

@ V.R.Marcelino
Created on Wed Jul 25 17:17:18 2018

"""

# load modules
import subprocess


# variables (to be taken from function)

th = '3'
out_fp = "06_TaxAssign/KMetagen"
db_its="../large_databases/KMA/Unite_ITS/ITS_unite"

inR1="test_mtt_R1.fasta"
inR2="test_mtt_R2.fasta"


# function to run KMA with the desired flags

def kma_runner(in_type, in_fp, ref, out_fp, th = '1', 
               pairing_method = 'p', one2one = True, sparse = False, 
               mem_mode = False):
    
    
    # create a new directory
    shell_command = "mkdir -p" + out_fp
    subprocess.run(shell_command, shell=True)
    
    if len(in_fp) != 0:
        print (len(in_fp))
    
    shell_command = "kma "+in_type+" "+ in_fp+" -o "+out_fp+" -t_db "+ref+" -t "+th
    
    print (shell_command)





kma_runner('-i', inR1, db_its,out_fp)










