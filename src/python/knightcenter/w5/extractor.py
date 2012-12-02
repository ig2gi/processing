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


def main():
  
  aggregates = {}
  lines = [line.strip() for line in open("climate_change/Country-Table 1.csv")] 
  for l in lines[1:17]:
    values = l.split(',')
    code = values[0].strip(' \t\n\r')
    name = values[1].strip(' \t\n\r')
    n = Node(name, code)
    aggregates[name] = n
    
  for l in lines[17:]:
    values = l.split(',')
    code = values[0].strip(' \t\n\r')
    name = values[1].strip(' \t\n\r')
    n = Node(name, code)
    region = values[3].strip(' \t\n\r')
    incomegroup = values[4].split(':')[0].strip(' \t\n\r')
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
      
  print world.json()
  
  f = open(data_dir + "/countries.json", 'w+')
  f.write(world.json())
  f.close()
  
  

  
  



if __name__ == '__main__':
  	main()
  
  
