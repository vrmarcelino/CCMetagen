"""
..
  Copyright 2020 The University of Sydney

.. moduleauthor:: Jan P Buchmann <jan.buchmann@sydney.edu.au>
"""

major = 1
minor = 1
micro = 5
revision = None

def get_version():
  if revision:
    return "{}.{}.{}+{}".format(major, minor, micro, revision)
  return "{}.{}.{}".format(major, minor, micro)
