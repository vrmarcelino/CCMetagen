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
centrifuge_o = "s06.2_centrifuge_all.txt"
krakenUniq_o = "s06.5_krakenUniq_refSeq_all.txt"
kma_o = "s06.1_KMA_all_db.txt"
kmetagen_o = "s06.1.2_KMetagen_all_db.txt"


# save as
output = "results.csv"


def calc_CPU_time(u_line,s_line):
    split = re.split(r'(\t|\n|m|s)', u_line)
    
    # convert secs to mins
    um1=float(split[6]) / 60
    #total user time in min:
    um = float(split[4]) + um1
            
    ### get sys time (min)
    split = re.split(r'(\t|\n|m|s)', s_line)
    # convert secs to mins
    sm1=float(split[8]) / 60
    #total user time in min:
    sm = float(split[6]) + sm1
            
    CPU_time = um + sm
    CPU_time = round(CPU_time, 4)
    return (CPU_time)



# create new dataframe:
time_results = pd.DataFrame(columns=['Sample', 'CPU_time', 'Ref_DB', 'Program'])


samples = ["1_mtt","2_mtg","3_mtt","4_nanop","5_mtt_ctg","6_mtg_ctg","7_mtt_ctg",
           "8_mtt","9_mtt_ctg",
           "1_mtt","2_mtg","3_mtt","4_nanop","5_mtt_ctg","6_mtg_ctg","7_mtt_ctg",
           "8_mtt","9_mtt_ctg",
           "1_mtt","2_mtg","3_mtt","4_nanop","5_mtt_ctg","6_mtg_ctg","7_mtt_ctg",
           "8_mtt","9_mtt_ctg"]



### Kraken2:
counter = 0
program = "kraken"
ref_databases = ["RefSeq_f_partial", "RefSeq_bf", "nt"]

with open(kraken_o) as o:
    for line in o:
        if line.startswith("user"):
            
            ### get user time (min)
            user_line = line
            sys_line = next(o)
            
            CPU_time = calc_CPU_time(user_line,sys_line)
                       
            if 0 <= counter < 9:
                ref = ref_databases[0]
                
            elif 9 <= counter < 18:
                ref = ref_databases[1]
            
            elif 18 <= counter < 27:
                ref = ref_databases[2]
            else:
                print ("number of results don't match")
                
            sample = samples[counter]
            results = pd.Series([sample, CPU_time, ref, program], index=['Sample', 'CPU_time', 'Ref_DB', 'Program'])
            time_results = time_results.append(results,ignore_index=True)
            
            counter += 1



### Centrifuge:
counter = 0
program = "Centrifuge"
ref_databases = ["nt","RefSeq_bf", "RefSeq_f_partial"]


with open(centrifuge_o) as o:
    for line in o:
        if line.startswith("user"):
            
            ### get user time (min)
            user_line = line
            sys_line = next(o)
            
            CPU_time = calc_CPU_time(user_line,sys_line)
                       
            if 0 <= counter < 9:
                ref = ref_databases[0]
                
            elif 9 <= counter < 18:
                ref = ref_databases[1]
            
            elif 18 <= counter < 27:
                ref = ref_databases[2]
            else:
                print ("number of results don't match")
                
            sample = samples[counter]
            results = pd.Series([sample, CPU_time, ref, program], index=['Sample', 'CPU_time', 'Ref_DB', 'Program'])
            time_results = time_results.append(results,ignore_index=True)
            
            counter += 1




### KrakenUniq
counter = 0
program = "KrakenUniq"
ref_databases = ["RefSeq_f_partial","RefSeq_bf"]


with open(krakenUniq_o) as o:
    for line in o:
        if line.startswith("user"):
            
            ### get user time (min)
            user_line = line
            sys_line = next(o)
            
            CPU_time = calc_CPU_time(user_line,sys_line)
                       
            if 0 <= counter < 9:
                ref = ref_databases[0]
                
            elif 9 <= counter < 18:
                ref = ref_databases[1]

            else:
                print ("number of results don't match")
                
            sample = samples[counter]
            results = pd.Series([sample, CPU_time, ref, program], index=['Sample', 'CPU_time', 'Ref_DB', 'Program'])
            time_results = time_results.append(results,ignore_index=True)
            
            counter += 1

##########################
######## KMA and Kmetagen
            
store_kma = []
store_filtering = pd.DataFrame(columns=['Sample', 'CPU_time', 'Ref_DB', 'Program'])

counter = 0
program = "KMetagen"
ref_databases = ["UNITE","RefSeq_f_partial","RefSeq_bf","nt"]
samples = ["2_mtg","3_mtt","4_nanop","6_mtg_ctg","7_mtt_ctg",
           "8_mtt","9_mtt_ctg",
           "1_mtt","2_mtg","3_mtt","4_nanop","5_mtt_ctg","6_mtg_ctg","7_mtt_ctg",
           "8_mtt","9_mtt_ctg",
           "1_mtt","2_mtg","3_mtt","4_nanop","5_mtt_ctg","6_mtg_ctg","7_mtt_ctg",
           "8_mtt","9_mtt_ctg",
           "1_mtt","2_mtg","3_mtt","4_nanop","5_mtt_ctg","6_mtg_ctg","7_mtt_ctg",
           "8_mtt","9_mtt_ctg"]

# save KMA's time to a list
with open(kma_o) as o:
    for line in o:
        if line.startswith("user"):
            
            ### get user time (min)
            user_line = line
            sys_line = next(o)

            CPU_time = calc_CPU_time(user_line,sys_line)
                       
            store_kma.append(CPU_time)

# then add it to Kmetagen's CPU time:
with open(kmetagen_o) as o:
    for line in o:
        if line.startswith("user"):
            
            ### get user time (min)
            user_line = line
            sys_line = next(o)
            
            CPU_time_filtering = calc_CPU_time(user_line,sys_line)
            KMA_time = store_kma[counter]
            CPU_time = CPU_time_filtering + KMA_time
            
            if 0 <= counter < 7:
                ref = ref_databases[0]
                
            elif 7 <= counter < 16:
                ref = ref_databases[1]
                
            elif 16 <= counter < 25:
                ref = ref_databases[2]
                
            elif 25 <= counter < 34:
                ref = ref_databases[3]
                
            else:
                print ("number of results don't match")
                
            sample = samples[counter]
            results = pd.Series([sample, CPU_time, ref, program], index=['Sample', 'CPU_time', 'Ref_DB', 'Program'])
            time_results = time_results.append(results,ignore_index=True)
            
            counter += 1



pd.DataFrame.to_csv(time_results, output)







