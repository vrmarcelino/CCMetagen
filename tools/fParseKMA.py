#!/usr/bin/env ipython
# -*- coding: utf-8 -*-
"""
Functions to parse KMA results

@ V.R.Marcelino
Created on 1 Aug 2018


"""
import re

# local imports
import cTaxInfo
import fNCBItax
import subprocess

# function to filter a res file in pandas df format:
def res_filter(df,ref_database, cov,Iden,Depth,p):
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
def populate_w_tax(in_df, ref_database,species_threshold,genus_threshold,
                   family_threshold,order_threshold,class_threshold,phylum_threshold):
    #defaults:
    #species_threshold = 98.41 # Yeast - Vu et al 2016
    #genus_threshold = 96.31 # Yeast - Vu et al 2016
    #family_threshold = 88.51 # Filamentous fungi - Vu et al 2019
    #order_threshold = 81.21 # Filamentous fungi - Vu et al 2019
    #class_threshold = 80.91 # Filamentous fungi - Vu et al 2019
    #phylum, kingdom and superkingdom = 0  # no data, no filtering


    # Make sure all taxa columns are strings (doesn't automatically happen if the first one is None)
    in_df = in_df.assign(LCA_TaxId="",Superkingdom="",Kingdom="",Phylum="",Class="",Order="",Family="",Genus="",Species="")


    # index == the #template (fungal match)
    for index, row in in_df.iterrows():
        match_info = cTaxInfo.TaxInfo()

        # define the tax. rank based on similarity:
        if ref_database == "UNITE":
            split_match = re.split (r'(\|| )', index)
            qiden = row['Query_Identity']
            match_info.Lineage = split_match[12]

            # if taxid is knwon:
            if split_match[4] != 'unk_taxid':
                
                match_info.TaxId = int(split_match[4])
                match_info = fNCBItax.lineage_extractor(match_info.TaxId , match_info)
                
                # Warning about unknown taxids: 
            else:
                print ("")
                print ("WARNING: based on accession number, no taxonomic information was found in NCBI for %s" %(match_info.Lineage))
                print ("This match will not get NCBItax taxonomic ranks")
                print ("")
                match_info.TaxId = split_match[4] # 'unk_taxid'


        elif ref_database == "RefSeq":
            split_match = re.split (r'(\|| )', index)
            qiden = row['Query_Identity']
            match_info.TaxId = int(split_match[4])
            species = split_match[6] + " " + split_match[8]
            match_info.Lineage = species
            # include info from NCBI:
            match_info = fNCBItax.lineage_extractor(match_info.TaxId, match_info)


        elif ref_database == "nt":
            split_match = re.split (r'(\|| )', index)
            qiden = row['Query_Identity']
            match_info.Lineage = split_match[4] + " " + split_match[6]
            
            #get taxid from accession number
            taxid = split_match[0]

            if taxid == 'unk_taxid':
                # Warning about unknown taxids: 
                print ("")
                print ("WARNING: no NCBI's taxid found for accession %s" %(match_info.Lineage))
                print ("This match will not get taxonomic ranks")
                print ("")
                
            else:
                match_info.TaxId = int(taxid)            
                match_info = fNCBItax.lineage_extractor(match_info.TaxId, match_info)
   
            
        # Populate the df with lineage info and the LCA taxid:
        # Assign LCA_taxid and lower rank taxa.  Go to Kingdom if possible:

        in_df.at[index, 'Superkingdom'] = match_info.Superkingdom
        in_df.at[index, 'LCA_TaxId'] = match_info.Superkingdom_TaxId
        
        if match_info.Superkingdom is None:
            match_info.Superkingdom = "unk_sk"
           
        in_df.at[index, 'Kingdom'] = match_info.Kingdom
        if match_info.Kingdom_TaxId is not None:
            in_df.at[index, 'LCA_TaxId'] = match_info.Kingdom_TaxId            
        else:
            in_df.at[index, 'Kingdom'] = str(match_info.Superkingdom) + ";_unk_k"

        # if it matches to uncultured or unclassified fungus, use the Fungi LCA itaxid:
        if match_info.Kingdom == 'Fungi':
            in_df.at[index, 'LCA_TaxId'] = 4751



        # fill in the rest of the table according to similarity threshold:
        if qiden >= phylum_threshold:
            if match_info.Phylum_TaxId != None:
                in_df.at[index, 'Phylum'] = match_info.Phylum
                in_df.at[index, 'LCA_TaxId'] = match_info.Phylum_TaxId
            else:
                in_df.at[index, 'Phylum'] = str(match_info.Kingdom) + ";_unk_p"

        if qiden >= class_threshold:
            in_df.at[index, 'Class'] = match_info.Class
            if match_info.Class_TaxId != None:
                in_df.at[index, 'LCA_TaxId'] = match_info.Class_TaxId
    
        if qiden >= order_threshold:
            in_df.at[index, 'Order'] = match_info.Order
            if match_info.Order_TaxId != None:
                in_df.at[index, 'LCA_TaxId'] = match_info.Order_TaxId

        if qiden >= family_threshold:
            in_df.at[index, 'Family'] = match_info.Family
            if match_info.Family_TaxId != None:
                in_df.at[index, 'LCA_TaxId'] = match_info.Family_TaxId
    
        if qiden >= genus_threshold:
            in_df.at[index, 'Genus'] = match_info.Genus
            if match_info.Genus_TaxId != None:
                in_df.at[index, 'LCA_TaxId'] = match_info.Genus_TaxId
    
        if qiden >= species_threshold:
            in_df.at[index, 'Species'] = match_info.Species
            if match_info.Species_TaxId != None:
                in_df.at[index, 'LCA_TaxId'] = match_info.Species_TaxId
    
    return in_df



