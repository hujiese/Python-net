#!/usr/bin/python3

import subprocess

r = subprocess.call('ps -aux|grep python', shell=True)

print('---------------')

r2 = subprocess.call(['ls', '-l'])

print('---------------')

r3 = subprocess.Popen(['ping','-c','4','www.baidu.com'])
r3.wait() # 让父进程等待子进程完成