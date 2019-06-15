#! /opt/python2.7/bin/python
# -*- coding: utf-8 -*-

from os import *
import imp

class Db:
	
	_autocommit	= False
	
	_last_insert_id = None
	_affected_rows	= None
	
	_config		= { 'hostname': None, 'username': None, 'password': None, 'database': None, 'adapter': 'MySQL' }
	
	_adapter	= None
	
	def __init__(self, options):
		
		if type(options).__name__ != 'dict':
			print self.__class__ + ': "options" type must be <dict>'
			#return False
		
		#try:
			
		if 'hostname' in options:
			self._config['hostname'] = options['hostname']
			
		if 'username' in options:
			self._config['username'] = options['username']
			
		if 'password' in options:
			self._config['password'] = options['password']
			
		if 'database' in options:
			self._config['database'] = options['database']
			
		if 'adapter' in options:
			self._config['adapter'] = options['adapter']
			
		#locals()[self._config['adapter']] = __import__('adapter.' + self._config['adapter'])
		#self._adapter = eval('adapter.' + self._config['adapter'])
		
		adapter = imp.load_source(self._config['adapter'], 'adapter/' + self._config['adapter'] + '.py')
		self._adapter = adapter.MySQL()
		
		self._adapter.connect(self._config)
			
		#return True
			
		#except Exception, e:
			#print str(self.__class__) + ': ' + str(e)
			#return False


	def fetch_all(self, mapper):
		
		return self._adapter.fetch_all(mapper)


	def fetch_row(self, mapper):
		
		return self._adapter.fetch_row(mapper)
	

	def insert(self, mapper, values):
		
		return self._adapter.insert(mapper, values)


	def update(self, mapper, values):
		
		return self._adapter.update(mapper, values)
	

	def delete(self, mapper, where):
		
		return self._adapter.delete(mapper, where)
	

	def affected_rows(self):
		
		return self._adapter.affected_rows()


	def insert_id(self):
		
		return self._adapter.insert_id()


	def execute(self, query):
		
		return self._adapter.execute(query)


	def commit(self):
	
		return self._adapter.commit()


	def rollback(self):
	
		return self._adapter.rollback()


	def disconnect(self):
		
		self._adapter.disconnect()
