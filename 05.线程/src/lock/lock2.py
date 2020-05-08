#!/usr/bin/python3

import threading
import time
num = 1
lock = threading.Lock()

def add_num():
	global num
	lock.acquire()
	try:
		num = num + 4
		time.sleep(1)
		print('In %s, the num is %d' % (threading.current_thread().name, num))
	finally:
		# 改完了一定要释放锁:
		lock.release()

def mul_num():
	global num
	lock.acquire()
	try:
		num = num * 4
		print('In %s, the num is %d' % (threading.current_thread().name, num))
	finally:
		# 改完了一定要释放锁:
		lock.release()

def main():
	t1 = threading.Thread(target= add_num, name='Thread-A')
	t2 = threading.Thread(target= mul_num, name='Thread-B')
	t1.start()
	t2.start()
	t1.join()
	t2.join()
	
if __name__ == '__main__':
	main()