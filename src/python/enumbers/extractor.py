#!/usr/local/bin/python2.6
# encoding: utf-8
"""
extractor.py

Created by Gilbert Perrin on 2012-10-07.
Copyright (c) 2012 __G2G__. All rights reserved.
"""
import os, sys; sys.path.insert(0, os.path.join("..","..","lib"))
from SPARQLWrapper import SPARQLWrapper, JSON
from domain import *
import web







def parseYear(text):
  if text.startswith('-0'):
    return '-' + text[1:5]
  return text[0:4]
  

def load_philosophers():
  philosophers = {}
  sparql = SPARQLWrapper("http://dbpedia.org/sparql")
  sparql.setQuery("""
      SELECT ?philosopher ?name ?era ?school ?birthDate ?deathDate WHERE {
      ?philosopher a <http://dbpedia.org/ontology/Philosopher>.
      ?philosopher rdfs:label ?name.
      ?philosopher <http://dbpedia.org/ontology/era>  ?era.
      ?philosopher <http://dbpedia.org/ontology/birthYear> ?birthDate.
      ?philosopher <http://dbpedia.org/ontology/deathYear> ?deathDate.
      FILTER(lang(?name) = "en").
      }ORDER BY ?era
  """)
  sparql.setReturnFormat(JSON)
  results = sparql.query().convert()
  id = 1
  for result in results["results"]["bindings"]:
      name = result["name"]["value"]
      birthYear = result["birthDate"]["value"]
      deathYear = result["deathDate"]["value"]
      p = Philosopher(id, name, int(parseYear(birthYear)), int(parseYear(deathYear)), 0)
      id = id + 1
      philosophers[p.name] = p
      
  print len(philosophers)
  l = philosophers.values()
  for p in sorted(l, key=lambda p: p.y1):
    s = "%i - %i %i : %s" % (p.id,  p.y1, p.y2, p.name)
    print(s)


def print_tables(article):
      for table in article.tables:
        print table.paragraph.title
        print table.title, "("+table.properties+")"
        for row in table:
            print "-"*50
            print " ; ".join(row)
            
      #
    

def main():
  
    
  article = web.wikipedia.search("Food_additive_code", language="en", light=False, cached=True)
  print_tables(article)    
  #print article.markup
  
      

if __name__ == '__main__':
	main()

