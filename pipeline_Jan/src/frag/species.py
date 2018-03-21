#-------------------------------------------------------------------------------
#  \file species.py
#  \author Jan P Buchmann <jan.buchmann@sydney.edu.au>
#  \copyright 2018 The University of Sydney
#  \version 0.0.0
#  \description
#-------------------------------------------------------------------------------
class Species:

  def __init__(self):
    self.name = None
    self.ncbi_accession = None
    self.parent = None
    self.uid = None
    self.description = None
    self.taxon = None

  def update(self, fields):
    print(fields)
    self.name = fields[0]
    self.ncbi_accesion = fields[1]
    self.uid = fields[2]
    self.description = fields[3]
