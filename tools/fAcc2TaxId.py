#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Functions to convert accession numbers to taxids

requires an accession_taxid_nucl.map file

@ V.R.Marcelino
Created on 18 Jul 2018
Modified: 17 Dec 2018
"""
import mmap
import re
import subprocess


### function that produces a filtered acc2taxid map based on KMA results
def filter_acc2taxid_map(in_res_file, acc2taxid_map_fp, threads, rb):
    # makes it run grep faster
    subprocess.run("export LC_ALL=C", shell=True)
                
    # extract accession numbers in one text file
    command = "awk '{print $1}' " + in_res_file + " > "+rb+ "_accessions.temp"
    subprocess.run(command, shell=True) 
    
    
    # if runing in a single core (localy)
    if threads == 1:
        print ("""Running KMetagen to parse nt results on a single core - this is rather slow.
If possible, use a multi-core computer with paralell installed
https://www.gnu.org/software/parallel/

Filtering acc2taxid map file ...

""")
        command = "grep -wf "+ rb +"_accessions.temp " + acc2taxid_map_fp + " > " + rb + "_acc2taxid_map_filtered.temp"
        subprocess.run(command, shell=True)
                
    # if running on multi-core computer:    
    else:
        command = "cat " + acc2taxid_map_fp + " | parallel -j " + str(threads) + " --pipe --block 2000M --cat grep -wf "+ rb +"_accessions.temp {} > " + rb + "_acc2taxid_map_filtered.temp"
        subprocess.run(command, shell=True)
                
### function to get taxids from accession numbers via dictionary
def get_tax_id_dic (accession, accession_dic):
    taxid = accession_dic.get(accession)
    return taxid


### function that deletes the temporary files:
def cleanup(rb):
    accessions = "rm " + rb + "_accessions.temp"
    subprocess.run(accessions, shell=True)         
    map_fp = "rm " + rb + "_acc2taxid_map_filtered.temp"
    subprocess.run(map_fp, shell=True)                  
                

                