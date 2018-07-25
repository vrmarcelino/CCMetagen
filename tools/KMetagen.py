#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
KMetagen main script

Version 0.1

@ V.R.Marcelino
Created on Wed Jul 25 17:13:10 2018

"""

# imports
import sys
from argparse import ArgumentParser


# help
if len(sys.argv) == 1:
    print ("")
    print (" KMetagen - Metagenomic analyses")
    print ("")
    print ("Usage: KMetagen.py <options> ")
    print ("")
    print ("")
    sys.exit()



# funcions