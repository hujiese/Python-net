#!/usr/bin/python3

import threading
    
# 创建全局ThreadLocal对象:
local_school = threading.local()
str = '-->'
def process_student():
	global str
	# 获取当前线程关联的student:
	std = local_school.student
	std = std + ' - ' + threading.current_thread().name
	str = str + ' - ' + threading.current_thread().name
	print('Hello, %s (in %s), the string is %s' % (std, threading.current_thread().name, str))

def process_thread(name):
	# 绑定ThreadLocal的student:
	local_school.student = name
	process_student()

def main():
	t1 = threading.Thread(target= process_thread, args=('Jack',), name='Thread-A')
	t2 = threading.Thread(target= process_thread, args=('Mark',), name='Thread-B')
	t1.start()
	t2.start()
	t1.join()
	t2.join()
	
if __name__ == '__main__':
	main()