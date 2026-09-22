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


def parse_mapstat_header(mapstat_fp):
    """Parse the '## key\\tvalue' metadata lines at the top of a KMA .mapstat file.

    Returns a (metadata, header_row) tuple: metadata is a dict of the '##'-tagged
    key/value pairs (e.g. metadata["fragmentCount"], metadata["command"]), and
    header_row is the 0-indexed line number of the '#refSequence  readCount  ...'
    column header line, for use as pandas.read_csv(mapstat_fp, header=header_row).

    KMA has changed how many '##' metadata lines it writes between versions --
    for example, newer versions add a '## command' line recording the kma
    invocation, which pushes the column header line down by one. Parsing by key
    name instead of assuming a fixed line number keeps this working regardless of
    how many '##' lines a given KMA version writes.
    """
    metadata = {}
    with open(mapstat_fp, encoding="latin1") as mapfile:
        for i, line in enumerate(mapfile):
            if line.startswith("##"):
                key, _, value = line[2:].strip().partition("\t")
                metadata[key.strip()] = value.strip()
            elif line.startswith("#"):
                return metadata, i
    raise ValueError(
        f"Could not find the column header line (starting with '#') in {mapstat_fp}"
    )


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
    # Force plain object dtype rather than pandas' newer strict StringDtype.
    # These columns hold a mix of types across rows (e.g. LCA_TaxId is usually
    # set to an int NCBI taxid below, but can also be the string 'unk_taxid').
    # pandas >=3.0 infers a strict string dtype from the "" values above, which
    # then raises TypeError the first time an int is assigned into it.
    tax_columns = [
        "LCA_TaxId",
        "Superkingdom",
        "Kingdom",
        "Phylum",
        "Class",
        "Order",
        "Family",
        "Genus",
        "Species",
    ]
    in_df = in_df.astype({col: object for col in tax_columns})

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
