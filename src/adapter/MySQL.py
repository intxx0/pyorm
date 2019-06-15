#! /opt/python2.7/bin/python
# -*- coding: utf-8 -*-

import MySQLdb, MySQLdb.cursors, sys, time

O_AND	= 'AND'
O_OR	= 'OR'

class MySQL():
	
	_conn = None
	_affected_rows = 0
	_insert_id = 0
	
	def __init__(self):
		
		pass
	

	def __build_select(self, mapper):
		
		query = 'SELECT '
		
		num_fields = len(mapper._fields)
		
		if num_fields>0:
			if num_fields>1:	
				fields = ''
				i = 1
				for f in mapper._fields:
					if i<num_fields:
						fields = fields + "{0}, ".format(f)
					else:
						fields = fields + "{0} ".format(f)
					i = i + 1
						
			query = query + fields
			
			
		query = query + "FROM {0} t1 ".format(mapper.name)
		
		for key, value in mapper._join_inner.items():
			query = query + "INNER JOIN {0} ON {1} ".format(key, str(value))

		for key, value in mapper._join_left.items():
			query = query + "LEFT JOIN {0} ON {1} ".format(key, str(value))
			
		if len(mapper._where)>0:
			where = 'WHERE '
			i = 1
			for w in mapper._where:
				
				where = where + "{0} {1} {2} ".format(str(w['field']), str(w['oper']), str(w['value']))
				
				if i<len(mapper._where):
					where = where + "{0} ".format(w['sql_oper'])
					
				i = i + 1
				
			query = query + where
			
		num_groups = len(mapper._group)
		
		if num_groups>0:
			group = 'GROUP BY '
			i = 1
			for g in mapper._group:
				if i<num_groups:
					group = group + "{0}, ".format(str(g))
				else:
					group = group + "{0} ".format(str(g))
				i = i + 1
						
			query = query + group
			
		
		num_orders = len(mapper._order)
		
		if num_orders>0:
			order = 'ORDER BY '
			i = 1
			for o in mapper._order:
				if i<num_orders:
					order = order + "{0}, ".format(str(o))
				else:
					order = order + "{0} ".format(str(o))
				i = i + 1
						
			query = query + order

		if len(mapper._limit)>0:
			query = query + ' LIMIT ' + mapper._limit
			
		return query
	

	def __build_insert(self, mapper, values):
		
		query = 'INSERT INTO %s SET ' % (mapper.name)
		
		i = 1
		
		for field in values:
			value = values[field]
			query = query + "`" + field + "`='" + str(value) + "'"
			if i<len(values):
				query = query + ', '
			i = i + 1
			
		query = query + ';'
		
		return query


	def __build_update(self, mapper, values):
		
		query = 'UPDATE %s SET ' % (mapper.name)
		
		i = 1
		
		for field in values:
			value = values[field]
			query = query + "`" + field + "`='" + str(value) + "'"
			if i<len(values):
				query = query + ', '
			i = i + 1
		
		query = query + ' WHERE %s = %s;' % (mapper.pk, str(values['id']))
		
		return query
	

	def __build_delete(self, mapper, where):
		
		query = 'DELETE FROM %s WHERE %s %s %s;' % (mapper.name, str(where['field']), str(where['oper']), str(where['value']))
		return query
	

	def fetch_all(self, mapper):
		
		cursor = self._conn.cursor()
		result = cursor.execute(self.__build_select(mapper))
		
		return cursor.fetchall()


	def fetch_row(self, mapper):
		
		cursor = self._conn.cursor()
		result = cursor.execute(self.__build_select(mapper))
		
		return cursor.fetchone()
	

	def insert(self, mapper, values):
		
		self.execute(self.__build_insert(mapper, values))
		return self._insert_id
	

	def update(self, mapper, values):
		
		return self.execute(self.__build_update(mapper, values))
	

	def delete(self, mapper, where):
		
		return self.execute(self.__build_delete(mapper, where))
	

	def affected_rows(self):
		
		return self._affected_rows


	def insert_id(self):
		
		return self._insert_id

	
	def execute(self, query):
		
		cursor = self._conn.cursor()
		result = cursor.execute(query)
		
		self._affected_rows = int(self._conn.affected_rows())
		self._insert_id = self._conn.insert_id()
		
		return result


	def commit(self):
	
		try:
			self._conn.commit()
			return True
		except MySQLdb.Error, e:
			print 'Error: %d: %s' % (e.args[0], e.args[1])
			return False


	def rollback(self):
	
		try:
			self._conn.rollback()
			return True
		except MySQLdb.Error, e:
			print 'Error: %d: %s' % (e.args[0], e.args[1])
			return False
	

	def connect(self, config):
		
		try:
			self._conn = MySQLdb.connect(config['hostname'], config['username'], config['password'], config['database'], cursorclass=MySQLdb.cursors.DictCursor)
			
			if 'autocommit' in config:
				if config['autocommit']==True:
					self._conn.autocommit(1)
				else:
					self._conn.autocommit(0)
			else:
				self._conn.autocommit(0)
				
			return True
		except MySQLdb.Error, e:
			print 'Error: %d: %s' % (e.args[0], e.args[1])
			return False
	

	def disconnect(self):
		
		try:
			self._conn.disconnect()
			return True
		except MySQLdb.Error, e:
			print 'Error: %d: %s' % (e.args[0], e.args[1])
			return False

