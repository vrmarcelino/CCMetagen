#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Function that takes a taxid as input and returns a class containing the taxonomic info and taxids
for multiple taxonomic ranks.

Required to parse the results of KMA and store them in the SQLite3 'bench.db'

@ V.R.Marcelino
Created on 12 Jul 2018.
"""

from ete3 import NCBITaxa

list_of_taxa_ranks = [
    "Superkingdom",
    "Kingdom",
    "Phylum",
    "Class",
    "Order",
    "Family",
    "Genus",
    "Species",
]

# NCBI rank names -> CCMetagen output column.
# In 2025 NCBI renamed the 'superkingdom' rank to 'domain' (Bacteria, Archaea,
# Eukaryota), so both are mapped to the Superkingdom column to support old and
# new ete3 taxonomy databases.
rank_to_column = {rank.lower(): rank for rank in list_of_taxa_ranks}
rank_to_column["domain"] = "Superkingdom"

# Viruses no longer have a superkingdom/domain rank in the new NCBI taxonomy
# (the 'Viruses' node was moved to a root-level rank), so they are identified
# by taxid instead, keeping 'Viruses' in the Superkingdom column as before.
VIRUSES_TAXID = 10239


def lineage_extractor(query_taxid, TaxInfo_object, taxfile=None):
    if taxfile is not None:
        ncbi = NCBITaxa(taxfile)
    else:
        ncbi = NCBITaxa()
    lineage = ncbi.get_lineage(query_taxid)
    ranks = ncbi.get_rank(lineage)
    names = ncbi.get_taxid_translator(lineage)

    # get known data
    for key, val in ranks.items():
        rank = rank_to_column.get(val.lower())
        if rank is not None:
            setattr(TaxInfo_object, rank, names[key])
            setattr(TaxInfo_object, rank + "_TaxId", key)

    if TaxInfo_object.Superkingdom is None and VIRUSES_TAXID in lineage:
        TaxInfo_object.Superkingdom = names[VIRUSES_TAXID]
        TaxInfo_object.Superkingdom_TaxId = VIRUSES_TAXID

    # fill in the blanks
    for attr in list_of_taxa_ranks:
        if getattr(TaxInfo_object, attr) is None:
            initial = attr.lower()[0] if attr != "Superkingdom" else "sk"
            setattr(TaxInfo_object, attr, "unk_" + initial)

    return TaxInfo_object
