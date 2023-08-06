# -*- coding: utf-8 -*-

"""Top-level package for LSDTopyTools."""

__author__ = """Boris Gailleton"""
__email__ = 'b.gailleton@sms.ed.ac.uk'
__version__ = '0.0.1'
import sys
# Dealing with the imports: making it compatible with python 3 and 2
if(sys.version[0] == 2):
	from main_window import *


else:
	from .main_window import *

