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


class WordCount(object):
  """
  """
  def __init__(self, w, c1, c2) :
    self.w = w
    self.c1 = int(c1)
    self.c2 = int(c2)
    
    
  def total(self):
    return self.c1 + self.c2
    
  def delta(self):
    return self.c1 - self.c2
    
  def ratio1(self):
    if self.c2 == 0:
      return 1000
    return float(self.c1) / float(self.c2)
    
  
  def ratio2(self):
    if self.c1 == 0: 
      return 1000   
    return float(self.c2) / float(self.c1)

  def csv(self):
    return "%s,%i,%i,%i,%i,%s,%f,%f" % (self.w, self.c1, self.c2,self.delta(),self.total(),"%i - %i" % (self.c1, self.c2), self.ratio1(), self.ratio2())
     
  def __cmp__(self, other):
    return math.fabs(self.delta) - math.fabs(other.delta)      
       

        
def main():
  lines = [line.strip() for line in open('extractor.txt')]     
  regex = "([a-zA-Z /]*)"
  regex2 = "([0-9]*) - ([0-9]*)"
  words = []
  counts = []
  for line in lines:
    #print line
    if re.match(regex, line):
      m = re.search(regex, line)
      words.append(m.group(1).strip())
    if re.match(regex2, line):
      m2 = re.search(regex2, line)
      counts.append(m2.group(1).strip())
      counts.append(m2.group(2).strip())
  i = 0
  wordcounts = []
  democrats = []
  republicans = []
  equals = []
  for w in words:
    if w:
      wc = WordCount(w, counts[i],counts[i+1])
      if wc.delta == 0:
        equals.append(wc)
      elif wc.delta > 0:
        democrats.append(wc)
      else:
        republicans.append(wc)
      i = i + 2
  democrats.sort(key = lambda x: x.ratio1(), reverse=True)
  republicans.sort(key = lambda x: x.ratio2(), reverse=True)
  wordcounts.extend(democrats)
  wordcounts.extend(equals)
  wordcounts.extend(republicans)
  
  
  
  
  f = open("words_convention.csv", 'w+')
  f.write("word,d,r,delta,total,counts,ratio1,ratio2" + '\n')
  for wc in wordcounts:
    f.write(wc.csv() + '\n')
  f.close()
  
  # top 10
  wordcounts.sort(key = lambda x: x.total(), reverse=True)
  f = open("words_convention_top_ten.csv", 'w+')
  f.write("word,d,r,delta,total,counts,ratio1,ratio2" + '\n')
  for wc in wordcounts:
    f.write(wc.csv() + '\n')
  f.close()
  
 

if __name__ == '__main__':
	main()

