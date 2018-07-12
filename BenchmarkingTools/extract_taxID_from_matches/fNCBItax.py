#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Function that takes a taxid as input and returns a class containing the taxonomic info and taxids 
for multiple taxonomic ranks. 

Required to parse the results of KMA and store them in the SQLite3 'bench.db'

@ V.R.Marcelino
Created on 12 Jul 2018

"""

from ete3 import NCBITaxa
ncbi = NCBITaxa()
import cTaxInfo # custom script where we store classes used here


def lineage_extractor(query_taxid):
    list_of_taxa_ranks = ['kingdom', 'phylum', 'class', 'order', 'family','genus', 'species']
    lineage = ncbi.get_lineage(query_taxid)
    ranks = ncbi.get_rank(lineage)
    names = ncbi.get_taxid_translator(lineage)

    tax_info = cTaxInfo.tax_info_from_ncbi()

    for key, val in ranks.items():
        if val == list_of_taxa_ranks[0]:
            tax_info.Kingdom = names[key]
            tax_info.Kingdom_TaxId = key
            
        elif val == list_of_taxa_ranks[1]:
            tax_info.Phylum = names[key]
            tax_info.Phylum_TaxId = key
            
        elif val == list_of_taxa_ranks[2]:
            tax_info.Class = names[key]
            tax_info.Class_TaxId = key
            
        elif val == list_of_taxa_ranks[3]:
            tax_info.Order = names[key]
            tax_info.Order_TaxId = key
        
        elif val == list_of_taxa_ranks[4]:
            tax_info.Class = names[key]
            tax_info.Class_TaxId = key
            
        elif val == list_of_taxa_ranks[5]:
            tax_info.Genus = names[key]
            tax_info.Genus_TaxId = key
            
        elif val == list_of_taxa_ranks[6]:
            tax_info.Species = names[key]
            tax_info.Species_TaxId = key
    return tax_info


