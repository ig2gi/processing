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

data_dir = '../../../html/knightcenter-w5/data/'

class Node(object):
  """
  """
  def __init__(self, name, code) :
    self.name = name
    self.code = code
    self.children = {}
    
  def addChild(self, name, node):
    self.children[name] = node
    
  def getChild(self, name):
    if name in self.children:
      return self.children[name] 
    return None
    
  def clone(self):
    return Node(self.name, self.code)
    
  def json(self):
    jsonObj = {"name": self.name, "code": self.code, "children": self.jsonObjChildren()}
    return json.dumps(jsonObj ,ensure_ascii=False,indent=2)
    
  def jsonObjChildren(self):
    jsonChildren = []
    for c in self.children.values():
      jsonChildren.append({"name": c.name, "code": c.code, "children": c.jsonObjChildren()})
    return jsonChildren
    
    
class Indicator(object):
      """
      """
      def __init__(self, code, name, topic, definition, source, numval = 1, func_val = lambda x: [x]) :
        self.name = name
        self.code = code
        self.topic = topic
        self.definition = definition
        self.source = source
        self.values = {}
        self.func_val = func_val
        
      def addValue(self, country, val):
        self.values[country] = val
        
      def getValue(self, country):
        if not self.values[country]:
          v = []
          for i in range(0,self.numval):
            v.append("..")
          return v
        return self.func_val(self.values[country])
        
        
      def __str__(self):
        s = self.code + ':\n\t'
        s = s + "\n\t".join("%s:%s" % (k,self.getValue(k)) for k in self.values.keys())
        return s
      
      @staticmethod
      def join(indicators):
        result = {}
        for i in indicators:
          for k in i.values.keys():
            if k not in result:
              result[k] = []
            result[k].extend(i.getValue(k))
        return result
        
        
       

class Country(object):
  """
  """
  def __init__(self, code, name, region, incomeGroup) :
    self.name = name
    self.code = code
    self.region = region
    self.incomeGroup = incomeGroup
    self.indicators = {}
  
  def addIndicator(self, indicator):
     self.indicators.append(indicator)
    





def main():
  
  aggregates = {}
  countries = {}
  lines = [line.strip() for line in open("climate_change/Country-Table 1.csv")] 
  for l in lines[1:17]:
    values = l.split(',')
    code = values[0].strip(' \t\n\r')
    name = values[1].strip(' \t\n\r')
    n = Node(name, code)
    aggregates[name] = n
    #ß®countries[code] = Country(code, name)
    
  for l in lines[17:]:
    values = l.split(',')
    code = values[0].strip(' \t\n\r')
    name = values[1].strip(' \t\n\r')
    n = Node(name, code)
    region = values[3].strip(' \t\n\r')
    incomegroup = values[4].split(':')[0].strip(' \t\n\r')
    countries[code] = Country(code, name, region, incomegroup)
    regionNode = aggregates[region]
    incomeNode = aggregates[incomegroup]
    child = regionNode.getChild(incomegroup)
    if child:
      child.addChild(name, n)
    else:
      regionNode.addChild(incomegroup, incomeNode.clone())
      regionNode.getChild(incomegroup).addChild(name, n)
  
  
  world = aggregates['World']
  for k in aggregates: 
    if k not in['World','Low income','High income', 'Lower middle income', 'Low & middle income', 'Middle income', 'Upper middle income']:
      world.addChild(aggregates[k].name, aggregates[k])
      
  #print world.json()
  
  f = open(data_dir + "/countries.json", 'w+')
  f.write(world.json())
  f.close()

  # Indicators
  indicators = {}
  lines = [line.strip() for line in open("climate_change/Series-Table 1.csv")]
  for l in lines[1:]:
    values = l.split(',')
    indicators[values[0]] = Indicator(values[0], values[1], values[4],'','')
    

  i1 = 'EN.CLC.MMDT.C'
  i2 = 'EN.CLC.PCAT.C'
  i3 = 'EN.CLC.HPPT.MM'
  i4 = 'EN.CLC.PCPT.MM'
  i5 = 'EN.CLC.PCHW'
  i6 = 'EN.CLC.PCCC'
  inds = [i1, i2, i3, i4, i5, i6]
  
  lines = [line.strip() for line in open("climate_change/Data-Table 1.csv")] 
  for l in lines:
    values = l.split(',')
    code = values[0].strip()
    val = values[len(values)-1].strip()
    indic = values[1].strip()
    if val not in['..', 'n/a']:
      if indic in inds:
        indicators[indic].addValue(code, val)
        
  indicators[i1].func_val = lambda x: [v.strip() for v in x.split('/')]
  indicators[i1].numval = 2
  indicators[i2].func_val = lambda x: [v.strip() for v in x.split(' to ')]
  indicators[i2].numval = 2
  indicators[i4].func_val = lambda x: [v.strip() for v in x.split(' to ')]
  indicators[i4].numval = 2
  indicators[i5].func_val = lambda x: [v.strip() for v in x.split(' / ')]
  indicators[i5].numval = 2
  indicators[i6].func_val = lambda x: [v.strip() for v in x.split(' / ')]
  indicators[i6].numval = 2
  
  f1 = Indicator.join([indicators[i] for i in inds])
  print f1
  f = open(data_dir + "/climate.csv", 'w+')
  f.write("code,name,tmin,tmax,t10th,t90th,ppt,p10th,p90th,h10th,h90th,c10th,c90th\n")
  for k in f1.keys():
    l = [k, countries[k].name]
    l.extend(f1[k])
    f.write(",".join(l) + '\n')
  f.close()
  
  f = open(data_dir + "/countries.csv", 'w+')
  f.write("code,name,region,incomegroup\n")
  listcountries = countries.values()
  listcountries.sort(key=lambda x: x.name)
  for c in listcountries:
    f.write("%s,%s,%s,%s" % (c.code, c.name, c.region, c.incomeGroup) + '\n')
  f.close()


if __name__ == '__main__':
  	main()
  
  
