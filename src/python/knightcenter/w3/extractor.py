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

class Score(object):
  """
  """
  def __init__(self, name, s2011, s2012) :
    self.name = name
    self.s2011 = s2011.split('%')[0]
    self.s2012 = s2012.split('%')[0]
    
  def csv(self):
    return "%s,%s,%s" % (self.name,self.s2011,self.s2012)
    
  def delta(self):
    return self.s2012 - self.s2011
    


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
  
  
  scores = []

  
  lines = [line.strip() for line in open('Aid transparency - 2011 and 12 comparable data.csv')]
  for l in lines[1:59]:
    values = l.split(',')[2:6]
    name = values[0]
    s2011 = values[1].split('%')[0]
    s2012 = values[2].split('%')[0]
    scores.append(Score(name, s2011, s2012))
    
  f = open(data_dir + "overall-result-3.csv", 'w+')
  f.write('shortname,s2011,s2012\n')
  for s in scores:
    f.write(s.csv() + '\n')  
  f.close() 
  
  
  # 
  f = open(data_dir + "overall-result-3-2.csv", 'w+')
  f.write('group,n2011,n2012\n')
  for k in range(20,120,20):
    group = "%i-%i" % (k-20, k)
    n2011 = len([s for s in scores if float(s.s2011) >= (k - 20) and float(s.s2011) < k])
    n2012 = len([s for s in scores if float(s.s2012) >= (k - 20) and float(s.s2012) < k])
    f.write("%s,%i,%i" % (group,n2011,n2012) + '\n')  
  f.close()
  
  

    
    
if __name__ == '__main__':
	main()
