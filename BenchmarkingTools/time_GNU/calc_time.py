#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Calculate CPU time
actual CPU time = User + Sys
@ V.R.Marcelino
Created on Wed Jan  2 10:01:15 2019
"""


#import time
import re
import pandas as pd


# load files
kraken_o = "s06.6_kraken.sh.e2637431.txt"

samples = ["1_mtt_fp","2_mtg_fp","3_mtt_fp","4_nanop_fp","5_mtt_ctg_fp","6_mtg_ctg_fp","7_mtt_ctg_fp",
           "8_mtt_fp","9_mtt_ctg_fp",
           "1_mtt_bf","2_mtg_bf","3_mtt_bf","4_nanop_bf","5_mtt_ctg_bf","6_mtg_ctg_bf","7_mtt_ctg_bf",
           "8_mtt_bf","9_mtt_ctg_bf",
           "1_mtt_nt","2_mtg_nt","3_mtt_nt","4_nanop_nt","5_mtt_ctg_nt","6_mtg_ctg_nt","7_mtt_ctg_nt",
           "8_mtt_nt","9_mtt_ctg_nt"]

ref_databases = ["RefSeq fungi partial", "RefSeq bf", "nt"] 

# dict to store results:
results_dict = {}


# create new dataframe:
time_results = pd.DataFrame()

counter = 0

program = "kraken"
output = "kraken_results"

with open(kraken_o) as o:
    for line in o:
        if line.startswith("user"):
            
            ### get user time (min)
            split = re.split(r'(\t|\n|m|s)', line)
            # convert secs to mins
            um1=float(split[6]) * 0.0166667
            #total user time in min:
            um = float(split[4]) + um1
            
            ### get sys time (min)
            sys_str = next(o)
            split = re.split(r'(\t|\n|m|s)', sys_str)
            # convert secs to mins
            sm1=float(split[8]) * 0.0166667
            #total user time in min:
            sm = float(split[6]) + sm1
            
            CPU_time = um + sm
            CPU_time = round(CPU_time, 4)
            
            if 0 <= counter < 9:
                ref = ref_databases[0]
                
            elif 9 <= counter < 18:
                ref = ref_databases[1]
            
            elif 18 <= counter < 27:
                ref = ref_databases[2]
            else:
                print ("number of results don't match")
                
            results = [program, ref, CPU_time]
            sample = samples[counter]
            results_dict[sample] = results
            
            counter += 1
            
df = pd.DataFrame.from_dict(results_dict,orient='index')
out = output + ".csv"
pd.DataFrame.to_csv(df, out)










