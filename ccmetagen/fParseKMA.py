#!/usr/bin/env ipython
# -*- coding: utf-8 -*-

"""
Functions to parse KMA results

@ V.R.Marcelino
Created on 1 Aug 2018.
"""

import re

# local imports
from ccmetagen import cTaxInfo, fNCBItax

# function to filter a res file in pandas df format:
def res_filter(df, cov, Iden, Depth, p):
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
def populate_w_tax(
    in_df,
    ref_database,
    species_threshold,
    genus_threshold,
    family_threshold,
    order_threshold,
    class_threshold,
    phylum_threshold,
    taxfile=None,
):
    # For default thresholds, see ccmetagen/__init__.py

    # Make sure all taxa columns are strings (doesn't automatically happen if the first one is None)
    in_df = in_df.assign(
        LCA_TaxId="",
        Superkingdom="",
        Kingdom="",
        Phylum="",
        Class="",
        Order="",
        Family="",
        Genus="",
        Species="",
    )

    # index == the #template (fungal match)
    for index, row in in_df.iterrows():
        match_info = cTaxInfo.TaxInfo()

        # define the tax. rank based on similarity:
        if ref_database == "UNITE":
            split_match = re.split(r"(\|| )", index)
            qiden = row["Query_Identity"]
            match_info.Lineage = split_match[12]

            # if taxid is knwon:
            if split_match[4] != "unk_taxid":
                match_info.TaxId = int(split_match[4])
                match_info = fNCBItax.lineage_extractor(
                    match_info.TaxId, match_info, taxfile
                )

                # Warning about unknown taxids:
            else:
                print("")
                print(
                    "WARNING: based on accession number, no taxonomic information was found in NCBI for %s"
                    % (match_info.Lineage)
                )
                print("This match will not get NCBItax taxonomic ranks")
                print("")
                match_info.TaxId = split_match[4]  # 'unk_taxid'

        elif ref_database == "RefSeq":
            split_match = re.split(r"(\|| )", index)
            qiden = row["Query_Identity"]
            match_info.TaxId = int(split_match[4])
            species = split_match[6] + " " + split_match[8]
            match_info.Lineage = species
            # include info from NCBI:
            match_info = fNCBItax.lineage_extractor(
                match_info.TaxId, match_info, taxfile
            )

        elif ref_database == "nt":
            split_match = re.split(r"(\|| )", index)
            qiden = row["Query_Identity"]
            match_info.Lineage = split_match[2]

            # get taxid from accession number
            taxid = split_match[0]

            if taxid == "unk_taxid":
                # Warning about unknown taxids:
                print("")
                print(
                    "WARNING: no NCBI's taxid found for accession %s"
                    % (match_info.Lineage)
                )
                print("This match will not get taxonomic ranks")
                print("")

            else:
                match_info.TaxId = int(taxid)
                match_info = fNCBItax.lineage_extractor(
                    match_info.TaxId, match_info, taxfile
                )

        # Populate the df with lineage info and the LCA taxid:
        in_df.at[index, "Superkingdom"] = match_info.Superkingdom
        in_df.at[index, "Kingdom"] = match_info.Kingdom

        # Assign LCA_taxid. Go to Kingdom if possible:
        in_df.at[index, "LCA_TaxId"] = match_info.Superkingdom_TaxId

        if match_info.Kingdom_TaxId is not None:
            in_df.at[index, "LCA_TaxId"] = match_info.Kingdom_TaxId

        # if it matches to uncultured or unclassified fungus, use the Fungi LCA itaxid:
        if match_info.Kingdom == "Fungi":
            in_df.at[index, "LCA_TaxId"] = 4751

        thresholds = {
            "Phylum": phylum_threshold,
            "Class": class_threshold,
            "Order": order_threshold,
            "Family": family_threshold,
            "Genus": genus_threshold,
            "Species": species_threshold
        }

        for rank, threshold in thresholds.items():
            if qiden >= threshold:
                tax_info_attr = f"{rank}_TaxId"

                in_df.at[index, rank] = getattr(match_info, rank)

                if getattr(match_info, tax_info_attr) is not None:
                    in_df.at[index, "LCA_TaxId"] = getattr(match_info, tax_info_attr)

    return in_df
