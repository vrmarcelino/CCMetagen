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
import re
import mmap

input_seqs="ITS-unite.fasta"
map_fp="accession_taxid_nucl.map"
output_fp="ITS-unite-renamed.fasta"


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
    

# function that get accession number from 1 seq record and include taxids
def rename(seq_record):
    get_ass = re.split("\|", seq_record.id)
    accession = get_ass[1]
    
    last_piece_1 = get_ass[1:]
    last_piece_2 = "|".join(last_piece_1)
    
    taxid = get_tax_id(accession, map_fp)
      
    new_seq_name = get_ass[0] + "|taxid|" + taxid + "|" + last_piece_2
    
    seq = str(seq_record.seq)
    new_record = SeqRecord(Seq(seq), id=new_seq_name, description='')
    print(new_seq_name)
    return new_record
    

# Run it and save on the fly:
SeqIO.write((rename(r) for r in SeqIO.parse(input_seqs, "fasta")),
            output_fp, "fasta")



print ("")
print ("Done!")
print ("")




