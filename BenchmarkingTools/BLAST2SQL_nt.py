#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Parse the results of large BLAST tabular results with the nt ref database
and store it in the SQLite3 'bench.db'

Requires Jan's scripts: https://gitlab.com/janpb/blib

USAGE ex: python BLAST2SQL_nt.py -i 2_mtg_nt.txt -n 2_mtg -sql benchm.db

Authors:
Jan P Buchmann 
V.R.Marcelino 

Created on 20 Jul 2018
Last update: 24 Jul 2018
"""

import os
import sys 
import sqlite3
from argparse import ArgumentParser
sys.path.insert(1,os.path.join(sys.path[0], '/Users/vanessamarcelino/Documents/Programs/blib/ncbi/src'))
import edirect.callimachus.ncbi_callimachus
import edirect.edbase.edanalyzer
sys.path.insert(1,os.path.join(sys.path[0], '/Users/vanessamarcelino/Documents/Programs/blib/taxonomy/src'))
import taxonomist


parser = ArgumentParser()
parser.add_argument('-i', '--input_blastn_result', help='The path to the .txt file in tabular format', required=True)
parser.add_argument('-n', '--input_sample_name', help='Tthe name of the sample', required=True)
parser.add_argument('-sql', '--SQL_db', help='SQL database where it should store the data', required=True)

# import files:
args = parser.parse_args()
blast_raw_res = args.input_blastn_result
ref_database = "nt"
sql_fp = args.SQL_db
sample = args.input_sample_name

#blast_raw_res = "../work/0_mtt_nt_test.txt"
#sql_fp = "../work/benchm.db"
#sample = "0_mtt_test_JansWay"
#ref_database = "nt"


class NcbiDocsumAnalyzer(edirect.edbase.edanalyzer.EdAnalyzer):

	def __init__(self):
		super().__init__()
		self.queries = {}

	def fetch_sequence_info(self, queries):
		self.queries = queries
		nc = edirect.callimachus.ncbi_callimachus.NcbiCallimachus(email='tets')
		qry = nc.new_query()
		fq = qry.new_fetch(analyzer=self,
					  options={'db' : 'nuccore',
					           'retmode' : 'json',
					           'rettype' : 'docsum',
					           'id' : [x for x in queries]})
		qry.add_query(fq)
		nc.run_query(qry)
	
	def analyze_result(self, response, request):
		for i in response['result']['uids']:
			if response['result'][i]['accessionversion'] in self.queries:
				self.queries[response['result'][i]['accessionversion']] = int(response['result'][i]['taxid'])



class TaxonomyAnalyzer(edirect.edbase.edanalyzer.EdAnalyzer):

  def __init__(self):
    super().__init__()
    self.taxonomist = taxonomist.NcbiTaxonomist()
    self.queries = {}

  def analyze_result(self, reponse, request):
    self.taxonomist.parse(reponse)

  def fetch_lineages(self, taxids):
    nc = edirect.callimachus.ncbi_callimachus.NcbiCallimachus(email='jan')
    qry = nc.new_query()
    qid = qry.add_query(qry.new_fetch(analyzer=self,
                                      options={'db' : 'taxonomy',
                                               'retmode' : 'xml',
                                               'id' : taxids}))
    nc.run_query(qry)

## create a sqlite3 table -- in memory -- with blast result columns, e.g. qaccver,saccver,evalue...

connection = sqlite3.connect(":memory:")
cursor = connection.cursor()

createstmt = """CREATE TABLE IF NOT EXISTS BLASTn_raw_results (rowid INTEGER PRIMARY KEY, qseqid TEXT, sseqid text, 
pident FLOAT, length INT, mismatches INT, gapopen INT,qstart integer,
qend INT, sstart integer, ssend INT, evalue FLOAT, bitscore INT);"""
cursor.execute(createstmt)
connection.commit()

rowbuffer = []
rowcount = 0
threshold = 1000000
insertstmt = "INSERT INTO BLASTn_raw_results (qseqid, sseqid, pident, length, mismatches, gapopen,qstart,qend,sstart,ssend,evalue,bitscore) VALUES (?,?,?,?,?,?,?,?,?,?,?,?);"
accessions = {'queries' : {},
			  'hits' : {}}
with open(blast_raw_res) as res:
	for i in res:
		rowcount += 1
		cols = i.rstrip().split('\t')
		if cols[0] not in accessions['queries']:
			accessions['queries'][cols[0]] = 0
		if cols[1] not in accessions['hits']:
			accessions['hits'][cols[1]] = 0
		accessions['queries'][cols[0]] += 1
		accessions['hits'][cols[1]] += 1	
		if rowcount % threshold == 0:
			cursor.executemany(insertstmt, rowbuffer)
			connection.commit()
			print("Added {} entries".format(threshold))
			rowbuffer = []
		rowbuffer.append(cols)


#print(stmt, rowbuffer)

cursor.executemany(insertstmt, rowbuffer)
print("Added {} entries in total in the temporary sql table BLASTn_raw_results ".format(rowcount))
#stmt = """SELECT COUNT(*) FROM BLASTn_raw_results"""

stmt = """SELECT DISTINCT sseqid FROM BLASTn_raw_results"""
for i in cursor.execute(stmt):
	print(i)
connection.commit()

accession_queries = {}
for i in accessions['hits']:
	accession_queries[i] = None

# get taxids for accessions:
nda = NcbiDocsumAnalyzer()
nda.fetch_sequence_info(accession_queries)

# not sure what this does - see bad request error
stmt_create_accs_tbl = """ CREATE TABLE IF NOT EXISTS accessions (accession TEXT, taxid INT)"""
cursor.execute(stmt_create_accs_tbl)
connection.commit()
stmt_insert_accessions = """ INSERT INTO accessions (accession, taxid) VALUES(?,?)"""
rowbuffer= []
rowcount = 0
for i in accession_queries:
	rowcount += 1
	if rowcount % 500 == 0:
		cursor.executemany(stmt_insert_accessions, rowbuffer)
		rowbuffer = []
	rowbuffer.append((i, accession_queries[i]))
cursor.executemany(stmt_insert_accessions, rowbuffer)

for i in cursor.execute("""SELECT * FROM accessions"""):
	print(i)

fh_sql = open('memdump.sql', 'w')
for i in connection.iterdump():
	fh_sql.write(i+'\n')
fh_sql.close()


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



t = taxonomist.NcbiTaxonomist()
ta = TaxonomyAnalyzer()
taxids = {}
for i in accession_queries:
	taxids[accession_queries[i]] = 0
ta.fetch_lineages([x for x in taxids])

### note that there will be one row per match, and no abundance calculation.

rowbuffer = []
rowcount = 0
threshold = 1000
query = """INSERT INTO BLASTn (TaxID, Lineage, Sample, RefDatabase, 
Abundance, Kingdom ,Kingdom_TaxId, Phylum, Phylum_TaxId, Class, Class_TaxId,
OOrder, Order_TaxId, Family, Family_TaxId, Genus, Genus_TaxId, Species,
Species_TaxId) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?);"""


for i in taxids:
    if i != None:
        rowcount += 1
        
        # if multiple of 500, dump into sql
        if rowcount % threshold == 0:
            cursor.executemany(query, rowbuffer)
            rowbuffer = []
        
        clade = t.get_clade_from_taxid(i)
        lin = t.assemble_lineage_from_taxid(i)
        norm = t.get_normalized_clade_lineage(clade, lin)
        
        # check if it has all the fields:
        if len(norm) == 17:
        
        # output as a SQLite3:
            variables_in_one_line = (i, "No Lineage for nt", sample, ref_database, 
                0, norm[1].name, norm[1].taxid, norm[2].name, norm[2].taxid,
                norm[4].name, norm[4].taxid, norm[6].name, norm[6].taxid, 
                norm[11].name, norm[11].taxid,norm[13].name, norm[13].taxid,
                norm[15].name, norm[15].taxid)
        
            rowbuffer.append(variables_in_one_line)
        
        else:
            print ("not enought information for taxid %i" %(i))
            print ("will continue without this hit")
            print ("")

    else:
        print ("taxid = None")


cursor.executemany(query, rowbuffer)
connection.commit()

print ("")
print ("Done!")
print ("Table BLASTn saved in %s sqlite3 database" %(sql_fp))
print ("")


# tests
#for i in norm:
#    print (i.name, i.rank, i.taxid)




