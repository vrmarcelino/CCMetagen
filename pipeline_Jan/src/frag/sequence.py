#-------------------------------------------------------------------------------
#  \file sequence.py
#  \author Jan P Buchmann <jan.buchmann@sydney.edu.au>
#  \copyright 2018 The University of Sydney
#  \version 0.0.0
#  \description
#-------------------------------------------------------------------------------
from . import species

class Sequence:

  def __init__(self):
    self.sequence = None
    self.species = species.Species()
