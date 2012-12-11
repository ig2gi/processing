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

aggregates = {}
countries = {}
regions = {}



class Node(object):
  """
  """
  def __init__(self, name, code, attrs = None) :
    self.name = name
    self.code = code
    self.children = {}
    self.attrs = attrs
    
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
    if self.attrs:
      for k,v in self.attrs.iteritems():
        jsonObj[k] = v
    return json.dumps(jsonObj ,ensure_ascii=False,indent=2)
    
  def jsonObjChildren(self):
    jsonChildren = []
    for c in self.children.values():
      child = {"name": c.name, "code": c.code, "children": c.jsonObjChildren()}
      if c.attrs:
        for k,v in c.attrs.iteritems():
          child[k] = v
      jsonChildren.append(child)
    return jsonChildren
    
    
class Indicator(object):
      """
      """
      def __init__(self, code, name, topic, definition, source, numval = 1, func_val = lambda x: x) :
        self.name = name
        self.code = code
        self.topic = topic
        self.definition = definition
        self.source = source
        self.values = {}
        self.func_val = func_val
        self.numval = numval
        
      def addValue(self, country, val):
        self.values[country] = val
        
      def getValue(self, country):
        if country not in self.values:
          v = []
          for i in range(0,self.numval):
            v.append("..")
          return v
        return self.func_val(self.values[country])
        
        
      def __str__(self):
        return self.code
        
      def write(self, file, columns):
        f = open(data_dir + "/" + file, 'w+')
        f.write(columns + '\n')
        for k in self.values.keys():
          if k in countries:
            l = [k, countries[k].name]
            l.extend(self.getValue(k))
            f.write(",".join(l) + '\n')
        f.close()
      
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
    self.unfccc = 'no'
  
  def addIndicator(self, indicator):
     self.indicators.append(indicator)
    





def main():
  
  unfccc = {}
  lines = [line.strip() for line in open("levelactions.csv")] 
  for l in lines:
    v = l.split(',')
    unfccc[v[0]] = v[2]
    
  
  lines = [line.strip() for line in open("climate_change/Country-Table 1.csv")] 
  for l in lines[1:17]:
    values = l.split(',')
    code = values[0].strip(' \t\n\r')
    name = values[1].strip(' \t\n\r')
    if code not in ['EMU', 'SID']: 
     n = Node(name, code)
     aggregates[name] = n
     regions[code] = Country(code, name, '', '')
 
    
  for l in lines[17:]:
    values = l.split(',')
    code = values[0].strip(' \t\n\r')
    name = values[1].strip(' \t\n\r')
    if code in unfccc:
      n = Node(name, code, {'unfccc':unfccc[code]})
      print n.json()
    else: n = Node(name, code)
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
  i13 = 'AG.LND.EL5M.ZS'
  
  i7 = 'SP.POP.TOTL'
  i14 = 'NY.GDP.MKTP.CD'
  
  i8 = 'EN.ATM.CO2E.KT'
  i9 = 'EN.ATM.METH.KT.CE'
  i10 = 'EN.ATM.NOXE.KT.CE'
  i11 = 'EN.ATM.GHGO.KT.CE'
  
  i12 = 'EG.USE.PCAP.KG.OE'
  
  i15 = 'EN.CLC.NCOM'
  
  
  inds_climate = [i1, i2, i3, i4, i5, i6]
  inds_economy = [i7,i14]
  inds_emission = [i8, i9, i10, i11]
  inds_energyuse = [i12]
  inds_actions = [i15]
  
  
  labels_emission = {i8:'CO2', i9:'CH4', i10:'N2O',i11: 'GHG'}
  
  regioncodes = ['EAP','ECA','LAC','MNA','SAS','SSA','NME']
  
  
  lines = [line.strip() for line in open("climate_change/Data-Table 1.csv")] 
  for l in lines:
    values = l.split(',')
    code = values[0].strip()
    indic = values[1].strip()
    if indic == i13:
      indicators[indic].addValue(code, values[15])
    if indic in inds_climate :
      val = values[len(values)-1].strip()
      if val not in['..', 'n/a']:
        indicators[indic].addValue(code, val)
    if indic in inds_actions :
        val = values[len(values)-1].strip()
        if val not in['..']:
            indicators[indic].addValue(code, val)
    if indic in inds_economy:
      indicators[indic].addValue(code, values[5:]);
      indicators[indic].numval = len(values[5:])
    if indic in inds_emission or indic in inds_energyuse:
      val = values[6:len(values)-1]
      indicators[indic].addValue(code, val);
      
  indicators[i1].func_val = lambda x: [v.strip() for v in x.split('/')]
  indicators[i1].numval = 2
  indicators[i2].func_val = lambda x: [v.strip() for v in x.split(' to ')]
  indicators[i2].numval = 2
  indicators[i3].func_val = lambda x: [x]
  indicators[i3].numval = 1
  indicators[i13].func_val = lambda x: [x]
  indicators[i13].numval = 1
  indicators[i4].func_val = lambda x: [v.strip() for v in x.split(' to ')]
  indicators[i4].numval = 2
  indicators[i5].func_val = lambda x: [v.strip() for v in x.split(' / ')]
  indicators[i5].numval = 2
  indicators[i6].func_val = lambda x: [v.strip() for v in x.split(' / ')]
  indicators[i6].numval = 2
  indicators[i8].func_val = lambda x: [v.strip() for v in x]
  indicators[i15].func_val = lambda x: ['no' if x.strip() == 'n/a' else 'yes']
  indicators[i15].numval = 1
  
  #print world.json()
  
  f = open(data_dir + "/countries.json", 'w+')
  f.write(world.json())
  f.close()
  
  
  l = [indicators[i] for i in inds_climate]
  l.append(indicators[i13])
  f1 = Indicator.join(l)
  #print f1
  f = open(data_dir + "/climate.csv", 'w+')
  f.write("code,name,tmin,tmax,t10th,t90th,ppt,p10th,p90th,h10th,h90th,c10th,c90th,area5m\n")
  for k in f1.keys():
    if k in countries:
      l = [k, countries[k].name]
      l.extend(f1[k])
      f.write(",".join(l) + '\n')
  f.close()
  

  indicators[i7].write("population.csv", "code,name," + ','.join([str(i) for i in range(1990,2012)]))
  
  indicators[i14].write("gdp.csv", "code,name," + ','.join([str(i) for i in range(1990,2012)]))
  
  print indicators[i15].values
  indicators[i15].write("levelactions.csv", "code,name,UNFCCC")
  
  
  def fct(x):
    if x != '..':
      return float(x)
    return 0.0
  
  f3 = Indicator.join([indicators[i] for i in inds_emission])
  #print f3
  f = open(data_dir + "/emissions.csv", 'w+')
  f.write("code,name,indicator,value,year" + '\n')
  emissions_json = {'name': 'world', 'children':[]}
  for k in regions:
        name = regions[k].name
        if k in regioncodes:
          region_json = {'name': name, 'emission':0, 'energy': 0}
          emissions_json['children'].append(region_json)
          size = 0
          for ind in inds_energyuse:
            vals = indicators[ind].getValue(k)
            if k == 'NME':
                             vals1 = [fct(v) for v in indicators[ind].getValue('USA')]
                             vals2 = [fct(v) for v in indicators[ind].getValue('CAN')]
                             vals = [(x + y) for x,y in zip(vals1, vals2)]
                             vals = ['..' if x == 0.0 else str(x) for x in vals]
            for v in reversed(vals):
              if v != '..':
                  region_json['energy'] = fct(v)
                  break
            
        for ind in inds_emission:
          l = [k, name, ind]
          if k == 'NME':
            vals1 = [fct(v) for v in indicators[ind].getValue('USA')]
            vals2 = [fct(v) for v in indicators[ind].getValue('CAN')]
            #print vals1
            #print vals2
            vals = [(x + y) for x,y in zip(vals1, vals2)]
            #print vals
            vals = ['..' if x == 0.0 else str(x) for x in vals]
          else: vals = indicators[ind].getValue(k)
          #print vals
          vals_f = [fct(v) for v in vals]
          y = 2011
          for v in reversed(vals):
            #if v != '..':
            if y == 2006: 
              if k in regioncodes:
                size = size + fct(v)
                #region_json['children'].append({'name': labels_emission[ind], 'size':fct(v)})
              l.extend([v,str(y)])
              break
            y = y - 1
          #print l
          if k in regioncodes:
            region_json['emission'] = size
          f.write(",".join(l) + '\n')
  f.close();
  
  emissions2_json = {'name': 'world', 'children':[]}
  region_nodes = {}
  for k in countries:
    name = countries[k].name
    region = countries[k].region
    if region not in region_nodes:
      n = {'name': region, 'children':[]}
      region_nodes[region] = n
      emissions2_json['children'].append(n)
    emission = 0
    yemission = 2011
    energy = 0
    yenergy = 2010
    # emission
    for ind in inds_emission:
      vals = indicators[ind].getValue(k)
      yemission = 2011
      for v in reversed(vals):
        if v != '..':
          emission = emission + fct(v)
          break
        yemission = yemission -1
    # energy use
    vals = indicators[i12].getValue(k)
    for v in reversed(vals):
      if v != '..':
        energy = fct(v)
        break
      yenergy = yenergy - 1
    if emission != 0 and energy != 0:
      region_nodes[region]['children'].append({'name': name, 'emission':emission, 'yemission': yemission,'energy': energy, 'yenergy':yenergy})
  
  f = open(data_dir + "/emissions2.json", 'w+')
  s = json.dumps(emissions2_json ,ensure_ascii=False,indent=2)
  #print s
  f.write(s)
  f.close()

  
  f = open(data_dir + "/emissions.json", 'w+')
  s = json.dumps(emissions_json ,ensure_ascii=False,indent=2)
  #print s
  f.write(s)
  f.close()
  

  
  f = open(data_dir + "/countries.csv", 'w+')
  f.write("code,name,region,incomegroup\n")
  listcountries = countries.values()
  listcountries.sort(key=lambda x: x.name)
  for c in listcountries:
    f.write("%s,%s,%s,%s" % (c.code, c.name, c.region, c.incomeGroup) + '\n')
  f.close()
  
 
  f = open(data_dir + "/regions.csv", 'w+')
  f.write("code,name\n")
  listregions = regions.values()
  listregions.sort(key=lambda x: x.name)
  for c in listregions:
    if c.code in regioncodes:
      f.write("%s,%s" % (c.code, c.name) + '\n')
  f.close()
  
 
  
  
  


if __name__ == '__main__':
  	main()
  
  
