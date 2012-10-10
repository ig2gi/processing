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


class ENumberSource:
  
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
    
  def __init__(self, number, code, name, source = None, synonym='', since=None) :
      self.number = int(number)
      self.code = code
      self.name = name
      self.sources = []
      if source:
        self.add_source(source)
      self.synonym = synonym
      self.since = since
      self.subcode = code.replace(number,'')
  
  def since(self) :
    """in years"""
    return 2012 - self.since
    
  def add_source(self, source):
      self.sources.append(source)
    
  def __str__(self):
    return "E%i\t%s\t%s \t%s\t/%s" % (self.number, self.subcode, "-".join(str(s.number) for s in self.sources), self.name, self.synonym)
  
  def __cmp__(self, other):
    return cmp(self.number, other.number)
  
  


def print_tables(article):
      for table in article.tables:
        print "="*100
        print table.paragraph.title
        print "="*100
        print table.title, "("+table.properties+")"
        for row in table:
            print "-"*50
            print " ; ".join(row)
            
      #
    

def main():
  
  # E Numbers dictionnary
  enumbers = {}
  
  
  # ==============================================================
  # WIKIPEDIA 
  # 
  # ==============================================================
  #article = web.wikipedia.search("Food_additive_code", language="en", light=False, cached=True)
  #print_tables(article)    
  #print article.markup
  
  
  
  # ==============================================================
  # CODEX ALIMENTARIUS
  # http://www.codexalimentarius.net/gsfaonline/additives/index.html
  # ==============================================================
  source1 = ENumberSource(1, "GSFA codexalimentarius", "http://www.codexalimentarius.net/gsfaonline/additives/index.html")
  
  # FOOD ADDITIVE INDEX
  lines = [line.strip() for line in open('food_additive_index.txt')]
  regex = "(.*) \((.*)\)"
  for line in lines:
    m = re.search(regex, line)
    code = m.group(2)
    name = m.group(1)
    number = re.search("[0-9]*", code).group(0)
    enumbers[code] = ENumber(number, code, name, source1)
  
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
  source2 = ENumberSource(2, "FOOD LAW", "http://www.foodlaw.rdg.ac.uk/additive-list.htm")
  lines = [line.strip() for line in open('foodlaw_enumbers.txt')]
  regex = "E ([0-9]*[a-z]?) (.*)"
  for line in lines:
    m = re.search(regex, line)
    if m:
      code = m.group(1)
      name = m.group(2)
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
        enumbers[code] = ENumber(number, code, name, source2, synonym)
  
  
  # print E numbers
  sort_enumbers = [x for x in enumbers.values()]
  sort_enumbers.sort(key=lambda x: x.number, reverse=False)
  for e in sort_enumbers:
    print e
    
  print len(enumbers)
  
      

if __name__ == '__main__':
	main()

