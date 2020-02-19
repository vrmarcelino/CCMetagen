"""
Function that takes a taxid as input and returns a class containing the taxonomic info and taxids
for multiple taxonomic ranks.

Required to parse the results of KMA and store them in the SQLite3 'bench.db'

@ V.R.Marcelino
Created on 12 Jul 2018

"""


from ete3 import NCBITaxa


def lineage_extractor(query_taxid, TaxInfo_object):
    list_of_taxa_ranks = ['superkingdom', 'kingdom', 'phylum', 'class', 'order', 'family','genus', 'species']
    ncbi = NCBITaxa()
    lineage = ncbi.get_lineage(query_taxid)
    ranks = ncbi.get_rank(lineage)
    names = ncbi.get_taxid_translator(lineage)

# get known data
    for key, val in ranks.items():

        if val == list_of_taxa_ranks[0]:
            TaxInfo_object.Superkingdom = names[key]
            TaxInfo_object.Superkingdom_TaxId = key

        elif val == list_of_taxa_ranks[1]:
            TaxInfo_object.Kingdom = names[key]
            TaxInfo_object.Kingdom_TaxId = key

        elif val == list_of_taxa_ranks[2]:
            TaxInfo_object.Phylum = names[key]
            TaxInfo_object.Phylum_TaxId = key

        elif val == list_of_taxa_ranks[3]:
            TaxInfo_object.Class = names[key]
            TaxInfo_object.Class_TaxId = key

        elif val == list_of_taxa_ranks[4]:
            TaxInfo_object.Order = names[key]
            TaxInfo_object.Order_TaxId = key

        elif val == list_of_taxa_ranks[5]:
            TaxInfo_object.Family = names[key]
            TaxInfo_object.Family_TaxId = key

        elif val == list_of_taxa_ranks[6]:
            TaxInfo_object.Genus = names[key]
            TaxInfo_object.Genus_TaxId = key

        elif val == list_of_taxa_ranks[7]:
            TaxInfo_object.Species = names[key]
            TaxInfo_object.Species_TaxId = key

# fill in the blanks
    if TaxInfo_object.Superkingdom is None:
        TaxInfo_object.Superkingdom = "unk_sk"

    if TaxInfo_object.Kingdom is None:
        TaxInfo_object.Kingdom = "unk_k"

    if TaxInfo_object.Phylum is None:
        TaxInfo_object.Phylum = "unk_p"

    if TaxInfo_object.Class is None:
        TaxInfo_object.Class = "unk_c"

    if TaxInfo_object.Order is None:
        TaxInfo_object.Order = "unk_o"

    if TaxInfo_object.Family is None:
        TaxInfo_object.Family = "unk_f"

    if TaxInfo_object.Genus is None:
        TaxInfo_object.Genus = "unk_g"

    if TaxInfo_object.Species is None:
        TaxInfo_object.Species = "unk_s"
