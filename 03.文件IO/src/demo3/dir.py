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
