__version__ = "1.4.3"

# This can be configured
_RANK_THRESHOLDS = {
    "species_threshold": 98.41, # Yeast - Vu et al 2016
    "genus_threshold": 96.31,   # Yeast - Vu et al 2016
    "family_threshold": 88.51,  # Filamentous fungi - Vu et al 2019
    "order_threshold": 81.21,   # Filamentous fungi - Vu et al 2019
    "class_threshold": 80.91,   # Filamentous fungi - Vu et al 2019
    "phylum_threshold": 0,      # no data, no filtering    
}
_ARGPARSE_DEFAULTS = {
    "mode": "both",
    "output_fp": "CCMetagen_out",
    "reference_database": "nt",
    "extended_output_file": "n",
    "depth_unit": "kma",
    "mapstat": None,
    "depth": 0.2,
    "coverage": 20,
    "query_identity": 50,
    "pvalue": 0.05,
    "krona_mode": "Depth",
    "local_taxfile": None,
    "turn_off_sim_thresholds": "n",
    **_RANK_THRESHOLDS,
}

__all__ = ["__version__", "_ARGPARSE_DEFAULTS", "_RANK_THRESHOLDS"]
