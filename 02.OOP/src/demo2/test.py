#!/usr/bin/python3
from extends import son

if __name__ == '__main__':
	s = son('jack', 20, 10010, 'student', 96)
	s.test_private() # jack \n 20 \n student \n 96
	s.print() # son jack 说: 我 20 岁了。
	# 测试父类方法
	s.foobar() # foo bar ...
	
	


 
