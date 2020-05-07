#!/usr/bin/python3

#类定义
class person:
	#定义基本属性
	weight = 0
	#定义私有属性,私有属性在类外部无法直接进行访问
	__name = ''
	__age = 0
	#定义构造函数
	def __init__(self,n,a,w):
		self.weight = w
		self.__name = n
		self.__age = a
		
	def setName(self, name):
		self.__name = name
		
	def getName(self):
		return self.__name
		
	def setAge(self, age):
		self.__age = age;
		
	def getAge(self):
		return self.__age
		
	def __private(self):
		print("私有方法，外部不可访问")
		
	def call_private_func(self):
		print("间接调用私有方法")
		self.__private()
		
	# 定义普通成员函数，可以被外部调用
	def speak(self):
		print("%s 说: 我 %d 岁。" %(self.__name,self.__age))
	