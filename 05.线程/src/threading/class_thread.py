#!/usr/bin/python3

import threading
from time import sleep, ctime

class myThread (threading.Thread):
	def __init__(self, func, args, name = ''):
		threading.Thread.__init__(self)
		self.func = func
		self.name = name
		self.args = args

	def run(self):
		self.func(*self.args)

def loop(delay, num):
	print('start loop', num, 'at:', ctime())
	sleep(delay)
	print('loop', num, 'done at:', ctime())
	
def main():
	# 创建新线程
	thread1 = myThread(loop, (1, 't1'), 'thread1')
	thread2 = myThread(loop, (2, 't2'), 'thread1')

	# 开启新线程
	thread1.start()
	thread2.start()
	thread1.join()
	thread2.join()
	print ("退出主线程")

if __name__ == '__main__':
	main()