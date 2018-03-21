#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
#  \file fragfilter.py
#  \author Jan P Buchmann <jan.buchmann@sydney.edu.au>
#  \copyright 2018 The University of Sydney
#  \version 0.0.0
#  \description
#-------------------------------------------------------------------------------
import io
import os
import sys

#local imports
from frag import filter

def main():
  f = filter.FragFilter()
  f.parse_templates(sys.argv[1])
  for i in f.templates:
    f.get_lineage(f.templates[i].species.name)
    print("--------------------")
  f.get_lineage('Hymenochaetaceae')
  return 0

if __name__ == '__main__':
  main()
