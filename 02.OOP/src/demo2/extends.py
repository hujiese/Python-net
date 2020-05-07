from base import father

class son(father):
	def __init__(self, name, age, id, info, grade):
	    # 调用父类构造函数
		father.__init__(self, name, age, id, info)
		self.grade = grade
		
	def test_private(self):
		print(self._name)
		print(self._age)
		# print(self.__id) # 父类私有变量不可调用
		print(self.info)
		print(self.grade)
		# self.__private() # 父类私有方法不可调用
		
	# 重写父类方法
	def print(self):
		print("son %s 说: 我 %d 岁了。" %(self._name,self._age))	
	
		