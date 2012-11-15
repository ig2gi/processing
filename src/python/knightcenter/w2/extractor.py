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

data_dir = '../../nodebox3/knightcenter/w2/data/'

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
    
    
  def fontname1(self):
    if self.ratio1() >= 1000 and self.c1 > 10:
        return "EurostileBold"
    if self.c1 > 10 and self.ratio1() > 2: 
        return "EurostileBold"
    return "Eurostile"
    
  def fontname2(self):
      if self.ratio2() >= 1000 and self.c2 > 10:
          return "EurostileBold"
      if self.c2 > 10 and self.ratio2() > 2: 
          return "EurostileBold"
      return "Eurostile"
    
  def ratio1(self):    
    if self.c2 == 0:
      return 1000
    return float(self.c1) / float(self.c2)
    
  
  def ratio2(self):
    if self.c1 == 0: 
      return 1000   
    return float(self.c2) / float(self.c1)

  def csv(self):
    return "%s,%i,%i,%i,%i,%s,%f,%f,%s,%s" % (self.w, self.c1, self.c2,self.delta(),self.total(),"%i - %i" % (self.c1, self.c2), self.ratio1(), self.ratio2(), self.fontname1(),self.fontname2() )
     
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
      if wc.delta() == 0:
        equals.append(wc)
      elif wc.delta() > 0:
        democrats.append(wc)
      else:
        republicans.append(wc)
      i = i + 2
  democrats.sort(key = lambda x: x.ratio1(), reverse=True)
  republicans.sort(key = lambda x: x.ratio2(), reverse=False## Indicators
  ![indicators](https://raw.github.com/ig2gi/processing/master/build/w3/indicators.png))
  wordcounts.extend(democrats)
  wordcounts.extend(equals)
  wordcounts.extend(republicans)
  
  for wc in democrats:
    print wc.delta()
  
  
  f = open(data_dir + "words_convention.csv", 'w+')
  f.write("word,d,r,delta,total,counts,ratio1,ratio2,fontname1,fontname2" + '\n')
  for wc in wordcounts:
    f.write(wc.csv() + '\n')
  f.close()
  
  # top 15
  wordcounts.sort(key = lambda x: x.total(), reverse=True)
  f = open(data_dir + "words_convention_top_ten.csv", 'w+')
  f.write("word,d,r,delta,total,counts,ratio1,ratio2" + '\n')
  for wc in wordcounts:
    f.write(wc.csv() + '\n')
  f.close()
  
  # top 15 words democrats
  democrats.sort(key = lambda x: x.c1, reverse=True)
  f = open(data_dir + "words_democrats_top.csv", 'w+')
  f.write("word,d,r,delta,total,counts,ratio1,ratio2" + '\n')
  for wc in democrats:
    f.write(wc.csv() + '\n')
  f.close()
  
  # top 15 words republicans
  republicans.sort(key = lambda x: x.c2, reverse=True)
  f = open(data_dir + "words_republicans_top.csv", 'w+')
  f.write("word,d,r,delta,total,counts,ratio1,ratio2" + '\n')
  for wc in republicans:
    print wc
    f.write(wc.csv() + '\n')
    
  f.close()
  
    
 

if __name__ == '__main__':
	main()

