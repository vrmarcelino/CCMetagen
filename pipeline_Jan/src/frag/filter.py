#-------------------------------------------------------------------------------
#  \file filter.py
#  \author Jan P Buchmann <jan.buchmann@sydney.edu.au>
#  \copyright 2018 The University of Sydney
#  \version 0.0.0
#  \description
#-------------------------------------------------------------------------------
import io
import os
import sys

from . import template

class Taxon:

  def __init__(self, rank=None, name=None, parent=None):
    self.rank = rank
    self.name = name
    self.parent = parent

class FragFilter:

  def __init__(self):
    self.templates = {}
    self.paired_ends = {}
    self.taxdb = {}

  def parse_templates(self, resfile):
    fh = open(resfile, 'r')
    for i in fh:
      if i[0] != '#':
        cols = i.strip().split()
        templ = template.Template(cols[0])
        self.parse_taxonomy(cols[0].split('|')[4])
        if templ.uid not in self.templates:
          print(templ.uid)
          self.templates[templ.uid] = templ
    fh.close()

    #for i in self.taxdb:
      #print(self.taxdb[i].name, self.taxdb[i], self.taxdb[i].rank, self.taxdb[i].parent)

  def get_lineage(self, name):
    taxon = self.taxdb[name]
    while taxon.parent != None:
      print(taxon.name, taxon.rank, taxon.parent)
      taxon = self.taxdb[taxon.parent.name]
    print(taxon.name, taxon.rank, taxon.parent)

  def parse_taxonomy(self, taxo_string):
    parent = None
    for i in taxo_string.split(';'):
      t = Taxon(i.split("__")[0], i.split("__")[1], parent)
      if t.name not in self.taxdb:
        self.taxdb[t.name] = t
      parent = self.taxdb[t.name]

  def filter(self, fragfile):
    fh = open(fragfile, 'r')
    for i in fh:
      cols = i.strip().split()
