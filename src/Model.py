#! /opt/python2.7/bin/python
# -*- coding: utf-8 -*-

class Model(object):
	
	_attr = {}
	
	def __init__(self):
		
		self._attr[id(self)] = {}

			
	def __setattr__(self, name, value):
		
		if name in self._attr[id(self)]:
			self._attr[id(self)][name] = value
		else:
			self._attr[id(self)].update({name: value})
		return self
	

	def __getattr__(self, name):
		
		if name in self._attr[id(self)]:
			return self._attr[id(self)][name]
		else:
			return False
		
	
