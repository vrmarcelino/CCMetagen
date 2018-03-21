#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FunMetagenomics

Step 3 - Filter frags files to remove the sequences that failed in the coverage filtering.

@ V.R.Marcelino
12 - March -2018

"""

# load modules
import csv
from argparse import ArgumentParser
import sys
import subprocess

#help
if len(sys.argv) == 1:
    print ("")
    print ("Script to filter .frag files to remove the sequences that failed in the first QC")
    print ("")
    print ("Usage: KMetagen_part3_QC2_FilterFrags.py dataset.fas -r res_file_path -f frags_file_path")
    print ("")
    print ("")
    sys.exit()


# Input and output files
parser = ArgumentParser()
parser.add_argument('-r', '--res_fp', help='The path to the filtered res file', required=True)
parser.add_argument('-f', '--frags_fp', help='The path to the frags file', required=True)

args = parser.parse_args()
res_fp = args.res_fp
frags_fp = args.frags_fp

out_frags_good = args.frags_fp + ".pass.txt"
out_frags_good_sorted = args.frags_fp + ".pass_sorted.txt"
out_frags_fail = args.frags_fp + ".fail.txt"

# debbugging (Delete this later)
#res_fp = "00_very_small_test/test.res.filtered.txt"
#frags_fp = "00_very_small_test/test.frag"

#res_fp = "01_small_test/test.res.filtered.txt"
#frags_fp = "01_small_test/test.frag"

#out_frags_good = "00_very_small_test/test.frag.pass.txt"
#out_frags_fail = "00_very_small_test/test.frag.fail.txt"


# Read and store species in res file
res_species = []
with open(res_fp) as res:
    next (res) # skip first line
    for line in csv.reader(res):
        filt_sp = line[0].split('|')[2] # 'species' level
        res_species.append(filt_sp)


# Read frags file and save the filtered one
ofile_good = open(out_frags_good, "w")
ofile_fail = open(out_frags_fail, "w")

cg = 0 #count good reads
cb = 0 #count failed reads
with open(frags_fp) as frags:
    for line in csv.reader(frags):
        species = line[0].split('|')[2]
        
        if species in res_species:
            ofile_good.write(line[0] + "\n")
            cg += 1
            
        else:
            ofile_fail.write(line[0] + "\n")
            cb += 1
            
ofile_good.close()
ofile_fail.close()

print ("")
print ("Saved %i sequences in the frags.pass.txt file." %(cg))
print ("%i reads did not meet the coverage QC threshold" %(cb))
print ("")

print ("sorting...")

shell_command = "sort -k 7,7 " + out_frags_good + " > " + out_frags_good_sorted

subprocess.run(shell_command, shell=True)

print ("Done!")
print (" .pass.txt and .fail.txt files can be deleted")
print ("")
