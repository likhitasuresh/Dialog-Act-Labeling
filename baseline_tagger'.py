# -*- coding: utf-8 -*-
"""
Created on Sat Apr 11 12:45:35 2020

@author: Likhita Suresh
"""

import pycrfsuite
import hw2_corpus_tools as tools
import os

path = os.getcwd()+"\\trainSmall"
print (path)

csv_data = list(tools.get_data(path))
print(csv_data)