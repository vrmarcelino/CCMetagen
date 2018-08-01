#!/usr/bin/env ipython
# -*- coding: utf-8 -*-
"""
Functions to parse KMA results

Working with UNITE - ITS at the moment.
-- RefSeq - to be done.

@ V.R.Marcelino
Created on 1 Aug 2018

"""
import re

# local imports
import cTaxInfo
import fNCBItax


# function to filter a res file in pandas df format:
def res_filter(df,cov,Iden,Depth,p):
    df = df.drop(df[df.Template_Coverage < cov].index)
      
    # filter based on identity
    df = df.drop(df[df.Query_Identity < Iden].index)
        
    # filter based on depth
    df = df.drop(df[df.Depth < Depth].index)

    # filter based on p-values
    df = df.drop(df[df.p_value > p].index)
     
    return df



# function that takes as input a pandas dataframe with KMA results 
# and add tax information to results 
def populate_w_tax(in_df, ref_database):

    # similarity thresholds to accept the tax rank:
    species_threshold = 98.41 # Yeast - Vu et al 2016
    genus_threshold = 96.31 # Yeast - Vu et al 2016
    family_threshold = 88.51 # Filamentous fungi - Vu et al 2019
    order_threshold = 81.21 # Filamentous fungi - Vu et al 2019
    class_threshold = 80.91 # Filamentous fungi - Vu et al 2019
    phyllum_threshold = 0  # no data, no filtering
    
    # index == the #template (fungal match)
    for index, row in in_df.iterrows():
    
        split_match = re.split (r'(\|| )', index)
        match_info = cTaxInfo.TaxInfo()

        # define the tax. rank based on similarity:
        qiden = row['Query_Identity']

        if ref_database == "ITS":
            match_info.Lineage = split_match[12]
    
            # if taxid is knwon:
            if split_match[4] != 'unk_taxid':
                
                match_info.TaxId = int(split_match[4])
                match_info = fNCBItax.lineage_extractor(match_info.TaxId , match_info)
                
                # Warning about unknown taxids: 
            else:
                print ("")
                print ("WARNING: based on accession #, no taxonomic information found in NCBI for %s" %(match_info.Lineage))
                print ("This match will not get NCBItax taxonomic ranks")
                print ("")
                match_info.TaxId = split_match[4] # 'unk_taxid'


        elif ref_database == "RefSeq":
            match_info.TaxId = split_match[4]
            species = split_match[6] + " " + split_match[8]
            match_info.Lineage = species
            # include info from NCBI:
            match_info = fNCBItax.lineage_extractor(match_info.TaxId, match_info)


        # Populate the df with lineage info:
        in_df.at[index, 'Kingdom'] = match_info.Kingdom
        in_df.at[index, 'Phylum '] = match_info.Phylum

        if qiden >= class_threshold:
            in_df.at[index, 'Class'] = match_info.Class
    
        if qiden >= order_threshold:
            in_df.at[index, 'Order'] = match_info.Order

        if qiden >= family_threshold:
            in_df.at[index, 'Order'] = match_info.Family
    
        if qiden >= genus_threshold:
            in_df.at[index, 'Genus'] = match_info.Genus
    
        if qiden >= species_threshold:
            in_df.at[index, 'Species'] = match_info.Species

    return in_df






