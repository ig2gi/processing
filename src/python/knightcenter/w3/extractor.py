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
  # transpose
  row = 0
  cols = []
  c = 0
  for l in lines:
    if row != 1 and row <14:
      cols.append([])
      values = l.split(',')
      for k in range(1, len(values)):
        v = values[k]
        if c in [4,5,6,7,8,9,10]:
          v = v.split('%')[0]
        cols[c].append(v)
      c = c + 1
    row = row + 1
    
  nrows = len(cols[0])
  
  f = open(data_dir + "overall-result-1.csv", 'w+')
  for i in range(0, nrows -1):
    row = [cols[c][i] for c in range(0, len(cols)-1)]
    f.write(",".join(row) + '\n')  
  f.close()
  
  lines = [line.strip() for line in open('Aid transparency - 2011 and 12 comparable data.csv')]
  new_lines = []
  for l in lines:
    values = l.split(',')
    new_lines.append([v.split('%')[0] for v in values[2:6]])
  f = open(data_dir + "overall-result-3.csv", 'w+')
  for l in new_lines:
    f.write(",".join(l) + '\n')  
  f.close() 
  

    
    
if __name__ == '__main__':
	main()
