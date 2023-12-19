#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script to add taxids to nt collection

@ V.R.Marcelino
Created on Fri Dec 28 10:37:56 2018
"""
import re
import logging


logging.info("Starting script.")

# Input files:
acc2taxid_map = "accession_taxid_nucl.map"
nt_in = "nt_sequential.fa"

# Output file:
nt_out = "nt_w_taxid.fas"

# Function to get taxids from accession numbers
def get_tax_id_dic(accession, accession_dic):
    taxid = accession_dic.get(accession, "unk_taxid")
    return taxid

# Read acc2taxid.map as a dictionary
logging.info("Reading acc2taxid.map as a dictionary.")
with open(acc2taxid_map) as a:
    acc2tax_dic = dict(x.rstrip().split(None, 1) for x in a)

logging.info(f"Dictionary has {len(acc2tax_dic)} entries.")

# Read fasta file and write the new file on the fly
logging.info("Reading nt file and writing new file.")
with open(nt_in) as nt, open(nt_out, 'w') as new_nt:
    ix = 0
    for line in nt:
        ix += 1
        if not ix % 1000000:
            logging.info("Processed {} lines.".format(ix))

        if line.startswith(">"):
            splited_rec = re.split(r'(>| )', line)
            accession = splited_rec[2]
            taxid = get_tax_id_dic(accession, acc2tax_dic)
            line = ">" + taxid + "|" + "".join(splited_rec[2:])
        new_nt.write(line)

logging.info("All done.")
