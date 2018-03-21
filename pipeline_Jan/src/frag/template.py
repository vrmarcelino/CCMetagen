#-------------------------------------------------------------------------------
#  \file template.py
#  \author Jan P Buchmann <jan.buchmann@sydney.edu.au>
#  \copyright 2018 The University of Sydney
#  \version 0.0.0
#  \description
#-------------------------------------------------------------------------------
from . import species

class Template:

  def __init__(self, descr):
    self.uid = None
    self.descr = None
    self.score = None
    self.expected = None
    self.length_coverage = None
    self.depth = None
    self.qval = None
    self.pval = None
    self.species = species.Species()
    self.parse(descr)

  def parse(self, cols):
    self.species.update(cols.split('|')[:4])
    self.uid = self.species.uid
    self.description = self.species.description
    self.score = cols[1]
    self.expected = cols[2]
    self.length_coverage = cols[3]
    self.depth = cols[4]
    self.qval = cols[5]
    self.pval = cols[6]
