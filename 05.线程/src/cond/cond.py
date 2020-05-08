#!/usr/bin/python3

# 信号量解决生产者消费者问题
import random;
import threading;
import time;
 
# 声明条件量
con = threading.Condition()
 
flag = False;
 
def product():#生产者
	global flag
	while True:
		if con.acquire(): # 内部加锁
			time.sleep(1);
			if flag == False:
				flag = True
				print("AA")
			con.notify() # 通知解除阻塞
			con.release() # 释放锁
	
def consumer():
	global flag
	while True:
		if con.acquire(): # 内部加锁
			while flag == False:
				con.wait() # 解锁，阻塞
			print("BB")
			flag = False
		con.release() # 释放锁

def main():
	t1=threading.Thread(target=consumer);
	t2=threading.Thread(target=product);

	t1.start();
	t2.start();

	t1.join();
	t2.join();

if __name__ == '__main__':
	main()