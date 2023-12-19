#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
CCMetagen main script

@ V.R.Marcelino
Created on Wed Jul 25 17:13:10 2018.
"""

# imports
import sys
import pandas as pd
import argparse
import subprocess
import os
from ete3 import NCBITaxa
import re

# local imports
from ccmetagen import __version__, _ARGPARSE_DEFAULTS, fParseKMA

# version formatting
version_numb = "v" + __version__

# help
if __name__ == "__main__":
    if len(sys.argv) == 1:
        print("")
        print("CCMetagen - Identify species in metagenome datasets")
        print(version_numb)
        print("To be used with KMA")
        print("")
        print("Usage: CCMetagen.py <options> ")
        print("Ex: CCMetagen.py -i KMA_out/2_mtg.res -o 2_mtg_result")
        print("")
        print("")
        print(
            """When running CCMetagen on multiple files in a folder:
    input_dir=KMA_out
    output_dir=CCMetagen_results
    mkdir $output_dir
    for f in $input_dir/*.res; do
        out=$output_dir/${f/$input_dir\\/}
        CCMetagen.py -i $f -o $out
    done"""
        )
        print("")
        print("For help and options, type: CCMetagen.py -h")
        print("")
        print("")
        sys.exit()

    parser = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter
    )

    parser.add_argument(
        "-m",
        "--mode",
        default=_ARGPARSE_DEFAULTS.get("mode"),
        help="""
        What would you like CCMetagen to do?\n
        Valid options are 'visual', 'text' or 'both':\n
            \ttext: parses kma, filters based on quality and output a text file with taxonomic information and detailed mapping information.\n
            \tvisual: parses kma, filters based on quality and output a simplified text file and a krona html file for visualization.\n
            \tboth: outputs both text and visual file formats.
            """,
        required=False,
    )

    parser.add_argument(
        "-i", "--res_fp", help="Path to the KMA result (.res file)", required=True
    )
    parser.add_argument(
        "-o",
        "--output_fp",
        default=_ARGPARSE_DEFAULTS.get("output_fp"),
        help="Path to the output file.",
        required=False,
    )
    parser.add_argument(
        "-r",
        "--reference_database",
        default=_ARGPARSE_DEFAULTS.get("reference_database"),
        help="Which reference database was used. Options: UNITE, RefSeq or nt.",
        required=False,
    )
    parser.add_argument(
        "-ef",
        "--extended_output_file",
        default=_ARGPARSE_DEFAULTS.get("extended_output_file"),
        help="""Produce an extended output file that includes the percentage of classified reads.
                        Options: y or n. To use this featire, you need to generate the mapstat file when
                        required unning KMA (use flag -ef), and use it as input in CCMetagen (flag --mapstat). 
                        """,
        required=False,
    )

    parser.add_argument(
        "-du",
        "--depth_unit",
        default=_ARGPARSE_DEFAULTS.get("depth_unit"),
        help="""Desired unit for Depth(abundance) measurements.
                        Default = kma (KMA default depth, which is the number of nucleotides overlapping each template,
                        divided by the lengh of the template).
                        Alternatively, you can have abundance calculated in Reads Per Million (RPM, option 'rpm'), 
                        in number of nucleotides overlaping the template (option 'nc') or in number of fragments (i.e. PE reads, option 'fr').
                        If you use the 'nc', 'rpm' or 'fr' options, remember to change the default --depth parameter accordingly.
                        Valid options are 'nc', 'rpm', 'fr' and 'kma'.""",
        required=False,
    )
    parser.add_argument(
        "-map",
        "--mapstat",
        default=_ARGPARSE_DEFAULTS.get("mapstat"),
        help="""Path to the mapstat file produced with KMA when using the -ef flag (.mapstat).
                        Required when calculating abundances in RPM or in number of fragments, visualing the abundances in readCounts or readContAln
                        for the krona graph or when producing the extended_output_file.""",
        required=False,
    )
    parser.add_argument(
        "-d",
        "--depth",
        default=_ARGPARSE_DEFAULTS.get("depth"),
        help="""Minimum sequencing depth. The unit corresponds to the one used with --depth_unit
                        If you use --depth_unit different from the default, change this accordingly.
                        """,
        type=float,
        required=False,
    )
    parser.add_argument(
        "-c",
        "--coverage",
        default=_ARGPARSE_DEFAULTS.get("coverage"),
        help="""Percetange of minimum coverage, e.g. 20 means 20%% of the reference sequence.""",
        type=float,
        required=False,
    )
    parser.add_argument(
        "-q",
        "--query_identity",
        default=_ARGPARSE_DEFAULTS.get("query_identity"),
        help="Minimum query identity (Phylum level).",
        type=float,
        required=False,
    )
    parser.add_argument(
        "-p",
        "--pvalue",
        default=_ARGPARSE_DEFAULTS.get("pvalue"),
        help="Minimum p-value.",
        type=float,
        required=False,
    )
    parser.add_argument(
        "-k",
        "--krona_mode",
        default=_ARGPARSE_DEFAULTS.get("krona_mode"),
        help="""Abundance measure for the Krona graph. 
                        You can choose depth ('Depth'), readCount ('rc') or readCountAln ('rca').
                        'rc' and 'rca' require a specified --mapstat file.
                        """,
        required=False,
    )
    parser.add_argument(
        "-tax",
        "--local_taxfile",
        default=_ARGPARSE_DEFAULTS.get("local_taxfile"),
        help="Use if a local taxdump file wants to be used.",
        required=False,
    )

    # similarity thresholds:
    parser.add_argument(
        "-st",
        "--species_threshold",
        default=_ARGPARSE_DEFAULTS.get("species_threshold"),
        help="Species-level similarity threshold.",
        type=float,
        required=False,
    )
    parser.add_argument(
        "-gt",
        "--genus_threshold",
        default=_ARGPARSE_DEFAULTS.get("genus_threshold"),
        help="Genus-level similarity threshold.",
        type=float,
        required=False,
    )
    parser.add_argument(
        "-ft",
        "--family_threshold",
        default=_ARGPARSE_DEFAULTS.get("family_threshold"),
        help="Family-level similarity threshold.",
        type=float,
        required=False,
    )
    parser.add_argument(
        "-ot",
        "--order_threshold",
        default=_ARGPARSE_DEFAULTS.get("order_threshold"),
        help="Order-level similarity threshold.",
        type=float,
        required=False,
    )
    parser.add_argument(
        "-ct",
        "--class_threshold",
        default=_ARGPARSE_DEFAULTS.get("class_threshold"),
        help="Class-level similarity threshold.",
        type=float,
        required=False,
    )
    parser.add_argument(
        "-pt",
        "--phylum_threshold",
        default=_ARGPARSE_DEFAULTS.get("phylum_threshold"),
        help="Phylum-level similarity threshold. 0 means not applied.",
        type=float,
        required=False,
    )
    parser.add_argument(
        "-off",
        "--turn_off_sim_thresholds",
        default=_ARGPARSE_DEFAULTS.get("turn_off_sim_thresholds"),
        help="Turns simularity-based filtering off. Options = 'y' or 'n'.",
        required=False,
    )

    parser.add_argument("-v", "--version", action="version", version=version_numb)

    args = parser.parse_args()

    mode = args.mode
    f = args.res_fp
    ref_database = args.reference_database
    c = args.coverage
    q = args.query_identity
    du = args.depth_unit
    d = args.depth
    p = args.pvalue
    mapstat = args.mapstat
    ef = args.extended_output_file
    k = args.krona_mode
    taxfile = args.local_taxfile
    if taxfile is not None and not os.path.isfile(taxfile):
        raise ValueError("If used, the argument taxfile has to point to a taxdump file")

    # taxonomic thresholds:
    off = args.turn_off_sim_thresholds

    if off == "y":
        st = 0
        gt = 0
        ft = 0
        ot = 0
        ct = 0
        pt = 0

    elif off == "n":
        st = args.species_threshold
        gt = args.genus_threshold
        ft = args.family_threshold
        ot = args.order_threshold
        ct = args.class_threshold
        pt = args.phylum_threshold

    else:
        print("-off argument should be either y or n. ")
        sys.exit("Try again.")

    # developing and debugging:
    # args.output_fp = "CCMetagen_nt_results"
    # f = "sim_metagen.res"
    # mapstat="sim_metagen.mapstat"
    # ref_database = "nt"
    # mode = 'text'
    # c = 20
    # q = 50
    # d = 0.2
    # p = 0.05
    # st = 99
    # gt = 98
    # ft = 95
    # ot = 80
    # ct = 0
    # pt = 0
    # du = 'kma'
    # ef = 'y' # extended format - add a flag, default = 'n'
    # k = 'Depth'

    ##### Checks:

    # Run implicitly ete3.NCBITaxa.__init__() to check for valid taxonomy database
    # NCBITaxa()
    if taxfile is not None:
        NCBITaxa(taxfile)
    else:
        NCBITaxa()

    # Warning if RefDatabase is unknown
    if ref_database not in ("UNITE", "RefSeq", "nt"):
        print(
            """ Reference database (-r) must be either UNITE, RefSeq or nt.
            the input is case sensitive and the default is nt."""
        )
        sys.exit("Try again.")

    # check if ef flag is correct
    if ef not in ("y", "n"):
        print(
            "Unrecognized argument %s. Use either '-ef n' (default) or '-ef y'" % (ef)
        )
        sys.exit("Try again.")

    ##### Read input files and output a pandas dataframe
    print("")
    print("Reading file %s" % (f))
    print("")

    df = pd.read_csv(f, sep="\t", index_col=0, encoding="latin1")

    # Rename headers:
    df.index.name = "Closest_match"

    ##### Adjust depth to reflect number of bases or RPM if needed:

    # number of nucleotides:
    if du == "nc":
        df["Depth"] = df.Depth * df.Template_length
        print("Calculating depth as number of nucleotides, ignoring template length.")
        print(
            """Remember to adjust minimum depth value (ex: -d 200) to filter low abundance hits."""
        )

    # RPM:
    elif du == "rpm":
        print("Calculating RPM...")
        print(
            """
            Note 1: to calculate RPM, you need to generate the mapstat file when
            running KMA (flag -ef), and use it as input in CCMetagen (flag --mapstat).
            
            Note 2: you might want to adjust the minimum depth (-d) value accordingly.
            The default minimum depth is 0.2.
            """
        )

        with open(mapstat) as mapfile:
            fragments_line = mapfile.readlines()[3]
        total_frags = re.split(r"(\t|\n)", fragments_line)[2]
        df_stats = pd.read_csv(
            mapstat, sep="\t", index_col=0, header=6, encoding="latin1"
        )
        df["Depth"] = 1000000 * df_stats["fragmentCount"] / int(total_frags)

    # number of PE reads (frags):
    elif du == "fr":
        print("Calculating number of PE reads (fragments)")
        print(
            """
            Note 1: to calculate number of fragments, you need to generate the mapstat file when
            running KMA (flag -ef), and use it as input in CCMetagen (flag --mapstat).
            
            Note 2: you might want to adjust the minimum depth (-d) value accordingly.
            Ex: Use -d 2 to only consider matches with 2 fragments or more.
            """
        )

        with open(mapstat) as mapfile:
            fragments_line = mapfile.readlines()[3]
        total_frags = re.split(r"(\t|\n)", fragments_line)[2]
        df_stats = pd.read_csv(
            mapstat, sep="\t", index_col=0, header=6, encoding="latin1"
        )
        df["Depth"] = df_stats["fragmentCount"]

    elif du == "kma":
        print("")

    else:
        print(
            """Warning: the depth unit you specified makes no sense.
            --depth_unit option must be nc, rpm, fr or kma. Using 'kma'."""
        )
        print("")

    ##### Quality control + taxonomic assignments

    # quality filter (coverage, query identity, Depth and p-value)
    df = fParseKMA.res_filter(df, ref_database, c, q, d, p)

    # add tax info
    df = fParseKMA.populate_w_tax(df, ref_database, st, gt, ft, ot, ct, pt)

    ##### Output a file with tax info
    if (mode == "text") or (mode == "both"):
        # save to file
        out = args.output_fp + ".ccm.csv"
        pd.DataFrame.to_csv(df, out)

        print("csv file saved as %s" % (out))
        print("")

    ##### Output a Krona file based on specified mode
    if (mode == "visual") or (mode == "both"):
        # ReadCount (number of reads mapped to the template)
        if k == "rc":
            if mapstat is not None:
                print("Extracting read count from mapstat file")
                # load mapstat file if needed
                if du == "kma" or du == "nc":
                    print(mapstat)
                    df_stats = pd.read_csv(
                        mapstat, sep="\t", index_col=0, header=6, encoding="latin1"
                    )

                df["readCount"] = df_stats["readCount"]
                krona_info = df[
                    [
                        "readCount",
                        "Superkingdom",
                        "Kingdom",
                        "Phylum",
                        "Class",
                        "Order",
                        "Family",
                        "Genus",
                        "Species",
                    ]
                ]
            else:
                print("""Error, no mapstat file specified""")
                print(
                    """To calculate the read count for this krona mode, you need to generate the mapstat file when
                running KMA (flag -ef), and use it as input in CCMetagen (flag --mapstat).
                """
                )
                print("")

        # ReadCountAln (number of reads aligned)
        elif k == "rca":
            if mapstat is not None:
                print("Extracting read count alignment from mapstat file")
                # load mapstat file if needed
                if du == "kma" or du == "nc":
                    df_stats = pd.read_csv(
                        mapstat, sep="\t", index_col=0, header=6, encoding="latin1"
                    )

                df["readCountAln"] = df_stats["readCountAln"]
                krona_info = df[
                    [
                        "readCountAln",
                        "Superkingdom",
                        "Kingdom",
                        "Phylum",
                        "Class",
                        "Order",
                        "Family",
                        "Genus",
                        "Species",
                    ]
                ]
            else:
                print("""Error, no mapstat file specified""")
                print(
                    """To calculate the read count alignment for this krona mode, you need to generate the mapstat file when
                    running KMA (flag -ef), and use it as input in CCMetagen (flag --mapstat).
                    """
                )
                print("")

        # Depth (default)
        elif k == "Depth":
            krona_info = df[
                [
                    "Depth",
                    "Superkingdom",
                    "Kingdom",
                    "Phylum",
                    "Class",
                    "Order",
                    "Family",
                    "Genus",
                    "Species",
                ]
            ]

        else:
            print(
                """Error: Invalid --krona_mode argument. 
            Possible arguments: rc, rca, or Depth."""
            )
            print("")

        # remove the unk_xx for better krona representation
        krona_info = krona_info.replace("unk_.*$", value="", regex=True)

        # save dataframe to file
        out1 = args.output_fp + ".tsv"
        pd.DataFrame.to_csv(krona_info, out1, sep="\t", index=False, header=False)

        # save krona file
        out2 = args.output_fp + ".html"

        shell_command = "ktImportText " + out1 + " -o " + out2
        subprocess.run(shell_command, shell=True)

        print("krona file saved as %s" % (out2))
        print("")

    ##### Extended format - calculate read mapping stats
    if ef == "y":
        print("Calculating read mapping stats...")

        with open(mapstat) as mapfile:
            fragments_line = mapfile.readlines()[3]
        total_frags = re.split(r"(\t|\n)", fragments_line)[2]

        ### check if the input was single-end or paired end ###
        with open(mapstat) as mapfile:
            kma_command_line = mapfile.readlines()[5]
        input_file_command = re.split(r"(\t|\n| )", kma_command_line)[6]

        if input_file_command == "-i":
            print("""Parsing results based on single-end sequences.""")
            total_reads = int(total_frags)
        elif input_file_command == "-ipe":
            print(
                """Parsing results based on paired-end sequences.
            Your data should have the same number of reads in the fwd and rev files."""
            )

            total_reads = 2 * int(total_frags)
        else:
            print(
                """Could not identify whether your input files were single- or paired-end. 
                    Treating as paired-end."""
            )
            total_reads = 2 * int(total_frags)
        ###

        df_stats = pd.read_csv(
            mapstat, sep="\t", index_col=0, header=6, encoding="latin1"
        )

        # delete species in df_stats that are not in the CCM result dataframe:
        df_stats_filt = df_stats[
            df_stats.index.isin(df.index)
        ].copy()  # the copy handles the pandas warning
        df_stats_filt["perc_map"] = df_stats_filt["readCount"] / total_reads * 100
        total_mapped = sum(df_stats_filt["perc_map"])

        stats_out = args.output_fp + "_stats.csv"
        pd.DataFrame.to_csv(df_stats_filt, stats_out)

        print("\nStats file saved as %s" % (stats_out))
        print(
            """\nProportion of reads mapped to the database: %f%%\n""" % (total_mapped)
        )
