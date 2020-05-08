#!/usr/bin/python3
import multiprocessing
import os,time,random

#写数据进程执行的代码
def proc_send(pipe,urls):
	#print 'Process is write....'
	for url in urls:
		time.sleep(random.random())
		print('Process is send :%s' %url)
		pipe.send(url)
        

#读数据进程的代码
def proc_recv(pipe):
    while True:
        print('Process rev:%s' %pipe.recv())

if __name__ == '__main__':
    #父进程创建pipe，并传给各个子进程，duplex设置为True，全双工
    pipe = multiprocessing.Pipe(duplex=True)
    p1 = multiprocessing.Process(target=proc_send,args=(pipe[0],['url_'+str(i) for i in range(5) ]))
    p2 = multiprocessing.Process(target=proc_recv,args=(pipe[1],))
    #启动子进程，写入
    p1.start()
    p2.start()

    p1.join()
    p2.terminate()
