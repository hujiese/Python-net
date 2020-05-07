[TOC]

# Python3 模块

### 1、import 导入模块

**以src/demo1中的代码为例**，有 func.py模块，其内容如下：

```python
#! /usr/bin/python3

def func1():
	print('func1....')

def func2():
	print('func2....')
	
if __name__ == '__main__':
	print('__main__')
else:
	print('not main')
```

有测试文件test.py，test.py中的内容如下：

```python
#! /usr/bin/python3

import func

if __name__ == '__main__':
	func.func1()
	func.func2()
```

测试代码中直接import func，然后调用func中的func1和func2函数。测试结果如下：

```
not main
func1....
func2....
```

可以看到，执行结果中还打印了 *not main*  当一个模块被导入时，该模块中的全局的一些变量和代码也会被初始化和执行，由于是别的代码导入了 func.py ，所以：

```python
if __name__ == '__main__':
	print('__main__')
else:
	print('not main')
```

这部分代码会执行 else 分支。

### 2、from ... import... 导入模块

**以src/demo2中的代码为例**，func.py 的代码没有任何变化，但是test.py 代码有改动，代码如下：

```python
#! /usr/bin/python3

from func import func1, func2

if __name__ == '__main__':
	func1()
	func2()
```

通过这种方法可以直接使用func中的函数，而不需要向之前那样通过 func.func1() 方式来调用。

### 3、从 package 中导入

**以src/demo3中的代码为例**，demo3中目录结构如下：

```shell
.
├── module
│   ├── func.py
└── test.py

```

其中func.py里面的内容没有任何变化，但是test.py的导入模块方式却不一样了，test.py代码如下：

```python
#! /usr/bin/python3

from module.func import func1, func2

if __name__ == '__main__':
	func1()
	func2()
```

由于func.py在module文件夹下，所以需要使用 **from module.func import func1, func2** 方法来导入模块，当然也可以使用 **import module.func** 方式来导入模块，但是调用func1和func2时就不是很方便，需要用 **module.func.func1()** 这种方式来调用。