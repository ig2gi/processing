#!/usr/local/bin/python2.6
# encoding: utf-8
"""
extractor.py

Created by Gilbert Perrin on 2012-10-07.
Copyright (c) 2012 __G2G__. All rights reserved.
"""
import os, sys; sys.path.insert(0, os.path.join("..","..","..","lib"))
from SPARQLWrapper import SPARQLWrapper, JSON
import web
import re


class CSVWriter:
  """
  """
  def __init__(self, filename, objects, sep=',') :
    self.filename = filename
    self.objects = objects
    self.sep = sep
    
    
  def write(self):
    f = open(self.filename, 'w+')
    title = "id," + self.sep.join(self.objects[0].csvtitle())
    f.write(title + '\n')
    id = 1
    for o in self.objects:
      line = self.sep.join(str(v).replace(',',';') for v in o.csv())
      f.write(("%i,%s" % (id,line))+ '\n')
      id = id + 1
    f.close()

  @staticmethod
  def _write_(filename, list, title):
    f = open(filename, 'w+')
    f.write("id," + title + '\n')
    id = 1
    for o in list:
      f.write(("%i,%s" % (id,",".join(str(v) for v in o)))+ '\n')
      id = id + 1
    f.close()
  

class ENumberClass(object):
  """
  """
  def __init__(self, n1, n2, name) :
    self.n1 = n1
    self.n2 = n2
    self.name = name
    self.subclasses = []
    self.parent = None
    self.enumbers = []
       
  def range():
    return [n1, n2]
    
  def add_subclass(self, c):
    if self.include(c):
      self.subclasses.append(c)
      c.parent = self
    else:
      print "error"
      
  def get_eclass(self, n):
    if self.contains(n):
      if len(self.subclasses) > 1:
        for child in self.subclasses:
          if child.contains(n):
            return child.get_eclass(n)
      else:
        return self
    return None
  
  def classify(self, enumber):
      if self.contains(enumber.number):
        self.enumbers.append(enumber)
        if len(self.subclasses) > 0:
          for child in self.subclasses:
            child.classify(enumber)
        else:
          enumber.eclass = self
    
  def count_enumbers(self):
    return len(self.enumbers)
    
  def list_enumbers(self, sort=True):
    if sort:
      sort_enumbers = [x for x in self.enumbers]
      sort_enumbers.sort(key=lambda x: x.number, reverse=False)
      return sort_enumbers
    return self.enumbers
    
  def get_estats(self):
    elist1 = [x.number for x in self.list_enumbers()]
    elist1.sort()
    print elist1
    count = 0
    cumul = 0
    d = {}
    for i in sorted(set(elist1)):
      count = elist1.count(i)
      cumul += count
      d[i] = [count, cumul]
    result = [[k,'E'+ str(k),v[0],v[1]] for k,v in d.iteritems()]
    result.sort(key=lambda x: x[0], reverse=False)
    print result
    return result
        
  def all(self, level=0):
    all = []
    if level == 0:
      all.append(self)
      return all
    for child in self.subclasses:
      all.extend(child.all(level-1))
    return all
    
  def csv(self):
    return [self.n1, self.n2, self.parent.name, self.name, self.count_enumbers()]
    
  @classmethod
  def csvtitle(cls):
      return ["n1","n2", "parent", "name", "counte"]
    
  def label(self):
    return "%s: %s" % (self.parent.name, self.name)
  
  
  def contains(self, number):    
    return (number >= self.n1) & (self.n2 >= number)
    
  def include(self, other):
    return (other.n1-self.n1) >= 0 & (other.n2-self.n2) >= 0
  
  def __str__(self):
    s = "\n\t".join(str(x) for x in self.subclasses)
    return "%d-%d : %s\n\t%s" % (self.n1, self.n2, self.name, s)


class InformationSource:
  """
  """
  def __init__(self, number, name, url) :
      self.number = number
      self.name = name
      self.url = url
      
  def __str__(self):
      return "%s" % (self.name)

class ENumber:
  """ENumber.
     Food Additive
  """
    
  def __init__(self, number, code, name, source = None, synonym='', eclass=None, since=None ) :
      self.number = int(number)
      self.code = code
      self.name = name
      self.sources = []
      if source:
        self.add_source(source)
      self.synonym = synonym
      self.since = since
      self.subcode = code.replace(number,'')
      self.eclass = eclass
      self.occurences = 1
     
  
  def since(self) :
    """in years"""
    return 2012 - self.since
    
  def add_source(self, source):
      self.sources.append(source)
      
  def csv(self):
    return [self.E(),self.code,self.number, self.subcode, self.since, "[" + "][".join(str(s.number) for s in self.sources) + "]", self.name, self.synonym]
  
  @classmethod
  def csvtitle(cls):
    return ["e","code","number", "subcode", "since","sources", "name", "synonym"]
  
  def E(self):
    return "E%s" % self.number
        
  def __str__(self):
    return "   ".join(str(v) for v in self.csv())
  
  def __cmp__(self, other):
    return cmp(self.number, other.number)
  
   

def main():
  
  # E Numbers dictionnary
  enumbers = {}
  # E Numbers Classification
  root_eclasses = ENumberClass(100, 1600, "root")
  
  
  
  # ==============================================================
  # WIKIPEDIA 
  # http://en.wikipedia.org/wiki/E_number
  # ==============================================================
  source3 = InformationSource(1, "WIKIPEDIA", "http://en.wikipedia.org/wiki/E_number")
  # Classification
  article = web.wikipedia.search("Food_additive_code", language="en", light=False, cached=True)
  regex = "([0-9]*).([0-9]*)"
  for row in article.tables[0][1:]:
    i1,i2 = 0,1
    if len(row) == 3: # range
      range1 = row[0].split("(full list)")
      name = range1[1].strip()
      m = re.search(regex, range1[0].strip())
      n1 = int(m.group(1))
      n2 = int(m.group(2))
      c = ENumberClass(n1, n2, name)
      root_eclasses.add_subclass(c)
      i1,i2 = 1,2
    # sub range
    name = row[i2]
    if name:
      m = re.search(regex, row[i1])
      n1 = int(m.group(1))
      n2 = int(m.group(2))
      c2 = ENumberClass(n1,n2, name)
      c.add_subclass(c2)
    

  
  
  
  # ==============================================================
  # CODEX ALIMENTARIUS
  # http://www.codexalimentarius.net/gsfaonline/additives/index.html
  # ==============================================================
  source1 = InformationSource(1, "GSFA codexalimentarius", "http://www.codexalimentarius.net/gsfaonline/additives/index.html")
  
  # FOOD ADDITIVE INDEX
  lines = [line.strip() for line in open('food_additive_index.txt')]
  regex = "(.*) \((.*)\)"
  for line in lines:
    m = re.search(regex, line)
    code = m.group(2)
    name = m.group(1).strip()
    number = re.search("[0-9]*", code).group(0)
    e = ENumber(number, code, name, source1)
    root_eclasses.classify(e)
    enumbers[code] = e
  
  # FOOD ADDITIVE SYNONYMS
  lines = [line.strip() for line in open('food_additive_synonym.txt')]
  regex = "(.*) \((.*)\)"
  for line in lines:
    m = re.search(regex, line)
    if m:
      code = m.group(2)
      synonym = m.group(1)
      en = enumbers[code]
      en.synonym = synonym
    else:
      print "error:%s" % line
  
  # ==============================================================
  # FOOD LAW
  # http://www.foodlaw.rdg.ac.uk/additive-list.htm
  # ==============================================================
  source2 = InformationSource(2, "FOOD LAW", "http://www.foodlaw.rdg.ac.uk/additive-list.htm")
  lines = [line.strip() for line in open('foodlaw_enumbers.txt')]
  regex = "E ([0-9]*[a-z]?) (.*)"
  for line in lines:
    m = re.search(regex, line)
    if m:
      code = m.group(1)
      name = m.group(2).strip()
      if code in enumbers:
        en = enumbers[code]
        en.add_source(source2)
      else: # new ENumber
        synonym = ''
        number = re.search("[0-9]*", code).group(0)
        m2 = re.search("(\(.*\))",name)
        if m2:
          synonym = m2.group(1)
          name = name.replace(synonym, '')
          synonym = synonym[1:-1]
        en = ENumber(number, code, name, source2, synonym) 
        root_eclasses.classify(en)
        enumbers[code] = en
  
  
  # print E numbers
  sort_enumbers = [x for x in enumbers.values()]
  sort_enumbers.sort(key=lambda x: x.number, reverse=False)
  for e in sort_enumbers:
    print e
  
  # ==============================================================
  # PRINT CSV FILES
  # ==============================================================
  CSVWriter('../../nodebox3/enumbers/eclasses1.csv', [x for x in root_eclasses.all(1)]).write()
  CSVWriter('../../nodebox3/enumbers/eclasses2.csv', [x for x in root_eclasses.all(2)]).write()
  CSVWriter('../../nodebox3/enumbers/enumbers-all.csv', sort_enumbers).write()
  
  for ec in root_eclasses.subclasses:
    if ec.count_enumbers() > 0:
      filename = '../../nodebox3/enumbers/enumbers-' + ec.name[0:4] 
      CSVWriter(filename + '.csv', ec.list_enumbers()).write()
      CSVWriter._write_(filename + '-estats.csv',ec.get_estats() , "N,EN,Co,Cu")
      

if __name__ == '__main__':
	main()

