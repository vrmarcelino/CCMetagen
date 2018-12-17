#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Function that takes a accession number and returns the taxid 

requires accession_taxid_nucl.map file

Required to parse the results of BLAST (nt) and store them in the SQLite3 'benchm.db'

@ V.R.Marcelino
Created on 18 Jul 2018

"""
import mmap
import re

# function to get taxids from accession numbers
def get_tax_id (accession, map_fp):
    with open(map_fp, 'rb', 0) as f:
    
        # open it as a memory-mapped file
        mm = mmap.mmap(f.fileno(), 0,access=mmap.ACCESS_COPY)
        
        # transform accession to bytes
        b = accession.encode('utf-8') 
    
        # search, convert result to string and return taxid
        result = mm.find(b)
        
        # if taxid exists, convert it to string and return taxid
        if result != -1:
            mm.seek(result)
            found_line = str(mm.readline())
        
            taxid_part = re.split('t', found_line)[1]
            taxid = taxid_part.replace("\\n'","")
        
        else:
            taxid = 'unk_taxid'
        return taxid

