#!/usr/bin/python
#coding=UTF-8

import sys
import xml.sax
import pymongo

DB_URI =	'mongodb://localhost:27017/'
DB_NAME =	'weatherapp_db'

db_client = pymongo.MongoClient(DB_URI)
db = db_client[DB_NAME]


class yandex_cities_list_parser_handler(xml.sax.ContentHandler):
	def __init__(self):
		self.country = ''
		self.doc = {'_id':0,'list':[]}
		self.clear_city( )

	def clear_city(self):
		self.city = {'name':'','country':'','id':0}

	def startElement(self, name, attrs):
		if name == 'city':
			self.city['id'] = int(attrs.get('id',0))
			self.city['country'] = attrs.get('country','')

	def endElement(self, name):
		if name == 'city':
			if self.city['country'] == u'Россия': # Nazi nazi code code
				self.doc['list'] += [self.city]
			self.clear_city( )

	def characters(self,content):
		if self.city['id'] != 0:
			self.city['name'] += content

parser = xml.sax.make_parser()
sax_handler = yandex_cities_list_parser_handler( )
parser.setContentHandler(sax_handler)
parser.parse(sys.stdin)

sax_handler.doc['list'].sort()

db.clities_list.save(sax_handler.doc)
