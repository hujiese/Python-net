#!/usr/bin/python3
from extends import son
from base import father

def print(father):
	father.print()
	
if __name__ == '__main__':
	f = father('jack', 50, 50050, 'boss')
	s = son('jackson', 20, 10010, 'student', 96)
	
	print(f) # father jack 说: 我 50 岁了。
	print(s) # son jackson 说: 我 20 岁了。
	
	f = s
	f.print() # son jackson 说: 我 20 岁了。