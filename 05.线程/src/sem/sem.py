#!/usr/bin/python3

# 信号量解决生产者消费者问题
import random;
import threading;
import time;
 
# 声明信号量
sema=threading.Semaphore(0);# 必须写参数， 0表示当前无可以使用数
# sema2=threading.BoundedSemaphore(1); # 使用budedsemaphore时候不允许设置初始为0，将会抛出异常
 
apple=0;
 
def product():#生产者
	global apple;
	time.sleep(3);
	apple=random.randint(1,100);
	print("生成苹果:",apple);
	sema.release();#+ 1 解除消费者阻塞
	
def consumer():
	print("等待");
	sema.acquire();# -1 阻塞等待信号量可用
	print("消费：",apple);

def main():
	t1=threading.Thread(target=consumer);
	t2=threading.Thread(target=product);

	t1.start();
	t2.start();

	t1.join();
	t2.join();

if __name__ == '__main__':
	main()