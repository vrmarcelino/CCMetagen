#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Rename ITS sequences from the Unit datatase so they include a TaxId
@ V.R.Marcelino
Created on Fri Jul  6 15:51:37 2018
"""

from Bio import SeqIO
from Bio.SeqRecord import SeqRecord
from Bio.Seq import Seq
from Bio import Entrez
import re
import mmap
import contextlib

input_seqs="ITS-unite_test.fasta"
map_fp="accession_taxid_nucl.map"

# get accession numbers
for seq_record in SeqIO.parse(input_seqs, "fasta"):
    get_ass = re.split("\|", seq_record.id)
    accession = get_ass[1]
    print (accession)



# get taxids
with open(map_fp, 'rb', 0) as f:
    accession = 'DQ656654'
    
    # open it as a memory-mapped file
    mm = mmap.mmap(f.fileno(), 0,access=mmap.ACCESS_COPY)
    
    # transform accession to bytes
    b = accession.encode('utf-8') 
    
    # search, convert result to string and return taxid
    result = mm.find(b)
    mm.seek(result)
    found_line = str(mm.readline())

    taxid_part = re.split('t', found_line)[1]
    taxid = taxid_part.replace("\\n'","")
    print (taxid)
    





