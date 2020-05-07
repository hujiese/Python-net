<!-- START doctoc generated TOC please keep comment here to allow auto update -->
<!-- DON'T EDIT THIS SECTION, INSTEAD RE-RUN doctoc TO UPDATE -->

- [文件IO](#%E6%96%87%E4%BB%B6io)
    - [一、文件读写](#%E4%B8%80%E6%96%87%E4%BB%B6%E8%AF%BB%E5%86%99)
      - [1、案例一--普通文本文件拷贝](#1%E6%A1%88%E4%BE%8B%E4%B8%80--%E6%99%AE%E9%80%9A%E6%96%87%E6%9C%AC%E6%96%87%E4%BB%B6%E6%8B%B7%E8%B4%9D)
      - [2、案例二--按行读取文本文件并写入](#2%E6%A1%88%E4%BE%8B%E4%BA%8C--%E6%8C%89%E8%A1%8C%E8%AF%BB%E5%8F%96%E6%96%87%E6%9C%AC%E6%96%87%E4%BB%B6%E5%B9%B6%E5%86%99%E5%85%A5)
      - [3、案例三--拷贝图片](#3%E6%A1%88%E4%BE%8B%E4%B8%89--%E6%8B%B7%E8%B4%9D%E5%9B%BE%E7%89%87)

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



