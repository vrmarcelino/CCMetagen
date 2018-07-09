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
import multiprocessing
from multiprocessing import Pool

input_seqs="ITS-unite.fasta"
map_fp="accession_taxid_nucl.map"
output_fp="ITS-unite-renamed_test_mproc.fasta"
th=16

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
    
## function from https://biopython.org/wiki/Split_large_file
def batch_iterator(iterator, batch_size):
    """Returns lists of length batch_size.

    This can be used on any iterator, for example to batch up
    SeqRecord objects from Bio.SeqIO.parse(...), or to batch
    Alignment objects from Bio.AlignIO.parse(...), or simply
    lines from a file handle.

    This is a generator function, and it returns lists of the
    entries from the supplied iterator.  Each list will have
    batch_size entries, although the final list may be shorter.
    """
    entry = True  # Make sure we loop once
    while entry:
        batch = []
        while len(batch) < batch_size:
            try:
                entry = iterator.__next__()
            except StopIteration:
                entry = None
            if entry is None:
                # End of file
                break
            batch.append(entry)
        if batch:
            yield batch




def open_and_save_rec (batch_name):
    renamed_batch_name = batch_name + "renamed.fasta"
    ofile = open(renamed_batch_name, "w")
    for seq_record in SeqIO.parse(batch_name, "fasta"):
        get_ass = re.split("\|", seq_record.id)
        accession = get_ass[1]
    
        last_piece_1 = get_ass[1:]
        last_piece_2 = "|".join(last_piece_1)
    
        taxid = get_tax_id(accession, map_fp)
      
        new_seq_name = ">" + get_ass[0] + "|taxid|" + taxid + "|" + last_piece_2
        
        print (new_seq_name)
    
        ofile.write(new_seq_name + "\n" + str(seq_record.seq) + "\n")
    ofile.close()




# divide the fasta file into multiple files:
count_groups = 0
record_iter=SeqIO.parse(open(input_seqs),"fasta")
for i, batch in enumerate(batch_iterator(record_iter, 4000)):
    count_groups += 1
    filename = "group_%i.fasta" % (i + 1)
    with open(filename, "w") as handle:
        count = SeqIO.write(batch, handle, "fasta")
    print("Wrote %i records to %s" % (count, filename))


for i in range(count_groups):
    filename = "group_%i.fasta" % (i + 1)
    p_i = multiprocessing.Process(target=open_and_save_rec, args=(filename,))
    p_i.start()

p_i.join()




print ("")
print ("Done!")
print ("")




