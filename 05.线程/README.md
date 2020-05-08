<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->


- [线程](#%E7%BA%BF%E7%A8%8B)
    - [一、全局解释器锁](#%E4%B8%80%E5%85%A8%E5%B1%80%E8%A7%A3%E9%87%8A%E5%99%A8%E9%94%81)
    - [二、_thread](#%E4%BA%8C_thread)
    - [三、threading](#%E4%B8%89threading)
      - [1、创建线程](#1%E5%88%9B%E5%BB%BA%E7%BA%BF%E7%A8%8B)
        - [（1）传递函数](#1%E4%BC%A0%E9%80%92%E5%87%BD%E6%95%B0)
        - [（2）继承线程类](#2%E7%BB%A7%E6%89%BF%E7%BA%BF%E7%A8%8B%E7%B1%BB)
      - [2、ThreadLocal](#2threadlocal)
    - [四、线程同步](#%E5%9B%9B%E7%BA%BF%E7%A8%8B%E5%90%8C%E6%AD%A5)
      - [1、互斥锁](#1%E4%BA%92%E6%96%A5%E9%94%81)
      - [2、条件变量](#2%E6%9D%A1%E4%BB%B6%E5%8F%98%E9%87%8F)
      - [3、信号量](#3%E4%BF%A1%E5%8F%B7%E9%87%8F)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

# 线程

Python 提供了多个模块来支持多线程编程，包括 `thread、threading 和 Queue` 模块等。程
序是可以使用 thread 和 threading 模块来创建与管理线程。thread 模块提供了基本的线程和锁
定支持；而 threading 模块提供了更高级别、功能更全面的线程管理。使用 Queue 模块，用户
可以创建一个队列数据结构，用于在多线程之间进行共享。

### 一、全局解释器锁

`该部分来自《Python 核心编程 第三版》4.3.1节。`

Python 代码的执行是由 Python 虚拟机（又名解释器主循环）进行控制的。Python 在设计时是这样考虑的，在主循环中同时只能有一个控制线程在执行，就像单核 CPU 系统中的多进程一样。内存中可以有许多程序，但是在任意给定时刻只能有一个程序在运行。同理，**尽管 Python 解释器中可以运行多个线程，但是在任意给定时刻只有一个线程会被解释器执行**。

对 Python 虚拟机的访问是由全局解释器锁（GIL）控制的。这个锁就是用来保证同时只能有一个线程运行的。在多线程环境中，Python 虚拟机将按照下面所述的方式执行：
	1、设置 GIL。
	2、切换进一个线程去运行。
	3、执行下面操作之一。
		a、指定数量的字节码指令。
		b、线程主动让出控制权（可以调用 time.sleep(0)来完成）。
	4、把线程设置回睡眠状态（切换出线程）。
	5、解锁 GIL。
	6、重复上述步骤。
当调用外部代码（即，任意 C/C++扩展的内置函数）时，GIL 会保持锁定，直至函数执行结束（因为在这期间没有 Python 字节码计数）。编写扩展函数的程序员有能力解锁 GIL，然而，作为 Python 开发者，你并不需要担心 Python 代码会在这些情况下被锁住。例如，对于任意面向 I/O 的 Python 例程（调用了内置的操作系统 C 代码的那种），GIL 会在 I/O 调用前被释放，以允许其他线程在 I/O 执行的时候运行。而对于那些没有太多 I/O 操作的代码而言，更倾向于在该线程整个时间片内始终占有处理器（和 GIL）。换句话说就是，**I/O 密集型的 Python 程序要比计算密集型的代码能够更好地利用多线程环境**。

### 二、_thread

thread 模块已被废弃。用户可以使用 threading 模块代替。所以，在 Python3 中不能再使用"thread" 模块。为了兼容性，Python3 将 thread 重命名为 "_thread"。

_thread 提供了低级别的、原始的线程以及一个简单的锁，它相比于 threading 模块的功能还是比较有限的，所以不推荐使用。这里还是展示一个案例，该案例在src/\_thread/thread.py中：

```python
#!/usr/bin/python3

import _thread
import time

# 为线程定义一个函数
def print_time(threadName, delay):
   count = 0
   while count < 5:
      time.sleep(delay)
      count += 1
      print ("%s: %s" % ( threadName, time.ctime(time.time()) ))

# 创建两个线程
try:
   _thread.start_new_thread( print_time, ("Thread-1", 2, ) )
   _thread.start_new_thread( print_time, ("Thread-2", 4, ) )
except:
   print ("Error: 无法启动线程")

while 1:
   pass
```

执行结果如下：

```shell
Thread-1: Fri May  8 15:55:35 2020
Thread-1: Fri May  8 15:55:37 2020
Thread-2: Fri May  8 15:55:37 2020
Thread-1: Fri May  8 15:55:39 2020
Thread-2: Fri May  8 15:55:41 2020
Thread-1: Fri May  8 15:55:41 2020
Thread-1: Fri May  8 15:55:43 2020
Thread-2: Fri May  8 15:55:45 2020
Thread-2: Fri May  8 15:55:49 2020
Thread-2: Fri May  8 15:55:53 2020


^CTraceback (most recent call last):
  File "./thread.py", line 22, in <module>
    pass
KeyboardInterrupt
```

直接ctrl+c退出。

### 三、threading

现在介绍更高级别的 threading 模块。除了 Thread 类以外，该模块还包括许多同步机制：

| 对 象            | 描 述                                                        |
| ---------------- | ------------------------------------------------------------ |
| Thread           | 表示一个执行线程的对象                                       |
| Lock             | 锁原语对象（和 thread 模块中的锁一样）                       |
| RLock            | 可重入锁对象，使单一线程可以（再次）获得已持有的锁（递归锁） |
| Condition        | 条件变量对象，使得一个线程等待另一个线程满足特定的“条件”，比如改变状态或某个数据值 |
| Event            | 条件变量的通用版本，任意数量的线程等待某个事件的发生，在该事件发生后所有线程将被激活 |
| Semaphore        | 为线程间共享的有限资源提供了一个“计数器”，如果没有可用资源时会被阻塞 |
| BoundedSemaphore | 与 Semaphore 相似，不过它不允许超过初始值                    |
| Timer            | 与 Thread 相似，不过它要在运行前等待一段时间                 |
| Barrier          | 创建一个“障碍”，必须达到指定数量的线程后才可以继续           |

#### 1、创建线程

threading 模块的 Thread 类是主要的执行对象。它有 thread 模块中没有的很多函数。

使用 Thread 类，可以有很多方法来创建线程。这里有三种方法，但第一个方法很方便，第二个方法不推荐使用，这里最推荐第三种方法：
•  创建 Thread 的实例，传给它一个函数。
•  创建 Thread 的实例，传给它一个可调用的类实例。
•  派生 Thread 的子类，并创建子类的实例。

##### （1）传递函数

源码可见/src/threading/fun_thread.py：

```python
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
```

程序中创建了两个线程，都执行loop函数。执行结果如下：

```
thread MainThread is running...
thread LoopThread1 is running...
thread LoopThread1 >>> 1
thread LoopThread2 is running...
thread LoopThread2 >>> 1
thread LoopThread1 >>> 2
thread LoopThread2 >>> 2
thread LoopThread1 >>> 3
thread LoopThread2 >>> 3
thread LoopThread1 ended.
thread LoopThread2 ended.
thread MainThread ended.
```

##### （2）继承线程类

该部分代码可见/src/threading/class_thread.py：

```python
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
```

myThread非常简单，就是继承threading.Thread类，并重写run方法。执行结果如下：

```shell
start loop t1 at: Fri May  8 16:44:36 2020
start loop t2 at: Fri May  8 16:44:36 2020
loop t1 done at: Fri May  8 16:44:37 2020
loop t2 done at: Fri May  8 16:44:38 2020
退出主线程
```

#### 2、ThreadLocal

在多线程环境下，每个线程都有自己的数据，这些数据往往都不相同，都是局部的数据。对于全局的数据，每个线程都能访问和修改，这就不安全了，ThreadLocal这种方法可以让让每个线程拥有一份全局定义的数据，这份数据每个线程都是私有的，但外部看却是全局的。

在Linux中对于POD数据，可以采用`__thread`修饰，对于class类型数据，可以使用`pthread_setspecific`和`pthread_getspecific`两个函数结合`pthread_key_t` 变量来通过类似于key-value方法设置/获取线程私有数据。

当然，Python中也提供类似的功能，测试代码可见src/threading/threadlocal.py，代码如下所示：

```python
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
```

这里通过 `local_school = threading.local()`来定义一个ThreadLocal变量，为了对比，这里也定义了str变量。测试结果如下：

```
Hello, Jack - Thread-A (in Thread-A), the string is --> - Thread-A
Hello, Mark - Thread-B (in Thread-B), the string is --> - Thread-A - Thread-B
```

从结果中可以看到，local_school.student变量是每个线程独享的，而全局的str变量则先后被两个线程修改过。

### 四、线程同步

#### 1、互斥锁

直接看案例，这是个反面案例，线程不同步所造成的 src/lock/lock.py：

```python
#!/usr/bin/python3

import threading
import time
num = 1

def add_num():
	global num
	num = num + 4
	time.sleep(1)
	print('In %s, the num is %d' % (threading.current_thread().name, num))

def mul_num():
	global num
	num = num * 4
	print('In %s, the num is %d' % (threading.current_thread().name, num))
	
def main():
	t1 = threading.Thread(target= add_num, name='Thread-A')
	t2 = threading.Thread(target= mul_num, name='Thread-B')
	t1.start()
	t2.start()
	t1.join()
	t2.join()
	
if __name__ == '__main__':
	main()
```

上面的程序创建了两个线程，一个线程对全局变量num进行加四操作，另一个做乘四操作，值得注意的是，在add_num函数中加四之后还sleep了一段时间，用于模拟该线程在做其他事情，这时mul_num的线程抢占num资源并修改，从而导致线程不同步输出不是预期的效果，下面是输出结果：

```
In Thread-B, the num is 20
In Thread-A, the num is 20
```

一种预期结果是，在A线程中num的值是5，而B线程中的值为20。但是在add_num中，num值变成5后就sleep了，CPU执行权被让出（当然即使不sleep该过程也可能会被其他线程打断，让出CPU执行权），mul_num线程执行，将num值乘以4，得到20。当A线程重新获取CPU执行权之后num值已经是20了。

所以对于线程的共享变量，需要一种同步机制，互斥锁是一个很典型的方法，下面直接看如何使用互斥锁解决这个问题，代码可见 src/lock/lock2.py：

```python
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
```

在修改/获取 num值的区间使用互斥锁保护，输出结果如下：

```
In Thread-A, the num is 5
In Thread-B, the num is 20
```

这次就正常了。

但是使用互斥锁老是要获取和释放锁，获取还好，很多人总是忘记了释放，在C++11里有lock_guard和unique_lock方便使用，muduo网络库中也封装了一个MutexLockGuard类。同样地，python中可以使用with关键字来达成相同目的 src/lock/lock3.py：

```python
#!/usr/bin/python3

import threading
import time
num = 1
lock = threading.Lock()

def add_num():
	global num
	with lock:
		num = num + 4
		time.sleep(1)
		print('In %s, the num is %d' % (threading.current_thread().name, num))

def mul_num():
	global num
	with lock:
		num = num * 4
		print('In %s, the num is %d' % (threading.current_thread().name, num))

def main():
	t1 = threading.Thread(target= add_num, name='Thread-A')
	t2 = threading.Thread(target= mul_num, name='Thread-B')
	t1.start()
	t2.start()
	t1.join()
	t2.join()
	
if __name__ == '__main__':
	main()
```

输出结果：

```
In Thread-A, the num is 5
In Thread-B, the num is 20
```

#### 2、条件变量

互斥锁是最简单的线程同步机制，Python提供的Condition对象提供了对复杂线程同步问题的支持。Condition被称为条件变量，除了提供与Lock类似的acquire和release方法外，还提供了wait和notify方法。线程首先acquire一个条件变量，然后判断一些条件。如果条件不满足则wait；如果条件满足，进行一些处理改变条件后，通过notify方法通知其他线程，其他处于wait状态的线程接到通知后会重新判断条件。不断的重复这一过程，从而解决复杂的同步问题。

可以认为Condition对象维护了一个锁（Lock/RLock)和一个waiting池。线程通过acquire获得Condition对象，当调用wait方法时，线程会释放Condition内部的锁并进入blocked状态，同时在waiting池中记录这个线程。当调用notify方法时，Condition对象会从waiting池中挑选一个线程，通知其调用acquire方法尝试取到锁。

**Condition对象的构造函数可以接受一个Lock/RLock对象作为参数，如果没有指定，则Condition对象会在内部自行创建一个RLock。除了notify方法外，Condition对象还提供了notifyAll方法，可以通知waiting池中的所有线程尝试acquire内部锁。**由于上述机制，处于waiting状态的线程只能通过notify方法唤醒，所以notifyAll的作用在于防止有线程永远处于沉默状态。

下面是一道经典的面试题，循环打印AABBAABB....，可以使用条件变量来完成需求，代码可见src/cond/cond.py：

```python
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
```

打印结果如下：

```
AA
BB
AA
BB
AA
BB
...
```



#### 3、信号量

可用于解决生产者消费者问题，直接上代码src/sem/sem.py：

```python
#!/usr/bin/python3

# 信号量解决生产者消费者问题
import random
import threading
import time
 
# 声明信号量
sema=threading.Semaphore(0)# 必须写参数， 0表示当前无可以使用数
# sema2=threading.BoundedSemaphore(1); # 使用budedsemaphore时候不允许设置初始为0，将会抛出异常
 
apple=0
 
def product():#生产者
	global apple
	time.sleep(3)
	apple=random.randint(1,100)
	print("生成苹果:",apple)
	sema.release();#+ 1 解除消费者阻塞
	
def consumer():
	print("等待")
	sema.acquire()# -1 阻塞等待信号量可用
	print("消费：",apple)

def main():
	t1=threading.Thread(target=consumer)
	t2=threading.Thread(target=product)

	t1.start()
	t2.start()

	t1.join()
	t2.join()

if __name__ == '__main__':
	main()
```

需要注意的是：

1、调用relarse(）信号量会+1，调用 acquire() 信号量会-1，这个可以理解为对于临界资源的使用，以及进入临界区的判断条件。

2、boudedsemphore()：边界信号量，当调用relarse() 会+1 , 并且会检查信号量的上限情况。不允许超过上限。使用budedsemaphore时候不允许设置初始为0，将会抛出异常。所以至少设置为1 ，如consumer product 时候应该在外设置一个变量，启动时候对变量做判断。

输出结果如下：

```
等待
生成苹果: 58
消费： 58
```



