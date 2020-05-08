#!/usr/bin/python3

import time, threading

# 新线程执行的代码:
def loop():
    print('thread %s is running...' % threading.current_thread().name)
    n = 0
    while n < 3:
        n = n + 1
        print('thread %s >>> %s' % (threading.current_thread().name, n))
        time.sleep(1)
    print('thread %s ended.' % threading.current_thread().name)

if __name__ == '__main__':
	print('thread %s is running...' % threading.current_thread().name)
	t1 = threading.Thread(target=loop, name='LoopThread1')
	t2 = threading.Thread(target=loop, name='LoopThread2')
	
	t1.start()
	t2.start()
	
	t1.join()
	t2.join()
	print('thread %s ended.' % threading.current_thread().name)