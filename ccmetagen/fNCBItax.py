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


def lineage_extractor(query_taxid, TaxInfo_object, taxfile=None):
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
    if taxfile is not None:
        ncbi = NCBITaxa(taxfile)
    else:
        ncbi = NCBITaxa()
    lineage = ncbi.get_lineage(query_taxid)
    ranks = ncbi.get_rank(lineage)
    names = ncbi.get_taxid_translator(lineage)

    # get known data
    for key, val in ranks.items():
        for rank in list_of_taxa_ranks:
            if val == rank:
                setattr(TaxInfo_object, rank, names[key])
                setattr(TaxInfo_object, rank + "_TaxId", key)

    # fill in the blanks
    for attr in list_of_taxa_ranks:
        if getattr(TaxInfo_object, attr) is None:
            initial = attr.lower()[0] if attr != "Superkingdom" else "sk"
            setattr(TaxInfo_object, attr, "unk_" + initial)

    return TaxInfo_object
