#!/usr/bin/python3

# 导入 socket、sys 模块
import socket
import sys
from multiprocessing import Pool
import os

# 端口
port = 9999
# 缓冲区大小
BUFSIZ = 1024
# 本机地址
host = '127.0.0.1'
# 进程池大小
POOLSIZE = 4
# 子进程要执行的代码
def service(conn, addr):
	print('Run child process %s ...' % (os.getpid()))
	while True: 
		try:
			recvdata = conn.recv(BUFSIZ).decode('utf-8')
		except Exception:
			print('Time out ...')
		# read返回0，说明对方已经关闭连接，服务端处于CLOSE_WAIT状态
		if not recvdata:
			print('client ', addr, ' off line ...')
			break
		else:
			print(os.getpid(), ' receive from ', addr, ' ,data is ', recvdata)
			# 回射回去
			conn.send(recvdata.encode('utf-8'))		
	conn.close()
	print('Exit child process %s ...' % (os.getpid()))
	
def main():
	# 创建 socket 对象
	serversocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM) 

	# 设置地址复用
	serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	# 设置保活时间
	serversocket.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
	serversocket.setsockopt(socket.SOL_TCP, socket.TCP_KEEPIDLE, 2)
	serversocket.setsockopt(socket.SOL_TCP, socket.TCP_KEEPINTVL, 1)
	serversocket.setsockopt(socket.SOL_TCP, socket.TCP_KEEPCNT, 3)
		
	# 绑定端口号
	serversocket.bind((host, port))
	# 设置最大连接数，超过后排队
	serversocket.listen(5)

	p = Pool(POOLSIZE)
	while True:
		# 建立客户端连接
		conn, addr = serversocket.accept()  
		print('connect from:', addr)
		p.apply_async(service, args=(conn, addr,))
		#conn.close() #千万不可调用此句，否则会关闭进程中的连接
					
	serversocket.close()
	p.join()
	p.close()
	
if __name__ == "__main__":
    main()