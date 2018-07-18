#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Parse the results of 1 BLAST tabular result and store it in the SQLite3 'bench.db'

USAGE ex: python BLAST2SQL.py -i 2_mtg_ITS.txt -n 2_mtg -sql benchm.db -r ITS

@ V.R.Marcelino
Created on 13 Jul 2018

Last update: 18 Jul 2018
"""

import re
from argparse import ArgumentParser
import sqlite3
from ete3 import NCBITaxa
ncbi = NCBITaxa()
import cTaxInfo # script that define classes used here
import fNCBItax # script with function to get lineage from taxid
import pandas as pd
import fAcc2TaxId

parser = ArgumentParser()
parser.add_argument('-i', '--input_blastn_result', help='The path to the .txt file in tabular format', required=True)
parser.add_argument('-n', '--input_sample_name', help='Tthe name of the sample', required=True)
parser.add_argument('-r', '--reference_database', help='Reference database used, options are ITS, RefSeq_f_partial, RefSeq_bf and nt', required=True)
parser.add_argument('-sql', '--SQL_db', help='SQL database where it should store the data', required=True)
parser.add_argument('-map', '--acc2taxmap', help='path to the accession_taxid_nucl.map file', required=False)

args = parser.parse_args()
in_res_file = args.input_blastn_result
ref_database = args.reference_database
sql_fp = args.SQL_db
sample_name = args.input_sample_name

# Tests and torubleshooting
#in_res_file = "mtt_nt_test.txt"
#in_res_file = "2_mtg_ITS.txt"
#sql_fp="benchm.db"
#sample_name="mtt"
#ref_database = "RefSeq_bf"
#ref_database = "nt"
#acc2taxid_map_fp = "accession_taxid_nucl.map"

############# 
connection = sqlite3.connect(sql_fp)
cursor = connection.cursor()

# Create a table if it does not exist:
# Note that Order is written with two 'O's, as Order is a sql command
query = """CREATE TABLE IF NOT EXISTS BLASTn (TaxID integer, Lineage text, 
Sample text, RefDatabase text, Abundance real, Kingdom text,Kingdom_TaxId integer,
Phylum text, Phylum_TaxId integer, Class text, Class_TaxId integer, OOrder text,
Order_TaxId integer, Family text, Family_TaxId integer, Genus text, 
Genus_TaxId integer, Species text, Species_TaxId integer);"""

cursor.execute(query)
connection.commit()

#############

# Since Blast and Diamond output one line per read, we need to calculate the
# abundance of each hit.
result_all_reads = pd.read_csv(in_res_file, sep='\t', header=None)

# count read names in every tax matched
print ("calculating matches... takes a while for large files")
one_line_per_match = result_all_reads.groupby([result_all_reads.iloc[:,1]]).count()


#############

# note:
if ref_database == "nt":
    print ("nt takes a long time to run. Suggest to do this in a HPC server.")

#############
# Read and store taxids in list of classes
print ("getting taxonomic information")
store_lineage_info = []

for line in one_line_per_match.iterrows():
    split_match = re.split (r'(\|| )', line[0])

    match_info = cTaxInfo.TaxInfo()
    
    if ref_database == "ITS":
        
        match_info.Lineage = split_match[12]

        if split_match[4] != 'unk_taxid':
                
            match_info.TaxId = int(split_match[4])
            match_info = fNCBItax.lineage_extractor(match_info.TaxId , match_info)
                
        # Handle unknown taxids: 
        else:
            full_lin = split_match[12]
            species_full_name = full_lin.split('_')[-2:]
            species_name_part2 = species_full_name[1].replace('sp', 'sp.')
            species_name = species_full_name[0] + " " + species_name_part2
                
            # get taxid from species name
            retrieved_taxid = ncbi.get_name_translator([species_name])
                
            # if found, add to class object
            if len(retrieved_taxid) != 0:
                match_info.TaxId = retrieved_taxid[species_name][0]
                match_info = fNCBItax.lineage_extractor(match_info.TaxId, match_info)
        
            # if unkwnon, try with genus only:
            else:
                retrieved_taxid = ncbi.get_name_translator([species_full_name[0]])
                    
                # if found, add to class object
                if len(retrieved_taxid) != 0:
                    match_info.TaxId = retrieved_taxid[species_full_name[0]][0]
                    match_info = fNCBItax.lineage_extractor(match_info.TaxId, match_info)
                
                # if still not found, print warning
                else:
                    print ("")
                    print ("WARNING: no taxid found for %s" %(full_lin))
                    print ("this match will not get the NCBItax lineage information")
                    print ("and will not be included in the analyses")
                    print ("")
                    match_info.TaxId = split_match[4] # 'unk_taxid'
                    match_info.Lineage = split_match[12] # lineage from ITS - Unite db only.

    elif ref_database == "RefSeq_f_partial" or ref_database == "RefSeq_bf":
        match_info.TaxId = split_match[4]
        match_info.Lineage = split_match[0] # the accession id of the match
        match_info = fNCBItax.lineage_extractor(match_info.TaxId, match_info)
    
    elif ref_database == "nt":
        acc2taxid_map_fp = args.acc2taxmap
        match_info.Lineage = split_match[0] # the accession number
        print ("processing accession %s" %(match_info.Lineage))
        
        retrieved_taxid = fAcc2TaxId.get_tax_id(match_info.Lineage,acc2taxid_map_fp) #get taxid from accession number
        
        # if found, add to class object
        if len(retrieved_taxid) != 0:
            match_info.TaxId = retrieved_taxid
            match_info = fNCBItax.lineage_extractor(match_info.TaxId, match_info)
        else:
            print ("")
            print ("WARNING: no taxid found for accession %s" %(match_info.Lineage))
            print ("this match will not get the NCBItax lineage information")
            print ("and will not be included in the analyses")
            print ("")
            
    else:
        print ("ref_database must be ITS, RefSeq_f_part, RefSeq_bf or nt")
    
    Abund = line[1][0] # How many reads for that match
    match_info.Abundance = float(Abund)
    match_info.Sample = sample_name
    match_info.RefDatabase = ref_database
    store_lineage_info.append(match_info)


#### output as a SQLite3:
query = "INSERT INTO BLASTn VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);"
for i in store_lineage_info:
    cursor.execute(query,(i.TaxId,i.Lineage,i.Sample,i.RefDatabase,i.Abundance,
                          i.Kingdom,i.Kingdom_TaxId,i.Phylum,i.Phylum_TaxId,
                          i.Class,i.Class_TaxId,i.Order,i.Order_TaxId,i.Family,
                          i.Family_TaxId,i.Genus,i.Genus_TaxId,i.Species,
                          i.Species_TaxId))
        
#### Save db
connection.commit()
connection.close()

print ("")
print ("Done!")
print ("Table BLASTn saved in %s sqlite3 database" %(sql_fp))
print ("")


#################
#check it is all right
#for i in store_lineage_info:
#    print (i.TaxId)
#    print (i.Lineage)
#    print (i.Sample)
#    print (i.RefDatabase)
#    print (i.Abundance)
#    print (i.Family)

#for i in store_lineage_info:
#    if i.TaxId == 'unk_taxid':
#        print (i.TaxId)
#        print (i.Lineage)
        