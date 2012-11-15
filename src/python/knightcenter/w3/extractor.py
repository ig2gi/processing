#!/usr/bin/env python
# encoding: utf-8
"""
extractor.py

Created by Gilbert Perrin on 2012-11-05.
Copyright (c) 2012 __G2G__. All rights reserved.
"""

import sys
import os
import re
import math

data_dir = '../../../nodebox3/knightcenter/w3/data/'


def main():
  lines = [line.strip() for line in open('overall-result.csv')]   
  new_lines = []
  # transpose
  row = 0
  cols = []
  c = 0
  for l in lines:
    if row != 1 and row <14:
      cols.append([])
      values = l.split(',')
      for k in range(1, len(values)):
        cols[c].append(values[k])
      c = c + 1
    row = row + 1
    
  nrows = len(cols[0])
  
  f = open(data_dir + "overall-result-1.csv", 'w+')
  for i in range(0, nrows -1):
    row = [cols[c][i] for c in range(0, len(cols)-1)]
    f.write(",".join(row) + '\n')  
  f.close()

    
    
if __name__ == '__main__':
	main()
