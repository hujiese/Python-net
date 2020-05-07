<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->

- [进程](#%E8%BF%9B%E7%A8%8B)
    - [一、fork 系统调用](#%E4%B8%80fork-%E7%B3%BB%E7%BB%9F%E8%B0%83%E7%94%A8)
    - [二、multiprocessing](#%E4%BA%8Cmultiprocessing)
    - [三、进程池](#%E4%B8%89%E8%BF%9B%E7%A8%8B%E6%B1%A0)
    - [四、subprocess](#%E5%9B%9Bsubprocess)
    - [五、进程间通信](#%E4%BA%94%E8%BF%9B%E7%A8%8B%E9%97%B4%E9%80%9A%E4%BF%A1)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

# 进程

参考 [多进程](https://www.liaoxuefeng.com/wiki/1016959663602400/1017628290184064)

### 一、fork 系统调用

在linux/unix中可以通过fork来创建一个子进程，同样地，python也提供了这样的一个函数，测试代码见src/demo1/fork.py：

```python
#!/usr/bin/python3

import os

print('Process (%s) start...' % os.getpid())
# Only works on Unix/Linux/Mac:
pid = os.fork()
if pid == 0:
    print('I am child process (%s) and my parent is %s.' % (os.getpid(), os.getppid()))
else:
    print('I (%s) just created a child process (%s).' % (os.getpid(), pid))
```

测试结果如下：

```
Process (55857) start...
I (55857) just created a child process (55858).
I am child process (55858) and my parent is 55857.
```

使用fork方法来创建进程只能在UNIX/Linux系统中使用，无法在Windows下使用。

### 二、multiprocessing

为了达到跨平台的目的，python也提供了`multiprocessing`模块来解决这个问题。`multiprocessing`模块提供了一个`Process`类来代表一个进程对象。测试代码在src/demo2/multipro.py，代码如下：

```python
#!/usr/bin/python3

from multiprocessing import Process
import os

# 子进程要执行的代码
def run_proc(name):
    print('Run child process %s (%s)...' % (name, os.getpid()))

if __name__=='__main__':
    print('Parent process %s.' % os.getpid())
    p = Process(target=run_proc, args=('test',))
    print('Child process will start.')
    p.start()
    p.join()
    print('Child process end.')
```

测试结果如下：

```
Parent process 55884.
Child process will start.
Run child process test (55885)...
Child process end.
```

操作方法有点像C++11中的Thread类。创建子进程时，只需要传入一个执行函数和函数的参数，创建一个`Process`实例，用`start()`方法启动，这样创建进程比`fork()`还要简单。`join()`方法可以等待子进程结束后再继续往下运行，通常用于进程间的同步。

### 三、进程池

直接上代码：

```python
#!/usr/bin/python3

from multiprocessing import Pool
import os, time, random

def long_time_task(name):
    print('Run task %s (%s)...' % (name, os.getpid()))
    start = time.time()
    time.sleep(random.random() * 3)
    end = time.time()
    print('Task %s runs %0.2f seconds.' % (name, (end - start)))

if __name__=='__main__':
    print('Parent process %s.' % os.getpid())
    p = Pool(4)
    for i in range(5):
        p.apply_async(long_time_task, args=(i,))
    print('Waiting for all subprocesses done...')
    p.close()
    p.join()
    print('All subprocesses done.')
```

测试结果不唯一，其中一个如下所示：

```
Parent process 55917.
Waiting for all subprocesses done...
Run task 0 (55919)...
Run task 1 (55920)...
Run task 2 (55921)...
Run task 3 (55918)...
Task 3 runs 0.28 seconds.
Run task 4 (55918)...
Task 1 runs 0.35 seconds.
Task 4 runs 1.15 seconds.
Task 0 runs 2.59 seconds.
Task 2 runs 2.92 seconds.
All subprocesses done.
```

### 四、subprocess

这个subprocess有点像linux里的exec函数簇，可以执行一个程序映像，并支持传入程序映像所需的命令行参数。直接上代码，代码可见src/demo2/subpro.py，具体代码如下：

```python
#!/usr/bin/python3

import subprocess

r = subprocess.call('ps -aux|grep python', shell=True)

print('---------------')

r2 = subprocess.call(['ls', '-l'])

print('---------------')

r3 = subprocess.Popen(['ping','-c','4','www.baidu.com'])
r3.wait() # 让父进程等待子进程完成
```

执行结果如下：

```shell
jack      54392  0.0  2.8 835628 57992 ?        Sl   11:17   0:26 /usr/bin/python /usr/bin/terminator
jack      56041  0.0  0.4  32560  9448 pts/0    S+   21:37   0:00 /usr/bin/python3 ./subpro.py
jack      56042  0.0  0.0   4448   780 pts/0    S+   21:37   0:00 /bin/sh -c ps -aux|grep python
jack      56044  0.0  0.1  15944  2564 pts/0    S+   21:37   0:00 grep python
---------------
total 2
-rwxrwxrwx 1 root root 399  5月  7 20:52 multipro.py
-rwxrwxrwx 1 root root 578  5月  7 21:06 propool.py
drwxrwxrwx 1 root root   0  5月  7 20:46 __pycache__
-rwxrwxrwx 1 root root 249  5月  7 21:37 subpro.py
---------------
PING www.a.shifen.com (36.152.44.95) 56(84) bytes of data.
64 bytes from localhost (36.152.44.95): icmp_seq=1 ttl=128 time=26.6 ms
64 bytes from localhost (36.152.44.95): icmp_seq=2 ttl=128 time=22.1 ms
64 bytes from localhost (36.152.44.95): icmp_seq=3 ttl=128 time=24.0 ms
64 bytes from localhost (36.152.44.95): icmp_seq=4 ttl=128 time=22.9 ms

--- www.a.shifen.com ping statistics ---
4 packets transmitted, 4 received, 0% packet loss, time 3005ms
rtt min/avg/max/mdev = 22.181/23.969/26.632/1.683 ms
```

### 五、进程间通信

Python的`multiprocessing`模块包装了底层的机制，提供了`Queue`、`Pipes`等多种方式来交换数据。下面以`Queue`为例，在父进程中创建两个子进程，一个往`Queue`里写数据，一个从`Queue`里读数据，代码在src/demo2/commu.py中：

```python
#!/usr/bin/python3

from multiprocessing import Process, Queue
import os, time, random

# 写数据进程执行的代码:
def write(q):
    print('Process to write: %s' % os.getpid())
    for value in ['A', 'B', 'C']:
        print('Put %s to queue...' % value)
        q.put(value)
        time.sleep(random.random())

# 读数据进程执行的代码:
def read(q):
    print('Process to read: %s' % os.getpid())
    while True:
        value = q.get(True)
        print('Get %s from queue.' % value)

if __name__=='__main__':
    # 父进程创建Queue，并传给各个子进程：
    q = Queue()
    pw = Process(target=write, args=(q,))
    pr = Process(target=read, args=(q,))
    # 启动子进程pw，写入:
    pw.start()
    # 启动子进程pr，读取:
    pr.start()
    # 等待pw结束:
    pw.join()
    # pr进程里是死循环，无法等待其结束，只能强行终止:
    pr.terminate()
```

输出结果如下：

```
Process to write: 56081
Put A to queue...
Process to read: 56082
Get A from queue.
Put B to queue...
Get B from queue.
Put C to queue...
Get C from queue.
```

