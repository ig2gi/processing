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
import json

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
  
  ids = {}
  f = open("us-states.json")
  data = json.load(f)
  for i in range(0, len(data["features"])-1):
    state = data["features"][i]
    ids[state["properties"]["name"]] = state["id"]
  f.close
  
  #print ids
  
  lines = [line.strip() for line in open('US_unemployment_old.csv')]   
  tsv = []
  regex = re.compile('.*,("[0-9,]*"),.*')
  row = 0
  us_rates = []
  for l in lines:
    if regex.search(l):
      m = regex.search(l)
      v = m.group(1)
      l = l.replace(v, v.replace('"','').replace(',',''))
    values = l.split(',')
    if row != 0 and values[0] in ids:
      #print values[0]
      id = ids[values[0]] + ','
      rec_values = []
      rec_values.append(values[0])
      rec_values.extend([v for v in values[5:52]])
      tsv.append(id + ",".join(rec_values))
    elif row != 0:
      us_rates.extend([v for v in values[5:52]])
    row = row + 1
    
  print len(us_rates)

    
  months = ['January','February','March','April','May','June','July','August','September','October','November','December']
  
  years = [2011,2010,2009]
  
  f = open("US_unemployment.csv", 'w+')
  columns = ['id','state']
  columns.extend([m + ' 2012' for m in months[8::-1]])
  for y in years:
    months_year = [m + ' ' + str(y)  for m in months[11::-1]]
    columns.extend(months_year)
  f.write(','.join(columns) + '\n')
  for l in tsv:
    f.write(l + '\n')  
  f.close()
  
  print len(columns)
  f = open("US_unemployment_rate.csv", 'w+')
  f.write('month,label,rate' + '\n')
  col = 0
  for c in columns[2:]:
      v = c.split(' ')
      label =  v[0][0:3] + ' ' + v[1]
      f.write(c + ',' + label + ',' + us_rates[col] + '\n')
      col = col + 1  
  f.close()
  

  
  



if __name__ == '__main__':
  	main()
  
  
