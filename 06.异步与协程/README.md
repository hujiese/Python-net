<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->

- [异步IO](#%E5%BC%82%E6%AD%A5io)
    - [1、协程](#1%E5%8D%8F%E7%A8%8B)
    - [2、async](#2async)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

# 异步IO

参考 [异步IO](https://www.liaoxuefeng.com/wiki/1016959663602400/1017959540289152)  [python多任务—协程（一）](https://blog.csdn.net/weixin_41599977/article/details/93656042)

协程，又称为微线程，它是实现多任务的另一种方式，只不过是比线程更小的执行单元。因为它自带CPU的上下文，这样只要在合适的时机，我们可以把一个协程切换到另一个协程。

从宏观上看就是一个在一个线程里交替执行一些任务，而切换都是在线程里进行的，代价比线程和进程小得多。

### 1、协程

要切换任务，python提供了yield来实现，代码可见src/yield.py：

```python
#!/usr/bin/python3
import time

def task_1():
    while True:
        print("--This is task 1!--before")
        yield
        print("--This is task 1!--after")
        time.sleep(0.5)

def task_2():
    while True:
        print("--This is task 2!--before")
        yield
        print("--This is task 2!--after")
        time.sleep(0.5)
        
if __name__ == "__main__":
    t1 = task_1()  # 生成器对象
    t2 = task_2()
    # print(t1, t2)
    while True:
        next(t1)  # 1、唤醒生成器t1，执行到yield后，保存上下文，挂起任务；下次再次唤醒之后，从yield继续往下执行
        print("\nThe main thread!\n")  # 2、继续往下执行
        next(t2)  # 3、唤醒生成器t2，....
```

运行结果如下：

```
--This is task 1!--before

The main thread!

--This is task 2!--before
--This is task 1!--after
--This is task 1!--before

The main thread!

--This is task 2!--after
--This is task 2!--before
--This is task 1!--after
--This is task 1!--before

The main thread!

--This is task 2!--after
--This is task 2!--before
--This is task 1!--after
--This is task 1!--before
...

```

### 2、async

`asyncio`是Python 3.4版本引入的标准库，直接内置了对异步IO的支持。`asyncio`的编程模型就是一个消息循环。我们从`asyncio`模块中直接获取一个`EventLoop`的引用，然后把需要执行的协程扔到`EventLoop`中执行，就实现了异步IO。

直接看一个案例src/async.py：

```python
#!/usr/bin/python3

import threading
import asyncio

@asyncio.coroutine
def task_1():
    while True:
        print("--This is task 1!--before %s"  %(threading.currentThread()))
        yield from asyncio.sleep(1)
        print("--This is task 1!--after %s"  %(threading.currentThread()))

@asyncio.coroutine
def task_2():
    while True:
        print("--This is task 2!--before %s"  %(threading.currentThread()))
        yield from asyncio.sleep(1)
        print("--This is task 2!--after %s"  %(threading.currentThread()))

if __name__ == "__main__":
	loop = asyncio.get_event_loop()
	tasks = [task_1(), task_2()]
	loop.run_until_complete(asyncio.wait(tasks))
	loop.close()
```

输出结果如下：

```
--This is task 1!--before <_MainThread(MainThread, started 140414068295488)>
--This is task 2!--before <_MainThread(MainThread, started 140414068295488)>
--This is task 1!--after <_MainThread(MainThread, started 140414068295488)>
--This is task 1!--before <_MainThread(MainThread, started 140414068295488)>
--This is task 2!--after <_MainThread(MainThread, started 140414068295488)>
--This is task 2!--before <_MainThread(MainThread, started 140414068295488)>
--This is task 1!--after <_MainThread(MainThread, started 140414068295488)>
--This is task 1!--before <_MainThread(MainThread, started 140414068295488)>
--This is task 2!--after <_MainThread(MainThread, started 140414068295488)>
--This is task 2!--before <_MainThread(MainThread, started 140414068295488)>
...
```

用`asyncio`提供的`@asyncio.coroutine`可以把一个generator标记为coroutine类型，然后在coroutine内部用`yield from`调用另一个coroutine实现异步操作。

为了简化并更好地标识异步IO，从Python 3.5开始引入了新的语法`async`和`await`，可以让coroutine的代码更简洁易读。

请注意，`async`和`await`是针对coroutine的新语法，要使用新的语法，只需要做两步简单的替换：

1. 把`@asyncio.coroutine`替换为`async`；
2. 把`yield from`替换为`await`。

**注意：新语法只能用在Python 3.5以及后续版本，如果使用3.4版本，则仍需使用前面的方案。**

上面代码通过这种方法重写后 src/async2.py：

```python
#!/usr/bin/python3

import threading
import asyncio

async def task_1():
    while True:
        print("--This is task 1!--before %s"  %(threading.currentThread()))
        await asyncio.sleep(1)
        print("--This is task 1!--after %s"  %(threading.currentThread()))

async def task_2():
    while True:
        print("--This is task 2!--before %s"  %(threading.currentThread()))
        await asyncio.sleep(1)
        print("--This is task 2!--after %s"  %(threading.currentThread()))

if __name__ == "__main__":
	loop = asyncio.get_event_loop()
	tasks = [task_1(), task_2()]
	loop.run_until_complete(asyncio.wait(tasks))
	loop.close()
```

效果和前面的方法是一样的。