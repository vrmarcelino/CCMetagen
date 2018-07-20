#!/usr/bin/env python3
import os
import sys 
import sqlite3

sys.path.insert(1,os.path.join(sys.path[0], '/Users/vanessamarcelino/Documents/Programs/blib/ncbi/src'))
import edirect.callimachus.ncbi_callimachus
import edirect.edbase.edanalyzer
sys.path.insert(1,os.path.join(sys.path[0], '/Users/vanessamarcelino/Documents/Programs/blib/taxonomy/src'))
import taxonomist


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

connection = sqlite3.connect(":memory:")
cursor = connection.cursor()
## assuming a sqlite3 table with baslt result columns, e.g. qaccver,saccver,evalue...
createstmt = """CREATE TABLE IF NOT EXISTS BLASTn (rowid INTEGER PRIMARY KEY, qseqid TEXT, sseqid text, 
pident FLOAT, length INT, mismatches INT, gapopen INT,qstart integer,
qend INT, sstart integer, ssend INT, evalue FLOAT, bitscore INT);"""
cursor.execute(createstmt)
connection.commit()

rowbuffer = []
rowcount = 0
threshold = 1000000
insertstmt = "INSERT INTO BLASTn (qseqid, sseqid, pident, length, mismatches, gapopen,qstart,qend,sstart,ssend,evalue,bitscore) VALUES (?,?,?,?,?,?,?,?,?,?,?,?);"
accessions = {'queries' : {},
			  'hits' : {}}
for i in sys.stdin:
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
print("Added {} entries in total".format(rowcount))
stmt = """SELECT COUNT(*) FROM BLASTn"""

stmt = """SELECT DISTINCT sseqid FROM BLASTn"""
for i in cursor.execute(stmt):
	print(i)
connection.commit()

accession_queries = {}
for i in accessions['hits']:
	accession_queries[i] = None

nda = NcbiDocsumAnalyzer()
nda.fetch_sequence_info(accession_queries)

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

t = taxonomist.NcbiTaxonomist()
ta = TaxonomyAnalyzer()
taxids = {}
for i in accession_queries:
	taxids[accession_queries[i]] = 0
ta.fetch_lineages([x for x in taxids])
for i in taxids:
	clade = t.get_clade_from_taxid(i)
	lin = t.assemble_lineage_from_taxid(i)
	norm = t.get_normalized_clade_lineage(clade, lin)
	for i in norm:
		print(i.name, i.rank, i.taxid)
	print("----------")
