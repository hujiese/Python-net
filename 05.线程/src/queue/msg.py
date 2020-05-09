#!/usr/bin/python3

import threading
import queue
import time

exitFlag = False

lock = threading.Lock()
workQueue = queue.Queue(10)

def customer():
	global exitFlag
	while not exitFlag:
		#with lock:
		if not workQueue.empty():
			data = workQueue.get()
			print(threading.current_thread().name + ' get ' + data)
			time.sleep(1)
	print('customer ' + threading.current_thread().name + ' end ... ')

def product(nums):
	global exitFlag
	while not exitFlag:
		with lock:
			if workQueue.empty():
				for i in range(nums):
					workQueue.put('product' + str(i))
	print('product end ... ')
			

def main():
	global exitFlag
	threads = []
	# 生产者线程，一次性向队列生产4个消息
	prod = threading.Thread(target= product, args= (4,), name='product')
	prod.start()
	# 创建三个消费者线程
	for i in range(3):
		t = threading.Thread(target= customer, name='Thread-' + str(i))
		threads.append(t)
	# 启动消费者线程
	for t in threads:
		t.start()

	# 等待队列清空
	while not workQueue.empty():
		pass
	# 设置退出flag
	exitFlag = True
	
	prod.join()
	for t in threads:
		t.join()
	
	print ("退出主线程")
	
if __name__ == '__main__':
	main()