"""
..
  Copyright 2020 The University of Sydney

.. moduleauthor:: Jan P Buchmann <jan.buchmann@sydney.edu.au>
"""


import sys
import subprocess
import setuptools

sys.path.insert(1, 'ccmetagen')
import version


setuptools.setup(version=version.get_version())


