#!/usr/bin/python3

class father:
	def __init__(self, name, age, id, info):
		self._name = name
		self._age = age
		self.__id = id
		self.info = info
		
	def __private(self):
		print("私有方法，外部不可访问")
		
	def print(self):
		print("father %s 说: 我 %d 岁了。" %(self._name,self._age))
		
	def foobar(self):
		print("foo bar ... ")