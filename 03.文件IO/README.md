<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->


- [文件IO](#%E6%96%87%E4%BB%B6io)
    - [一、文件读写](#%E4%B8%80%E6%96%87%E4%BB%B6%E8%AF%BB%E5%86%99)
      - [1、案例一--普通文本文件拷贝](#1%E6%A1%88%E4%BE%8B%E4%B8%80--%E6%99%AE%E9%80%9A%E6%96%87%E6%9C%AC%E6%96%87%E4%BB%B6%E6%8B%B7%E8%B4%9D)
      - [2、案例二--按行读取文本文件并写入](#2%E6%A1%88%E4%BE%8B%E4%BA%8C--%E6%8C%89%E8%A1%8C%E8%AF%BB%E5%8F%96%E6%96%87%E6%9C%AC%E6%96%87%E4%BB%B6%E5%B9%B6%E5%86%99%E5%85%A5)
      - [3、案例三--拷贝图片](#3%E6%A1%88%E4%BE%8B%E4%B8%89--%E6%8B%B7%E8%B4%9D%E5%9B%BE%E7%89%87)
    - [二、操作文件和目录](#%E4%BA%8C%E6%93%8D%E4%BD%9C%E6%96%87%E4%BB%B6%E5%92%8C%E7%9B%AE%E5%BD%95)
      - [1、系统和环境变量](#1%E7%B3%BB%E7%BB%9F%E5%92%8C%E7%8E%AF%E5%A2%83%E5%8F%98%E9%87%8F)
      - [2、操作文件和目录](#2%E6%93%8D%E4%BD%9C%E6%96%87%E4%BB%B6%E5%92%8C%E7%9B%AE%E5%BD%95)

<!-- END doctoc generated TOC please keep comment here to allow auto update -->

# 文件IO

该部分更多内容可见 [Python3 File(文件) 方法](https://www.runoob.com/python3/python3-file-methods.html)

### 一、文件读写

Python也提供了一系列文件读写函数，这里直接上案例。

文件打开的mode参数如下所示：

| 模式 | 描述                                                         |
| :--: | ------------------------------------------------------------ |
|  t   | 文本模式 (默认)。                                            |
|  x   | 写模式，新建一个文件，如果该文件已存在则会报错。             |
|  b   | 二进制模式。                                                 |
|  +   | 打开一个文件进行更新(可读可写)。                             |
|  U   | 通用换行模式（**Python 3 不支持**）。                        |
|  r   | 以只读方式打开文件。文件的指针将会放在文件的开头。这是默认模式。 |
|  rb  | 以二进制格式打开一个文件用于只读。文件指针将会放在文件的开头。这是默认模式。一般用于非文本文件如图片等。 |
|  r+  | 打开一个文件用于读写。文件指针将会放在文件的开头。           |
| rb+  | 以二进制格式打开一个文件用于读写。文件指针将会放在文件的开头。一般用于非文本文件如图片等。 |
|  w   | 打开一个文件只用于写入。如果该文件已存在则打开文件，并从开头开始编辑，即原有内容会被删除。如果该文件不存在，创建新文件。 |
|  wb  | 以二进制格式打开一个文件只用于写入。如果该文件已存在则打开文件，并从开头开始编辑，即原有内容会被删除。如果该文件不存在，创建新文件。一般用于非文本文件如图片等。 |
|  w+  | 打开一个文件用于读写。如果该文件已存在则打开文件，并从开头开始编辑，即原有内容会被删除。如果该文件不存在，创建新文件。 |
| wb+  | 以二进制格式打开一个文件用于读写。如果该文件已存在则打开文件，并从开头开始编辑，即原有内容会被删除。如果该文件不存在，创建新文件。一般用于非文本文件如图片等。 |
|  a   | 打开一个文件用于追加。如果该文件已存在，文件指针将会放在文件的结尾。也就是说，新的内容将会被写入到已有内容之后。如果该文件不存在，创建新文件进行写入。 |
|  ab  | 以二进制格式打开一个文件用于追加。如果该文件已存在，文件指针将会放在文件的结尾。也就是说，新的内容将会被写入到已有内容之后。如果该文件不存在，创建新文件进行写入。 |
|  a+  | 打开一个文件用于读写。如果该文件已存在，文件指针将会放在文件的结尾。文件打开时会是追加模式。如果该文件不存在，创建新文件用于读写。 |
| ab+  | 以二进制格式打开一个文件用于追加。如果该文件已存在，文件指针将会放在文件的结尾。如果该文件不存在，创建新文件用于读写。 |

#### 1、案例一--普通文本文件拷贝

代码在src/demo1/test.py中，代码如下：

```python
#!/usr/bin/env python3

content = ''
with open('readfile.txt', 'r') as f:
    content = f.read()
    print('open for read...')
    print(content)
	
with open('writefile.txt', 'w') as f:
	f.write(content)
	print('write ok ...')
```

#### 2、案例二--按行读取文本文件并写入

代码在src/demo1/test2.py中，代码如下：

```python
#!/usr/bin/env python3

content = ''
# with open('readfile.txt', 'r', encoding='gbk') as f:
with open('readfile.txt', 'r') as f:
	print('open for read...')
	for line in f.readlines():
		content += line.strip()
		
print(content)

# with open('writefile.txt', 'w', encoding='gbk') as f:
with open('writefile.txt', 'w') as f:
	f.write(content)
	print('write ok ...')
```

#### 3、案例三--拷贝图片

代码在src/demo1/test3.py中，代码如下：

```python
#!/usr/bin/env python3

content = ''
with open('pic.jpg', 'rb') as f:
    content = f.read()
    print('open for read...')
	
with open('write.jpg', 'wb') as f:
	f.write(content)
	print('write ok ...')
```

### 二、操作文件和目录

更多可参考 [Python3 OS 文件/目录方法](https://www.runoob.com/python3/python3-os-file-methods.html)

#### 1、系统和环境变量

测试代码可见src/demo2/os.py，内容和结果如下：

```python
#!/usr/bin/env python3

import os

'''
功能：打印操作系统类型
说明：如果是posix，说明系统是Linux、Unix或Mac OS X，如果是nt，就是Windows系统
测试结果：posix
'''
print(os.name) 

'''
功能：获取详细的系统信息
说明：uname()函数在Windows上不提供，也就是说，os模块的某些函数是跟操作系统相关的
测试结果：
posix.uname_result(sysname='Linux', nodename='jack-virtual-machine', release='4.4.0-31-generic', version='#50~14.04.1-Ubuntu SMP Wed Jul 13 01:07:32 UTC 2016', machine='x86_64')
'''
print(os.uname())

'''
功能：获取操作系统中定义的环境变量
测试结果：
environ({'SESSION': 'ubuntu', 'TEXTDOMAINDIR': '/usr/share/locale/',.......,
'PATH':'/usr/local/java/jdk1.8.0_191/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games', 'WINDOWID': '23068676'})

'''
print(os.environ)

'''
功能：获取某个环境变量的值
测试结果：
/usr/local/java/jdk1.8.0_191/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games
'''
print(os.environ.get('PATH'))
```

#### 2、操作文件和目录

Python的`os`模块封装了操作系统的目录和文件操作，要注意这些函数有的在`os`模块中，有的在`os.path`模块中。直接放案例，案例在src/demo3/dir.py中：

```python
#!/usr/bin/env python3

import os

'''
功能：查看当前目录的绝对路径
测试结果：/mnt/hgfs/vmshared/python_net/03.file/demo3
'''
print(os.path.abspath('.'))

'''
功能：拼接字符串，生成目录完整路径
说明：把两个路径合成一个时，不要直接拼字符串，而要通过os.path.join()函数，这样可以正确处理不同操作系统的路径分隔符
测试结果：./testdir
'''
print(os.path.join('./', 'testdir'))

'''
功能：把一个路径拆分为两部分，后一部分总是最后级别的目录或文件名
测试结果：
.
dir.py
('.', 'dir.py')
'''
path = os.path.split('./dir.py')
print(path[0]) 
print(path[1])
print(path)

'''
功能：得到文件扩展名
测试结果：
./dir
.py
('./dir', '.py')
'''
py = os.path.splitext('./dir.py')
print(py[0]) 
print(py[1])
print(py)

'''
功能：创建一个目录
'''
#os.mkdir('./testdir')

'''
功能：删除一个目录
'''
# os.rmdir('./testdir')

'''
功能：对文件重命名
'''
# os.rename('file.txt', 'file.cpp')

'''
功能：删除一个文件
'''
# os.remove('file.cpp')

'''
功能：列出当前路径下的所有的.py文件
'''
dirs = [x for x in os.listdir('.') if os.path.isdir(x)]
print(dirs)

'''
功能：列出当前路径下的所有目录
'''
pf = [x for x in os.listdir('.') if os.path.isfile(x) and os.path.splitext(x)[1]=='.py']
print(pf)
```

