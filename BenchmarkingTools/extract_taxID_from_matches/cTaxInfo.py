#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Classes that store taxonomic info from KMA matches and NCBI lineage

Required to parse the results of KMA and store them in the SQLite3 'bench.db'

@ V.R.Marcelino
Created on 12 Jul 2018

"""
### Stores taxid and other info
class tax_info_from_match(): 
    
    def __init__(self, TaxId=None, Lineage=None, Sample=None, RefDatabase=None, 
                 Abundance=None):
        
        # info from matches
        self.TaxId = TaxId
        self.Lineage = Lineage
        self.Sample = Sample
        self.RefDatabase = RefDatabase
        self.Abundance = Abundance




### Stores lineage in ranks using NCBI taxa
class tax_info_from_ncbi(): 
    
    def __init__(self, Kingdom=None, Kingdom_TaxId=None, Phylum=None, 
                 Phylum_TaxId=None, Class=None, Class_TaxId=None,
                 Order=None, Order_TaxId=None, Family=None, Family_TaxId=None,
                 Genus=None, Genus_TaxId=None, Species=None, Species_TaxId=None):

        # info from NCBI
        self.Kingdom = Kingdom
        self.Kingdom_TaxId = Kingdom_TaxId
        self.Phylum = Phylum
        self.Phylum_TaxId = Phylum_TaxId
        self.Class = Class
        self.Class_TaxId = Class_TaxId
        self.Order = Order
        self.Order_TaxId = Order_TaxId
        self.Genus = Genus
        self.Genus_TaxId = Genus_TaxId
        self.Species = Species
        self.Species_TaxId = Species_TaxId

