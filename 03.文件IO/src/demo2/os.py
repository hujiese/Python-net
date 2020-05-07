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
