#! /opt/python2.7/bin/python
# -*- coding: utf-8 -*-

from Db import *
from Model import *
from copy import *

O_AND	= 'AND'
O_OR	= 'OR'

class DbMapper():
	
	name	= None
	pk	= 'id'
	
	_fields = ()
	_where	= ()
	_join_inner = {}
	_join_left  = {}
	_order	= ()
	_group	= ()
	_limit	= ''
	
	_database = None
	
	def __init__(self, database):
		
		if type(database)=='None':
			raise Exception('Database instance must be specified.')
		
		self._database = database
	

	def fields(self, fields):
		
		self._fields = fields
		return True

	
	def where(self, field, operator, value, sql_operator = O_AND):
		
		self._where = self._where + ({'field': field, 'oper': operator, 'value': value, 'sql_oper': sql_operator},)
		return True


	def join_inner(self, table, where):
		
		self._join_inner[table] = where
		return True
	

	def join_left(self, table, where):
		
		self._join_left[table] = where
		return True
	

	def order(self, order):
		
		self._order = self._order + (order,)
		return True
	

	def group(self, group):
		
		self._group = self._group + (group,)
		return True
	

	def limit(self, limit):
		
		self._limit = limit
		return True

	def fetch_all(self):
		
		result = self._database.fetch_all(self)
		
		rowset = ()
		
		for r in result:
			row = Model()
			for key in r:
				value = r[key]
				if isinstance(value, str):
					value = "'" + str(value) + "'"
				exec('row.' + key + ' = ' + str(value))
			rowset = rowset + (row,)
			#print rowset

		return rowset


	def fetch_row(self):
		
		result = self._database.fetch_row(self)
		
		row = Model()
		
		for key in result:
			value = result[key]
			if isinstance(value, str):
				value = "'" + str(value) + "'"
			exec('row.' + key + ' = ' + str(value))
				
		return row
	

	def save(self, row):
		
		values = {}
		
		#for attr, value in row.__dict__.iteritems():
		#	values.update({attr: value})
		
		for attr in row._attr[id(row)]:
			values.update({attr: row._attr[id(row)][attr]})
		
		if self.pk in values:
			return self._database.update(self, values)
		else:
			return self._database.insert(self, values)
	

	def delete(self, field, operator, value):
		
		where = {'field': field, 'oper': operator, 'value': value}
		return self._database.delete(self, where)


	def commit(self):
	
		return self._database.commit()


	def rollback(self):
	
		return self._database.rollback()


