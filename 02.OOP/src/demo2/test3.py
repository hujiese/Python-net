#!/usr/bin/python3
from extends import son
from base import father
	
if __name__ == '__main__':
	f = father('jack', 50, 50050, 'boss')
	s = son('jackson', 20, 10010, 'student', 96)
	
	print(type(f)) # <class 'base.father'>
	print(type(s)) # <class 'extends.son'>
	
	print(isinstance(s, father)) # True
	
	print(dir(f))
	'''['__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', '_age', '_father__id', '_father__private', '_name', 'foobar', 'info', 'print']
	'''
	print(dir(s))
	'''
	['__class__', '__delattr__', '__dict__', '__dir__', '__doc__', '__eq__', '__format__', '__ge__', '__getattribute__', '__gt__', '__hash__', '__init__', '__le__', '__lt__', '__module__', '__ne__', '__new__', '__reduce__', '__reduce_ex__', '__repr__', '__setattr__', '__sizeof__', '__str__', '__subclasshook__', '__weakref__', '_age', '_father__id', '_father__private', '_name', 'foobar', 'grade', 'info', 'print', 'test_private']
	'''